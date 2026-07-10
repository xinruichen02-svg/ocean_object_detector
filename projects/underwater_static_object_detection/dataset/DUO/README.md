# DUO 数据集

本目录集中保存 DUO 的原始数据入口、YOLO 数据配置、图片划分和标签划分。

```text
DUO/
├── data.yaml
├── raw/             原始 DUO 数据和 COCO 标注，只读保留
├── images/
│   ├── train/       训练图片
│   ├── val/         验证图片
│   └── test/        测试图片
└── labels/
    ├── train/       训练图片对应的 YOLO 标签
    ├── val/         验证图片对应的 YOLO 标签
    └── test/        测试图片对应的 YOLO 标签
```

当前这些目录已经建立，但数据仍在用户本机 `E:\DUO`，当前 Linux 工作区无法
访问，因此图片和标签尚未导入。正式转换前需要先读取原始 COCO JSON，确认
类别 ID 和原始数据划分。

图片、JSON 和标签等数据文件不提交 Git，目录中的 `.gitkeep` 只用于保留空目录。
