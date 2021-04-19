import os
from run import create_app
import psycopg2 


basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'postgresql://arbokcnvtiwojp:413a24ecf8f6da746c05dabd7226702ef6bbf871942e8db3d821c509718fb8c6@ec2-34-233-0-64.compute-1.amazonaws.com:5432/dvicsp59t2n5d'
