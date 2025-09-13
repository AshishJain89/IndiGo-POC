from fastapi import APIRouter


from backend.infrastructure.api.controllers.flight_controller import router as flight_router
from backend.infrastructure.api.controllers.crew_controller import router as crew_router
from backend.infrastructure.api.controllers.roster_controller import router as roster_router
from backend.infrastructure.api.controllers.disruptions_controller import router as disruptions_router
from backend.infrastructure.api.routes.chat import router as chat_router
from backend.infrastructure.api.controllers.compliance_controller import router as compliance_router
from backend.infrastructure.api.controllers.conflicts_controller import router as conflicts_router
from backend.infrastructure.api.routes.analytics import router as analytics_router

api_router = APIRouter()
api_router.include_router(flight_router)
api_router.include_router(crew_router)
api_router.include_router(roster_router)

api_router.include_router(disruptions_router)
api_router.include_router(chat_router, prefix="/api")
api_router.include_router(compliance_router)
api_router.include_router(conflicts_router)
api_router.include_router(analytics_router, prefix="/api")
