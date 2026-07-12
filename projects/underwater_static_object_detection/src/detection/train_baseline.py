#!/usr/bin/env python3
"""Train the phase-1 DUO baseline without optional image augmentation."""

from __future__ import annotations

import argparse
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a YOLO baseline on original DUO images.")
    parser.add_argument("--model", default="yolo11n.pt")
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--device", default=None, help="Examples: 0, cpu, mps")
    parser.add_argument("--workers", type=int, default=8)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        from ultralytics import YOLO
    except ImportError as error:
        raise SystemExit("Ultralytics is not installed. Run: pip install -r requirements.txt") from error

    data_yaml = PROJECT_ROOT / "dataset" / "DUO" / "data.yaml"
    if not (PROJECT_ROOT / "dataset" / "DUO" / "splits" / "train.txt").is_file():
        raise SystemExit("Dataset is not prepared. Run src/datasets/prepare_duo.py first.")

    settings = {
        "data": str(data_yaml),
        "epochs": args.epochs,
        "imgsz": args.imgsz,
        "batch": args.batch,
        "workers": args.workers,
        "project": str(PROJECT_ROOT / "results"),
        "name": "直接训练",
        "exist_ok": False,
        "seed": 42,
        "deterministic": True,
        "rect": True,
        # Phase 1: turn off optional color and geometric augmentation.
        "hsv_h": 0.0,
        "hsv_s": 0.0,
        "hsv_v": 0.0,
        "degrees": 0.0,
        "translate": 0.0,
        "scale": 0.0,
        "shear": 0.0,
        "perspective": 0.0,
        "flipud": 0.0,
        "fliplr": 0.0,
        "mosaic": 0.0,
        "mixup": 0.0,
        "copy_paste": 0.0,
        "erasing": 0.0,
    }
    if args.device is not None:
        settings["device"] = args.device

    YOLO(args.model).train(**settings)


if __name__ == "__main__":
    main()
