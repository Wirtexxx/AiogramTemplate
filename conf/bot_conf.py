import os
from dotenv import load_dotenv
import conf.paths


load_dotenv(conf.paths.env_file)

message_delay = 1

BOT_TOKEN = os.getenv('BOTTOKEN')
BOT_ID = ""
