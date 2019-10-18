#!/usr/bin/env python3

from PIL import ExifTags, Image
import sys

# Size of output image in pixels
output_size = 4000

if len(sys.argv) != 7:
    print(f"Usage: {sys.argv[0]} <6 input files>")
    sys.exit(1)

# Get the EXIF orientation tag so we display things the right way up
orientation_key = None
for k, v in ExifTags.TAGS.items():
    if v == 'Orientation':
        orientation_key = k
        break
else:
    print("Warning: Couldn't find EXIF orientation tag")

# Put the blank image at the start as image zero
blank_img = Image.new("1", (output_size//2, output_size//2), 1)
blank_dict = {"x": blank_img}

imgs = [blank_dict]

for img in sys.argv[1:7]:
    i = Image.open(img)

    # Rotate if necessary
    if orientation_key:
        orientation = i._getexif().get(orientation_key, 1)

        if orientation == 2:
            i = i.transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == 3:
            i = i.rotate(180)
        elif orientation == 4:
            i = i.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == 5:
            i = i.rotate(-90).transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == 6:
            i = i.rotate(-90)
        elif orientation == 7:
            i = i.rotate(90).transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == 8:
            i = i.rotate(90)

    # Crop to square (centered)
    x, y = i.size
    if x != y:
        if x > y:
            crop_coord = ((x-y)//2, 0, (x+y)//2, y)
        else:
            crop_coord = (0, (y-x)//2, x, (y+x)//2)
        i = i.crop(crop_coord)

    # Scale to final size
    i = i.resize((output_size//2, output_size//2))
    size, _ = i.size

    # Break into quarters
    img_dict = {}
    img_dict["tl"] = i.crop((0, 0, size//2, size//2))
    img_dict["tr"] = i.crop((size//2, 0, size, size//2))
    img_dict["bl"] = i.crop((0, size//2, size//2, size))
    img_dict["br"] = i.crop((size//2, size//2, size, size))

    imgs.append(img_dict)


# Definition of output grid. Interestingly, the back is the same layout, just
# subtract one from the image number

outputs = {
    "front": [[(4, "tr", 180), (4, "tl", 180), (2, "tl", 180), (6, "tl", 0)],
              [(2, "tr", 0), (0, "x", 0), (0, "x", 0), (6, "bl", 0)],
              [(6, "tr", 0), (0, "x", 0), (0, "x", 0), (2, "bl", 0)],
              [(6, "br", 0), (2, "br", 180), (4, "br", 180), (4, "bl", 180)]],
    "back": [[(3, "tr", 180), (3, "tl", 180), (1, "tl", 180), (5, "tl", 0)],
             [(1, "tr", 0), (0, "x", 0), (0, "x", 0), (5, "bl", 0)],
             [(5, "tr", 0), (0, "x", 0), (0, "x", 0), (1, "bl", 0)],
             [(5, "br", 0), (1, "br", 180), (3, "br", 180), (3, "bl", 180)]]
}

for name, grid in outputs.items():
    output = Image.new("RGB", (output_size, output_size), None)

    for x, row in enumerate(grid):
        for y, square in enumerate(row):
            piece = imgs[square[0]][square[1]]
            if square[2]:
                piece = piece.rotate(square[2])
            output.paste(piece, (y*output_size//4, x*output_size//4))

    output.save(name + ".jpg")
