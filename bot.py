import asyncio, random, time
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config, database as db

bot = Bot(token=config.TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# === ДАННЫЕ ===

CARS = {
    1:("Honda Civic",4600),2:("BMW E28",4900),3:("Ford Transit",4500),
    4:("BMW M5 E34",5800),5:("Mercedes W140",5500),6:("Mazda RX-8",5500),
    7:("Toyota AE86",25000),8:("BMW M3 E36",12000),9:("Audi RS4",40000),
    10:("Ford Mustang",45000),11:("BMW M5 E60",38000),12:("Dodge Charger",25000),
    13:("BMW M4 F82",80000),14:("Porsche 911",192000),15:("Ferrari 458",300000),
    16:("Lamborghini Huracan",385000),17:("Bugatti Chiron",4200000),
    18:("Rolls-Royce Cullinan",1500000),19:("Koenigsegg Agera",3000000),
    20:("McLaren P1",1500000),
    # Автосалон
    101:("Koenigsegg Agera",200000000),
    102:("Range Rover Autobiography 2025",22000000),
    103:("Mercedes-Benz CLS63s AMG",5500000),
    104:("Mercedes-Benz G63 AMG",18000000),
    105:("Toyota Camry XV70",2500000),
    106:("Dodge RAM TRX",9500000),
    107:("BMW M2 G87",9000000),
    108:("BMW M8 F92",8500000),
    109:("Toyota Celica GT-Four",1000000),
    110:("Toyota Camry XV80",3750000),
    111:("Mercedes-Benz E500 W124",3300000),
}

ALL_JOBS = {
    "Механик":3200,"Строитель":3350,"Шеф-повар":3500,"Курьер":3350,
    "Таксист":3400,"Водитель автобуса":3500,"Электрик":3750,"Дальнобойщик":3850,
    "Пожарный":3700,"Врач":6000,"Хирург":8500,"Полицейский":4500,
    "Прокурор":15000,"Судья":17000,"Министр":12000,"Канцлер":20000,
}

BUSINESSES = {
    1:("Мотель",250000,15000),2:("Заправка",280000,17000),
    3:("Автосервис",300000,18500),4:("Супермаркет",1500000,49500),
    5:("McDonald's",500000,25000),6:("Парковка",400000,18000),
    7:("Шиномонтаж",65000,5000),8:("Кафе",900000,35000),
}

APARTMENTS = {
    1:("Хостел",7500),2:("1-комнатная квартира",25000),3:("Дом",50000),
    4:("Люкс апартаменты",100000),5:("Элитный пентхаус",1800000),
}

BTC_PRICE = 55000.0
PENDING_REGISTRATIONS: dict = {}

class Reg(StatesGroup):
    rp = State(); cid = State(); app = State(); src = State()

class AddPromoFSM(StatesGroup):
    code = State(); amount = State(); max_uses = State(); confirm = State()

class DisablePromoFSM(StatesGroup):
    code = State()

def f(n): return f"{int(n):,}".replace(",", ".")+"₽"
def adm(uid): return uid in config.ADMIN_IDS or db.is_db_admin(uid)
def fnd(uid): return uid in config.ADMIN_IDS
def chk(u):
    if not u: return "no"
    if u[9]: return "ban"
    return "ok"
def mget(m): return next((p[1:] for p in m.text.split() if p.startswith("@")), None)

def info_txt(u):
    uid,un,cid,gn,bal,bnk,_,job,_,_,lic,slots,x2,crd,*_ = u
    cars = db.get_cars(uid)
    bizs = db.get_businesses(uid)
    apts = db.get_apartments(uid)
    btc_bal = db.get_crypto_holding(uid, "BTC")[0]
    return (
        f"👤 {gn} (@{un})\n"
        f"🆔 CPM ID: {cid}\n"
        f"💰 Баланс: {f(bal)}\n"
        f"🏦 Банк: {f(bnk)}\n"
        f"💳 Кредит: {f(crd)}\n"
        f"₿ Bitcoin: {btc_bal:.4f} (~{f(btc_bal*BTC_PRICE)})\n"
        f"💼 Работа: {job or 'нет'}\n"
        f"🚗 Авто: {len(cars)}/{slots} | Права: {'✅' if db.has_license(uid) else '❌'}\n"
        f"🏢 Бизнесов: {len(bizs)} | 🏠 Недвижимость: {len(apts)}"
        + (" | 🔥 x2" if db.has_x2(uid) else "")
    )

def info_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💵 Баланс", callback_data="inf_bal")],
        [InlineKeyboardButton(text="🏦 Банк", callback_data="inf_bnk")],
        [InlineKeyboardButton(text="🚗 Гараж", callback_data="inf_gar")],
        [InlineKeyboardButton(text="🏢 Мои бизнесы", callback_data="inf_biz")],
        [InlineKeyboardButton(text="🏠 Недвижимость", callback_data="inf_apt")],
        [InlineKeyboardButton(text="₿ Bitcoin", callback_data="inf_btc")],
    ])

# === РЕГИСТРАЦИЯ ===

@dp.message(Command("start"))
async def cmd_start(m: types.Message, state: FSMContext):
    if db.get_user(m.from_user.id):
        await m.answer("уже зарегистрирован. напиши инфо")
        return
    await m.answer("добро пожаловать в BRILLIANT RP\n\nвведи rp имя и фамилию\nпример: Владимир Харитонов")
    await state.set_state(Reg.rp)

@dp.message(Reg.rp)
async def reg_rp(m, state):
    await state.update_data(rp=m.text.strip())
    await m.answer("введи свой id в car parking multiplayer\nпример: 123456789")
    await state.set_state(Reg.cid)

@dp.message(Reg.cid)
async def reg_cid(m, state):
    await state.update_data(cid=m.text.strip())
    await m.answer("опиши внешность персонажа\nпример: высокий, тёмные волосы, борода, спортивная одежда")
    await state.set_state(Reg.app)

@dp.message(Reg.app)
async def reg_app(m, state):
    await state.update_data(app=m.text.strip())
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="TikTok", callback_data="src_tiktok"),
        InlineKeyboardButton(text="Telegram", callback_data="src_telegram"),
        InlineKeyboardButton(text="Друг", callback_data="src_friend"),
        InlineKeyboardButton(text="Другое", callback_data="src_other"),
    ]])
    await m.answer("откуда узнал о сервере?", reply_markup=kb)
    await state.set_state(Reg.src)

