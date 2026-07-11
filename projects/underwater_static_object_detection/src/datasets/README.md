# 数据集处理模块

当前包含：

- `prepare_duo.py`：校验 COCO、转换 YOLO 标签、固定划分并输出统计报告。
- `visualize_labels.py`：在原图副本上画框，仅用于人工抽检报告。

两个脚本都不会修改 `dataset/DUO/images/` 中的原始图片。
