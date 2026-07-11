# 第一阶段：原始图像 Baseline

本阶段只用 DUO 原始图片训练四类目标检测模型，不创建增强版图片，也关闭训练
中的可选颜色与几何增强。训练所必需的 letterbox/resize 和张量归一化仍会执行。

需要记录：

- 数据集版本。
- 模型版本。
- 训练参数。
- 训练日志路径。
- 验证指标。
- 推理可视化结果。
- 遇到的问题。

## 数据准备

从正式项目目录运行：

```bash
python src/datasets/prepare_duo.py
python src/datasets/visualize_labels.py --split val --count 20
```

确认 `dataset/DUO/reports/visualized_val/` 中的类别和框位置正确后，再启动训练。

## 训练命令

```bash
python src/detection/train_baseline.py \
  --model yolo11n.pt \
  --epochs 100 \
  --imgsz 640 \
  --batch 16
```

如果没有 GPU，可添加 `--device cpu` 先做小规模运行检查。训练结果写入
`results/training/phase1_original_images*`，不会混入数据集目录。

首次完整训练结束后，在本文件记录实际设备、耗时、指标和失败案例。
