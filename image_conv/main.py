import os
import time
import logging

from PIL import Image

base_path = "main_images"
output = "output"

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

def get_files(loc: str):
    pathfiles = os.listdir(loc)
    for pathfile in pathfiles:
        yield pathfile




def main():
    if not os.path.exists(output):
        os.mkdir(output)
    
    for fname in get_files(base_path):
        file = os.path.join(base_path, fname)
        img_file = Image.open(file)

        
        img_resize = img_file.resize((1200,1200))
        
        output_file = os.path.join(output, fname)
        img_resize.save(output_file, dpi=(1200,1200), quality=)
        logging.info(f"Convert image {fname}")
    return






if __name__ == "__main__": 
    
    folder = input("Masukkan lokasi gambar: ")
    base_path = folder
    
    main()
    
    import sys
    for i in range(10, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write('menutup program dalam %i ' % i)
        sys.stdout.flush()
        
        time.sleep(1)

    sys.stdout.write("\r")