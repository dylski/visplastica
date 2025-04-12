import argparse
from atproto import Client, models # Import models for embed structure
from pathlib import Path
from secrets import bluesky # Assuming secrets.py contains: bluesky = {'username': 'YOUR_USERNAME', 'key': 'YOUR_APP_PASSWORD'}
import sys # To use sys.exit()

# https://docs.bsky.app/docs/advanced-guides/posts
# https://atproto.blue/en/latest/atproto_client/api.html#atproto_client.client.client.Client.send_post

def post(text, filename=None):
    """
    Logs into Bluesky and sends a post, optionally with an image.

    Args:
        text (str): The text content of the post.
        filename (str, optional): The path to the image file to attach. Defaults to None.
    """
    try:
        client = Client()
        print("Logging into Bluesky...")
        client.login(bluesky['username'], bluesky['key'])
        print(f"Logged in as {bluesky['username']}")

        image_embed = None
        if filename:
            print(f"Uploading image: {filename}...")
            img_path = Path(filename)
            if not img_path.is_file():
                 print(f"Error: Image file not found at {filename}")
                 return # Exit the function if image not found

            try:
                with open(img_path, 'rb') as f:
                    img_data = f.read()
                    # Upload the image data to get a blob reference
                    upload_response = client.upload_blob(img_data)
                    print("Image uploaded successfully.")

                    # Create the image embed structure
                    image_embed = models.AppBskyEmbedImages.Main(
                        images=[
                            models.AppBskyEmbedImages.Image(
                                alt=text[:100],  # Use post text for alt text (max 1000 chars, but keep it reasonable)
                                image=upload_response.blob # Reference the uploaded blob
                            )
                        ]
                    )
            except Exception as e:
                print(f"Error uploading image: {e}")
                return # Exit if image upload fails

        print("Sending post...")
        # Use **{'embed': image_embed} syntax to conditionally add the embed
        # If image_embed is None, it won't be added to kwargs
        post_response = client.send_post(
            text=text,
            **({'embed': image_embed} if image_embed else {})
        )
        print(f"Post successful! URI: {post_response.uri}")
        print(f"Post CID: {post_response.cid}")

    except Exception as e:
        print(f"An error occurred during the posting process: {e}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Post text and optionally an image to Bluesky.")
    ap.add_argument("-f", "--filename", help="Path to the image file name", default=None)
    ap.add_argument("-t", "--text", help="Post text", required=True) # Made text required
    args = vars(ap.parse_args())

    filename_arg = args.get("filename")
    post_text_arg = args.get("text")

    # No need for this check as argparse handles 'required=True'
    # if not post_text_arg:
    #     print("Missing post body (use -t)")
    #     sys.exit(1) # Use sys.exit for cleaner exit

    # Append additional text/hashtags
    # Consider making these optional via args too
    # post_text_arg += " @visplastica.com" # Be careful with mentions if not intended
    post_text_arg += " #AIart #GenerativeArt #MachineLearning #jetsonnano" # Example hashtags

    # Basic validation for filename if provided (detailed check is now in the post function)
    if filename_arg is not None:
        print(f"Preparing to post with text and image: {filename_arg}")
        file_path = Path(filename_arg)
        if not file_path.is_file():
             # Check before calling post to avoid unnecessary login attempt if file is missing
            print(f'Error: Cannot find image file: {filename_arg}')
            sys.exit(1)
        # Call post function with image
        post(text=post_text_arg, filename=filename_arg)
    else:
        print("Preparing to post text only.")
        # Call post function without image
        post(text=post_text_arg)

    print("Script finished.")
