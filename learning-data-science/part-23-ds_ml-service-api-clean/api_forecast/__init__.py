from fastapi import FastAPI #type: ignore
from api_forecast.controllers import api_router
from fastapi.middleware.cors import CORSMiddleware #type: ignore
from prometheus_fastapi_instrumentator import Instrumentator #type: ignore

def create_app():

    app = FastAPI()

    app.include_router(api_router)

    app.add_middleware(
                        CORSMiddleware,
                        allow_origins=["*"],
                        allow_credentials=True,
                        allow_methods=["*"],
                        allow_headers=["*"]

    )

    Instrumentator().instrument(app).expose(app)

    return app

