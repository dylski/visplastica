"""
Copyright 2021 Kevin Frans
Copyright 2021 Dylan Banarse

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


CLIP Draw

Uses CLIPDraw process develoepd by Kevin Frans, et al 
to generate images from line strokes that match a text prompt. 
The image generator is guided by gradients from the OpenAI CLIP model which 
assess how close the generated image to the text prompt.
Intermediate images are saved as latest.png in the current directory.
Final outputs (image at different scales) are saved in the directory 'done'. 


Heavily based on CLIPDraw Colab from Kevin Frans, et al.
https://www.crosslabs.org/blog/clipdraw-exploring-text-to-drawing-synthesis
"""


import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prompt", help="text prompt", default="a chicken")
ap.add_argument("-f", "--filename", help="file base name", default="test")
ap.add_argument("-i", "--iter", help="number of iterations", default="500")
args = vars(ap.parse_args())
prompt = args.get("prompt")
filename = args.get("filename")
num_iter = int(args.get("iter"))

import base64
import clip
import io
import matplotlib.pylab as pl
import numpy as np
import os
from pathlib import Path
import pickle
import PIL.Image, PIL.ImageDraw
import pydiffvg
import random
import requests
import subprocess
from subprocess import call
import torch
import torchvision
from torchvision import transforms

orig_prompt = prompt
orig_filename = filename
Path("done").mkdir(parents=True, exist_ok=True)
for i in range(2, 100):
    test_file = Path("done/{}_x1.png".format(filename))
    if test_file.is_file():
        prompt = orig_prompt + " edition {}".format(i)
        filename = orig_filename + "_ed_{}".format(i)
        print("'{}' files already exists, changing prompt to '{}'.".format(
            test_file, prompt))
print('Using prompt "{}" and filename {}'.format(prompt, filename))

neg_prompt = "writing"
neg_prompt_2 = "letters and digits"
use_negative = True  # Use negative prompts?

# ARGUMENTS. Feel free to play around with these, especially num_paths.
args = lambda: None
canvas_width, canvas_height = 224, 224 # 448, 448  # 224, 224
args.num_paths = 1000  # 384 works on Jetson Nano without disabling the gpu timeouts. 1500 takes about 8 hours.
args.num_iter = num_iter  # 500 is generally good with 1000 lines.
args.max_width = 480  # (reset to 480 from the 24/11/2021, was 300)  # Large like 480 enables background fill-type effects.

CUDA_version = [s for s in subprocess.check_output(
    ["nvcc", "--version"]).decode("UTF-8").split(", ") if s.startswith(
        "release")][0].split(" ")[-1]
print("CUDA version:", CUDA_version)
if CUDA_version == "10.0":
    torch_version_suffix = "+cu100"
elif CUDA_version == "10.1":
    torch_version_suffix = "+cu101"
elif CUDA_version == "10.2":
    torch_version_suffix = ""
else:
    torch_version_suffix = "+cu110"
print("Torch version:", torch.__version__)

# Load the model
print("Loading CLIP model")
# Might be able to use 'cpu' if running on Raspberry Pi?
device = torch.device('cuda')
# model, preprocess = clip.load('ViT-B/32', device, jit=False)
model, preprocess = clip.load('clip_models/ViT-B-32.pt', device, jit=False)

text_input = clip.tokenize(prompt).to(device)
text_input_neg1 = clip.tokenize(neg_prompt).to(device)
text_input_neg2 = clip.tokenize(neg_prompt_2).to(device)

# Thanks to Katherine Crowson for this. 
# In the CLIPDraw code used to generate examples, we don't normalize images
# before passing into CLIP, but really you should. Set this to True to do that.
use_normalized_clip = True 

# Calculate features
with torch.no_grad():
    text_features = model.encode_text(text_input)
    text_features_neg1 = model.encode_text(text_input_neg1)
    text_features_neg2 = model.encode_text(text_input_neg2)

pydiffvg.set_print_timing(False)

gamma = 1.0

# Use GPU if available
pydiffvg.set_use_gpu(torch.cuda.is_available())
pydiffvg.set_device(device)

num_paths = args.num_paths
max_width = args.max_width

# Image Augmentation Transformation
augment_trans = transforms.Compose([
    transforms.RandomPerspective(fill=1, p=1, distortion_scale=0.5),
    transforms.RandomResizedCrop(224, scale=(0.7,0.9)),
])

if use_normalized_clip:
    augment_trans = transforms.Compose([
    transforms.RandomPerspective(fill=1, p=1, distortion_scale=0.5),
    transforms.RandomResizedCrop(224, scale=(0.7,0.9)),
    transforms.Normalize((0.48145466, 0.4578275, 0.40821073),
        (0.26862954, 0.26130258, 0.27577711))
])


