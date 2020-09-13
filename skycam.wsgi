#/usr/bin/python3
import sys

# the path in the server that contains main.py so it can imported
sys.path.insert(0, "/var/www/skycam/")

from main import app as application
