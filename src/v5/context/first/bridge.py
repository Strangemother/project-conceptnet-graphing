
import sys

sys.path.append('C:/Users/jay/Documents/projects/context-api/context/src')

from database.graph import *
import database
from database.db import *

ASSERTIONS_DIR = "E:/conceptnet/_lmdb_assertions/"
BRIDGE_DB_DIR = "E:/conceptnet/_lmdb_server_ui/"

"""The persistent source of original knowledge. held in the shared resource."""
assertions_db = GraphDB(write=False, directory=ASSERTIONS_DIR, name='assertions')
"""Any relative data to store for the internal procedures."""
db = GraphDB(directory=BRIDGE_DB_DIR, name='bridge')
