from aiogram import Router
from components.organizer_mode.features.applicationsService.apps_management import router as application_router

applications_router = Router()
applications_router.include_routers(application_router)
