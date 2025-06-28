# Background Removal Script

Batch remove backgrounds from images using AI. Fast, simple, configurable.

## Quick Start

```bash
pip install rembg pillow
python bg_remove.py
```

## Setup

1. Install dependencies:
   ```bash
   pip install rembg pillow
   ```

2. Create folders:
   ```
   input/    # put your images here
   output/   # processed images go here
   ```

3. Drop images in `input/` folder and run the script

## Configuration

Edit these variables at the top of `bg_remove.py`:

```python
INPUT_DIR = Path("input")           # source folder
OUTPUT_DIR = Path("output")         # destination folder  
MAX_WORKERS = 4                     # parallel processes (adjust for your CPU)
JPEG_QUALITY = 95                   # 1-100, higher = better quality
OUTPUT_FORMAT = "JPEG"              # JPEG, PNG, WEBP
BLACK_BACKGROUND = True             # False for transparent PNG
```

## Performance Tuning

- **MAX_WORKERS**: Start with your CPU core count, adjust based on RAM usage
- **JPEG_QUALITY**: 95 is high quality, use 85 for smaller files
- **OUTPUT_FORMAT**: JPEG for photos, PNG for graphics with transparency

## Supported Formats

Input: JPG, JPEG, PNG, WEBP, BMP, TIFF
Output: JPEG, PNG, WEBP

## Notes

- Original files are deleted after processing
- Output files are numbered: `img_0001.jpg`, `img_0002.jpg`, etc.
- Script resumes numbering from last processed batch
- First run downloads AI model (~100MB)

## Troubleshooting

**Out of memory**: Reduce `MAX_WORKERS` to 1-2
**Slow processing**: Increase `MAX_WORKERS` up to CPU core count
**Large files**: Lower `JPEG_QUALITY` to 75-85
