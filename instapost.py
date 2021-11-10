# Post an image and caption to Instagram - based on https://levelup.gitconnected.com/automating-instagram-posts-with-python-and-instagram-graph-api-374f084b9f2b
import requests
import json
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-u", "--url", help="URL to image")
ap.add_argument("-t", "--text", help="Text to post")
args = vars(ap.parse_args())
url = args.get("url")
text = args.get("text")

if url is None or text is None:
    raise ValueError("Missing args")

ig_user_id = "YOUR_IG_USER_ID"
user_access_token = "YOUR_USER_ACCESS_TOKEN"
def postInstagramQuote(url, text):
#Post the Image
    post_url = 'https://graph.facebook.com/v10.0/{}/media'.format(ig_user_id)
    payload = {
        'image_url': url,
        'caption': text,
        'access_token': user_access_token
    }
    r = requests.post(post_url, data=payload)
    print(r.text)
    result = json.loads(r.text)
    if 'id' in result:
        creation_id = result['id']
        second_url = 'https://graph.facebook.com/v10.0/{}/media_publish'.format(ig_user_id)
        second_payload = {
            'creation_id': creation_id,
            'access_token': user_access_token
        }
        r = requests.post(second_url, data=second_payload)
        print('--------Just posted to instagram--------')
        print(r.text)
    else:
        print('HOUSTON we have a problem')

url = "https://www.visplastica.com/gallery/" + url
text += "                    #AIart #GenerativeArt #MachineLearning #jetsonnano"
postInstagramQuote(url, text)