@dp.callback_query(Reg.src, F.data.startswith("src_"))
async def reg_src(cb: types.CallbackQuery, state: FSMContext):
    src_map = {"src_tiktok":"TikTok","src_telegram":"Telegram","src_friend":"Друг","src_other":"Другое"}
    src = src_map.get(cb.data, "Другое")
    d = await state.get_data()
    await state.clear()
    uid = cb.from_user.id
    un = cb.from_user.username or cb.from_user.first_name
    rp, cid, app = d["rp"], d["cid"], d["app"]
    if not config.REGISTRATION_CHAT_ID:
        db.register_user(uid, un, cid, rp, app, src)
        await cb.message.edit_text(f"зарегистрирован\nимя: {rp}\nбаланс: {f(config.START_BALANCE)}\n\nнапиши инфо")
        await cb.answer()
        return
    PENDING_REGISTRATIONS[uid] = {"rp":rp,"cid":cid,"app":app,"src":src,"un":un}
    text = f"📋 Новая анкета\n@{un} (ID:{uid})\nRP: {rp}\nCPM: {cid}\nВнешность: {app}\nИсточник: {src}"
    kb2 = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Принять", callback_data=f"apr_{uid}"),
        InlineKeyboardButton(text="❌ Отклонить", callback_data=f"rjt_{uid}"),
    ]])
    try:
        kw = dict(chat_id=config.REGISTRATION_CHAT_ID, text=text, reply_markup=kb2)
        if config.REGISTRATION_TOPIC_ID: kw["message_thread_id"] = config.REGISTRATION_TOPIC_ID
        await bot.send_message(**kw)
    except Exception:
        db.register_user(uid, un, cid, rp, app, src)
        await cb.message.edit_text(f"зарегистрирован. {rp}\n{f(config.START_BALANCE)}")
        await cb.answer()
        return
    await cb.message.edit_text(f"анкета отправлена\nжди одобрения")
    await cb.answer()

@dp.callback_query(F.data.startswith("apr_"))
async def cb_apr(cb: types.CallbackQuery):
    if not adm(cb.from_user.id): await cb.answer("❌ Нет доступа", show_alert=True); return
    uid = int(cb.data.split("_")[1])
    p = PENDING_REGISTRATIONS.pop(uid, None)
    if not p: await cb.answer("Уже обработано", show_alert=True); return
    db.register_user(uid, p["un"], p["cid"], p["rp"], p["app"], p["src"])
    try: await bot.send_message(uid, f"принят. {p['rp']}\nбаланс: {f(config.START_BALANCE)}\n\nнапиши инфо")
    except: pass
    await cb.message.edit_text(cb.message.text + f"\n\n✅ @{cb.from_user.username}")
    await cb.answer("✅")

@dp.callback_query(F.data.startswith("rjt_"))
async def cb_rjt(cb: types.CallbackQuery):
    if not adm(cb.from_user.id): await cb.answer("❌", show_alert=True); return
    uid = int(cb.data.split("_")[1])
    p = PENDING_REGISTRATIONS.pop(uid, None)
    if not p: await cb.answer("Нет", show_alert=True); return
    try: await bot.send_message(uid, "отклонено. обратись к администратору")
    except: pass
    await cb.message.edit_text(cb.message.text + f"\n\n❌ @{cb.from_user.username}")
    await cb.answer("❌")

# === ПРОФИЛЬ ===

@dp.message(lambda m: m.text and m.text.lower().strip() in ["инфо", "профиль"])
async def cmd_info(m: types.Message):
    u = db.get_user(m.from_user.id)
    s = chk(u)
    if s == "no": await m.answer("❌ Вы не зарегистрированы. Напишите /start"); return
    if s == "ban": await m.answer("⛔ Вы заблокированы."); return
    await m.answer(info_txt(u), reply_markup=info_kb())

@dp.callback_query(F.data == "inf_bal")
async def cb_inf_bal(cb: types.CallbackQuery):
    u = db.get_user(cb.from_user.id)
    if not u: await cb.answer("❌", show_alert=True); return
    crd = db.get_credit(cb.from_user.id)
    await cb.answer(
        f"💵 Наличные: {f(u[4])}\n🏦 Банк: {f(u[5])}\n💳 Кредит: {f(crd)}",
        show_alert=True
    )

@dp.callback_query(F.data == "inf_bnk")
async def cb_inf_bnk(cb: types.CallbackQuery):
    u = db.get_user(cb.from_user.id)
    if not u: await cb.answer("❌", show_alert=True); return
    db.apply_bank_interest(cb.from_user.id); u = db.get_user(cb.from_user.id)
    crd = db.get_credit(cb.from_user.id)
    await cb.answer(
        f"🏦 Банк\n💵 Нал: {f(u[4])}\n🏦 Счёт: {f(u[5])}\n💳 Долг: {f(crd)}\n\nвнести / вывести / кредит / погасить",
        show_alert=True
    )

@dp.callback_query(F.data == "inf_gar")
async def cb_inf_gar(cb: types.CallbackQuery):
    u = db.get_user(cb.from_user.id)
    if not u: await cb.answer("❌", show_alert=True); return
    cars = db.get_cars_full(cb.from_user.id)
    sl = db.get_garage_slots(cb.from_user.id)
    lic = "✅" if db.has_license(cb.from_user.id) else "❌"
    if not cars:
        await cb.answer(f"🚗 Гараж пуст (0/{sl})\n🪪 Права: {lic}", show_alert=True); return
    lines = [f"🚗 Гараж ({len(cars)}/{sl}) | 🪪 {lic}"]
    for i, (_, n, tok, pl) in enumerate(cars[:8], 1):
        lines.append(f"{i}. {n} | {tok}")
    await cb.answer("\n".join(lines), show_alert=True)

@dp.callback_query(F.data == "inf_biz")
async def cb_inf_biz(cb: types.CallbackQuery):
    u = db.get_user(cb.from_user.id)
    if not u: await cb.answer("❌", show_alert=True); return
    bizs = db.get_businesses_full(cb.from_user.id)
    if not bizs:
        await cb.answer("🏢 Бизнесов нет.", show_alert=True); return
    lines = [f"🏢 Бизнесы ({len(bizs)} шт.):"]
    for _, n, inc, _ in bizs: lines.append(f"• {n} +{f(inc)}/день")
    lines.append(f"📈 Итого: {f(sum(i for _,_,i,_ in bizs))}/день")
    await cb.answer("\n".join(lines), show_alert=True)

@dp.callback_query(F.data == "inf_apt")
async def cb_inf_apt(cb: types.CallbackQuery):
    u = db.get_user(cb.from_user.id)
    if not u: await cb.answer("❌", show_alert=True); return
    apts = db.get_apartments_full(cb.from_user.id)
    if not apts:
        await cb.answer("🏠 Недвижимости нет.", show_alert=True); return
    lines = [f"🏠 Недвижимость ({len(apts)} шт.):"]
    for _, n, tok in apts: lines.append(f"• {n} | {tok}")
    await cb.answer("\n".join(lines), show_alert=True)

@dp.callback_query(F.data == "inf_btc")
async def cb_inf_btc(cb: types.CallbackQuery):
    held, _ = db.get_crypto_holding(cb.from_user.id, "BTC")
    await cb.answer(
        f"₿ Bitcoin\nКоличество: {held:.4f} BTC\nЦена: {f(BTC_PRICE)}\nСтоимость: {f(held*BTC_PRICE)}",
        show_alert=True
    )

