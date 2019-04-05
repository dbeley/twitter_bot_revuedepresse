import datetime
import locale
import argparse
import configparser
import tweepy
import time
import logging
from pathlib import Path

logger = logging.getLogger()
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
temps_debut = time.time()
config = configparser.ConfigParser()
config.read('config.ini')
locale.setlocale(locale.LC_TIME, "fr_FR.utf-8")
jour = datetime.datetime.now().strftime("%A %d %B %Y")
auj = datetime.datetime.now().strftime("%Y-%m-%d")


def tweet_image(api, filename, title):
    message = f'''{title} du {jour}
#revuedepresse
    '''
    api.update_with_media(filename, status=message)


def twitterconnect():
    ConsumerKey = config['twitter']['ConsumerKey']
    SecretKey = config['twitter']['SecretKey']
    AccessToken = config['twitter']['AccessToken']
    AccessTokenSecret = config['twitter']['AccessTokenSecret']

    auth = tweepy.OAuthHandler(ConsumerKey, SecretKey)
    auth.set_access_token(AccessToken, AccessTokenSecret)
    return tweepy.API(auth)


def main():
    args = parse_args()
    # test = args.test
    international = args.international

    api = twitterconnect()

    if international:
        directory = f"Images/{auj}_international"
    else:
        directory = f"Images/{auj}"
    p = Path(directory).glob('**/*')

    for file in sorted(p):
        name = file.stem.split('_', 1)[-1].replace("_", " ")
        print(name)
        # print(file)
        tweet_image(api, str(file), name)


def parse_args():
    parser = argparse.ArgumentParser(description='Twitter bot')
    parser.add_argument('--debug', help="Display debugging information", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO)
    parser.add_argument('-i', '--international', help="International mode (parse the international version)", dest='international', action='store_true')
    parser.set_defaults(international=False)
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    return args


if __name__ == '__main__':
    main()
