from fastapi import FastAPI
from app.routes import products, orders
from app.database import init_db
from contextlib import asynccontextmanager
import asyncio
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost",  # or the origin where your client is hosted
    "http://127.0.0.1",  # local development

]
@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.to_thread(init_db)  # Initialize the database on startup
    yield
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(products.router)
app.include_router(orders.router)

# Add a simple health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Welcome to the our app"}
