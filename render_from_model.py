import argparse
import pickle

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", help="Name of pickled model state")
ap.add_argument("-s", "--scale", help="Scale as multiple of 224x224")
ap.add_argument("-i", "--iter", help="number of iterations", default="500")
args = vars(ap.parse_args())
filename = args.get("file")
scale = int(args.get("scale"))
# num_iter appears to have NO effect
num_iter = int(args.get("iter"))

import pydiffvg
basename, ext = filename.rsplit(".", 1)
target_file = f"{basename}_x{scale}.png"

with open(filename, 'rb') as handle:
    scene_args = pickle.load(handle)

print("Saving {}".format(target_file))
canvas_width, canvas_height = 224, 224
img = pydiffvg.RenderFunction.apply(
        canvas_width * scale, 
        canvas_height * scale, 2, 2, num_iter, None, *scene_args)
img = img[:, :, :3]
pydiffvg.imwrite(img.cpu(), target_file, gamma=1.0)

