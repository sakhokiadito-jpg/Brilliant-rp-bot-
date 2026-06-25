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

# ==================== ДАННЫЕ ====================

CARS = {
    1:   ("VAZ 2107", 100_000),
    2:   ("Honda Civic", 150_000),
    3:   ("Lada Priora", 300_000),
    4:   ("VAZ 2114", 200_000),
    5:   ("Volkswagen Scirocco", 900_000),
    6:   ("Chrysler 300C", 1_300_000),
    7:   ("BMW M135i", 1_700_000),
    8:   ("Mercedes-Benz E190", 550_000),
    9:   ("BMW E36", 1_100_000),
    10:  ("Dacia Logan", 400_000),
    11:  ("Mitsubishi Lancer Evo XIII", 1_700_000),
    12:  ("Lada Niva", 370_000),
    13:  ("Honda Civic", 2_500_000),
    14:  ("Ford Mustang Boss 302", 6_500_000),
    15:  ("Toyota Supra", 3_300_000),
    16:  ("Mercedes-Benz S600 W140", 1_700_000),
    17:  ("BMW E46", 2_100_000),
    18:  ("Ford Focus RS", 2_300_000),
    19:  ("Honda Civic Type R", 1_800_000),
    20:  ("Cadillac Escalade GMT900", 1_500_000),
    21:  ("Cadillac Escalade-V", 12_000_000),
    22:  ("Ford F-150 SVT Raptor", 2_400_000),
    23:  ("BMW E34", 800_000),
    24:  ("Cadillac CTS", 1_800_000),
    25:  ("Volkswagen Passat B8", 1_500_000),
    26:  ("Toyota Alteza", 1_300_000),
    27:  ("Lexus IS300", 1_300_000),
    28:  ("Lexus IS-F", 3_500_000),
    29:  ("BMW E39", 1_000_000),
    30:  ("Nissan 350Z", 1_850_000),
    31:  ("Toyota Crown Athlete", 2_800_000),
    32:  ("Nissan Skyline R33", 3_500_000),
    33:  ("Nissan Skyline R32", 3_200_000),
    34:  ("Nissan Skyline R34", 3_800_000),
    35:  ("Nissan Silvia S15", 2_500_000),
    36:  ("Nissan Silvia S13", 2_200_000),
    37:  ("Mitsubishi Lancer Evo X", 2_800_000),
    38:  ("Subaru Impreza STI", 1_700_000),
    39:  ("Kia Stinger GT", 2_200_000),
    40:  ("BMW M5 E60", 3_500_000),
    41:  ("Mercedes-Benz G65", 4_700_000),
    42:  ("Dodge Charger SRT", 5_000_000),
    43:  ("Mercedes-Benz C63 AMG", 3_400_000),
    44:  ("Volkswagen Golf GTI", 400_000),
    45:  ("Volkswagen Golf R", 2_200_000),
    46:  ("BMW X5 E70", 1_800_000),
    47:  ("Dodge Durango", 3_300_000),
    48:  ("Chevrolet Tahoe 2018", 3_500_000),
    49:  ("Chevrolet Camaro SS", 3_750_000),
    50:  ("Audi RS5", 3_800_000),
    51:  ("Alfa Romeo Giulia", 1_600_000),
    52:  ("BMW M5 F10", 4_500_000),
    53:  ("Range Rover SVR", 7_000_000),
    54:  ("Mercedes-Benz CL65", 2_800_000),
    55:  ("BMW M4 F82", 3_800_000),
    56:  ("Mercedes-Benz S680", 37_800_000),
    57:  ("Ford Mustang S650", 4_000_000),
    58:  ("Ford Mustang S550", 2_500_000),
    59:  ("Toyota Land Cruiser 200", 4_000_000),
    60:  ("Mercedes-Benz GLE63", 8_500_000),
    61:  ("Ferrari 458 Italia", 18_000_000),
    62:  ("BMW M6 F13", 4_700_000),
    63:  ("Toyota Yaris GR", 2_500_000),
    64:  ("Porsche 911", 9_000_000),
    65:  ("Porsche Spyder 918", 175_000_000),
    66:  ("Porsche Carrera GT", 140_000_000),
    67:  ("BMW X6m", 5_000_000),
    68:  ("Audi RS6", 14_000_000),
    69:  ("Skoda Octavia A9", 3_200_000),
    70:  ("Audi RS7", 15_500_000),
    71:  ("BMW M3 Touring G81", 12_000_000),
    72:  ("BMW M4 G82", 7_500_000),
    73:  ("BMW X7", 8_500_000),
    74:  ("BMW 760i xDrive", 13_000_000),
    75:  ("BMW M5 G90", 18_000_000),
    76:  ("BMW M5 F90 pre-facelift", 7_500_000),
    77:  ("BMW M5 F90 facelift", 9_000_000),
    78:  ("Dodge Challenger", 6_500_000),
    79:  ("Land Rover Defender", 7_000_000),
    80:  ("Toyota Land Cruiser 80", 1_500_000),
    81:  ("Ford Raptor F150", 4_350_000),
    82:  ("BMW M2 F87", 5_000_000),
    83:  ("Mercedes-Benz S63 AMG", 2_400_000),
    84:  ("Audi R8 V8 (Type 42)", 6_000_000),
    85:  ("Audi R8 (Type 4S)", 13_000_000),
    86:  ("Chevrolet Corvette C6", 3_500_000),
    87:  ("Chevrolet Corvette C7", 5_000_000),
    88:  ("Chevrolet Corvette C8", 10_000_000),
    89:  ("Nissan GT-R R35", 9_000_000),
    90:  ("Porsche 911 GT3 RS", 40_000_000),
    91:  ("Ferrari Berlinetta", 28_000_000),
    92:  ("Rolls-Royce Cullinan", 38_000_000),
    93:  ("Lamborghini Urus", 25_000_000),
    94:  ("Lamborghini Aventador", 30_500_000),
    95:  ("Lamborghini Huracan", 27_000_000),
    96:  ("McLaren P1", 20_000_000),
    97:  ("McLaren 720S", 30_000_000),
    98:  ("Bentley Continental GT", 15_000_000),
    99:  ("Mercedes-Benz GT63s AMG", 8_500_000),
    100: ("Lamborghini Aventador SVJ", 75_000_000),
    101: ("Koenigsegg Agera", 200_000_000),
    102: ("Range Rover Autobiography 2025", 22_000_000),
    103: ("Mercedes-Benz CLS63s AMG", 5_500_000),
    104: ("Mercedes-Benz G63 AMG", 18_000_000),
    105: ("Toyota Camry XV70", 2_500_000),
    106: ("Dodge RAM TRX", 9_500_000),
    107: ("BMW M2 G87", 9_000_000),
    108: ("BMW M8 F92", 8_500_000),
    109: ("Toyota Celica GT-Four", 1_000_000),
    110: ("Toyota Camry XV80", 3_750_000),
    111: ("Mercedes-Benz E500 W124", 3_300_000),
}

# ==================== РАБОТЫ ====================

JOBS = {
    "Заправщик": 60_000,
    "Механик": 70_000,
    "Инкассатор": 90_000,
    "Курьер": 60_000,
    "Кассир": 70_000,
    "Таксист": 60_000,
    "Режиссёр (телевидение)": 80_000,
}

GOV_JOBS = {
    "Охранник (Правительство)": 40_000,
    "Секретарь (Правительство)": 50_000,
    "Юрист (Правительство)": 60_000,
    "Адвокат (Правительство)": 120_000,
    "Прокурор (Правительство)": 150_000,
    "Глава аппарата": 190_000,
    "Вице-губернатор": 250_000,
    "Губернатор": 350_000,
    "Министр": 400_000,
    "Премьер-Министр": 500_000,
    "Младший сержант (ФСБ)": 80_000,
    "Сержант (ФСБ)": 120_000,
    "Младший лейтенант (ФСБ)": 170_000,
    "Капитан (ФСБ)": 200_000,
    "Майор (ФСБ)": 220_000,
    "Подполковник (ФСБ)": 250_000,
    "Генерал-майор (ФСБ)": 300_000,
    "Генерал-лейтенант (ФСБ)": 330_000,
    "Сержант (МВД)": 60_000,
    "Лейтенант (МВД)": 80_000,
    "Капитан (МВД)": 120_000,
    "Майор (МВД)": 150_000,
    "Подполковник (МВД)": 180_000,
    "Полковник (МВД)": 220_000,
    "Генерал-майор (МВД)": 270_000,
    "Генерал-лейтенант (МВД)": 320_000,
    "Медик (Мин.Здрав)": 80_000,
    "Врач (Мин.Здрав)": 120_000,
    "Заместитель глав.врача": 160_000,
    "Глав-врач": 240_000,
    "Сержант (ВсРФ)": 70_000,
    "Лейтенант (ВсРФ)": 110_000,
    "Капитан (ВсРФ)": 140_000,
    "Майор (ВсРФ)": 180_000,
    "Подполковник (ВсРФ)": 220_000,
    "Полковник (ВсРФ)": 260_000,
    "Генерал-майор (ВсРФ)": 280_000,
    "Генерал-лейтенант (ВсРФ)": 340_000,
    "Дорожный патруль (ЦОДД)": 50_000,
    "Мобильный ситуационный центр (ЦОДД)": 80_000,
    "Дорожные координаторы (ЦОДД)": 140_000,
    "Служба эксплуатации (ЦОДД)": 150_000,
    "Ситуационный центр (ЦОДД)": 300_000,
    "Мл. лейтенант юстиции (СК)": 130_000,
    "Лейтенант юстиции (СК)": 150_000,
    "Ст. лейтенант юстиции (СК)": 170_000,
    "Капитан юстиции (СК)": 180_000,
    "Майор юстиции (СК)": 200_000,
    "Подполковник юстиции (СК)": 240_000,
    "Полковник юстиции (СК)": 270_000,
    "Генерал-майор юстиции (СК)": 300_000,
    "Генерал-лейтенант юстиции (СК)": 350_000,
}

ALL_JOBS = {**JOBS, **GOV_JOBS}

