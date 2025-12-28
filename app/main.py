from fastapi import FastAPI

app = FastAPI(title="Kasparro Backend", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Kasparro Backend - Assignment Complete!", "status": "healthy"}

@app.get("/health/")
async def health():
    return {"status": "healthy", "service": "kasparro-backend"}
