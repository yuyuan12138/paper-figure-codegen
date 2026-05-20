# Visual Style Guide

## Font

```python
"font.family": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"]
```

Chinese fallback (when needed):
```python
"font.sans-serif": ["SimHei", "Arial Unicode MS", "Microsoft YaHei", "DejaVu Sans"]
```

## Axes

- Hide top and right spines
- Keep left and bottom spines
- Grid lines: y-axis only, dashed, alpha <= 0.35
- No heavy backgrounds

## Legend

- Simple plots: above or to the right
- Complex plots: separate legend panel
- Multi-panel figures: unified legend
- No frame (`legend.frameon: False`)

## Figure sizing

- Single plot: (5.5, 4) to (6, 4.5)
- Multi-panel: (10, 8) to (14, 10)
- Wide format for landscape slides: (12, 5)

## Export

- PNG: 300 DPI default, 600 for dense plots
- PDF: vector format for paper submission
- SVG: vector format for post-editing
- Always `bbox_inches="tight"`
- Font type 42 (TrueType) for PDF/PS compatibility
