from aiogram import Bot, Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from components.shared.routing import setup_callbacks

from components.participant_registration.logic.main import *
from components.participant_registration.logic.browse import *
from components.participant_registration.logic.register import *

router = Router()

setup_callbacks(router, {
  "pr_cb_main": pr_cb_main,
  "pr_cb_user_browse": pr_cb_user_browse,
  "pr_cb_user_register": pr_cb_user_register
})
