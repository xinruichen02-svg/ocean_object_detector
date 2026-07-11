#!/usr/bin/env python3
"""Draw random YOLO labels on original DUO images for manual inspection."""

from __future__ import annotations

import argparse
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


CLASS_NAMES = ["holothurian", "echinus", "scallop", "starfish"]
COLORS = ["#ff4d4f", "#52c41a", "#1677ff", "#faad14"]
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATASET_ROOT = PROJECT_ROOT / "dataset" / "DUO"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Visualize a random sample of DUO YOLO labels.")
    parser.add_argument("--dataset-root", type=Path, default=DEFAULT_DATASET_ROOT)
    parser.add_argument("--split", choices=("train", "val", "test"), default="val")
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def label_path_for(image_path: Path) -> Path:
    parts = list(image_path.parts)
    try:
        index = parts.index("images")
    except ValueError as error:
        raise ValueError(f"Image path does not contain an images directory: {image_path}") from error
    parts[index] = "labels"
    return Path(*parts).with_suffix(".txt")


def main() -> None:
    args = parse_args()
    root = args.dataset_root.resolve()
    split_file = root / "splits" / f"{args.split}.txt"
    if not split_file.is_file():
        raise FileNotFoundError(f"Run prepare_duo.py first; missing {split_file}")
    image_paths = [
        (split_file.parent / line.strip()).resolve()
        for line in split_file.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if args.count <= 0:
        raise ValueError("--count must be positive")
    selected = random.Random(args.seed).sample(image_paths, min(args.count, len(image_paths)))
    output_dir = (args.output or (root / "reports" / f"visualized_{args.split}")).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default()

    for image_path in selected:
        with Image.open(image_path) as source:
            image = source.convert("RGB")
        draw = ImageDraw.Draw(image)
        width, height = image.size
        label_path = label_path_for(image_path)
        for line in label_path.read_text(encoding="utf-8").splitlines():
            class_id_text, cx_text, cy_text, box_width_text, box_height_text = line.split()
            class_id = int(class_id_text)
            cx, cy = float(cx_text) * width, float(cy_text) * height
            box_width, box_height = float(box_width_text) * width, float(box_height_text) * height
            x1, y1 = cx - box_width / 2, cy - box_height / 2
            x2, y2 = cx + box_width / 2, cy + box_height / 2
            color = COLORS[class_id]
            line_width = max(2, round(min(width, height) / 400))
            draw.rectangle((x1, y1, x2, y2), outline=color, width=line_width)
            draw.text((x1 + 2, max(0, y1 - 12)), CLASS_NAMES[class_id], fill=color, font=font)
        image.save(output_dir / image_path.name, quality=92)

    print(f"Saved {len(selected)} labeled previews to: {output_dir}")


if __name__ == "__main__":
    main()
