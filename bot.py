import asyncio
import random
import time

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import config
import database as db

bot = Bot(token=config.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


import string

GERMAN_REGIONS = [
    "B", "M", "HH", "K", "F", "S", "D", "L"
]

def generate_german_plate():
    region = random.choice(GERMAN_REGIONS)
    letters_count = random.randint(1, 2)
    letters = ''.join(random.choices(string.ascii_uppercase, k=letters_count))
    numbers = random.randint(1, 9999)
    return f"{region} {letters} {numbers}"


# ==================== ДАННЫЕ ====================

CARS = {
    1:   ("Honda Civic Mk6 — 175 HP", 4_600),
    2:   ("Smart Fortwo — 100 HP", 4_000),
    3:   ("Peugeot 406 — 207 HP", 4_800),
    4:   ("BMW E28 — 286 HP", 4_900),
    5:   ("BMW M135i — 326 HP", 5_500),
    6:   ("Ford Transit — 220 HP", 4_500),
    7:   ("Peugeot 308 — 180 HP", 4_900),
    8:   ("Mercedes W140 — 390 HP", 5_500),
    9:   ("BMW M5 E34 — 340 HP", 5_800),
    10:  ("Mazda RX-8 — 210 HP", 5_500),
    11:  ("Honda S2000 — 240 HP", 5_700),
    12:  ("Mercedes-Benz 190 (W201) — 220 HP", 4_800),
    13:  ("BMW 5 Series (E39) — 400 HP", 10_000),
    14:  ("Dodge Diplomat — 140 HP", 3_200),
    15:  ("Ford Crown Vic — 240 HP", 5_500),
    16:  ("Audi Quattro (Sport) — 306 HP", 15_000),
    17:  ("Toyota AE86 Trueno — 140 HP", 25_000),
    18:  ("Honda Del Sol — 160 HP", 15_000),
    19:  ("Volkswagen Golf II GTI — 112 HP", 15_000),
    20:  ("Mazda MX-5 — 190 HP", 12_400),
    21:  ("Volkswagen Scirocco — 250 HP", 5_400),
    22:  ("BMW M3 E36 — 320 HP", 12_000),
    23:  ("Audi RS 4 Avant — 450 HP", 40_000),
    24:  ("Ford Mustang VI — 310 HP", 45_000),
    25:  ("Mercedes-Benz W210 — 354 HP", 15_000),
    26:  ("Dodge Charger — 420 HP", 25_000),
    27:  ("Chevrolet Camaro — 490 HP", 38_000),
    28:  ("Toyota Camry 70 — 280 HP", 28_000),
    29:  ("Volkswagen Passat B8 — 190 HP", 30_000),
    30:  ("BMW M5 E60 — 507 HP", 38_000),
    31:  ("Kia Stinger GT — 361 HP", 34_000),
    32:  ("BMW M3 E92 — 420 HP", 30_000),
    33:  ("Cadillac Escalade — 400 HP", 28_000),
    34:  ("Mercedes-AMG C 63 Coupe W204 — 487 HP", 30_000),
    35:  ("Cadillac CTS — 320 HP", 33_000),
    36:  ("Subaru BRZ — 220 HP", 16_000),
    37:  ("Mercedes G 65 — 575 HP", 47_000),
    38:  ("BMW X5 E70 — 555 HP", 35_000),
    39:  ("Alfa Romeo Giulia Quadrifoglio — 505 HP", 45_000),
    40:  ("Subaru WRX STI — 300 HP", 37_000),
    41:  ("BMW M2 F87 — 450 HP", 50_000),
    42:  ("BMW M5 F10 — 560 HP", 38_000),
    43:  ("Toyota Land Cruiser 200 — 362 HP", 38_000),
    44:  ("Mercedes-Benz GLE — 435 HP", 38_000),
    45:  ("Audi RS2 Avant — 315 HP", 35_000),
    46:  ("Nissan Skyline R34 — 270 HP", 36_000),
    47:  ("Nissan Skyline R32 — 220 HP", 28_000),
    48:  ("Toyota Crown — 315 HP", 25_000),
    49:  ("Toyota Supra A80 — 280 HP", 37_000),
    50:  ("Mercedes-Benz CL 65 AMG — 630 HP", 50_000),
    51:  ("Mercedes-Benz S-Klasse W221 — 650 HP", 40_000),
    52:  ("Chevrolet Tahoe — 420 HP", 37_000),
    53:  ("Mitsubishi Lancer Evolution X — 295 HP", 55_000),
    54:  ("Subaru Impreza WRX STI GVB — 300 HP", 45_000),
    55:  ("Subaru WRX STI VA — 300 HP", 47_000),
    56:  ("Mercedes-Benz Actros — 625 HP", 110_000),
    57:  ("Scania R730 — 600 HP", 135_000),
    58:  ("Nissan 240SX S13 — 240 HP", 35_000),
    59:  ("Skoda Octavia A8 Combi — 190 HP", 32_000),
    60:  ("Mazda RX-7 FD3S — 280 HP", 55_000),
    61:  ("Toyota Mark II JZX100 — 280 HP", 40_000),
    62:  ("Ford Focus RS — 350 HP", 35_000),
    63:  ("Toyota Altezza RS200 — 210 HP", 12_500),
    64:  ("Dacia Logan — 90 HP", 6_000),
    65:  ("Fiat Doblo — 105 HP", 14_500),
    66:  ("Honda Civic Type R FK8 — 320 HP", 42_000),
    67:  ("Chevrolet C10 Silverado — 165 HP", 22_000),
    68:  ("Volkswagen Golf VII R — 300 HP", 40_000),
    69:  ("BMW M4 F82 — 431 HP", 80_000),
    70:  ("Toyota GR Yaris — 261 HP", 45_000),
    71:  ("Ford Bronco — 310 HP", 95_000),
    72:  ("Infiniti G37 Coupe — 333 HP", 75_000),
    73:  ("Airstream Motorhome — 190 HP", 110_000),
    74:  ("Toyota Hilux — 150 HP", 38_000),
    75:  ("GMC Sierra 3500HD — 445 HP", 75_000),
    76:  ("Nissan Z Proto — 400 HP", 55_000),
    77:  ("Toyota Fortuner — 204 HP", 48_000),
    78:  ("Mercedes-AMG GT S — 510 HP", 169_000),
    79:  ("Porsche 911 Carrera 4S — 580 HP", 192_000),
    80:  ("BMW M5 F90 — 650 HP", 146_000),
    81:  ("BMW M6 F12 — 560 HP", 92_300),
    82:  ("Ferrari 458 Italia — 570 HP", 300_000),
    83:  ("Audi RS6 C8 — 600 HP", 246_000),
    84:  ("Lamborghini Huracán — 680 HP", 385_000),
    85:  ("Audi R8 V10 — 550 HP", 132_000),
    86:  ("BMW M4 G82 Competition — 510 HP", 223_000),
    87:  ("Mercedes-Benz E63 AMG — 630 HP", 119_000),
    88:  ("Mercedes-AMG GT — 640 HP", 154_000),
    89:  ("Audi RS7 — 630 HP", 246_000),
    90:  ("BMW M8 F92 — 625 HP", 277_000),
    91:  ("Dodge Challenger SRT — 780 HP", 231_000),
    92:  ("Chevrolet Corvette C7 — 600 HP", 145_000),
    93:  ("Porsche Panamera Turbo — 520 HP", 85_000),
    94:  ("RAM TRX — 712 HP", 254_000),
    95:  ("BMW i8 — 420 HP", 145_000),
    96:  ("Lamborghini Urus — 650 HP", 385_000),
    97:  ("BMW X7 M50i — 400 HP", 154_000),
    98:  ("BMW i7 — 544 HP", 231_000),
    99:  ("Nissan GT-R R35 — 500 HP", 92_300),
    100: ("BMW X6 M F86 — 575 HP", 80_800),
    101: ("Porsche 911 Carrera 4 — 272 HP", 154_000),
    102: ("Mercedes G-Class — 575 HP", 210_000),
    103: ("Dodge Viper — 650 HP", 185_000),
    104: ("Cadillac Escalade-V — 682 HP", 230_000),
    105: ("Range Rover Sport SV — 542 HP", 198_000),
    106: ("BMW M5 G90 2025 — 717 HP", 250_000),
    107: ("Mercedes-Maybach S680 W223 — 603 HP", 320_000),
    108: ("Ford Mustang 2024 — 500 HP", 110_000),
    109: ("Mercedes-Benz S-Class W222 — 612 HP", 140_000),
    110: ("Chevrolet Camaro ZL1 — 650 HP", 95_000),
    111: ("Bentley Continental GT — 640 HP", 220_000),
    112: ("Toyota Supra A90 — 340 HP", 85_000),
    113: ("Land Rover Defender 110 V8 — 525 HP", 195_000),
    114: ("Ford F-150 Raptor R — 720 HP", 265_000),
    115: ("Jeep Gladiator Rubicon — 285 HP", 200_000),
    116: ("Lamborghini Gallardo Spyder — 650 HP", 390_000),
    117: ("Jeep Grand Cherokee SRT8 — 475 HP", 180_000),
    118: ("Porsche 911 GT3 RS — 525 HP", 280_000),
    119: ("Hummer H1 Alpha — 300 HP", 145_000),
    120: ("BMW M2 G87 — 460 HP", 82_000),
    121: ("Ford F-650 Super Duty — 330 HP", 120_000),
    122: ("Porsche Carrera GT — 612 HP", 650_000),
    123: ("Lexus LFA — 560 HP", 450_000),
    124: ("Porsche 918 Spyder — 887 HP", 950_000),
    125: ("Mercedes-Benz CLK GTR — 612 HP", 13_000_000),
    126: ("Rolls-Royce Cullinan Blue — 555 HP", 1_500_000),
    127: ("Lamborghini Aventador Orange — 700 HP", 950_000),
    128: ("Rolls-Royce Dawn — 570 HP", 1_200_000),
    129: ("Ferrari F40 — 478 HP", 2_500_000),
    130: ("Lamborghini Aventador SVJ — 790 HP", 850_000),
    131: ("Pagani Zonda Cinque — 764 HP", 9_500_000),
    132: ("Lamborghini Veneno — 750 HP", 3_500_000),
    133: ("Ferrari LaFerrari — 949 HP", 3_600_000),
    134: ("Bugatti Chiron Sport — 1500 HP", 4_200_000),
    135: ("Koenigsegg Jesko Attack — 1280 HP", 5_500_000),
    136: ("Mercedes G-Class 6x6 — 544 HP", 950_000),
    137: ("McLaren 720S — 710 HP", 450_000),
    138: ("McLaren P1 — 920 HP", 1_500_000),
    139: ("Bugatti Veyron — 1001 HP", 1_900_000),
    140: ("Koenigsegg Agera RS — 1115 HP", 3_000_000),
}

JOBS = {
    "Работник кафе": 600,
    "Автомаляр": 1_850,
    "Инкассатор": 2_200,
    "Строитель": 2_000,
    "Шеф-повар": 2_900,
    "Кассир (Lidl / Aldi)": 1_600,
    "Заправщик АЗС": 1_600,
    "Мойщик автомобилей": 1_900,
    "Курьер (DHL / Amazon)": 1_800,
    "Сотрудник фастфуда (McDonald's / KFC)": 1_500,
    "Садовник / Фермер": 1_700,
    "Таксист (Эконом)": 2_500,
    "Таксист (Бизнес-класс)": 7_200,
    "Водитель автобуса": 3_000,
    "Эвакуаторщик": 4_500,
    "Автомеханик / Электрик": 4_800,
    "Дальнобойщик (LKW)": 9_000,
}

GOV_JOBS = {
    "Парамедик (Скорая помощь)": 3_200,
    "Врач неотложной помощи": 6_000,
    "Хирург": 8_500,
    "Главврач": 14_000,
    "Помощник прокурора": 1_450,
    "Прокурор": 15_000,
    "Старший прокурор": 2_200,
    "Прокурор района": 2_650,
    "Прокурор города": 3_300,
    "Прокурор области": 4_200,
    "Генеральный прокурор": 18_000,
    "Судья": 17_000,
    "Адвокат": 7_400,
    "Охранник Правительства": 900,
    "Водитель Правительства": 1_000,
    "Секретарь Правительства": 1_100,
    "Депутат": 2_450,
    "Министр": 3_100,
    "Заместитель губернатора": 3_900,
    "Губернатор": 5_000,
    "Телохранитель правительства": 6_000,
    "Бургомистр (Мэр)": 17_000,
    "Министр обороны": 17_500,
    "Министр МВД": 17_500,
    "Министр здравоохранения": 17_500,
    "Вице-канцлер": 19_500,
    "Федеральный канцлер": 20_000,
    "Курсант (Стажер)": 2_000,
    "Мастер полиции": 3_200,
    "Комиссар полиции": 5_000,
    "Старший комиссар": 6_500,
    "Главный комиссар (Детектив)": 8_000,
    "Директор полиции": 13_500,
    "Президент полиции (Шеф)": 15_000,
    "Спецагент BKA": 12_500,
    "Оперативник GSG 9": 12_000,
    "Командир GSG 9 (Спецназ)": 15_000,
    "Президент BKA (Уголовный розыск)": 16_000,
    "Пожарный (Feuerwehr)": 4_500,
    "Командир пожарной части": 9_500,
    "Глава пожарной службы": 15_000,
    "Ефрейтор (Рядовой)": 0,
    "Унтер-офицер (Сержант)": 5_500,
    "Лейтенант": 8_500,
    "Майор": 9_500,
    "Подполковник": 11_500,
    "Полковник": 14_000,
    "Генерал": 18_500,
}

ALL_JOBS = {**JOBS, **GOV_JOBS}

BUSINESSES = {
    1:  ("Мотель Grand Rock", 250_000, 15_000),
    2:  ("Central Gas Station", 280_000, 17_000),
    3:  ("Central Service Center", 300_000, 18_500),
    4:  ("Central SuperMarket", 1_500_000, 49_500),
    5:  ("McDonald's Teddy Donuts & Burgers", 500_000, 25_000),
    6:  ("Teddy Donuts & Burgers Munich", 750_000, 30_000),
    7:  ("WAVERIK Gas Station", 950_000, 38_000),
    8:  ("Bavaria Cargo Port", 4_500_000, 89_000),
    9:  ("CPM Service", 700_000, 25_000),
    10: ("Рекламная вывеска Тип 1", 42_000, 3_000),
    11: ("Вендинговый аппарат Тип 1", 15_000, 1_200),
    12: ("Тележка с напитками Тип 1", 18_500, 1_350),
    13: ("Тележка с напитками Тип 2", 18_500, 1_350),
    14: ("Рекламная вывеска Тип 2", 42_000, 3_000),
    15: ("Рекламная вывеска Тип 3", 42_000, 3_000),
    16: ("Рекламная вывеска Тип 4", 42_000, 3_000),
    17: ("Вендинговый аппарат Тип 2", 15_000, 1_200),
    18: ("Рекламный баннер Тип 1", 18_500, 1_200),
    19: ("Minimarket Small Way", 100_000, 6_000),
    20: ("Berlin Safe-Stop Parking", 300_000, 14_000),
    21: ("CPM HOTEL & RESORT", 1_800_000, 48_000),
    22: ("Großes Zentrale Kaffe", 900_000, 35_000),
    23: ("Schuppig Center", 1_500_000, 50_000),
    24: ("Privat Parkplatz", 400_000, 18_000),
    25: ("Autoteile", 690_000, 30_000),
    26: ("Автозаправка-мойка", 400_000, 19_500),
    27: ("Mechanis PRO", 450_000, 21_500),
    28: ("Supermarket Bavaria", 324_000, 18_500),
    29: ("Рекламный баннер Тип 2", 18_500, 1_200),
    30: ("Рекламный баннер Тип 3", 18_500, 1_200),
    31: ("Автосервис TASSIMOV", 750_000, 34_000),
    32: ("Заправка Пригород", 250_000, 17_000),
    33: ("Заправка Магистраль", 380_000, 20_000),
    34: ("Заправка Элитный посёлок", 410_000, 22_000),
    35: ("Рекламная вывеска Бавария", 26_000, 1_900),
    36: ("STREETFOOD Bavaria", 340_000, 19_000),
    37: ("MOTEL RTT", 580_000, 28_000),
    38: ("АЗС Пригород", 370_000, 20_000),
    39: ("Berlin GROUND Parking", 850_000, 35_000),
    40: ("McDonald's Berlin", 480_000, 25_000),
    41: ("СТО Берлин", 250_000, 14_500),
    42: ("АЗС Munich Region", 395_000, 22_000),
    43: ("Шиномонтаж Тип 1", 65_000, 5_000),
    44: ("Шиномонтаж Тип 2", 65_000, 5_000),
    45: ("Шиномонтаж Тип 3", 65_000, 5_000),
    46: ("Шиномонтаж Тип 4", 65_000, 5_000),
    47: ("СТО Объект", 460_000, 28_500),
    48: ("АЗС Объект", 450_000, 27_500),
}

APARTMENTS = {
    1:  ("Хостел / комната", 7_500),
    2:  ("1-комнатная квартира", 25_000),
    3:  ("Дом / апартаменты", 50_000),
    4:  ("Luxury Studio (элитный небоскрёб)", 100_000),
    5:  ("Посёлок с частными домами", 45_000),
    6:  ("Современный многоквартирный дом", 75_000),
    7:  ("Квартирные дома старого типа", 12_300),
    8:  ("Посёлок с частными домами (бюджет район)", 35_000),
    9:  ("Luxury Studio Munich", 150_000),
    10: ("Апартаменты Среднего класса Bavaria", 100_000),
    11: ("Апартаменты Business класса Berlin", 890_000),
    12: ("Апартаменты Среднего класса Северная Бавария", 180_000),
    13: ("Апартаменты Business класса Lindau", 450_000),
    14: ("Апартаменты Среднего класса Munich", 190_000),
    15: ("Апартаменты ELITE класса", 1_800_000),
    16: ("Апартаменты Среднего класса Berlin Outskirts", 80_000),
    17: ("Квартирный дом эконом класса", 40_000),
    18: ("Квартирный дом с кофейней", 40_000),
    19: ("Элитные дома рядом с Мюнхеном", 1_800_000),
}

# ==================== PENDING DICTS ====================

PENDING_REGISTRATIONS: dict = {}
PENDING_SALES: dict = {}

# ==================== FSM ====================

class Registration(StatesGroup):
    spm_id = State()
    game_name = State()

# ==================== ХЕЛПЕРЫ ====================

def fmt(n):
    return f"{int(n):,}".replace(",", ".") + "€"

def is_admin(uid):
    return uid in config.ADMIN_IDS

GARAGE_SLOT_PRICES = {
    3: 1_100,
    4: 1_650,
    5: 2_200,
    6: 2_750,
    7: 3_300,
    8: 4_400,
    9: 5_500,
    10: 6_650,
}

def info_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🚗 Гараж", callback_data="list_cars"),
            InlineKeyboardButton(text="💼 Работа", callback_data="list_jobs"),
        ],
        [
            InlineKeyboardButton(text="🏢 Бизнесы", callback_data="list_biz"),
            InlineKeyboardButton(text="🏠 Недвижимость", callback_data="list_apts"),
        ],
        [
            InlineKeyboardButton(text="🏛️ Организации", callback_data="list_orgs"),
            InlineKeyboardButton(text="🏦 Банк", callback_data="bank_menu"),
        ],
    ])