# === БАЛАНС ===

@dp.message(lambda m: m.text and m.text.lower().strip() in ["баланс", "б"])
async def cmd_bal(m: types.Message):
    u = db.get_user(m.from_user.id)
    if not u: await m.answer("❌ Не зарегистрированы."); return
    await m.answer(f"💵 Наличные: {f(u[4])}\n🏦 Банк: {f(u[5])}\n💳 Кредит: {f(db.get_credit(m.from_user.id))}")

# === ЗАРПЛАТА ===

@dp.message(lambda m: m.text and m.text.lower().strip() in ["зарплата", "зп"] and "@" not in (m.text or ""))
async def cmd_zp(m: types.Message):
    if config.GAME_CHAT_ID and m.chat.id != config.GAME_CHAT_ID:
        await m.answer("⛔ Зарплату можно получить только в игровом чате."); return
    u = db.get_user(m.from_user.id)
    s = chk(u)
    if s != "ok": await m.answer("❌ Не зарегистрированы." if s == "no" else "⛔ Вы заблокированы."); return
    uid,_,_,_,bal,_,_,job,last_sal,*_ = u
    if not job: await m.answer("❌ У вас нет работы. Обратитесь к администратору."); return
    rem = config.SALARY_COOLDOWN - (int(time.time()) - last_sal)
    if rem > 0: await m.answer(f"⏰ Зарплата через {rem//60} мин. {rem%60} сек."); return
    sal = ALL_JOBS.get(job, 0)
    if not sal: await m.answer("❌ Работа не найдена."); return
    mult = 2 if db.has_x2(uid) else 1
    fs = sal * mult
    db.update_balance(uid, fs); db.update_salary_time(uid)
    await m.answer(f"💵 Зарплата: +{f(fs)}{' 🔥 x2' if mult==2 else ''}\n💰 Баланс: {f(bal+fs)}")

@dp.message(lambda m: m.text and m.text.lower().startswith(("зп ", "зарплата ")) and "@" in m.text and not m.text.lower().startswith(("зп бизнес","зарплата бизнес")))
async def cmd_zp_user(m: types.Message):
    un = mget(m)
    if not un: await m.answer("❌ Формат: зп @никнейм"); return
    tgt = db.get_user_by_username(un)
    if not tgt: return
    if chk(tgt) == "ban": await m.answer(f"⛔ @{un} заблокирован."); return
    uid,_,_,_,bal,_,_,job,last_sal,*_ = tgt
    if not job: await m.answer(f"❌ У @{un} нет работы."); return
    rem = config.SALARY_COOLDOWN - (int(time.time()) - last_sal)
    if rem > 0: await m.answer(f"⏰ @{un}: зарплата через {rem//60} мин. {rem%60} сек."); return
    sal = ALL_JOBS.get(job, 0)
    if not sal: await m.answer("❌ Работа не найдена."); return
    mult = 2 if db.has_x2(uid) else 1
    fs = sal * mult
    db.update_balance(uid, fs); db.update_salary_time(uid)
    await m.answer(f"💵 @{un} получил зарплату: +{f(fs)}{' 🔥 x2' if mult==2 else ''}\n💰 Баланс: {f(bal+fs)}")
    try: await bot.send_message(uid, f"💵 Вам выдали зарплату: +{f(fs)}")
    except: pass

# === ЗП БИЗНЕС @ник ===

@dp.message(lambda m: m.text and m.text.lower().startswith(("зп бизнес","зарплата бизнес")) and "@" in m.text)
async def cmd_zp_biz(m: types.Message):
    un = mget(m)
    if not un: await m.answer("❌ Формат: зп бизнес @никнейм"); return
    tgt = db.get_user_by_username(un)
    if not tgt: return
    if chk(tgt) == "ban": await m.answer(f"⛔ @{un} заблокирован."); return
    uid,_,_,_,bal,_,_,job,last_sal,*_ = tgt
    mult = 2 if db.has_x2(uid) else 1
    now = int(time.time()); total = 0; lines = []
    if job:
        sal = ALL_JOBS.get(job, 0)
        if sal:
            rem = config.SALARY_COOLDOWN - (now - last_sal)
            if rem > 0: lines.append(f"⏰ Зарплата: ещё {rem//60} мин.")
            else:
                fs = sal*mult; db.update_balance(uid, fs); db.update_salary_time(uid)
                total += fs; lines.append(f"💵 Зарплата: +{f(fs)}")
    bizs = db.get_businesses(uid)
    if bizs:
        rem = config.BIZ_COOLDOWN - (now - db.get_biz_income_time(uid))
        if rem > 0: lines.append(f"⏰ Бизнес: ещё {rem//3600} ч. {rem%3600//60} мин.")
        else:
            fi = sum(i for _,i in bizs)*mult; db.update_balance(uid, fi); db.update_biz_income_time(uid)
            total += fi; lines.append(f"🏢 Бизнес: +{f(fi)}")
    await m.answer(f"@{un}{' 🔥 x2' if mult==2 else ''}\n"+"\n".join(lines)+f"\n{'📊 Итого: +'+f(total) if total else '⚠️ Ничего не выдано'}\n💵 Баланс: {f(bal+total)}")
    if total:
        try: await bot.send_message(uid, f"💰 Вам выплачено: +{f(total)}")
        except: pass

# === БИЗНЕС @ник ===

@dp.message(lambda m: m.text and m.text.lower().startswith("бизнес ") and "@" in m.text)
async def cmd_biz_user(m: types.Message):
    un = mget(m)
    if not un: await m.answer("❌ Формат: бизнес @никнейм"); return
    tgt = db.get_user_by_username(un)
    if not tgt: return
    if chk(tgt) == "ban": await m.answer(f"⛔ @{un} заблокирован."); return
    uid,_,_,_,bal,*_ = tgt
    bizs = db.get_businesses(uid)
    if not bizs: await m.answer(f"🏢 У @{un} нет бизнесов."); return
    rem = config.BIZ_COOLDOWN - (int(time.time()) - db.get_biz_income_time(uid))
    if rem > 0: await m.answer(f"⏰ @{un}: бизнес через {rem//3600} ч. {rem%3600//60} мин."); return
    mult = 2 if db.has_x2(uid) else 1
    fi = sum(i for _,i in bizs)*mult
    db.update_balance(uid, fi); db.update_biz_income_time(uid)
    await m.answer(f"🏢 @{un} получил доход от бизнесов{' 🔥 x2' if mult==2 else ''}: +{f(fi)}\n💰 Баланс: {f(bal+fi)}")
    try: await bot.send_message(uid, f"🏢 Доход от бизнесов: +{f(fi)}")
    except: pass

# === ПЕРЕВОД ===

