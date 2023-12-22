from fastapi import FastAPI, APIRouter
import uvicorn

app = FastAPI()
router = APIRouter()

@router.get("/api")
async def root():
  return {"message": "Hello World"}

app.include_router(router)
if __name__ == "__main__":
  uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)