def back_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_info")]
    ])

def check_user(user):
    if not user:
        return "not_registered"
    if user[9]:
        return "banned"
    return "ok"

def parse_mentioned_username(text: str) -> str | None:
    parts = text.split()
    for part in parts:
        if part.startswith("@") and len(part) > 1:
            return part[1:]
    return None

# ==================== РЕГИСТРАЦИЯ ====================

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    user = db.get_user(message.from_user.id)
    if user:
        await message.answer("✅ Вы уже зарегистрированы!\n\nНапишите инфо для просмотра профиля.")
        return
    await message.answer(
        "👋 Добро пожаловать в Deutschland RP!\n\n"
        "Для регистрации введите ваш СПМ айди:"
    )
    await state.set_state(Registration.spm_id)

@dp.message(Registration.spm_id)
async def reg_spm_id(message: types.Message, state: FSMContext):
    await state.update_data(spm_id=message.text.strip())
    await message.answer("✍️ Теперь введите ваше имя в игре:")
    await state.set_state(Registration.game_name)

@dp.message(Registration.game_name)
async def reg_game_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    spm_id = data["spm_id"]
    game_name = message.text.strip()
    username = message.from_user.username or message.from_user.first_name
    uid = message.from_user.id
    await state.clear()

    if not config.REGISTRATION_CHAT_ID:
        db.register_user(uid, username, spm_id, game_name)
        await message.answer(
            f"✅ Регистрация завершена!\n\n"
            f"👤 Ник в TG: @{username}\n"
            f"🎮 Имя в игре: {game_name}\n"
            f"🆔 СПМ айди: {spm_id}\n"
            f"💰 Стартовый баланс: {fmt(config.START_BALANCE)}\n\n"
            f"Напишите инфо для просмотра профиля."
        )
        return

    PENDING_REGISTRATIONS[uid] = {
        "spm_id": spm_id,
        "game_name": game_name,
        "username": username,
    }

    text = (
        f"📋 Deutschland RP — Новая анкета\n\n"
        f"👤 TG: @{username} (ID: {uid})\n"
        f"🎮 Имя в игре: {game_name}\n"
        f"🆔 СПМ айди: {spm_id}"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Одобрить", callback_data=f"approve_reg_{uid}"),
        InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_reg_{uid}"),
    ]])
    try:
        send_kwargs = dict(chat_id=config.REGISTRATION_CHAT_ID, text=text, reply_markup=kb)
        if config.REGISTRATION_TOPIC_ID:
            send_kwargs["message_thread_id"] = config.REGISTRATION_TOPIC_ID
        await bot.send_message(**send_kwargs)
    except Exception:
        db.register_user(uid, username, spm_id, game_name)
        await message.answer(
            f"✅ Регистрация завершена!\n\n"
            f"👤 Ник в TG: @{username}\n"
            f"🎮 Имя в игре: {game_name}\n"
            f"🆔 СПМ айди: {spm_id}\n"
            f"💰 Стартовый баланс: {fmt(config.START_BALANCE)}\n\n"
            f"Напишите инфо для просмотра профиля."
        )
        return

    await message.answer(
        f"📋 Анкета отправлена на рассмотрение!\n\n"
        f"🎮 Имя в игре: {game_name}\n"
        f"🆔 СПМ айди: {spm_id}\n\n"
        f"Ожидайте одобрения от администратора.\n"
        f"Вам придёт уведомление."
    )