@dp.message(lambda m: m.text and m.text.lower().startswith("дать ") and "@" in m.text and m.reply_to_message is None and not adm(m.from_user.id if m.from_user else 0))
async def cmd_dat(m: types.Message):
    u = db.get_user(m.from_user.id)
    if chk(u) != "ok": await m.answer("❌ Не зарегистрированы." if chk(u)=="no" else "⛔ Заблокированы."); return
    parts = m.text.split()
    try:
        amt = int(parts[1])
        un = next(p[1:] for p in parts if p.startswith("@"))
    except: await m.answer("❌ Формат: дать [сумма] @никнейм"); return
    if amt <= 0: await m.answer("❌ Сумма должна быть больше 0"); return
    if u[4] < amt: await m.answer(f"❌ Недостаточно средств. Баланс: {f(u[4])}"); return
    if un.lower() == (m.from_user.username or "").lower(): await m.answer("❌ Нельзя переводить себе"); return
    tgt = db.get_user_by_username(un)
    if not tgt: return
    db.update_balance(m.from_user.id, -amt); db.update_balance(tgt[0], amt)
    db.add_log(m.from_user.id, 'transfer', f'→@{un}', amt)
    await m.answer(f"✅ Переведено {f(amt)} → @{un}")
    try: await bot.send_message(tgt[0], f"💸 Вам перевели {f(amt)} от @{m.from_user.username or m.from_user.first_name}")
    except: pass

@dp.message(lambda m: m.text and m.text.startswith("+") and len(m.text.split()) >= 2 and m.text[1:].split()[0].isdigit())
async def cmd_plus(m: types.Message):
    u = db.get_user(m.from_user.id)
    if chk(u) != "ok": return
    try:
        parts = m.text.split(); amt = int(parts[0][1:]); un = parts[1].replace("@", "")
    except: return
    if amt <= 0 or u[4] < amt: await m.answer(f"❌ Недостаточно средств. {f(u[4])}"); return
    tgt = db.get_user_by_username(un)
    if not tgt or tgt[0] == m.from_user.id: return
    db.update_balance(m.from_user.id, -amt); db.update_balance(tgt[0], amt)
    await m.answer(f"✅ {f(amt)} → @{un}")
    try: await bot.send_message(tgt[0], f"💸 {f(amt)} от @{m.from_user.username or m.from_user.first_name}")
    except: pass

# === КАЗИНО ===

@dp.message(lambda m: m.text and m.text.lower().strip() == "казино")
async def cmd_casino(m: types.Message):
    u = db.get_user(m.from_user.id)
    if chk(u) != "ok": await m.answer("❌ Не зарегистрированы." if chk(u)=="no" else "⛔ Заблокированы."); return
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="100€", callback_data="ks|100"),
         InlineKeyboardButton(text="500€", callback_data="ks|500"),
         InlineKeyboardButton(text="1 000€", callback_data="ks|1000"),
         InlineKeyboardButton(text="5 000€", callback_data="ks|5000")],
    ])
    await m.answer(f"🎰 Казино BRILLIANT RP\n💵 Баланс: {f(u[4])}\n\nВыберите ставку:", reply_markup=kb)

@dp.callback_query(F.data.startswith("ks|"))
async def cb_ks(cb: types.CallbackQuery):
    uid = cb.from_user.id
    u = db.get_user(uid)
    if not u: await cb.answer("❌", show_alert=True); return
    bet = int(cb.data.split("|")[1])
    if u[4] < bet: await cb.answer(f"❌ Нужно {f(bet)}, у вас {f(u[4])}", show_alert=True); return
    win = random.random() < 0.45
    db.update_balance(uid, bet if win else -bet)
    nb = u[4] + (bet if win else -bet)
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="100€", callback_data="ks|100"),
        InlineKeyboardButton(text="500€", callback_data="ks|500"),
        InlineKeyboardButton(text="1 000€", callback_data="ks|1000"),
        InlineKeyboardButton(text="5 000€", callback_data="ks|5000"),
    ]])
    if win:
        txt = f"🎉 Выигрыш! +{f(bet)}\n💵 Баланс: {f(nb)}"
    else:
        txt = f"💀 Проигрыш -{f(bet)}\n💵 Баланс: {f(nb)}"
    await cb.message.edit_text(txt, reply_markup=kb)
    await cb.answer("🎉" if win else "💀")

# === БИТКОИН ===

@dp.message(lambda m: m.text and m.text.lower().strip() in ["биткоин", "btc", "крипто"])
async def cmd_btc(m: types.Message):
    u = db.get_user(m.from_user.id)
    if not u: await m.answer("❌ Не зарегистрированы."); return
    held, _ = db.get_crypto_holding(m.from_user.id, "BTC")
    await m.answer(
        f"₿ Bitcoin\n"
        f"Цена: {f(BTC_PRICE)}\n"
        f"У вас: {held:.4f} BTC (~{f(held*BTC_PRICE)})\n\n"
        f"купить btc [количество] — купить\n"
        f"продать btc [количество] — продать"
    )

@dp.message(lambda m: m.text and m.text.lower().startswith("купить btc") and len(m.text.split()) >= 3)
async def cmd_buy_btc(m: types.Message):
    u = db.get_user(m.from_user.id)
    if not u: await m.answer("❌ Не зарегистрированы."); return
    try: amt = float(m.text.split()[2].replace(",", ".")); assert amt > 0
    except: await m.answer("❌ Формат: купить btc [количество]"); return
    cost = amt * BTC_PRICE
    if u[4] < cost: await m.answer(f"❌ Нужно {f(cost)}, у вас {f(u[4])}"); return
    db.update_balance(m.from_user.id, -cost)
    db.buy_crypto(m.from_user.id, "BTC", amt, BTC_PRICE)
    await m.answer(f"✅ Куплено {amt:.4f} BTC за {f(cost)}")

@dp.message(lambda m: m.text and m.text.lower().startswith("продать btc") and len(m.text.split()) >= 3)
async def cmd_sell_btc(m: types.Message):
    u = db.get_user(m.from_user.id)
    if not u: await m.answer("❌ Не зарегистрированы."); return
    try: amt = float(m.text.split()[2].replace(",", ".")); assert amt > 0
    except: await m.answer("❌ Формат: продать btc [количество]"); return
    held, _ = db.get_crypto_holding(m.from_user.id, "BTC")
    if held < amt - 1e-9: await m.answer(f"❌ У вас только {held:.4f} BTC"); return
    rcv = amt * BTC_PRICE
    db.sell_crypto(m.from_user.id, "BTC", amt)
    db.update_balance(m.from_user.id, rcv)
    await m.answer(f"✅ Продано {amt:.4f} BTC за {f(rcv)}")

# === ТОП ===

@dp.message(lambda m: m.text and m.text.lower().strip() == "топ")
async def cmd_top(m: types.Message):
    rows = db.get_top(10)
    med = ["🥇", "🥈", "🥉"]
    txt = "🏆 Топ игроков по балансу\n\n"
    for i, (un, gn, bal) in enumerate(rows, 1):
        txt += f"{med[i-1] if i<=3 else str(i)+'.'} {gn} (@{un}) — {f(bal)}\n"
    await m.answer(txt or "Пусто")

