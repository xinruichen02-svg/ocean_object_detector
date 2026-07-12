# 水下静态物体识别

使用 DUO 数据集训练海参、海胆、扇贝和海星四类目标检测模型。当前阶段直接
训练原始图片，不做水下颜色校正、去雾、亮度增强或数据增强。

## 目录职责

```text
dataset/       DUO 图片、标注、数据划分和 data.yaml
docs/          项目目标、路线、类别和数据集接入说明
results/       正式训练结果和中文训练日志
src/           数据准备与目标检测脚本
```

## 第一阶段运行

在本目录执行：

```bash
python -m pip install -r requirements.txt
python src/datasets/prepare_duo.py
python src/datasets/visualize_labels.py --split val --count 20
python src/detection/train_baseline.py --model yolo11n.pt --epochs 80
```

训练脚本关闭了 YOLO 的颜色、翻转、缩放、Mosaic、MixUp 等可选增强。模型仍会
执行训练必需的尺寸适配和张量归一化；这不生成或替换处理后的数据集图片。

第一次训练结果见 [第一次直接训练](results/第一次直接训练/README.md)，关键过程和
指标见 [训练日志](results/训练日志.md)。数据说明见
[DUO 数据集接入记录](docs/DUO数据集接入记录.md)。