@dp.callback_query(F.data.startswith("approve_reg_"))
async def cb_approve_reg(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    uid = int(callback.data.split("_")[2])
    pending = PENDING_REGISTRATIONS.pop(uid, None)
    if not pending:
        if db.get_user(uid):
            await callback.answer("✅ Уже одобрено", show_alert=True)
        else:
            await callback.answer("❌ Анкета не найдена (устарела)", show_alert=True)
        return
    db.register_user(uid, pending["username"], pending["spm_id"], pending["game_name"])
    try:
        await bot.send_message(
            uid,
            f"✅ Deutschland RP — Ваша анкета одобрена!\n\n"
            f"🎮 Имя в игре: {pending['game_name']}\n"
            f"🆔 СПМ айди: {pending['spm_id']}\n"
            f"💰 Стартовый баланс: {fmt(config.START_BALANCE)}\n\n"
            f"Напишите инфо для просмотра профиля."
        )
    except Exception:
        pass
    admin_name = callback.from_user.username or callback.from_user.first_name
    await callback.message.edit_text(callback.message.text + f"\n\n✅ Одобрено: @{admin_name}")
    await callback.answer("✅ Игрок зарегистрирован!")

@dp.callback_query(F.data.startswith("reject_reg_"))
async def cb_reject_reg(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
    uid = int(callback.data.split("_")[2])
    pending = PENDING_REGISTRATIONS.pop(uid, None)
    if not pending:
        await callback.answer("❌ Анкета не найдена (устарела)", show_alert=True)
        return
    try:
        await bot.send_message(uid, "❌ Deutschland RP — Ваша анкета отклонена.\n\nОбратитесь к администратору.")
    except Exception:
        pass
    admin_name = callback.from_user.username or callback.from_user.first_name
    await callback.message.edit_text(callback.message.text + f"\n\n❌ Отклонено: @{admin_name}")
    await callback.answer("❌ Анкета отклонена")

# ==================== ИНФО ====================

@dp.message(lambda m: m.text and m.text.lower() == "инфо")
async def info_cmd(message: types.Message):
    user = db.get_user(message.from_user.id)
    status = check_user(user)
    if status == "not_registered":
        await message.answer("❌ Вы не зарегистрированы. Напишите /start")
        return
    if status == "banned":
        await message.answer("⛔ Вы заблокированы.")
        return
    await message.answer(build_profile_text(user), reply_markup=info_keyboard())

# ==================== БАЛАНС ====================

@dp.message(lambda m: m.text and m.text.lower() in ["б", "баланс"])
async def balance_cmd(message: types.Message):
    user = db.get_user(message.from_user.id)
    if not user:
        await message.answer("❌ Вы не зарегистрированы. Напишите /start")
        return
    await message.answer(f"💰 Ваш баланс: {fmt(user[4])}\n🏦 Банк: {fmt(user[5])}")

# ==================== ЗП (для себя) ====================

@dp.message(lambda m: m.text and m.text.lower() in ["зп", "зарплата"])
async def salary_cmd(message: types.Message):
    user = db.get_user(message.from_user.id)
    status = check_user(user)
    if status == "not_registered":
        await message.answer("❌ Вы не зарегистрированы. Напишите /start")
        return
    if status == "banned":
        await message.answer("⛔ Вы заблокированы.")
        return

    uid, username, spm_id, game_name, balance, bank, btc, job, last_salary, banned, *_ = user

    if not job:
        await message.answer("❌ У вас нет работы. Обратитесь к администратору.")
        return

    now = int(time.time())
    if now - last_salary < config.SALARY_COOLDOWN:
        remaining = config.SALARY_COOLDOWN - (now - last_salary)
        mins = remaining // 60
        secs = remaining % 60
        await message.answer(f"⏰ Зарплата будет доступна через {mins} мин. {secs} сек.")
        return

    salary = ALL_JOBS.get(job, 0)
    if salary == 0:
        await message.answer("❌ Работа не найдена. Обратитесь к администратору.")
        return

    multiplier = 2 if db.has_x2(uid) else 1
    final_salary = salary * multiplier

    db.update_balance(uid, final_salary)
    db.update_salary_time(uid)

    x2_text = " (х2 бонус! 🔥)" if multiplier == 2 else ""
    await message.answer(
        f"💵 Вы получили зарплату: +{fmt(final_salary)}{x2_text}\n"
        f"💰 Новый баланс: {fmt(balance + final_salary)}"
    )

# ==================== ЗП @ЮЗЕР ====================

@dp.message(lambda m: (
    m.text and
    m.text.lower().startswith("зп ") and
    "@" in m.text and
    not m.text.lower().startswith("зп бизнес")
))
async def salary_mention_cmd(message: types.Message):
    target_username = parse_mentioned_username(message.text)
    if not target_username:
        await message.answer("❌ Формат: зп @никнейм")
        return

    target = db.get_user_by_username(target_username)
    if not target:
        return

    status = check_user(target)
    if status == "banned":
        await message.answer(f"⛔ Игрок @{target_username} заблокирован.")
        return

    uid, username, spm_id, game_name, balance, bank, btc, job, last_salary, banned, *_ = target

    if not job:
        await message.answer(f"❌ У @{target_username} нет работы.")
        return

    now = int(time.time())
    if now - last_salary < config.SALARY_COOLDOWN:
        remaining = config.SALARY_COOLDOWN - (now - last_salary)
        mins = remaining // 60
        secs = remaining % 60
        await message.answer(f"⏰ @{target_username}, зарплата будет доступна через {mins} мин. {secs} сек.")
        return

    salary = ALL_JOBS.get(job, 0)
    if salary == 0:
        await message.answer(f"❌ Работа игрока @{target_username} не найдена.")
        return

    multiplier = 2 if db.has_x2(uid) else 1
    final_salary = salary * multiplier

    db.update_balance(uid, final_salary)
    db.update_salary_time(uid)

    x2_text = " (х2 бонус! 🔥)" if multiplier == 2 else ""
    await message.answer(
        f"💵 @{target_username} получил зарплату: +{fmt(final_salary)}{x2_text}\n"
        f"💼 Должность: {job}\n"
        f"💰 Новый баланс: {fmt(balance + final_salary)}"
    )

    try:
        await bot.send_message(
            uid,
            f"💵 Вам выдали зарплату: +{fmt(final_salary)}{x2_text}\n"
            f"💼 Должность: {job}\n"
            f"💰 Новый баланс: {fmt(balance + final_salary)}"
        )
    except Exception:
        pass

# ==================== ЗП БИЗНЕС @ЮЗЕР ====================

@dp.message(lambda m: (
    m.text and
    m.text.lower().startswith("зп бизнес") and
    "@" in m.text
))
async def salary_and_biz_cmd(message: types.Message):
    target_username = parse_mentioned_username(message.text)
    if not target_username:
        await message.answer("❌ Формат: зп бизнес @никнейм")
        return

    target = db.get_user_by_username(target_username)
    if not target:
        return

    status = check_user(target)
    if status == "banned":
        await message.answer(f"⛔ Игрок @{target_username} заблокирован.")
        return

    uid, username, spm_id, game_name, balance, bank, btc, job, last_salary, banned, *_ = target
    multiplier = 2 if db.has_x2(uid) else 1
    x2_text = " (х2 бонус! 🔥)" if multiplier == 2 else ""
    now = int(time.time())
    lines = []
    total_earned = 0

    if job:
        salary = ALL_JOBS.get(job, 0)
        if salary > 0:
            if now - last_salary < config.SALARY_COOLDOWN:
                rem = config.SALARY_COOLDOWN - (now - last_salary)
                lines.append(f"⏰ Зарплата: ещё {rem // 60} мин. {rem % 60} сек.")
            else:
                final_sal = salary * multiplier
                db.update_balance(uid, final_sal)
                db.update_salary_time(uid)
                total_earned += final_sal
                lines.append(f"💵 Зарплата ({job}): +{fmt(final_sal)}")
    else:
        lines.append("💼 Работа: нет")

    bizs = db.get_businesses(uid)
    if bizs:
        last_biz_time = db.get_biz_income_time(uid)
        if now - last_biz_time < config.SALARY_COOLDOWN:
            rem = config.SALARY_COOLDOWN - (now - last_biz_time)
            lines.append(f"⏰ Бизнес: ещё {rem // 60} мин. {rem % 60} сек.")
        else:
            total_inc = sum(inc for _, inc in bizs)
            final_inc = total_inc * multiplier
            db.update_balance(uid, final_inc)
            db.update_biz_income_time(uid)
            total_earned += final_inc
            biz_lines = "\n".join(f"  • {name}: +{fmt(inc * multiplier)}" for name, inc in bizs)
            lines.append(f"🏢 Бизнесы:\n{biz_lines}\n  📈 Итого бизнес: +{fmt(final_inc)}")
    else:
        lines.append("🏢 Бизнесов нет")

    new_balance = balance + total_earned
    report = "\n".join(lines)
    await message.answer(
        f"💰 Deutschland RP — Выплата @{target_username}{x2_text}\n\n"
        f"{report}\n\n"
        f"{'📊 Итого получено: +' + fmt(total_earned) if total_earned else '⚠️ Ничего не выдано'}\n"
        f"💵 Баланс: {fmt(new_balance)}"
    )
    if total_earned:
        try:
            await bot.send_message(
                uid,
                f"💰 Deutschland RP — Вам выплачено{x2_text}\n\n"
                f"{report}\n\n"
                f"📊 Итого получено: +{fmt(total_earned)}\n"
                f"💵 Баланс: {fmt(new_balance)}"
            )
        except Exception:
            pass

# ==================== БИЗНЕС @ЮЗЕР ====================

@dp.message(lambda m: (
    m.text and
    m.text.lower().startswith("бизнес ") and
    "@" in m.text
))
async def business_only_cmd(message: types.Message):
    target_username = parse_mentioned_username(message.text)
    if not target_username:
        await message.answer("❌ Формат: бизнес @никнейм")
        return

    target = db.get_user_by_username(target_username)
    if not target:
        return

    status = check_user(target)
    if status == "banned":
        await message.answer(f"⛔ Игрок @{target_username} заблокирован.")
        return

    uid, username, spm_id, game_name, balance, bank, btc, job, last_salary, banned, *_ = target
    multiplier = 2 if db.has_x2(uid) else 1
    x2_text = " (х2 бонус! 🔥)" if multiplier == 2 else ""
    now = int(time.time())

    bizs = db.get_businesses(uid)
    if not bizs:
        await message.answer(f"🏢 У @{target_username} нет бизнесов.")
        return

    last_biz_time = db.get_biz_income_time(uid)
    if now - last_biz_time < config.SALARY_COOLDOWN:
        rem = config.SALARY_COOLDOWN - (now - last_biz_time)
        await message.answer(f"⏰ @{target_username}, бизнес-доход будет доступен через {rem // 60} мин. {rem % 60} сек.")
        return

    total_income = sum(inc for _, inc in bizs)
    final_income = total_income * multiplier
    db.update_balance(uid, final_income)
    db.update_biz_income_time(uid)

    biz_lines = "\n".join(f"  • {name}: +{fmt(inc * multiplier)}" for name, inc in bizs)
    await message.answer(
        f"🏢 @{target_username} получил доход от бизнесов{x2_text}:\n\n"
        f"{biz_lines}\n\n"
        f"📈 Итого: +{fmt(final_income)}\n"
        f"💰 Новый баланс: {fmt(balance + final_income)}"
    )
    try:
        await bot.send_message(
            uid,
            f"🏢 Deutschland RP — Вам выдан доход от бизнесов{x2_text}:\n\n"
            f"{biz_lines}\n\n"
            f"📈 Итого: +{fmt(final_income)}\n"
            f"💰 Новый баланс: {fmt(balance + final_income)}"
        )
    except Exception:
        pass

# ==================== ПЕРЕВОД ИГРОК→ИГРОК ====================

@dp.message(lambda m: (
    m.text and m.text.lower().startswith("дать ") and
    "@" in m.text and
    m.reply_to_message is None and
    (m.from_user is None or m.from_user.id not in config.ADMIN_IDS)
))
async def player_give_cmd(message: types.Message):
    user = db.get_user(message.from_user.id)
    status = check_user(user)
    if status == "not_registered":
        await message.answer("❌ Вы не зарегистрированы. Напишите /start")
        return
    if status == "banned":
        await message.answer("⛔ Вы заблокированы.")
        return
    parts = message.text.strip().split()
    try:
        amount = int(parts[1])
        username = next(p for p in parts if p.startswith("@"))[1:]
    except Exception:
        await message.answer("❌ Формат: дать [сумма] @никнейм")
        return
    if amount <= 0:
        await message.answer("❌ Сумма должна быть больше 0")
        return
    balance = user[4]
    if balance < amount:
        await message.answer(f"❌ Недостаточно средств. Ваш баланс: {fmt(balance)}")
        return
    if username.lower() == (message.from_user.username or "").lower():
        await message.answer("❌ Нельзя переводить самому себе")
        return
    target = db.get_user_by_username(username)
    if not target:
        return
    db.update_balance(message.from_user.id, -amount)
    db.update_balance(target[0], amount)
    sender = message.from_user.username or message.from_user.first_name
    await message.answer(f"✅ Переведено {fmt(amount)} → @{username}")
    try:
        await bot.send_message(target[0], f"💸 Вам перевели {fmt(amount)} от @{sender}")
    except Exception:
        pass

@dp.message(lambda m: m.text and m.text.startswith("+") and len(m.text.split()) >= 2 and m.text[1:].split()[0].isdigit())
async def transfer_cmd(message: types.Message):
    user = db.get_user(message.from_user.id)
    status = check_user(user)
    if status == "not_registered":
        await message.answer("❌ Вы не зарегистрированы. Напишите /start")
        return
    if status == "banned":
        await message.answer("⛔ Вы заблокированы.")
        return
    try:
        parts = message.text.split()
        amount = int(parts[0][1:])
        target_username = parts[1].replace("@", "")
    except Exception:
        await message.answer("❌ Формат: +сумма @никнейм")
        return
    if amount <= 0:
        await message.answer("❌ Сумма должна быть больше 0")
        return
    balance = user[4]
    if balance < amount:
        await message.answer(f"❌ Недостаточно средств. Ваш баланс: {fmt(balance)}")
        return
    target = db.get_user_by_username(target_username)
    if not target:
        return
    if target[0] == message.from_user.id:
        await message.answer("❌ Нельзя переводить самому себе")
        return
    db.update_balance(message.from_user.id, -amount)
    db.update_balance(target[0], amount)
    await message.answer(f"✅ Переведено {fmt(amount)} → @{target_username}")
    try:
        sender = message.from_user.username or message.from_user.first_name
        await bot.send_message(target[0], f"💸 Вам перевели {fmt(amount)} от @{sender}")
    except Exception:
        pass

# ==================== КАЗИНО ====================

CASINO_DAILY_LIMIT = 1000

def _casino_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"🎰 Слоты ({fmt(config.CASINO_BET)})", callback_data="cas_slot"),
            InlineKeyboardButton(text=f"🎲 Кубик ({fmt(config.CASINO_BET)})", callback_data="cas_dice"),
        ],
    ])

def _casino_text(user, plays_today: int) -> str:
    balance = user[4]
    remaining = CASINO_DAILY_LIMIT - plays_today
    return (
        f"🎰 <b>КАЗИНО Deutschland RP</b>\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"💵 Баланс: <b>{fmt(balance)}</b>\n"
        f"🎟 Осталось игр сегодня: <b>{remaining}</b>\n\n"
        f"💰 Ставка: <b>{fmt(config.CASINO_BET)}</b>\n"
        f"🎁 Выигрыш: <b>{fmt(config.CASINO_PRIZE)}</b>\n\n"
        f"Выберите игру:"
    )

@dp.message(lambda m: m.text and m.text.lower().strip() == "казино")
async def casino_cmd(message: types.Message):
    user = db.get_user(message.from_user.id)
    status = check_user(user)
    if status == "not_registered":
        await message.answer("❌ Вы не зарегистрированы. Напишите /start")
        return
    if status == "banned":
        await message.answer("⛔ Вы заблокированы.")
        return
    today = time.strftime("%Y-%m-%d")
    plays_today = db.get_casino_plays(message.from_user.id, today)
    await message.answer(_casino_text(user, plays_today), parse_mode="HTML", reply_markup=_casino_menu_kb())

async def _play_casino(callback: types.CallbackQuery, game: str):
    uid = callback.from_user.id
    user = db.get_user(uid)
    if not user:
        await callback.answer("❌ Не зарегистрированы", show_alert=True)
        return
    today = time.strftime("%Y-%m-%d")
    plays_today = db.get_casino_plays(uid, today)
    if plays_today >= CASINO_DAILY_LIMIT:
        await callback.answer("⛔ Лимит игр на сегодня исчерпан", show_alert=True)
        return
    balance = user[4]
    if balance < config.CASINO_BET:
        await callback.answer(f"❌ Нужно {fmt(config.CASINO_BET)}, у вас {fmt(balance)}", show_alert=True)
        return

    db.increment_casino_plays(uid, today)

    if game == "slot":
        symbols = ["🍒", "🍋", "🍇", "🔔", "💎", "7️⃣"]
        reels = [random.choice(symbols) for _ in range(3)]
        win = (reels[0] == reels[1] == reels[2])
        animation = f"{reels[0]} | {reels[1]} | {reels[2]}"
        title = "🎰 СЛОТЫ"
    else:
        roll = random.randint(1, 6)
        dice_emoji = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"][roll - 1]
        win = roll >= 4
        animation = f"{dice_emoji}  ({roll})"
        title = "🎲 КУБИК"

    if win:
        net = config.CASINO_PRIZE - config.CASINO_BET
        db.update_balance(uid, net)
        new_bal = balance + net
        result = f"🎉 <b>ВЫИГРЫШ!</b>\n💰 +{fmt(config.CASINO_PRIZE)}"
    else:
        db.update_balance(uid, -config.CASINO_BET)
        new_bal = balance - config.CASINO_BET
        result = f"💀 <b>Проигрыш</b>\n💸 −{fmt(config.CASINO_BET)}"

    new_user = db.get_user(uid)
    plays_today += 1
    text = (
        f"{title}\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"   {animation}\n"
        f"━━━━━━━━━━━━━━━━━━━\n\n"
        f"{result}\n"
        f"💵 Баланс: <b>{fmt(new_bal)}</b>\n"
        f"🎟 Осталось игр: <b>{CASINO_DAILY_LIMIT - plays_today}</b>"
    )
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=_casino_menu_kb())
    await callback.answer("🎉 Победа!" if win else "💀 Не повезло")

@dp.callback_query(F.data == "cas_slot")
async def cb_cas_slot(callback: types.CallbackQuery):
    await _play_casino(callback, "slot")

@dp.callback_query(F.data == "cas_dice")
async def cb_cas_dice(callback: types.CallbackQuery):
    await _play_casino(callback, "dice")

# ==================== ТОП ====================

@dp.message(lambda m: m.text and m.text.lower() in ["топ", "топ баланс"])
async def top_cmd(message: types.Message):
    players = db.get_top(10)
    medals = ["🥇", "🥈", "🥉"]
    text = "🏆 ТОП ИГРОКОВ ПО БАЛАНСУ\n\n"
    for i, (username, game_name, balance) in enumerate(players, 1):
        icon = medals[i - 1] if i <= 3 else f"{i}."
        text += f"{icon} {game_name} (@{username})\n   💰 {fmt(balance)}\n\n"
    await message.answer(text)

@dp.message(lambda m: m.text and m.text.lower() == "топ имущество")
async def top_wealth_cmd(message: types.Message):
    all_users = db.get_all_users_info()
    wealth = []
    for uid, username, game_name in all_users:
        car_ids = db.get_car_ids(uid)
        biz_ids = db.get_biz_ids(uid)
        apt_ids = db.get_apt_ids(uid)
        car_val = sum(CARS[c][1] for c in car_ids if c in CARS)
        biz_val = sum(BUSINESSES[b][1] for b in biz_ids if b in BUSINESSES)
        apt_val = sum(APARTMENTS[a][1] for a in apt_ids if a in APARTMENTS)
        total = car_val + biz_val + apt_val
        wealth.append((username, game_name, total))
    wealth.sort(key=lambda x: x[2], reverse=True)
    top = wealth[:10]
    medals = ["🥇", "🥈", "🥉"]
    text = "🏠 ТОП ИГРОКОВ ПО ИМУЩЕСТВУ\n\n"
    for i, (username, game_name, total) in enumerate(top, 1):
        if total == 0:
            continue
        icon = medals[i - 1] if i <= 3 else f"{i}."
        text += f"{icon} {game_name} (@{username})\n   💎 {fmt(total)}\n\n"
    if text.strip() == "🏠 ТОП ИГРОКОВ ПО ИМУЩЕСТВУ":
        text += "Пока нет игроков с имуществом."
    await message.answer(text)

# ==================== КУПИТЬ АВТО ====================