# BUSINESSES: { biz_type: (display_name, {slot: (price, income)}) }
# Уникальный DB-id = biz_type * 100 + slot_num
BUSINESSES: dict = {
    1:  ("Бинокль",                              {i: (400_000, 5_700)    for i in range(1, 7)}),
    2:  ("Мини заведения",                       {i: (600_000, 10_500)   for i in range(1, 11)}),
    3:  ("Рекламные баннеры",                    {i: (750_000, 10_800)   for i in range(1, 21)}),
    4:  ("Заведения на колёсах",                 {1: (1_200_000, 17_000), 2: (1_200_000, 17_000),
                                                  3: (1_000_000, 14_000), 4: (1_000_000, 14_000)}),
    5:  ("Шиномонтаж на колёсах",               {i: (1_400_000, 20_000) for i in range(1, 5)}),
    6:  ("Автомойка",                            {1: (9_000_000, 128_000), 2: (9_000_000, 128_000)}),
    7:  ("СТО",                                  {1: (10_000_000, 142_000)}),
    8:  ("Колесо обозрения",                     {1: (9_500_000,  135_000)}),
    9:  ("АЗС",                                  {i: (13_000_000, 185_000) for i in range(1, 10)}),
    10: ("Старбакс #1",                          {1: (2_300_000,  47_000)}),
    11: ("Старбакс #2",                          {1: (3_100_000,  44_000)}),
    12: ("Магазин",                              {1: (1_500_000,  31_000)}),
    13: ("Отель «Летняя радость»",               {1: (81_000_000, 1_160_000)}),
    14: ("Спортивный комплекс «Победа»",         {1: (78_000_000, 2_000_000)}),
    15: ("Супермаркет «Яблоко»",                 {1: (23_000_000, 330_000)}),
    16: ("Маяк",                                 {1: (31_000_000, 450_000)}),
    17: ("Авторынок",                            {1: (68_000_000, 980_000)}),
    18: ("Гоночная компания «Winner»",           {1: (120_000_000, 1_720_000)}),
    19: ("Шаурмечная «Лучшая шаурма страны!»",  {1: (2_200_000,  31_500)}),
    20: ("Театр «Медвежий город»",               {1: (3_100_000,  44_200)}),
    21: ("Платная парковка #1",                  {1: (2_200_000,  31_500)}),
    22: ("Платная парковка #2",                  {1: (2_400_000,  34_000)}),
    23: ("Торговый центр «Бесконечность»",       {1: (3_300_000,  47_200)}),
    24: ("Автосалон «Счастливая поездка»",       {1: (12_000_000, 171_500)}),
    25: ("Рынок «Посиделки»",                    {1: (11_000_000, 157_000)}),
    26: ("Отель «Прелестная погода»",            {1: (24_000_000, 343_000)}),
    27: ("Кинотеатр «Евро-серия»",               {1: (34_000_000, 486_000)}),
}

def _biz_db_id(biz_type: int, slot: int) -> int:
    """Уникальный ID для базы данных: тип*100 + слот"""
    return biz_type * 100 + slot

def _biz_slot_data(biz_type: int, slot: int):
    """Возвращает (display_name, price, income) или None"""
    if biz_type not in BUSINESSES:
        return None
    name, slots = BUSINESSES[biz_type]
    if slot not in slots:
        return None
    price, income = slots[slot]
    display = f"{name} #{slot}" if len(slots) > 1 else name
    return display, price, income

APARTMENTS: dict = {
    # ЖК «Sunset Blocks»
    1:  ("Квартира №1 — ЖК «Sunset Blocks»",             1_200_000),
    2:  ("Квартира №2 — ЖК «Sunset Blocks»",             1_200_000),
    3:  ("Квартира №3 — ЖК «Sunset Blocks»",             1_200_000),
    4:  ("Квартира №4 — ЖК «Sunset Blocks»",             1_300_000),
    5:  ("Квартира №5 — ЖК «Sunset Blocks»",             1_400_000),
    # ЖК «Pacific Terrace»
    6:  ("Квартира №6 — ЖК «Pacific Terrace»",           2_000_000),
    7:  ("Квартира №7 — ЖК «Pacific Terrace»",           2_000_000),
    8:  ("Квартира №8 — ЖК «Pacific Terrace»",           2_200_000),
    9:  ("Квартира №9 — ЖК «Pacific Terrace»",           2_300_000),
    10: ("Квартира №10 — ЖК «Pacific Terrace»",          2_500_000),
    # ЖК «Ocean Crown Residences»
    11: ("Квартира №11 — ЖК «Ocean Crown Residences»",   4_000_000),
    12: ("Квартира №12 — ЖК «Ocean Crown Residences»",   4_200_000),
    13: ("Квартира №13 — ЖК «Ocean Crown Residences»",   4_500_000),
    14: ("Квартира №14 — ЖК «Ocean Crown Residences»",   5_000_000),
    15: ("Квартира №15 — ЖК «Ocean Crown Residences»",   5_800_000),
    # Дома
    16: ("Дом #1",   5_000_000),
    17: ("Дом #2",   7_000_000),
    18: ("Дом #3",   6_000_000),
    19: ("Дом #4",   5_200_000),
    20: ("Дом #5",   7_500_000),
    21: ("Дом #6",  15_000_000),
    22: ("Дом #7",   6_800_000),
    23: ("Дом #8",   7_000_000),
    24: ("Дом #9",   7_100_000),
    25: ("Дом #10",  8_000_000),
    26: ("Дом #11", 185_000_000),
    27: ("Дом #12",  45_000_000),
    28: ("Дом #13",  60_000_000),
    29: ("Дом #14",  57_000_000),
    30: ("Дом #15",  48_500_000),
    31: ("Дом #16",  53_000_000),
    32: ("Дом #17",   7_500_000),
    33: ("Дом #18",   8_000_000),
    34: ("Дом #19",   7_900_000),
    35: ("Дом #20",   8_500_000),
    36: ("Дом #21",   8_000_000),
    37: ("Дом #22",   5_500_000),
    38: ("Дом #23",   4_000_000),
    39: ("Дом #24",   5_000_000),
}

# ==================== PENDING DICTS ====================

PENDING_REGISTRATIONS: dict = {}
PENDING_SALES: dict = {}

# ==================== FSM ====================

class Registration(StatesGroup):
    rp_name = State()
    cpm_id = State()
    appearance = State()
    source = State()

class AddCarFSM(StatesGroup):
    name = State()
    price = State()
    description = State()
    specs = State()
    confirm = State()

class AddBizFSM(StatesGroup):
    name = State()
    price = State()
    income = State()
    description = State()
    confirm = State()

class AddAptFSM(StatesGroup):
    name = State()
    price = State()
    description = State()
    confirm = State()

class AddPromoFSM(StatesGroup):
    code = State()
    amount = State()
    max_uses = State()
    confirm = State()

class DisablePromoFSM(StatesGroup):
    code = State()

# ==================== ХЕЛПЕРЫ ====================

def fmt(n):
    return f"{int(n):,}".replace(",", ".") + "₽"

def is_admin(uid):
    return uid in config.ADMIN_IDS or db.is_db_admin(uid)

def is_founder(uid):
    return uid in config.ADMIN_IDS

GARAGE_SLOT_PRICES = {
    3: 1_100,
    4: 1_650,
    5: 2_200,
    6: 2_750,
    7: 3_300,
    8: 4_400,
}

def info_keyboard(uid: int):
    u = str(uid)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚗 Гараж", callback_data=f"list_cars|{u}")],
        [InlineKeyboardButton(text="💼 Работа", callback_data=f"list_jobs|{u}")],
        [InlineKeyboardButton(text="🏢 Бизнесы", callback_data=f"list_biz|{u}")],
        [InlineKeyboardButton(text="🏠 Недвижимость", callback_data=f"list_apts|{u}")],
        [InlineKeyboardButton(text="🏦 Банк", callback_data=f"bank_menu|{u}")],
    ])

def back_keyboard(uid: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_to_info|{uid}")]
    ])

def _parse_menu_owner(data: str):
    if "|" in data:
        try:
            return int(data.split("|", 1)[1])
        except Exception:
            return None
    return None

async def _assert_owner(callback: types.CallbackQuery):
    owner_uid = _parse_menu_owner(callback.data)
    if owner_uid is not None and callback.from_user.id != owner_uid:
        await callback.answer("⛔ Это меню принадлежит другому игроку.", show_alert=True)
        return None
    return owner_uid if owner_uid is not None else callback.from_user.id

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
        "👋 Добро пожаловать в Brilliant RP!\n\n"
        "Давай начнём регистрацию.\n\n"
        "1️⃣ Введи своё RP имя и фамилию:\n"
        "Пример: Владимир Харитонов"
    )
    await state.set_state(Registration.rp_name)

@dp.message(Registration.rp_name)
async def reg_rp_name(message: types.Message, state: FSMContext):
    await state.update_data(rp_name=message.text.strip())
    await message.answer(
        "2️⃣ Введи свой CPM ID:\n"
        "Пример: ОО093723"
    )
    await state.set_state(Registration.cpm_id)

@dp.message(Registration.cpm_id)
async def reg_cpm_id(message: types.Message, state: FSMContext):
    await state.update_data(cpm_id=message.text.strip())
    await message.answer(
        "3️⃣ Опиши свою внешность:\n\n"
        "Пример:\n"
        "Рост: 185 см\n"
        "Телосложение: спортивное\n"
        "Особые приметы: шрам на щеке"
    )
    await state.set_state(Registration.appearance)

@dp.message(Registration.appearance)
async def reg_appearance(message: types.Message, state: FSMContext):
    await state.update_data(appearance=message.text.strip())
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="TikTok", callback_data="reg_source_tiktok"),
            InlineKeyboardButton(text="Telegram", callback_data="reg_source_telegram"),
        ],
        [
            InlineKeyboardButton(text="Рекомендация друга", callback_data="reg_source_friend"),
            InlineKeyboardButton(text="Другое", callback_data="reg_source_other"),
        ],
    ])
    await message.answer("4️⃣ Откуда ты узнал о нас?", reply_markup=kb)
    await state.set_state(Registration.source)

