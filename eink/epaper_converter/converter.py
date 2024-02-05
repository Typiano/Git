from io import BytesIO
from PIL import Image, ImageOps
import sys
from os import path as Path

if len(sys.argv) == 4:
    path_to_image = str(sys.argv[1])
    image_name = Path.basename(path_to_image).split('/')[-1].split('.')[0]
    x = int(sys.argv[2])
    y = int(sys.argv[3])
    outfile = image_name+str(x)+"x"+str(y)

    im = Image.open(path_to_image).convert('1')
    im_invert = ImageOps.invert(im)
    im_resize = im_invert.resize((x,y))
    buf = BytesIO()
    im_resize.save(buf, 'ppm')
    byte_im = buf.getvalue()
    temp = len(str(x) + ' ' + str(y)) + 4
    print(byte_im[temp::])
    f = open(outfile+".py", "w")
    f.write(outfile + " = bytearray(")
    f.write(str(byte_im[temp::]))
    f.write(")")
    f.close()
else:
    print("please specify the location of image i.e img2bytearray.py image width heigh")  