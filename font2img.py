import argparse
from glob import glob
import json
import os
import unicodedata

import fontforge

parser = argparse.ArgumentParser(description='Convert font file to images')
parser.add_argument('--resolution', type=int, default=320, metavar='R',
                    help='image resolution (default: 320)')

args = parser.parse_args()

with open('fonts/cjk.json') as handle:
    cjk_dict = json.load(handle)

CN_CHARSET = cjk_dict["gbk"]
charset_list = []

for u in CN_CHARSET:
    try: 
        charset_list.append(unicodedata.name(u).split('-')[-1])
        # print(u)
    except:
        pass

ttf_list = glob('fonts/*.ttf')
ttc_list = glob('fonts/*.ttc')
otf_list = glob('fonts/*.otf')

font_list = ttf_list + ttc_list + otf_list
fail_list = []

for filename in font_list:
    print("===========================")
    print("Processing font: {}".format(filename))
    print("===========================")
    abs_path = os.path.abspath(filename)
    path_stem = abs_path.split('.')[0]
    stem, ext = os.path.splitext(filename)

    if not os.path.isdir(path_stem + '/' + str(args.resolution) + '/'):
        os.makedirs(path_stem + '/' + str(args.resolution) + '/')

    try:
        F = fontforge.open(filename)
    except:
        print("Failed to process {}".format(filename))
        fail_list.append(filename)
        continue

    for name in F:
        if 'uni' in name and name[3:] in charset_list:
            filename = name[3:] + ".png"
            path_list = [path_stem, str(args.resolution), filename]
            try:
                F[name].export('/'.join(path_list), args.resolution)
            except:
                print("Failed to export character: {}".format(name[3:]))




