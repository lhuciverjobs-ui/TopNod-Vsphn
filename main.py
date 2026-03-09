import requests
import time
import json
import logging
import sys
from datetime import datetime
from config_ui import UI, WALLET_TAB_MAP, DELAY

# ============================================================
# KONFIGURASI
# ============================================================

EMAIL        = "@gmail.com"
PASSWORD_MD5 = "--"
BASE         = "https://api.vsphone.com/vsphone/api"
TARGET_PKG   = "com.ant.dt.topnod"

POLL_WAIT       = 3
INSTALL_TIMEOUT = 20
LAUNCH_WAIT     = 20

REFERRAL_CODE   = "ISIREF"
WALLET_PASSWORD = "masuk123"
EXCLUDE_DEVICES = {"ACP250929NBUC1VX"}
OTP_TIMEOUT     = 180

# ============================================================
# WARNA & TAMPILAN CLI
# ============================================================

class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"

    BLACK  = "\033[30m"
    RED    = "\033[31m"
    GREEN  = "\033[32m"
    YELLOW = "\033[33m"
    BLUE   = "\033[34m"
    PURPLE = "\033[35m"
    CYAN   = "\033[36m"
    WHITE  = "\033[37m"

    BG_BLACK  = "\033[40m"
    BG_BLUE   = "\033[44m"
    BG_PURPLE = "\033[45m"
    BG_CYAN   = "\033[46m"


W = 58  # lebar box

def box_top(title: str = "", color: str = C.CYAN):
    if title:
        pad   = W - len(title) - 4
        left  = pad // 2
        right = pad - left
        print(f"{color}{C.BOLD}╔{'═' * (left+1)} {title} {'═' * (right+1)}╗{C.RESET}")
    else:
        print(f"{color}{C.BOLD}╔{'═' * (W+2)}╗{C.RESET}")

def box_mid(text: str = "", color: str = C.CYAN, text_color: str = C.WHITE):
    inner = f"  {text}"
    pad   = W - len(_strip_ansi(inner))
    print(f"{color}{C.BOLD}║{C.RESET}{text_color}{inner}{' ' * max(pad, 0)}{C.RESET}{color}{C.BOLD}║{C.RESET}")

def box_sep(color: str = C.CYAN):
    print(f"{color}{C.BOLD}╠{'═' * (W+2)}╣{C.RESET}")

def box_bot(color: str = C.CYAN):
    print(f"{color}{C.BOLD}╚{'═' * (W+2)}╝{C.RESET}")

def box_line(color: str = C.CYAN):
    print(f"{color}{'─' * (W+4)}{C.RESET}")

def _strip_ansi(s: str) -> str:
    import re
    return re.sub(r"\033\[[0-9;]*m", "", s)

def tag_ok(msg: str)   -> str: return f"{C.GREEN}✔{C.RESET}  {msg}"
def tag_err(msg: str)  -> str: return f"{C.RED}✘{C.RESET}  {msg}"
def tag_warn(msg: str) -> str: return f"{C.YELLOW}⚠{C.RESET}  {msg}"
def tag_info(msg: str) -> str: return f"{C.CYAN}›{C.RESET}  {msg}"
def tag_wait(msg: str) -> str: return f"{C.YELLOW}◷{C.RESET}  {msg}"
def tag_run(msg: str)  -> str: return f"{C.PURPLE}⟳{C.RESET}  {msg}"

def print_ok(msg: str):   print(f"  {tag_ok(msg)}")
def print_err(msg: str):  print(f"  {tag_err(msg)}")
def print_warn(msg: str): print(f"  {tag_warn(msg)}")
def print_info(msg: str): print(f"  {tag_info(msg)}")
def print_wait(msg: str): print(f"  {tag_wait(msg)}")
def print_run(msg: str):  print(f"  {tag_run(msg)}")

def section(title: str):
    print()
    print(f"  {C.BOLD}{C.CYAN}▸ {title}{C.RESET}")
    print(f"  {C.DIM}{'─' * (W - 2)}{C.RESET}")

def countdown(seconds: int, label: str = "Melanjutkan dalam"):
    for i in range(seconds, 0, -5):
        print(f"\r  {C.YELLOW}◷{C.RESET}  {label} {C.BOLD}{i}s{C.RESET}...   ", end="", flush=True)
        time.sleep(min(5, i))
    print(f"\r  {C.GREEN}✔{C.RESET}  {label} {C.BOLD}0s{C.RESET}    ")

