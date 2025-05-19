from aiogram import Router
from components.participant_drawer.features.activities.activity import (
    router as activity_router,
)
from components.participant_drawer.features.activities.committee import (
    router as committee_router,
)

activities_router = Router()
activities_router.include_routers(committee_router, activity_router)
