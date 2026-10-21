"""Aiqon beige/brown theme."""
import streamlit as st

def apply_styles():
    st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{--aiqon-ink:#49372B;--aiqon-muted:#78685B;--aiqon-line:#E7DCCB;--aiqon-panel:#FFFCF6;--aiqon-bg:#F5EFE4;--aiqon-teal:#8A5A3B;--aiqon-blue:#9A765B}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
[data-testid="stAppViewContainer"]{background:var(--aiqon-bg)}
[data-testid="stHeader"]{background:rgba(245,239,228,.94)}
[data-testid="stMainBlockContainer"]{max-width:1480px;padding-top:1.6rem;padding-bottom:3rem}
h1,h2,h3{font-family:'Manrope',sans-serif!important;color:var(--aiqon-ink);letter-spacing:-.035em}
h2{font-size:1.35rem!important;font-weight:750!important;margin-bottom:.25rem!important}
h3{font-size:1.03rem!important;font-weight:700!important}
p,label,[data-testid="stCaptionContainer"]{color:var(--aiqon-muted)}
[data-testid="stVerticalBlockBorderWrapper"]{background:var(--aiqon-panel);border:1px solid var(--aiqon-line);border-radius:16px;box-shadow:0 2px 8px rgba(73,55,43,.04)}
[data-testid="stMetric"]{background:#FFFCF6;border:1px solid var(--aiqon-line);padding:16px 18px;border-radius:14px;min-height:108px}
[data-testid="stMetricLabel"]{font-size:.82rem;font-weight:600;color:#78685B}
[data-testid="stMetricValue"]{font-family:'Manrope',sans-serif;color:var(--aiqon-ink);font-weight:800;font-size:1.55rem}
[data-testid="stSelectbox"] label,[data-testid="stNumberInput"] label,[data-testid="stSlider"] label{color:#59483C;font-size:.86rem;font-weight:650}
[data-testid="stSelectbox"] div[data-baseweb="select"]>div,[data-testid="stNumberInput"] input{border-radius:10px;border-color:#D8C8B5;background:#FFFCF6}
[data-testid="stBaseButton-primary"]{background:var(--aiqon-ink);border:1px solid var(--aiqon-ink);border-radius:10px;font-weight:700;min-height:2.7rem}
[data-testid="stBaseButton-primary"]:hover{background:#6E4933;border-color:#6E4933}
[data-testid="stBaseButton-secondary"]{border-radius:10px;font-weight:650}
[data-testid="stDataFrame"]{border:1px solid var(--aiqon-line);border-radius:12px;overflow:hidden}
hr{border-color:var(--aiqon-line);margin:1.4rem 0}
.aiqon-hero{background:linear-gradient(120deg,#49372B 0%,#6B4C39 65%,#9B7456 100%);color:#FFFCF6;border-radius:20px;padding:26px 30px;margin-bottom:18px;box-shadow:0 10px 26px rgba(73,55,43,.10)}
.aiqon-brand{font-family:'Manrope',sans-serif;font-size:.77rem;font-weight:800;text-transform:uppercase;letter-spacing:.16em;color:#E8C9A7;margin-bottom:8px}
.aiqon-hero-title{font-family:'Manrope',sans-serif;color:#FFFCF6;font-size:2rem;line-height:1.2;font-weight:800;letter-spacing:-.045em;margin:0 0 8px}
.aiqon-hero-subtitle{color:#F5E8D6;font-size:.98rem;margin:0;max-width:760px}
.aiqon-section-kicker{color:#8A5A3B;font-size:.72rem;font-weight:800;letter-spacing:.13em;text-transform:uppercase;margin-bottom:4px}
.aiqon-route-label{color:#78685B;font-size:.8rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;margin-bottom:5px}
.aiqon-route-id{color:#49372B;font-family:'Manrope',sans-serif;font-size:1.55rem;font-weight:800;letter-spacing:-.04em;margin:0}
.aiqon-route-path{color:#69584A;font-size:.92rem;line-height:1.6;margin-top:10px}
.aiqon-note{background:#FBF6ED;border:1px solid #E7DCCB;border-radius:12px;padding:12px 15px;color:#69584A;font-size:.86rem;line-height:1.55}
@media(max-width:768px){.aiqon-hero{padding:22px}.aiqon-hero-title{font-size:1.6rem}}
</style>""", unsafe_allow_html=True)
