import os

ROOT_DIR = os.getenv('APP_ROOT')
if not ROOT_DIR:
    try:
        ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), "../.."))
    except:
        ROOT_DIR = ".."