def banner():
    print()
    box_top("TopNod Auto Wallet Bot", C.CYAN)
    box_mid(f"{C.DIM}vsphone.com  ·  v1.0  ·  resolusi 1080×1920{C.RESET}", C.CYAN, "")
    box_bot(C.CYAN)
    print()

# ============================================================
# LOGGING (file only — console pakai print cantik di atas)
# ============================================================

from logging.handlers import RotatingFileHandler
import glob, os

_old_logs = sorted(glob.glob("topnod_log_*.txt"))
for _f in _old_logs[:-4]:
    try: os.remove(_f)
    except Exception: pass

log_filename = f"topnod_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
_fmt          = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
_file_handler = RotatingFileHandler(log_filename, maxBytes=2*1024*1024, backupCount=3, encoding="utf-8")
_file_handler.setFormatter(_fmt)

# Console handler hanya tampilkan WARNING ke atas di terminal (biar tidak kotor)
_con_handler = logging.StreamHandler(sys.stdout)
_con_handler.setFormatter(_fmt)
_con_handler.setLevel(logging.WARNING)

logging.basicConfig(level=logging.INFO, handlers=[_file_handler, _con_handler])
log = logging.getLogger(__name__)

# ============================================================
# SESSION & HEADERS
# ============================================================

session = requests.Session()
headers = {
    "Content-Type":  "application/json",
    "Clienttype":    "web",
    "Appversion":    "2003702",
    "Requestsource": "wechat-miniapp",
    "Suppliertype":  "0"
}

# ============================================================
# STEP 1 — LOGIN
# ============================================================

def login():
    section("Login")
    r    = session.post(
        f"{BASE}/user/login",
        json={"mobilePhone": EMAIL, "loginType": 1,
              "password": PASSWORD_MD5, "channel": "web"},
        headers=headers, timeout=15
    )
    data = r.json()
    if data.get("code") != 200:
        print_err(f"Login gagal: {data.get('msg')}")
        raise Exception(f"Login gagal: {data.get('msg')}")
    token   = data["data"]["token"]
    user_id = str(data["data"]["userId"])
    headers["token"]  = token
    headers["userid"] = user_id
    log.info(f"Login OK — UserID: {user_id}")
    print_ok(f"Login berhasil  {C.DIM}UserID: {user_id}{C.RESET}")

# ============================================================
# STEP 2 — GET DEVICES
# ============================================================

def get_devices():
    section("Mengambil daftar device")
    r      = session.get(
        f"{BASE}/userEquipment/list",
        params={"supplierType": -1, "queryAuthorizedEquipments": "true"},
        headers=headers, timeout=15
    )
    data    = r.json()
    groups  = data.get("data", [])
    devices = []
    for g in groups:
        for p in g.get("userPads", []):
            d = {
                "id":      str(p.get("equipmentId")),
                "name":    p.get("equipmentName", str(p.get("equipmentId"))),
                "padCode": p.get("padCode"),
            }
            devices.append(d)
            log.info(f"Device: {d['name']}  padCode={d['padCode']}")
            print_info(f"{C.BOLD}{d['name']}{C.RESET}  {C.DIM}{d['padCode']}{C.RESET}")
    print_ok(f"Total {C.BOLD}{len(devices)}{C.RESET} device ditemukan")
    return devices

# ============================================================
# STEP 3 — CEK TOPNOD TERINSTALL
# ============================================================

def check_installed(devices: list) -> set:
    section("Cek TopNod terinstall")
    try:
        r        = session.post(
            f"{BASE}/pcVersion/getListInstalledApp",
            json={"padCodeList": [d["padCode"] for d in devices]},
            headers=headers, timeout=15
        )
        data     = r.json()
        app_list = data.get("data", [])

        installed_pads = set()
        if isinstance(app_list, list):
            installed_pads = {
                a.get("padCode") for a in app_list
                if a.get("packageName") == TARGET_PKG or
                   a.get("apkPackageName") == TARGET_PKG
            }
        elif isinstance(app_list, dict):
            for pad_code, apps in app_list.items():
                if isinstance(apps, list):
                    for a in apps:
                        if a.get("packageName") == TARGET_PKG:
                            installed_pads.add(pad_code)

        for d in devices:
            if d["padCode"] in installed_pads:
                print_ok(f"{d['name']}  {C.DIM}sudah terinstall{C.RESET}")
            else:
                print_info(f"{d['name']}  {C.YELLOW}perlu install{C.RESET}")
        return installed_pads
    except Exception as e:
        log.warning(f"cek install error: {e}")
        print_warn(f"Cek install gagal — akan install ke semua device")
        return set()

# ============================================================
# STEP 4 — INSTALL APK
# ============================================================