@dp.callback_query(Registration.source, F.data.startswith("reg_source_"))
async def reg_source(callback: types.CallbackQuery, state: FSMContext):
    source_map = {
        "reg_source_tiktok":   "TikTok",
        "reg_source_telegram": "Telegram",
        "reg_source_friend":   "Рекомендация друга",
        "reg_source_other":    "Другое",
    }
    source = source_map.get(callback.data, "Другое")
    data = await state.get_data()
    await state.clear()
    await callback.message.edit_reply_markup(reply_markup=None)

    rp_name    = data["rp_name"]
    cpm_id     = data["cpm_id"]
    appearance = data["appearance"]
    uid        = callback.from_user.id
    username   = callback.from_user.username or callback.from_user.first_name

    if not config.REGISTRATION_CHAT_ID:
        db.register_user(uid, username, cpm_id, rp_name, appearance, source)
        await callback.message.answer(
            f"✅ Регистрация завершена!\n\n"
            f"👤 RP имя: {rp_name}\n"
            f"🆔 CPM ID: {cpm_id}\n"
            f"🌐 Источник: {source}\n"
            f"💰 Стартовый баланс: {fmt(config.START_BALANCE)}\n\n"
            f"Напишите инфо для просмотра профиля."
        )
        await callback.answer()
        return

    PENDING_REGISTRATIONS[uid] = {
        "rp_name": rp_name,
        "cpm_id": cpm_id,
        "appearance": appearance,
        "source": source,
        "username": username,
    }

    text = (
        f"📋 Brilliant RP — Новая анкета\n\n"
        f"👤 TG: @{username} (ID: {uid})\n"
        f"🎮 RP имя: {rp_name}\n"
        f"🆔 CPM ID: {cpm_id}\n"
        f"🪞 Внешность:\n{appearance}\n"
        f"🌐 Источник: {source}"
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
        db.register_user(uid, username, cpm_id, rp_name, appearance, source)
        await callback.message.answer(
            f"✅ Регистрация завершена!\n\n"
            f"👤 RP имя: {rp_name}\n"
            f"🆔 CPM ID: {cpm_id}\n"
            f"💰 Стартовый баланс: {fmt(config.START_BALANCE)}\n\n"
            f"Напишите инфо для просмотра профиля."
        )
        await callback.answer()
        return

    await callback.message.answer(
        f"📋 Анкета отправлена на рассмотрение!\n\n"
        f"🎮 RP имя: {rp_name}\n"
        f"🆔 CPM ID: {cpm_id}\n\n"
        f"⏳ Ожидайте одобрения от администратора.\n"
        f"Вам придёт уведомление."
    )
    await callback.answer()

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
    db.register_user(
        uid, pending["username"], pending["cpm_id"], pending["rp_name"],
        pending["appearance"], pending["source"]
    )
    try:
        await bot.send_message(
            uid,
            f"✅ Brilliant RP — Анкета одобрена!\n\n"
            f"🎮 RP имя: {pending['rp_name']}\n"
            f"🆔 CPM ID: {pending['cpm_id']}\n"
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
        await bot.send_message(uid, "❌ Brilliant RP — Анкета отклонена.\n\nОбратитесь к администратору.")
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
    await message.answer(build_profile_text(user), reply_markup=info_keyboard(message.from_user.id))

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
    if message.chat.type == "private":
        await message.answer("⛔ Зарплату можно получить только в игровом чате.")
        return
    if config.GAME_CHAT_ID and message.chat.id != config.GAME_CHAT_ID:
        await message.answer("⛔ Зарплату можно получить только в игровом чате.")
        return
    user = db.get_user(message.from_user.id)
    status = check_user(user)
    if status == "not_registered":
        await message.answer("❌ Вы не зарегистрированы. Напишите /start")
        return
    if status == "banned":
        await message.answer("⛔ Вы заблокированы.")
        return

    uid, username, cpm_id, game_name, balance, bank, btc, job, last_salary, banned, *_ = user

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

# ==================== АДМИН В ЛС: ЗП / ЗП БИЗНЕС ====================

@dp.message(lambda m: (
    m.chat.type == "private" and
    m.from_user and is_admin(m.from_user.id) and
    m.text and "@" in m.text and
    (m.text.lower().startswith("зп бизнес ") or
     (m.text.lower().startswith("зп ") and not m.text.lower().startswith("зп бизнес ")))
))
async def admin_dm_salary(message: types.Message):
    text_lower = message.text.lower()
    give_biz = text_lower.startswith("зп бизнес ")

    target_username = parse_mentioned_username(message.text)
    if not target_username:
        await message.answer("❌ Формат: зп @ник  или  зп бизнес @ник")
        return

    target = db.get_user_by_username(target_username)
    if not target:
        await message.answer(f"❌ Игрок @{target_username} не найден.")
        return

    uid, username, spm_id, game_name, balance, bank, btc, job, last_salary, banned, *_ = target

    if banned:
        await message.answer(f"⛔ @{target_username} заблокирован.")
        return

    lines = []
    total = 0

    # --- зарплата ---
    salary = ALL_JOBS.get(job, 0) if job else 0
    if salary > 0:
        multiplier = 2 if db.has_x2(uid) else 1
        final_salary = salary * multiplier
        db.update_balance(uid, final_salary)
        db.update_salary_time(uid)
        x2_text = " (х2 🔥)" if multiplier == 2 else ""
        lines.append(f"💵 Зарплата: +{fmt(final_salary)}{x2_text} ({job})")
        total += final_salary
    else:
        lines.append("💵 Зарплата: нет работы")

    # --- доход с бизнесов ---
    if give_biz:
        businesses = db.get_businesses(uid)
        if businesses:
            biz_total = sum(inc for _, inc in businesses)
            db.update_balance(uid, biz_total)
            db.update_biz_income_time(uid)
            lines.append(f"🏢 Доход с бизнесов ({len(businesses)} шт.): +{fmt(biz_total)}")
            total += biz_total
        else:
            lines.append("🏢 Бизнесов нет")

    new_balance = balance + total
    lines.append(f"💰 Новый баланс: {fmt(new_balance)}")
    result_text = "\n".join(lines)

    await message.answer(f"✅ @{target_username}\n\n{result_text}")

    try:
        await bot.send_message(
            uid,
            f"{'🏢 Зарплата + доход с бизнесов' if give_biz else '💵 Вам выдали зарплату'}:\n\n"
            f"{result_text}"
        )
    except Exception:
        pass


# ==================== ЗП @ЮЗЕР ====================

@dp.message(lambda m: (
    m.text and
    m.text.lower().startswith("зп ") and
    "@" in m.text
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

# ==================== ПЕРЕВОД ИГРОК→ИГРОК ====================

@dp.message(lambda m: (
    m.text and m.text.lower().startswith("дать ") and
    "@" in m.text and
    m.reply_to_message is None and
    (m.from_user is None or not is_admin(m.from_user.id))
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
    db.add_log(message.from_user.id, 'transfer', f'→ @{username}', amount)
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

# ==================== БАНК ====================

def _bank_kb(uid: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💰 Внести", callback_data="bank_help_dep"),
            InlineKeyboardButton(text="💸 Вывести", callback_data="bank_help_wd"),
        ],
        [
            InlineKeyboardButton(text="📈 Взять кредит", callback_data="bank_help_cr"),
            InlineKeyboardButton(text="✅ Погасить", callback_data="bank_help_rp"),
        ],
        [InlineKeyboardButton(text="🔄 Обновить", callback_data=f"bank_menu|{uid}")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_to_info|{uid}")],
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
        f"🏦 <b>БАНК Brilliant RP</b>\n"
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
    await message.answer(_bank_text(message.from_user.id), parse_mode="HTML", reply_markup=_bank_kb(message.from_user.id))

@dp.callback_query(F.data.startswith("bank_menu"))
async def cb_bank_menu(callback: types.CallbackQuery):
    uid = await _assert_owner(callback)
    if uid is None:
        return
    await callback.message.edit_text(_bank_text(uid), parse_mode="HTML", reply_markup=_bank_kb(uid))
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
    await message.answer(_bank_text(message.from_user.id), parse_mode="HTML", reply_markup=_bank_kb(message.from_user.id))

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
    await message.answer(_bank_text(message.from_user.id), parse_mode="HTML", reply_markup=_bank_kb(message.from_user.id))

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
        parse_mode="HTML", reply_markup=_bank_kb(message.from_user.id)
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
        parse_mode="HTML", reply_markup=_bank_kb(message.from_user.id)
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
            text="🪪 Купить права — 200₽",
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
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_to_info|{uid}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def build_profile_text(user):
    uid, username, spm_id, game_name, balance, bank, btc, job, last_salary, banned, license_, garage_slots, x2, credit, bank_last_updated, biz_income_time, *extra = user
    appearance = extra[0] if len(extra) > 0 else ""
    text = (
        f"👤 Профиль игрока\n\n"
        f"🎮 RP имя: {game_name}\n"
        f"🆔 CPM ID: {spm_id}\n"
        f"📱 Ник в TG: @{username}\n"
    )
    if appearance:
        text += f"🪞 Внешность: {appearance}\n"
    text += (
        f"💰 Баланс: {fmt(balance)}\n"
        f"🏦 Банк: {fmt(bank)}\n"
        f"💼 Работа: {job if job else 'Безработный'}"
    )
    credit_val = db.get_credit(uid)
    if credit_val > 0:
        text += f"\n\n📉 Кредит: {fmt(credit_val)}"
    return text

@dp.callback_query(F.data.startswith("back_to_info"))
async def cb_back_to_info(callback: types.CallbackQuery):
    uid = await _assert_owner(callback)
    if uid is None:
        return
    user = db.get_user(uid)
    if not user:
        await callback.answer("❌ Не зарегистрированы")
        return
    await callback.message.edit_text(build_profile_text(user), reply_markup=info_keyboard(uid))
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

@dp.callback_query(F.data.startswith("list_cars"))
async def cb_cars(callback: types.CallbackQuery):
    uid = await _assert_owner(callback)
    if uid is None:
        return
    user = db.get_user(uid)
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
        await callback.answer("❌ Недостаточно денег. Нужно 200₽", show_alert=True)
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
            text="🔢 Купить номера — 200₽",
            callback_data=f"buy_plate_{db_id}"
        )])
    else:
        buttons.append([InlineKeyboardButton(
            text="🔄 Перебить номера — 200₽",
            callback_data=f"reroll_plate_{db_id}"
        )])
        buttons.append([InlineKeyboardButton(
            text="🗑 Снять номера — 50₽",
            callback_data=f"del_plate_{db_id}"
        )])
    buttons.append([InlineKeyboardButton(
        text="🔄 Обменять авто",
        callback_data=f"swap_car_menu_{db_id}"
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
        await callback.answer("❌ Недостаточно денег. Нужно 200₽", show_alert=True)
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
    buttons = [
        [InlineKeyboardButton(text="🔄 Перебить номера — 200₽", callback_data=f"reroll_plate_{db_id}")],
        [InlineKeyboardButton(text="🗑 Снять номера — 50₽",     callback_data=f"del_plate_{db_id}")],
        [InlineKeyboardButton(text="🔄 Обменять авто",           callback_data=f"swap_car_menu_{db_id}")],
        [InlineKeyboardButton(text="🔙 Назад",                   callback_data="list_cars")],
    ]
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    await callback.answer(f"✅ Номера: {plate}")

@dp.callback_query(F.data.startswith("del_plate_"))
async def cb_del_plate(callback: types.CallbackQuery):
    user = db.get_user(callback.from_user.id)
    if not user:
        await callback.answer("❌ Не зарегистрированы")
        return
    db_id = int(callback.data.split("_")[2])
    PRICE = 50
    car = db.get_car_by_dbid(db_id)
    if not car or car[1] != callback.from_user.id:
        await callback.answer("❌ Авто не найдено", show_alert=True)
        return
    if not car[5]:
        await callback.answer("❌ Номеров нет", show_alert=True)
        return
    if user[4] < PRICE:
        await callback.answer("❌ Нужно 50₽ для снятия номеров", show_alert=True)
        return
    db.update_balance(user[0], -PRICE)
    db.update_car_plate(db_id, None)
    cdb_id, uid, car_id, car_name, token, _ = car
    text = (f"🚗 {car_name}\n\n🔑 Токен: {token}\n🔢 Номера: ❌ Нет номеров")
    buttons = [
        [InlineKeyboardButton(text="🔢 Купить номера — 200₽", callback_data=f"buy_plate_{db_id}")],
        [InlineKeyboardButton(text="🔄 Обменять авто",         callback_data=f"swap_car_menu_{db_id}")],
        [InlineKeyboardButton(text="🔙 Назад",                 callback_data="list_cars")],
    ]
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    await callback.answer("✅ Номера сняты")

@dp.callback_query(F.data.startswith("swap_car_menu_"))
async def cb_swap_car_menu(callback: types.CallbackQuery):
    user = db.get_user(callback.from_user.id)
    if not user:
        await callback.answer("❌ Не зарегистрированы")
        return
    db_id = int(callback.data.split("_")[3])
    car = db.get_car_by_dbid(db_id)
    if not car or car[1] != callback.from_user.id:
        await callback.answer("❌ Авто не найдено", show_alert=True)
        return
    _, uid, car_id, car_name, token, plate = car
    car_price = CARS[car_id][1] if car_id in CARS else 0
    await callback.message.edit_text(
        f"🔄 Обмен авто: {car_name}\n"
        f"💰 Стоимость вашего авто: {fmt(car_price)}\n\n"
        f"Напишите команду:\n"
        f"<code>обменять авто {token} [номер нового авто]</code>\n\n"
        f"Пример: <code>обменять авто {token} 15</code>\n\n"
        f"Вы доплачиваете или получаете разницу в цене.\n"
        f"Каталог авто: напишите <b>каталог авто</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data=f"car_det_{db_id}")]
        ])
    )
    await callback.answer()

@dp.message(lambda m: m.text and m.text.lower().startswith("обменять авто "))
async def swap_car_cmd(message: types.Message):
    user = db.get_user(message.from_user.id)
    status = check_user(user)
    if status != "ok":
        await message.answer("❌ Вы не зарегистрированы." if status == "not_registered" else "⛔ Вы заблокированы.")
        return
    parts = message.text.strip().split()
    if len(parts) < 4:
        await message.answer("❌ Формат: обменять авто [токен] [номер нового авто]\nПример: обменять авто ABC123 15")
        return
    token = parts[2].upper()
    try:
        new_car_id = int(parts[3])
    except Exception:
        await message.answer("❌ Укажите номер нового авто из каталога.")
        return
    car = db.get_car_by_token(token)
    if not car or car[1] != message.from_user.id:
        await message.answer("❌ Авто с таким токеном не найдено в вашем гараже.")
        return
    if new_car_id not in CARS:
        await message.answer(f"❌ Авто №{new_car_id} не найдено. Напишите <b>каталог авто</b>.", parse_mode="HTML")
        return
    cdb_id, uid, old_car_id, old_car_name, old_token, plate = car
    old_price = CARS[old_car_id][1] if old_car_id in CARS else 0
    new_car_name, new_price = CARS[new_car_id]
    diff = new_price - old_price
    balance = user[4]
    if diff > 0 and balance < diff:
        await message.answer(
            f"❌ Недостаточно средств для обмена.\n\n"
            f"Ваше авто: {old_car_name} ({fmt(old_price)})\n"
            f"Новое авто: {new_car_name} ({fmt(new_price)})\n"
            f"Нужно доплатить: {fmt(diff)}\n"
            f"Ваш баланс: {fmt(balance)}"
        )
        return
    diff_text = f"Доплата: {fmt(diff)}" if diff > 0 else (f"Возврат: {fmt(-diff)}" if diff < 0 else "Доплата: 0₽")
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Подтвердить обмен", callback_data=f"swap_confirm_{cdb_id}_{new_car_id}"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="cbuy_cancel"),
    ]])
    await message.answer(
        f"🔄 Обмен автомобиля\n\n"
        f"Отдаёте: {old_car_name} ({fmt(old_price)})\n"
        f"Получаете: {new_car_name} ({fmt(new_price)})\n"
        f"{diff_text}\n\n"
        f"Подтвердить?",
        reply_markup=kb
    )

@dp.callback_query(F.data.startswith("swap_confirm_"))
async def cb_swap_confirm(callback: types.CallbackQuery):
    user = db.get_user(callback.from_user.id)
    if not user:
        await callback.answer("❌ Не зарегистрированы")
        return
    parts = callback.data.split("_")
    cdb_id = int(parts[2])
    new_car_id = int(parts[3])
    car = db.get_car_by_dbid(cdb_id)
    if not car or car[1] != callback.from_user.id:
        await callback.answer("❌ Авто не найдено", show_alert=True)
        return
    if new_car_id not in CARS:
        await callback.answer("❌ Новое авто не найдено", show_alert=True)
        return
    _, uid, old_car_id, old_car_name, _, plate = car
    old_price = CARS[old_car_id][1] if old_car_id in CARS else 0
    new_car_name, new_price = CARS[new_car_id]
    diff = new_price - old_price
    balance = user[4]
    if diff > 0 and balance < diff:
        await callback.answer(f"❌ Недостаточно средств. Нужно {fmt(diff)}", show_alert=True)
        return
    # Удаляем старое авто, добавляем новое (сохраняем номера)
    db.remove_car(cdb_id)
    db.add_car(uid, new_car_id, new_car_name)
    if diff != 0:
        db.update_balance(uid, -diff)
    # Если были номера — переносим на новое авто
    if plate:
        new_cars = db.get_cars_full(uid)
        if new_cars:
            newest = new_cars[-1]
            db.update_car_plate(newest[0], plate)
    diff_text = f"Доплачено: {fmt(diff)}" if diff > 0 else (f"Возвращено: {fmt(-diff)}" if diff < 0 else "")
    await callback.message.edit_text(
        f"✅ Обмен выполнен!\n\n"
        f"Отдали: {old_car_name}\n"
        f"Получили: {new_car_name}\n"
        + (f"{diff_text}\n" if diff_text else "") +
        f"💰 Баланс: {fmt(balance - diff)}"
    )
    await callback.answer("✅ Авто обменяно!")

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

# ==================== РАБОТЫ (ИНЛАЙН) ====================

JOBS_LIST = list(JOBS.items())
JOBS_PER_PAGE = 5

GOV_JOB_CATEGORIES = [
    ("🇷🇺 Правительство", [
        "Охранник (Правительство)", "Секретарь (Правительство)", "Юрист (Правительство)",
        "Адвокат (Правительство)", "Прокурор (Правительство)", "Глава аппарата",
        "Вице-губернатор", "Губернатор", "Министр", "Премьер-Министр",
    ]),
    ("🇷🇺 ФСБ", [
        "Младший сержант (ФСБ)", "Сержант (ФСБ)", "Младший лейтенант (ФСБ)",
        "Капитан (ФСБ)", "Майор (ФСБ)", "Подполковник (ФСБ)",
        "Генерал-майор (ФСБ)", "Генерал-лейтенант (ФСБ)",
    ]),
    ("🤩 МВД", [
        "Сержант (МВД)", "Лейтенант (МВД)", "Капитан (МВД)", "Майор (МВД)",
        "Подполковник (МВД)", "Полковник (МВД)", "Генерал-майор (МВД)",
        "Генерал-лейтенант (МВД)",
    ]),
    ("🇷🇺 Мин.Здрав", [
        "Медик (Мин.Здрав)", "Врач (Мин.Здрав)", "Заместитель глав.врача", "Глав-врач",
    ]),
    ("🇷🇺 ВсРФ (армия)", [
        "Сержант (ВсРФ)", "Лейтенант (ВсРФ)", "Капитан (ВсРФ)", "Майор (ВсРФ)",
        "Подполковник (ВсРФ)", "Полковник (ВсРФ)", "Генерал-майор (ВсРФ)",
        "Генерал-лейтенант (ВсРФ)",
    ]),
    ("🇷🇺 ЦОДД", [
        "Дорожный патруль (ЦОДД)", "Мобильный ситуационный центр (ЦОДД)",
        "Дорожные координаторы (ЦОДД)", "Служба эксплуатации (ЦОДД)",
        "Ситуационный центр (ЦОДД)",
    ]),
    ("Следственный комитет", [
        "Мл. лейтенант юстиции (СК)", "Лейтенант юстиции (СК)", "Ст. лейтенант юстиции (СК)",
        "Капитан юстиции (СК)", "Майор юстиции (СК)", "Подполковник юстиции (СК)",
        "Полковник юстиции (СК)", "Генерал-майор юстиции (СК)", "Генерал-лейтенант юстиции (СК)",
    ]),
]

def _main_jobs_kb(uid: int, has_job: bool) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text="💼 Гражданские работы", callback_data="jobs_civ_0")],
        [InlineKeyboardButton(text="🏛 Гос. должности", callback_data="jobs_gov_cats")],
    ]
    if has_job:
        rows.append([InlineKeyboardButton(text="🚪 Уволиться", callback_data="quit_job")])
    rows.append([InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_to_info|{uid}")])
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

@dp.callback_query(F.data.startswith("list_jobs"))
async def cb_jobs(callback: types.CallbackQuery):
    uid = await _assert_owner(callback)
    if uid is None:
        return
    user = db.get_user(uid)
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
    await callback.message.edit_text(text, reply_markup=_main_jobs_kb(uid, bool(job)))
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
    await callback.message.edit_text(text, reply_markup=back_keyboard(callback.from_user.id))
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
        reply_markup=back_keyboard(callback.from_user.id)
    )
    await callback.answer("Вы уволились")

@dp.callback_query(F.data.startswith("list_biz"))
async def cb_biz(callback: types.CallbackQuery):
    uid = await _assert_owner(callback)
    if uid is None:
        return
    user = db.get_user(uid)
    if not user:
        await callback.answer("❌ Не зарегистрированы")
        return
    bizs = db.get_businesses_full(uid)
    text = "🏢 Ваши бизнесы\n\n"
    if bizs:
        total = sum(inc for _, _, inc, _ in bizs)
        for i, (bid, name, income, token) in enumerate(bizs, 1):
            text += f"{i}. {name}\n   💵 {fmt(income)}/день | 🔑 {token}\n"
        text += f"\n📈 Суммарный доход: {fmt(total)}/день"
    else:
        text += "У вас нет бизнесов.\n📝 Купить: купить бизнес [номер]"
    await callback.message.edit_text(text, reply_markup=back_keyboard(uid))
    await callback.answer()

@dp.callback_query(F.data.startswith("list_apts"))
async def cb_apts(callback: types.CallbackQuery):
    uid = await _assert_owner(callback)
    if uid is None:
        return
    user = db.get_user(uid)
    if not user:
        await callback.answer("❌ Не зарегистрированы")
        return
    apts = db.get_apartments_full(uid)
    text = "🏠 Ваша недвижимость\n\n"
    if apts:
        for i, (aid, name, token) in enumerate(apts, 1):
            text += f"{i}. {name} | 🔑 {token}\n"
    else:
        text += "У вас нет недвижимости.\n📝 Купить: купить недвижимость [номер]"
    await callback.message.edit_text(text, reply_markup=back_keyboard(uid))
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
            f"🔑 Токен сделки: {sale_token}\n"
            f"💰 Цена: {fmt(sale_price)}\n\n"
            f"Для подтверждения напишите:\n"
            f"<code>купить сделка {sale_token}</code>"
        )
        try:
            await bot.send_message(target[0], offer_text, parse_mode="HTML")
        except Exception:
            pass
        await message.answer(
            f"✅ Предложение отправлено @{target_nick}\n"
            f"🔑 Токен сделки: {sale_token}\n"
            f"💰 Цена: {fmt(sale_price)}"
        )
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=f"✅ Продать за {fmt(state_price)}", callback_data=f"sell_confirm_{atype}_{db_id}"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="sell_cancel"),
    ]])
    await message.answer(
        f"🏷 {type_name}: {asset_name}\n\n"
        f"💰 Полная цена: {fmt(full_price)}\n"
        f"🏛 Государству (50%): {fmt(state_price)}\n\n"
        f"Продать государству?",
        reply_markup=kb
    )

