import os
from dotenv import load_dotenv
import conf.paths

load_dotenv(conf.paths.env_file)


DB_URI = os.getenv('DBURI')

