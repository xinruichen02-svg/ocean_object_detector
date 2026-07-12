# 第一次原图训练

本目录保存第一次直接训练的关键产物。为精简仓库，仅保留最佳与最终权重、逐轮
指标、曲线和必要的训练/验证预览图。

## 训练配置

| 项目 | 值 |
| --- | --- |
| 任务 | 目标检测 |
| 模型 | YOLO11n (`yolo11n.pt`) |
| 训练轮数 | 80 epochs |
| 输入尺寸 | 640 |
| Batch size | 16 |
| 随机种子 | 42 |
| 设备 | 单 GPU (`device: 0`) |
| 确定性训练 | 是 |
| AMP | 是 |
| 数据增强 | 关闭 |
| 训练时长 | 14,588.2 秒（约 4.052 小时） |

完整参数见 [`args.yaml`](args.yaml)。

## 关键指标

| 结果 | Epoch | Precision | Recall | mAP50 | mAP50-95 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 最佳综合指标 | 23 | 0.78482 | 0.67584 | 0.74291 | 0.52387 |
| 最终轮次 | 80 | 0.82312 | 0.64644 | 0.71480 | 0.51138 |

逐轮指标见 [`results.csv`](results.csv)，训练与验证曲线见 [`results.png`](results.png)。

## 目录内容

- `weights/best.pt`：训练过程中保存的最佳权重。
- `weights/last.pt`：第 80 轮结束时的最终权重。
- `Box*.png`：Precision、Recall、F1 和 PR 曲线。
- `confusion_matrix*.png`：原始及归一化混淆矩阵。
- `val_batch*_labels.jpg`、`val_batch*_pred.jpg`：验证标签与预测对照。
- `train_batch*.jpg`：训练批次预览。
- `labels.jpg`：数据标签分布可视化。

每 10 轮生成的中间检查点和内容重复的训练预览图已删除；完整训练趋势仍可通过
`results.csv` 和 `results.png` 查看。
