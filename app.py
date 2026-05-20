"""
app.py
Deprem Sonrasi Acil Risk Degerlendirme Sistemi
Streamlit Arayuz Modulu

Calistirma:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as _plt

from fuzzy_system import hesapla_risk, aktif_kurallari_bul
from plots import (
    grafik_uyelik_fonksiyonlari,
    grafik_durulastirma,
    grafik_test_senaryolari,
)
from test_scenarios import senaryolari_hesapla, siniflandir

# ---------------------------------------------------------------------------
# SAYFA YAPILANDIRMASI
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Deprem Risk Degerlendirme",
    page_icon="seismic",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# GLOBAL CSS
# ---------------------------------------------------------------------------

st.markdown("""
<style>

/* ---- Genel arka plan ---- */
.stApp {
    background-color: #1E1E2E;
    color: #E0E0E0;
    font-family: 'Segoe UI', sans-serif;
}

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {
    background-color: #16162A;
    border-right: 1px solid #2A2A3E;
}
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #CFD8DC;
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    margin-top: 1.1rem;
    margin-bottom: 0.35rem;
}

/* ---- Slider ---- */
.stSlider label {
    color: #ECEFF1 !important;
    font-size: 0.88rem;
    font-weight: 500;
}
.stSlider span {
    color: #90CAF9 !important;
    font-weight: 600;
}