@dp.callback_query(F.data.startswith("sell_confirm_"))
async def cb_sell_confirm(callback: types.CallbackQuery):
    user = db.get_user(callback.from_user.id)
    if not user:
        await callback.answer("❌ Не зарегистрированы")
        return
    parts = callback.data.split("_")
    atype = parts[2]
    db_id = int(parts[3])
    uid = user[0]

    if atype == "car":
        asset = db.get_car_by_dbid(db_id)
        if not asset or asset[1] != uid:
            await callback.answer("❌ Авто не найдено", show_alert=True)
            return
        asset_id = asset[2]
        asset_name = asset[3]
        full_price = _get_asset_price("car", asset_id)
        state_price = full_price // 2
        db.update_balance(uid, state_price)
        db.remove_car(db_id)
    elif atype == "biz":
        asset = db.get_business_by_dbid(db_id)
        if not asset or asset[1] != uid:
            await callback.answer("❌ Бизнес не найден", show_alert=True)
            return
        asset_id = asset[2]
        asset_name = asset[3]
        full_price = _get_asset_price("biz", asset_id)
        state_price = full_price // 2
        db.update_balance(uid, state_price)
        db.remove_business(db_id)
    else:
        asset = db.get_apartment_by_dbid(db_id)
        if not asset or asset[1] != uid:
            await callback.answer("❌ Объект не найден", show_alert=True)
            return
        asset_id = asset[2]
        asset_name = asset[3]
        full_price = _get_asset_price("apt", asset_id)
        state_price = full_price // 2
        db.update_balance(uid, state_price)
        db.remove_apartment(db_id)

    await callback.message.edit_text(
        f"✅ Продано государству!\n\n"
        f"📋 {asset_name}\n"
        f"💰 Получено: {fmt(state_price)}"
    )
    await callback.answer()

