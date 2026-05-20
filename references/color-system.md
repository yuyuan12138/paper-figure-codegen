# Color System

## Default palette (PAPER_PALETTE)

Low-saturation academic colors:
- Blues: blue_main (#5B8DB8), blue_dark (#3E6F95), blue_light (#BFD8EA)
- Teals: teal_main (#6FA8A6), teal_dark (#4D8583)
- Greens: green_main (#9CCB9E), green_light (#CFE8D5)
- Warm: yellow_light (#F3E6B3), orange_light (#E8B77D), orange_main (#D99A5E)
- Purple: purple_light (#C9BEDF), pink_light (#E7C1C0)
- Neutral: gray_light (#E8ECEF), gray (#BFC7CD), gray_dark (#66727C)
- Semantic: positive (#6FA8A6), negative (#D99A5E), neutral (#BFC7CD), highlight (#F3C567)

## Color assignment rules

| Groups | kind | Colors |
|--------|------|--------|
| 2 | binary | blue_main, orange_main |
| 3 | categorical | blue_main, green_main, orange_light |
| 4-6 | categorical | blue, teal, green, yellow, orange, purple (first n) |
| 7+ | categorical | tab20 fallback |
| continuous | sequential | Blues colormap |
| positive/negative | diverging | orange → gray → blue |
| significant vs not | significance | dark + marker vs light gray + alpha |

## Usage in generated code

Every generated script includes the full PAPER_PALETTE dict. The `get_palette(n, kind)` function handles selection.