# === КУПИТЬ АВТО / БИЗНЕС / НЕДВИЖИМОСТЬ ===

@dp.message(lambda m: m.text and m.text.lower().startswith("купить авто"))
async def cmd_buy_car(m: types.Message):
    u = db.get_user(m.from_user.id)
    if chk(u) != "ok": await m.answer("❌ Не зарегистрированы." if chk(u)=="no" else "⛔ Заблокированы."); return
    try: cid = int(m.text.split()[2])
    except: await m.answer("❌ Формат: купить авто [номер]"); return
    if cid not in CARS: await m.answer(f"❌ Авто №{cid} не найдено. Доступны: 1–{max(CARS)}"); return
    cn, cp = CARS[cid]
    sl = db.get_garage_slots(m.from_user.id); cur = db.get_cars(m.from_user.id)
    if u[4] < cp: await m.answer(f"🚗 {cn}\n💰 Цена: {f(cp)}\n❌ Недостаточно средств. У вас: {f(u[4])}"); return
    if len(cur) >= sl: await m.answer(f"❌ Гараж заполнен ({len(cur)}/{sl})"); return
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Купить", callback_data=f"bc_{cid}"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="cx"),
    ]])
    await m.answer(f"🚗 {cn}\n💰 Цена: {f(cp)}\n💵 Ваш баланс: {f(u[4])}\n\nПодтвердить покупку?", reply_markup=kb)

@dp.message(lambda m: m.text and m.text.lower().startswith("купить бизнес"))
async def cmd_buy_biz(m: types.Message):
    u = db.get_user(m.from_user.id)
    if chk(u) != "ok": await m.answer("❌"); return
    try: bid = int(m.text.split()[2])
    except: await m.answer("❌ Формат: купить бизнес [номер]"); return
    if bid not in BUSINESSES: await m.answer(f"❌ Бизнес №{bid} не найден. Доступны: 1–{max(BUSINESSES)}"); return
    bn, bp, bi = BUSINESSES[bid]
    if db.get_biz_owner(bid): await m.answer("❌ Этот бизнес уже занят."); return
    if u[4] < bp: await m.answer(f"🏢 {bn}\n💰 Цена: {f(bp)}\n❌ Недостаточно средств."); return
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Купить", callback_data=f"bb_{bid}"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="cx"),
    ]])
    await m.answer(f"🏢 {bn}\n💰 Цена: {f(bp)}\n📈 Доход: {f(bi)}/день\n💵 Ваш баланс: {f(u[4])}\n\nПодтвердить?", reply_markup=kb)

@dp.message(lambda m: m.text and m.text.lower().startswith("купить недвижимость"))
async def cmd_buy_apt(m: types.Message):
    u = db.get_user(m.from_user.id)
    if chk(u) != "ok": await m.answer("❌"); return
    try: aid = int(m.text.split()[2])
    except: await m.answer("❌ Формат: купить недвижимость [номер]"); return
    if aid not in APARTMENTS: await m.answer(f"❌ №{aid} не найден. Доступны: 1–{max(APARTMENTS)}"); return
    an, ap = APARTMENTS[aid]
    if u[4] < ap: await m.answer(f"🏠 {an}\n💰 Цена: {f(ap)}\n❌ Недостаточно средств."); return
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Купить", callback_data=f"ba_{aid}"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="cx"),
    ]])
    await m.answer(f"🏠 {an}\n💰 Цена: {f(ap)}\n💵 Ваш баланс: {f(u[4])}\n\nПодтвердить?", reply_markup=kb)

@dp.callback_query(F.data.startswith("bc_"))
async def cb_bc(cb: types.CallbackQuery):
    u = db.get_user(cb.from_user.id)
    if not u: await cb.answer("❌"); return
    cid = int(cb.data.split("_")[1]); cn, cp = CARS[cid]
    if len(db.get_cars(cb.from_user.id)) >= db.get_garage_slots(cb.from_user.id):
        await cb.answer("❌ Гараж заполнен!", show_alert=True); return
    if u[4] < cp: await cb.answer(f"❌ Недостаточно средств.", show_alert=True); return
    db.update_balance(cb.from_user.id, -cp); db.add_car(cb.from_user.id, cid, cn)
    db.add_log(cb.from_user.id, 'buy_car', cn, cp)
    await cb.message.edit_text(f"🚗 Куплено!\n{cn}\n💰 Потрачено: {f(cp)}\n💵 Остаток: {f(u[4]-cp)}")
    await cb.answer("✅")

@dp.callback_query(F.data.startswith("bb_"))
async def cb_bb(cb: types.CallbackQuery):
    u = db.get_user(cb.from_user.id)
    if not u: await cb.answer("❌"); return
    bid = int(cb.data.split("_")[1]); bn, bp, bi = BUSINESSES[bid]
    if db.get_biz_owner(bid): await cb.answer("❌ Уже занят.", show_alert=True); return
    if u[4] < bp: await cb.answer("❌ Недостаточно средств.", show_alert=True); return
    db.update_balance(cb.from_user.id, -bp); db.add_business(cb.from_user.id, bid, bn, bi)
    db.add_log(cb.from_user.id, 'buy_biz', bn, bp)
    await cb.message.edit_text(f"🏢 Куплено!\n{bn}\n💰 Потрачено: {f(bp)}\n📈 Доход: {f(bi)}/день")
    await cb.answer("✅")

@dp.callback_query(F.data.startswith("ba_"))
async def cb_ba(cb: types.CallbackQuery):
    u = db.get_user(cb.from_user.id)
    if not u: await cb.answer("❌"); return
    aid = int(cb.data.split("_")[1]); an, ap = APARTMENTS[aid]
    if u[4] < ap: await cb.answer("❌ Недостаточно средств.", show_alert=True); return
    db.update_balance(cb.from_user.id, -ap); db.add_apartment(cb.from_user.id, aid, an)
    db.add_log(cb.from_user.id, 'buy_apt', an, ap)
    await cb.message.edit_text(f"🏠 Куплено!\n{an}\n💰 Потрачено: {f(ap)}")
    await cb.answer("✅")

@dp.callback_query(F.data == "cx")
async def cb_cx(cb): await cb.message.edit_text("❌ Отменено."); await cb.answer()

# === МОЁ ИМУЩЕСТВО ===

@dp.message(lambda m: m.text and m.text.lower().strip() in ["гараж", "мои авто"])
async def cmd_garage(m: types.Message):
    u = db.get_user(m.from_user.id)
    if not u: await m.answer("❌ Не зарегистрированы."); return
    cars = db.get_cars_full(m.from_user.id); sl = db.get_garage_slots(m.from_user.id)
    lic = "✅ есть" if db.has_license(m.from_user.id) else "❌ нет"
    if not cars: await m.answer(f"🚗 Гараж пуст ({len(cars)}/{sl})\n🪪 Права: {lic}\nКупить: купить авто [номер]"); return
    txt = f"🚗 Гараж ({len(cars)}/{sl}) | 🪪 Права: {lic}\n\n"
    for i, (_, n, tok, pl) in enumerate(cars, 1):
        txt += f"{i}. {n}\n   🔑 {tok} | 🔢 {pl or 'нет номеров'}\n"
    await m.answer(txt)

