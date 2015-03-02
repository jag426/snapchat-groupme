from argparse import ArgumentParser
from snapchat_bots import SnapchatBot
import json
import requests

class GroupmeBot(SnapchatBot):
    def __init__(self, username, password, botid, token):
        SnapchatBot.__init__(self, username, password)
        self.botid = botid
        self.token = token

    def on_snap(self, sender, snap):
        """
        On snap, upload image to groupme image service, then use groupme 
        image URL to post it to the group
        """
        # Make sure the snap is an image. GroupMe doesn't expose an API for
        # uploading videos.
        # todo: magic number!
        if snap.media_type != 0:
            # not an image. abort.
            print("Ignoring non-image snap.")
            return
        # upload image to groupme image service
        headers = {'content-type': 'application/json'}
        url = 'https://image.groupme.com/pictures'
        files = {'file': open(snap.file.name, 'rb')}
        payload = {'access_token': self.token}
        r = requests.post(url, files=files, params=payload)
        imageurl = r.json()['payload']['url']
        # post image to groupme
        url = 'https://api.groupme.com/v3/bots/post'
        payload = {'bot_id': self.botid, 'text': 'snap from ' + sender,
                'attachments': [
                    {
                        'type': 'image',
                        'url': imageurl
                    }
                ]
        }
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        print("Posted snap from " + sender + ".")

    def on_friend_add(self, friend):
        """ Add anyone who adds me """
        self.add_friend(friend)

    def on_friend_delete(self, friend):
        """ Delete anyone who deletes me """
        self.delete_friend(friend)

if __name__ == '__main__':
    parser = ArgumentParser("Groupme Bot")
    parser.add_argument(
            '-u', '--username', required=True, type=str,
            help="Snapchat username to run the bot on")
    parser.add_argument(
            '-p', '--password', required=True, type=str,
            help="Snapchat password")
    parser.add_argument(
            '-b', '--botid', required=True, type=str,
            help='Groupme bot id')
    parser.add_argument(
            '-t', '--token', required=True, type=str,
            help='Groupme access token')

    args = parser.parse_args()

    bot = GroupmeBot(args.username, args.password, args.botid, args.token)
    bot.listen(timeout=5)
