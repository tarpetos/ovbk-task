from faker import Faker
from fastapi import FastAPI, APIRouter
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()
router = APIRouter()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

fake = Faker()

user_data = []
chat_data = []
active_connections = {}

user_data_file = "user_data.txt"
