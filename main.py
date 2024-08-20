import threading
import traceback
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, text
import uvicorn
from config.constants import get_settings
from config.database_config import engine, Base
from config.log_config import Logger
from config.clients import redis_client
from kafka_config.consumer import consume_messages, kafka_consumer
from kafka_config.producer import create_kafka_producer
from contextlib import asynccontextmanager
from models import *
from routers import user_management, user_connections
from chat_socket import sio_app
import time


settings= get_settings()
kafka_producer=  create_kafka_producer()

success_logger= Logger.get_success_logger()
error_logger= Logger.get_error_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    thread = threading.Thread(target=consume_messages, daemon=True)
    thread.start()
    
    yield
    kafka_consumer.close()
    thread.join() 

    
app = FastAPI(lifespan=lifespan, title= "Socially")
app.mount("/web_socket", sio_app)

app.include_router(user_management.user_manager, prefix= '/user-management', tags=["user-management"])
app.include_router(user_connections.connection_manager, prefix= '/user-connections', tags=["user-connections"])

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
        if not redis_client.ping():
            raise HTTPException(status_code=500, detail="Cannot connect to Redis")

        # Check PostgreSQL connection
        with engine.connect() as conn:
            conn.execute(text("SELECT NOW()"))

        # Check Kafka connection
        response= kafka_producer.send(settings.kafka_topic, value={"status": "ping"})
        kafka_producer.flush()

        return {"status": "ok", "time": time.strftime("%Y-%m-%d %H:%M:%S")}
    
    except Exception as e:
        error_logger.error("Exception occurred", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    uvicorn.run("main:app", host='localhost', port=8000)