# Initialize Random Curves
shapes = []
shape_groups = []
for i in range(num_paths):
    num_segments = random.randint(1, 3)
    num_control_points = torch.zeros(num_segments, dtype = torch.int32) + 2
    points = []
    p0 = (random.random(), random.random())
    points.append(p0)
    for j in range(num_segments):
        radius = 0.02
        p1 = (p0[0] + radius * (random.random() - 0.5),
                p0[1] + radius * (random.random() - 0.5))
        p2 = (p1[0] + radius * (random.random() - 0.5),
                p1[1] + radius * (random.random() - 0.5))
        p3 = (p2[0] + radius * (random.random() - 0.5),
                p2[1] + radius * (random.random() - 0.5))
        points.append(p1)
        points.append(p2)
        points.append(p3)
        p0 = p3
    points = torch.tensor(points)
    points[:, 0] *= canvas_width
    points[:, 1] *= canvas_height
    path = pydiffvg.Path(num_control_points=num_control_points, points=points, 
            stroke_width=torch.tensor(1.0), is_closed=False)
    shapes.append(path)
    path_group = pydiffvg.ShapeGroup(
            shape_ids=torch.tensor([len(shapes) - 1]), fill_color = None,
            stroke_color = torch.tensor([random.random(), random.random(),
                random.random(), 0.8 * random.random()]))
    shape_groups.append(path_group)

# Just some diffvg setup
scene_args = pydiffvg.RenderFunction.serialize_scene(\
    canvas_width, canvas_height, shapes, shape_groups)
render = pydiffvg.RenderFunction.apply
img = render(canvas_width, canvas_height, 2, 2, 0, None, *scene_args)
points_vars = []
stroke_width_vars = []
color_vars = []
for path in shapes:
    path.points.requires_grad = True
    points_vars.append(path.points)
    path.stroke_width.requires_grad = True
    stroke_width_vars.append(path.stroke_width)
for group in shape_groups:
    group.stroke_color.requires_grad = True
    color_vars.append(group.stroke_color)


# Optimizers
points_optim = torch.optim.Adam(points_vars, lr=1.0)
width_optim = torch.optim.Adam(stroke_width_vars, lr=0.1)
color_optim = torch.optim.Adam(color_vars, lr=0.01)

# Run the main optimization loop
for t in range(args.num_iter):

    # Anneal learning rate (makes videos look cleaner)
    if t == int(args.num_iter * 0.5):
        for g in points_optim.param_groups:
            g['lr'] = 0.4
    if t == int(args.num_iter * 0.75):
        for g in points_optim.param_groups:
            g['lr'] = 0.1

    points_optim.zero_grad()
    width_optim.zero_grad()
    color_optim.zero_grad()
    scene_args = pydiffvg.RenderFunction.serialize_scene(\
        canvas_width, canvas_height, shapes, shape_groups)
    img = render(canvas_width, canvas_height, 2, 2, t, None, *scene_args)
    # Include if you want a white background
    img = img[:, :, 3:4] * img[:, :, :3] + torch.ones(
            img.shape[0], img.shape[1], 3, 
            device=pydiffvg.get_device()) * (1 - img[:, :, 3:4])
    img = img[:, :, :3]
    if t % 50 == 0:
        pydiffvg.imwrite(img.cpu(), './latest.png', gamma=gamma)
    img = img.unsqueeze(0)
    img = img.permute(0, 3, 1, 2) # NHWC -> NCHW

    loss = 0
    NUM_AUGS = 4
    img_augs = []
    for n in range(NUM_AUGS):
        img_augs.append(augment_trans(img))
    im_batch = torch.cat(img_augs)
    image_features = model.encode_image(im_batch)
    for n in range(NUM_AUGS):
        loss -= torch.cosine_similarity(
                text_features, image_features[n:n+1], dim=1)
        if use_negative:
            loss += torch.cosine_similarity(
                    text_features_neg1, image_features[n:n+1], dim=1) * 0.3
            loss += torch.cosine_similarity(
                    text_features_neg2, image_features[n:n+1], dim=1) * 0.3

    # Backpropagate the gradients.
    loss.backward()

    # Take a gradient descent step.
    points_optim.step()
    width_optim.step()
    color_optim.step()
    for path in shapes:
        path.stroke_width.data.clamp_(1.0, max_width)
    for group in shape_groups:
        group.stroke_color.data.clamp_(0.0, 1.0)
    
    if t % 50 == 0:
        print('render loss:', loss.item())
        print('iteration:', t)

print("Saving {} images for prompt '{}'".format(filename, prompt))
scene_args = pydiffvg.RenderFunction.serialize_scene(\
            canvas_width, canvas_height, shapes, shape_groups)

pickled = f"done/{filename}.pt"
with open(pickled, 'wb') as handle:
    pickle.dump(scene_args, handle)

svg_filename = f"done/{filename}.svg"
pydiffvg.save_svg(svg_filename, canvas_width, canvas_height,
                  shapes, shape_groups, use_gamma=False)

# Smallest size
canvas_width, canvas_height = 224, 224
for scale_size in [1, 2, 3, 4, 8]:
    img = render(canvas_width * scale_size, 
            canvas_height * scale_size, 2, 2, args.num_iter, None, *scene_args)
    img = img[:, :, :3]
    pydiffvg.imwrite(img.cpu(), 'done/{}_x{}.png'.format(
        filename, scale_size), gamma=gamma)