@dp.message(lambda m: m.text and m.text.lower().strip() in ["мои бизнесы", "бизнесы"])
async def cmd_mybiz(m: types.Message):
    u = db.get_user(m.from_user.id)
    if not u: await m.answer("❌ Не зарегистрированы."); return
    bizs = db.get_businesses_full(m.from_user.id)
    if not bizs: await m.answer("🏢 Нет бизнесов.\nКупить: купить бизнес [номер]"); return
    txt = "🏢 Мои бизнесы:\n\n"
    for _, n, inc, tok in bizs: txt += f"• {n}\n  +{f(inc)}/день | {tok}\n"
    txt += f"\n📈 Итого: {f(sum(i for _,_,i,_ in bizs))}/день"
    await m.answer(txt)

@dp.message(lambda m: m.text and m.text.lower().strip() in ["моя недвижимость", "недвижимость"])
async def cmd_myapts(m: types.Message):
    u = db.get_user(m.from_user.id)
    if not u: await m.answer("❌ Не зарегистрированы."); return
    apts = db.get_apartments_full(m.from_user.id)
    if not apts: await m.answer("🏠 Нет недвижимости.\nКупить: купить недвижимость [номер]"); return
    txt = "🏠 Моя недвижимость:\n\n"
    for _, n, tok in apts: txt += f"• {n} | {tok}\n"
    await m.answer(txt)

# === БАНК ===

def btext(uid):
    db.apply_bank_interest(uid); u = db.get_user(uid)
    crd = db.get_credit(uid)
    dep_day = config.BANK_DEPOSIT_RATE_PER_HOUR * 24 * 100
    cr_day = config.BANK_CREDIT_RATE_PER_HOUR * 24 * 100
    return (
        f"🏦 Банк BRILLIANT RP\n"
        f"💵 Наличные: {f(u[4])}\n"
        f"🏦 На счёте: {f(u[5])}\n"
        f"📉 Кредит: {f(crd)}\n"
        f"📈 Вклад: +{dep_day:.1f}%/сутки | Кредит: +{cr_day:.1f}%/сутки\n\n"
        f"внести [сумма] — положить на счёт\n"
        f"вывести [сумма] — снять со счёта\n"
        f"кредит [сумма] — взять кредит\n"
        f"погасить [сумма] — погасить кредит"
    )

@dp.message(lambda m: m.text and m.text.lower().strip() == "банк")
async def cmd_bank(m: types.Message):
    u = db.get_user(m.from_user.id)
    if not u: await m.answer("❌ Не зарегистрированы."); return
    await m.answer(btext(m.from_user.id))

@dp.message(lambda m: m.text and m.text.lower().startswith("внести "))
async def cmd_deposit(m: types.Message):
    u = db.get_user(m.from_user.id)
    if not u: return
    try: amt = int(m.text.split()[1]); assert amt > 0
    except: await m.answer("❌ Формат: внести [сумма]"); return
    db.apply_bank_interest(m.from_user.id); u = db.get_user(m.from_user.id)
    if u[4] < amt: await m.answer(f"❌ Недостаточно наличных. У вас: {f(u[4])}"); return
    db.bank_deposit(m.from_user.id, amt); await m.answer(btext(m.from_user.id))

@dp.message(lambda m: m.text and m.text.lower().startswith("вывести "))
async def cmd_withdraw(m: types.Message):
    u = db.get_user(m.from_user.id)
    if not u: return
    try: amt = int(m.text.split()[1]); assert amt > 0
    except: await m.answer("❌ Формат: вывести [сумма]"); return
    db.apply_bank_interest(m.from_user.id); u = db.get_user(m.from_user.id)
    if u[5] < amt: await m.answer(f"❌ Недостаточно на счёте. На счёте: {f(u[5])}"); return
    db.bank_withdraw(m.from_user.id, amt); await m.answer(btext(m.from_user.id))

@dp.message(lambda m: m.text and m.text.lower().startswith("кредит "))
async def cmd_credit(m: types.Message):
    u = db.get_user(m.from_user.id)
    if not u: return
    try: amt = int(m.text.split()[1]); assert amt > 0
    except: await m.answer("❌ Формат: кредит [сумма]"); return
    db.apply_bank_interest(m.from_user.id); u = db.get_user(m.from_user.id)
    crd = db.get_credit(m.from_user.id); mx = max(50000, u[4]*config.CREDIT_LIMIT_MULT)
    if crd + amt > mx: await m.answer(f"❌ Лимит кредита: {f(mx)}, уже взято: {f(crd)}"); return
    db.take_credit(m.from_user.id, amt); await m.answer(btext(m.from_user.id))

@dp.message(lambda m: m.text and m.text.lower().startswith("погасить "))
async def cmd_repay(m: types.Message):
    u = db.get_user(m.from_user.id)
    if not u: return
    try: amt = int(m.text.split()[1]); assert amt > 0
    except: await m.answer("❌ Формат: погасить [сумма]"); return
    db.apply_bank_interest(m.from_user.id); u = db.get_user(m.from_user.id)
    crd = db.get_credit(m.from_user.id)
    if crd <= 0: await m.answer("ℹ️ У вас нет долга."); return
    amt = min(amt, int(crd))
    if u[4] < amt: await m.answer(f"❌ Недостаточно наличных. У вас: {f(u[4])}"); return
    db.repay_credit(m.from_user.id, amt); await m.answer(btext(m.from_user.id))

# === ПРОМОКОД ===

@dp.message(lambda m: m.text and m.text.lower().startswith("активировать "))
async def cmd_promo(m: types.Message):
    u = db.get_user(m.from_user.id)
    if chk(u) != "ok": await m.answer("❌ Не зарегистрированы." if chk(u)=="no" else "⛔ Заблокированы."); return
    parts = m.text.strip().split(maxsplit=1)
    if len(parts) < 2: await m.answer("❌ Формат: активировать [КОД]"); return
    code = parts[1].strip().upper()
    ok, amt, reason = db.use_promo_code(m.from_user.id, code)
    if ok:
        db.update_balance(m.from_user.id, amt)
        bal = db.get_user(m.from_user.id)[4]
        await m.answer(f"✅ Промокод {code} активирован!\n💰 +{f(amt)}\n💵 Баланс: {f(bal)}")
    else:
        msgs = {"not_found":"❌ Промокод не найден.","disabled":"❌ Промокод отключён.","exhausted":"❌ Промокод исчерпан.","already_used":"❌ Вы уже использовали этот промокод."}
        await m.answer(msgs.get(reason, "❌ Ошибка."))

# === КАТАЛОГИ ===