@dp.message(lambda m: m.text and m.text.lower().startswith("купить авто"))
async def buy_car(message: types.Message):
    user = db.get_user(message.from_user.id)
    status = check_user(user)
    if status != "ok":
        await message.answer("❌ Вы не зарегистрированы." if status == "not_registered" else "⛔ Вы заблокированы.")
        return
    try:
        car_id = int(message.text.split()[2])
    except Exception:
        await message.answer("❌ Формат: купить авто [номер]")
        return
    if car_id not in CARS:
        await message.answer(f"❌ Авто №{car_id} не найдено. Доступны: 1–140")
        return
    car_name, car_price = CARS[car_id]
    balance = user[4]
    garage_slots = db.get_garage_slots(message.from_user.id)
    current_cars = db.get_cars(message.from_user.id)
    if balance < car_price:
        await message.answer(
            f"🚗 {car_name}\n"
            f"💰 Цена: {fmt(car_price)}\n\n"
            f"❌ Недостаточно средств. Баланс: {fmt(balance)}"
        )
        return
    if len(current_cars) >= garage_slots:
        await message.answer(
            f"🚗 {car_name}\n"
            f"💰 Цена: {fmt(car_price)}\n\n"
            f"❌ Гараж заполнен ({len(current_cars)}/{garage_slots} мест).\n"
            f"Купите дополнительное место в разделе Инфо → Гараж"
        )
        return
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Купить", callback_data=f"bc_{car_id}"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="cbuy_cancel"),
    ]])
    await message.answer(
        f"🚗 {car_name}\n\n"
        f"💰 Цена: {fmt(car_price)}\n"
        f"💵 Ваш баланс: {fmt(balance)}\n\n"
        f"Подтвердить покупку?",
        reply_markup=kb
    )

# ==================== КУПИТЬ БИЗНЕС ====================

@dp.message(lambda m: m.text and m.text.lower().startswith("купить бизнес"))
async def buy_business(message: types.Message):
    user = db.get_user(message.from_user.id)
    status = check_user(user)
    if status != "ok":
        await message.answer("❌ Вы не зарегистрированы." if status == "not_registered" else "⛔ Вы заблокированы.")
        return
    try:
        biz_id = int(message.text.split()[2])
    except Exception:
        await message.answer("❌ Формат: купить бизнес [номер]")
        return
    if biz_id not in BUSINESSES:
        await message.answer(f"❌ Бизнес №{biz_id} не найден. Доступны: 1–48")
        return
    biz_name, biz_price, biz_income = BUSINESSES[biz_id]
    balance = user[4]
    if balance < biz_price:
        await message.answer(
            f"🏢 {biz_name}\n"
            f"💰 Цена: {fmt(biz_price)}\n"
            f"📈 Доход: {fmt(biz_income)}/день\n\n"
            f"❌ Недостаточно средств. Баланс: {fmt(balance)}"
        )
        return
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Купить", callback_data=f"bb_{biz_id}"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="cbuy_cancel"),
    ]])
    await message.answer(
        f"🏢 {biz_name}\n\n"
        f"💰 Цена: {fmt(biz_price)}\n"
        f"📈 Доход: {fmt(biz_income)}/день\n"
        f"💵 Ваш баланс: {fmt(balance)}\n\n"
        f"Подтвердить покупку?",
        reply_markup=kb
    )

# ==================== КУПИТЬ НЕДВИЖИМОСТЬ ====================

@dp.message(lambda m: m.text and m.text.lower().startswith("купить недвижимость"))
async def buy_apt(message: types.Message):
    user = db.get_user(message.from_user.id)
    status = check_user(user)
    if status != "ok":
        await message.answer("❌ Вы не зарегистрированы." if status == "not_registered" else "⛔ Вы заблокированы.")
        return
    try:
        apt_id = int(message.text.split()[2])
    except Exception:
        await message.answer("❌ Формат: купить недвижимость [номер]")
        return
    if apt_id not in APARTMENTS:
        await message.answer(f"❌ Объект №{apt_id} не найден. Доступны: 1–19")
        return
    apt_name, apt_price = APARTMENTS[apt_id]
    balance = user[4]
    if balance < apt_price:
        await message.answer(
            f"🏠 {apt_name}\n"
            f"💰 Цена: {fmt(apt_price)}\n\n"
            f"❌ Недостаточно средств. Баланс: {fmt(balance)}"
        )
        return
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Купить", callback_data=f"ba_{apt_id}"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="cbuy_cancel"),
    ]])
    await message.answer(
        f"🏠 {apt_name}\n\n"
        f"💰 Цена: {fmt(apt_price)}\n"
        f"💵 Ваш баланс: {fmt(balance)}\n\n"
        f"Подтвердить покупку недвижимости?",
        reply_markup=kb
    )

# ==================== ПОДТВЕРЖДЕНИЕ ПОКУПКИ ====================

@dp.callback_query(F.data.startswith("bc_"))
async def confirm_buy_car(callback: types.CallbackQuery):
    user = db.get_user(callback.from_user.id)
    if not user:
        await callback.answer("❌ Не зарегистрированы")
        return
    car_id = int(callback.data.split("_")[1])
    if car_id not in CARS:
        await callback.answer("❌ Авто не найдено")
        return
    car_name, car_price = CARS[car_id]
    balance = user[4]
    garage_slots = db.get_garage_slots(callback.from_user.id)
    current_cars = db.get_cars(callback.from_user.id)
    if len(current_cars) >= garage_slots:
        await callback.answer("❌ Гараж заполнен! Купите место.", show_alert=True)
        return
    if balance < car_price:
        await callback.answer(f"❌ Недостаточно средств. Нужно {fmt(car_price)}", show_alert=True)
        return
    db.update_balance(callback.from_user.id, -car_price)
    db.add_car(callback.from_user.id, car_id, car_name)
    await callback.message.edit_text(
        f"🚗 Поздравляем!\n\n"
        f"Вы купили: {car_name}\n"
        f"Потрачено: {fmt(car_price)}\n"
        f"Остаток: {fmt(balance - car_price)}"
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("bb_"))
async def confirm_buy_biz(callback: types.CallbackQuery):
    user = db.get_user(callback.from_user.id)
    if not user:
        await callback.answer("❌ Не зарегистрированы")
        return
    biz_id = int(callback.data.split("_")[1])
    if biz_id not in BUSINESSES:
        await callback.answer("❌ Бизнес не найден")
        return
    biz_name, biz_price, biz_income = BUSINESSES[biz_id]
    balance = user[4]
    if balance < biz_price:
        await callback.answer(f"❌ Недостаточно средств. Нужно {fmt(biz_price)}", show_alert=True)
        return
    db.update_balance(callback.from_user.id, -biz_price)
    db.add_business(callback.from_user.id, biz_id, biz_name, biz_income)
    await callback.message.edit_text(
        f"🏢 Поздравляем!\n\n"
        f"Вы купили: {biz_name}\n"
        f"Потрачено: {fmt(biz_price)}\n"
        f"Доход: {fmt(biz_income)}/день\n"
        f"Остаток: {fmt(balance - biz_price)}"
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("ba_"))
async def confirm_buy_apt(callback: types.CallbackQuery):
    user = db.get_user(callback.from_user.id)
    if not user:
        await callback.answer("❌ Не зарегистрированы")
        return
    apt_id = int(callback.data.split("_")[1])
    if apt_id not in APARTMENTS:
        await callback.answer("❌ Квартира не найдена")
        return
    apt_name, apt_price = APARTMENTS[apt_id]
    balance = user[4]
    if balance < apt_price:
        await callback.answer(f"❌ Недостаточно средств. Нужно {fmt(apt_price)}", show_alert=True)
        return
    db.update_balance(callback.from_user.id, -apt_price)
    db.add_apartment(callback.from_user.id, apt_id, apt_name)
    await callback.message.edit_text(
        f"🏠 Поздравляем!\n\n"
        f"Вы купили: {apt_name}\n"
        f"Потрачено: {fmt(apt_price)}\n"
        f"Остаток: {fmt(balance - apt_price)}"
    )
    await callback.answer()

@dp.callback_query(F.data == "cbuy_cancel")
async def cancel_buy(callback: types.CallbackQuery):
    await callback.message.edit_text("❌ Покупка отменена.")
    await callback.answer()

# ==================== БАНК ====================

def _bank_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💰 Внести", callback_data="bank_help_dep"),
            InlineKeyboardButton(text="💸 Вывести", callback_data="bank_help_wd"),
        ],
        [
            InlineKeyboardButton(text="📈 Взять кредит", callback_data="bank_help_cr"),
            InlineKeyboardButton(text="✅ Погасить", callback_data="bank_help_rp"),
        ],
        [InlineKeyboardButton(text="🔄 Обновить", callback_data="bank_menu")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_info")],
    ])

def _bank_text(uid: int) -> str:
    db.apply_bank_interest(uid)
    user = db.get_user(uid)
    balance = user[4]
    bank = user[5]
    credit = db.get_credit(uid)
    dep_day = config.BANK_DEPOSIT_RATE_PER_HOUR * 24 * 100
    cr_day = config.BANK_CREDIT_RATE_PER_HOUR * 24 * 100
    return (
        f"🏦 <b>БАНК Deutschland RP</b>\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"💵 Наличные: <b>{fmt(balance)}</b>\n"
        f"🏦 На счёте: <b>{fmt(bank)}</b>\n"
        f"📉 Кредит:  <b>{fmt(credit)}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"📈 Доход по вкладу: <b>+{dep_day:.1f}%</b> в сутки\n"
        f"💢 Кредит растёт: <b>+{cr_day:.1f}%</b> в сутки\n\n"
        f"<b>Команды:</b>\n"
        f"<code>внести [сумма]</code> — положить деньги\n"
        f"<code>вывести [сумма]</code> — снять деньги\n"
        f"<code>кредит [сумма]</code> — взять кредит\n"
        f"<code>погасить [сумма]</code> — погасить кредит"
    )

@dp.message(lambda m: m.text and m.text.lower().strip() == "банк")
async def bank_cmd(message: types.Message):
    user = db.get_user(message.from_user.id)
    if not user:
        await message.answer("❌ Вы не зарегистрированы.")
        return
    await message.answer(_bank_text(message.from_user.id), parse_mode="HTML", reply_markup=_bank_kb())

@dp.callback_query(F.data == "bank_menu")
async def cb_bank_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(_bank_text(callback.from_user.id), parse_mode="HTML", reply_markup=_bank_kb())
    await callback.answer()

_BANK_HELP = {
    "bank_help_dep": "💰 Чтобы внести: напишите внести [сумма]",
    "bank_help_wd":  "💸 Чтобы вывести: напишите вывести [сумма]",
    "bank_help_cr":  "📈 Чтобы взять кредит: напишите кредит [сумма]",
    "bank_help_rp":  "✅ Чтобы погасить: напишите погасить [сумма]",
}

@dp.callback_query(lambda c: c.data in _BANK_HELP)
async def cb_bank_help(callback: types.CallbackQuery):
    await callback.answer(_BANK_HELP[callback.data], show_alert=True)

@dp.message(lambda m: m.text and m.text.lower().startswith("внести "))
async def bank_deposit_cmd(message: types.Message):
    user = db.get_user(message.from_user.id)
    if not user:
        return
    try:
        amount = int(message.text.split()[1])
        if amount <= 0:
            raise ValueError
    except Exception:
        await message.answer("❌ Формат: внести [сумма]")
        return
    db.apply_bank_interest(message.from_user.id)
    user = db.get_user(message.from_user.id)
    if user[4] < amount:
        await message.answer(f"❌ Недостаточно наличных. У вас: {fmt(user[4])}")
        return
    db.bank_deposit(message.from_user.id, amount)
    await message.answer(_bank_text(message.from_user.id), parse_mode="HTML", reply_markup=_bank_kb())

@dp.message(lambda m: m.text and m.text.lower().startswith("вывести "))
async def bank_withdraw_cmd(message: types.Message):
    user = db.get_user(message.from_user.id)
    if not user:
        return
    try:
        amount = int(message.text.split()[1])
        if amount <= 0:
            raise ValueError
    except Exception:
        await message.answer("❌ Формат: вывести [сумма]")
        return
    db.apply_bank_interest(message.from_user.id)
    user = db.get_user(message.from_user.id)
    if user[5] < amount:
        await message.answer(f"❌ Недостаточно на счёте. На счёте: {fmt(user[5])}")
        return
    db.bank_withdraw(message.from_user.id, amount)
    await message.answer(_bank_text(message.from_user.id), parse_mode="HTML", reply_markup=_bank_kb())

@dp.message(lambda m: m.text and m.text.lower().startswith("кредит "))
async def bank_credit_cmd(message: types.Message):
    user = db.get_user(message.from_user.id)
    if not user:
        return
    try:
        amount = int(message.text.split()[1])
        if amount <= 0:
            raise ValueError
    except Exception:
        await message.answer("❌ Формат: кредит [сумма]")
        return
    db.apply_bank_interest(message.from_user.id)
    user = db.get_user(message.from_user.id)
    current_credit = db.get_credit(message.from_user.id)
    max_credit = max(50_000, user[4] * config.CREDIT_LIMIT_MULT)
    if current_credit + amount > max_credit:
        await message.answer(
            f"❌ Превышен лимит кредита.\n"
            f"Макс: {fmt(max_credit)}\n"
            f"Уже взято: {fmt(current_credit)}"
        )
        return
    db.take_credit(message.from_user.id, amount)
    await message.answer(
        f"📈 Кредит выдан: <b>+{fmt(amount)}</b>\n"
        f"⚠️ Не забывайте о процентах!\n\n" + _bank_text(message.from_user.id),
        parse_mode="HTML", reply_markup=_bank_kb()
    )

@dp.message(lambda m: m.text and m.text.lower().startswith("погасить "))
async def bank_repay_cmd(message: types.Message):
    user = db.get_user(message.from_user.id)
    if not user:
        return
    try:
        amount = int(message.text.split()[1])
        if amount <= 0:
            raise ValueError
    except Exception:
        await message.answer("❌ Формат: погасить [сумма]")
        return
    db.apply_bank_interest(message.from_user.id)
    user = db.get_user(message.from_user.id)
    credit = db.get_credit(message.from_user.id)
    if credit <= 0:
        await message.answer("ℹ️ У вас нет долга.")
        return
    if amount > credit:
        amount = int(credit)
    if user[4] < amount:
        await message.answer(f"❌ Не хватает наличных. У вас: {fmt(user[4])}")
        return
    db.repay_credit(message.from_user.id, amount)
    await message.answer(
        f"✅ Погашено: <b>−{fmt(amount)}</b>\n\n" + _bank_text(message.from_user.id),
        parse_mode="HTML", reply_markup=_bank_kb()
    )