def get_topnod_apk():
    section("Mencari APK TopNod di cloud storage")
    for op in [2, 1, 3, None]:
        params = {"operType": op} if op is not None else {}
        r      = session.post(
            f"{BASE}/cloudFile/selectFilesByUserId",
            params=params, json={},
            headers=headers, timeout=15
        )
        files = r.json().get("data") or []
        apks  = [f for f in files if f.get("fileType") == 2]
        for f in apks:
            if "topnod" in f.get("fileName", "").lower():
                log.info(f"APK found: {f['fileName']}  id={f['fileId']}")
                print_ok(f"APK ditemukan: {C.BOLD}{f['fileName']}{C.RESET}  {C.DIM}id={f['fileId']}{C.RESET}")
                return f
        if apks:
            print_warn(f"Tidak ada APK bernama topnod. APK tersedia ({len(apks)}):")
            for i, f in enumerate(apks, 1):
                size_mb = round(f.get("fileSize", 0) / 1024 / 1024, 1)
                print(f"    {C.CYAN}{i}.{C.RESET}  {f['fileName']}  {C.DIM}({size_mb} MB)  id={f['fileId']}{C.RESET}")
            return apks
    return None

def install_to_devices(devices: list, apk_info: dict) -> dict:
    section(f"Install APK → {len(devices)} device")
    task_list = [{
        "taskType":    10000,
        "padCode":     d["padCode"],
        "equipmentId": d["id"],
        "taskContent": json.dumps({
            "downloadUrl": apk_info["downloadUrl"],
            "fileName":    apk_info["fileName"],
            "fileType":    2,
            "fileId":      apk_info.get("fileId", 0)
        })
    } for d in devices]
    r    = session.post(
        f"{BASE}/padTask/addPadTaskByJiGuang",
        json={"taskList": task_list},
        headers=headers, timeout=30
    )
    data = r.json()
    if data.get("code") != 200:
        raise Exception(f"addPadTask gagal: {data.get('msg')}")
    tasks    = data.get("data", [])
    task_map = {}
    for t in tasks:
        tid = t["taskId"]
        task_map[tid] = {
            "taskId":  tid,
            "padCode": t["padCode"],
            "name":    next((d["name"] for d in devices
                             if d["padCode"] == t["padCode"]), t["padCode"]),
        }
        print_info(f"Task {C.DIM}{tid}{C.RESET} → {task_map[tid]['name']}")
    return task_map

def poll_tasks(task_map: dict) -> dict:
    print_wait(f"Memantau install  {C.DIM}(timeout {INSTALL_TIMEOUT}s){C.RESET}")
    STATUS_LABELS = {0: "Pending", 1: "Running", 2: "Sukses", 3: "Gagal", 4: "Skip"}
    STATUS_COLORS = {0: C.DIM, 1: C.YELLOW, 2: C.GREEN, 3: C.RED, 4: C.CYAN}
    done_ids   = set()
    results    = {}
    start_time = time.time()
    while True:
        pending = [tid for tid in task_map if tid not in done_ids]
        if not pending:
            print_ok("Semua install task selesai"); break
        if time.time() - start_time >= INSTALL_TIMEOUT:
            print_warn("Timeout install — lanjut otomatis")
            for tid in pending:
                results[tid] = {"name": task_map[tid]["name"], "success": True, "msg": "Timeout"}
            break
        try:
            r     = session.post(f"{BASE}/padTask/getPadTaskByTaskIds",
                                 json={"taskIds": pending}, headers=headers, timeout=15)
            tasks = r.json().get("data", [])
        except Exception as e:
            log.warning(f"Poll error: {e}"); time.sleep(POLL_WAIT); continue
        for t in tasks:
            tid, status = t["taskId"], t.get("status", 0)
            msg  = t.get("taskMsg", "") or ""
            prog = t.get("taskProgress", "")
            name = task_map[tid]["name"]
            col  = STATUS_COLORS.get(status, C.WHITE)
            lbl  = STATUS_LABELS.get(status, f"Status {status}")
            if status in (2, 3, 4):
                done_ids.add(tid)
                results[tid] = {"name": name, "success": status == 2, "msg": msg or lbl}
                sym = "✔" if status == 2 else "✘"
                print(f"  {col}{sym}{C.RESET}  {name}  {col}{lbl}{C.RESET}{f'  {C.DIM}{msg}{C.RESET}' if msg else ''}")
            else:
                sisa = max(0, INSTALL_TIMEOUT - (time.time() - start_time))
                prog_str = f" {prog}%" if prog else ""
                print(f"  {col}◷{C.RESET}  {name}  {col}{lbl}{prog_str}{C.RESET}  {C.DIM}{sisa:.0f}s{C.RESET}", end="\r")
        if len(task_map) - len(done_ids) > 0:
            time.sleep(POLL_WAIT)
    return results

