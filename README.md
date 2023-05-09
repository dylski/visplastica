# Vis Plastica
## Constantly generating AI-generated images on a low-end computer.

![Grey Skies by Piet Mondrian](https://github.com/dylski/visplastica/blob/main/examples/gray_skies_by_Piet_Mondrian.png?raw=true)

*Grey Skies by Piet Mondrian*

This project is running 24/7 on a single-board computer, feeding images to [@visplastica](https://twitter.com/VisPlastica) and [visplastica.com](https://www.visplastica.com)

The Jetson Nano is a sort-of Raspberry Pi with 128 CUDA cores. An image usingi the CLIPDraw algorithm takes about 4-5 hours with CUDA and 8-9 hours with CPU.
This may work on a 4GB Raspberry Pi 4 with 64bit Raspbian OS; possibly slightly faster than the Nano's CPU time due to faster CPUs.

Currently the only AI-painting algorithm implemented is [CLIPDraw](https://github.com/kvfrans/clipdraw) but I'll introduce others if they are feasible.

[![Twitter URL](https://img.shields.io/twitter/url/https/twitter.com/visplastica.svg?style=social&label=Follow%20%40visplastica)](https://twitter.com/visplastica)
## Caveats

1) These instructions are only based on my experiences with the Jetson Nano 4GB, JetPack 4.6.
1) Looks like most of the 4GB is being used so the 2GB version may not work.
1) I'm running without desktop GUI. If you have the desktop running you may encounter memory issues.
1) Requires python 3.7 which is not installed by default.
1) I'm powering through the DC power socket with an average current usage us 3.6A

## Installation
Here are my notes from setting up the nano.
```
# NOTE use 'pip --default-timeout=1000 ...' if you have timeouts which I had with tensorboard

sudo apt-get install python3.7
sudo apt-get install python3.7-venv
python3.7 -m venv venv
. venv/bin/activate

# I found pip to be broken at this point (TypeError: expected str, bytes or os.PathLike object, not int)
# It might be fixed by now but if not here's how to upgrade to a working version
python -m pip --no-cache-dir install pip --upgrade

pip3 install nvidia-pyindex
pip3 install wget
pip3 install Cython
pip3 install wheel
pip3 install svgpathtools
pip3 install numpy
pip3 install cpython
pip3 install cssutils
pip3 install pycuda
pip3 install tweepy

# https://forums.developer.nvidia.com/t/instll-python-packages-librosa-and-llvm-on-jetson-nano-developer-kit-problem/74543/9
sudo apt-get install llvm-10
cd /usr/bin
sudo ln -s llvm-config-10 llvm-config

pip3 install numba
pip3 install torch-tools
pip3 install visdom
pip3 install ftfy regex tqdm
pip3 install git+https://github.com/openai/CLIP.git --no-deps
```
Next is needed CUDA-enabled pytorch for python 3.7 which is not readily available yet.
I followed instructions at https://qengineering.eu/install-pytorch-on-jetson-nano.html where they also have instructions for the Raspberry Pi.
Although note that the files to edit has changed for torch 10.
* pytorch/aten/src/ATen/cpu/vec/vec256/vec256_float_neon.h
* Now gone: aten/src/THCUNN/common.h

I had to increase the swap space from 2GB to 4GB to build pytorch. The build takes about 12 hours! This creates a 'wheel' file that you install with ```pip install name_of_wheel_file.whl``` Alternatively try using the one I built [torch-1.10.0a0+git36449ea-cp37-cp37m-linux_aarch64.whl](https://drive.google.com/file/d/1BSJHVRIDSHv2lg50GTIrHJG938euoD6T/view?usp=sharing) from Google Drive.

After installing the CUDA-enabled torch it is time to build diffvg.

First you need to update CMake as we need version > 3.10
These instructions are from https://askubuntu.com/questions/355565/how-do-i-install-the-latest-version-of-cmake-from-the-command-line
```
sudo apt purge --auto-remove cmake
sudo apt update && sudo apt install -y software-properties-common lsb-release && sudo apt clean all
wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | sudo tee /etc/apt/trusted.gpg.d/kitware.gpg >/dev/null
sudo apt-add-repository "deb https://apt.kitware.com/ubuntu/ $(lsb_release -cs) main"
sudo apt update
sudo apt install kitware-archive-keyring
sudo apt update
sudo apt install cmake
```
Now build and install diffvg
```
git clone https://github.com/BachiLi/diffvg
cd diffvg
git submodule update --init --recursive
                                                                                                                                                                                                                                                                                                                                                          30,0-1        Top
cd diffvg
git submodule update --init --recursive
python setup.py install
```
That should be all the installations!

For reference this will install everything I have in my virtual env (probably more than necessary):
```
python -m pip install -r requirements.txt

```
Finally, configure upload.py and tweeter.py with your details for web upload and twitter if desired.

To run with more than 384 line segments without CUDA timeout errors you need to deactivate the timeout:
```
sudo sh -c 'echo N >/sys/kernel/debug/57000000.gpu/timeouts_enabled'
```
# Usage
Remember to activate the python environment before running
```source venv/bin/activate```
## Single CLIPDraw image

`python clip_draw.py -p "An Aardvark in a disco" -f aarvark_disco -i 500`

## Random painting followed by posting and upload. Forever.
Edit `secrets_template.py` with your creditials for upload and posting and save as `secrets.py`. 
Alternatively, comment out relevant lines in `get_painting.sh`.

To generate images forever:
```
./get_painting.sh
```
Note `subjects.txt` contains the possible painting titles and `artists.txt` the artist styles.


# Notes
##  Patch sets
The online patch set file names taken from the Colab:
 
* Fruit and veg : fruit.npy
* Sea glass : shore_glass.npy
* Handwritten MNIST : handwritten_mnist.npy
* Animals : animals.npy
* Animal Forms: animal_forms.npy
* Plant Forms: plant_forms.npy
* Waste: waste.npy
* Human artefacts: human_artefacts.npy
* Leaves: open_leaves.npy
* Broken plate: broken_plate.npy
* Natural forms: natural_forms.npy