/* ---- Metrik kutulari ---- */
[data-testid="stMetric"] {
    background-color: #252535;
    border: 1px solid #3A3A4E;
    border-radius: 10px;
    padding: 14px 16px;
    min-height: 110px;
}
[data-testid="stMetricLabel"] { color: #90CAF9 !important; font-size: 0.76rem; }
[data-testid="stMetricValue"] { color: #E0E0E0 !important; font-size: 1.6rem; font-weight: 700; }

/* ---- Risk karti ---- */
.risk-card {
    border-radius: 10px;
    padding: 18px 22px;
    min-height: 110px;
    border-left: 5px solid;
    box-shadow: 0 3px 14px rgba(0,0,0,0.3);
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.risk-dusuk  { background: #0C1A28; border-color: #29B6F6; }
.risk-orta   { background: #1C1200; border-color: #FFA726; }
.risk-yuksek { background: #1C0800; border-color: #EF5350; }
.risk-kritik { background: #160000; border-color: #B71C1C; }

.risk-label   { font-size:0.72rem; letter-spacing:0.07em; text-transform:uppercase; opacity:0.7; margin-bottom:5px; }
.risk-value   { font-size:2.2rem; font-weight:700; line-height:1; }
.risk-sinif   { font-size:1.1rem; font-weight:600; margin-top:7px; }
.risk-aciklama{ font-size:0.82rem; opacity:0.85; margin-top:7px; line-height:1.55; }

/* ---- Kural satirlari ---- */
.kural-satir {
    background-color: #252535;
    border: 1px solid #3A3A4E;
    border-radius: 7px;
    padding: 8px 13px;
    margin: 4px 0;
    font-size: 0.80rem;
    font-family: 'Courier New', monospace;
    color: #D0D0E0;
}
.kural-aktif { border-left: 4px solid #4CAF50; }
.kural-zayif { border-left: 4px solid #FFA726; opacity: 0.80; }

/* ---- Sekmeler ---- */
[data-baseweb="tab-list"] { background-color: #252535; border-radius: 9px; padding: 3px; }
[data-baseweb="tab"]      { color: #90CAF9 !important; font-weight: 500; }

/* ---- Buton ---- */
.stButton > button {
    background-color: #1565C0;
    color: white; border: none; border-radius: 8px;
    font-size: 0.90rem; font-weight: 600;
    padding: 0.55rem 1.4rem; width: 100%;
    transition: background 0.2s;
}
.stButton > button:hover { background-color: #1E88E5; }

/* ---- Scrollbar ---- */
::-webkit-scrollbar       { width: 6px; }
::-webkit-scrollbar-thumb { background: #3A3A4E; border-radius: 8px; }

hr { border-color: #2A2A3E; }

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# YARDIMCI FONKSIYONLAR
# ---------------------------------------------------------------------------

def _risk_rengi(skor):
    if skor < 25:   return "#29B6F6"
    if skor < 50:   return "#FFA726"
    if skor < 75:   return "#EF5350"
    return "#B71C1C"


def _risk_css(sinif):
    return {
        "Dusuk Risk":  "risk-dusuk",
        "Orta Risk":   "risk-orta",
        "Yuksek Risk": "risk-yuksek",
        "Kritik Risk": "risk-kritik",
    }.get(sinif, "risk-dusuk")


def _risk_aciklama(sinif):
    return {
        "Dusuk Risk":  "Bina guvenli gorunmektedir. Standart tedbir yeterlidir.",
        "Orta Risk":   "Bina inceleme gerektirmektedir. Hasar tespiti onerilir.",
        "Yuksek Risk": "Tahliye degerlendirilmelidir. Uzman incelemesi sartdir.",
        "Kritik Risk": "Bina derhal tahliye edilmelidir. Acil mudahale ekibi gereklidir.",
    }.get(sinif, "")

# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("""
    <div style="color:#CFD8DC; font-size:1.15rem; font-weight:700; margin-bottom:8px;">
        Sistem Parametreleri
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### Deprem")
    deprem = st.slider(
        "Deprem Siddeti (Richter)",
        min_value=0.0, max_value=10.0, value=5.0, step=0.1,
        help="0: Hissedilmez  |  5: Orta siddtetli  |  10: Yikici"
    )

    st.markdown("### Bina")
    bina = st.slider(
        "Bina Yasi (Yıl)",
        min_value=0, max_value=80, value=30, step=1,
        help="Insaa tarihinden itibaren gecen sure"
    )
    kat = st.slider(
        "Kat Sayisi",
        min_value=1, max_value=30, value=8, step=1,
        help="Toplam kat adedi"
    )

    st.markdown("### Zemin")
    zemin = st.slider(
        "Zemin Durumu",
        min_value=0.0, max_value=10.0, value=5.0, step=0.1,
        help="0: Sivilasma riski yuksek  |  10: Kayalik / cok sagla"
    )

    st.markdown("---")
    hesapla_btn = st.button("Riski Hesapla", use_container_width=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.76rem; color:#90A4AE; line-height:1.75;
                background:#1A1A2E; padding:13px; border-radius:8px;
                border:1px solid #2F3552;">
        <b style="color:#CFD8DC;">Sistem Bilgisi</b><br>
        Cikarim   : <b>Mamdani</b><br>
        Durulaştırma: <b>Centroid</b><br>
        Kural Sayisi: <b>40</b><br>
        Giris Degiskeni: <b>4</b><br>
        Cikis Degiskeni: <b>1</b><br><br>
        <b style="color:#CFD8DC;">Zemin Olcegi</b><br>
        0 &rarr; Sivi / sivilasma riski<br>
        10 &rarr; Kayalik / sagla zemin
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# BASLIK
# ---------------------------------------------------------------------------

st.markdown("""
<div style="padding:14px 0 6px 0;">
    <h1 style="color:#90CAF9; font-size:1.5rem; font-weight:700; margin:0;">
        Deprem Sonrasi Acil Risk Degerlendirme Sistemi
    </h1>
    <p style="color:#7986CB; font-size:0.83rem; margin:3px 0 0 0;">
        Bulanik Mantik Tabanli Karar Destek Sistemi &nbsp;|&nbsp;
        Mamdani Cikarim &nbsp;|&nbsp; Centroid Durulaştırma
    </p>
</div>
<hr style="margin:6px 0 14px 0; border-color:#2A2A3E;">
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------------------------

if "skor" not in st.session_state:
    st.session_state["skor"] = None

# ---------------------------------------------------------------------------
# HESAPLAMA VE GOSTERIM
# ---------------------------------------------------------------------------

if hesapla_btn or st.session_state["skor"] is not None:

    if hesapla_btn:
        with st.spinner("Bulanik cikarim hesaplaniyor..."):
            skor    = hesapla_risk(deprem, bina, zemin, kat)
            sinif   = siniflandir(skor)
            kurallar = aktif_kurallari_bul(deprem, bina, zemin, kat)
        st.session_state.update({
            "skor": skor, "sinif": sinif, "kurallar": kurallar,
            "girisler": (deprem, bina, zemin, kat),
        })
    else:
        skor    = st.session_state["skor"]
        sinif   = st.session_state["sinif"]
        kurallar = st.session_state["kurallar"]
        deprem, bina, zemin, kat = st.session_state["girisler"]

    # ---- Risk karti + Metrikler ----
    kol1, kol2 = st.columns([1.25, 2.75])

    with kol1:
        st.markdown(f"""
        <div class="risk-card {_risk_css(sinif)}">
            <div class="risk-label">Hesaplanan Risk Skoru</div>
            <div class="risk-value" style="color:{_risk_rengi(skor)};">{skor:.1f}</div>
            <div class="risk-sinif" style="color:{_risk_rengi(skor)};">{sinif}</div>
            <div class="risk-aciklama">{_risk_aciklama(sinif)}</div>
        </div>
        """, unsafe_allow_html=True)

    with kol2:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Deprem Siddeti", f"{deprem:.1f}")
        m2.metric("Bina Yaşı",      f"{int(bina)} yıl")
        m3.metric("Zemin Durumu",   f"{zemin:.1f}")
        m4.metric("Kat Sayısı",     f"{int(kat)} kat")

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ---- Sekmeler ----
    t1, t2, t3, t4 = st.tabs([
        "Durulaştırma Grafiği",
        "Üyelik Fonksiyonları",
        "Aktif Kurallar",
        "Test Senaryoları",
    ])

    # -- Sekme 1: Durulaştırma --
    with t1:
        st.markdown("#### Centroid Durulaştırma Sonucu")
        st.caption(
            "Kesilmis (clipped) çıktı üyelik alanlari fill_between ile boyali gosterilmektedir. "
            "Beyaz dikey cizgi centroid (agirlik merkezi) noktasini isaretler."
        )
        fig_dur = grafik_durulastirma(deprem, bina, zemin, kat, skor)
        st.pyplot(fig_dur, use_container_width=True)
        _plt.close(fig_dur)

    # -- Sekme 2: Üyelik fonksiyonlari --
    with t2:
        st.markdown("#### Üyelik Fonksiyonlari — Aktif Bölgeler Vurgulandı")
        st.caption(
            "Mevcut giris degerine karsilik gelen aktivasyon noktasi her grafik uzerinde "
            "dolu daire ile isaretlenmis; aktif üyelik bolgesi dolgulu alan olarak gosterilmistir."
        )
        fig_uf = grafik_uyelik_fonksiyonlari(deprem, bina, zemin, kat, skor)
        st.pyplot(fig_uf, use_container_width=True)
        _plt.close(fig_uf)

    # -- Sekme 3: Aktif Kurallar --
    with t3:
        st.markdown(f"#### Aktif Kurallar &nbsp;({len(kurallar)} adet)")

        if not kurallar:
            st.info(
                "Mevcut parametre kombinasyonunda aktivasyon esigini (mu >= 0.05) "
                "gecen kural bulunamadi."
            )
        else:
            for k in kurallar:
                css  = "kural-aktif" if k["aktivasyon"] >= 0.3 else "kural-zayif"
                renk = "#4CAF50"    if k["aktivasyon"] >= 0.3 else "#FFA726"
                st.markdown(f"""
                <div class="kural-satir {css}">
                    <span style="color:#90CAF9; font-weight:600;">[K{k['kural_no']:02d}]</span>
                    &nbsp;{k['tanim']}
                    <span style="float:right; color:{renk}; font-weight:600;">
                        &mu; = {k['aktivasyon']:.4f}
                    </span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""
            <div style='font-size:0.76rem; color:#777; margin-top:8px;'>
            <b>Not:</b> Yesil = guclu aktif (mu &ge; 0.30), Turuncu = zayif aktif (mu &lt; 0.30)
            </div>
            """, unsafe_allow_html=True)

    # -- Sekme 4: Test Senaryolari --
    with t4:
        st.markdown("#### Onceden Tanimlanmis Test Senaryolari")

        with st.spinner("Senaryolar hesaplaniyor..."):
            sonuclar = senaryolari_hesapla()

        df_rows = []
        for s in sonuclar:
            df_rows.append({
                "Senaryo":         s["isim"],
                "Deprem Şiddeti":  s["deprem"],
                "Bina Yaşı (yıl)": int(s["bina_yasi"]),
                "Zemin Durumu":    s["zemin"],
                "Kat Sayısı":      int(s["kat"]),
                "Risk Skoru":      s["skor"],
                "Risk Sınıfı":     s["sinif"],
                "Beklenen":        s["beklenen_sinif"],
            })

        df = pd.DataFrame(df_rows)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Risk Skoru": st.column_config.NumberColumn(format="%.2f"),
            }
        )

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        st.markdown("#### Karsilastirmali Risk Grafigi")
        fig_test = grafik_test_senaryolari(sonuclar)
        st.pyplot(fig_test, use_container_width=True)
        _plt.close(fig_test)

# ---------------------------------------------------------------------------
# ILKIAKID EKRANI (Henuz hesap yapilmadi)
# ---------------------------------------------------------------------------

else:
    st.info(
        "Sistem hazir. Sol panelden parametre degerlerini belirleyin "
        "ve **Riski Hesapla** butonuna basin."
    )
    st.markdown("#### Üyelik Fonksiyonlari (Baslangic Görünümü)")
    fig_uf0 = grafik_uyelik_fonksiyonlari()
    st.pyplot(fig_uf0, use_container_width=True)
    _plt.close(fig_uf0)

# ---------------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------------

st.markdown("""
<hr style="margin:32px 0 8px 0; border-color:#2A2A3E;">
<div style="font-size:0.70rem; color:#444; text-align:center;">
    Deprem Sonrası Acil Risk Değerlendirme Sistemi &nbsp;|&nbsp;
    Python / scikit-fuzzy / Streamlit &nbsp;|&nbsp;
    Mamdani Cikarim &mdash; Centroid Durulaştırma
</div>
""", unsafe_allow_html=True)
