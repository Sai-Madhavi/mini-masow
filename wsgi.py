import sys
path = '/home/Madhavi1234/baby-masow'
if path not in sys.path:
    sys.path.append(path)

from app import app as application