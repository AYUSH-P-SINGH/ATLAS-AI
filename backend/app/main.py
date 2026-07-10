from fastapi import FastAPI

app = FastAPI(title="Atlas AI API")

@app.get("/")
async def root():
    return {"message": "Atlas AI API"}
