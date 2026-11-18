from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from DB.db_config import create_tables
from Authentications import basic_route, session_route

@asynccontextmanager
async def life_cycle(app:FastAPI):
    print("Table creation start")
    create_tables()
    print("Table Created")
    yield

app = FastAPI(
    title="All Types Authentication",
    lifespan=life_cycle
)

@app.get("/")
def get_helth():
    return {
        "message":"All Ok buddy 🫠"
    }

app.include_router(basic_route)
app.include_router(session_route)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