# ==================== МОИ АКТИВЫ ====================

@dp.message(lambda m: m.text and m.text.lower() in ["мои авто", "гараж"])
async def my_cars(message: types.Message):
    user = db.get_user(message.from_user.id)
    if not user:
        await message.answer("❌ Вы не зарегистрированы.")
        return
    cars = db.get_cars_full(message.from_user.id)
    has_lic = db.has_license(message.from_user.id)
    lic_text = "✅ Права есть" if has_lic else "❌ Прав нет"
    if not cars:
        await message.answer(f"🚗 У вас нет автомобилей\n{lic_text}\nКупить: купить авто [номер]")
        return
    text = f"🚗 Ваши автомобили:\n🪪 {lic_text}\n\n"
    for i, (db_id, name, token, plate) in enumerate(cars, 1):
        plate_str = plate if plate else "нет номеров"
        text += f"{i}. {name}\n   🔑 {token} | 🔢 {plate_str}\n"
    await message.answer(text)

@dp.message(lambda m: m.text and m.text.lower() in ["мои бизнесы", "бизнесы"])
async def my_businesses(message: types.Message):
    user = db.get_user(message.from_user.id)
    if not user:
        await message.answer("❌ Вы не зарегистрированы.")
        return
    bizs = db.get_businesses_full(message.from_user.id)
    if not bizs:
        await message.answer("🏢 У вас нет бизнесов\nКупить: купить бизнес [номер]")
        return
    text = "🏢 Ваши бизнесы:\n\n"
    for i, (bid, name, income, token) in enumerate(bizs, 1):
        text += f"{i}. {name}\n   💵 {fmt(income)}/день | 🔑 {token}\n"
    await message.answer(text)

@dp.message(lambda m: m.text and m.text.lower() in ["мои объекты", "недвижимость", "мои квартиры"])
async def my_apts(message: types.Message):
    user = db.get_user(message.from_user.id)
    if not user:
        await message.answer("❌ Вы не зарегистрированы.")
        return
    apts = db.get_apartments_full(message.from_user.id)
    if not apts:
        await message.answer("🏠 У вас нет недвижимости\nКупить: купить недвижимость [номер]")
        return
    text = "🏠 Ваша недвижимость:\n\n"
    for i, (aid, name, token) in enumerate(apts, 1):
        text += f"{i}. {name} | 🔑 {token}\n"
    await message.answer(text)

# ==================== ИНЛАЙН КНОПКИ ====================

def build_garage_kb(uid, cars_full, garage_slots, has_lic):
    buttons = []
    if not has_lic:
        buttons.append([InlineKeyboardButton(
            text="🪪 Купить права — 200€",
            callback_data="buy_license"
        )])
    for db_id, car_name, token, plate in cars_full:
        buttons.append([InlineKeyboardButton(
            text=f"🚗 {car_name}",
            callback_data=f"car_det_{db_id}"
        )])
    next_slot = garage_slots + 1
    if next_slot in GARAGE_SLOT_PRICES:
        price = GARAGE_SLOT_PRICES[next_slot]
        buttons.append([InlineKeyboardButton(
            text=f"🔓 Пополнить место в гараже — {fmt(price)}",
            callback_data=f"buy_slot_{next_slot}"
        )])
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_info")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def build_profile_text(user):
    uid, username, spm_id, game_name, balance, bank, btc, job, last_salary, banned, *_ = user
    text = (
        f"👤 Профиль игрока\n\n"
        f"🆔 CPM айди: {spm_id}\n"
        f"🎮 Имя в игре: {game_name}\n"
        f"📱 Ник в TG: @{username}\n"
        f"💰 Баланс: {fmt(balance)}\n"
        f"🏦 Банк: {fmt(bank)}\n"
        f"₿ BTC: {btc:.4f}\n"
        f"💼 Работа: {job if job else 'Безработный'}"
    )
    orgs = db.get_user_orgs(uid)
    if orgs:
        text += "\n\n━━━━━━━━━━━━━━━━━━━━━"
        for org_type, is_owner in orgs:
            info = db.ORG_DISPLAY.get(org_type)
            if info:
                icon, _ = info
                org_name = db.get_org_name(org_type)
                role = "👑 Владелец" if is_owner else "👤 Участник"
                text += f"\n{icon} {org_name} — {role}"
        text += "\n━━━━━━━━━━━━━━━━━━━━━"
    credit = db.get_credit(uid)
    if credit > 0:
        text += f"\n\n📉 Кредит: {fmt(credit)}"
    return text

@dp.callback_query(F.data == "back_to_info")
async def cb_back_to_info(callback: types.CallbackQuery):
    user = db.get_user(callback.from_user.id)
    if not user:
        await callback.answer("❌ Не зарегистрированы")
        return
    await callback.message.edit_text(build_profile_text(user), reply_markup=info_keyboard())
    await callback.answer()

async def _show_garage(callback: types.CallbackQuery):
    uid = callback.from_user.id
    cars_full = db.get_cars_full(uid)
    garage_slots = db.get_garage_slots(uid)
    has_lic = db.has_license(uid)
    lic_icon = "✅" if has_lic else "❌"
    text = (
        f"🚗 Ваш гараж ({len(cars_full)}/{garage_slots} мест)\n\n"
        f"🪪 Права: {lic_icon} {'Есть' if has_lic else 'Нет'}\n\n"
    )
    if not cars_full:
        text += "Гараж пустой\n📝 Купить авто: купить авто [номер]"
    await callback.message.edit_text(
        text,
        reply_markup=build_garage_kb(uid, cars_full, garage_slots, has_lic)
    )

@dp.callback_query(F.data == "list_cars")
async def cb_cars(callback: types.CallbackQuery):
    user = db.get_user(callback.from_user.id)
    if not user:
        await callback.answer("❌ Не зарегистрированы")
        return
    await _show_garage(callback)
    await callback.answer()

@dp.callback_query(F.data == "buy_license")
async def cb_buy_license(callback: types.CallbackQuery):
    user = db.get_user(callback.from_user.id)
    if not user:
        await callback.answer("❌ Не зарегистрированы")
        return
    uid = user[0]
    PRICE = 200
    if db.has_license(uid):
        await callback.answer("✅ У вас уже есть права!", show_alert=True)
        return
    if user[4] < PRICE:
        await callback.answer("❌ Недостаточно денег. Нужно 200€", show_alert=True)
        return
    db.update_balance(uid, -PRICE)
    db.set_license(uid, True)
    await callback.answer("✅ Права получены!", show_alert=True)
    await _show_garage(callback)

@dp.callback_query(F.data.startswith("car_det_"))
async def cb_car_detail(callback: types.CallbackQuery):
    user = db.get_user(callback.from_user.id)
    if not user:
        await callback.answer("❌ Не зарегистрированы")
        return
    try:
        db_id = int(callback.data.split("_")[2])
    except Exception:
        await callback.answer("❌ Ошибка")
        return
    car = db.get_car_by_dbid(db_id)
    if not car or car[1] != callback.from_user.id:
        await callback.answer("❌ Авто не найдено", show_alert=True)
        return
    cdb_id, uid, car_id, car_name, token, plate = car
    plate_text = f"✅ {plate}" if plate else "❌ Нет номеров"
    text = (
        f"🚗 {car_name}\n\n"
        f"🔑 Токен: {token}\n"
        f"🔢 Номера: {plate_text}"
    )
    buttons = []
    if not plate:
        buttons.append([InlineKeyboardButton(
            text="🔢 Купить номера — 200€",
            callback_data=f"buy_plate_{db_id}"
        )])
    else:
        buttons.append([InlineKeyboardButton(
            text="🔄 Перебить номера — 200€",
            callback_data=f"reroll_plate_{db_id}"
        )])
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="list_cars")])
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    await callback.answer()

@dp.callback_query(lambda c: c.data and (c.data.startswith("buy_plate_") or c.data.startswith("reroll_plate_")))
async def cb_plate_action(callback: types.CallbackQuery):
    user = db.get_user(callback.from_user.id)
    if not user:
        await callback.answer("❌ Не зарегистрированы")
        return
    parts = callback.data.split("_")
    db_id = int(parts[2])
    PRICE = 200
    car = db.get_car_by_dbid(db_id)
    if not car or car[1] != callback.from_user.id:
        await callback.answer("❌ Авто не найдено", show_alert=True)
        return
    if user[4] < PRICE:
        await callback.answer("❌ Недостаточно денег. Нужно 200€", show_alert=True)
        return
    db.update_balance(user[0], -PRICE)
    plate = db.gen_plate()
    db.update_car_plate(db_id, plate)
    cdb_id, uid, car_id, car_name, token, _ = car
    text = (
        f"🚗 {car_name}\n\n"
        f"🔑 Токен: {token}\n"
        f"🔢 Номера: ✅ {plate}"
    )
    buttons = [[InlineKeyboardButton(
        text="🔄 Перебить номера — 200€",
        callback_data=f"reroll_plate_{db_id}"
    )], [InlineKeyboardButton(text="🔙 Назад", callback_data="list_cars")]]
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    await callback.answer(f"✅ Номера: {plate}")

@dp.callback_query(F.data.startswith("buy_slot_"))
async def cb_buy_garage_slot(callback: types.CallbackQuery):
    user = db.get_user(callback.from_user.id)
    if not user:
        await callback.answer("❌ Не зарегистрированы")
        return
    uid = user[0]
    balance = user[4]
    slot_num = int(callback.data.split("_")[2])
    price = GARAGE_SLOT_PRICES.get(slot_num)
    if not price:
        await callback.answer("❌ Место не найдено")
        return
    current_slots = db.get_garage_slots(uid)
    if current_slots >= slot_num:
        await callback.answer("✅ Место уже куплено")
        return
    if balance < price:
        await callback.answer(f"❌ Недостаточно денег. Нужно {fmt(price)}", show_alert=True)
        return
    db.update_balance(uid, -price)
    db.update_garage_slots(uid, slot_num)
    await callback.answer(f"✅ Куплено {slot_num}-е место в гараже!")
    await _show_garage(callback)

JOBS_LIST = list(JOBS.items())
GOV_JOBS_LIST = list(GOV_JOBS.items())

JOBS_PER_PAGE = 5

GOV_JOB_CATEGORIES = [
    ("🏥 Медицина", [
        "Парамедик (Скорая помощь)", "Врач неотложной помощи", "Хирург", "Главврач",
    ]),
    ("⚖️ Юстиция", [
        "Помощник прокурора", "Прокурор", "Старший прокурор", "Прокурор района",
        "Прокурор города", "Прокурор области", "Генеральный прокурор", "Судья", "Адвокат",
    ]),
    ("🏛 Правительство", [
        "Охранник Правительства", "Водитель Правительства", "Секретарь Правительства",
        "Депутат", "Министр", "Заместитель губернатора", "Губернатор",
        "Телохранитель правительства", "Бургомистр (Мэр)", "Министр обороны",
        "Министр МВД", "Министр здравоохранения", "Вице-канцлер", "Федеральный канцлер",
    ]),
    ("👮 Полиция", [
        "Курсант (Стажер)", "Мастер полиции", "Комиссар полиции", "Старший комиссар",
        "Главный комиссар (Детектив)", "Директор полиции", "Президент полиции (Шеф)",
        "Спецагент BKA", "Оперативник GSG 9", "Командир GSG 9 (Спецназ)",
        "Президент BKA (Уголовный розыск)",
    ]),
    ("🎖 Армия", [
        "Ефрейтор (Рядовой)", "Унтер-офицер (Сержант)", "Лейтенант",
        "Майор", "Подполковник", "Полковник", "Генерал",
    ]),
]

