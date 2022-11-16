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
        url = "http://127.0.0.1:8000/chan-share-ytb/api/0.0/songs/"
        b = {'url_ytb':'https://www.youtube.com/watch?v=algNQYMP8Qs'}
        h = {'Authorization':f'Bearer {token}'}
        r = requests.post(url, data=b, headers=h)
        id = r.json()['id']
        assert r.status_code == 201
