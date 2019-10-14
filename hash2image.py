import os
import io
import base64
import hashlib
from PIL import Image


resource_dir = os.path.join(os.path.dirname(__file__), 'sets')


def set_with_subsets(setname):
    path = os.path.join(resource_dir, setname)
    dict_whith_all_files = {}
    pathfiles1 = sorted(os.listdir(path))
    path1 = os.path.join(path, pathfiles1[0])
    sudirectories = False
    if os.path.isdir(path1):
        pathfiles2 = os.listdir(path1)
        path2 = os.path.join(path1, pathfiles2[0])
        if os.path.isdir(path2):
            return True, pathfiles1
    return False, []


def generate_hash(string_value):
    """
        1. Generates hexdigest out of a string_value
    """
    hash = hashlib.sha512()
    hash.update(string_value.encode('utf-8'))
    return hash.hexdigest()


def split_hash(hdigest, number_of_parts):
    """
        Splits hexdigest in equal parts according to number_of_parts
        Returns an array of splitted hexdigest in integer(10) format
    """
    blocksize = int(len(hdigest) / number_of_parts)
    hasharray = []
    for i in range(number_of_parts):
        currentstart = i * blocksize
        currentend = (1 + i) * blocksize
        hasharray.append(int(hdigest[currentstart:currentend], 16))
    return hasharray


def get_all_image_parts(selected_set_dir):
    """Returns a dictionary of the form:
       {'pathtodir1': ['000.png, '001.png'],
       'pathdir2: ['000.png', '001.png'],
        ...
       }
    """
    path = os.path.join(resource_dir, selected_set_dir)
    dict_whith_all_files = {}
    for root, dirs, files in os.walk(path):
        if not dirs:
            if files:
                files.sort()
                dict_whith_all_files[root] = files
    return dict_whith_all_files


def select_image_parts(all_files_dict, hdigest):
    futures_number = len(all_files_dict)
    hasharray = split_hash(hdigest, futures_number)
    selected = []
    fingerprint = ''
    for i, cat in enumerate(sorted(all_files_dict)):
        future_images_number = len(all_files_dict[cat])
        number_from_hash = hasharray[i] % future_images_number
        fname = all_files_dict[cat][number_from_hash]
        selected.append(os.path.join(cat, fname))
        fingerprint += str(number_from_hash)
    return selected, fingerprint


def paint_image(image_parts):
    img = Image.open(image_parts[0])
    img = img.resize((1024, 1024))
    for png_image in image_parts:
        temp_image = Image.open(png_image)
        temp_image = temp_image.resize((1024, 1024))
        try:
            img.paste(temp_image, (0, 0), temp_image)
        except ValueError:
            print(f'Image {png_image} has problem')
    return img


def create_image(htext, sizexy, rset):
    hexhash = generate_hash(htext)
    is_set_with_subsets, subdirs = set_with_subsets(rset)
    if is_set_with_subsets:
        number_from_hash = int(hexhash[-8:], 16) % len(subdirs)
        fset = os.path.join(rset, subdirs[number_from_hash])
        hexhash = hexhash[:-8]
        subdir_fingerprint = str(number_from_hash)
    else:
        fset = rset
        subdir_fingerprint = ''
    all_files = get_all_image_parts(fset)
    img_parts, fingerprint = select_image_parts(all_files, hexhash)
    image = paint_image(img_parts).resize((sizexy, sizexy), Image.ANTIALIAS)
    final_fingerprint = f'{subdir_fingerprint}{fingerprint}'
    return image, final_fingerprint


def hash2image(htext, image_set='coats', sizexy=300):
    if image_set not in (
        'cats', 'coats', 'monsters', 'people', 'robotfaces', 'robots'):
        image_set = 'monsters'
    if sizexy > 4096:
        sizexy = 1024
    elif sizexy < 0:
        sizexy = 300
    imagef, fingerprint = create_image(htext, sizexy, image_set)
    imagef.save(f'{htext}.{fingerprint}.png', format='png')