def _main_jobs_kb(has_job: bool) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text="💼 Гражданские работы", callback_data="jobs_civ_0")],
        [InlineKeyboardButton(text="🏛 Гос. должности", callback_data="jobs_gov_cats")],
    ]
    if has_job:
        rows.append([InlineKeyboardButton(text="🚪 Уволиться", callback_data="quit_job")])
    rows.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_info")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def _civ_jobs_kb(page: int, has_job: bool) -> InlineKeyboardMarkup:
    total = len(JOBS_LIST)
    total_pages = (total + JOBS_PER_PAGE - 1) // JOBS_PER_PAGE
    start = page * JOBS_PER_PAGE
    chunk = JOBS_LIST[start:start + JOBS_PER_PAGE]
    rows = []
    for i, (job_name, salary) in enumerate(chunk):
        rows.append([InlineKeyboardButton(
            text=f"💼 {job_name} — {fmt(salary)}",
            callback_data=f"apj_{start + i}"
        )])
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="◀️", callback_data=f"jobs_civ_{page - 1}"))
    nav.append(InlineKeyboardButton(text=f"{page + 1}/{total_pages}", callback_data="noop"))
    if start + JOBS_PER_PAGE < total:
        nav.append(InlineKeyboardButton(text="▶️", callback_data=f"jobs_civ_{page + 1}"))
    rows.append(nav)
    if has_job:
        rows.append([InlineKeyboardButton(text="🚪 Уволиться", callback_data="quit_job")])
    rows.append([InlineKeyboardButton(text="🔙 Назад", callback_data="list_jobs")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def _gov_cats_kb() -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(text=cat, callback_data=f"jobs_gov_{i}")]
            for i, (cat, _) in enumerate(GOV_JOB_CATEGORIES)]
    rows.append([InlineKeyboardButton(text="🔙 Назад", callback_data="list_jobs")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def _gov_cat_kb(cat_id: int) -> InlineKeyboardMarkup:
    _, jobs = GOV_JOB_CATEGORIES[cat_id]
    rows = []
    for job_name in jobs:
        salary = GOV_JOBS.get(job_name, 0)
        rows.append([InlineKeyboardButton(
            text=f"🔒 {job_name} — {fmt(salary)}",
            callback_data="gov_locked"
        )])
    rows.append([InlineKeyboardButton(text="🔙 Назад", callback_data="jobs_gov_cats")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

@dp.callback_query(F.data == "noop")
async def cb_noop(callback: types.CallbackQuery):
    await callback.answer()

@dp.callback_query(F.data == "gov_locked")
async def cb_gov_locked(callback: types.CallbackQuery):
    await callback.answer(
        "🔒 Гос. должность\n\nНазначается только администратором.",
        show_alert=True
    )

@dp.callback_query(F.data == "list_jobs")
async def cb_jobs(callback: types.CallbackQuery):
    user = db.get_user(callback.from_user.id)
    if not user:
        await callback.answer("❌ Не зарегистрированы")
        return
    job = user[7]
    salary = ALL_JOBS.get(job, 0) if job else 0
    if job:
        job_type = "🏛 Гос. должность" if job in GOV_JOBS else "💼 Гражданская работа"
        text = (
            f"💼 Работа\n\n"
            f"📋 Должность: {job}\n"
            f"💵 Зарплата: {fmt(salary)}\n"
            f"📌 Тип: {job_type}\n\n"
            f"Получить зарплату: зп"
        )
    else:
        text = "💼 Биржа труда\n\nВыбери раздел:"
    await callback.message.edit_text(text, reply_markup=_main_jobs_kb(bool(job)))
    await callback.answer()

@dp.callback_query(F.data.startswith("jobs_civ_"))
async def cb_jobs_civ(callback: types.CallbackQuery):
    user = db.get_user(callback.from_user.id)
    if not user:
        await callback.answer("❌ Не зарегистрированы")
        return
    try:
        page = int(callback.data.split("_")[2])
    except Exception:
        page = 0
    total_pages = (len(JOBS_LIST) + JOBS_PER_PAGE - 1) // JOBS_PER_PAGE
    text = f"💼 Гражданские работы — стр. {page + 1}/{total_pages}\n\nВыбери профессию:"
    await callback.message.edit_text(text, reply_markup=_civ_jobs_kb(page, bool(user[7])))
    await callback.answer()

@dp.callback_query(F.data == "jobs_gov_cats")
async def cb_gov_cats(callback: types.CallbackQuery):
    text = (
        "🏛 Гос. должности\n\n"
        "Выбери ведомство:\n\n"
        "🔒 Все должности назначаются только администратором."
    )
    await callback.message.edit_text(text, reply_markup=_gov_cats_kb())
    await callback.answer()

@dp.callback_query(F.data.startswith("jobs_gov_"))
async def cb_gov_cat_jobs(callback: types.CallbackQuery):
    try:
        cat_id = int(callback.data.split("_")[2])
        cat_name, _ = GOV_JOB_CATEGORIES[cat_id]
    except Exception:
        await callback.answer("❌ Ошибка")
        return
    text = f"{cat_name}\n\n🔒 Все должности назначаются только администратором.\n\nНажми на должность для просмотра зарплаты."
    await callback.message.edit_text(text, reply_markup=_gov_cat_kb(cat_id))
    await callback.answer()

@dp.callback_query(F.data.startswith("apj_"))
async def cb_apply_job(callback: types.CallbackQuery):
    user = db.get_user(callback.from_user.id)
    if not user:
        await callback.answer("❌ Не зарегистрированы")
        return
    try:
        idx = int(callback.data.split("_")[1])
        job_name, salary = JOBS_LIST[idx]
    except Exception:
        await callback.answer("❌ Ошибка")
        return
    current_job = user[7]
    if current_job == job_name:
        await callback.answer(f"Вы уже работаете: {job_name}", show_alert=True)
        return
    db.set_job(user[0], job_name)
    text = (
        f"✅ Вы устроились на работу!\n\n"
        f"💼 Должность: {job_name}\n"
        f"💵 Зарплата: {fmt(salary)}\n\n"
        f"Получить зарплату: зп"
    )
    await callback.message.edit_text(text, reply_markup=back_keyboard())
    await callback.answer(f"✅ Вы теперь {job_name}!")

@dp.callback_query(F.data == "quit_job")
async def cb_quit_job(callback: types.CallbackQuery):
    user = db.get_user(callback.from_user.id)
    if not user:
        await callback.answer("❌ Не зарегистрированы")
        return
    job = user[7]
    if not job:
        await callback.answer("У вас нет работы", show_alert=True)
        return
    if job in GOV_JOBS:
        await callback.answer("❌ Уволиться с гос. должности может только администратор", show_alert=True)
        return
    db.set_job(user[0], "")
    await callback.message.edit_text(
        "🚪 Вы уволились с работы.\n\nВыбрать новую работу: инфо → Работа",
        reply_markup=back_keyboard()
    )
    await callback.answer("Вы уволились")

@dp.callback_query(F.data == "list_biz")
async def cb_biz(callback: types.CallbackQuery):
    user = db.get_user(callback.from_user.id)
    if not user:
        await callback.answer("❌ Не зарегистрированы")
        return
    bizs = db.get_businesses_full(callback.from_user.id)
    text = "🏢 Ваши бизнесы\n\n"
    if bizs:
        total = sum(inc for _, _, inc, _ in bizs)
        for i, (bid, name, income, token) in enumerate(bizs, 1):
            text += f"{i}. {name}\n   💵 {fmt(income)}/день | 🔑 {token}\n"
        text += f"\n📈 Суммарный доход: {fmt(total)}/день"
    else:
        text += "У вас нет бизнесов.\n📝 Купить: купить бизнес [номер]"
    await callback.message.edit_text(text, reply_markup=back_keyboard())
    await callback.answer()

@dp.callback_query(F.data == "list_apts")
async def cb_apts(callback: types.CallbackQuery):
    user = db.get_user(callback.from_user.id)
    if not user:
        await callback.answer("❌ Не зарегистрированы")
        return
    apts = db.get_apartments_full(callback.from_user.id)
    text = "🏠 Ваша недвижимость\n\n"
    if apts:
        for i, (aid, name, token) in enumerate(apts, 1):
            text += f"{i}. {name} | 🔑 {token}\n"
    else:
        text += "У вас нет недвижимости.\n📝 Купить: купить недвижимость [номер]"
    await callback.message.edit_text(text, reply_markup=back_keyboard())
    await callback.answer()

# ==================== ПРОДАЖА ИМУЩЕСТВА ====================

def _parse_sell_cmd(text: str):
    parts = text.strip().split()
    if len(parts) < 3:
        return None
    asset_map = {
        "авто": "car", "машину": "car", "машина": "car",
        "бизнес": "biz",
        "квартиру": "apt", "недвижимость": "apt", "объект": "apt",
    }
    asset_raw = parts[1].lower()
    asset_type = asset_map.get(asset_raw)
    if not asset_type:
        return None
    token = parts[2].upper()
    if len(parts) >= 5:
        nick = next((p for p in parts[3:] if p.startswith("@")), None)
        price_str = next((p for p in parts[3:] if p.isdigit()), None)
        if nick and price_str:
            return {"type": asset_type, "token": token, "nick": nick[1:], "price": int(price_str)}
    return {"type": asset_type, "token": token, "nick": None, "price": None}

def _get_asset_price(asset_type: str, asset_id: int) -> int:
    if asset_type == "car":
        data = CARS.get(asset_id)
        return data[1] if data else 0
    elif asset_type == "biz":
        data = BUSINESSES.get(asset_id)
        return data[1] if data else 0
    elif asset_type == "apt":
        data = APARTMENTS.get(asset_id)
        return data[1] if data else 0
    return 0

@dp.message(lambda m: m.text and m.text.lower().startswith("продать "))
async def sell_asset_cmd(message: types.Message):
    user = db.get_user(message.from_user.id)
    status = check_user(user)
    if status != "ok":
        await message.answer("❌ Вы не зарегистрированы." if status == "not_registered" else "⛔ Вы заблокированы.")
        return

    parsed = _parse_sell_cmd(message.text)
    if not parsed:
        await message.answer("❌ Формат: продать авто/бизнес/недвижимость [токен] [@ник цена]")
        return

    atype = parsed["type"]
    token = parsed["token"]
    uid = user[0]

    if atype == "car":
        asset = db.get_car_by_token(token)
    elif atype == "biz":
        asset = db.get_business_by_token(token)
    else:
        asset = db.get_apartment_by_token(token)

    if not asset or asset[1] != uid:
        await message.answer("❌ Актив не найден или не является вашим.")
        return

    db_id = asset[0]
    asset_name = asset[3]
    asset_id = asset[2]
    full_price = _get_asset_price(atype, asset_id)
    state_price = full_price // 2

    type_names = {"car": "Автомобиль", "biz": "Бизнес", "apt": "Недвижимость"}
    type_name = type_names[atype]

    if parsed["nick"] and parsed["price"]:
        target_nick = parsed["nick"]
        sale_price = parsed["price"]
        target = db.get_user_by_username(target_nick)
        if not target:
            await message.answer(f"❌ Игрок @{target_nick} не найден.")
            return
        if target[0] == uid:
            await message.answer("❌ Нельзя продавать самому себе.")
            return

        import secrets as _secrets
        sale_token = _secrets.token_hex(4).upper()

        PENDING_SALES[sale_token] = {
            "type": atype, "db_id": db_id, "seller_uid": uid,
            "buyer_uid": target[0], "price": sale_price, "name": asset_name
        }

        seller_nick = message.from_user.username or message.from_user.first_name
        offer_text = (
            f"💼 Предложение о покупке от @{seller_nick}\n\n"
            f"📋 {type_name}: {asset_name}\n"
            f"🔑 Токен: {sale_token}\n"
            f"💰 Цена: {fmt(sale_price)}\n\n"
            f"Ваш баланс: {fmt(target[4])}"
        )
        kb = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="✅ Принять", callback_data=f"asale_{sale_token}"),
            InlineKeyboardButton(text="❌ Отказать", callback_data=f"rsale_{sale_token}"),
        ]])
        try:
            await bot.send_message(target[0], offer_text, reply_markup=kb)
        except Exception:
            PENDING_SALES.pop(sale_token, None)
            await message.answer(f"❌ Не удалось отправить предложение @{target_nick}.")
            return
        await message.answer(
            f"✅ Предложение отправлено @{target_nick}!\n\n"
            f"📋 {asset_name} | {fmt(sale_price)}\n"
            f"Ожидаем ответа покупателя."
        )
    else:
        kb = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=f"✅ Продать за {fmt(state_price)}", callback_data=f"csell_{atype}_{token}"),
            InlineKeyboardButton(text="❌ Отмена", callback_data=f"xsell_{token}"),
        ]])
        await message.answer(
            f"🏛 Продажа государству (50% от стоимости)\n\n"
            f"📋 {type_name}: {asset_name}\n"
            f"💰 Получите: {fmt(state_price)}\n\n"
            f"Или: продать авто {token} @ник [цена]",
            reply_markup=kb
        )

@dp.callback_query(lambda c: c.data and c.data.startswith("csell_"))
async def cb_confirm_sell_state(callback: types.CallbackQuery):
    user = db.get_user(callback.from_user.id)
    if not user:
        await callback.answer("❌ Не зарегистрированы")
        return
    parts = callback.data.split("_")
    atype = parts[1]
    token = "_".join(parts[2:])
    uid = user[0]

    if atype == "car":
        asset = db.get_car_by_token(token)
    elif atype == "biz":
        asset = db.get_business_by_token(token)
    else:
        asset = db.get_apartment_by_token(token)

    if not asset or asset[1] != uid:
        await callback.answer("❌ Актив не найден или не ваш", show_alert=True)
        return

    db_id = asset[0]
    asset_name = asset[3]
    asset_id = asset[2]
    full_price = _get_asset_price(atype, asset_id)
    state_price = full_price // 2

    if atype == "car":
        db.remove_car_db(db_id)
    elif atype == "biz":
        db.remove_business_db(db_id)
    else:
        db.remove_apartment_db(db_id)

    db.update_balance(uid, state_price)
    type_names = {"car": "Автомобиль", "biz": "Бизнес", "apt": "Недвижимость"}
    await callback.message.edit_text(
        f"✅ {type_names[atype]} продан государству!\n\n"
        f"📋 {asset_name}\n"
        f"💰 Получено: +{fmt(state_price)}\n"
        f"💵 Баланс: {fmt(user[4] + state_price)}"
    )
    await callback.answer("✅ Продано!")

@dp.callback_query(lambda c: c.data and c.data.startswith("xsell_"))
async def cb_cancel_sell(callback: types.CallbackQuery):
    await callback.message.edit_text("❌ Продажа отменена.")
    await callback.answer("Отменено")

@dp.callback_query(lambda c: c.data and c.data.startswith("asale_"))
async def cb_accept_sale(callback: types.CallbackQuery):
    token = callback.data[6:]
    sale = PENDING_SALES.get(token)
    if not sale:
        await callback.answer("❌ Предложение устарело или отменено", show_alert=True)
        await callback.message.edit_reply_markup()
        return
    if callback.from_user.id != sale["buyer_uid"]:
        await callback.answer("❌ Это предложение не для вас", show_alert=True)
        return

    buyer = db.get_user(sale["buyer_uid"])
    if not buyer or buyer[4] < sale["price"]:
        await callback.answer("❌ Недостаточно средств на балансе", show_alert=True)
        return

    db.update_balance(sale["buyer_uid"], -sale["price"])
    db.update_balance(sale["seller_uid"], sale["price"])

    atype = sale["type"]
    db_id = sale["db_id"]
    if atype == "car":
        db.transfer_car(db_id, sale["buyer_uid"])
    elif atype == "biz":
        db.transfer_business(db_id, sale["buyer_uid"])
    else:
        db.transfer_apartment(db_id, sale["buyer_uid"])

    PENDING_SALES.pop(token, None)
    type_names = {"car": "Автомобиль", "biz": "Бизнес", "apt": "Недвижимость"}
    tn = type_names.get(atype, "Актив")

    await callback.message.edit_text(
        f"✅ Покупка совершена!\n\n"
        f"📋 {tn}: {sale['name']}\n"
        f"💰 Оплачено: {fmt(sale['price'])}\n"
        f"💵 Баланс: {fmt(buyer[4] - sale['price'])}"
    )
    await callback.answer("✅ Сделка совершена!")
    try:
        buyer_nick = buyer[1] or "Покупатель"
        await bot.send_message(
            sale["seller_uid"],
            f"✅ Deutschland RP — Сделка совершена!\n\n"
            f"📋 {tn}: {sale['name']}\n"
            f"👤 Покупатель: @{buyer_nick}\n"
            f"💰 Получено: +{fmt(sale['price'])}"
        )
    except Exception:
        pass

@dp.callback_query(lambda c: c.data and c.data.startswith("rsale_"))
async def cb_reject_sale(callback: types.CallbackQuery):
    token = callback.data[6:]
    sale = PENDING_SALES.get(token)
    if not sale:
        await callback.answer("❌ Предложение не найдено", show_alert=True)
        return
    if callback.from_user.id != sale["buyer_uid"]:
        await callback.answer("❌ Это предложение не для вас", show_alert=True)
        return
    PENDING_SALES.pop(token, None)
    await callback.message.edit_text("❌ Вы отказались от покупки.")
    await callback.answer("Отказано")
    try:
        buyer = db.get_user(sale["buyer_uid"])
        buyer_nick = (buyer[1] if buyer else None) or "Покупатель"
        await bot.send_message(
            sale["seller_uid"],
            f"❌ @{buyer_nick} отказался от покупки {sale['name']}."
        )
    except Exception:
        pass

