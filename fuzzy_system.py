"""
fuzzy_system.py
Deprem Sonrasi Acil Risk Değerlendirme Sistemi - Bulanık Mantık Motoru

Yöntem : Mamdani çıkarım sistemi
Durulaştırma : Centroid
Kutuphane  : scikit-fuzzy
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# ---------------------------------------------------------------------------
# EVREN TANIMI
# ---------------------------------------------------------------------------

u_deprem = np.arange(0, 10.01, 0.05)
u_bina   = np.arange(0, 80.01, 0.1)
u_zemin  = np.arange(0, 10.01, 0.05)   # 0 = cok kotu / sivila?ma riski, 10 = kayalik/sagla
u_kat    = np.arange(1, 30.01, 0.1)
u_risk   = np.arange(0, 100.01, 0.1)

# ---------------------------------------------------------------------------
# ANTECEDENT / CONSEQUENT TANIMLARI
# ---------------------------------------------------------------------------

deprem_siddeti = ctrl.Antecedent(u_deprem, "deprem_siddeti")
bina_yasi      = ctrl.Antecedent(u_bina,   "bina_yasi")
zemin_durumu   = ctrl.Antecedent(u_zemin,  "zemin_durumu")
kat_sayisi     = ctrl.Antecedent(u_kat,    "kat_sayisi")
risk_seviyesi  = ctrl.Consequent(u_risk,   "risk_seviyesi", defuzzify_method="centroid")

# ---------------------------------------------------------------------------
# UYELIK FONKSIYONLARI
# ---------------------------------------------------------------------------

# -- Deprem Siddeti (0-10 Richter) --
# Dusuk  : 0-4.5 arasi  (max 0-3)
# Orta   : 3.5-7.0      (tepe 5.2)
# Yuksek : 6.0-10       (max 7.5-10)
deprem_siddeti["dusuk"]   = fuzz.trapmf(u_deprem, [0,   0,   3.0, 4.5])
deprem_siddeti["orta"]    = fuzz.trimf( u_deprem, [3.5, 5.2, 6.8])
deprem_siddeti["yuksek"]  = fuzz.trapmf(u_deprem, [6.0, 7.5, 10,  10])

# -- Bina Yasi (0-80 yil) --
# Yeni       : 0-20      (tepe 0-10)
# Orta Yasli : 15-55     (tepe 35)
# Eski       : 45-80     (tepe 60-80)
bina_yasi["yeni"]       = fuzz.trapmf(u_bina, [0,  0,  10, 22])
bina_yasi["orta_yasli"] = fuzz.trimf( u_bina, [15, 35, 55])
bina_yasi["eski"]       = fuzz.trapmf(u_bina, [45, 60, 80, 80])

# -- Zemin Durumu (0=kotu, 10=iyi) --
# Kotu : 0-4.5          (tepe 0-2.5)
# Orta : 3.0-7.5        (tepe 5.0)
# Iyi  : 6.0-10         (tepe 8.0-10)
zemin_durumu["kotu"] = fuzz.trapmf(u_zemin, [0,   0,   2.5, 4.5])
zemin_durumu["orta"] = fuzz.trimf( u_zemin, [3.0, 5.0, 7.5])
zemin_durumu["iyi"]  = fuzz.trapmf(u_zemin, [6.0, 8.0, 10,  10])

# -- Kat Sayisi (1-30) --
# Az Katli   : 1-6      (tepe 1-3)
# Orta Katli : 4-18     (tepe 10)
# Cok Katli  : 14-30    (tepe 20-30)
kat_sayisi["az_katli"]   = fuzz.trapmf(u_kat, [1,  1,  3,  6])
kat_sayisi["orta_katli"] = fuzz.trimf( u_kat, [4,  10, 18])
kat_sayisi["cok_katli"]  = fuzz.trapmf(u_kat, [14, 20, 30, 30])

# -- Risk Seviyesi (0-100) --
# Cakisma noktalari duzenlendi; aralik bosluklari yok
risk_seviyesi["dusuk"]  = fuzz.trapmf(u_risk, [0,   0,  18,  32])
risk_seviyesi["orta"]   = fuzz.trimf( u_risk, [25,  42,  58])
risk_seviyesi["yuksek"] = fuzz.trimf( u_risk, [50,  67,  82])
risk_seviyesi["kritik"] = fuzz.trapmf(u_risk, [72,  88, 100, 100])

# ---------------------------------------------------------------------------
# KURAL TABANI  (28 kural)
# ---------------------------------------------------------------------------

# Her kural icin not: AND = minimum, OR = maximum (Mamdani standardi)

kurallar = [

    # ---- KRITIK RISK (8 kural) ----
    # En tehlikeli kombinasyonlar: yuksek deprem + kotu zemin + diger faktOrler
    ctrl.Rule(
        deprem_siddeti["yuksek"] & zemin_durumu["kotu"] & bina_yasi["eski"],
        risk_seviyesi["kritik"]
    ),
    ctrl.Rule(
        deprem_siddeti["yuksek"] & zemin_durumu["kotu"] & kat_sayisi["cok_katli"],
        risk_seviyesi["kritik"]
    ),
    ctrl.Rule(
        deprem_siddeti["yuksek"] & bina_yasi["eski"] & kat_sayisi["cok_katli"],
        risk_seviyesi["kritik"]
    ),
    ctrl.Rule(
        deprem_siddeti["yuksek"] & zemin_durumu["kotu"],
        risk_seviyesi["kritik"]
    ),
    ctrl.Rule(
        zemin_durumu["kotu"] & bina_yasi["eski"] & kat_sayisi["cok_katli"],
        risk_seviyesi["kritik"]
    ),
    ctrl.Rule(
        deprem_siddeti["yuksek"] & bina_yasi["eski"] & zemin_durumu["orta"],
        risk_seviyesi["kritik"]
    ),
    ctrl.Rule(
        deprem_siddeti["orta"] & zemin_durumu["kotu"] & bina_yasi["eski"] & kat_sayisi["cok_katli"],
        risk_seviyesi["kritik"]
    ),
    ctrl.Rule(
        deprem_siddeti["yuksek"] & zemin_durumu["orta"] & bina_yasi["eski"],
        risk_seviyesi["kritik"]
    ),

    # ---- YUKSEK RISK (9 kural) ----
    ctrl.Rule(
        deprem_siddeti["yuksek"] & zemin_durumu["orta"] & kat_sayisi["cok_katli"],
        risk_seviyesi["yuksek"]
    ),
    ctrl.Rule(
        deprem_siddeti["yuksek"] & zemin_durumu["iyi"] & bina_yasi["eski"],
        risk_seviyesi["yuksek"]
    ),
    ctrl.Rule(
        deprem_siddeti["yuksek"] & bina_yasi["yeni"] & zemin_durumu["kotu"],
        risk_seviyesi["yuksek"]
    ),
    ctrl.Rule(
        deprem_siddeti["orta"] & zemin_durumu["kotu"] & bina_yasi["eski"],
        risk_seviyesi["yuksek"]
    ),
    ctrl.Rule(
        deprem_siddeti["orta"] & zemin_durumu["kotu"] & kat_sayisi["cok_katli"],
        risk_seviyesi["yuksek"]
    ),
    ctrl.Rule(
        deprem_siddeti["yuksek"] & bina_yasi["orta_yasli"] & zemin_durumu["orta"],
        risk_seviyesi["yuksek"]
    ),
    ctrl.Rule(
        deprem_siddeti["yuksek"] & kat_sayisi["cok_katli"],
        risk_seviyesi["yuksek"]
    ),
    ctrl.Rule(
        zemin_durumu["kotu"] & bina_yasi["orta_yasli"] & kat_sayisi["cok_katli"],
        risk_seviyesi["yuksek"]
    ),
    ctrl.Rule(
        deprem_siddeti["orta"] & bina_yasi["eski"] & kat_sayisi["cok_katli"],
        risk_seviyesi["yuksek"]
    ),

    # ---- ORTA RISK (7 kural) ----
    ctrl.Rule(
        deprem_siddeti["orta"] & zemin_durumu["orta"] & bina_yasi["orta_yasli"],
        risk_seviyesi["orta"]
    ),
    ctrl.Rule(
        deprem_siddeti["orta"] & zemin_durumu["iyi"] & bina_yasi["eski"],
        risk_seviyesi["orta"]
    ),
    ctrl.Rule(
        deprem_siddeti["orta"] & zemin_durumu["kotu"] & bina_yasi["yeni"],
        risk_seviyesi["orta"]
    ),
    ctrl.Rule(
        deprem_siddeti["dusuk"] & zemin_durumu["kotu"] & bina_yasi["eski"],
        risk_seviyesi["orta"]
    ),
    ctrl.Rule(
        deprem_siddeti["dusuk"] & zemin_durumu["kotu"] & kat_sayisi["cok_katli"],
        risk_seviyesi["orta"]
    ),
    ctrl.Rule(
        deprem_siddeti["yuksek"] & zemin_durumu["iyi"] & bina_yasi["yeni"],
        risk_seviyesi["orta"]
    ),
    ctrl.Rule(
        deprem_siddeti["orta"] & bina_yasi["orta_yasli"] & kat_sayisi["orta_katli"],
        risk_seviyesi["orta"]
    ),

    # ---- DUSUK RISK (4 kural) ----
    ctrl.Rule(
        deprem_siddeti["dusuk"] & zemin_durumu["iyi"] & bina_yasi["yeni"],
        risk_seviyesi["dusuk"]
    ),
    ctrl.Rule(
        deprem_siddeti["dusuk"] & zemin_durumu["iyi"] & kat_sayisi["az_katli"],
        risk_seviyesi["dusuk"]
    ),
    ctrl.Rule(
        deprem_siddeti["dusuk"] & zemin_durumu["orta"] & bina_yasi["yeni"],
        risk_seviyesi["dusuk"]
    ),
    ctrl.Rule(
        deprem_siddeti["dusuk"] & bina_yasi["yeni"] & kat_sayisi["az_katli"],
        risk_seviyesi["dusuk"]
    ),
]

sistem = ctrl.ControlSystem(kurallar)

# ---------------------------------------------------------------------------
# FALLBACK HESAPLAMA
# ---------------------------------------------------------------------------

def _fallback_hesapla(dep, bina, zemin, kat):
    """
    Bulanik sistemin sonuc uretemediginde devreye giren deterministik
    agirlikli hesaplama. Gercek fuzzy sonuclarini hic etkilemez.
    """
    skor = (
        (dep / 10.0)      * 42 +
        ((10 - zemin) / 10.0) * 30 +
        (bina / 80.0)     * 18 +
        ((kat - 1) / 29.0) * 10
    )
    return float(np.clip(skor, 0.0, 100.0))

# ---------------------------------------------------------------------------
# ANA HESAPLAMA FONKSIYONU
# ---------------------------------------------------------------------------

def hesapla_risk(deprem, bina, zemin, kat):
    """
    Verilen giris degerleri icin risk skorunu hesaplar ve dondurur.

    Parametreler
    ----------
    deprem : float  0-10 Richter
    bina   : float  0-80 yil
    zemin  : float  0-10 (0=kotu, 10=iyi)
    kat    : float  1-30

    Donus
    ------
    float  0.0 - 100.0 arasi risk skoru
    """
    deprem = float(np.clip(deprem, 0.0, 10.0))
    bina   = float(np.clip(bina,   0.0, 80.0))
    zemin  = float(np.clip(zemin,  0.0, 10.0))
    kat    = float(np.clip(kat,    1.0, 30.0))

    try:
        sim = ctrl.ControlSystemSimulation(sistem)
        sim.reset()

        sim.input["deprem_siddeti"] = deprem
        sim.input["bina_yasi"]      = bina
        sim.input["zemin_durumu"]   = zemin
        sim.input["kat_sayisi"]     = kat

        sim.compute()

        if "risk_seviyesi" not in sim.output:
            return _fallback_hesapla(deprem, bina, zemin, kat)

        return float(np.clip(sim.output["risk_seviyesi"], 0.0, 100.0))

    except Exception:
        return _fallback_hesapla(deprem, bina, zemin, kat)

# ---------------------------------------------------------------------------
# AKTIF KURAL BULMA
# ---------------------------------------------------------------------------

def aktif_kurallari_bul(deprem, bina, zemin, kat):
    """
    Verilen girislerde aktivasyon esigini (0.05) gecen kurallari dondurur.

    Donus
    ------
    list[dict]  kural_no, tanim, aktivasyon anahtarlari iceren sozlukler listesi
    """
    deprem = float(np.clip(deprem, 0.0, 10.0))
    bina   = float(np.clip(bina,   0.0, 80.0))
    zemin  = float(np.clip(zemin,  0.0, 10.0))
    kat    = float(np.clip(kat,    1.0, 30.0))

    # Uyelik dereceleri
    dep_d = float(fuzz.interp_membership(u_deprem, deprem_siddeti["dusuk"].mf,  deprem))
    dep_o = float(fuzz.interp_membership(u_deprem, deprem_siddeti["orta"].mf,   deprem))
    dep_y = float(fuzz.interp_membership(u_deprem, deprem_siddeti["yuksek"].mf, deprem))

    bin_y = float(fuzz.interp_membership(u_bina, bina_yasi["yeni"].mf,       bina))
    bin_o = float(fuzz.interp_membership(u_bina, bina_yasi["orta_yasli"].mf, bina))
    bin_e = float(fuzz.interp_membership(u_bina, bina_yasi["eski"].mf,       bina))

    zem_k = float(fuzz.interp_membership(u_zemin, zemin_durumu["kotu"].mf, zemin))
    zem_o = float(fuzz.interp_membership(u_zemin, zemin_durumu["orta"].mf, zemin))
    zem_i = float(fuzz.interp_membership(u_zemin, zemin_durumu["iyi"].mf,  zemin))

    kat_a = float(fuzz.interp_membership(u_kat, kat_sayisi["az_katli"].mf,   kat))
    kat_o = float(fuzz.interp_membership(u_kat, kat_sayisi["orta_katli"].mf, kat))
    kat_c = float(fuzz.interp_membership(u_kat, kat_sayisi["cok_katli"].mf,  kat))

    # (aktivasyon, tanimlama) cifti
    kural_bilgi = [
        # --- KRITIK ---
        (min(dep_y, zem_k, bin_e),        "Deprem yuksek, zemin kotu ve bina eski -> Kritik Risk"),
        (min(dep_y, zem_k, kat_c),        "Deprem yuksek, zemin kotu ve cok katli -> Kritik Risk"),
        (min(dep_y, bin_e, kat_c),        "Deprem yuksek, bina eski ve cok katli -> Kritik Risk"),
        (min(dep_y, zem_k),               "Deprem yuksek ve zemin kotu -> Kritik Risk"),
        (min(zem_k, bin_e, kat_c),        "Zemin kotu, bina eski ve cok katli -> Kritik Risk"),
        (min(dep_y, bin_e, zem_o),        "Deprem yuksek, bina eski ve zemin orta -> Kritik Risk"),
        (min(dep_o, zem_k, bin_e, kat_c), "Deprem orta, zemin kotu, bina eski ve cok katli -> Kritik Risk"),
        (min(dep_y, zem_o, bin_e),        "Deprem yuksek, zemin orta ve bina eski -> Kritik Risk"),
        # --- YUKSEK ---
        (min(dep_y, zem_o, kat_c),        "Deprem yuksek, zemin orta ve cok katli -> Yuksek Risk"),
        (min(dep_y, zem_i, bin_e),        "Deprem yuksek, zemin iyi fakat bina eski -> Yuksek Risk"),
        (min(dep_y, bin_y, zem_k),        "Deprem yuksek, bina yeni fakat zemin kotu -> Yuksek Risk"),
        (min(dep_o, zem_k, bin_e),        "Deprem orta, zemin kotu ve bina eski -> Yuksek Risk"),
        (min(dep_o, zem_k, kat_c),        "Deprem orta, zemin kotu ve cok katli -> Yuksek Risk"),
        (min(dep_y, bin_o, zem_o),        "Deprem yuksek, bina orta yasli ve zemin orta -> Yuksek Risk"),
        (min(dep_y, kat_c),               "Deprem yuksek ve cok katli -> Yuksek Risk"),
        (min(zem_k, bin_o, kat_c),        "Zemin kotu, bina orta yasli ve cok katli -> Yuksek Risk"),
        (min(dep_o, bin_e, kat_c),        "Deprem orta, bina eski ve cok katli -> Yuksek Risk"),
        # --- ORTA ---
        (min(dep_o, zem_o, bin_o),        "Deprem orta, zemin orta ve bina orta yasli -> Orta Risk"),
        (min(dep_o, zem_i, bin_e),        "Deprem orta, zemin iyi fakat bina eski -> Orta Risk"),
        (min(dep_o, zem_k, bin_y),        "Deprem orta, zemin kotu fakat bina yeni -> Orta Risk"),
        (min(dep_d, zem_k, bin_e),        "Deprem dusuk, zemin kotu ve bina eski -> Orta Risk"),
        (min(dep_d, zem_k, kat_c),        "Deprem dusuk, zemin kotu ve cok katli -> Orta Risk"),
        (min(dep_y, zem_i, bin_y),        "Deprem yuksek, zemin iyi ve bina yeni -> Orta Risk"),
        (min(dep_o, bin_o, kat_o),        "Deprem orta, bina orta yasli ve kat orta -> Orta Risk"),
        # --- DUSUK ---
        (min(dep_d, zem_i, bin_y),        "Deprem dusuk, zemin iyi ve bina yeni -> Dusuk Risk"),
        (min(dep_d, zem_i, kat_a),        "Deprem dusuk, zemin iyi ve az katli -> Dusuk Risk"),
        (min(dep_d, zem_o, bin_y),        "Deprem dusuk, zemin orta ve bina yeni -> Dusuk Risk"),
        (min(dep_d, bin_y, kat_a),        "Deprem dusuk, bina yeni ve az katli -> Dusuk Risk"),
    ]

    sonuc = []
    for idx, (aktivasyon, tanim) in enumerate(kural_bilgi, start=1):
        if aktivasyon >= 0.05:
            sonuc.append({
                "kural_no":   idx,
                "tanim":      tanim,
                "aktivasyon": round(float(aktivasyon), 4),
            })

    sonuc.sort(key=lambda x: x["aktivasyon"], reverse=True)
    return sonuc

# ---------------------------------------------------------------------------
# UYELIK VERI IHRACATI (plots.py icin)
# ---------------------------------------------------------------------------

def get_membership_data():
    """
    Tum üyelik fonksiyonu verilerini sozluk olarak dondurur.
    plots.py bu fonksiyonu kullanarak grafik olusturur.
    """
    return {
        "deprem": {
            "universe": u_deprem,
            "mfs": {
                "Dusuk":  deprem_siddeti["dusuk"].mf,
                "Orta":   deprem_siddeti["orta"].mf,
                "Yuksek": deprem_siddeti["yuksek"].mf,
            },
        },
        "bina": {
            "universe": u_bina,
            "mfs": {
                "Yeni":       bina_yasi["yeni"].mf,
                "Orta_Yasli": bina_yasi["orta_yasli"].mf,
                "Eski":       bina_yasi["eski"].mf,
            },
        },
        "zemin": {
            "universe": u_zemin,
            "mfs": {
                "Kotu": zemin_durumu["kotu"].mf,
                "Orta": zemin_durumu["orta"].mf,
                "Iyi":  zemin_durumu["iyi"].mf,
            },
        },
        "kat": {
            "universe": u_kat,
            "mfs": {
                "Az_Katli":   kat_sayisi["az_katli"].mf,
                "Orta_Katli": kat_sayisi["orta_katli"].mf,
                "Cok_Katli":  kat_sayisi["cok_katli"].mf,
            },
        },
        "risk": {
            "universe": u_risk,
            "mfs": {
                "Dusuk":  risk_seviyesi["dusuk"].mf,
                "Orta":   risk_seviyesi["orta"].mf,
                "Yuksek": risk_seviyesi["yuksek"].mf,
                "Kritik": risk_seviyesi["kritik"].mf,
            },
        },
    }
