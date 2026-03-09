# ============================================================
# CONFIG UI — Koordinat klik untuk semua halaman TopNod
# ============================================================
# Resolusi: 1080x1920, DPI 320
# Cara cari koordinat:
#   uiautomator dump /sdcard/ui.xml && cp /sdcard/ui.xml /sdcard/ui2.txt
#   grep -o '<node[^>]*KEYWORD[^>]*>' /sdcard/ui2.txt
#   Dari bounds="[x1,y1][x2,y2]" → tengah = ((x1+x2)//2, (y1+y2)//2)
# ============================================================

DELAY = {
    "after_tap_wallet_tab":     5,
    "after_agree_checkbox":     3,
    "after_create_wallet_btn":  6,
    "after_agree_terms_btn":    6,
    "after_tap_email_field":    3,
    "after_type_email":         3,
    "after_send_otp":           5,
    "after_tap_otp_field":      3,
    "after_type_otp":           3,
    "after_tap_reff_dropdown":  4,
    "after_tap_reff_field":     3,
    "after_type_reff":          3,
    "after_next_button":        8,
    "after_tap_pass_field":     3,
    "after_type_password":      3,
    "after_hide_keyboard":      3,
    "after_tap_confirm_pass":   3,
    "after_agree_forget_cb":    3,
    "after_final_continue":     5,
    "after_google_save_cancel": 5,
    "after_skip_biometric":     5,
    "after_set_up_later":       4,
}

WALLET_TAB = {
    "default":          (945, 1809),  # ✅ bounds=[810,1699][1080,1920]
    "APP5BK4M191Z0R29": (945, 1809),
    "APP5CI50JWFL91N4": (945, 1809),
    "ACP5CM52M50ZWJYI": (945, 1809),
    "ACP5CM52KXCBFX2W": (945, 1809),
    "ACP250915SMMDBIO": (945, 1809),
}

WALLET_INTRO = {
    "create_wallet_btn": (540, 1629),  # ✅ bounds=[58,1581][1022,1677]
    "agree_terms_btn":   (540, 1788),  # ✅ bounds=[40,1744][1040,1832]
}

CREATE_WALLET = {
    "email_field":   (528,  476),  # ✅ bounds=[61,432][995,520]
    "otp_field":     (496,  660),  # ✅ bounds=[61,616][931,704]
    "send_otp_btn":  (979,  660),  # ✅ bounds=[947,616][1011,704]
    "reff_dropdown": (540,  770),  # ✅ bounds=[40,752][1040,788]
    "reff_field":    (528,  848),  # ✅ bounds=[61,804][995,892]
    "next_button":   (540, 1036),  # ✅ bounds=[40,988][1040,1084] KB buka
}

SET_PASSWORD = {
    "pass_field":         (504,  578),  # ✅ bounds=[61,534][947,622] KB tutup
    "confirm_pass_field": (504,  606),  # ✅ bounds=[61,562][947,650] KB buka
    "agree_forget_cb":    (58,  1636),  # ✅ bounds=[40,1618][76,1654]
    "final_continue_btn": (540, 1768),  # ✅ bounds=[40,1720][1040,1816]
}

POPUPS = {
    "skip_biometric":     (1001,  90),  # ✅ bounds=[962,68][1040,112]
    "set_up_later":       (540, 1772),  # ✅ bounds=[58,1724][1022,1820]
    "google_save_cancel": (250, 1000),  # ⚠️  belum dikalibrasi
}

LOGOUT = {
    "logout_btn":     (539, 1644),  # ✅ bounds=[490,1626][589,1662]
    "logout_confirm": (794, 1700),  # ✅ bounds=[741,1684][848,1716]
}

# ── Gabung semua ke UI dict ──────────────────────────────────
UI = {}
UI.update(WALLET_INTRO)
UI.update(CREATE_WALLET)
UI.update(SET_PASSWORD)
UI.update(POPUPS)
UI.update(LOGOUT)
UI["wallet_tab"]     = WALLET_TAB["default"]
UI["agree_checkbox"] = (0, 0)  # placeholder — tidak dipakai

WALLET_TAB_MAP = {k: v for k, v in WALLET_TAB.items() if k != "default"}