# ==================== ОРГАНИЗАЦИИ ====================

ORG_KEYWORDS = {
    "ф1":     "ф1",
    "футбол": "футбол",
    "семья":  "семья",
}

def _parse_org_cmd(text: str):
    parts = text.strip().split()
    if len(parts) < 2:
        return None
    key = parts[0].lower()
    if key not in ORG_KEYWORDS:
        return None
    target = parts[1]
    is_owner = False
    name = None
    if len(parts) >= 3:
        if parts[2].lower() == "владелец":
            is_owner = True
            if len(parts) >= 4:
                name = " ".join(parts[3:])
        else:
            name = " ".join(parts[2:])
    return ORG_KEYWORDS[key], target, is_owner, name

@dp.message(lambda m: m.text and m.text.strip().split()[0].lower() in ORG_KEYWORDS and m.from_user and m.from_user.id in config.ADMIN_IDS)
async def org_add_cmd(message: types.Message):
    parsed = _parse_org_cmd(message.text)
    if not parsed:
        await message.answer("❌ Формат: ф1 @юз [владелец]")
        return
    org_key, target_str, is_owner, custom_name = parsed
    target_user = None
    if target_str.startswith("@"):
        target_user = db.get_user_by_username(target_str[1:])
    else:
        try:
            target_user = db.get_user(int(target_str))
        except Exception:
            pass
    if not target_user:
        return
    target_uid = target_user[0]
    target_name = f"@{target_user[1]}" if target_user[1] else str(target_uid)
    db.add_org_member(target_uid, org_key, is_owner)
    if custom_name:
        db.set_org_name(org_key, custom_name)
    icon, _default = db.ORG_DISPLAY[org_key]
    org_name = db.get_org_name(org_key)
    role = "👑 Владелец" if is_owner else "👤 Участник"
    name_note = f"\n📝 Название: {org_name}" if custom_name else ""
    await message.answer(
        f"✅ {icon} {org_name}{name_note}\n\n"
        f"Игрок {target_name} добавлен как {role}"
    )
    try:
        await bot.send_message(
            target_uid,
            f"🎉 Вас добавили в организацию!\n\n"
            f"{icon} <b>{org_name}</b>\n"
            f"Статус: {role}\n\n"
            f"Это отображается в вашем профиле (инфо → Организации).",
            parse_mode="HTML"
        )
    except Exception:
        pass

@dp.message(lambda m: m.text and m.text.lower().startswith("имя ") and m.from_user and m.from_user.id in config.ADMIN_IDS)
async def org_rename_cmd(message: types.Message):
    parts = message.text.strip().split(maxsplit=2)
    if len(parts) < 3:
        await message.answer("❌ Формат: имя ф1 [новое название]")
        return
    org_key = parts[1].lower()
    if org_key not in ORG_KEYWORDS:
        await message.answer("❌ Доступно: ф1, футбол, семья")
        return
    new_name = parts[2].strip()
    db.set_org_name(org_key, new_name)
    icon, _ = db.ORG_DISPLAY[org_key]
    await message.answer(f"✅ {icon} Название обновлено: <b>{new_name}</b>", parse_mode="HTML")

@dp.message(lambda m: m.text and m.text.lower().startswith("убрать ") and m.from_user and m.from_user.id in config.ADMIN_IDS)
async def org_remove_cmd(message: types.Message):
    parts = message.text.strip().split()
    if len(parts) < 3:
        await message.answer("❌ Формат: убрать ф1 @юз")
        return
    org_key = parts[1].lower()
    if org_key not in ORG_KEYWORDS:
        return
    target_str = parts[2]
    target_user = None
    if target_str.startswith("@"):
        target_user = db.get_user_by_username(target_str[1:])
    else:
        try:
            target_user = db.get_user(int(target_str))
        except Exception:
            pass
    if not target_user:
        return
    target_uid = target_user[0]
    target_name = f"@{target_user[1]}" if target_user[1] else str(target_uid)
    db.remove_org_member(target_uid, org_key)
    icon, org_name = db.ORG_DISPLAY[org_key]
    await message.answer(f"✅ {target_name} убран из «{icon} {org_name}»")
    try:
        await bot.send_message(
            target_uid,
            f"ℹ️ Вас убрали из организации {icon} <b>{org_name}</b>.",
            parse_mode="HTML"
        )
    except Exception:
        pass

@dp.message(lambda m: m.text and m.text.lower().startswith("состав") and m.from_user and m.from_user.id in config.ADMIN_IDS)
async def org_roster_cmd(message: types.Message):
    parts = message.text.strip().split()
    if len(parts) < 2:
        await message.answer("❌ Формат: состав ф1 / состав футбол / состав семья")
        return
    org_key = parts[1].lower()
    if org_key not in ORG_KEYWORDS:
        await message.answer("❌ Неизвестная организация. Доступно: ф1, футбол, семья")
        return
    await message.answer(_render_org_card(org_key), parse_mode="HTML")

def _render_org_card(org_key: str) -> str:
    icon, _ = db.ORG_DISPLAY[org_key]
    org_name = db.get_org_name(org_key)
    members = db.get_org_members(org_key)
    text = f"{icon} <b>{org_name}</b>\n"
    if not members:
        text += "\n<i>Пусто — нет участников.</i>"
        return text
    owners = []
    participants = []
    for uid, is_owner in members:
        u = db.get_user(uid)
        name = f"@{u[1]}" if u and u[1] else str(uid)
        game = f" — {u[3]}" if u and u[3] else ""
        if is_owner:
            owners.append(f"  👑 {name}{game}")
        else:
            participants.append(f"  • {name}{game}")
    if owners:
        text += "\n👑 <b>Владелец:</b>\n" + "\n".join(owners)
    if participants:
        text += f"\n\n👥 <b>Участники ({len(participants)}):</b>\n" + "\n".join(participants)
    return text

@dp.callback_query(F.data == "list_orgs")
async def cb_list_orgs(callback: types.CallbackQuery):
    uid = callback.from_user.id
    orgs = db.get_user_orgs(uid)
    if not orgs:
        await callback.message.edit_text(
            "🏛️ <b>Организации</b>\n\n<i>Вы пока ни в одной организации не состоите.</i>",
            parse_mode="HTML",
            reply_markup=back_keyboard()
        )
        await callback.answer()
        return
    parts = []
    for org_key, _is_owner in orgs:
        parts.append(_render_org_card(org_key))
    text = "🏛️ <b>Ваши организации</b>\n\n" + "\n\n━━━━━━━━━━━━━━━━\n\n".join(parts)
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_keyboard())
    await callback.answer()

# ==================== СПИСОК АКТИВОВ ====================

@dp.message(lambda m: m.text and m.text.lower() in ["каталог авто", "список авто"])
async def catalog_cars(message: types.Message):
    lines = ["🚗 Каталог автомобилей:\n"]
    for cid, (name, price) in CARS.items():
        lines.append(f"{cid}. {name} — {fmt(price)}")
    text = "\n".join(lines)
    for i in range(0, len(text), 4000):
        await message.answer(text[i:i+4000])

@dp.message(lambda m: m.text and m.text.lower() in ["каталог бизнесов", "список бизнесов"])
async def catalog_biz(message: types.Message):
    lines = ["🏢 Каталог бизнесов:\n"]
    for bid, (name, price, income) in BUSINESSES.items():
        lines.append(f"{bid}. {name} — {fmt(price)} (доход: {fmt(income)}/день)")
    text = "\n".join(lines)
    for i in range(0, len(text), 4000):
        await message.answer(text[i:i+4000])

@dp.message(lambda m: m.text and m.text.lower() in ["каталог недвижимости", "список недвижимости", "каталог квартир"])
async def catalog_apts(message: types.Message):
    lines = ["🏠 Каталог недвижимости:\n"]
    for aid, (name, price) in APARTMENTS.items():
        lines.append(f"{aid}. {name} — {fmt(price)}")
    text = "\n".join(lines)
    for i in range(0, len(text), 4000):
        await message.answer(text[i:i+4000])

# ==================== АДМИН КОМАНДЫ ====================

