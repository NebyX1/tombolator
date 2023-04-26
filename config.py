from dotenv import load_dotenv
import os

load_dotenv()

user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
host = os.environ['POSTGRES_HOST']
database = os.environ['POSTGRES_DATABASE']

DATABASE_CONNECTION_URI = f'postgresql://{user}:{password}@{host}/{database}'