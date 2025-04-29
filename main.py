from dotenv import load_dotenv
import uvicorn
import os

load_dotenv()

PROJECT_HOST = os.getenv('PROJECT_HOST')
PROJECT_PORT = os.getenv('PROJECT_PORT')
RELOAD = os.getenv('RELOAD')


if __name__ == "__main__":
    uvicorn.run("config:app", host=PROJECT_HOST, port=int(PROJECT_PORT))
