from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware;
from dotenv import load_dotenv
import uvicorn, requests, os, json

# load environment variables
load_dotenv()

app = FastAPI()
router = APIRouter()

# setup cors
origins = [
  '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)

# define headers
HEADERS = {
  'X-RapidAPI-Host': 'exercisedb.p.rapidapi.com',
  'X-RapidAPI-Key': os.environ['API_KEY']
}


async def make_request(extension: str):
  url = os.environ['ROOT_URL'] + extension
  
  # make request
  r = requests.get(url, headers=HEADERS)
  data = r.json()

  return data

@router.get("/api")
async def root():
  return {"message": "Hello World"}

# returns list of muscle groups
@router.get('/api/muscles')
async def get_muscles():
  return await make_request('/targetList')

# returns list of exercise equipment
@router.get('/api/equipment')
async def get_equipment():
  return await make_request('/equipmentList')

# returns list of exercises
@router.get('/api/exercises')
async def get_exercises():
  return await make_request('')

# returns list of body parts
@router.get('/api/bodyparts')
async def get_bodyparts():
  return await make_request('/bodyPartList')

#### SPECIFIC LISTS ####

# returns list of exercies by muscle group
@router.get('/api/exercises/{group_id}')
async def get_group(group_id: int):
  try:
    data = await get_muscles()
    return await make_request('/target/' + data[group_id])
  except:
    return { 'message': 'List Index out of range'}

# returns list of exercies by equipment type
@router.get('/api/equipment/{equip_id}')
async def get_equip(equip_id: int):
  try:
    data = await get_equipment()
    return await make_request('/equipment/' + data[equip_id])
  except:
    return { 'message': 'List Index out of range'}

# returns list of exercies by body part (and also cardio)
@router.get('/api/bodyparts/{part_id}')
async def get_part(part_id: int):
  try:
    data = await get_bodyparts()
    return await make_request('/bodyPart/' + data[part_id])
  except:
    return { 'message': 'List Index out of range'}



app.include_router(router)
if __name__ == "__main__":
  uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)