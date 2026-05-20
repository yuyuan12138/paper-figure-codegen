# Troubleshooting

## Chinese text shows as squares

Add before plotting:
```python
plt.rcParams["font.sans-serif"] = ["SimHei", "Arial Unicode MS", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
```

## Optional dependency missing

All optional deps (scipy, sklearn, mne, statsmodels) use try/except with fallback:
```python
try:
    from scipy import stats
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False
```

## Figure clipped / labels cut off

Add `fig.tight_layout(pad=1.2)` before returning figure.
Use `savefig(bbox_inches="tight")` in export.

## Colors too similar for many groups

For >6 groups, `get_palette` falls back to `tab20`. Consider splitting into multiple subplots.

## Heatmap too crowded

- Reduce annotation font size
- Use `figsize` with wider dimensions
- Rotate x-axis labels: `ax.set_xticklabels(labels, rotation=45, ha="right")`
