# coding=utf-8
import json
import markovify
import numpy as np

from random import random
import requests
from flask import request, Flask

app = Flask(__name__)

token = 'EAAGAJhMhKRABAFbFsT55sDbAfalbtB2ZCZCbEzxZARGZBGVgARFTslOfQGTCLmIWV1zN7KbUY2qezIGmrobdbA2HkCvKo7gerksQbXhKpkhgteqCZA3R98M0XFZAwZCHdO7F2hUaRkxT9elEqF7NyqRFmaEP0g1dZA4IJsWfmX5tTwZDZD'  # noqa


@app.route('/receive', methods=['GET'])
def serve():
    if (
        request.args.get('hub.mode') == 'subscribe' and
        request.args.get('hub.verify_token') == 'moo'
    ):
        return request.args.get('hub.challenge')
    return 'arimooster'


mooster_resps = [
    "🐮s are social animals, and they naturally form large herds. And like people, they will make friends and bond to some herd members, while avoiding others",
    "🐮s are red-green colorblind. In a bullfight, its the waving of the cape that attracts the bull not the red color",
    "A 🐮's heart beats between 60 and 70 beats per minute",
    "🐮s can hear lower and higher frequencies better than humans.",
    "An average dairy 🐮 weighs about 1,200 pounds.",
    "A 🐮s normal body temperature is 101.5°F.",
    "The average 🐮 chews at least 50 times per minute.",
    "The typical 🐮 stands up and sits down about 14 times a day.",
    "An average 🐮 has more than 40,000 jaw movements in a day.",
    "🐮s actually do not bite grass; instead they curl their tongue around it.",
    "🐮s have almost total 360-degree panoramic vision.",
    "🐮s have a single stomach, but four different digestive compartments.",
    "🐮s are pregnant for 9 months just like people",
    "A dairy 🐮 can produce 125 lbs. of saliva a day",
    "🐮s spend 8 hours per day eating, 8 hours chewing her cud (regurgitated, partially digested food), and 8 hours sleeping",
    "You can lead a 🐮 upstairs, but not downstairs. 🐮s knees can't bend properly to walk downstairs.",
    "🐮s can't vomit",
    "The average 🐮 drinks 30 to 50 gallons of water each day",
    "The average 🐮 produces 70 lbs. of milk. That's 8 gallons per day!",
    "🐮s only have teeth on the bottom",
    "🐮s have a great sense of smell. They can smell something up to 6 miles away",
    "Dairy 🐮s are economic job creating machines! 1 dairy 🐮 creates 4 full time jobs in the local community",
    "A Holstein's spots are like a fingerprint. No two 🐮s have exactly the same pattern of black and white spots. They are all different",
    "The average 🐮 will eat about 100 lbs. of feed per day",
    "Like humans, 🐮s (🐮s) form close friendships and choose to spend much of their time with 2-4 preferred individuals. They also hold grudges for years and may dislike particular individuals.",
    "🐮s display emotions and have been shown to produce more milk when they are treated better and as individuals.",
    "🐮s get excited when they solve problems. When faced with the challenge of trying find out how to open a door to reach food, their heartbeats went up, their brainwaves showed excitement, and some even jumped into the air.",
    "🐮s show their excitement when let out into a field after long periods confined indoors.",
    "🐮s like to sleep close to their families, and sleeping arrangements are determined by individuals’ rank in the social hierarchy.",
    "🐮s are devotional mothers and are known to walk for miles to find their calves.",
    "🐮s are extremely curious and inquisitive animals which will investigate everything.",
    "Like many other grazing animals 🐮s have one stomach which is divided into four compartments or chambers: the rumen, reticulum, omasum and abomasum. This allows them to digest grain and grasses most effectively.",
    "🐮s have almost 360° panoramic vision. This helps them to see predators coming from any direction.",
    "🐮s have an excellent sense of smell. They can detect odours up to five miles away. They can also hear both low and high frequency sounds beyond human capability.",
    "The 🐮 is a protected animal in Hinduism, and Hindus do not eat beef. 🐮s are honoured at least once a year, on Gopastami. On this day 🐮s are washed and decorated in temples.",
    "Mahatma Ghandi described a 🐮 as “a poem of compassion”, also stating that “I worship the 🐮 and I shall defend its worship against the whole world”.",
    "The meat of 🐮s is widely eaten by people across the world. 🐮s’ milk is also drunk and used to make other products such as cheese and butter. Many people who consume animal products would like to choose products from animals kept in higher welfare systems. The majority of 🐮s farmed across the world are reared in intensive farming systems which can cause them to suffer greatly.",
]

def generate_ari_speech():
    # Get raw text as string.
    with open("ari_parsed_text.txt") as f:
        text = f.read()

    # Build the model.
    text_model = markovify.Text(text)

    # Print five randomly-generated sentences
    num_sentences = max(1, int(round(np.random.normal(3, 2, 1)[0], 0)))

    sentences = []
    print num_sentences
    for i in range(num_sentences):
        sentences.append(text_model.make_sentence(tries=1000))

    sentences = " ".join(sentences)

    return sentences

@app.route('/receive', methods=['POST'])
def receive():
    print(request.data)
    data = json.loads(request.data)

    sentences = generate_ari_speech()

    try:
        for entry in data['entry']:
            for message in entry['messaging']:
                sender = message['sender']['id']
                content = message['message']['text']

                resp_msg = {
                    'recipient': {
                        'id': sender,
                    },
                    'message': {
                        'text': sentences,
                    },
                }

                response = requests.post(
                    'https://graph.facebook.com/v2.6/me/messages',
                    params={'access_token': token},
                    json=resp_msg,
                )
                print('Sent requests %s' % json.dumps(resp_msg))
                print('Received response %s' % response.text)
    except Exception as e:
        print(e)
        return 'not handled'

    return 'success'
