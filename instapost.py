import argparse
import json
import requests
from secrets import instagram
import time

ap = argparse.ArgumentParser()
ap.add_argument("-u", "--url", help="URL to image")
ap.add_argument("-t", "--text", help="Text to post")
args = vars(ap.parse_args())
url = args.get("url")
text = args.get("text")

if url is None or text is None:
    raise ValueError("Missing args")

ig_user_id = instagram["ig_user_id"]
user_access_token = instagram["user_access_token"]
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
        return False
    return True

url = "https://www.visplastica.com/gallery/" + url
text += "                                                            Click bio for info and code. #AIart #GenerativeArt #MachineLearning #jetsonnano"
print("Posting {} with caption {}".format(url, text))
for tries in range(5):
    if postInstagramQuote(url, text):
        break
    time.sleep(10)
    
