from dotenv import load_dotenv

load_dotenv()

SQLITE_CONNECTION_STRING = 'sqlite:///videos.db?check_same_thread=False'
THREAD_WORKERS = 5
