import argparse
from atproto import Client
from pathlib import Path
from secrets import bluesky
# https://docs.bsky.app/docs/advanced-guides/posts


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--filename", help="image file name", default=None)
    ap.add_argument("-t", "--text", help="Tweet text")
    args = vars(ap.parse_args())

    filename = args.get("filename")
    text = args.get("text")

    if not text:
        print("Missing text body (use -t)")
        exit()

    text += "@visplastica.com"
    text += " #AIart #GenerativeArt #MachineLearning #jetsonnano"

    if filename is not None:
        file_path = Path(filename)
        if not file_path.is_file():
            print('Cannot find ', filename)
            exit()

        # Upload image
        # Post text with image
        with open(filename, 'rb') as f:
            img_data = f.read()

        client = Client()
        client.login(bluesky['username'], bluesky['key'])
        client.send_image(text=text, image=img_data, image_alt=f'AI generated collage of {text}')
    
    else:
        print("No Image")
        exit(1)
        # client = Client()
        # client.login(bluesky['username'], bluesky['key'])
        # post = client.send_post('Hello world! I posted this via the Python SDK.')

