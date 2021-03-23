import env
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tw import auth

app = FastAPI()
app.include_router(auth.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://'+env.UI_HOST+':'+env.UI_PORT],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run(app, host=env.API_HOST, port=int(env.API_PORT))
