from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Kasparro Backend API", 
    version="1.0.0",
    docs_url="/docs",  # ✅ Enables Swagger
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Kasparro Backend API - Ready!", "status": "healthy"}

@app.get("/health/")
async def health():
    return {"status": "healthy", "service": "kasparro-backend"}

@app.get("/api/v1/stats/coins")
async def get_coins():
    return [{"symbol": "BTC", "price_usd": 94567.89}]
