import env
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tw import auth, dashboard

app = FastAPI()
app.include_router(auth.router)
app.include_router(dashboard.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run(app, host=env.API_HOST, port=int(env.API_PORT))
