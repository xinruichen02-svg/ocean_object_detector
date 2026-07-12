# 第一次原图训练

本目录保存 `E:\duo_result_v1` 的完整云端训练输出。原始文件名与目录结构均未改动，便于与 Ultralytics 训练产物直接对照。

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
- `weights/epoch0.pt` 至 `weights/epoch70.pt`：每 10 轮保存的检查点。
- `Box*.png`：Precision、Recall、F1 和 PR 曲线。
- `confusion_matrix*.png`：原始及归一化混淆矩阵。
- `val_batch*_labels.jpg`、`val_batch*_pred.jpg`：验证标签与预测对照。
- `train_batch*.jpg`：训练批次预览。
- `labels.jpg`：数据标签分布可视化。

## 原始输出说明

以下三对训练预览图的 SHA-256 完全一致：

- `train_batch0.jpg` 与 `train_batch24850.jpg`
- `train_batch1.jpg` 与 `train_batch24851.jpg`
- `train_batch2.jpg` 与 `train_batch24852.jpg`

为保留云端训练输出的完整性，这些重复文件均未删除。

除本 README 外，本目录包含 32 个原始文件，共 186,749,783 字节；所有单文件均小于 GitHub 100 MB 限制。
