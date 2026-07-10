# 公开数据集调研：水下静态物体识别

本文件记录公开水下数据集候选。当前只做调研，不下载、不训练。

## 初步结论

当前最适合先看的数据集方向是：

```text
DUO / UDD / UODD / URPC 系列
```

它们更贴近水下机器人采摘、底栖生物识别和目标检测任务，常见类别包括：

```text
sea cucumber
scallop
sea urchin
starfish
```

“石头类”公开检测数据较少，更常见于底质分类、栖息地分类或分割数据。它可以作为后续扩展方向，但不建议作为第一版 YOLO 检测主类别。

## 数据集候选表

| 数据集 | 优先级 | 相关类别 | 任务类型 | 标注格式 | 当前判断 |
| --- | --- | --- | --- | --- | --- |
| DUO | 高 | scallop, starfish, sea cucumber, sea urchin | 检测 | 待下载确认 | 最推荐先调研 |
| UDD | 高 | sea cucumber, sea urchin, scallop | 检测 | 待下载确认 | 适合机器人采摘方向 |
| UODD | 高 | sea cucumber, sea urchin, scallop | 检测 | COCO/检测标注 | 可作为第二候选 |
| URPC / UTDAC / S-URPC | 中高 | holothurian, echinus, scallop, starfish | 检测 | 待确认 | 类别匹配，但下载源要确认 |
| MOUD | 中 | scallop, conch, holothuria, reef, abalone, barnacle 等 | 检测/分割/重建 | JSON/分割/检测 | 类别丰富，但偏模拟场景 |
| Roboflow SeaCucumber-Shell | 中 | SeaCucumber, Shell | 检测 | Roboflow 导出格式 | 小规模上手可用，需确认质量 |
| JAMBO | 中低 | sand, stone, bad | 分类 | 图像级分类 | 适合研究石头/底质，不适合直接 YOLO 检测 |
| SUIM | 低到中 | reef, sea-floor 等 | 语义分割 | 像素级标注 | 可用于背景/场景理解，不是第一版检测数据 |
| Brackish | 低 | crab, starfish 等 | 检测 | 待确认 | 类别不够贴合贝壳/海参/石头 |
| TrashCan | 低 | 垃圾、ROV 相关 | 分割/实例 | COCO 类 | 偏垃圾识别，不是当前主线 |

## 1. DUO
https:
- 地址：//github.com/chongweiliu/DUO
- 任务：水下目标检测。
- 相关类别：scallop、starfish、sea cucumber、sea urchin。
- 适合程度：高。
- 可能用途：第一版水下静态物体检测 baseline。
- 需要确认：
  - 下载链接是否可用。
  - 标注格式是否能直接转 YOLO。
  - 训练集和测试集划分方式。
  - 类别名称和编号。

调研依据：DUO 仓库说明其目标是 underwater object detection for robot picking，并提到面向机器人嵌入式环境评估。

## 2. UDD

- 论文/说明：A New Dataset, Poisson GAN and AquaNet for Underwater Object Grabbing。
- 任务：水下目标检测。
- 相关类别：sea cucumber、sea urchin、scallop。
- 适合程度：高。
- 可能用途：海参、扇贝、海胆检测。
- 需要确认：
  - 原始数据下载地址。
  - 是否仍然公开可访问。
  - 标注格式和划分。

调研依据：公开论文摘要称 UDD 包含 2,227 张真实开放海域养殖场图像，类别包括 seacucumber、seaurchin、scallop。

## 3. UODD

- 地址：https://github.com/LehiChiang/Underwater-object-detection-dataset
- 任务：水下物种检测。
- 相关类别：sea cucumber、sea urchin、scallop。
- 适合程度：高。
- 标注格式：仓库说明为 MS COCO format。
- 可能用途：作为 COCO 到 YOLO 转换学习数据。
- 需要确认：
  - 图片数量。
  - 类别 id。
  - COCO 标注字段是否完整。

## 4. URPC / UTDAC / S-URPC 系列

- 汇总地址：https://github.com/mousecpn/Collection-of-Underwater-Object-Detection-Dataset
- 任务：水下目标检测。
- 相关类别：holothurian、echinus、scallop、starfish。
- 适合程度：中高。
- 可能用途：补充 sea cucumber / sea urchin / scallop / starfish 类别。
- 需要确认：
  - 不同年份数据是否能下载。
  - 标注质量是否一致。
  - 类别英文名称是否需要统一。

类别名称映射建议：

```text
holothurian -> sea_cucumber
echinus -> sea_urchin
scallop -> scallop
starfish -> starfish
```

## 5. MOUD

- 论文页面：https://www.nature.com/articles/s41597-025-05797-w
- 任务：水下图像增强、检测、分割、重建。
- 相关类别：scallop、starfish、conch、holothuria、seaweed、coral、reef、abalone、barnacle。
- 适合程度：中。
- 优点：
  - 类别很贴合静态物体识别。
  - 有检测、分割和 3D 重建相关信息。
  - 包含不同光照和浑浊模拟。
- 风险：
  - 是水下模拟场景，不一定等价于真实海底。
  - 标注和工具需要单独解析。
  - 数据量较大，当前阶段不要急着下载。

## 6. Roboflow SeaCucumber-Shell

- 地址：https://universe.roboflow.com/yolo-adfzk/underwater-qoqz8
- 任务：SeaCucumber 和 Shell 检测。
- 相关类别：SeaCucumber、Shell。
- 适合程度：中。
- 优点：
  - 类别和当前方向高度相关。
  - 页面显示为开放数据，许可为 CC BY 4.0。
  - 数据规模小，适合后续快速上手。
- 风险：
  - 需要检查标注质量。
  - 数据来源和采集条件说明不足。
  - 小数据集不能作为主要结论来源。

## 7. JAMBO

- 地址：https://vap.aau.dk/jambo/
- 任务：底栖栖息地图像分类。
- 相关类别：sand、stone、bad。
- 适合程度：中低。
- 优点：
  - 对“石头类/底质”方向有参考价值。
  - ROV 采集，贴近水下机器人视角。
- 风险：
  - 是图像级分类，不是目标检测。
  - 不能直接训练 YOLO 检测框。

## 当前推荐路线

第一阶段只筛选和确认：

```text
DUO
UODD
UDD
URPC/UTDAC 系列
Roboflow SeaCucumber-Shell
```

第二阶段再判断是否加入：

```text
MOUD
JAMBO
SUIM
```

当前不要急着合并所有数据。先确认一个数据集是否能稳定转成 YOLO，再考虑混合数据。

