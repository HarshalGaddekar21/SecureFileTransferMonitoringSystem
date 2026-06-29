import os
import sqlite3
import platform
from datetime import datetime


DATABASE = "database/filemonitor.db"


def get_settings():

    database_exists = os.path.exists(DATABASE)

    database_size = 0

    if database_exists:
        database_size = round(
            os.path.getsize(DATABASE) / 1024,
            2
        )

    return {

        "project_name":
            "Secure File Transfer Monitoring System",

        "version":
            "2.0",

        "developer":
            "Harshal Gaddekar",

        "database":
            "SQLite",

        "database_exists":
            database_exists,

        "database_size":
            database_size,

        "python_version":
            platform.python_version(),

        "operating_system":
            platform.system() + " " + platform.release(),

        "hostname":
            platform.node(),

        "server_status":
            "Running",

        "monitor_status":
            "Active",

        "last_updated":
            datetime.now().strftime(
                "%d %B %Y %I:%M %p"
            )
    }
