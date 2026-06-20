import sqlite3, random, string, time, os
import config as _cfg

DB_PATH = os.path.join(os.path.dirname(__file__), "bot.db")

ORG_DISPLAY = {
    "ф1": ("🏎️", "Формула-1"),
    "футбол": ("⚽", "Футбол"),
    "семья": ("👨‍👩‍👧‍👦", "Семья"),
}

def _conn():
    c = sqlite3.connect(DB_PATH, check_same_thread=False)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    with _conn() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            uid INTEGER PRIMARY KEY, username TEXT, spm_id TEXT, game_name TEXT,
            balance REAL DEFAULT 550, bank REAL DEFAULT 0, btc REAL DEFAULT 0,
            job TEXT DEFAULT '', last_salary INTEGER DEFAULT 0, banned INTEGER DEFAULT 0,
            license INTEGER DEFAULT 0, garage_slots INTEGER DEFAULT 2, x2 INTEGER DEFAULT 0,
            credit REAL DEFAULT 0, bank_last_updated INTEGER DEFAULT 0,
            biz_income_time INTEGER DEFAULT 0, appearance TEXT DEFAULT '', source TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT, uid INTEGER, car_id INTEGER,
            name TEXT, token TEXT UNIQUE, plate TEXT DEFAULT NULL
        );
        CREATE TABLE IF NOT EXISTS businesses (
            id INTEGER PRIMARY KEY AUTOINCREMENT, uid INTEGER, biz_id INTEGER,
            name TEXT, income REAL, token TEXT UNIQUE
        );
        CREATE TABLE IF NOT EXISTS apartments (
            id INTEGER PRIMARY KEY AUTOINCREMENT, uid INTEGER, apt_id INTEGER,
            name TEXT, token TEXT UNIQUE
        );
        CREATE TABLE IF NOT EXISTS casino_plays (
            uid INTEGER, date TEXT, plays INTEGER DEFAULT 0, PRIMARY KEY (uid, date)
        );
        CREATE TABLE IF NOT EXISTS org_members (
            uid INTEGER, org_key TEXT, is_owner INTEGER DEFAULT 0, PRIMARY KEY (uid, org_key)
        );
        CREATE TABLE IF NOT EXISTS org_names (org_key TEXT PRIMARY KEY, name TEXT);
        CREATE TABLE IF NOT EXISTS crypto_portfolio (
            uid INTEGER, symbol TEXT, amount REAL DEFAULT 0, avg_buy_price REAL DEFAULT 0,
            PRIMARY KEY (uid, symbol)
        );
        CREATE TABLE IF NOT EXISTS promo_codes (
            code TEXT PRIMARY KEY, amount REAL NOT NULL, max_uses INTEGER DEFAULT 1,
            used_count INTEGER DEFAULT 0, active INTEGER DEFAULT 1,
            added_by INTEGER DEFAULT 0, added_at INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS promo_uses (
            uid INTEGER, code TEXT, used_at INTEGER DEFAULT 0, PRIMARY KEY (uid, code)
        );
        CREATE TABLE IF NOT EXISTS admins (
            uid INTEGER PRIMARY KEY, granted_by INTEGER DEFAULT 0,
            granted_at INTEGER DEFAULT 0, active INTEGER DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS transaction_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT, ts INTEGER NOT NULL, uid INTEGER NOT NULL,
            action TEXT NOT NULL, details TEXT DEFAULT '', amount REAL DEFAULT 0, admin_uid INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS catalog_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT, item_type TEXT NOT NULL, game_id INTEGER NOT NULL,
            name TEXT NOT NULL, price REAL NOT NULL, income REAL DEFAULT 0,
            description TEXT DEFAULT '', specs TEXT DEFAULT '', active INTEGER DEFAULT 1,
            added_by INTEGER DEFAULT 0, added_at INTEGER DEFAULT 0
        );
        """)
        for col, default in [("appearance", "''"), ("source", "''")]:
            try:
                c.execute(f"ALTER TABLE users ADD COLUMN {col} TEXT DEFAULT {default}")
            except Exception:
                pass

def _gen_token(n=6):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=n))

def gen_plate():
    letters = "АВЕКМНОРСТУХ"
    digits = "".join(random.choices(string.digits, k=4))
    region = random.choice(["77","78","50","99","47","116","161"])
    return f"{random.choice(letters)}{digits}{random.choice(letters)}{random.choice(letters)} {region}"

def _unique_token(table):
    with _conn() as c:
        for _ in range(100):
            t = _gen_token()
            if not c.execute(f"SELECT 1 FROM {table} WHERE token=?", (t,)).fetchone():
                return t
    return _gen_token(10)

def register_user(uid, username, spm_id, game_name, appearance='', source=''):
    with _conn() as c:
        c.execute("""INSERT OR REPLACE INTO users
            (uid,username,spm_id,game_name,balance,bank,btc,job,last_salary,banned,license,
             garage_slots,x2,credit,bank_last_updated,biz_income_time,appearance,source)
            VALUES (?,?,?,?,?,0,0,'',0,0,0,2,0,0,?,0,?,?)""",
            (uid, username, spm_id, game_name, _cfg.START_BALANCE, int(time.time()), appearance, source))

def get_user(uid):
    with _conn() as c:
        r = c.execute("SELECT * FROM users WHERE uid=?", (uid,)).fetchone()
        return tuple(r) if r else None

def get_user_by_username(username):
    with _conn() as c:
        r = c.execute("SELECT * FROM users WHERE LOWER(username)=LOWER(?)", (username,)).fetchone()
        return tuple(r) if r else None

def get_all_users():
    with _conn() as c:
        return [r[0] for r in c.execute("SELECT uid FROM users").fetchall()]

def get_all_users_info():
    with _conn() as c:
        return [tuple(r) for r in c.execute("SELECT uid,username,game_name FROM users").fetchall()]

def get_top(n=10):
    with _conn() as c:
        rows = c.execute("SELECT username,game_name,balance FROM users WHERE banned=0 ORDER BY balance DESC LIMIT ?", (n,)).fetchall()
        return [tuple(r) for r in rows]

def update_balance(uid, delta):
    with _conn() as c:
        c.execute("UPDATE users SET balance=balance+? WHERE uid=?", (delta, uid))

def set_balance(uid, amount):
    with _conn() as c:
        c.execute("UPDATE users SET balance=? WHERE uid=?", (amount, uid))

def update_salary_time(uid):
    with _conn() as c:
        c.execute("UPDATE users SET last_salary=? WHERE uid=?", (int(time.time()), uid))

def set_job(uid, job):
    with _conn() as c:
        c.execute("UPDATE users SET job=? WHERE uid=?", (job, uid))

def ban_user(uid):
    with _conn() as c:
        c.execute("UPDATE users SET banned=1 WHERE uid=?", (uid,))

def unban_user(uid):
    with _conn() as c:
        c.execute("UPDATE users SET banned=0 WHERE uid=?", (uid,))

def has_x2(uid):
    with _conn() as c:
        r = c.execute("SELECT x2 FROM users WHERE uid=?", (uid,)).fetchone()
        return bool(r[0]) if r else False

def set_x2(uid, v):
    with _conn() as c:
        c.execute("UPDATE users SET x2=? WHERE uid=?", (int(v), uid))

def delete_user(uid):
    with _conn() as c:
        for t in ["users","cars","businesses","apartments","casino_plays","org_members"]:
            c.execute(f"DELETE FROM {t} WHERE uid=?", (uid,))

def has_license(uid):
    with _conn() as c:
        r = c.execute("SELECT license FROM users WHERE uid=?", (uid,)).fetchone()
        return bool(r[0]) if r else False

def set_license(uid, v):
    with _conn() as c:
        c.execute("UPDATE users SET license=? WHERE uid=?", (int(v), uid))

def get_garage_slots(uid):
    with _conn() as c:
        r = c.execute("SELECT garage_slots FROM users WHERE uid=?", (uid,)).fetchone()
        return r[0] if r else 2

def update_garage_slots(uid, slots):
    with _conn() as c:
        c.execute("UPDATE users SET garage_slots=? WHERE uid=?", (slots, uid))

def add_car(uid, car_id, car_name):
    token = _unique_token("cars")
    with _conn() as c:
        c.execute("INSERT INTO cars (uid,car_id,name,token) VALUES (?,?,?,?)", (uid, car_id, car_name, token))
    return token

def get_cars(uid):
    with _conn() as c:
        return [tuple(r) for r in c.execute("SELECT id,name FROM cars WHERE uid=?", (uid,)).fetchall()]

def get_cars_full(uid):
    with _conn() as c:
        return [tuple(r) for r in c.execute("SELECT id,name,token,plate FROM cars WHERE uid=?", (uid,)).fetchall()]

def get_car_ids(uid):
    with _conn() as c:
        return [r[0] for r in c.execute("SELECT car_id FROM cars WHERE uid=?", (uid,)).fetchall()]

def get_car_by_token(token):
    with _conn() as c:
        r = c.execute("SELECT id,uid,car_id,name,token,plate FROM cars WHERE token=?", (token,)).fetchone()
        return tuple(r) if r else None

def get_car_by_dbid(db_id):
    with _conn() as c:
        r = c.execute("SELECT id,uid,car_id,name,token,plate FROM cars WHERE id=?", (db_id,)).fetchone()
        return tuple(r) if r else None

def remove_car_db(db_id):
    with _conn() as c:
        c.execute("DELETE FROM cars WHERE id=?", (db_id,))

def transfer_car(db_id, new_uid):
    with _conn() as c:
        c.execute("UPDATE cars SET uid=? WHERE id=?", (new_uid, db_id))

def update_car_plate(db_id, plate):
    with _conn() as c:
        c.execute("UPDATE cars SET plate=? WHERE id=?", (plate, db_id))

def add_business(uid, biz_id, biz_name, income):
    token = _unique_token("businesses")
    with _conn() as c:
        c.execute("INSERT INTO businesses (uid,biz_id,name,income,token) VALUES (?,?,?,?,?)", (uid, biz_id, biz_name, income, token))
    return token

def get_businesses(uid):
    with _conn() as c:
        return [tuple(r) for r in c.execute("SELECT name,income FROM businesses WHERE uid=?", (uid,)).fetchall()]

def get_businesses_full(uid):
    with _conn() as c:
        return [tuple(r) for r in c.execute("SELECT id,name,income,token FROM businesses WHERE uid=?", (uid,)).fetchall()]

def get_biz_ids(uid):
    with _conn() as c:
        return [r[0] for r in c.execute("SELECT biz_id FROM businesses WHERE uid=?", (uid,)).fetchall()]

def get_business_by_token(token):
    with _conn() as c:
        r = c.execute("SELECT id,uid,biz_id,name,income,token FROM businesses WHERE token=?", (token,)).fetchone()
        return tuple(r) if r else None

def remove_business_db(db_id):
    with _conn() as c:
        c.execute("DELETE FROM businesses WHERE id=?", (db_id,))

def transfer_business(db_id, new_uid):
    with _conn() as c:
        c.execute("UPDATE businesses SET uid=? WHERE id=?", (new_uid, db_id))

def get_biz_income_time(uid):
    with _conn() as c:
        r = c.execute("SELECT biz_income_time FROM users WHERE uid=?", (uid,)).fetchone()
        return r[0] if r else 0

def update_biz_income_time(uid):
    with _conn() as c:
        c.execute("UPDATE users SET biz_income_time=? WHERE uid=?", (int(time.time()), uid))

def add_apartment(uid, apt_id, apt_name):
    token = _unique_token("apartments")
    with _conn() as c:
        c.execute("INSERT INTO apartments (uid,apt_id,name,token) VALUES (?,?,?,?)", (uid, apt_id, apt_name, token))
    return token

def get_apartments(uid):
    with _conn() as c:
        return [tuple(r) for r in c.execute("SELECT name FROM apartments WHERE uid=?", (uid,)).fetchall()]

def get_apartments_full(uid):
    with _conn() as c:
        return [tuple(r) for r in c.execute("SELECT id,name,token FROM apartments WHERE uid=?", (uid,)).fetchall()]

def get_apt_ids(uid):
    with _conn() as c:
        return [r[0] for r in c.execute("SELECT apt_id FROM apartments WHERE uid=?", (uid,)).fetchall()]

def get_apartment_by_token(token):
    with _conn() as c:
        r = c.execute("SELECT id,uid,apt_id,name,token FROM apartments WHERE token=?", (token,)).fetchone()
        return tuple(r) if r else None

def remove_apartment_db(db_id):
    with _conn() as c:
        c.execute("DELETE FROM apartments WHERE id=?", (db_id,))

def transfer_apartment(db_id, new_uid):
    with _conn() as c:
        c.execute("UPDATE apartments SET uid=? WHERE id=?", (new_uid, db_id))

def apply_bank_interest(uid):
    with _conn() as c:
        r = c.execute("SELECT bank,credit,bank_last_updated FROM users WHERE uid=?", (uid,)).fetchone()
        if not r: return
        bank, credit, last = r
        now = int(time.time())
        if last == 0:
            c.execute("UPDATE users SET bank_last_updated=? WHERE uid=?", (now, uid))
            return
        hrs = (now - last) / 3600.0
        if hrs < 0.01: return
        nb = bank * ((1 + _cfg.BANK_DEPOSIT_RATE_PER_HOUR) ** hrs)
        nc = credit * ((1 + _cfg.BANK_CREDIT_RATE_PER_HOUR) ** hrs) if credit > 0 else 0
        c.execute("UPDATE users SET bank=?,credit=?,bank_last_updated=? WHERE uid=?", (nb, nc, now, uid))

def bank_deposit(uid, amount):
    with _conn() as c:
        c.execute("UPDATE users SET balance=balance-?,bank=bank+? WHERE uid=?", (amount, amount, uid))

def bank_withdraw(uid, amount):
    with _conn() as c:
        c.execute("UPDATE users SET bank=bank-?,balance=balance+? WHERE uid=?", (amount, amount, uid))

def get_credit(uid):
    with _conn() as c:
        r = c.execute("SELECT credit FROM users WHERE uid=?", (uid,)).fetchone()
        return r[0] if r else 0

def take_credit(uid, amount):
    with _conn() as c:
        c.execute("UPDATE users SET credit=credit+?,balance=balance+? WHERE uid=?", (amount, amount, uid))

def repay_credit(uid, amount):
    with _conn() as c:
        c.execute("UPDATE users SET credit=MAX(0,credit-?),balance=balance-? WHERE uid=?", (amount, amount, uid))

def get_casino_plays(uid, date):
    with _conn() as c:
        r = c.execute("SELECT plays FROM casino_plays WHERE uid=? AND date=?", (uid, date)).fetchone()
        return r[0] if r else 0

def increment_casino_plays(uid, date):
    with _conn() as c:
        c.execute("INSERT INTO casino_plays (uid,date,plays) VALUES (?,?,1) ON CONFLICT(uid,date) DO UPDATE SET plays=plays+1", (uid, date))

def add_org_member(uid, org_key, is_owner):
    with _conn() as c:
        c.execute("INSERT INTO org_members (uid,org_key,is_owner) VALUES (?,?,?) ON CONFLICT(uid,org_key) DO UPDATE SET is_owner=excluded.is_owner", (uid, org_key, int(is_owner)))

def remove_org_member(uid, org_key):
    with _conn() as c:
        c.execute("DELETE FROM org_members WHERE uid=? AND org_key=?", (uid, org_key))

def get_user_orgs(uid):
    with _conn() as c:
        return [(r[0], bool(r[1])) for r in c.execute("SELECT org_key,is_owner FROM org_members WHERE uid=?", (uid,)).fetchall()]

def get_org_members(org_key):
    with _conn() as c:
        return [(r[0], bool(r[1])) for r in c.execute("SELECT uid,is_owner FROM org_members WHERE org_key=?", (org_key,)).fetchall()]

def set_org_name(org_key, name):
    with _conn() as c:
        c.execute("INSERT INTO org_names (org_key,name) VALUES (?,?) ON CONFLICT(org_key) DO UPDATE SET name=excluded.name", (org_key, name))

def get_org_name(org_key):
    with _conn() as c:
        r = c.execute("SELECT name FROM org_names WHERE org_key=?", (org_key,)).fetchone()
        if r: return r[0]
        _, default = ORG_DISPLAY.get(org_key, ("", org_key))
        return default

def get_crypto_portfolio(uid):
    with _conn() as c:
        return [(r[0], r[1], r[2]) for r in c.execute("SELECT symbol,amount,avg_buy_price FROM crypto_portfolio WHERE uid=? AND amount>0", (uid,)).fetchall()]

def get_crypto_holding(uid, symbol):
    with _conn() as c:
        r = c.execute("SELECT amount,avg_buy_price FROM crypto_portfolio WHERE uid=? AND symbol=?", (uid, symbol)).fetchone()
        return (r[0], r[1]) if r else (0.0, 0.0)

def buy_crypto(uid, symbol, amount, price):
    with _conn() as c:
        r = c.execute("SELECT amount,avg_buy_price FROM crypto_portfolio WHERE uid=? AND symbol=?", (uid, symbol)).fetchone()
        if r:
            na = r[0] + amount
            np = (r[0]*r[1] + amount*price) / na if na > 0 else price
            c.execute("UPDATE crypto_portfolio SET amount=?,avg_buy_price=? WHERE uid=? AND symbol=?", (na, np, uid, symbol))
        else:
            c.execute("INSERT INTO crypto_portfolio (uid,symbol,amount,avg_buy_price) VALUES (?,?,?,?)", (uid, symbol, amount, price))

def sell_crypto(uid, symbol, amount):
    with _conn() as c:
        r = c.execute("SELECT amount,avg_buy_price FROM crypto_portfolio WHERE uid=? AND symbol=?", (uid, symbol)).fetchone()
        if not r or r[0] < amount - 1e-9: return False
        c.execute("UPDATE crypto_portfolio SET amount=? WHERE uid=? AND symbol=?", (max(0.0, r[0]-amount), uid, symbol))
        return True

def is_db_admin(uid):
    with _conn() as c:
        return bool(c.execute("SELECT 1 FROM admins WHERE uid=? AND active=1", (uid,)).fetchone())

def grant_admin(uid, granted_by):
    with _conn() as c:
        c.execute("INSERT OR REPLACE INTO admins (uid,granted_by,granted_at,active) VALUES (?,?,?,1)", (uid, granted_by, int(time.time())))

def revoke_admin(uid):
    with _conn() as c:
        c.execute("UPDATE admins SET active=0 WHERE uid=? AND active=1", (uid,))
        return bool(c.execute("SELECT changes()").fetchone()[0])

def get_admins():
    with _conn() as c:
        return [tuple(r) for r in c.execute("SELECT uid,granted_by,granted_at FROM admins WHERE active=1").fetchall()]

def add_log(uid, action, details='', amount=0, admin_uid=0):
    with _conn() as c:
        c.execute("INSERT INTO transaction_logs (ts,uid,action,details,amount,admin_uid) VALUES (?,?,?,?,?,?)", (int(time.time()), uid, action, details, float(amount), admin_uid))

def get_biz_owner(biz_id):
    with _conn() as c:
        r = c.execute("SELECT uid FROM businesses WHERE biz_id=?", (biz_id,)).fetchone()
        return r[0] if r else None

def remove_all_cars(uid):
    with _conn() as c:
        n = c.execute("SELECT COUNT(*) FROM cars WHERE uid=?", (uid,)).fetchone()[0]
        c.execute("DELETE FROM cars WHERE uid=?", (uid,))
        return n

def remove_all_businesses(uid):
    with _conn() as c:
        n = c.execute("SELECT COUNT(*) FROM businesses WHERE uid=?", (uid,)).fetchone()[0]
        c.execute("DELETE FROM businesses WHERE uid=?", (uid,))
        return n

def remove_all_apartments(uid):
    with _conn() as c:
        n = c.execute("SELECT COUNT(*) FROM apartments WHERE uid=?", (uid,)).fetchone()[0]
        c.execute("DELETE FROM apartments WHERE uid=?", (uid,))
        return n

def add_catalog_item(item_type, game_id, name, price, income=0, description='', specs='', added_by=0):
    with _conn() as c:
        c.execute("INSERT INTO catalog_items (item_type,game_id,name,price,income,description,specs,added_by,added_at) VALUES (?,?,?,?,?,?,?,?,?)",
            (item_type, game_id, name, price, income, description, specs, added_by, int(time.time())))

def get_catalog_items(item_type):
    with _conn() as c:
        return [tuple(r) for r in c.execute("SELECT id,item_type,game_id,name,price,income,description,specs FROM catalog_items WHERE item_type=? AND active=1", (item_type,)).fetchall()]

def add_promo_code(code, amount, max_uses, added_by):
    with _conn() as c:
        try:
            c.execute("INSERT INTO promo_codes (code,amount,max_uses,added_by,added_at) VALUES (?,?,?,?,?)",
                (code.upper(), float(amount), int(max_uses), added_by, int(time.time())))
            return True
        except Exception:
            return False

def disable_promo_code(code):
    with _conn() as c:
        c.execute("UPDATE promo_codes SET active=0 WHERE code=?", (code.upper(),))
        return c.execute("SELECT changes()").fetchone()[0] > 0

def get_active_promos():
    with _conn() as c:
        return [tuple(r) for r in c.execute("SELECT code,amount,max_uses,used_count,added_at FROM promo_codes WHERE active=1 ORDER BY added_at DESC").fetchall()]

def use_promo_code(uid, code):
    code = code.upper()
    with _conn() as c:
        p = c.execute("SELECT code,amount,max_uses,used_count,active FROM promo_codes WHERE code=?", (code,)).fetchone()
        if not p: return False, 0.0, "not_found"
        if not p[4]: return False, 0.0, "disabled"
        if p[2] > 0 and p[3] >= p[2]: return False, 0.0, "exhausted"
        if c.execute("SELECT 1 FROM promo_uses WHERE uid=? AND code=?", (uid, code)).fetchone():
            return False, 0.0, "already_used"
        c.execute("INSERT INTO promo_uses (uid,code,used_at) VALUES (?,?,?)", (uid, code, int(time.time())))
        c.execute("UPDATE promo_codes SET used_count=used_count+1 WHERE code=?", (code,))
        return True, float(p[1]), "ok"

init_db()
