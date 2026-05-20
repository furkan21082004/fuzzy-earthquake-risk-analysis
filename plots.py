"""
plots.py
Deprem Sonrasi Acil Risk Değerlendirme Sistemi - Grafik Modulu

Tum grafikler Matplotlib ile olusturulur; Streamlit icinde st.pyplot() ile gosterilir.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from fuzzy_system import get_membership_data

# ---------------------------------------------------------------------------
# RENK PALETI
# ---------------------------------------------------------------------------

C = {
    "dusuk":  "#29B6F6",   # mavi
    "orta":   "#FFA726",   # turuncu
    "yuksek": "#EF5350",   # kirmizi
    "kritik": "#B71C1C",   # koyu kirmizi
    "bg":     "#1E1E2E",   # arka plan
    "panel":  "#252535",   # panel arka plan
    "grid":   "#3A3A4E",
    "text":   "#E0E0E0",
    "spine":  "#555566",
    "line":   "#FFFFFF",
}

MF_RENKLER = {
    # giris degiskenleri
    "Dusuk":      C["dusuk"],
    "Orta":       C["orta"],
    "Yuksek":     C["yuksek"],
    "Yeni":       C["dusuk"],
    "Orta_Yasli": C["orta"],
    "Eski":       C["yuksek"],
    "Kotu":       C["kritik"],
    "Iyi":        C["dusuk"],
    "Az_Katli":   C["dusuk"],
    "Orta_Katli": C["orta"],
    "Cok_Katli":  C["yuksek"],
    # cikis
    "Kritik":     C["kritik"],
}

ETIKET = {
    "Dusuk":      "Dusuk",
    "Orta":       "Orta",
    "Yuksek":     "Yuksek",
    "Yeni":       "Yeni",
    "Orta_Yasli": "Orta Yasli",
    "Eski":       "Eski",
    "Kotu":       "Kotu",
    "Iyi":        "Iyi",
    "Az_Katli":   "Az Katli",
    "Orta_Katli": "Orta Katli",
    "Cok_Katli":  "Cok Katli",
    "Kritik":     "Kritik",
}

# ---------------------------------------------------------------------------
# YARDIMCI: EKSENE STIL UYGULA
# ---------------------------------------------------------------------------

def _stil(ax, title="", xlabel="", ylabel="Üyelik Derecesi"):
    ax.set_facecolor(C["panel"])
    ax.grid(True, color=C["grid"], alpha=0.25, linewidth=0.7)
    ax.set_ylim(-0.04, 1.12)
    ax.tick_params(colors=C["text"], labelsize=9)
    ax.set_xlabel(xlabel, color=C["text"], fontsize=9)
    ax.set_ylabel(ylabel, color=C["text"], fontsize=9)
    ax.set_title(title, color=C["text"], fontsize=11, fontweight="bold", pad=8)
    for sp in ax.spines.values():
        sp.set_color(C["spine"])
    ax.xaxis.label.set_color(C["text"])
    ax.yaxis.label.set_color(C["text"])

# ---------------------------------------------------------------------------
# YARDIMCI: TEK DEGISKEN CIZIMI (fill_between + dikey cizgi + aktivasyon noktasi)
# ---------------------------------------------------------------------------

def _ciz_degisken(ax, evren, mf_dict, deger=None, title="", xlabel=""):
    """
    Bir degiskenin tum üyelik fonksiyonlarini cizer.
    deger verilirse:
      - Her MF icin aktif aktivasyon noktasini dolgulu gosterir
      - Dikey cizgi cizer
    """
    for isim, mf in mf_dict.items():
        renk = MF_RENKLER.get(isim, C["orta"])
        etk  = ETIKET.get(isim, isim)

        # Cizgi
        ax.plot(evren, mf, color=renk, linewidth=2.2, label=etk, zorder=3)

        if deger is not None:
            # Tum MF alani hafif dolgulu
            ax.fill_between(evren, 0, mf, color=renk, alpha=0.10, zorder=1)

            # Aktif aktivasyon degeri
            aktif = float(np.interp(deger, evren, mf))
            if aktif > 0.005:
                # Kesilmis (aktif) bolgeyi koyu dolgulu goster
                kesilmis = np.minimum(mf, aktif)
                ax.fill_between(evren, 0, kesilmis, color=renk, alpha=0.42, zorder=2)
                # Aktivasyon noktasini isaretcik ile goster
                ax.plot(deger, aktif, "o", color=renk, markersize=7,
                        markeredgecolor="white", markeredgewidth=1.2, zorder=5)
                # Yatay kesik cizgi (aktivasyon yuksekligi)
                ax.axhline(aktif, color=renk, linestyle="--", linewidth=0.8,
                           alpha=0.5, zorder=2)
        else:
            ax.fill_between(evren, 0, mf, color=renk, alpha=0.12, zorder=1)

    if deger is not None:
        # Dikey cizgi (mevcut giris degeri)
        ax.axvline(deger, color=C["line"], linestyle="--", linewidth=1.6,
                   alpha=0.85, zorder=4, label=f"Giris = {deger:.2f}")

    _stil(ax, title=title, xlabel=xlabel)
    ax.legend(fontsize=8, facecolor=C["bg"], edgecolor=C["spine"],
              labelcolor=C["text"], loc="upper right")

# ---------------------------------------------------------------------------
# GRAFIK 1: UYELIK FONKSIYONLARI (5 alt grafik)
# ---------------------------------------------------------------------------

def grafik_uyelik_fonksiyonlari(deprem=None, bina=None, zemin=None, kat=None, risk_skoru=None):
    """
    4 giris + 1 cikis degiskeninin üyelik fonksiyonlarini cizer.
    Deger parametreleri verilirse aktif bolgeler vurgulanir.
    """
    veri = get_membership_data()

    fig, eksenler = plt.subplots(5, 1, figsize=(11, 20))
    fig.patch.set_facecolor(C["bg"])
    fig.subplots_adjust(hspace=0.45)

    _ciz_degisken(
        eksenler[0],
        veri["deprem"]["universe"],
        veri["deprem"]["mfs"],
        deger=deprem,
        title="Deprem Siddeti Üyelik Fonksiyonlari",
        xlabel="Richter Ölçeği (0 = hissedilmez, 10 = yıkıcı)"
    )

    _ciz_degisken(
        eksenler[1],
        veri["bina"]["universe"],
        veri["bina"]["mfs"],
        deger=bina,
        title="Bina Yasi Üyelik Fonksiyonlari",
        xlabel="Bina Yasi (yil)"
    )

    _ciz_degisken(
        eksenler[2],
        veri["zemin"]["universe"],
        veri["zemin"]["mfs"],
        deger=zemin,
        title="Zemin Durumu Üyelik Fonksiyonlari",
        xlabel="Zemin Kalitesi (0 = kotu / sivilasma riski, 10 = kayalik)"
    )

    _ciz_degisken(
        eksenler[3],
        veri["kat"]["universe"],
        veri["kat"]["mfs"],
        deger=kat,
        title="Kat Sayisi Üyelik Fonksiyonlari",
        xlabel="Kat Adedi"
    )

    _ciz_degisken(
        eksenler[4],
        veri["risk"]["universe"],
        veri["risk"]["mfs"],
        deger=risk_skoru,  # cikis degiskeninde dikey cizgi gostermiyoruz
        title="Risk Seviyesi Üyelik Fonksiyonlari (Cikis)",
        xlabel="Risk Skoru (0 - 100)"
    )

    return fig

# ---------------------------------------------------------------------------
# YARDIMCI: CIKTI AKTIVASYONLARINI HESAPLA
# ---------------------------------------------------------------------------

def _cikti_aktivasyonlari(deprem, bina, zemin, kat):
    """
    Her cikis sinifi (Dusuk/Orta/Yuksek/Kritik) icin en buyuk kural aktivasyonunu dondurur.
    Bu fonksiyondaki kural mantigi fuzzy_system.py ile uyumlu tutulmustur.
    """
    veri = get_membership_data()
    dep_x = veri["deprem"]["universe"]
    bin_x = veri["bina"]["universe"]
    zem_x = veri["zemin"]["universe"]
    kat_x = veri["kat"]["universe"]

    def mu(x, evren, mf):
        return float(np.interp(x, evren, mf))

    dep_d = mu(deprem, dep_x, veri["deprem"]["mfs"]["Dusuk"])
    dep_o = mu(deprem, dep_x, veri["deprem"]["mfs"]["Orta"])
    dep_y = mu(deprem, dep_x, veri["deprem"]["mfs"]["Yuksek"])

    bin_y = mu(bina, bin_x, veri["bina"]["mfs"]["Yeni"])
    bin_o = mu(bina, bin_x, veri["bina"]["mfs"]["Orta_Yasli"])
    bin_e = mu(bina, bin_x, veri["bina"]["mfs"]["Eski"])

    zem_k = mu(zemin, zem_x, veri["zemin"]["mfs"]["Kotu"])
    zem_o = mu(zemin, zem_x, veri["zemin"]["mfs"]["Orta"])
    zem_i = mu(zemin, zem_x, veri["zemin"]["mfs"]["Iyi"])

    kat_a = mu(kat, kat_x, veri["kat"]["mfs"]["Az_Katli"])
    kat_o = mu(kat, kat_x, veri["kat"]["mfs"]["Orta_Katli"])
    kat_c = mu(kat, kat_x, veri["kat"]["mfs"]["Cok_Katli"])

    kritik = max(
        min(dep_y, zem_k, bin_e),
        min(dep_y, zem_k, kat_c),
        min(dep_y, bin_e, kat_c),
        min(dep_y, zem_k),
        min(zem_k, bin_e, kat_c),
        min(dep_y, bin_e, zem_o),
        min(dep_o, zem_k, bin_e, kat_c),
        min(dep_y, zem_o, bin_e),
    )

    yuksek = max(
        min(dep_y, zem_o, kat_c),
        min(dep_y, zem_i, bin_e),
        min(dep_y, bin_y, zem_k),
        min(dep_o, zem_k, bin_e),
        min(dep_o, zem_k, kat_c),
        min(dep_y, bin_o, zem_o),
        min(dep_y, kat_c),
        min(zem_k, bin_o, kat_c),
        min(dep_o, bin_e, kat_c),
        min(dep_o, zem_k, bin_o),
        min(dep_o, zem_k, kat_o),
        min(dep_y, zem_i, bin_o),
    )

    orta = max(
        min(dep_o, zem_o, bin_o),
        min(dep_o, zem_i, bin_e),
        min(dep_o, zem_k, bin_y),
        min(dep_d, zem_k, bin_e),
        min(dep_d, zem_k, kat_c),
        min(dep_y, zem_i, bin_y),
        min(dep_o, bin_o, kat_o),
        min(dep_d, zem_k, bin_o),
        min(dep_d, zem_k, kat_o),
        min(dep_d, bin_o, kat_o),
        min(dep_d, zem_k),
        min(dep_o, zem_o, kat_o),
        min(dep_o, zem_i, bin_o),
        min(dep_d, zem_o, bin_o),
        min(dep_d, zem_o, kat_o),
    )

    dusuk = max(
        min(dep_d, zem_i, bin_y),
        min(dep_d, zem_i, kat_a),
        min(dep_d, zem_o, bin_y),
        min(dep_d, bin_y, kat_a),
        min(dep_d, zem_i, bin_o, kat_a),
    )

    return {"Dusuk": dusuk, "Orta": orta, "Yuksek": yuksek, "Kritik": kritik}

# ---------------------------------------------------------------------------
# GRAFIK 2: DURULASTIRMA (Centroid)
# ---------------------------------------------------------------------------

def grafik_durulastirma(deprem, bina, zemin, kat, skor):
    """
    Mamdani cikarimi sonucunda olusan cikti üyelik alanini ve centroid noktasini gosterir.
    Kesilmis (clipped) üyelik alanlari fill_between ile boyali gosterilir.
    """
    veri = get_membership_data()
    risk_x = veri["risk"]["universe"]

    mf_d = veri["risk"]["mfs"]["Dusuk"]
    mf_o = veri["risk"]["mfs"]["Orta"]
    mf_y = veri["risk"]["mfs"]["Yuksek"]
    mf_k = veri["risk"]["mfs"]["Kritik"]

    akt = _cikti_aktivasyonlari(deprem, bina, zemin, kat)

    clip_d = np.minimum(mf_d, akt["Dusuk"])
    clip_o = np.minimum(mf_o, akt["Orta"])
    clip_y = np.minimum(mf_y, akt["Yuksek"])
    clip_k = np.minimum(mf_k, akt["Kritik"])

    birlesis = np.maximum.reduce([clip_d, clip_o, clip_y, clip_k])

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor(C["bg"])

    # -- Tam uyelik egrileri (ince, transparan) --
    ax.plot(risk_x, mf_d, color=C["dusuk"],  linewidth=1.4, alpha=0.4, linestyle="--")
    ax.plot(risk_x, mf_o, color=C["orta"],   linewidth=1.4, alpha=0.4, linestyle="--")
    ax.plot(risk_x, mf_y, color=C["yuksek"], linewidth=1.4, alpha=0.4, linestyle="--")
    ax.plot(risk_x, mf_k, color=C["kritik"], linewidth=1.4, alpha=0.4, linestyle="--")

    # -- Kesilmis (aktif) alanlar -- fill_between --
    ax.fill_between(risk_x, 0, clip_d,
                    color=C["dusuk"],  alpha=0.55, label=f"Dusuk  (akt={akt['Dusuk']:.3f})")
    ax.fill_between(risk_x, 0, clip_o,
                    color=C["orta"],   alpha=0.55, label=f"Orta   (akt={akt['Orta']:.3f})")
    ax.fill_between(risk_x, 0, clip_y,
                    color=C["yuksek"], alpha=0.55, label=f"Yuksek (akt={akt['Yuksek']:.3f})")
    ax.fill_between(risk_x, 0, clip_k,
                    color=C["kritik"], alpha=0.55, label=f"Kritik (akt={akt['Kritik']:.3f})")

    # -- Birlesen cikti alani (taramali) --
    ax.fill_between(risk_x, 0, birlesis,
                    color="white", alpha=0.07,
                    hatch="///", edgecolor="white", linewidth=0.0,
                    label="Birlesik Cikti Alani")

    # -- Centroid dikey cizgisi --
    ax.axvline(
        skor, color="white", linestyle="-", linewidth=2.5, zorder=6,
        label=f"Centroid = {skor:.1f}"
    )
    ax.plot(skor, 0, marker="^", color="white", markersize=10,
            markeredgecolor="#aaa", zorder=7)

    # -- Bilgi kutusu --
    bilgi = (
        f"Giris Degerleri\n"
        f"{'Deprem':12s}: {deprem:.1f} Richter\n"
        f"{'Bina Yasi':12s}: {int(bina)} yil\n"
        f"{'Zemin':12s}: {zemin:.1f}\n"
        f"{'Kat Sayisi':12s}: {int(kat)}\n\n"
        f"Kural Aktivasyonlari\n"
        f"{'Dusuk':12s}: {akt['Dusuk']:.3f}\n"
        f"{'Orta':12s}: {akt['Orta']:.3f}\n"
        f"{'Yuksek':12s}: {akt['Yuksek']:.3f}\n"
        f"{'Kritik':12s}: {akt['Kritik']:.3f}"
    )
    ax.text(
        0.013, 0.97, bilgi,
        transform=ax.transAxes,
        fontsize=8.5,
        verticalalignment="top",
        fontfamily="monospace",
        bbox=dict(boxstyle="round,pad=0.6", facecolor="#1A1A2E",
                  edgecolor="#555566", alpha=0.92),
        color=C["text"],
        zorder=8,
    )

    # -- Risk sinifi esik cizgileri --
    for esik, renk, etiket in [(25, C["orta"], "25"), (50, C["yuksek"], "50"), (75, C["kritik"], "75")]:
        ax.axvline(esik, color=renk, linewidth=0.8, linestyle=":", alpha=0.6)
        ax.text(esik + 0.8, 1.02, etiket, color=renk, fontsize=7.5, alpha=0.8)

    _stil(ax, title="Durulastirma Sonucu — Centroid Yontemi (Mamdani)",
          xlabel="Risk Skoru (0 = dusuk risk, 100 = kritik risk)")
    ax.set_ylim(-0.06, 1.14)

    ax.legend(loc="upper right", fontsize=8.5,
              facecolor=C["bg"], edgecolor=C["spine"], labelcolor=C["text"])

    fig.tight_layout()
    return fig

# ---------------------------------------------------------------------------
# GRAFIK 3: TEST SENARYOLARI BAR GRAFIGI
# ---------------------------------------------------------------------------
def grafik_test_senaryolari(sonuclar):
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(C["bg"])
    ax.set_facecolor(C["panel"])

    isimler = [s["isim"].split(" - ")[0] for s in sonuclar]
    skorlar = [s["skor"] for s in sonuclar]

    def bar_rengi(skor):
        if skor < 25:
            return C["dusuk"]
        if skor < 50:
            return C["orta"]
        if skor < 75:
            return C["yuksek"]
        return C["kritik"]

    renkler = [bar_rengi(skor) for skor in skorlar]

    x = np.arange(len(isimler))
    bars = ax.bar(x, skorlar, color=renkler, width=0.55)

    for bar, skor in zip(bars, skorlar):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            skor + 1.5,
            f"{skor:.1f}",
            ha="center",
            va="bottom",
            color=C["text"],
            fontsize=9,
            fontweight="bold"
        )

    ax.axhspan(0, 25, alpha=0.06, color=C["dusuk"])
    ax.axhspan(25, 50, alpha=0.06, color=C["orta"])
    ax.axhspan(50, 75, alpha=0.06, color=C["yuksek"])
    ax.axhspan(75, 100, alpha=0.06, color=C["kritik"])

    ax.axhline(25, color=C["dusuk"], linestyle="--", linewidth=1, alpha=0.6)
    ax.axhline(50, color=C["orta"], linestyle="--", linewidth=1, alpha=0.6)
    ax.axhline(75, color=C["yuksek"], linestyle="--", linewidth=1, alpha=0.6)

    ax.set_title("Test Senaryolari - Risk Skoru Karsilastirmasi",
                 color=C["text"], fontsize=12, fontweight="bold")
    ax.set_xlabel("Senaryolar", color=C["text"])
    ax.set_ylabel("Risk Skoru", color=C["text"])
    ax.set_ylim(0, 105)

    ax.set_xticks(x)
    ax.set_xticklabels(isimler, rotation=0, color=C["text"], fontsize=9)

    ax.tick_params(colors=C["text"])
    ax.grid(axis="y", color=C["grid"], alpha=0.25)

    for sp in ax.spines.values():
        sp.set_color(C["spine"])

    ax.legend(
        handles=[
            mpatches.Patch(color=C["dusuk"], label="Dusuk Risk"),
            mpatches.Patch(color=C["orta"], label="Orta Risk"),
            mpatches.Patch(color=C["yuksek"], label="Yuksek Risk"),
            mpatches.Patch(color=C["kritik"], label="Kritik Risk"),
        ],
        loc="upper left",
        fontsize=8,
        facecolor=C["bg"],
        edgecolor=C["spine"],
        labelcolor=C["text"]
    )

    fig.tight_layout()
    return fig