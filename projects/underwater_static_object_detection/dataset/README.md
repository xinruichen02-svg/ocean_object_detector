# 数据集目录

正式项目的数据全部放在本目录。第一阶段只使用 `DUO/`，不修改原始图片像素。

```text
DUO/
├── annotations/          原始 COCO 标注
├── images/
│   ├── train/            DUO 原训练图片（原文件）
│   └── test/             DUO 原测试图片（原文件）
├── labels/               由脚本生成的 YOLO 标签（不提交）
├── splits/               训练、验证、测试图片清单
├── reports/              数据检查报告和抽检图
└── data.yaml             Ultralytics 数据配置
```

验证集通过 `splits/val.txt` 从原训练集选择，不复制或处理图片。`train.txt` 与
`val.txt` 不重叠，原测试集保持独立。

生成数据：

```bash
python src/datasets/prepare_duo.py
```

随机查看带框图片：

```bash
python src/datasets/visualize_labels.py --split val --count 20
```
