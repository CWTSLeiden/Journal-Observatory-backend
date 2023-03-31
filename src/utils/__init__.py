import os
from configparser import ConfigParser

ROOT_DIR = os.getenv('APP_ROOT')
if not ROOT_DIR:
    try:
        ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), "../.."))
    except:
        ROOT_DIR = ".."

class CustomConfigParser(ConfigParser):
    def getpath(self, section, option, **kwargs):
        base = os.getenv('APP_ROOT', self.get("main", "root_dir", fallback=ROOT_DIR))
        path = self.get(section, option, **kwargs)
        if len(path) > 0:
            if not path[0] in ("/", "~", "$"):
                path = f"{base}/{path}"
        return path


db_config = CustomConfigParser()
db_config.read(f"{ROOT_DIR}/config/db.conf")
