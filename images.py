import os
from PIL import Image, ImageOps
from unidecode import unidecode
import PIL
# PIL.Image.Image.
target_size = 300

for dirName, subdirList, fileList in os.walk('./img/src'):
    for f in fileList:
        os.path.basename(f)
        image = Image.open(f'img/src/{f}')
        o_width, o_height = image.size
        ratio = max(o_width, o_height)/target_size
        n_width, n_height = (int(o_width/ratio), int(o_height/ratio))
        image = ImageOps.expand(image, border=15, fill=0xffffff)
        image.resize((n_width, n_height)).save(f'img/scaled/{unidecode(f.split(".")[0]).lower()}.png', 'png')

