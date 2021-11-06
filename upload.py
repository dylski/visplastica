import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--filename", help="file base name")
args = vars(ap.parse_args())
basename = args.get("filename")

import os
for s in [1, 2, 3, 4]:
    filename = "{}_x{}.png".format(basename, s)
    local_name = "done/" + filename
    os.system("scp {} USERNAME@DOMAIN.COM:DIRECTORY/{}".format(local_name, filename))