@dp.message(lambda m: m.text and m.text.lower().strip() in ["список авто", "авто список"])
async def cmd_car_list(m: types.Message):
    txt = "🚗 Каталог авто (купить авто [номер]):\n\n"
    for cid, (cn, cp) in CARS.items(): txt += f"{cid}. {cn} — {f(cp)}\n"
    await m.answer(txt)

@dp.message(lambda m: m.text and m.text.lower().strip() in ["список бизнесов", "бизнес список"])
async def cmd_biz_list(m: types.Message):
    txt = "🏢 Каталог бизнесов (купить бизнес [номер]):\n\n"
    for bid, (bn, bp, bi) in BUSINESSES.items(): txt += f"{bid}. {bn} — {f(bp)} | +{f(bi)}/день\n"
    await m.answer(txt)

@dp.message(lambda m: m.text and m.text.lower().strip() in ["список недвижимости", "недвижимость список"])
async def cmd_apt_list(m: types.Message):
    txt = "🏠 Каталог недвижимости (купить недвижимость [номер]):\n\n"
    for aid, (an, ap) in APARTMENTS.items(): txt += f"{aid}. {an} — {f(ap)}\n"
    await m.answer(txt)

# === ПОМОЩЬ ===

@dp.message(lambda m: m.text and m.text.lower().strip() in ["помощь", "команды", "help"])
async def cmd_help(m: types.Message):
    await m.answer(
        "📋 Команды BRILLIANT RP:\n\n"
        "инфо / профиль — ваш профиль\n"
        "баланс / б — баланс\n"
        "зарплата / зп — получить зарплату\n"
        "зп @никнейм — зарплата другому\n"
        "зп бизнес @ник — зп + бизнес\n"
        "бизнес @ник — только бизнес\n"
        "дать [сумма] @ник — перевод\n"
        "+[сумма] @ник — перевод\n"
        "казино — казино\n"
        "биткоин / крипто — Bitcoin\n"
        "купить btc [кол] — купить BTC\n"
        "продать btc [кол] — продать BTC\n"
        "топ — топ игроков\n"
        "список авто — каталог авто\n"
        "список бизнесов — бизнесы\n"
        "список недвижимости — недвижимость\n"
        "купить авто [N] — купить авто\n"
        "купить бизнес [N] — купить бизнес\n"
        "купить недвижимость [N] — купить\n"
        "гараж / мои авто — мои машины\n"
        "мои бизнесы — мои бизнесы\n"
        "моя недвижимость — недвижимость\n"
        "банк — банк\n"
        "внести / вывести / кредит / погасить\n"
        "активировать [КОД] — промокод"
    )

# === ADMIN ===

@dp.message(lambda m: m.text and m.from_user and adm(m.from_user.id) and
    m.text.lower().startswith("выдать ") and "@" in m.text and m.reply_to_message is None and
    not any(m.text.lower().startswith(f"выдать {x}") for x in ["авто","бизнес","работу","недвижимость"]))
async def cmd_adm_give(m: types.Message):
    parts = m.text.strip().split()
    try:
        amt = int(parts[1])
        un = next(p[1:] for p in parts if p.startswith("@"))
    except: await m.answer("❌ Формат: выдать [сумма] @никнейм"); return
    if amt <= 0: return
    tgt = db.get_user_by_username(un)
    if not tgt: await m.answer("❌ Игрок не найден"); return
    db.update_balance(tgt[0], amt); db.add_log(tgt[0], 'give', '', amt, m.from_user.id)
    await m.answer(f"✅ Выдано {f(amt)} → @{un}")
    try: await bot.send_message(tgt[0], f"💰 Вам выдано {f(amt)} администратором.")
    except: pass

@dp.message(lambda m: m.text and m.from_user and adm(m.from_user.id) and m.text.lower().startswith("выдать работу") and "@" in m.text)
async def cmd_adm_job(m: types.Message):
    un = mget(m)
    if not un: await m.answer("❌ Формат: выдать работу [должность] @никнейм"); return
    tgt = db.get_user_by_username(un)
    if not tgt: await m.answer("❌ Игрок не найден"); return
    parts = m.text.strip().split()
    job_parts = []
    for p in parts[2:]:
        if p.startswith("@"): break
        job_parts.append(p)
    job = " ".join(job_parts)
    if not job: await m.answer("❌ Укажите должность"); return
    db.set_job(tgt[0], job)
    await m.answer(f"✅ @{un} — должность: {job}")
    try: await bot.send_message(tgt[0], f"💼 Вам выдана работа: {job}")
    except: pass

@dp.message(lambda m: m.text and m.from_user and adm(m.from_user.id) and m.text.lower().startswith("бан ") and "@" in m.text)
async def cmd_adm_ban(m: types.Message):
    un = mget(m)
    tgt = db.get_user_by_username(un) if un else None
    if not tgt: await m.answer("❌ Игрок не найден"); return
    db.ban_user(tgt[0]); await m.answer(f"⛔ @{un} заблокирован.")

@dp.message(lambda m: m.text and m.from_user and adm(m.from_user.id) and m.text.lower().startswith("разбан ") and "@" in m.text)
async def cmd_adm_unban(m: types.Message):
    un = mget(m)
    tgt = db.get_user_by_username(un) if un else None
    if not tgt: await m.answer("❌ Игрок не найден"); return
    db.unban_user(tgt[0]); await m.answer(f"✅ @{un} разблокирован.")

@dp.message(lambda m: m.text and m.from_user and adm(m.from_user.id) and m.text.lower().startswith("х2 ") and "@" in m.text)
async def cmd_adm_x2(m: types.Message):
    un = mget(m)
    tgt = db.get_user_by_username(un) if un else None
    if not tgt: await m.answer("❌ Не найден"); return
    new = not db.has_x2(tgt[0]); db.set_x2(tgt[0], new)
    await m.answer(f"{'🔥 x2 включён' if new else '🔕 x2 выключен'} — @{un}")

@dp.message(lambda m: m.text and m.from_user and adm(m.from_user.id) and m.text.lower().startswith("забрать ") and "@" in m.text)
async def cmd_adm_seize(m: types.Message):
    parts = m.text.lower().split(); what = parts[1] if len(parts) > 1 else ""; un = mget(m)
    tgt = db.get_user_by_username(un) if un else None
    if not tgt: await m.answer("❌ Не найден"); return
    if what in ["авто", "машину"]:
        n = db.remove_all_cars(tgt[0]); await m.answer(f"✅ Изъято авто у @{un}: {n} шт.")
        try: await bot.send_message(tgt[0], "⚠️ Администратор изъял ваши автомобили.")
        except: pass
    elif what in ["бизнес", "бизнесы"]:
        n = db.remove_all_businesses(tgt[0]); await m.answer(f"✅ Изъято бизнесов у @{un}: {n} шт.")
        try: await bot.send_message(tgt[0], "⚠️ Администратор изъял ваши бизнесы.")
        except: pass
    elif what in ["недвижимость", "квартиры"]:
        n = db.remove_all_apartments(tgt[0]); await m.answer(f"✅ Изъято недвижимости у @{un}: {n} шт.")
        try: await bot.send_message(tgt[0], "⚠️ Администратор изъял вашу недвижимость.")
        except: pass
    else:
        await m.answer("❌ Формат: забрать [авто/бизнес/недвижимость] @никнейм")

