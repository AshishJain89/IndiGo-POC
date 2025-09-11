from fastapi import APIRouter


from infrastructure.api.controllers.flight_controller import router as flight_router
from infrastructure.api.controllers.crew_controller import router as crew_router
from infrastructure.api.controllers.roster_controller import router as roster_router
from infrastructure.api.controllers.disruptions_controller import router as disruptions_router
from infrastructure.api.routes.chat import router as chat_router

api_router = APIRouter()
api_router.include_router(flight_router)
api_router.include_router(crew_router)
api_router.include_router(roster_router)

api_router.include_router(disruptions_router)
api_router.include_router(chat_router, prefix="/api")
