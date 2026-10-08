from pathlib import Path
import sqlite3
from datetime import datetime
with sqlite3.connect('db.sqlite3') as source:
    with sqlite3.connect('scratch/antes_painel_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.sqlite3') as target:
        source.backup(target)