# ============================================================
# STEP 5 — LAUNCH APP
# ============================================================

def launch_app(devices: list) -> dict:
    section(f"Launch TopNod — {len(devices)} device")
    pad_code_list = [d["padCode"] for d in devices]
    try:
        r    = session.post(f"{BASE}/pcVersion/restartApp",
                            json={"padCodeList": pad_code_list, "apkPackageList": [TARGET_PKG]},
                            headers=headers, timeout=15)
        d    = r.json()
        code = d.get("code")
        log.info(f"restartApp code={code}")
        if code == 200:
            print_ok("TopNod berhasil diluncurkan")
            return {dev["name"]: {"success": True} for dev in devices}
    except Exception as e:
        log.warning(f"restartApp Exception: {e}")
    print_err("Launch gagal")
    return {dev["name"]: {"success": False} for dev in devices}

# ============================================================
# vcAdb — Kirim ADB command
# ============================================================

VCADB_ASYNC  = f"{BASE}/vcAdb/asyncAdb"
VCADB_RESULT = f"{BASE}/vcAdb/getAdbResult"

def vcadb_exec(pad_codes: list, adb_str: str, poll_timeout: int = 30) -> dict:
    log.info(f"vcAdb → {adb_str[:80]}...")
    r = session.post(VCADB_ASYNC,
                     json={"padCodes": pad_codes, "adbStr": adb_str},
                     headers=headers, timeout=15)
    d = r.json()
    if d.get("code") != 200:
        log.warning(f"asyncAdb gagal: {d}")
        return {}

    base_task_id = d["data"]
    deadline     = time.time() + poll_timeout
    while time.time() < deadline:
        time.sleep(2)
        r2   = session.post(VCADB_RESULT,
                            json={"baseTaskId": base_task_id},
                            headers=headers, timeout=15)
        d2   = r2.json()
        data = d2.get("data", "")
        if not data:
            continue
        try:
            results = json.loads(data) if isinstance(data, str) else data
            done    = {item["padCode"]: item["taskStatus"] for item in results}
            if not [pc for pc in pad_codes if pc not in done]:
                return done
        except Exception as e:
            log.warning(f"Parse result error: {e}")
    log.warning(f"vcAdb timeout {poll_timeout}s")
    return {}

# ============================================================
# LOGOUT ALL
# ============================================================

LOGOUT_WAIT = 5

def logout_all(devices: list):
    """Tap Log out → Confirm di semua device sekaligus."""
    section(f"Logout — {len(devices)} device")
    pad_codes = [d["padCode"] for d in devices]
    lx, ly   = UI["logout_btn"]
    cx, cy   = UI["logout_confirm"]
    cmd = f"input tap {lx} {ly} && sleep 2 && input tap {cx} {cy}"
    results  = vcadb_exec(pad_codes, cmd, poll_timeout=30)
    ok = sum(1 for v in results.values() if v == 3)
    print_ok(f"Logout selesai  {C.DIM}{ok}/{len(devices)} device OK{C.RESET}")
    log.info(f"Logout: {ok}/{len(devices)} OK")
    countdown(LOGOUT_WAIT, "Tunggu device logout")

# ============================================================
# MAILTM — Email temporer otomatis
# ============================================================

MAILTM_API  = "https://api.mail.tm"
MAILTM_PASS = "zays12345"

