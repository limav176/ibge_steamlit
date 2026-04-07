import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="📊 População por UF – IBGE",
    page_icon="🇧🇷",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #0e1117; }
    .insight-card {
        background: linear-gradient(135deg, #1e2130, #252840);
        border-radius: 14px;
        padding: 20px 24px;
        border-left: 4px solid;
        margin-bottom: 8px;
    }
    .card-1 { border-color: #4f8ef7; }
    .card-2 { border-color: #f7844f; }
    .card-3 { border-color: #4ff7a0; }
    .card-4 { border-color: #f74f8e; }
    .insight-title { font-size: 1.05rem; font-weight: 700; margin-bottom: 6px; }
    .insight-text  { font-size: 0.88rem; color: #adb5bd; line-height: 1.5; }
    h1 { font-size: 2rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("/Users/valmirlima/Documents/py/br_ibge_populacao_uf.csv")
    df = df.dropna(subset=["sigla_uf"])
    df["ano"] = df["ano"].astype(int)
    df["populacao"] = df["populacao"].astype(int)
    return df

df = load_data()

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🇧🇷 População por Estado Brasileiro – IBGE (1991–2025)")
st.markdown("Dashboard interativo com os **4 principais insights** sobre a evolução populacional por UF.")
st.divider()

# ── Insight cards ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("""<div class="insight-card card-1">
        <div class="insight-title">🏆 São Paulo: gigante que só cresce</div>
        <div class="insight-text">De ~31,6 mi (1991) para ~46 mi (2025). Crescimento absoluto maior que a população inteira de Goiás.</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="insight-card card-3">
        <div class="insight-title">🚀 Roraima: maior crescimento proporcional</div>
        <div class="insight-text">+239% em 34 anos (217 mil → 738 mil). Influência direta da imigração venezuelana (2017–2021).</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown("""<div class="insight-card card-2">
        <div class="insight-title">📉 Nordeste cresce menos que o Centro-Sul</div>
        <div class="insight-text">Bahia cresceu ~26% desde 1991. SP cresceu ~46% no mesmo período, evidenciando fluxo migratório.</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="insight-card card-4">
        <div class="insight-title">🏙️ DF quase dobrou de tamanho</div>
        <div class="insight-text">1,6 mi (1991) → 3 mi (2025). Maior densidade per km² fora do litoral. Pressão crescente em infraestrutura.</div>
    </div>""", unsafe_allow_html=True)

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# INSIGHT 1 – SP vs outros maiores estados
# ═══════════════════════════════════════════════════════════════════════════════
st.subheader("📈 Insight 1 – São Paulo vs. Maiores Estados (1991–2025)")

top_states = ["SP", "MG", "RJ", "BA", "PR", "RS"]
df_top = df[df["sigla_uf"].isin(top_states)]

fig1 = px.line(
    df_top.sort_values("ano"),
    x="ano", y="populacao", color="sigla_uf",
    labels={"ano": "Ano", "populacao": "População", "sigla_uf": "Estado"},
    color_discrete_sequence=px.colors.qualitative.Bold,
    template="plotly_dark",
)
fig1.update_layout(
    plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    hovermode="x unified",
)
fig1.update_traces(line=dict(width=2.5))
st.plotly_chart(fig1, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# INSIGHT 2 – Crescimento proporcional Nordeste vs Centro-Sul
# ═══════════════════════════════════════════════════════════════════════════════
st.subheader("📉 Insight 2 – Crescimento Proporcional por Região (1991 → 2025)")

nordeste = ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"]
centro_sul = ["SP", "MG", "RJ", "PR", "RS", "SC", "GO", "DF", "MS", "MT"]

def calc_growth(states):
    rows = []
    for uf in states:
        d = df[df["sigla_uf"] == uf].sort_values("ano")
        if len(d) >= 2:
            pop91 = d[d["ano"] == d["ano"].min()]["populacao"].values[0]
            pop25 = d[d["ano"] == d["ano"].max()]["populacao"].values[0]
            growth = (pop25 - pop91) / pop91 * 100
            rows.append({"UF": uf, "Crescimento (%)": round(growth, 1)})
    return pd.DataFrame(rows)

df_ne  = calc_growth(nordeste)
df_cs  = calc_growth(centro_sul)
df_ne["Região"] = "Nordeste"
df_cs["Região"] = "Centro-Sul"
df_growth = pd.concat([df_ne, df_cs]).sort_values("Crescimento (%)", ascending=True)

fig2 = px.bar(
    df_growth, x="Crescimento (%)", y="UF", color="Região",
    orientation="h",
    color_discrete_map={"Nordeste": "#f7844f", "Centro-Sul": "#4f8ef7"},
    template="plotly_dark",
    labels={"UF": "Estado"},
)
fig2.update_layout(
    plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
st.plotly_chart(fig2, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# INSIGHT 3 – Roraima: explosão demográfica
# ═══════════════════════════════════════════════════════════════════════════════
st.subheader("🚀 Insight 3 – Roraima: Explosão Demográfica (1991–2025)")

col_rr, col_menor = st.columns([2, 1])

with col_rr:
    df_rr = df[df["sigla_uf"] == "RR"].sort_values("ano")
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=df_rr["ano"], y=df_rr["populacao"],
        mode="lines+markers",
        line=dict(color="#4ff7a0", width=3),
        marker=dict(size=7),
        fill="tozeroy",
        fillcolor="rgba(79, 247, 160, 0.10)",
        name="RR",
    ))
    fig3.add_vrect(x0=2016, x1=2022, fillcolor="rgba(247, 132, 79, 0.15)",
                   annotation_text="Crise venezuelana", annotation_position="top left",
                   line_width=0)
    fig3.update_layout(
        plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
        template="plotly_dark",
        xaxis_title="Ano", yaxis_title="População",
        showlegend=False,
    )
    st.plotly_chart(fig3, use_container_width=True)

with col_menor:
    st.metric("População 1991", "217.583")
    st.metric("População 2025", "738.772", delta="+239%")
    st.markdown("---")
    st.info("📌 Roraima tem a **menor** população absoluta do Brasil, mas o **maior crescimento relativo** desde 1991.")

# ═══════════════════════════════════════════════════════════════════════════════
# INSIGHT 4 – Mapa de população 2025
# ═══════════════════════════════════════════════════════════════════════════════
st.subheader("🗺️ Insight 4 – Distribuição Populacional por Estado (2025)")

df_2025 = df[df["ano"] == 2025].copy()

fig4 = px.bar(
    df_2025.sort_values("populacao", ascending=True),
    x="populacao", y="sigla_uf",
    orientation="h",
    color="populacao",
    color_continuous_scale="Viridis",
    labels={"populacao": "População", "sigla_uf": "Estado"},
    template="plotly_dark",
    text_auto=".2s",
)
fig4.update_layout(
    plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
    coloraxis_showscale=False,
    height=650,
)
fig4.update_traces(textfont_size=11, textposition="outside")
st.plotly_chart(fig4, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption("Fonte: IBGE – Estimativas de população por UF (1991–2025) | Dashboard por Valmir Lima")
