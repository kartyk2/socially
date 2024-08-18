from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, text
from config.constants import get_settings
from config.redis_config import redis_client
import time


app = FastAPI()
settings= get_settings()

pg_engine = create_engine(settings.pg_dsn.unicode_string())

# Middleware to log the time taken for each request
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Middleware to handle global exceptions
@app.middleware("http")
async def handle_exceptions(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": "An internal error occurred. Please try again later."},
        )

@app.get("/")
def read_root():
    return {"message": "Welcome to the WhatsApp Clone Backend!"}

@app.get("/healthcheck")
async def healthcheck():
    try:
        # Check Redis connection
        if not redis_client.ping():
            raise HTTPException(status_code=500, detail="Cannot connect to Redis")
        
        # Check PostgreSQL connection
        with pg_engine.connect() as conn:
            conn.execute(text("SELECT NOW()"))
        
        return {"status": "ok", "time": time.strftime("%Y-%m-%d %H:%M:%S")}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