@dp.callback_query(F.data == "sell_cancel")
async def cb_sell_cancel(callback: types.CallbackQuery):
    await callback.message.edit_text("❌ Продажа отменена.")
    await callback.answer()

@dp.message(lambda m: m.text and m.text.lower().startswith("купить сделка "))
async def buy_deal_cmd(message: types.Message):
    user = db.get_user(message.from_user.id)
    status = check_user(user)
    if status != "ok":
        await message.answer("❌ Вы не зарегистрированы." if status == "not_registered" else "⛔ Вы заблокированы.")
        return
    parts = message.text.strip().split()
    if len(parts) < 3:
        await message.answer("❌ Формат: купить сделка [токен]")
        return
    sale_token = parts[2].upper()
    deal = PENDING_SALES.get(sale_token)
    if not deal:
        await message.answer("❌ Сделка не найдена или устарела.")
        return
    if deal["buyer_uid"] != user[0]:
        await message.answer("❌ Эта сделка не для вас.")
        return
    if user[4] < deal["price"]:
        await message.answer(f"❌ Недостаточно средств. Нужно {fmt(deal['price'])}")
        return

    PENDING_SALES.pop(sale_token, None)
    atype = deal["type"]
    db_id = deal["db_id"]
    seller_uid = deal["seller_uid"]
    buyer_uid = user[0]
    price = deal["price"]
    name = deal["name"]

    if atype == "car":
        asset = db.get_car_by_dbid(db_id)
        if not asset or asset[1] != seller_uid:
            await message.answer("❌ Актив уже продан или недоступен.")
            return
        db.update_balance(buyer_uid, -price)
        db.update_balance(seller_uid, price)
        db.transfer_car(db_id, buyer_uid)
    elif atype == "biz":
        asset = db.get_business_by_dbid(db_id)
        if not asset or asset[1] != seller_uid:
            await message.answer("❌ Актив уже продан или недоступен.")
            return
        db.update_balance(buyer_uid, -price)
        db.update_balance(seller_uid, price)
        db.transfer_business(db_id, buyer_uid)
    else:
        asset = db.get_apartment_by_dbid(db_id)
        if not asset or asset[1] != seller_uid:
            await message.answer("❌ Актив уже продан или недоступен.")
            return
        db.update_balance(buyer_uid, -price)
        db.update_balance(seller_uid, price)
        db.transfer_apartment(db_id, buyer_uid)

    await message.answer(f"✅ Сделка завершена!\n\n📋 {name}\n💰 Оплачено: {fmt(price)}")
    try:
        buyer_nick = message.from_user.username or message.from_user.first_name
        await bot.send_message(seller_uid, f"✅ Продажа завершена!\n\n📋 {name}\n💰 Получено: {fmt(price)}\nКупил: @{buyer_nick}")
    except Exception:
        pass

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
        await message.answer(f"❌ Авто №{car_id} не найдено. Доступны: 1–111")
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
    parts = message.text.strip().split()
    # форматы: "купить бизнес 7"  или  "купить бизнес 3 номер 5"
    try:
        biz_type = int(parts[2])
        if len(parts) >= 5 and parts[3].lower() == "номер":
            slot = int(parts[4])
        else:
            slot = 1
    except Exception:
        await message.answer("❌ Формат: купить бизнес [номер]\nДля многослотовых: купить бизнес [номер] номер [слот]")
        return
    data = _biz_slot_data(biz_type, slot)
    if data is None:
        name_hint = BUSINESSES[biz_type][0] if biz_type in BUSINESSES else f"№{biz_type}"
        slots_hint = len(BUSINESSES[biz_type][1]) if biz_type in BUSINESSES else 0
        if biz_type not in BUSINESSES:
            await message.answer(f"❌ Бизнес №{biz_type} не найден. Доступны: 1–27")
        else:
            await message.answer(f"❌ Слот #{slot} не существует для «{name_hint}» (доступно: 1–{slots_hint})")
        return
    biz_name, biz_price, biz_income = data
    db_biz_id = _biz_db_id(biz_type, slot)
    owner = db.get_biz_owner(db_biz_id)
    if owner:
        err = "Вы уже владеете этим слотом." if owner == message.from_user.id else "Этот слот уже принадлежит другому игроку."
        await message.answer(f"❌ {err}")
        return
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
        InlineKeyboardButton(text="✅ Купить", callback_data=f"bb_{biz_type}_{slot}"),
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
        await message.answer(f"❌ Объект №{apt_id} не найден. Доступны: 1–39")
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
    db.add_log(callback.from_user.id, 'buy_car', car_name, car_price)
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
    # callback_data = "bb_{biz_type}_{slot}"
    parts = callback.data.split("_")
    try:
        biz_type = int(parts[1])
        slot = int(parts[2])
    except Exception:
        await callback.answer("❌ Ошибка данных")
        return
    data = _biz_slot_data(biz_type, slot)
    if data is None:
        await callback.answer("❌ Бизнес не найден")
        return
    biz_name, biz_price, biz_income = data
    db_biz_id = _biz_db_id(biz_type, slot)
    owner = db.get_biz_owner(db_biz_id)
    if owner:
        err = "Вы уже владеете этим слотом." if owner == callback.from_user.id else "Этот слот уже принадлежит другому игроку."
        await callback.answer(f"❌ {err}", show_alert=True)
        return
    balance = user[4]
    if balance < biz_price:
        await callback.answer(f"❌ Недостаточно средств. Нужно {fmt(biz_price)}", show_alert=True)
        return
    db.update_balance(callback.from_user.id, -biz_price)
    db.add_business(callback.from_user.id, db_biz_id, biz_name, biz_income)
    db.add_log(callback.from_user.id, 'buy_biz', biz_name, biz_price)
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
    db.add_log(callback.from_user.id, 'buy_apt', apt_name, apt_price)
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
        def _biz_price_by_db_id(db_id):
            biz_type, slot = db_id // 100, db_id % 100
            d = _biz_slot_data(biz_type, slot)
            return d[1] if d else 0
        biz_val = sum(_biz_price_by_db_id(b) for b in biz_ids)
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

# ==================== КАТАЛОГИ ====================

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
    for biz_type, (name, slots) in BUSINESSES.items():
        if len(slots) == 1:
            price, income = slots[1]
            lines.append(f"№{biz_type}. {name} — {fmt(price)} (доход: {fmt(income)}/день)")
        else:
            # Показываем диапазон цен если отличаются
            prices = set(p for p, i in slots.values())
            incomes = set(i for p, i in slots.values())
            price_str = fmt(min(prices)) if len(prices) == 1 else f"{fmt(min(prices))}–{fmt(max(prices))}"
            income_str = fmt(min(incomes)) if len(incomes) == 1 else f"{fmt(min(incomes))}–{fmt(max(incomes))}"
            lines.append(f"№{biz_type}. {name} [{len(slots)} слота] — {price_str} (доход: {income_str}/день)")
            lines.append(f"   ↳ Команда: купить бизнес {biz_type} номер [1–{len(slots)}]")
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

# ==================== ПОМОЩЬ ====================

@dp.message(lambda m: m.text and m.text.lower() in ["помощь", "команды", "/help"])
async def help_cmd(message: types.Message):
    await message.answer(
        "📋 Brilliant RP — Команды:\n\n"
        "━━━━ 👤 Профиль ━━━━\n"
        "инфо — профиль\n"
        "б / баланс — текущий баланс\n\n"
        "━━━━ 💼 Работа и зарплата ━━━━\n"
        "зп — получить зарплату\n"
        "зп @ник — зарплата игроку\n\n"
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
        "━━━━ 🏦 Банк ━━━━\n"
        "банк\n"
        "внести / вывести [сумма]\n"
        "кредит / погасить [сумма]\n\n"
        "━━━━ 🎟 Промокоды ━━━━\n"
        "активировать [КОД] — активировать промокод\n\n"
        "━━━━ 🛒 Покупки ━━━━\n"
        "купить авто [id]\n"
        "купить бизнес [id]\n"
        "купить недвижимость [id]\n\n"
        "━━━━ 📋 Каталоги ━━━━\n"
        "каталог авто / каталог бизнесов / каталог недвижимости\n\n"
        "мои авто / мои бизнесы / мои объекты"
    )

# ==================== ДИНАМИЧЕСКИЙ КАТАЛОГ (МАШИНЫ) ====================

