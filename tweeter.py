import argparse
from pathlib import Path
import tweepy
from secrets import twitter

def connect():
    # Your app's API/consumer key and secret can be found under the Consumer Keys
    # section of the Keys and Tokens tab of your app, under the
    # Twitter Developer Portal Projects & Apps page at
    # https://developer.twitter.com/en/portal/projects-and-apps
    consumer_key = twitter["consumer_key"]
    consumer_secret = twitter["consumer_secret"]
    # Your account's (the app owner's account's) access token and secret for your
    # app can be found under the Authentication Tokens section of the
    # Keys and Tokens tab of your app, under the
    # Twitter Developer Portal Projects & Apps page at
    # https://developer.twitter.com/en/portal/projects-and-apps
    access_token = twitter["access_token"]
    access_token_secret = twitter["access_token_secret"]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    return api



if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--filename", help="image file name", default=None)
    ap.add_argument("-t", "--text", help="Tweet text")
    args = vars(ap.parse_args())
    filename = args.get("filename")
    tweet = args.get("text")

    if not tweet:
        print("Missing tweet body (use -t)")
        exit()

    spaces = "                                                           "
    tweet += "  instagram.com/vis_plastica visplastica.com"
    tweet += spaces + "#AIart #GenerativeArt #MachineLearning #jetsonnano"

    #import pdb; pdb.set_trace()
    api = connect()

    if filename is not None:
        file_path = Path(filename)
        if not file_path.is_file():
            print('Cannot find ', filename)
            exit()
        # Upload image
        media = api.media_upload(filename)
        # Post tweet with image
        post_result = api.update_status(status=tweet, media_ids=[media.media_id])
    else:
      # Post text-only tweet
      post_result = api.update_status(status=tweet)


