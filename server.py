from flask import Flask
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.config['SQL_ALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)

app.config['JWT_SECRET_KEY']=os.getenv('JWT_SECRET')

@app.get('/')
def index():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
