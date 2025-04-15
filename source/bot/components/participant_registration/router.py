from aiogram import Bot, Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from components.shared.routing import setup_callbacks

from components.participant_registration.frontend import *

router = Router()

setup_callbacks(router, {
  "pr_cb_pre_main": pr_cb_pre_main,
  "pr_cb_user_main": pr_cb_user_main,
})
