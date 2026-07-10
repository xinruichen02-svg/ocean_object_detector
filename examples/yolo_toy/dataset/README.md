# YOLO Toy Example Dataset

这是一个最小 YOLO 格式示例数据集，用于学习训练流程和标签格式。

它不是水下真实数据集，也不能用于说明模型效果。

## 数据内容

- 类别数量：1
- 类别名称：`toy_object`
- 训练图片：2 张
- 验证图片：2 张
- 图片尺寸：`320 x 240`

## 目录结构

```text
examples/yolo_toy/dataset/
├── data.yaml
├── images/
│   ├── train/
│   └── val/
└── labels/
    ├── train/
    └── val/
```

## 学习重点

请重点观察：

- 图片文件名和标签文件名是否一一对应。
- 每个标签文件中一行代表一个目标。
- 标签中的坐标是归一化坐标，不是像素坐标。
- `data.yaml` 中的类别编号和标签中的 `class_id` 是否一致。
