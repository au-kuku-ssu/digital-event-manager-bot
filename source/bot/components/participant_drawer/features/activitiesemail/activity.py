from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import smtplib
import random
import string

router = Router()

SMTP_SERVER = 'smtp.mail.ru'
SMTP_PORT = 465
EMAIL_FROM = 'egorlevoshin@mail.ru'
EMAIL_PASSWORD = 'EaT23nAxjyxZBku7jU5u'

def generate_code():
    characters = string.digits + string.ascii_letters
    return ''.join(random.choice(characters) for _ in range(6))

temp_storage = {}

@router.message(CommandStart())#Старт бота
async def cmd_start(message: Message):
    await message.answer('📧 Привет! Отправь мне свой email для получения кода активации')

@router.message()#обработка сообщения
async def chat(message: Message):
    text = message.text.strip()
    if "@" in text:#смотрим отправил ли он почту
        await mail(message, text)
    else:
        await verify(message, text)

async def mail(message: Message, email: str):#отправка сообщениея на почту пользователя и сейв почты 
    email_to = message.text.strip()
    try:
        code= generate()
        user[message.from_user.id] = {
            "email": email,
            "code": code
        }
        msg = MIMEText(f"Ваш код для активации аккаунта: {code}")
        msg['Subject'] = '🔐 Код активации'
        msg['From'] = EMAIL_FROM
        msg['To'] = email_to
        # Отправка через SMTP (с SSL или TLS)
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) if SMTP_PORT == 465 else smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            if SMTP_PORT == 587:  # Если используется TLS (порт 587)
                server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, email_to, msg.as_string())
        await message.answer(f"✅ Письмо отправлено на {email_to}! Введите его сюда для проверки:")
    except Exception as e:
        await message.answer(f"❌ Ошибка, попробуйте позже")

async def verify(message: Message, user_input: str):
    user_data = user.get(message.from_user.id)
    if not user_data:
        await message.answer("❌ Сначала отправьте email для получения кода")
        return
    
    if user_input == user_data["code"]:
        await message.answer("🎉 Код верный! Активация прошла успешно!")
        # Удаляем использованный код
        del user[message.from_user.id]
    else:
        await message.answer("❌ Неверный код. Попробуйте еще раз")