class MailTM:
    def __init__(self):
        self.address  = None
        self.token    = None
        self.s        = requests.Session()
        self.seen_ids = set()

    def create_account(self) -> bool:
        import random, string
        try:
            r       = self.s.get(f"{MAILTM_API}/domains", timeout=10)
            domains = r.json().get("hydra:member", [])
            if not domains:
                return False
            domain = domains[0]["domain"]
        except Exception as e:
            log.error(f"MailTM domain error: {e}")
            return False

        username     = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
        self.address = f"{username}@{domain}"
        try:
            r = self.s.post(f"{MAILTM_API}/accounts",
                            json={"address": self.address, "password": MAILTM_PASS},
                            timeout=10)
            if r.status_code == 429:
                time.sleep(10)
                r = self.s.post(f"{MAILTM_API}/accounts",
                                json={"address": self.address, "password": MAILTM_PASS},
                                timeout=10)
            if r.status_code not in (200, 201):
                log.error(f"MailTM create {r.status_code}: {r.text[:80]}")
                return False
            log.info(f"MailTM OK: {self.address}")
            return True
        except Exception as e:
            log.error(f"MailTM create exception: {e}")
            return False

    def get_token(self) -> bool:
        try:
            r          = self.s.post(f"{MAILTM_API}/token",
                                     json={"address": self.address, "password": MAILTM_PASS},
                                     timeout=10)
            self.token = r.json().get("token")
            return bool(self.token)
        except Exception as e:
            log.error(f"MailTM token error: {e}")
            return False

    def wait_for_otp(self, timeout: int = 180) -> str | None:
        import re
        if not self.token and not self.get_token():
            return None
        auth     = {"Authorization": f"Bearer {self.token}"}
        deadline = time.time() + timeout
        log.info(f"MailTM polling OTP: {self.address}")
        while time.time() < deadline:
            time.sleep(5)
            try:
                r        = self.s.get(f"{MAILTM_API}/messages", headers=auth, timeout=10)
                msgs     = r.json().get("hydra:member", [])
                new_msgs = [m for m in msgs if m["id"] not in self.seen_ids]
                for msg in new_msgs:
                    mid  = msg["id"]
                    r2   = self.s.get(f"{MAILTM_API}/messages/{mid}", headers=auth, timeout=10)
                    body = r2.json().get("text", "") or r2.json().get("html", "") or ""
                    m    = re.search(r"(\d{4,8})", body)
                    self.seen_ids.add(mid)
                    if m:
                        otp = m.group(1)
                        log.info(f"MailTM OTP: {otp}")
                        return otp
            except Exception as e:
                log.warning(f"MailTM poll error: {e}")
        log.error(f"MailTM timeout {timeout}s")
        return None

# ============================================================
# BOT FLOW — Create Wallet
# ============================================================

def escape_adb(text: str) -> str:
    result = ""
    for ch in text:
        if ch == " ":
            result += "%s"
        elif ch in "\\()&|;<>!$`\"'`":
            result += "\\" + ch
        else:
            result += ch
    return result


def _nav_and_send_otp(dev: dict, mail, results: dict):
    pc   = dev["padCode"]
    name = dev["name"]
    D    = DELAY
    try:
        escaped_email = mail.address.replace(" ", "%s")
        wt  = WALLET_TAB_MAP.get(pc, UI["wallet_tab"])
        cmd = (
            f"input tap {wt[0]} {wt[1]} && sleep {D['after_tap_wallet_tab']} && "
            f"input tap {UI['create_wallet_btn'][0]} {UI['create_wallet_btn'][1]} && sleep {D['after_create_wallet_btn']} && "
            f"input tap {UI['agree_terms_btn'][0]} {UI['agree_terms_btn'][1]} && sleep {D['after_agree_terms_btn']} && "
            f"input tap {UI['email_field'][0]} {UI['email_field'][1]} && sleep {D['after_tap_email_field']} && "
            f"input text {escaped_email} && sleep {D['after_type_email']} && "
            f"input tap {UI['send_otp_btn'][0]} {UI['send_otp_btn'][1]}"
        )
        vcadb_exec([pc], cmd, poll_timeout=90)
        time.sleep(D["after_send_otp"])
        results[pc] = "ok"
        log.info(f"[{name}] Nav+OTP OK")
    except Exception as e:
        results[pc] = "error"
        log.error(f"[{name}] Nav error: {e}")


