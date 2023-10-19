import os
import time
import logging

from PIL import Image

base_path = "main_images"
output = "output"
max_size = 4
min_size = 3.5
 
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

def get_files(loc: str):
    pathfiles = os.listdir(loc)
    for pathfile in pathfiles:
        yield pathfile

def isValidSize(size):
    return size < max_size

def isValidOutput(output):
    output_info = os.stat(output)
    sizefile = size_mb(output_info.st_size)
    return isValidSize(sizefile)


def resize(output_name, img, size, quality = 95, subquality = 5):
    img_resize = img.resize(size)

    final_quality = quality+subquality 

    img_resize.save(output_name, quality=final_quality)

    if not isValidOutput(output_name):
        return resize(output_name, img, size, final_quality, -5)
    return

def generate_image(pathfile):
    file_info = os.stat(pathfile)
    sizefile = size_mb(file_info.st_size)
    
    img = Image.open(pathfile)
    img_size = img.size

    fname = os.path.split(pathfile)[-1]
    output_file = os.path.join(output, fname)

    if (sizefile // max_size) > 0:
        resize(output_file, img, img_size, 95, -5) 

    resize(output_file, img, img_size, 95, 0) 
    return 

def size_mb(size):
    return size / (1024*1024)

def main():
    if not os.path.exists(output):
        os.mkdir(output)
    
    for fname in get_files(base_path):
        file = os.path.join(base_path, fname)
        ext = os.path.splitext(file)[-1]
        if ext not in [".jpg", ".jpeg", ".png"]:
            continue

        generate_image(file)
        logging.info(f"Convert image {fname}")
    return

if __name__ == "__main__": 
    
    folder = input("Masukkan lokasi gambar: ")
    if folder != '':
        base_path = folder
    
    main()
    
    import sys
    for i in range(10, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write('menutup program dalam %i ' % i)
        sys.stdout.flush()
        
        time.sleep(1)

    sys.stdout.write("\r")
