from aiogram import Bot, Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from os.path import join, dirname

from components.shared.locale import load_locales, get_locale_str

locale = load_locales(join(dirname(__file__), "locale"))
getstr = lambda lang, path: get_locale_str(locale, f"{lang}.{path}")

