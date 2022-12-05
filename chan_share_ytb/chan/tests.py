import requests
import json
import logging


class TestSong:

    def get_token(self):
        url = 'http://127.0.0.1:8000/chan-share-ytb/api/0.0/token/'
        body = {'username':'admin','password':'admin'}
        r = requests.post(url, data=body)
        return r.json()['access']

    def test_basic_crud(self):
        token = self.get_token()
        # LIST
        url = "http://127.0.0.1:8000/chan-share-ytb/api/0.0/songs/"
        h = {'Authorization':f'Bearer {token}'}
        r = requests.get(url, headers=h)
        assert r.status_code == 200
        # DETAIL
        url = "http://127.0.0.1:8000/chan-share-ytb/api/0.0/songs/1"
        h = {'Authorization':f'Bearer {token}'}
        r = requests.get(url, headers=h)
        assert r.status_code == 200
        # CREATE
        url = "http://127.0.0.1:8000/chan-share-ytb/api/0.0/songs/"
        b = {'url_ytb':'https://www.youtube.com/watch?v=algNQYMP8Qs'}
        h = {'Authorization':f'Bearer {token}'}
        r = requests.post(url, data=b, headers=h)
        id = r.json()['id']
        assert r.status_code == 201
        # DELETE
        url = f'http://127.0.0.1:8000/chan-share-ytb/api/0.0/songs/{id}'
        b = {'url_ytb':'https://www.youtube.com/watch?v=algNQYMP8Qs'}
        h = {'Authorization':f'Bearer {token}'}
        r = requests.delete(url, headers=h)
        assert r.status_code == 201

    def test_create_download_delete(self):
        # CREATE
        token = self.get_token()
        url = "http://127.0.0.1:8000/chan-share-ytb/api/0.0/songs/"
        b = {'url_ytb':'https://www.youtube.com/watch?v=algNQYMP8Qs'}
        h = {'Authorization':f'Bearer {token}'}
        r = requests.post(url, data=b, headers=h)
        id = r.json()['id']
        assert r.status_code == 201

    def test_delete(self):
        token = self.get_token()
        url = "http://127.0.0.1:8000/chan-share-ytb/api/0.0/songs/"
        h = {'Authorization':f'Bearer {token}'}
        r = requests.get(url, headers=h)
        assert r.status_code == 200
        for song in r.json()['results']:
            url = f"http://127.0.0.1:8000/chan-share-ytb/api/0.0/songs/{song['id']}"
            r = requests.delete(url, headers=h)
            assert r.status_code == 204

class TestPlaylist:

    def get_token(self):
        url = 'http://127.0.0.1:8000/chan-share-ytb/api/0.0/token/'
        body = {'username':'admin','password':'admin'}
        r = requests.post(url, data=body)
        return r.json()['access']

    def test_list(self):
        token = self.get_token()
        # LIST
        url = "http://127.0.0.1:8000/chan-share-ytb/api/0.0/playlists/"
        h = {'Authorization':f'Bearer {token}'}
        r = requests.get(url, headers=h)
        print(r.status_code)
        print(r.json())
        assert r.status_code == 200

    def test_create(self):
        token = self.get_token()
        # LIST
        url = "http://127.0.0.1:8000/chan-share-ytb/api/0.0/playlists/"
        b = {'title':'mytitle', 'mode': 'PB'}
        h = {'Authorization':f'Bearer {token}'}
        r = requests.post(url, data=b, headers=h)
        print(r.status_code)
        print(r.json())
        assert r.status_code == 201

class TestUser:

    def get_token(self):
        url = 'http://127.0.0.1:8000/chan-share-ytb/api/0.0/token/'
        body = {'username':'admin','password':'admin'}
        r = requests.post(url, data=body)
        return r.json()['access']

    def test_list(self):
        token = self.get_token()
        # LIST
        url = "http://127.0.0.1:8000/chan-share-ytb/api/0.0/users/"
        h = {'Authorization':f'Bearer {token}'}
        r = requests.get(url, headers=h)
        print(r.status_code)
        print(r.json())
        assert r.status_code == 200

    def test_create(self):
        token = self.get_token()
        # LIST
        url = "http://127.0.0.1:8000/chan-share-ytb/api/0.0/playlists/"
        b = {'title':'mytitle', 'mode': 'PB'}
        h = {'Authorization':f'Bearer {token}'}
        r = requests.post(url, data=b, headers=h)
        print(r.status_code)
        print(r.json())
        assert r.status_code == 201
