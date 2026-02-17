import os
from pathlib import Path
from PIL import Image
import pandas as pd

image_files = []
widths_pixels = []
heights_pixels = []
formats = []

dpi_xs = []
dpi_ys = []
width_inches = []
height_inches = []

def dimensions(folder_path):
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp')
    
    path = Path(folder_path)
    for file_path in path.iterdir():
        if file_path.suffix.lower() in valid_extensions:
            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                    dpi = img.info.get("dpi", (300,300))
                    if isinstance(dpi, (int, float)):
                        dpi = (dpi, dpi)
                    dpi_x, dpi_y = dpi
                    dpi_x = dpi_x if dpi_x else 300
                    dpi_y = dpi_y if dpi_y else 300
                    dpi_x = float(dpi_x) if dpi_x else 300.0
                    dpi_y = float(dpi_y) if dpi_y else 300.0                    
                    w_in = float(width) / dpi_x
                    h_in = float(height) / dpi_y
                    w_in = width / dpi_x
                    h_in = height / dpi_y
                    
                    dpi_xs.append(dpi_x)
                    dpi_ys.append(dpi_y)
                    width_inches.append(w_in)
                    height_inches.append(h_in)
                    image_files.append(file_path.name)
                    widths_pixels.append(width)
                    heights_pixels.append(height)
                    formats.append(img.format)
                    #print(f"File: {file_path.name} | Dimensions: {width}x{height} | Format: {img.format}")
            except Exception as e:
                print(f"Could not read {file_path.name}: {e}")

IMAGE_FOLDER = "C:\\Users\\bhanu\\Pictures\\printing"

if __name__ == "__main__":
    if os.path.exists(IMAGE_FOLDER):
        dimensions(IMAGE_FOLDER)
    else:
        print(f"Error: Folder '{IMAGE_FOLDER}' not found.")

df = pd.DataFrame({
    "File": image_files,
    "Width_px": widths_pixels,
    "Height_px": heights_pixels,
    "DPI_X": dpi_xs,
    "DPI_Y": dpi_ys,
    "Width_in": width_inches,
    "Height_in": height_inches,
    "Format": formats
})

df["Width_in"] = df["Width_in"].round(2)
df["Height_in"] = df["Height_in"].round(2)

TARGET_DPIS = [300, 240, 200]

for dpi in TARGET_DPIS:
    df[f"MaxWidth_{dpi}dpi_in"] = (df["Width_px"]/dpi).round(2)
    df[f"MaxHeight_{dpi}dpi_in"] = (df["Height_px"]/dpi).round(2)

print(df)

df.to_csv('file_sizes.csv')