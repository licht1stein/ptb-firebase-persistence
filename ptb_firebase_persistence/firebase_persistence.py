import json
import os
from ast import literal_eval
from collections import defaultdict
from typing import Dict

import firebase_admin
from firebase_admin import db
from telegram.ext import BasePersistence


class FirebasePersistence(BasePersistence):
    def __init__(
        self,
        database_url: str,
        credentials: dict,
        store_user_data=True,
        store_chat_data=True,
        store_bot_data=True,
    ):
        cred = firebase_admin.credentials.Certificate(credentials)
        self.app = firebase_admin.initialize_app(cred, {"databaseURL": database_url})
        self.fb_user_data = db.reference("user_data")
        self.fb_chat_data = db.reference("chat_data")
        self.fb_bot_data = db.reference("bot_data")
        self.fb_conversations = db.reference("conversations")
        super().__init__(
            store_user_data=store_user_data,
            store_chat_data=store_chat_data,
            store_bot_data=store_bot_data,
        )

    @classmethod
    def from_environment(cls, **kwargs):
        credentials = json.loads(os.environ["FIREBASE_CREDENTIALS"])
        database_url = os.environ["FIREBASE_URL"]
        return cls(database_url=database_url, credentials=credentials, **kwargs)

    def get_user_data(self):
        data = self.fb_user_data.get() or {}
        output = self.convert_keys(data)
        return defaultdict(dict, output)

    def get_chat_data(self):
        data = self.fb_chat_data.get() or {}
        output = self.convert_keys(data)
        return defaultdict(dict, output)

    def get_bot_data(self):
        return defaultdict(dict, self.fb_bot_data.get() or {})

    def get_conversations(self, name):
        res = self.fb_conversations.child(name).get() or {}
        res = {literal_eval(k): v for k, v in res.items()}
        return res

    def update_conversation(self, name, key, new_state):
        if new_state:
            self.fb_conversations.child(name).child(str(key)).set(new_state)
        else:
            self.fb_conversations.child(name).child(str(key)).delete()

    def update_user_data(self, user_id, data):
        self.fb_user_data.child(str(user_id)).update(data)

    def update_chat_data(self, chat_id, data):
        self.fb_chat_data.child(str(chat_id)).update(data)

    def update_bot_data(self, data):
        self.fb_bot_data = data

    @staticmethod
    def convert_keys(data: Dict):
        output = {}
        for k, v in data.items():
            if k.isdigit():
                output[int(k)] = v
            else:
                output[k] = v
        return output