def run_create_wallet_all(devices: list):
    import threading

    section(f"Create Wallet — {len(devices)} device  ·  Ref: {C.BOLD}{REFERRAL_CODE}{C.RESET}")
    D  = DELAY
    ep = escape_adb(WALLET_PASSWORD)
    CONFIRM_KB_OPEN = (504, 606)

    MAIL_MAX_RETRY  = 5
    MAIL_RETRY_WAIT = 5

    # ── FASE 1: Buat email ───────────────────────────────────
    print()
    print(f"  {C.BOLD}{C.BLUE}[1/3]{C.RESET}  Membuat email temporer...")
    mail_map = {}
    for dev in devices:
        pc   = dev["padCode"]
        name = dev["name"]
        for attempt in range(1, MAIL_MAX_RETRY + 1):
            mail = MailTM()
            if mail.create_account():
                mail_map[pc] = mail
                print_ok(f"{C.BOLD}{name}{C.RESET}  {C.DIM}{mail.address}{C.RESET}  {C.DIM}(#{ attempt}){C.RESET}")
                break
            else:
                if attempt < MAIL_MAX_RETRY:
                    print_warn(f"{name}  gagal #{attempt} — retry {MAIL_RETRY_WAIT}s...")
                    time.sleep(MAIL_RETRY_WAIT)
                else:
                    print_err(f"{name}  gagal {MAIL_MAX_RETRY}x — skip")
        time.sleep(1)

    if not mail_map:
        print_err("Tidak ada email berhasil — abort"); return 0

    active_devices = [d for d in devices if d["padCode"] in mail_map]

    # ── FASE 2: Navigasi + send OTP paralel ─────────────────
    print()
    print(f"  {C.BOLD}{C.BLUE}[2/3]{C.RESET}  Navigasi + kirim OTP semua device...")
    nav_results = {}
    nav_threads = [
        threading.Thread(target=_nav_and_send_otp,
                         args=(dev, mail_map[dev["padCode"]], nav_results),
                         daemon=True)
        for dev in active_devices
    ]
    for t in nav_threads: t.start()
    for t in nav_threads: t.join()

    ok_nav = sum(1 for v in nav_results.values() if v == "ok")
    print_ok(f"Navigasi selesai  {C.DIM}{ok_nav}/{len(active_devices)} device OK{C.RESET}")

    # ── FASE 3: Captcha manual → OTP → password ──────────────
    print()
    print(f"  {C.BOLD}{C.BLUE}[3/3]{C.RESET}  Selesaikan CAPTCHA di semua device terlebih dahulu.")
    print()
    print(f"  {C.YELLOW}⚠{C.RESET}   Buka VSPhone, verifikasi captcha di SEMUA device,")
    print(f"       lalu tekan {C.BOLD}ENTER{C.RESET} satu kali untuk lanjut.")
    print()
    input(f"  {C.BOLD}  → Tekan ENTER setelah semua captcha selesai...{C.RESET}  ")
    print()
    print_run("Semua device jalan paralel...")

    ok_counter  = [0]
    result_lock = threading.Lock()

    def _finish_one(dev):
        pc   = dev["padCode"]
        name = dev["name"]
        mail = mail_map[pc]
        try:
            print_wait(f"[{name}] Menunggu OTP...")
            otp = mail.wait_for_otp(timeout=OTP_TIMEOUT)
            if not otp:
                print_err(f"[{name}] OTP tidak masuk — skip"); return

            print_ok(f"[{name}] OTP: {C.BOLD}{otp}{C.RESET}")

            cmd = (
                f"input tap {UI['otp_field'][0]} {UI['otp_field'][1]} && sleep {D['after_tap_otp_field']} && "
                f"input text {otp} && sleep {D['after_type_otp']} && "
                f"input tap {UI['reff_dropdown'][0]} {UI['reff_dropdown'][1]} && sleep {D['after_tap_reff_dropdown']} && "
                f"input tap {UI['reff_field'][0]} {UI['reff_field'][1]} && sleep {D['after_tap_reff_field']} && "
                f"input text {REFERRAL_CODE} && sleep {D['after_type_reff']} && "
                f"input tap {UI['next_button'][0]} {UI['next_button'][1]}"
            )
            vcadb_exec([pc], cmd, poll_timeout=60)
            time.sleep(D["after_next_button"])

            cmd1 = (
                f"input tap {UI['pass_field'][0]} {UI['pass_field'][1]} && sleep {D['after_tap_pass_field']} && "
                f"input text {ep} && sleep {D['after_type_password']}"
            )
            vcadb_exec([pc], cmd1, poll_timeout=30)
            time.sleep(D["after_tap_confirm_pass"])

            cmd2 = (
                f"input tap {CONFIRM_KB_OPEN[0]} {CONFIRM_KB_OPEN[1]} && sleep {D['after_tap_confirm_pass']} && "
                f"input text {ep} && sleep {D['after_type_password']} && "
                f"input keyevent 4 && sleep {D['after_hide_keyboard']} && "
                f"input tap {UI['agree_forget_cb'][0]} {UI['agree_forget_cb'][1]} && sleep {D['after_agree_forget_cb']} && "
                f"input tap {UI['final_continue_btn'][0]} {UI['final_continue_btn'][1]}"
            )
            vcadb_exec([pc], cmd2, poll_timeout=60)
            time.sleep(D["after_final_continue"])

            cmd3 = (
                f"input tap {UI['google_save_cancel'][0]} {UI['google_save_cancel'][1]} && sleep {D['after_google_save_cancel']} && "
                f"input tap {UI['skip_biometric'][0]} {UI['skip_biometric'][1]} && sleep {D['after_skip_biometric']} && "
                f"input tap {UI['set_up_later'][0]} {UI['set_up_later'][1]}"
            )
            vcadb_exec([pc], cmd3, poll_timeout=30)
            time.sleep(D["after_set_up_later"])

            result_line = f"Device={name} | Email={mail.address} | Pass={WALLET_PASSWORD} | Ref={REFERRAL_CODE}"
            log.info(f"[{name}] WALLET OK: {result_line}")
            print_ok(f"[{C.BOLD}{name}{C.RESET}]  {C.GREEN}Wallet berhasil dibuat!{C.RESET}")
            with result_lock:
                with open("wallet_sukses.txt", "a", encoding="utf-8") as f:
                    f.write(result_line + "\n")
                ok_counter[0] += 1

        except Exception as e:
            log.error(f"[{name}] Error: {e}")
            print_err(f"[{name}] Error: {e}")

    threads = []
    for dev in active_devices:
        if nav_results.get(dev["padCode"]) != "ok":
            print_warn(f"[{dev['name']}] Skip — navigasi gagal")
            continue
        t = threading.Thread(target=_finish_one, args=(dev,), daemon=True)
        threads.append(t)

    for t in threads: t.start()
    for t in threads: t.join()

    print()
    print_ok(f"Selesai  {C.BOLD}{ok_counter[0]}/{len(active_devices)}{C.RESET} wallet dibuat")
    return ok_counter[0]


