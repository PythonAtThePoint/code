import random
from PIL import Image, ImageDraw, ImageFont
import requests
import sys


class LastFMError(Exception):
    pass


class LastFMImage:
    def __init__(self, username):
        self.url = "http://ws.audioscrobbler.com/2.0/"
        self.method = "user.gettopartists"
        self.user = username or "alairock"
        self.api_key = '301a3a6d4301644d5a078e7f1fac0e78'
        self.limit = 9
        self.period = '3month'
        self.cache_path = '/Users/alairock/Desktop/demo'
        self.path = None
        self._create_collage()

    def _get_body(self):
        return {
            'method': self.method,
            'user': self.user,
            'api_key': self.api_key,
            'limit': self.limit,
            'period': self.period,
            'format': 'json'
        }

    def get_artists(self):
        r = requests.get(self.url, self._get_body())
        if r.status_code == 403:
            print('cannot access')
            sys.exit()
        if 'error' in r.json():
            raise LastFMError(r.json()['message'])
        artists = r.json()['topartists']['artist']
        return artists

    def _download_file(self, url):
        no = random.randint(1, 1000)
        path = self.cache_path + "/" + 'newfile+{no}.jpg'.format(no=no)
        with open(path, 'wb') as f:
            resp = requests.get(url)
            f.write(resp.content)
        return path

    def _get_images(self, artists):
        image_info = []
        for artist in artists:
            url = artist['image'][3]['#text']
            path = self._download_file(url)
            spot_info = {
                'name': artist['name'],
                'path': path,
            }
            image_info.append(spot_info)
        return image_info

    def _insert_name(self, image, name, cursor):
        draw = ImageDraw.Draw(image, 'RGBA')
        font = ImageFont.truetype(self.cache_path+'/myfont.ttf', size=17)
        x = cursor[0]
        y = cursor[1]
        draw.rectangle([(x, y+200), (x+300, y+240)], (0, 0, 0, 123))
        draw.text((x+8, y+210), name, (255, 255, 255), font=font)

    def _create_collage(self, cols=3, rows=3):
        artists = self.get_artists()
        images = self._get_images(artists)
        w, h = Image.open(images[0]['path']).size
        collage_width = cols * w
        collage_height = rows * h
        final_image = Image.new('RGB', (collage_width, collage_height))
        cursor = (0, 0)
        for image in images:
            # place image
            final_image.paste(Image.open(image['path']), cursor)

            # add name
            self._insert_name(final_image, image['name'], cursor)

            # move cursor
            y = cursor[1]
            x = cursor[0] + w
            if cursor[0] >= (collage_width - w):
                y = cursor[1] + h
                x = 0
            cursor = (x, y)

        final_path = self.cache_path+'/lastfm-final.jpg'
        final_image.save(final_path)
        self.path = final_path
        # final_image.show()
