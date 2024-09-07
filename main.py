from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes.users import user_router
from routes.events import event_router
# from database.connection import conn
from database.mongo_connection import Settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

origins = ["*"]


from contextlib import asynccontextmanager

import uvicorn
settings=Settings()

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     conn()
#     yield

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('''          
{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
{}    _         _   _                                                       {}
{}   / \  _   _| |_| |__   ___  _ __                                        {}
{}  / _ \| | | | __| '_ \ / _ \| '__|                                       {}
{} / ___ | |_| | |_| | | | (_) | |                                          {}
{}/_____\_\____|___|___|_|_____|_|  _ ___    ____ _   _ _____ ___  _        {}
{} / ___| | | |/ _ |_ _| | ____| | | |_ _|  / ___| | | | ____/ _ \| |       {}
{}| |   | |_| | | | | |  |  _| | | | || |  | |   | |_| |  _|| | | | |       {}
{}| |___|  _  | |_| | |  | |___| |_| || |  | |___|  _  | |__| |_| | |___    {}
{} \____|_| ___\___|____ |__________________\____|_| _____________________  {}
{} / _ \/ |/ _ \      | || | / _ |___ \ / _ \       ( _ )| || ||___ \ / _ \ {}
{}| | | | | | | |_____| || || (_) |__) | (_) |_____ / _ \| || |_ __) | (_) |{}
{}| |_| | | |_| |_____|__   _\__, / __/ \__, |_____| (_) |__   _/ __/ \__, |{}
{} \___/|_|\___/         |_|   /_|_____|  /_/       \___/   |_||_____|  /_/ {}
{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
          ''')
    await settings.initialize_database()
    yield
    print("Shut down the server!!")

app = FastAPI(
    title = "Planner homepage",
    lifespan=lifespan
)
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=origins
)
# app.add_middleware(
#     HTTPSRedirectMiddleware
# )
@app.get("/")
async def home():
    return RedirectResponse(url="/event/", status_code=307)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)