@dp.message(lambda m: m.text and m.text.lower().strip() == "добавить машину")
async def add_car_start(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.set_state(AddCarFSM.name)
    await message.answer("🚗 Добавление машины\n\nВведите название:")

@dp.message(AddCarFSM.name)
async def add_car_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(AddCarFSM.price)
    await message.answer("💰 Введите цену (только цифры, например: 95000):")

@dp.message(AddCarFSM.price)
async def add_car_price(message: types.Message, state: FSMContext):
    try:
        price = float(message.text.replace(" ", "").replace(",", "."))
        if price <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Некорректная цена. Введите число:")
        return
    await state.update_data(price=price)
    await state.set_state(AddCarFSM.description)
    await message.answer("📝 Введите описание (или напишите '-' чтобы пропустить):")

@dp.message(AddCarFSM.description)
async def add_car_description(message: types.Message, state: FSMContext):
    desc = message.text.strip()
    if desc == "-":
        desc = ""
    await state.update_data(description=desc)
    await state.set_state(AddCarFSM.specs)
    await message.answer("⚙️ Введите характеристики (или '-' чтобы пропустить):")

@dp.message(AddCarFSM.specs)
async def add_car_specs(message: types.Message, state: FSMContext):
    specs = message.text.strip()
    if specs == "-":
        specs = ""
    await state.update_data(specs=specs)
    await state.set_state(AddCarFSM.confirm)
    data = await state.get_data()
    text = (
        f"🚗 <b>Подтвердите добавление:</b>\n\n"
        f"Название: <b>{data['name']}</b>\n"
        f"Цена: <b>{fmt(data['price'])}</b>\n"
        f"Описание: {data.get('description') or '—'}\n"
        f"Характеристики: {data.get('specs') or '—'}\n\n"
        f"Написать <b>да</b> — добавить\n"
        f"Написать <b>нет</b> — отменить"
    )
    await message.answer(text, parse_mode="HTML")

@dp.message(AddCarFSM.confirm)
async def add_car_confirm(message: types.Message, state: FSMContext):
    answer = message.text.strip().lower()
    if answer != "да":
        await state.clear()
        await message.answer("❌ Отменено.")
        return
    data = await state.get_data()
    new_id = max(CARS.keys()) + 1
    CARS[new_id] = (data['name'], data['price'])
    db.add_catalog_item(
        item_type='car',
        game_id=new_id,
        name=data['name'],
        price=data['price'],
        description=data.get('description', ''),
        specs=data.get('specs', ''),
        added_by=message.from_user.id
    )
    await state.clear()
    await message.answer(
        f"✅ Машина добавлена!\n"
        f"ID в каталоге: <b>{new_id}</b>\n"
        f"Название: <b>{data['name']}</b>\n"
        f"Цена: <b>{fmt(data['price'])}</b>",
        parse_mode="HTML"
    )

# ==================== ДИНАМИЧЕСКИЙ КАТАЛОГ (БИЗНЕСЫ) ====================

@dp.message(lambda m: m.text and m.text.lower().strip() == "добавить бизнес")
async def add_biz_start(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.set_state(AddBizFSM.name)
    await message.answer("🏢 Добавление бизнеса\n\nВведите название:")

@dp.message(AddBizFSM.name)
async def add_biz_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(AddBizFSM.price)
    await message.answer("💰 Введите цену покупки:")

@dp.message(AddBizFSM.price)
async def add_biz_price(message: types.Message, state: FSMContext):
    try:
        price = float(message.text.replace(" ", "").replace(",", "."))
        if price <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Некорректная цена. Введите число:")
        return
    await state.update_data(price=price)
    await state.set_state(AddBizFSM.income)
    await message.answer("📈 Введите доход за 3 часа (например: 5000):")

@dp.message(AddBizFSM.income)
async def add_biz_income(message: types.Message, state: FSMContext):
    try:
        income = float(message.text.replace(" ", "").replace(",", "."))
        if income <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Некорректный доход. Введите число:")
        return
    await state.update_data(income=income)
    await state.set_state(AddBizFSM.description)
    await message.answer("📝 Введите описание (или '-' пропустить):")

@dp.message(AddBizFSM.description)
async def add_biz_description(message: types.Message, state: FSMContext):
    desc = message.text.strip()
    if desc == "-":
        desc = ""
    await state.update_data(description=desc)
    await state.set_state(AddBizFSM.confirm)
    data = await state.get_data()
    text = (
        f"🏢 <b>Подтвердите добавление:</b>\n\n"
        f"Название: <b>{data['name']}</b>\n"
        f"Цена: <b>{fmt(data['price'])}</b>\n"
        f"Доход/3ч: <b>{fmt(data['income'])}</b>\n"
        f"Описание: {data.get('description') or '—'}\n\n"
        f"Написать <b>да</b> — добавить\n"
        f"Написать <b>нет</b> — отменить"
    )
    await message.answer(text, parse_mode="HTML")

@dp.message(AddBizFSM.confirm)
async def add_biz_confirm(message: types.Message, state: FSMContext):
    answer = message.text.strip().lower()
    if answer != "да":
        await state.clear()
        await message.answer("❌ Отменено.")
        return
    data = await state.get_data()
    new_id = max(BUSINESSES.keys()) + 1
    BUSINESSES[new_id] = (data['name'], data['price'], data['income'])
    db.add_catalog_item(
        item_type='biz',
        game_id=new_id,
        name=data['name'],
        price=data['price'],
        income=data['income'],
        description=data.get('description', ''),
        added_by=message.from_user.id
    )
    await state.clear()
    await message.answer(
        f"✅ Бизнес добавлен!\n"
        f"ID в каталоге: <b>{new_id}</b>\n"
        f"Название: <b>{data['name']}</b>\n"
        f"Цена: <b>{fmt(data['price'])}</b>\n"
        f"Доход/3ч: <b>{fmt(data['income'])}</b>",
        parse_mode="HTML"
    )

# ==================== ДИНАМИЧЕСКИЙ КАТАЛОГ (НЕДВИЖИМОСТЬ) ====================

@dp.message(lambda m: m.text and m.text.lower().strip() == "добавить недвижимость")
async def add_apt_start(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.set_state(AddAptFSM.name)
    await message.answer("🏠 Добавление недвижимости\n\nВведите название:")

@dp.message(AddAptFSM.name)
async def add_apt_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(AddAptFSM.price)
    await message.answer("💰 Введите цену:")

@dp.message(AddAptFSM.price)
async def add_apt_price(message: types.Message, state: FSMContext):
    try:
        price = float(message.text.replace(" ", "").replace(",", "."))
        if price <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Некорректная цена. Введите число:")
        return
    await state.update_data(price=price)
    await state.set_state(AddAptFSM.description)
    await message.answer("📝 Введите описание (или '-' пропустить):")

@dp.message(AddAptFSM.description)
async def add_apt_description(message: types.Message, state: FSMContext):
    desc = message.text.strip()
    if desc == "-":
        desc = ""
    await state.update_data(description=desc)
    await state.set_state(AddAptFSM.confirm)
    data = await state.get_data()
    text = (
        f"🏠 <b>Подтвердите добавление:</b>\n\n"
        f"Название: <b>{data['name']}</b>\n"
        f"Цена: <b>{fmt(data['price'])}</b>\n"
        f"Описание: {data.get('description') or '—'}\n\n"
        f"Написать <b>да</b> — добавить\n"
        f"Написать <b>нет</b> — отменить"
    )
    await message.answer(text, parse_mode="HTML")

@dp.message(AddAptFSM.confirm)
async def add_apt_confirm(message: types.Message, state: FSMContext):
    answer = message.text.strip().lower()
    if answer != "да":
        await state.clear()
        await message.answer("❌ Отменено.")
        return
    data = await state.get_data()
    new_id = max(APARTMENTS.keys()) + 1
    APARTMENTS[new_id] = (data['name'], data['price'])
    db.add_catalog_item(
        item_type='apt',
        game_id=new_id,
        name=data['name'],
        price=data['price'],
        description=data.get('description', ''),
        added_by=message.from_user.id
    )
    await state.clear()
    await message.answer(
        f"✅ Недвижимость добавлена!\n"
        f"ID в каталоге: <b>{new_id}</b>\n"
        f"Название: <b>{data['name']}</b>\n"
        f"Цена: <b>{fmt(data['price'])}</b>",
        parse_mode="HTML"
    )

# ==================== ПРОМОКОДЫ ====================

@dp.message(lambda m: m.text and m.text.lower().strip() == "добавить промокод")
async def add_promo_start(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.set_state(AddPromoFSM.code)
    await message.answer("🎟 Создание промокода\n\nВведите код (латиница и цифры, например: PROMO50):")

@dp.message(AddPromoFSM.code)
async def add_promo_code_step(message: types.Message, state: FSMContext):
    code = message.text.strip().upper()
    if not code.replace("_", "").replace("-", "").isalnum():
        await message.answer("❌ Код может содержать только буквы и цифры. Введите заново:")
        return
    await state.update_data(code=code)
    await state.set_state(AddPromoFSM.amount)
    await message.answer(f"💰 Промокод: <b>{code}</b>\n\nВведите сумму награды:", parse_mode="HTML")

@dp.message(AddPromoFSM.amount)
async def add_promo_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text.replace(" ", "").replace(",", "."))
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Некорректная сумма. Введите число:")
        return
    await state.update_data(amount=amount)
    await state.set_state(AddPromoFSM.max_uses)
    await message.answer("🔢 Сколько раз можно использовать? (0 = неограниченно):")

@dp.message(AddPromoFSM.max_uses)
async def add_promo_max_uses(message: types.Message, state: FSMContext):
    try:
        max_uses = int(message.text.strip())
        if max_uses < 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Введите число (0 или больше):")
        return
    await state.update_data(max_uses=max_uses)
    await state.set_state(AddPromoFSM.confirm)
    data = await state.get_data()
    uses_text = "неограниченно" if max_uses == 0 else str(max_uses)
    text = (
        f"🎟 <b>Подтвердите создание:</b>\n\n"
        f"Код: <b>{data['code']}</b>\n"
        f"Сумма: <b>{fmt(data['amount'])}</b>\n"
        f"Использований: <b>{uses_text}</b>\n\n"
        f"Написать <b>да</b> — создать\n"
        f"Написать <b>нет</b> — отменить"
    )
    await message.answer(text, parse_mode="HTML")

@dp.message(AddPromoFSM.confirm)
async def add_promo_confirm(message: types.Message, state: FSMContext):
    answer = message.text.strip().lower()
    if answer != "да":
        await state.clear()
        await message.answer("❌ Отменено.")
        return
    data = await state.get_data()
    success = db.add_promo_code(data['code'], data['amount'], data['max_uses'], message.from_user.id)
    await state.clear()
    if success:
        uses_text = "неограниченно" if data['max_uses'] == 0 else str(data['max_uses'])
        await message.answer(
            f"✅ Промокод создан!\n"
            f"Код: <b>{data['code']}</b>\n"
            f"Сумма: <b>{fmt(data['amount'])}</b>\n"
            f"Использований: <b>{uses_text}</b>",
            parse_mode="HTML"
        )
    else:
        await message.answer("❌ Промокод с таким кодом уже существует.")

@dp.message(lambda m: m.text and m.text.lower().strip() == "выключить промокод")
async def disable_promo_start(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.set_state(DisablePromoFSM.code)
    await message.answer("🔴 Введите код промокода для отключения:")

@dp.message(DisablePromoFSM.code)
async def disable_promo_code_step(message: types.Message, state: FSMContext):
    code = message.text.strip().upper()
    await state.clear()
    success = db.disable_promo_code(code)
    if success:
        await message.answer(f"✅ Промокод <b>{code}</b> отключён.", parse_mode="HTML")
    else:
        await message.answer(f"❌ Промокод <b>{code}</b> не найден или уже отключён.", parse_mode="HTML")

@dp.message(lambda m: m.text and m.text.lower().strip() == "промокоды")
async def list_promos_cmd(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    promos = db.get_active_promos()
    if not promos:
        await message.answer("📋 Нет активных промокодов.")
        return
    lines = ["🎟 <b>Активные промокоды:</b>\n"]
    for code, amount, max_uses, used_count, added_at in promos:
        uses_str = f"{used_count}/{max_uses}" if max_uses > 0 else f"{used_count}/∞"
        lines.append(f"• <code>{code}</code> — {fmt(amount)} | использований: {uses_str}")
    await message.answer("\n".join(lines), parse_mode="HTML")

@dp.message(lambda m: m.text and m.text.lower().strip().startswith("активировать "))
async def activate_promo_cmd(message: types.Message):
    user = db.get_user(message.from_user.id)
    status = check_user(user)
    if status == "not_registered":
        await message.answer("❌ Вы не зарегистрированы. Напишите /start")
        return
    if status == "banned":
        await message.answer("⛔ Вы заблокированы.")
        return
    parts = message.text.strip().split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("❌ Формат: активировать [КОД]")
        return
    code = parts[1].strip().upper()
    success, amount, reason = db.use_promo_code(message.from_user.id, code)
    if success:
        db.update_balance(message.from_user.id, amount)
        balance = db.get_user(message.from_user.id)[4]
        await message.answer(
            f"✅ Промокод <b>{code}</b> активирован!\n"
            f"💰 Начислено: <b>+{fmt(amount)}</b>\n"
            f"💵 Баланс: <b>{fmt(balance)}</b>",
            parse_mode="HTML"
        )
    else:
        msgs = {
            "not_found": f"❌ Промокод <b>{code}</b> не найден.",
            "disabled": f"❌ Промокод <b>{code}</b> отключён.",
            "exhausted": f"❌ Промокод <b>{code}</b> исчерпан.",
            "already_used": f"❌ Вы уже использовали промокод <b>{code}</b>.",
        }
        await message.answer(msgs.get(reason, "❌ Ошибка активации."), parse_mode="HTML")

# ==================== ОСНОВАТЕЛЬ: УПРАВЛЕНИЕ АДМИНИСТРАТОРАМИ ====================

@dp.message(lambda m: m.text and m.text.lower().startswith("добавить администратора") and m.from_user and is_founder(m.from_user.id))
async def add_admin_cmd(message: types.Message):
    username = next((p[1:] for p in message.text.split() if p.startswith("@")), None)
    if not username:
        await message.answer("❌ Формат: добавить администратора @никнейм")
        return
    target = db.get_user_by_username(username)
    if not target:
        await message.answer("❌ Игрок не найден")
        return
    if is_founder(target[0]):
        await message.answer("❌ Этот игрок уже является основателем.")
        return
    db.grant_admin(target[0], message.from_user.id)
    db.add_log(target[0], 'admin_grant', f'выдал {message.from_user.id}', 0, message.from_user.id)
    await message.answer(f"✅ @{username} назначен администратором.")
    try:
        await bot.send_message(target[0], "✅ Вам выданы права администратора в Brilliant RP.")
    except Exception:
        pass

@dp.message(lambda m: m.text and m.text.lower().startswith("снять администратора") and m.from_user and is_founder(m.from_user.id))
async def remove_admin_cmd(message: types.Message):
    username = next((p[1:] for p in message.text.split() if p.startswith("@")), None)
    if not username:
        await message.answer("❌ Формат: снять администратора @никнейм")
        return
    target = db.get_user_by_username(username)
    if not target:
        await message.answer("❌ Игрок не найден")
        return
    if is_founder(target[0]):
        await message.answer("❌ Нельзя снять основателя.")
        return
    success = db.revoke_admin(target[0])
    if success:
        db.add_log(target[0], 'admin_revoke', f'снял {message.from_user.id}', 0, message.from_user.id)
        await message.answer(f"✅ Права администратора у @{username} сняты.")
        try:
            await bot.send_message(target[0], "⚠️ Ваши права администратора в Brilliant RP сняты.")
        except Exception:
            pass
    else:
        await message.answer(f"❌ @{username} не является администратором в БД.")

@dp.message(lambda m: m.text and m.text.lower().strip() == "администраторы" and m.from_user and is_admin(m.from_user.id))
async def list_admins_cmd(message: types.Message):
    import datetime
    lines = ["👑 <b>Администраторы Brilliant RP:</b>\n"]
    lines.append("<b>🔑 Основатели:</b>")
    for uid in config.ADMIN_IDS:
        u = db.get_user(uid)
        name = f"@{u[1]}" if u and u[1] else f"ID:{uid}"
        lines.append(f"  • {name}")
    db_admins = db.get_admins()
    if db_admins:
        lines.append("\n<b>👮 Администраторы (DB):</b>")
        for uid, granted_by, granted_at in db_admins:
            u = db.get_user(uid)
            name = f"@{u[1]}" if u and u[1] else f"ID:{uid}"
            dt = datetime.datetime.fromtimestamp(granted_at).strftime('%d.%m.%Y')
            lines.append(f"  • {name} (с {dt})")
    else:
        lines.append("\n<i>Нет администраторов в БД</i>")
    await message.answer("\n".join(lines), parse_mode="HTML")

# ==================== ИЗЪЯТИЕ ИМУЩЕСТВА ====================

@dp.message(lambda m: m.text and m.text.lower().startswith("забрать авто") and m.from_user and is_admin(m.from_user.id) and m.reply_to_message is None)
async def seize_cars_cmd(message: types.Message):
    username = next((p[1:] for p in message.text.split() if p.startswith("@")), None)
    if not username:
        await message.answer("❌ Формат: забрать авто @никнейм")
        return
    target = db.get_user_by_username(username)
    if not target:
        await message.answer("❌ Игрок не найден")
        return
    count = db.remove_all_cars(target[0])
    db.add_log(target[0], 'seize_cars', f'{count} авто', 0, message.from_user.id)
    await message.answer(f"✅ У @{username} изъято авто: {count} шт.")
    try:
        await bot.send_message(target[0], "⚠️ Администратор изъял все ваши автомобили.")
    except Exception:
        pass

@dp.message(lambda m: m.text and m.text.lower().startswith("забрать бизнес") and m.from_user and is_admin(m.from_user.id) and m.reply_to_message is None)
async def seize_biz_cmd(message: types.Message):
    username = next((p[1:] for p in message.text.split() if p.startswith("@")), None)
    if not username:
        await message.answer("❌ Формат: забрать бизнес @никнейм")
        return
    target = db.get_user_by_username(username)
    if not target:
        await message.answer("❌ Игрок не найден")
        return
    count = db.remove_all_businesses(target[0])
    db.add_log(target[0], 'seize_businesses', f'{count} бизнесов', 0, message.from_user.id)
    await message.answer(f"✅ У @{username} изъято бизнесов: {count} шт.")
    try:
        await bot.send_message(target[0], "⚠️ Администратор изъял все ваши бизнесы.")
    except Exception:
        pass

@dp.message(lambda m: m.text and (m.text.lower().startswith("забрать недвижимость") or m.text.lower().startswith("забрать квартиру")) and m.from_user and is_admin(m.from_user.id) and m.reply_to_message is None)
async def seize_apt_cmd(message: types.Message):
    username = next((p[1:] for p in message.text.split() if p.startswith("@")), None)
    if not username:
        await message.answer("❌ Формат: забрать недвижимость @никнейм")
        return
    target = db.get_user_by_username(username)
    if not target:
        await message.answer("❌ Игрок не найден")
        return
    count = db.remove_all_apartments(target[0])
    db.add_log(target[0], 'seize_apartments', f'{count} объектов', 0, message.from_user.id)
    await message.answer(f"✅ У @{username} изъято недвижимости: {count} шт.")
    try:
        await bot.send_message(target[0], "⚠️ Администратор изъял всю вашу недвижимость.")
    except Exception:
        pass

# ==================== ВЫДАТЬ ДЕНЬГИ @USERNAME (ADMIN) ====================

@dp.message(lambda m: (
    m.text and m.from_user and is_admin(m.from_user.id) and
    m.reply_to_message is None and
    m.text.lower().startswith("выдать ") and
    "@" in m.text and
    not m.text.lower().startswith("выдать авто") and
    not m.text.lower().startswith("выдать бизнес") and
    not m.text.lower().startswith("выдать недвижимость") and
    not m.text.lower().startswith("выдать квартиру") and
    not m.text.lower().startswith("выдать работу") and
    not m.text.lower().startswith("выдать номера")
))
async def admin_give_money_username(message: types.Message):
    parts = message.text.strip().split()
    try:
        amount = int(parts[1])
        username = next(p[1:] for p in parts if p.startswith("@"))
    except Exception:
        await message.answer("❌ Формат: выдать [сумма] @никнейм")
        return
    if amount <= 0:
        await message.answer("❌ Сумма должна быть больше 0")
        return
    target = db.get_user_by_username(username)
    if not target:
        await message.answer("❌ Игрок не найден")
        return
    db.update_balance(target[0], amount)
    db.add_log(target[0], 'admin_give_money', f'admin {message.from_user.id}', amount, message.from_user.id)
    await message.answer(f"✅ Выдано {fmt(amount)} → @{username}")
    try:
        await bot.send_message(target[0], f"💰 Вам выдано {fmt(amount)} администратором.")
    except Exception:
        pass

@dp.message(lambda m: (
    m.text and m.from_user and is_admin(m.from_user.id) and
    m.reply_to_message is None and
    m.text.lower().startswith("выдать авто ")
))
async def admin_give_car_username(message: types.Message):
    parts = message.text.strip().split()
    try:
        username = next(p for p in parts if p.startswith("@"))[1:]
        car_id = int(parts[-1])
    except Exception:
        await message.answer("❌ Формат: выдать авто @ник [номер авто]")
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
    m.text and m.from_user and is_admin(m.from_user.id) and
    m.reply_to_message is None and
    m.text.lower().startswith("выдать бизнес ")
))
async def admin_give_biz_username(message: types.Message):
    parts = message.text.strip().split()
    try:
        username = next(p for p in parts if p.startswith("@"))[1:]
        # форматы: "выдать бизнес @ник 3"  или  "выдать бизнес @ник 3 номер 5"
        num_parts = [p for p in parts if p.isdigit()]
        biz_type = int(num_parts[0])
        slot = int(num_parts[1]) if len(num_parts) >= 2 else 1
    except Exception:
        await message.answer("❌ Формат: выдать бизнес @ник [тип]\nДля многослотовых: выдать бизнес @ник [тип] номер [слот]")
        return
    target = db.get_user_by_username(username)
    if not target:
        return
    data = _biz_slot_data(biz_type, slot)
    if data is None:
        await message.answer(f"❌ Бизнес №{biz_type} слот #{slot} не найден.")
        return
    biz_name, _, biz_income = data
    db_biz_id = _biz_db_id(biz_type, slot)
    db.add_business(target[0], db_biz_id, biz_name, biz_income)
    await message.answer(f"✅ @{username} получил бизнес: {biz_name}")
    try:
        await bot.send_message(target[0], f"🏢 Вам выдали бизнес: {biz_name}\n💰 Доход: {fmt(biz_income)}/день")
    except Exception:
        pass

@dp.message(lambda m: (
    m.text and m.from_user and is_admin(m.from_user.id) and
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
        await message.answer("❌ Формат: выдать недвижимость @ник [номер 1–39]")
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
    m.text and m.from_user and is_admin(m.from_user.id) and
    m.reply_to_message is None and
    m.text.lower().startswith("выдать номера ") and
    "@" in m.text
))
async def admin_give_plate_username(message: types.Message):
    parts = message.text.strip().split()
    try:
        at_idx = next(i for i, p in enumerate(parts) if p.startswith("@"))
        username = parts[at_idx][1:]
        # всё что после @ника — это номер
        plate = " ".join(parts[at_idx + 1:]).upper()
    except Exception:
        await message.answer("❌ Формат: выдать номера @ник А100МР 77")
        return
    if not plate:
        await message.answer("❌ Укажите номерной знак. Пример: выдать номера @ник А100МР 77")
        return
    target = db.get_user_by_username(username)
    if not target:
        await message.answer(f"❌ Игрок @{username} не найден.")
        return
    cars = db.get_cars_full(target[0])
    if not cars:
        await message.answer(f"❌ У @{username} нет автомобилей.")
        return
    car_without_plate = next(((cid, cname, tok, pl) for cid, cname, tok, pl in cars if not pl), None)
    target_car = car_without_plate or cars[0]
    db_car_id, car_name = target_car[0], target_car[1]
    db.update_car_plate(db_car_id, plate)
    await message.answer(
        f"✅ Номер <code>{plate}</code> выдан @{username}\n🚗 Авто: {car_name}",
        parse_mode="HTML"
    )
    try:
        await bot.send_message(target[0], f"🔢 Вам выданы номера: <code>{plate}</code>\n🚗 Авто: {car_name}", parse_mode="HTML")
    except Exception:
        pass

@dp.message(lambda m: (
    m.text and m.from_user and is_admin(m.from_user.id) and
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

@dp.message(lambda m: m.text and m.text.lower().startswith("дать ") and m.from_user and is_admin(m.from_user.id) and m.reply_to_message is None)
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
    db.add_log(target[0], 'admin_give_money', f'admin {message.from_user.id}', amount, message.from_user.id)
    await message.answer(f"✅ Выдано {fmt(amount)} → @{username}")
    try:
        await bot.send_message(target[0], f"💰 Вам выдано {fmt(amount)} администратором.")
    except Exception:
        pass

# ==================== АДМИН ОТВЕТОМ ====================

@dp.message(lambda m: (
    m.reply_to_message is not None and
    m.text is not None and
    m.from_user is not None and
    is_admin(m.from_user.id)
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
            await message.answer("❌ Формат: выдать авто [номер]")
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
            num_parts = [p for p in parts if p.isdigit()]
            biz_type = int(num_parts[0])
            slot = int(num_parts[1]) if len(num_parts) >= 2 else 1
        except Exception:
            await message.answer("❌ Формат: выдать бизнес [тип] [слот]")
            return
        data = _biz_slot_data(biz_type, slot)
        if data is None:
            await message.answer(f"❌ Бизнес №{biz_type} слот #{slot} не найден.")
            return
        biz_name, _, biz_income = data
        db_biz_id = _biz_db_id(biz_type, slot)
        db.add_business(target_id, db_biz_id, biz_name, biz_income)
        await message.answer(f"✅ @{target_user.username or target_id} получил бизнес: {biz_name}")
        try:
            await bot.send_message(target_id, f"🏢 Вам выдали бизнес: {biz_name}\n💰 Доход: {fmt(biz_income)}/день")
        except Exception:
            pass

    elif text.startswith("выдать номера"):
        # выдать номера А100МР 100
        plate_parts = parts[2:]
        if not plate_parts:
            await message.answer("❌ Формат: выдать номера А100МР 77")
            return
        plate = " ".join(plate_parts).upper()
        cars = db.get_cars_full(target_id)
        if not cars:
            await message.answer(f"❌ У @{target_user.username or target_id} нет автомобилей.")
            return
        # Назначаем на первый авто без номера, или на первый авто если все с номерами
        car_without_plate = next(((cid, cname, tok, pl) for cid, cname, tok, pl in cars if not pl), None)
        target_car = car_without_plate or cars[0]
        db_car_id, car_name = target_car[0], target_car[1]
        db.update_car_plate(db_car_id, plate)
        await message.answer(f"✅ Номер <code>{plate}</code> выдан @{target_user.username or target_id}\n🚗 Авто: {car_name}")
        try:
            await bot.send_message(target_id, f"🔢 Вам выданы номера: <code>{plate}</code>\n🚗 Авто: {car_name}")
        except Exception:
            pass

    elif text.startswith("выдать недвижимость") or text.startswith("выдать квартиру"):
        try:
            apt_id = int(parts[-1])
        except Exception:
            await message.answer("❌ Формат: выдать недвижимость [номер 1–39]")
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

    elif text.startswith("забрать авто"):
        count = db.remove_all_cars(target_id)
        db.add_log(target_id, 'seize_cars', f'{count} авто', 0, message.from_user.id)
        await message.answer(f"✅ У @{target_user.username or target_id} изъято авто: {count} шт.")
        try:
            await bot.send_message(target_id, "⚠️ Администратор изъял все ваши автомобили.")
        except Exception:
            pass

    elif text.startswith("забрать бизнес"):
        count = db.remove_all_businesses(target_id)
        db.add_log(target_id, 'seize_businesses', f'{count} бизнесов', 0, message.from_user.id)
        await message.answer(f"✅ У @{target_user.username or target_id} изъято бизнесов: {count} шт.")
        try:
            await bot.send_message(target_id, "⚠️ Администратор изъял все ваши бизнесы.")
        except Exception:
            pass

    elif text.startswith("забрать недвижимость") or text.startswith("забрать квартиру"):
        count = db.remove_all_apartments(target_id)
        db.add_log(target_id, 'seize_apartments', f'{count} объектов', 0, message.from_user.id)
        await message.answer(f"✅ У @{target_user.username or target_id} изъято недвижимости: {count} шт.")
        try:
            await bot.send_message(target_id, "⚠️ Администратор изъял всю вашу недвижимость.")
        except Exception:
            pass

    elif text.startswith("выдать") or text.startswith("дать"):
        try:
            amount = int(parts[1])
        except Exception:
            await message.answer("❌ Формат: выдать [сумма]")
            return
        db.update_balance(target_id, amount)
        db.add_log(target_id, 'admin_give_money', f'admin {message.from_user.id}', amount, message.from_user.id)
        await message.answer(f"✅ Выдано {fmt(amount)} → @{target_user.username or target_id}")
        try:
            await bot.send_message(target_id, f"💰 Вам выдано {fmt(amount)} администратором.")
        except Exception:
            pass

    elif text.startswith("снять"):
        try:
            amount = int(parts[1])
        except Exception:
            await message.answer("❌ Формат: снять [сумма]")
            return
        db.update_balance(target_id, -amount)
        db.add_log(target_id, 'admin_take_money', f'admin {message.from_user.id}', amount, message.from_user.id)
        await message.answer(f"✅ Снято {fmt(amount)} у @{target_user.username or target_id}")

    elif text.startswith("бан"):
        db.ban_user(target_id)
        await message.answer(f"✅ Игрок @{target_user.username or target_id} заблокирован")

    elif text.startswith("разбан"):
        db.unban_user(target_id)
        await message.answer(f"✅ Игрок @{target_user.username or target_id} разблокирован")

# ==================== SLASH КОМАНДЫ АДМИНА ====================

def _resolve_user_by_nick(arg: str):
    username = arg.lstrip("@")
    return db.get_user_by_username(username)

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
        "  забрать авто — изъять все авто\n"
        "  забрать бизнес — изъять все бизнесы\n"
        "  забрать недвижимость — изъять всю недвижимость\n"
        "  бан — заблокировать игрока\n"
        "  разбан — разблокировать\n"
        "  х2 вкл / х2 выкл — бонус х2\n\n"
        "━━━━ 📌 По @нику (без ответа) ━━━━\n"
        "  выдать [сумма] @ник — выдать деньги\n"
        "  выдать авто @ник [номер]\n"
        "  выдать бизнес @ник [номер]\n"
        "  выдать недвижимость @ник [номер]\n"
        "  выдать работу @ник [название]\n"
        "  дать [сумма] @ник — выдать деньги\n"
        "  забрать авто @ник\n"
        "  забрать бизнес @ник\n"
        "  забрать недвижимость @ник\n\n"
        "━━━━ 📌 Слэш-команды ━━━━\n"
        "/addmoney @ник [сумма]\n"
        "/removemoney @ник [сумма]\n"
        "/setbalance @ник [сумма]\n"
        "/ban @ник / /unban @ник\n"
        "/reset @ник — полное обнуление\n"
        "/setjob @ник [работа]\n"
        "/removejob @ник\n"
        "/addcar @ник [номер]\n"
        "/addspecialcar [id/@ник] [название]\n"
        "/setx2 @ник [1/0]\n"
        "/userinfo @ник\n"
        "/broadcast [текст]\n\n"
        "━━━━ 👑 Управление администраторами ━━━━\n"
        "добавить администратора @ник\n"
        "снять администратора @ник\n"
        "администраторы\n\n"
        "━━━━ 🚗🏢🏠 Динамический каталог ━━━━\n"
        "добавить машину\n"
        "добавить бизнес\n"
        "добавить недвижимость\n\n"
        "━━━━ 🎟 Промокоды ━━━━\n"
        "добавить промокод\n"
        "выключить промокод\n"
        "промокоды"
    )

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
    await message.answer(f"♻️ Игрок {name} полностью обнулён.")
    try:
        await bot.send_message(
            target_id,
            "♻️ Brilliant RP — Ваш аккаунт был сброшен администратором.\n"
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
        f"💰 Баланс: {fmt(balance)}\n"
        f"🏦 Банк: {fmt(bank)}\n"
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

# ==================== ПЕРЕВОД ОТВЕТОМ НА СООБЩЕНИЕ ====================

@dp.message(lambda m: (
    m.text and m.text.lower().startswith("дать ") and
    m.reply_to_message is not None and
    m.from_user is not None and
    not is_admin(m.from_user.id)
))
async def player_give_reply_cmd(message: types.Message):
    user = db.get_user(message.from_user.id)
    status = check_user(user)
    if status == "not_registered":
        await message.answer("❌ Вы не зарегистрированы. Напишите /start")
        return
    if status == "banned":
        await message.answer("⛔ Вы заблокированы.")
        return
    target_user = message.reply_to_message.from_user
    if target_user.id == message.from_user.id:
        await message.answer("❌ Нельзя переводить самому себе")
        return
    target = db.get_user(target_user.id)
    if not target:
        return
    try:
        amount = int(message.text.strip().split()[1])
    except Exception:
        await message.answer("❌ Формат: дать [сумма]")
        return
    if amount <= 0:
        await message.answer("❌ Сумма должна быть больше 0")
        return
    balance = user[4]
    if balance < amount:
        await message.answer(f"❌ Недостаточно средств. Ваш баланс: {fmt(balance)}")
        return
    db.update_balance(message.from_user.id, -amount)
    db.update_balance(target_user.id, amount)
    db.add_log(message.from_user.id, 'transfer', f'→ {target_user.id}', amount)
    sender = message.from_user.username or message.from_user.first_name
    name = target_user.username or target_user.first_name
    await message.answer(f"✅ Переведено {fmt(amount)} → {name}")
    try:
        await bot.send_message(target_user.id, f"💸 Вам перевели {fmt(amount)} от @{sender}")
    except Exception:
        pass

# ==================== ЗАПУСК ====================

def load_catalog_from_db():
    for row in db.get_catalog_items('car'):
        _, _, game_id, name, price, *_ = row
        CARS[game_id] = (name, price)
    for row in db.get_catalog_items('biz'):
        _, _, game_id, name, price, income, *_ = row
        BUSINESSES[game_id] = (name, price, income)
    for row in db.get_catalog_items('apt'):
        _, _, game_id, name, price, *_ = row
        APARTMENTS[game_id] = (name, price)

async def main():
    db.init_db()
    load_catalog_from_db()
    print("✅ Бот Brilliant RP запущен!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
