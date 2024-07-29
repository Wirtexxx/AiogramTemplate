from pathlib import Path

home = Path.cwd()

conf = home / "conf"
core = home / "core"
db = home / "db"

creds_file = conf / ".creds.json"
env_file = conf / ".env"

cache = db / "cache"
