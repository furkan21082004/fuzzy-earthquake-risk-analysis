"""
test_scenarios.py
Deprem Sonrasi Acil Risk Degerlendirme Sistemi
Test Senaryolari ve Dogrulama Modulu
"""

from fuzzy_system import hesapla_risk


# ---------------------------------------------------------------------------
# RISK SINIFLANDIRMA
# ---------------------------------------------------------------------------

def siniflandir(skor: float) -> str:
    """Risk skorunu dilsel sinifa donusturur."""
    if skor < 25:
        return "Dusuk Risk"
    if skor < 50:
        return "Orta Risk"
    if skor < 75:
        return "Yuksek Risk"
    return "Kritik Risk"


# ---------------------------------------------------------------------------
# TEST SENARYOLARI
# ---------------------------------------------------------------------------

SENARYOLAR = [
    {
        "isim": "S1 - Guvenli Yeni Bina",
        "aciklama": "Yeni bina, sagla zemin, dusuk deprem, az katli",
        "deprem": 2.0,
        "bina_yasi": 4,
        "zemin": 9.0,
        "kat": 3,
        "beklenen_sinif": "Dusuk Risk",
    },
    {
        "isim": "S2 - Kritik Felaket",
        "aciklama": "Eski bina, cok kotu zemin, yuksek deprem, cok katli",
        "deprem": 9.5,
        "bina_yasi": 75,
        "zemin": 0.5,
        "kat": 28,
        "beklenen_sinif": "Kritik Risk",
    },
    {
        "isim": "S3 - Orta Riskli Yapi",
        "aciklama": "Orta yasli bina, orta deprem, orta zemin",
        "deprem": 5.2,
        "bina_yasi": 35,
        "zemin": 5.0,
        "kat": 9,
        "beklenen_sinif": "Orta Risk",
    },
    {
        "isim": "S4 - Kotu Zemin Etkisi",
        "aciklama": "Yeni bina ama zemin cok kotu ve deprem yuksek",
        "deprem": 7.8,
        "bina_yasi": 6,
        "zemin": 1.5,
        "kat": 12,
        "beklenen_sinif": "Yuksek Risk",
    },
    {
        "isim": "S5 - Eski Bina Sagla Zemin",
        "aciklama": "Eski bina fakat sagla zeminde, dusuk deprem",
        "deprem": 3.5,
        "bina_yasi": 65,
        "zemin": 8.5,
        "kat": 5,
        "beklenen_sinif": "Orta Risk",
    },
    {
        "isim": "S6 - Cok Katli Risk",
        "aciklama": "Kat sayisi yuksek, orta-yuksek deprem, orta zemin",
        "deprem": 6.8,
        "bina_yasi": 30,
        "zemin": 4.5,
        "kat": 24,
        "beklenen_sinif": "Yuksek Risk",
    },
    {
        "isim": "S7 - Guclendirilmis Yapi",
        "aciklama": "Yeni bina, iyi zemin, orta deprem, az katli",
        "deprem": 4.5,
        "bina_yasi": 3,
        "zemin": 8.8,
        "kat": 4,
        "beklenen_sinif": "Dusuk Risk",
    },
    {
        "isim": "S8 - Kritik Zemin Riski",
        "aciklama": "Zemin cok kotu, bina eski, orta-yuksek deprem",
        "deprem": 5.8,
        "bina_yasi": 55,
        "zemin": 0.8,
        "kat": 14,
        "beklenen_sinif": "Yuksek Risk",
    },
]


# ---------------------------------------------------------------------------
# HESAPLAMA
# ---------------------------------------------------------------------------

def senaryolari_hesapla():
    """
    Tum senaryolari hesaplayip sonuc listesi olarak dondurur.

    Donus
    ------
    list[dict]  Her eleman: senaryo alanlari + skor + sinif
    """
    sonuclar = []
    for s in SENARYOLAR:
        skor = hesapla_risk(
            deprem=s["deprem"],
            bina=s["bina_yasi"],
            zemin=s["zemin"],
            kat=s["kat"],
        )
        sonuclar.append({
            **s,
            "skor":  round(float(skor), 2),
            "sinif": siniflandir(skor),
        })
    return sonuclar


# ---------------------------------------------------------------------------
# TERMINALDEN CALISTIRMA
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("\n" + "=" * 110)
    print("  DEPREM SONRASI ACİL RİSK DEĞERLENDİRME SİSTEMİ — Test Senaryolari")
    print("=" * 110)

    sonuclar = senaryolari_hesapla()

    baslik = (
        f"{'#':<3} "
        f"{'Senaryo':<30} "
        f"{'Dep':>5} "
        f"{'Bina':>5} "
        f"{'Zemin':>6} "
        f"{'Kat':>4} "
        f"{'Skor':>7} "
        f"{'Sonuc':<18} "
        f"{'Beklenen':<18} "
        f"{'Durum'}"
    )
    print(baslik)
    print("-" * 110)

    tumu_gecti = True
    for i, s in enumerate(sonuclar, 1):
        eslesme = s["sinif"] == s["beklenen_sinif"]
        if not eslesme:
            tumu_gecti = False
        durum = "OK" if eslesme else "KONTROL ET"
        print(
            f"{i:<3} "
            f"{s['isim']:<30} "
            f"{s['deprem']:>5.1f} "
            f"{int(s['bina_yasi']):>5} "
            f"{s['zemin']:>6.1f} "
            f"{int(s['kat']):>4} "
            f"{s['skor']:>7.2f} "
            f"{s['sinif']:<18} "
            f"{s['beklenen_sinif']:<18} "
            f"{durum}"
        )

    print("=" * 110)
    sonuc_mesaj = (
        "  Tum senaryolar beklenen sınıfla uyumlu."
        if tumu_gecti
        else "  UYARI: Bazi senaryolar beklenen sınıfla uyuşmadi. Kural tabanını kontrol edin."
    )
    print(sonuc_mesaj)
    print()
