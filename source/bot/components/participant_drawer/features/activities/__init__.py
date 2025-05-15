from aiogram import Router
from committee import router as committee_router
from source.bot.components.participant_drawer.features.activities.activity import router as activity_router

activities_router = Router()
activities_router.include_routers(activity_router, committee_router)
