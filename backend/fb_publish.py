#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from facepy import GraphAPI
import facebook
import requests
from pathlib import Path
from parser import ConfigParser as JsonParser

_company_ = "AWP DIGITAL SOLUTIONS"
_about_ = "Automation software to post media in social media sites."
_developer_ = "Vijay Anand Pandian (https://www.github.com/vijayanandrp)"
_date_ = "26 Jan 2018"

config_file = Path(__file__).parent / "fb_config.json"



class FbPageAPI:
    def __init__(self, _access_token, limit=250):
        self.access_token = _access_token
        self.graph = GraphAPI(self.access_token)
        self.accounts = self._get_accounts(limit)

    def _get_accounts(self, limit=250):
        self.accounts = self.graph.get("me/accounts?limit=" + str(limit))
        return self.accounts["data"]

    def get_accounts(self):
        return self.accounts["data"]

    def get_page_access_token(self, _page_id):
        """
        :param _page_id:
        :return: page_specific_token
        """
        for data in self.accounts:
            if _page_id == data["id"]:
                _page_access_token = data["access_token"]
                # print('access_token: ', _page_access_token)
                print("")
                print("Page id: ", data["id"])
                print("Page Name: ", data["name"])
                return _page_access_token
        else:
            return None

    @staticmethod
    def post_in_page(page_access_token, page_id, image_file=None, message=None, comment=None):
        """
        Method to post the media and text message to your page you manage. 
        :param page_access_token: valid api token
        :param page_id: Your page id
        :param image_file: Image File along with path
        :param message: Text
        :param comment: Text
        :return: None
        """
        try:
            page_graph = GraphAPI(page_access_token)
            if image_file:
                image = open(image_file, 'rb')
                if message:
                    print(page_id)
                    post = page_graph.post(path=page_id + '/photos', source=image, message=message)
                    facebook.GraphAPI(page_access_token).put_comment(object_id=post['post_id'], message=comment)
                    print('Posting .....')
                else:
                    page_graph.post(path=page_id + '/photos', source=image)
            else:
                if not message:
                    message = 'Hello everyone!!'
                page_graph.post(path=page_id + '/feed', message=message)
            print('Posted Successfully !! ..')
        except Exception as error:
            raise error
            print('Posting failed .. ', str(error))


if __name__ == "__main__":
    config = JsonParser(config_file)

    access_token = config.access_token
    if not access_token:
        print(
            "Access token cannot be none. visit: https://developers.facebook.com/tools/explorer/"
        )
        exit()

    # this token is users (don't use the global token)
    fb = FbPageAPI(access_token)

    for index, page in enumerate(config.pages):
        # get page token
        for page_id in page.page_group:
            print(page.message)
            page_access_token = fb.get_page_access_token(_page_id=page_id)
            # publish
            fb.post_in_page(
                page_access_token=page_access_token,
                page_id=page_id,
                image_file=page.image_file,
                message=page.message,
                comment=page.comment, 
            )
