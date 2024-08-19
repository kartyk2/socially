import traceback
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, text
import uvicorn
from config.constants import get_settings
from config.database_config import engine, Base
from config.log_config import Logger
from config.clients import redis_client
from kafka_config.producer import create_kafka_producer
from contextlib import asynccontextmanager
from models import *
from routers import user_management
from websocket.chat_socket import sio_app
import time


settings= get_settings()
kafka_producer=  create_kafka_producer()

success_logger= Logger.get_success_logger()
error_logger= Logger.get_error_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan, title= "Socially")
app.mount("/", sio_app)

app.include_router(user_management.user_manager, prefix= '/user-management', tags=["user-management"])

# Middleware to log the time taken for each request
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/")
def read_root():
    return {"message": "Welcome to the Socially Backend!"}

@app.get("/healthcheck")
async def healthcheck():
    try:
        # Check Redis connection
        if not await redis_client.ping():
            raise HTTPException(status_code=500, detail="Cannot connect to Redis")

        # Check PostgreSQL connection
        with engine.connect() as conn:
            conn.execute(text("SELECT NOW()"))

        # Check Kafka connection
        kafka_producer.send('healthcheck_topic', value={"status": "ping"})
        kafka_producer.flush()

        return {"status": "ok", "time": time.strftime("%Y-%m-%d %H:%M:%S")}
    
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    uvicorn.run("main:app", host='localhost', port=8000, reload= True)