@dp.message(Command("adminhelp"))
async def admin_help(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer(
        "🔧 Команды администратора:\n\n"
        "━━━━ 📌 Ответом на сообщение ━━━━\n"
        "  выдать [сумма] — добавить деньги\n"
        "  снять [сумма] — снять деньги\n"
        "  выдать работу [название] — назначить работу\n"
        "  выдать авто [номер] — выдать авто\n"
        "  выдать бизнес [номер] — выдать бизнес\n"
        "  выдать недвижимость [номер] — выдать недвижимость\n"
        "  бан — заблокировать игрока\n"
        "  разбан — разблокировать\n"
        "  х2 вкл / х2 выкл — бонус х2\n\n"
        "━━━━ 📌 По @нику (без ответа) ━━━━\n"
        "  выдать авто @ник [номер]\n"
        "  выдать бизнес @ник [номер]\n"
        "  выдать недвижимость @ник [номер]\n"
        "  выдать работу @ник [название]\n"
        "  дать [сумма] @ник\n\n"
        "━━━━ 📌 Слэш-команды ━━━━\n"
        "/addmoney [id] [сумма]\n"
        "/removemoney [id] [сумма]\n"
        "/setbalance [id] [сумма]\n"
        "/ban [id] / /unban [id]\n"
        "/reset [id/@ник] — полное обнуление\n"
        "/setjob [id] [работа]\n"
        "/removejob [id]\n"
        "/addcar [id] [номер]\n"
        "/addspecialcar [id/@ник] [название]\n"
        "/setx2 [id] [1/0]\n"
        "/userinfo [id]\n"
        "/broadcast [текст]\n\n"
        "━━━━ 🏛️ Организации ━━━━\n"
        "ф1/футбол/семья @юз [владелец] [название]\n"
        "имя ф1/футбол/семья [название]\n"
        "убрать ф1/футбол/семья @юз\n"
        "состав ф1/футбол/семья"
    )

def _resolve_user_by_nick(arg: str):
    username = arg.lstrip("@")
    return db.get_user_by_username(username)

@dp.message(lambda m: m.text and m.text.startswith("/addmoney"))
async def admin_addmoney(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        amount = int(parts[2])
    except Exception:
        await message.answer("❌ Формат: /addmoney @ник [сумма]")
        return
    target = _resolve_user_by_nick(parts[1])
    if not target:
        await message.answer("❌ Игрок не найден")
        return
    db.update_balance(target[0], amount)
    await message.answer(f"✅ Добавлено {fmt(amount)} → @{target[1]}")

@dp.message(lambda m: m.text and m.text.startswith("/removemoney"))
async def admin_removemoney(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        amount = int(parts[2])
    except Exception:
        await message.answer("❌ Формат: /removemoney @ник [сумма]")
        return
    target = _resolve_user_by_nick(parts[1])
    if not target:
        await message.answer("❌ Игрок не найден")
        return
    db.update_balance(target[0], -amount)
    await message.answer(f"✅ Снято {fmt(amount)} у @{target[1]}")

@dp.message(lambda m: m.text and m.text.startswith("/setbalance"))
async def admin_setbalance(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        amount = int(parts[2])
    except Exception:
        await message.answer("❌ Формат: /setbalance @ник [сумма]")
        return
    target = _resolve_user_by_nick(parts[1])
    if not target:
        await message.answer("❌ Игрок не найден")
        return
    db.set_balance(target[0], amount)
    await message.answer(f"✅ Баланс @{target[1]} → {fmt(amount)}")

@dp.message(lambda m: m.text and m.text.startswith("/ban") and not m.text.startswith("/bank"))
async def admin_ban(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("❌ Формат: /ban @ник")
        return
    target = _resolve_user_by_nick(parts[1])
    if not target:
        await message.answer("❌ Игрок не найден")
        return
    db.ban_user(target[0])
    await message.answer(f"✅ Игрок @{target[1]} заблокирован")

@dp.message(lambda m: m.text and m.text.startswith("/unban"))
async def admin_unban(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("❌ Формат: /unban @ник")
        return
    target = _resolve_user_by_nick(parts[1])
    if not target:
        await message.answer("❌ Игрок не найден")
        return
    db.unban_user(target[0])
    await message.answer(f"✅ Игрок @{target[1]} разблокирован")

@dp.message(lambda m: m.text and m.text.lower().startswith("/reset"))
async def admin_reset_user(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.strip().split()
    if len(parts) < 2:
        await message.answer("❌ Формат: /reset @ник")
        return
    target = _resolve_user_by_nick(parts[1])
    if not target:
        await message.answer("❌ Игрок не найден")
        return
    target_id = target[0]
    name = f"@{target[1]}" if target[1] else str(target_id)
    db.delete_user(target_id)
    await message.answer(f"♻️ Игрок {name} полностью обнулён. Может регистрироваться заново.")
    try:
        await bot.send_message(
            target_id,
            "♻️ Deutschland RP — Ваш аккаунт был полностью сброшен администратором.\n"
            "Напишите /start для повторной регистрации."
        )
    except Exception:
        pass

@dp.message(lambda m: m.text and m.text.lower().startswith("/setjob"))
async def admin_setjob(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split(maxsplit=2)
        job = parts[2]
    except Exception:
        await message.answer("❌ Формат: /setjob @ник [работа]")
        return
    target = _resolve_user_by_nick(parts[1])
    if not target:
        await message.answer("❌ Игрок не найден")
        return
    if job not in ALL_JOBS:
        await message.answer(f"❌ Работа не найдена.")
        return
    db.set_job(target[0], job)
    await message.answer(f"✅ Работа @{target[1]}: {job}")

@dp.message(lambda m: m.text and m.text.startswith("/removejob"))
async def admin_removejob(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("❌ Формат: /removejob @ник")
        return
    target = _resolve_user_by_nick(parts[1])
    if not target:
        await message.answer("❌ Игрок не найден")
        return
    db.set_job(target[0], "")
    await message.answer(f"✅ Работа @{target[1]} удалена")

@dp.message(lambda m: m.text and m.text.startswith("/addcar"))
async def admin_addcar(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        car_id = int(parts[2])
    except Exception:
        await message.answer("❌ Формат: /addcar @ник [номер авто]")
        return
    target = _resolve_user_by_nick(parts[1])
    if not target:
        await message.answer("❌ Игрок не найден")
        return
    if car_id not in CARS:
        await message.answer(f"❌ Авто #{car_id} не найдено")
        return
    car_name, _ = CARS[car_id]
    db.add_car(target[0], car_id, car_name)
    await message.answer(f"✅ Авто {car_name} → @{target[1]}")

@dp.message(lambda m: m.text and m.text.startswith("/addspecialcar"))
async def admin_add_special_car(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.strip().split(maxsplit=2)
    if len(parts) < 3:
        await message.answer("❌ Формат: /addspecialcar [id или @ник] [название авто]")
        return
    target_str = parts[1].lstrip("@")
    car_name = parts[2]
    if target_str.isdigit():
        target = db.get_user(int(target_str))
    else:
        target = db.get_user_by_username(target_str)
    if not target:
        return
    db.add_car(target[0], 0, car_name)
    await message.answer(f"✅ Спец авто [{car_name}] выдано игроку @{target[1]}")
    try:
        await bot.send_message(target[0], f"🚗 Вам выдали специальный автомобиль: {car_name}")
    except Exception:
        pass

@dp.message(lambda m: m.text and m.text.startswith("/setx2"))
async def admin_setx2(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        value = int(parts[2])
        assert value in (0, 1)
    except Exception:
        await message.answer("❌ Формат: /setx2 @ник [1 или 0]")
        return
    target = _resolve_user_by_nick(parts[1])
    if not target:
        await message.answer("❌ Игрок не найден")
        return
    db.set_x2(target[0], bool(value))
    status = "включён 🔥" if value else "выключен"
    await message.answer(f"✅ Х2 бонус для @{target[1]}: {status}")

@dp.message(lambda m: m.text and m.text.startswith("/userinfo"))
async def admin_userinfo(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("❌ Формат: /userinfo @ник")
        return
    target = _resolve_user_by_nick(parts[1])
    if not target:
        await message.answer("❌ Игрок не найден")
        return
    uid, username, spm_id, game_name, balance, bank, btc, job, last_salary, banned, *_ = target
    x2 = db.has_x2(uid)
    text = (
        f"👤 Информация об игроке\n\n"
        f"🆔 ID: {uid}\n"
        f"📱 Username: @{username}\n"
        f"🎮 Имя в игре: {game_name}\n"
        f"🆔 CPM айди: {spm_id}\n"
        f"💰 Баланс: {fmt(balance)}\n"
        f"🏦 Банк: {fmt(bank)}\n"
        f"₿ BTC: {btc:.4f}\n"
        f"💼 Работа: {job if job else 'Безработный'}\n"
        f"🔥 Х2 бонус: {'Да' if x2 else 'Нет'}\n"
        f"⛔ Бан: {'Да' if banned else 'Нет'}"
    )
    await message.answer(text)

@dp.message(lambda m: m.text and m.text.startswith("/broadcast"))
async def admin_broadcast(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    try:
        text = message.text.split(maxsplit=1)[1]
    except Exception:
        await message.answer("❌ Формат: /broadcast [текст]")
        return
    users = db.get_all_users()
    sent = 0
    for uid in users:
        try:
            await bot.send_message(uid, f"📢 Объявление:\n\n{text}")
            sent += 1
        except Exception:
            pass
    await message.answer(f"✅ Отправлено {sent}/{len(users)} игрокам")

# ==================== АДМИН: ПО @ЮЗЕРНЕЙМУ ====================

@dp.message(lambda m: (
    m.text and m.from_user and m.from_user.id in config.ADMIN_IDS and
    m.reply_to_message is None and
    m.text.lower().startswith("выдать авто ")
))
async def admin_give_car_username(message: types.Message):
    parts = message.text.strip().split()
    try:
        username = next(p for p in parts if p.startswith("@"))[1:]
        car_id = int(parts[-1])
    except Exception:
        await message.answer("❌ Формат: выдать авто @ник [номер авто 1–140]")
        return
    target = db.get_user_by_username(username)
    if not target:
        return
    if car_id not in CARS:
        await message.answer(f"❌ Авто #{car_id} не найдено.")
        return
    car_name, _ = CARS[car_id]
    db.add_car(target[0], car_id, car_name)
    await message.answer(f"✅ @{username} получил авто: {car_name}")
    try:
        await bot.send_message(target[0], f"🚗 Вам выдали автомобиль: {car_name}")
    except Exception:
        pass

@dp.message(lambda m: (
    m.text and m.from_user and m.from_user.id in config.ADMIN_IDS and
    m.reply_to_message is None and
    m.text.lower().startswith("выдать бизнес ")
))
async def admin_give_biz_username(message: types.Message):
    parts = message.text.strip().split()
    try:
        username = next(p for p in parts if p.startswith("@"))[1:]
        biz_id = int(parts[-1])
    except Exception:
        await message.answer("❌ Формат: выдать бизнес @ник [номер бизнеса 1–48]")
        return
    target = db.get_user_by_username(username)
    if not target:
        return
    if biz_id not in BUSINESSES:
        await message.answer(f"❌ Бизнес #{biz_id} не найден.")
        return
    biz_name, _, biz_income = BUSINESSES[biz_id]
    db.add_business(target[0], biz_id, biz_name, biz_income)
    await message.answer(f"✅ @{username} получил бизнес: {biz_name}")
    try:
        await bot.send_message(target[0], f"🏢 Вам выдали бизнес: {biz_name}\n💰 Доход: {fmt(biz_income)}/день")
    except Exception:
        pass

@dp.message(lambda m: (
    m.text and m.from_user and m.from_user.id in config.ADMIN_IDS and
    m.reply_to_message is None and
    (m.text.lower().startswith("выдать недвижимость ") or
     m.text.lower().startswith("выдать квартиру "))
))
async def admin_give_apt_username(message: types.Message):
    parts = message.text.strip().split()
    try:
        username = next(p for p in parts if p.startswith("@"))[1:]
        apt_id = int(parts[-1])
    except Exception:
        await message.answer("❌ Формат: выдать недвижимость @ник [номер 1–19]")
        return
    target = db.get_user_by_username(username)
    if not target:
        return
    if apt_id not in APARTMENTS:
        await message.answer(f"❌ Объект #{apt_id} не найден.")
        return
    apt_name, _ = APARTMENTS[apt_id]
    db.add_apartment(target[0], apt_id, apt_name)
    await message.answer(f"✅ @{username} получил недвижимость: {apt_name}")
    try:
        await bot.send_message(target[0], f"🏠 Вам выдали недвижимость: {apt_name}")
    except Exception:
        pass

@dp.message(lambda m: (
    m.text and m.from_user and m.from_user.id in config.ADMIN_IDS and
    m.reply_to_message is None and
    m.text.lower().startswith("выдать работу ") and
    "@" in m.text
))
async def admin_give_job_username(message: types.Message):
    parts = message.text.strip().split()
    try:
        at_idx = next(i for i, p in enumerate(parts) if p.startswith("@"))
        username = parts[at_idx][1:]
        job_name = " ".join(parts[at_idx + 1:])
    except Exception:
        await message.answer("❌ Формат: выдать работу @ник [название работы]")
        return
    if not job_name:
        await message.answer("❌ Укажи название работы.")
        return
    target = db.get_user_by_username(username)
    if not target:
        return
    matched = None
    for j in ALL_JOBS.keys():
        if j.lower() == job_name.lower():
            matched = j
            break
    if not matched:
        await message.answer(f"❌ Работа не найдена: {job_name}")
        return
    salary = ALL_JOBS[matched]
    db.set_job(target[0], matched)
    await message.answer(f"✅ @{username} назначена работа: {matched} ({fmt(salary)}/зп)")
    try:
        await bot.send_message(target[0], f"💼 Вам назначена работа: {matched}\n💵 Зарплата: {fmt(salary)}")
    except Exception:
        pass

@dp.message(lambda m: m.text and m.text.lower().startswith("дать ") and m.from_user and m.from_user.id in config.ADMIN_IDS and m.reply_to_message is None)
async def admin_dat_cmd(message: types.Message):
    parts = message.text.strip().split()
    try:
        amount = int(parts[1])
        username = parts[2].lstrip("@")
    except Exception:
        await message.answer("❌ Формат: дать [сумма] @никнейм")
        return
    target = db.get_user_by_username(username)
    if not target:
        return
    db.update_balance(target[0], amount)
    await message.answer(f"✅ Выдано {fmt(amount)} → @{username}")

# ==================== АДМИН ОТВЕТОМ ====================

@dp.message(lambda m: (
    m.reply_to_message is not None and
    m.text is not None and
    m.from_user is not None and
    m.from_user.id in config.ADMIN_IDS
))
async def admin_reply_cmd(message: types.Message):
    target_user = message.reply_to_message.from_user
    target_id = target_user.id
    text = message.text.lower().strip()
    parts = message.text.strip().split()

    if not db.get_user(target_id):
        return

    if text.startswith("выдать работу") or text.startswith("дать работу"):
        if len(parts) < 3:
            await message.answer("❌ Формат: выдать работу [название]")
            return
        job_name = " ".join(parts[2:])
        matched = None
        for j in ALL_JOBS.keys():
            if j.lower() == job_name.lower():
                matched = j
                break
        if not matched:
            await message.answer(f"❌ Работа не найдена: {job_name}")
            return
        salary = ALL_JOBS[matched]
        db.set_job(target_id, matched)
        await message.answer(f"✅ Назначена работа [{matched}] → @{target_user.username or target_id}")
        try:
            await bot.send_message(target_id, f"💼 Вам назначена работа: {matched}\n💵 Зарплата: {fmt(salary)}")
        except Exception:
            pass

    elif text.startswith("выдать авто"):
        try:
            car_id = int(parts[-1])
        except Exception:
            await message.answer("❌ Формат: выдать авто [номер 1–140]")
            return
        if car_id not in CARS:
            await message.answer(f"❌ Авто #{car_id} не найдено.")
            return
        car_name, _ = CARS[car_id]
        db.add_car(target_id, car_id, car_name)
        await message.answer(f"✅ @{target_user.username or target_id} получил авто: {car_name}")
        try:
            await bot.send_message(target_id, f"🚗 Вам выдали автомобиль: {car_name}")
        except Exception:
            pass

    elif text.startswith("выдать бизнес"):
        try:
            biz_id = int(parts[-1])
        except Exception:
            await message.answer("❌ Формат: выдать бизнес [номер 1–48]")
            return
        if biz_id not in BUSINESSES:
            await message.answer(f"❌ Бизнес #{biz_id} не найден.")
            return
        biz_name, _, biz_income = BUSINESSES[biz_id]
        db.add_business(target_id, biz_id, biz_name, biz_income)
        await message.answer(f"✅ @{target_user.username or target_id} получил бизнес: {biz_name}")
        try:
            await bot.send_message(target_id, f"🏢 Вам выдали бизнес: {biz_name}\n💰 Доход: {fmt(biz_income)}/день")
        except Exception:
            pass

    elif text.startswith("выдать недвижимость") or text.startswith("выдать квартиру"):
        try:
            apt_id = int(parts[-1])
        except Exception:
            await message.answer("❌ Формат: выдать недвижимость [номер 1–19]")
            return
        if apt_id not in APARTMENTS:
            await message.answer(f"❌ Объект #{apt_id} не найден.")
            return
        apt_name, _ = APARTMENTS[apt_id]
        db.add_apartment(target_id, apt_id, apt_name)
        await message.answer(f"✅ @{target_user.username or target_id} получил недвижимость: {apt_name}")
        try:
            await bot.send_message(target_id, f"🏠 Вам выдали недвижимость: {apt_name}")
        except Exception:
            pass

    elif text.startswith("х2 вкл"):
        db.set_x2(target_id, True)
        await message.answer(f"✅ Х2 бонус ВКЛЮЧЁН для @{target_user.username or target_id} 🔥")

    elif text.startswith("х2 выкл"):
        db.set_x2(target_id, False)
        await message.answer(f"✅ Х2 бонус ВЫКЛЮЧЕН для @{target_user.username or target_id}")

    elif text.startswith("выдать") or text.startswith("дать"):
        try:
            amount = int(parts[1])
        except Exception:
            await message.answer("❌ Формат: выдать [сумма]")
            return
        db.update_balance(target_id, amount)
        await message.answer(f"✅ Выдано {fmt(amount)} → @{target_user.username or target_id}")

    elif text.startswith("снять"):
        try:
            amount = int(parts[1])
        except Exception:
            await message.answer("❌ Формат: снять [сумма]")
            return
        db.update_balance(target_id, -amount)
        await message.answer(f"✅ Снято {fmt(amount)} у @{target_user.username or target_id}")

    elif text.startswith("бан"):
        db.ban_user(target_id)
        await message.answer(f"✅ Игрок @{target_user.username or target_id} заблокирован")

    elif text.startswith("разбан"):
        db.unban_user(target_id)
        await message.answer(f"✅ Игрок @{target_user.username or target_id} разблокирован")

# ==================== ПОМОЩЬ ====================

@dp.message(lambda m: m.text and m.text.lower() in ["помощь", "команды", "/help"])
async def help_cmd(message: types.Message):
    await message.answer(
        "📋 Deutschland RP — Команды:\n\n"
        "━━━━ 👤 Профиль ━━━━\n"
        "инфо — профиль\n"
        "б / баланс — текущий баланс\n\n"
        "━━━━ 💼 Работа и зарплата ━━━━\n"
        "зп — получить зарплату\n"
        "зп @ник — зарплата игроку\n"
        "зп бизнес @ник — зарплата + доход от бизнесов\n"
        "бизнес @ник — только доход от бизнесов\n\n"
        "━━━━ 💰 Продажа имущества ━━━━\n"
        "продать авто [токен] — продать государству (50%)\n"
        "продать авто [токен] @ник [цена] — продать игроку\n"
        "продать бизнес/недвижимость [токен]\n\n"
        "━━━━ 💸 Переводы ━━━━\n"
        "дать [сумма] @ник\n"
        "+[сумма] @ник\n\n"
        "━━━━ 🏆 Рейтинги ━━━━\n"
        "топ / топ баланс\n"
        "топ имущество\n\n"
        "━━━━ 🏦 Банк и BTC ━━━━\n"
        "банк\n"
        "внести / вывести [сумма]\n"
        "кредит / погасить [сумма]\n"
        "биткоин\n"
        "купить бтс / продать бтс [кол-во]\n\n"
        "━━━━ 🎰 Казино ━━━━\n"
        "казино\n\n"
        "━━━━ 🛒 Покупки ━━━━\n"
        "купить авто [1–140]\n"
        "купить бизнес [1–48]\n"
        "купить недвижимость [1–19]\n\n"
        "━━━━ 📋 Каталоги ━━━━\n"
        "каталог авто / каталог бизнесов / каталог недвижимости\n\n"
        "мои авто / мои бизнесы / мои объекты"
    )

# ==================== ЗАПУСК ====================

async def main():
    print("✅ Бот Deutschland RP запущен!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
