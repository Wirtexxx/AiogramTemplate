import json
from core import loggers
import db
import redis
import uuid
from redis.commands.json.path import Path


client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
def id_maker():
    if client.exists("the_id"):
        the_id = int(client.get("the_id"))
        the_id = the_id + 1
        client.set("the_id", the_id)
        return the_id
    else:
        client.set("the_id", int(100000))
        the_id = int(client.get("the_id"))
        return the_id


class Caching:
    def __init__(self, telegram_id):
        super().__init__()
        self.telegram_id = telegram_id

    def add_user(self, info):
        client.set(f"user:{self.telegram_id}", json.dumps(info))

    def is_exists(self):
        if client.exists(f"user:{self.telegram_id}"):
            return True
        else:
            return False

    def update_user(self, info, sub_info: str = None, update_data=dict):
        if client.exists(f"user:{self.telegram_id}"):
            current_data = dict(json.loads(client.get(f"user:{self.telegram_id}")))
            if sub_info is None:
                current_data.update(info)
            else:
                sub_keys = sub_info.split(".")
                sub_dict = current_data.get(sub_keys[0], {})
                current_data[sub_keys[0]] = sub_dict

                if len(sub_keys) > 1:
                    nested_dict = sub_dict
                    for key in sub_keys[1:-1]:
                        nested_dict = nested_dict.setdefault(key, {})

                    last_key = sub_keys[-1]
                    if last_key in nested_dict and isinstance(nested_dict[last_key], dict):
                        nested_dict[last_key].update(info)
                    else:
                        nested_dict[last_key] = info
                else:
                    if sub_keys[0] in current_data and isinstance(current_data[sub_keys[0]], dict):
                        current_data[sub_keys[0]].update(info)
                    else:
                        current_data[sub_keys[0]] = info

            client.set(f"user:{self.telegram_id}", json.dumps(current_data))

    def remove(self):
        try:
            if client.exists(f"user:{self.telegram_id}"):
                client.delete(f"user:{self.telegram_id}")
        except Exception as ex:
            loggers.cache.exception(ex)

    def delete_data(self, key):
        if client.exists(f"user:{self.telegram_id}"):
            cached_data = json.loads(client.get(f"user:{self.telegram_id}"))
            if key in cached_data:
                del cached_data[key]
            client.set(f"user:{self.telegram_id}", json.dumps(cached_data))

    def get(self):
        if client.exists(f"user:{self.telegram_id}"):
            cached_data = client.get(f"user:{self.telegram_id}")

            if cached_data:
                return json.loads(cached_data)
            else:
                user_data = db.Account(self.telegram_id).get_data()
                if user_data is not None:
                    client.set(f"user:{self.telegram_id}", json.dumps(user_data))
                    return user_data
                else:
                    return None

    @staticmethod
    def get_all_users():
        all_keys = client.keys()
        users: dict[int, dict] = {}
        for key in all_keys:
            user = json.loads(client.get(key.decode('utf-8')))
            telegram_id: int = int(str(key.decode('utf-8')).replace("user:", ""))
            users[telegram_id] = user
        return users


def lang(telegram_id):
    if client.exists(f"user:{telegram_id}"):
        user = client.get(f"user:{telegram_id}")
        return json.loads(user).get("language")

    else:
        Caching(telegram_id).add_user({"language": "en"})
        user = client.get(f"user:{telegram_id}")
        return json.loads(user).get("language")


def edit_lang(telegram_id, language):
    if client.exists(f"user:{telegram_id}"):
        current_data = json.loads(client.get(f"user:{telegram_id}"))
        current_data.update({'language': language})
        Caching(telegram_id).update_user(current_data)