# ============================================================
# SET RESOLUSI
# ============================================================

def set_resolution_all(devices: list):
    section("Set resolusi → 1080×1920, DPI 320")
    pad_codes = [d["padCode"] for d in devices]
    vcadb_exec(pad_codes, "wm size 1080x1920 && wm density 320", poll_timeout=30)
    print_ok("Resolusi berhasil diset ke 1080×1920 DPI 320")


# ============================================================
# SATU SIKLUS
# ============================================================

def run_one_cycle(devices: list, apk_info: dict):
    print()
    box_top("Siklus Baru", C.PURPLE)
    box_mid(f"Device aktif: {C.BOLD}{len(devices)}{C.RESET}  ·  Referral: {C.BOLD}{REFERRAL_CODE}{C.RESET}", C.PURPLE, "")
    box_bot(C.PURPLE)

    installed_pads = check_installed(devices)
    need_install   = [d for d in devices if d["padCode"] not in installed_pads]

    if need_install:
        task_map     = install_to_devices(need_install, apk_info)
        inst_results = poll_tasks(task_map)
        ok = sum(1 for r in inst_results.values() if r["success"])
        print_ok(f"Install selesai  {C.DIM}{ok}/{len(need_install)} berhasil{C.RESET}")
        time.sleep(3)
    else:
        print_ok("Semua device sudah ada TopNod — skip install")

    launch_results = launch_app(devices)
    ok_launch      = sum(1 for r in launch_results.values() if r["success"])
    if ok_launch == 0:
        print_err("Launch gagal semua — abort"); return 0

    countdown(LAUNCH_WAIT, "Tunggu TopNod terbuka")
    set_resolution_all(devices)
    time.sleep(3)

    ok_wallet = run_create_wallet_all(devices)
    return ok_wallet


# ============================================================
# MAIN
# ============================================================