@dp.message(lambda m: m.text and m.from_user and adm(m.from_user.id) and m.text.lower().startswith("права ") and "@" in m.text)
async def cmd_adm_lic(m: types.Message):
    un = mget(m)
    tgt = db.get_user_by_username(un) if un else None
    if not tgt: await m.answer("❌ Не найден"); return
    new = not db.has_license(tgt[0]); db.set_license(tgt[0], new)
    await m.answer(f"{'✅ Права выданы' if new else '❌ Права изъяты'} — @{un}")

@dp.message(lambda m: m.text and m.from_user and fnd(m.from_user.id) and m.text.lower().startswith("добавить администратора") and "@" in m.text)
async def cmd_adm_add(m: types.Message):
    un = mget(m)
    tgt = db.get_user_by_username(un) if un else None
    if not tgt: await m.answer("❌ Не найден"); return
    if fnd(tgt[0]): await m.answer("❌ Уже является основателем."); return
    db.grant_admin(tgt[0], m.from_user.id)
    await m.answer(f"✅ @{un} назначен администратором.")
    try: await bot.send_message(tgt[0], "✅ Вам выданы права администратора в BRILLIANT RP.")
    except: pass

@dp.message(lambda m: m.text and m.from_user and fnd(m.from_user.id) and m.text.lower().startswith("снять администратора") and "@" in m.text)
async def cmd_adm_remove(m: types.Message):
    un = mget(m)
    tgt = db.get_user_by_username(un) if un else None
    if not tgt: await m.answer("❌ Не найден"); return
    if fnd(tgt[0]): await m.answer("❌ Нельзя снять основателя."); return
    ok = db.revoke_admin(tgt[0])
    await m.answer(f"{'✅ Права сняты' if ok else '❌ Не являлся администратором'} — @{un}")
    if ok:
        try: await bot.send_message(tgt[0], "⚠️ Ваши права администратора сняты.")
        except: pass

@dp.message(lambda m: m.text and m.from_user and adm(m.from_user.id) and m.text.lower().strip() == "администраторы")
async def cmd_adm_list(m: types.Message):
    lines = ["👑 Администраторы BRILLIANT RP:\n🔑 Основатели:"]
    for uid in config.ADMIN_IDS:
        u = db.get_user(uid)
        lines.append(f"  • @{u[1]}" if u and u[1] else f"  • ID:{uid}")
    dbadms = db.get_admins()
    if dbadms:
        lines.append("👮 Из базы данных:")
        for uid, _, _ in dbadms:
            u = db.get_user(uid)
            lines.append(f"  • @{u[1]}" if u and u[1] else f"  • ID:{uid}")
    await m.answer("\n".join(lines))

@dp.message(lambda m: m.text and m.from_user and adm(m.from_user.id) and m.text.lower().strip() == "промокоды")
async def cmd_promos(m: types.Message):
    promos = db.get_active_promos()
    if not promos: await m.answer("📋 Нет активных промокодов."); return
    txt = "🎟 Активные промокоды:\n\n"
    for code, amt, mx, used, _ in promos:
        txt += f"• {code} — {f(amt)} | {used}/{mx if mx else '∞'}\n"
    await m.answer(txt)

@dp.message(lambda m: m.text and m.from_user and adm(m.from_user.id) and m.text.lower().strip() == "добавить промокод")
async def cmd_add_promo(m: types.Message, state: FSMContext):
    await state.set_state(AddPromoFSM.code)
    await m.answer("🎟 Создание промокода\n\nВведите код (только буквы и цифры, например: PROMO50):")

@dp.message(AddPromoFSM.code)
async def promo_code(m: types.Message, state: FSMContext):
    code = m.text.strip().upper()
    if not code.replace("_","").replace("-","").isalnum():
        await m.answer("❌ Только буквы и цифры. Попробуйте снова:"); return
    await state.update_data(code=code); await state.set_state(AddPromoFSM.amount)
    await m.answer(f"Код: {code}\n\nВведите сумму награды:")

@dp.message(AddPromoFSM.amount)
async def promo_amt(m: types.Message, state: FSMContext):
    try: amt = float(m.text.replace(",",".")); assert amt > 0
    except: await m.answer("❌ Введите число:"); return
    await state.update_data(amount=amt); await state.set_state(AddPromoFSM.max_uses)
    await m.answer("Сколько раз можно использовать? (0 = неограниченно):")

@dp.message(AddPromoFSM.max_uses)
async def promo_mu(m: types.Message, state: FSMContext):
    try: mu = int(m.text.strip()); assert mu >= 0
    except: await m.answer("❌ Введите число:"); return
    await state.update_data(max_uses=mu); d = await state.get_data()
    await state.set_state(AddPromoFSM.confirm)
    await m.answer(f"Код: {d['code']}\nСумма: {f(d['amount'])}\nИспользований: {mu or '∞'}\n\nНаписать да — создать, нет — отменить")

@dp.message(AddPromoFSM.confirm)
async def promo_confirm(m: types.Message, state: FSMContext):
    if m.text.strip().lower() != "да": await state.clear(); await m.answer("❌ Отменено."); return
    d = await state.get_data()
    ok = db.add_promo_code(d['code'], d['amount'], d['max_uses'], m.from_user.id)
    await state.clear()
    await m.answer(f"✅ Промокод {d['code']} создан!" if ok else "❌ Такой промокод уже существует.")

@dp.message(lambda m: m.text and m.from_user and adm(m.from_user.id) and m.text.lower().strip() == "выключить промокод")
async def cmd_disable_promo(m: types.Message, state: FSMContext):
    await state.set_state(DisablePromoFSM.code)
    await m.answer("Введите код промокода для отключения:")

@dp.message(DisablePromoFSM.code)
async def disable_promo(m: types.Message, state: FSMContext):
    code = m.text.strip().upper(); await state.clear()
    ok = db.disable_promo_code(code)
    await m.answer(f"✅ Промокод {code} отключён." if ok else f"❌ Промокод {code} не найден.")

# === ЗАПУСК ===

def load_catalog():
    for r in db.get_catalog_items('car'):
        _,_,gid,n,p,*_=r; CARS[gid]=(n,p)
    for r in db.get_catalog_items('biz'):
        _,_,gid,n,p,inc,*_=r; BUSINESSES[gid]=(n,p,inc)
    for r in db.get_catalog_items('apt'):
        _,_,gid,n,p,*_=r; APARTMENTS[gid]=(n,p)

async def main():
    db.init_db(); load_catalog()
    print("✅ Бот BRILLIANT RP запущен!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
