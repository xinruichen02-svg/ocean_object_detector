# YOLO Toy Example Baseline

这是一次最小 YOLO 流程练习，目的不是得到好模型，而是确认以下链路可以跑通：

```text
YOLO 格式数据集 -> data.yaml -> train -> val -> predict -> 输出结果目录
```

## 数据集

使用数据集：

```text
examples/yolo_toy/dataset/
```

数据内容：

- 训练图片：2 张
- 验证图片：2 张
- 类别数量：1
- 类别名称：`toy_object`

这是合成玩具数据，不是真实水下数据。

## 环境处理

本环境中直接使用 `opencv-python` 会缺少系统图形库：

```text
ImportError: libGL.so.1
```

因此改用命令行环境更合适的 headless 版本：

```bash
python -m pip uninstall -y opencv-python
python -m pip install opencv-python-headless
```

## 训练命令

```bash
/usr/local/python/3.12.1/bin/yolo detect train \
  model=examples/yolo_toy/weights/yolo11n.pt \
  data=examples/yolo_toy/dataset/data.yaml \
  epochs=2 \
  imgsz=320 \
  batch=2 \
  device=cpu \
  workers=0 \
  project=examples/yolo_toy/outputs \
  name=train \
  exist_ok=True
```

## 预测命令

```bash
/usr/local/python/3.12.1/bin/yolo detect predict \
  model=examples/yolo_toy/outputs/train/weights/best.pt \
  source=examples/yolo_toy/dataset/images/val/toy_val_01.png \
  imgsz=320 \
  conf=0.01 \
  device=cpu \
  project=examples/yolo_toy/outputs \
  name=predict \
  exist_ok=True
```

## 本次观察

- YOLO 成功读取了训练集和验证集。
- 训练集扫描结果：2 张图片，0 张背景图，0 个损坏样本。
- 验证集扫描结果：2 张图片，0 张背景图，0 个损坏样本。
- 训练输出现整理在 `examples/yolo_toy/outputs/train/`。
- 预测输出现整理在 `examples/yolo_toy/outputs/predict/`。

## 不解读为模型效果

这次数据量极小，训练轮数也极少，所以指标和预测框数量都不能代表模型能力。

它只说明：

- 数据目录结构可被 YOLO 识别。
- 标签格式可被 YOLO 读取。
- 训练命令和预测命令可以跑通。

## 下一步

下一步建议手动查看：

- `examples/yolo_toy/dataset/data.yaml`
- `examples/yolo_toy/dataset/labels/train/toy_train_01.txt`
- `examples/yolo_toy/dataset/images/train/toy_train_01.png`
- `examples/yolo_toy/outputs/train/labels.jpg`
- `examples/yolo_toy/outputs/train/results.csv`
