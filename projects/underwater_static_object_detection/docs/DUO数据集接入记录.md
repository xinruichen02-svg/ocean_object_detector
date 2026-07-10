# DUO 数据集接入记录

## 当前决定

正式项目第一版采用 DUO，任务类型为四类目标检测，不是单标签图像分类。
DUO 面向水下机器人目标检测，一张图可以包含多个目标；保留边界框才能服务
后续目标定位、跟踪和机器人作业。

## 类别定义

| 项目类别编号 | 英文类别 | 中文含义 |
| --- | --- | --- |
| 0 | holothurian | 海参 |
| 1 | echinus | 海胆 |
| 2 | scallop | 扇贝 |
| 3 | starfish | 海星 |

这里的编号是转换为 YOLO 后的项目编号。转换时必须按原始 COCO 标注文件中
`categories` 的 `id` 和 `name` 建立映射，不能仅凭类别顺序猜测原始编号。

## 数据位置

- 用户本机原始路径：`E:\DUO`
- 原始数据位置：`dataset/DUO/raw/`
- 训练集：`dataset/DUO/images/train/` 和 `dataset/DUO/labels/train/`
- 验证集：`dataset/DUO/images/val/` 和 `dataset/DUO/labels/val/`
- 测试集：`dataset/DUO/images/test/` 和 `dataset/DUO/labels/test/`
- YOLO 数据配置：`dataset/DUO/data.yaml`

当前运行环境没有检测到 `E:\DUO`，也没有检测到常见 WSL 映射路径
`/mnt/e/DUO`。因此目前已经创建数据目录和类别配置，但各划分目录仍为空，
尚未读取图片、统计标注或生成 YOLO 标签。

## 接入后检查顺序

1. 查看 DUO 实际目录、图片数量和标注 JSON 文件名。
2. 读取 COCO `categories`，确认四个原始类别 ID。
3. 检查图片 ID、文件名、宽高和边界框是否完整。
4. 明确原始训练集、测试集以及验证集划分策略。
5. 将 COCO 边界框转换为 YOLO 归一化标签。
6. 随机可视化标签，确认类别和框位置正确。
7. 统计每类实例数量、空标签、越界框和缺失图片。

在以上检查完成前，不开始训练。
