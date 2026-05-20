# Export Policy

## Default formats

PNG, PDF, SVG — all three generated for every figure.

## DPI settings

| Scenario | DPI |
|----------|-----|
| Default | 300 |
| Dense plots (many points/labels) | 600 |
| Quick preview | 150 |

## File naming

`figure_{name}.{format}` — stored in `outputs/` directory.

Example: `outputs/figure_comparison.png`, `outputs/figure_comparison.pdf`, `outputs/figure_comparison.svg`

## Font embedding

```python
"pdf.fonttype": 42,    # TrueType
"ps.fonttype": 42,     # TrueType
"svg.fonttype": "none", # Text as text, not paths
```

This ensures fonts are editable in vector formats.
