import json
import os
from config import STATE_FILE


def load_state():

    if os.path.exists(STATE_FILE):

        with open(STATE_FILE) as f:
            data = json.load(f)

            return data.get("current_frame",0)

    return 0


def save_state(index):

    with open(STATE_FILE,"w") as f:

        json.dump({
            "current_frame":index
        },f,indent=2)