def main():
    banner()

    login()
    time.sleep(1)

    devices = get_devices()
    if not devices:
        print_err("Tidak ada device — abort"); return

    devices = [d for d in devices if d["padCode"] not in EXCLUDE_DEVICES]
    if EXCLUDE_DEVICES:
        print_info(f"Device dikecualikan: {C.DIM}{EXCLUDE_DEVICES}{C.RESET}")
    if not devices:
        print_err("Semua device dikecualikan — abort"); return

    # ── Tanya referral code ──────────────────────────────────
    global REFERRAL_CODE
    REFERRAL_BATCH_SIZE = 5

    def ask_referral():
        global REFERRAL_CODE
        print()
        print(f"  {C.CYAN}Referral code saat ini:{C.RESET} {C.BOLD}{REFERRAL_CODE}{C.RESET}")
        ref = input(f"  Masukkan referral baru (kosong = pakai default): ").strip()
        if ref:
            REFERRAL_CODE = ref
            print_ok(f"Referral diset → {C.BOLD}{REFERRAL_CODE}{C.RESET}")
        else:
            print_info(f"Pakai default: {C.BOLD}{REFERRAL_CODE}{C.RESET}")

    ask_referral()

    # ── Pilih device yang dikecualikan ───────────────────────
    print()
    section("Daftar device aktif")
    for i, d in enumerate(devices, 1):
        print(f"    {C.CYAN}{i}.{C.RESET}  {C.BOLD}{d['name']}{C.RESET}  {C.DIM}{d['padCode']}{C.RESET}")
    print()
    exclude_input = input("  Nomor device dikecualikan (pisah koma, kosong = semua): ").strip()
    if exclude_input:
        try:
            exclude_idx = {int(x.strip()) - 1 for x in exclude_input.split(",")}
            excluded    = [devices[i] for i in exclude_idx if 0 <= i < len(devices)]
            devices     = [d for i, d in enumerate(devices) if i not in exclude_idx]
            for d in excluded:
                print_warn(f"Dikecualikan: {d['name']}  {C.DIM}{d['padCode']}{C.RESET}")
        except ValueError:
            print_warn("Input tidak valid — pakai semua device")

    if not devices:
        print_err("Semua device dikecualikan — abort"); return

    print()
    print_ok(f"Device aktif: {C.BOLD}{len(devices)}{C.RESET}")
    for d in devices:
        print_info(f"{C.BOLD}{d['name']}{C.RESET}  {C.DIM}{d['padCode']}{C.RESET}")

    set_resolution_all(devices)
    time.sleep(3)

    # ── Pilih APK ────────────────────────────────────────────
    apk_result = get_topnod_apk()
    if apk_result is None:
        print_err("APK TopNod tidak ditemukan — abort"); return
    if isinstance(apk_result, list):
        while True:
            try:
                c = int(input(f"\n  Pilih nomor APK (1-{len(apk_result)}): "))
                if 1 <= c <= len(apk_result): break
            except ValueError:
                pass
        apk_info = apk_result[c - 1]
    else:
        apk_info = apk_result

    # ── Summary sebelum loop ─────────────────────────────────
    print()
    box_top("Konfigurasi Loop", C.BLUE)
    box_mid(f"APK      : {apk_info['fileName']}", C.BLUE, C.WHITE)
    box_mid(f"Device   : {len(devices)} aktif", C.BLUE, C.WHITE)
    box_mid(f"Referral : {REFERRAL_CODE}", C.BLUE, C.WHITE)
    box_mid(f"Batch    : {REFERRAL_BATCH_SIZE} device / referral", C.BLUE, C.WHITE)
    box_mid(f"Log file : {log_filename}", C.BLUE, C.DIM)
    box_bot(C.BLUE)
    print()

    # ── LOOP UTAMA ───────────────────────────────────────────
    siklus          = 0
    total_wallet    = 0
    device_in_batch = 0

    try:
        while True:
            sisa_batch  = REFERRAL_BATCH_SIZE - device_in_batch
            run_count   = min(len(devices), sisa_batch)
            devices_run = devices[:run_count]

            siklus += 1
            ok      = run_one_cycle(devices_run, apk_info)
            total_wallet    += ok
            device_in_batch += run_count

            # ── Ringkasan siklus ─────────────────────────────
            print()
            box_top(f"Siklus {siklus} Selesai", C.GREEN)
            box_mid(f"Wallet dibuat  : {C.BOLD}{ok}{C.RESET}/{run_count}", C.GREEN, C.WHITE)
            box_mid(f"Total wallet   : {C.BOLD}{total_wallet}{C.RESET}", C.GREEN, C.WHITE)
            box_mid(f"Batch progress : {device_in_batch}/{REFERRAL_BATCH_SIZE} device", C.GREEN, C.WHITE)
            box_mid(f"Hasil di       : wallet_sukses.txt", C.GREEN, C.DIM)
            box_bot(C.GREEN)

            log.info(f"Siklus {siklus} selesai — {ok} wallet, total {total_wallet}")

            if device_in_batch >= REFERRAL_BATCH_SIZE:
                print()
                print_ok(f"{C.BOLD}{REFERRAL_BATCH_SIZE}{C.RESET} device selesai — minta referral baru")
                device_in_batch = 0
                ask_referral()
            else:
                print()
                print_wait("Menunggu device reboot, lalu mulai siklus berikutnya...")

    except KeyboardInterrupt:
        print()
        box_top("Script Dihentikan", C.YELLOW)
        box_mid(f"Total siklus  : {siklus}", C.YELLOW, C.WHITE)
        box_mid(f"Total wallet  : {C.BOLD}{total_wallet}{C.RESET}", C.YELLOW, C.WHITE)
        box_bot(C.YELLOW)
        log.info(f"Script dihentikan. Siklus: {siklus}, Wallet: {total_wallet}")
    except Exception as e:
        print()
        print_err(f"Error fatal: {e}")
        log.error(f"Error fatal: {e}")


if __name__ == "__main__":

    main()
