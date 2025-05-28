from aiogram import Router
from components.participant_drawer.features.activities.activity import (
    router as activity_router,
)
from components.participant_drawer.features.activities.committee import (
    router as committee_router,
)
from components.participant_drawer.features.activities.middleware import RestoreDataMiddleware
from components.participant_drawer.features.activities.data import ACTIVITY_DATA_NAME

# activities_router = Router()
# activities_router.include_routers(committee_router, activity_router)
# activities_router.message.middleware(RestoreDataMiddleware(ACTIVITY_DATA_NAME))
# activities_router.callback_query.middleware(RestoreDataMiddleware(ACTIVITY_DATA_NAME))

# Activity name is set for the user the in activity_router handlers in FSMContext 
# with name ACTIVITY_DATA_NAME
# and needs to be saved so it doesn't get cleared
committee_router.message.middleware(RestoreDataMiddleware(ACTIVITY_DATA_NAME))
committee_router.callback_query.middleware(RestoreDataMiddleware(ACTIVITY_DATA_NAME))

activity_router.include_router(committee_router)
