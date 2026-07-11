#!/usr/bin/env python3
"""Validate DUO COCO annotations and prepare deterministic YOLO metadata."""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path


CLASS_NAMES = ["holothurian", "echinus", "scallop", "starfish"]
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATASET_ROOT = PROJECT_ROOT / "dataset" / "DUO"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert DUO COCO boxes to YOLO and create train/val/test lists."
    )
    parser.add_argument("--dataset-root", type=Path, default=DEFAULT_DATASET_ROOT)
    parser.add_argument("--val-ratio", type=float, default=0.15)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def load_coco(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"COCO annotation file not found: {path}")
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    for key in ("images", "annotations", "categories"):
        if key not in data or not isinstance(data[key], list):
            raise ValueError(f"{path} is missing a list field: {key}")
    return data


def category_mapping(coco: dict, source: Path) -> dict[int, int]:
    by_name = {item["name"]: int(item["id"]) for item in coco["categories"]}
    if set(by_name) != set(CLASS_NAMES):
        raise ValueError(
            f"Unexpected categories in {source}: {sorted(by_name)}; "
            f"expected {CLASS_NAMES}"
        )
    return {by_name[name]: index for index, name in enumerate(CLASS_NAMES)}


def convert_split(
    coco: dict,
    source_json: Path,
    image_dir: Path,
    label_dir: Path,
) -> tuple[dict[int, dict], dict[int, Counter], Counter]:
    mapping = category_mapping(coco, source_json)
    images = {int(item["id"]): item for item in coco["images"]}
    annotations_by_image: dict[int, list[dict]] = defaultdict(list)
    class_counts: Counter = Counter()
    invalid_counts: Counter = Counter()

    for annotation in coco["annotations"]:
        image_id = int(annotation["image_id"])
        if image_id not in images:
            invalid_counts["unknown_image_id"] += 1
            continue
        category_id = int(annotation["category_id"])
        if category_id not in mapping:
            invalid_counts["unknown_category_id"] += 1
            continue
        annotations_by_image[image_id].append(annotation)

    label_dir.mkdir(parents=True, exist_ok=True)
    image_class_counts: dict[int, Counter] = {}
    missing_images: list[str] = []

    for image_id, image in images.items():
        file_name = Path(image["file_name"]).name
        image_path = image_dir / file_name
        if not image_path.is_file():
            missing_images.append(file_name)

        width, height = float(image["width"]), float(image["height"])
        if width <= 0 or height <= 0:
            raise ValueError(f"Invalid image dimensions for {file_name}: {width}x{height}")

        lines: list[str] = []
        per_image: Counter = Counter()
        for annotation in annotations_by_image.get(image_id, []):
            x, y, box_width, box_height = map(float, annotation["bbox"])
            x1, y1 = max(0.0, x), max(0.0, y)
            x2, y2 = min(width, x + box_width), min(height, y + box_height)
            if x2 <= x1 or y2 <= y1:
                invalid_counts["invalid_bbox"] += 1
                continue
            if (x1, y1, x2 - x1, y2 - y1) != (x, y, box_width, box_height):
                invalid_counts["clipped_bbox"] += 1

            class_id = mapping[int(annotation["category_id"])]
            center_x = ((x1 + x2) / 2.0) / width
            center_y = ((y1 + y2) / 2.0) / height
            normalized_width = (x2 - x1) / width
            normalized_height = (y2 - y1) / height
            lines.append(
                f"{class_id} {center_x:.8f} {center_y:.8f} "
                f"{normalized_width:.8f} {normalized_height:.8f}"
            )
            per_image[class_id] += 1
            class_counts[class_id] += 1

        (label_dir / f"{Path(file_name).stem}.txt").write_text(
            "\n".join(lines) + ("\n" if lines else ""), encoding="utf-8"
        )
        image_class_counts[image_id] = per_image

    if missing_images:
        preview = ", ".join(missing_images[:10])
        raise FileNotFoundError(
            f"{len(missing_images)} images referenced by {source_json.name} are missing "
            f"from {image_dir}. First files: {preview}"
        )
    if invalid_counts["unknown_image_id"] or invalid_counts["unknown_category_id"]:
        raise ValueError(f"Broken annotation references in {source_json}: {invalid_counts}")
    return images, image_class_counts, class_counts | invalid_counts


def split_train_ids(image_ids: list[int], val_ratio: float, seed: int) -> tuple[list[int], list[int]]:
    if not 0.0 < val_ratio < 1.0:
        raise ValueError("--val-ratio must be between 0 and 1")
    shuffled = sorted(image_ids)
    random.Random(seed).shuffle(shuffled)
    val_count = max(1, round(len(shuffled) * val_ratio))
    val_ids = set(shuffled[:val_count])
    return sorted(set(image_ids) - val_ids), sorted(val_ids)


def write_image_list(path: Path, image_dir_name: str, ids: list[int], images: dict[int, dict]) -> None:
    # Ultralytics expands list entries beginning with "./" relative to the list file.
    lines = [f"./../images/{image_dir_name}/{Path(images[i]['file_name']).name}" for i in ids]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def count_for_ids(ids: list[int], image_class_counts: dict[int, Counter]) -> dict[str, int]:
    total: Counter = Counter()
    for image_id in ids:
        total.update(image_class_counts[image_id])
    return {CLASS_NAMES[i]: total[i] for i in range(len(CLASS_NAMES))}


def main() -> None:
    args = parse_args()
    root = args.dataset_root.resolve()
    annotation_dir = root / "annotations"
    image_dir = root / "images"
    label_dir = root / "labels"
    split_dir = root / "splits"
    report_dir = root / "reports"
    split_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    train_json = annotation_dir / "instances_train.json"
    test_json = annotation_dir / "instances_test.json"
    train_coco, test_coco = load_coco(train_json), load_coco(test_json)

    train_images, train_image_counts, train_counts = convert_split(
        train_coco, train_json, image_dir / "train", label_dir / "train"
    )
    test_images, test_image_counts, test_counts = convert_split(
        test_coco, test_json, image_dir / "test", label_dir / "test"
    )
    train_ids, val_ids = split_train_ids(list(train_images), args.val_ratio, args.seed)
    test_ids = sorted(test_images)

    write_image_list(split_dir / "train.txt", "train", train_ids, train_images)
    write_image_list(split_dir / "val.txt", "train", val_ids, train_images)
    write_image_list(split_dir / "test.txt", "test", test_ids, test_images)

    report = {
        "seed": args.seed,
        "val_ratio": args.val_ratio,
        "classes": {str(i): name for i, name in enumerate(CLASS_NAMES)},
        "splits": {
            "train": {"images": len(train_ids), "instances": count_for_ids(train_ids, train_image_counts)},
            "val": {"images": len(val_ids), "instances": count_for_ids(val_ids, train_image_counts)},
            "test": {"images": len(test_ids), "instances": count_for_ids(test_ids, test_image_counts)},
        },
        "conversion": {
            "train_source_annotations": len(train_coco["annotations"]),
            "test_source_annotations": len(test_coco["annotations"]),
            "train_clipped_boxes": train_counts["clipped_bbox"],
            "test_clipped_boxes": test_counts["clipped_bbox"],
            "train_invalid_boxes_skipped": train_counts["invalid_bbox"],
            "test_invalid_boxes_skipped": test_counts["invalid_bbox"],
        },
    }
    report_path = report_dir / "dataset_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"\nPrepared DUO dataset at: {root}")


if __name__ == "__main__":
    main()
