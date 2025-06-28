#!/usr/bin/env python3

import os
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Tuple
import io

from rembg import remove
from PIL import Image

# Configuration - edit these
INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
MAX_WORKERS = 4  # adjust based on your CPU
JPEG_QUALITY = 95  # 1-100, higher = better quality
OUTPUT_FORMAT = "JPEG"  # JPEG, PNG, WEBP
BLACK_BACKGROUND = True  # False for transparent PNG

SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff'}

def setup_dirs():
    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

def get_next_number():
    existing = list(OUTPUT_DIR.glob("img_*.jpg")) + list(OUTPUT_DIR.glob("img_*.png"))
    if not existing:
        return 1
    
    nums = []
    for f in existing:
        try:
            nums.append(int(f.stem.split("_")[1]))
        except (ValueError, IndexError):
            continue
    
    return max(nums) + 1 if nums else 1

def process_image(input_path: Path, output_num: int) -> Tuple[bool, str]:
    start = time.time()
    
    try:
        with open(input_path, 'rb') as f:
            result_bytes = remove(f.read())
        
        result_img = Image.open(io.BytesIO(result_bytes))
        
        if BLACK_BACKGROUND and OUTPUT_FORMAT != "PNG":
            if result_img.mode != 'RGBA':
                result_img = result_img.convert('RGBA')
            
            black_bg = Image.new('RGB', result_img.size, (0, 0, 0))
            black_bg.paste(result_img, mask=result_img.split()[-1])
            result_img = black_bg
        
        ext = ".jpg" if OUTPUT_FORMAT == "JPEG" else f".{OUTPUT_FORMAT.lower()}"
        output_path = OUTPUT_DIR / f"img_{output_num:04d}{ext}"
        
        save_kwargs = {}
        if OUTPUT_FORMAT == "JPEG":
            save_kwargs['quality'] = JPEG_QUALITY
        
        result_img.save(output_path, OUTPUT_FORMAT, **save_kwargs)
        
        input_path.unlink()
        
        elapsed = time.time() - start
        return True, f"{input_path.name} -> {output_path.name} ({elapsed:.1f}s)"
        
    except Exception as e:
        return False, f"Failed {input_path.name}: {str(e)}"

def main():
    setup_dirs()
    
    image_files = []
    for ext in SUPPORTED_FORMATS:
        image_files.extend(INPUT_DIR.glob(f"*{ext}"))
        image_files.extend(INPUT_DIR.glob(f"*{ext.upper()}"))
    
    if not image_files:
        print(f"No images found in {INPUT_DIR}")
        return
    
    print(f"Processing {len(image_files)} images with {MAX_WORKERS} workers...")
    
    start_num = get_next_number()
    success_count = 0
    
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_file = {
            executor.submit(process_image, img_file, start_num + i): img_file 
            for i, img_file in enumerate(image_files)
        }
        
        for future in as_completed(future_to_file):
            success, msg = future.result()
            print(msg)
            if success:
                success_count += 1
    
    print(f"\nDone: {success_count}/{len(image_files)} processed")

if __name__ == "__main__":
    main()
