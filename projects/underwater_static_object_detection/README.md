# 水下静态物体识别正式项目

本目录是水下机器人静态物体识别的正式工程区，当前目标是识别海参、
扇贝、海胆、海星等近底静态目标，并为后续接入 ROS1 水下机器人保留接口位置。

当前进入第一阶段 baseline：使用 DUO 的四类目标检测标注，只训练原始图片，
不做水下颜色校正、去雾、亮度增强或数据增强。

正式文档入口：[文档说明](docs/文档说明.md)。

## 目录职责

```text
configs/       模型和实验配置
dataset/       DUO 原图、COCO 标注、YOLO 标签、划分和 data.yaml
docs/          本项目目标、路线、类别设计、数据集调研和记录模板
experiments/   真实水下数据上的实验记录
notebooks/     数据检查、训练和结果分析笔记
results/       正式实验产生的图、表、日志和预测结果
src/           数据、增强、检测、跟踪和机器人接口代码
```

通用学习笔记位于仓库根目录的 `learning/`。玩具数据和练习输出位于
`examples/yolo_toy/`，不作为正式实验结果，也不与这里的数据和权重混用。

## 第一阶段运行

在本目录执行：

```bash
python -m pip install -r requirements.txt
python src/datasets/prepare_duo.py
python src/datasets/visualize_labels.py --split val --count 20
python src/detection/train_baseline.py --model yolo11n.pt --epochs 100
```

训练脚本关闭了 YOLO 的颜色、翻转、缩放、Mosaic、MixUp 等可选增强。模型仍会
执行训练必需的尺寸适配和张量归一化；这不生成或替换处理后的数据集图片。

详细说明见 [第一阶段 baseline](experiments/baseline/README.md) 和
[DUO 数据集接入记录](docs/DUO数据集接入记录.md)。
