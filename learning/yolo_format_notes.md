# YOLO 数据格式学习笔记

本文件用于记录 YOLO 目标检测数据格式的学习过程。当前阶段只学习和手算，不写转换代码，不训练模型。

## 1. 为什么先学习 YOLO 数据格式

YOLO baseline 的第一步不是训练模型，而是准备正确的数据格式。

如果数据格式不对，可能会出现：

- 模型找不到图片或标签。
- 标签框位置错乱。
- 类别编号和类别名称对不上。
- 训练能运行，但结果完全不可信。

所以在进入 baseline 之前，需要先理解图片、标签和配置文件之间的关系。

## 2. YOLO 检测数据的基本结构

一个常见的 YOLO 数据集结构如下：

```text
dataset/
├── images/
│   ├── train/
│   └── val/
├── labels/
│   ├── train/
│   └── val/
└── data.yaml
```

含义：

- `images/train/`：训练集图片。
- `images/val/`：验证集图片。
- `labels/train/`：训练集标签。
- `labels/val/`：验证集标签。
- `data.yaml`：告诉 YOLO 数据集路径、类别数量和类别名称。

## 3. 图片和标签的对应关系

YOLO 中通常一张图片对应一个同名 `.txt` 标签文件。

例如：

```text
images/train/0001.jpg
labels/train/0001.txt
```

如果 `0001.jpg` 中有目标，`0001.txt` 中就记录目标框。

如果一张图片中有多个目标，标签文件中会有多行，每一行表示一个目标。

如果一张图片中没有目标，不同训练框架的处理方式可能不同，后续需要根据所用 YOLO 版本确认。

## 4. YOLO 标签每一行的格式

标签文件中每一行通常是：

```text
class_id x_center y_center width height
```

含义：

- `class_id`：类别编号，从 `0` 开始。
- `x_center`：目标框中心点 x 坐标，占图片宽度的比例。
- `y_center`：目标框中心点 y 坐标，占图片高度的比例。
- `width`：目标框宽度，占图片宽度的比例。
- `height`：目标框高度，占图片高度的比例。

注意：

- 后 4 个数不是像素值，而是归一化后的比例。
- 后 4 个数通常应该在 `0` 到 `1` 之间。
- 类别编号必须和 `data.yaml` 中的类别名称顺序一致。

## 5. 从像素框转换为 YOLO 格式

假设一张图片的尺寸是：

```text
image_width = W
image_height = H
```

目标框的像素坐标是：

```text
x_min, y_min, x_max, y_max
```

转换公式：

```text
x_center = ((x_min + x_max) / 2) / W
y_center = ((y_min + y_max) / 2) / H
width = (x_max - x_min) / W
height = (y_max - y_min) / H
```

## 6. 手算例子 1

图片尺寸：

```text
宽 W = 1000
高 H = 500
```

目标框像素坐标：

```text
x_min = 200
y_min = 100
x_max = 400
y_max = 300
```

计算：

```text
x_center = ((200 + 400) / 2) / 1000 = 0.3
y_center = ((100 + 300) / 2) / 500 = 0.4
width = (400 - 200) / 1000 = 0.2
height = (300 - 100) / 500 = 0.4
```

如果类别编号是 `0`，YOLO 标签为：

```text
0 0.3 0.4 0.2 0.4
```

## 7. 手算例子 2

图片尺寸：

```text
宽 W = 640
高 H = 480
```

目标框像素坐标：

```text
x_min = 160
y_min = 120
x_max = 320
y_max = 240
```

计算：

```text
x_center = ((160 + 320) / 2) / 640 = 0.375
y_center = ((120 + 240) / 2) / 480 = 0.375
width = (320 - 160) / 640 = 0.25
height = (240 - 120) / 480 = 0.25
```

如果类别编号是 `1`，YOLO 标签为：

```text
1 0.375 0.375 0.25 0.25
```

## 8. 一个最小 data.yaml 示例

假设我们只有两个类别：

```text
0: fish
1: trash
```

那么 `data.yaml` 可能写成：

```yaml
path: dataset
train: images/train
val: images/val

names:
  0: fish
  1: trash
```

当前阶段只理解它的作用，暂时不创建真实训练配置。

## 9. 我需要重点理解的问题

- 为什么 YOLO 标签使用归一化坐标？
- 为什么类别编号从 `0` 开始？
- 图片文件名和标签文件名为什么必须对应？
- 如果标签框超出图片边界会发生什么？
- 如果类别编号写错，模型会学到什么错误信息？

## 10. 下一步练习

请自己手算下面这个例子：

```text
图片尺寸：宽 800，高 600
目标框：x_min = 100, y_min = 150, x_max = 300, y_max = 450
类别编号：0
```

需要算出：

```text
class_id x_center y_center width height
```

算完后可以把结果记录在这里，或者发给我，我帮你检查。

