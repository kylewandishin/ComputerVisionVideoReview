import os
import random
import shutil

base_dir = os.path.dirname(os.path.abspath(__file__))

images_dir = os.path.join(base_dir, 'images')
# src_dir = os.path.join(images_dir, "Raw_Frames")
src_dir = r'/Users/wadeturner/Desktop/Fresh Frames'
print(src_dir)
shuffled_dir = os.path.join(images_dir, 'Shuffled 5')

image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']

os.makedirs(shuffled_dir, exist_ok=True)


files = [f for f in os.listdir(src_dir) if f.lower().endswith('.jpg') and os.path.isfile(os.path.join(src_dir, f))]
print(files)

random.shuffle(files)

for i, filename in enumerate(files):
    name, ext = os.path.splitext(filename)
    print(name, ext)
    new_name = f'PXL_{i+7299+1}{ext}'
    src_path = os.path.join(src_dir, filename)
    dst_path = os.path.join(shuffled_dir, new_name)
    shutil.copy2(src_path, dst_path)

print(f"Shuffled and renamed {len(files)} files to {shuffled_dir}")
