import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ──────────────────────────────────────────────
# 페이지 설정
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="🏆 AI Battle Royale",
    page_icon="🏆",
    layout="wide",
)

# ──────────────────────────────────────────────
# 커스텀 CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Noto+Sans+KR:wght@400;700;900&display=swap');

.stApp {
    background: linear-gradient(135deg, #0a0a1a 0%, #1a0a2e 50%, #0a1628 100%);
}

.main-title {
    text-align: center;
    padding: 1rem 0;
}
.main-title h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.8rem;
    font-weight: 900;
    background: linear-gradient(90deg, #f9d423, #ff4e50, #f9d423);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 3s linear infinite;
    margin-bottom: 0;
}
@keyframes shine {
    to { background-position: 200% center; }
}
.main-title p {
    font-family: 'Noto Sans KR', sans-serif;
    color: #8888aa;
    font-size: 1rem;
    margin-top: 0.3rem;
}

.metric-row {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin: 1rem 0 1.5rem 0;
    flex-wrap: wrap;
}
.metric-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1rem 2.5rem;
    text-align: center;
    backdrop-filter: blur(10px);
}
.metric-card .num {
    font-family: 'Orbitron', sans-serif;
    font-size: 2rem;
    font-weight: 900;
    color: #f9d423;
}
.metric-card .label {
    font-family: 'Noto Sans KR', sans-serif;
    color: #8888aa;
    font-size: 0.85rem;
    margin-top: 0.2rem;
}

.section-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #ffffff;
    margin: 2rem 0 0.5rem 0;
    padding-left: 0.5rem;
    border-left: 4px solid #f9d423;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

/* 포디움 */
.podium-container {
    display: flex;
    justify-content: center;
    align-items: flex-end;
    gap: 1.2rem;
    padding: 2rem 0 0 0;
}
.podium-item {
    display: flex;
    flex-direction: column;
    align-items: center;
}
.podium-avatar {
    font-size: 3.5rem;
    margin-bottom: 0.5rem;
    animation: float 3s ease-in-out infinite;
}
.podium-avatar.gold { animation-delay: 0s; }
.podium-avatar.silver { animation-delay: 0.5s; }
.podium-avatar.bronze { animation-delay: 1s; }
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}
.podium-name {
    font-family: 'Orbitron', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    margin-bottom: 0.3rem;
}
.podium-votes {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 0.85rem;
    color: #aaa;
    margin-bottom: 0.5rem;
}
.podium-base {
    border-radius: 10px 10px 0 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Orbitron', sans-serif;
    font-size: 2rem;
    font-weight: 900;
    color: rgba(0,0,0,0.4);
    min-width: 140px;
}
.podium-1 {
    background: linear-gradient(180deg, #f9d423, #f5a623);
    height: 160px;
    box-shadow: 0 0 30px rgba(249,212,35,0.4);
}
.podium-2 {
    background: linear-gradient(180deg, #c0c0c0, #8a8a8a);
    height: 115px;
    box-shadow: 0 0 20px rgba(192,192,192,0.3);
}
.podium-3 {
    background: linear-gradient(180deg, #cd7f32, #a0522d);
    height: 80px;
    box-shadow: 0 0 15px rgba(205,127,50,0.3);
}

/* 리더보드 */
.leaderboard { max-width: 550px; margin: 1rem auto 0 auto; }
.lb-row {
    display: flex;
    align-items: center;
    padding: 0.7rem 1rem;
    margin: 0.4rem 0;
    border-radius: 12px;
    font-family: 'Noto Sans KR', sans-serif;
    transition: transform 0.2s;
}
.lb-row:hover { transform: scale(1.02); }
.lb-row.rank-1 {
    background: linear-gradient(90deg, rgba(249,212,35,0.2), transparent);
    border: 1px solid rgba(249,212,35,0.3);
}
.lb-row.rank-2 {
    background: linear-gradient(90deg, rgba(192,192,192,0.15), transparent);
    border: 1px solid rgba(192,192,192,0.2);
}
.lb-row.rank-3 {
    background: linear-gradient(90deg, rgba(205,127,50,0.15), transparent);
    border: 1px solid rgba(205,127,50,0.2);
}
.lb-rank {
    font-family: 'Orbitron', sans-serif;
    font-weight: 900;
    font-size: 1.2rem;
    width: 40px;
    text-align: center;
}
.lb-rank.r1 { color: #f9d423; }
.lb-rank.r2 { color: #c0c0c0; }
.lb-rank.r3 { color: #cd7f32; }
.lb-icon { font-size: 1.6rem; margin: 0 0.8rem; }
.lb-name { flex: 1; font-weight: 700; font-size: 1.05rem; color: #eee; }
.lb-bar-bg {
    flex: 1.5;
    height: 10px;
    background: rgba(255,255,255,0.08);
    border-radius: 5px;
    margin: 0 1rem;
    overflow: hidden;
}
.lb-bar-fill { height: 100%; border-radius: 5px; }
.lb-score {
    font-family: 'Orbitron', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    color: #f9d423;
}

/* 응답자 칩 */
.voter-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.7rem;
    justify-content: center;
    padding: 1rem 0;
}
.voter-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border-radius: 30px;
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 0.85rem;
    color: #ddd;
    border: 1px solid rgba(255,255,255,0.1);
    background: rgba(255,255,255,0.04);
}
.voter-chip .school-dot {
    width: 8px; height: 8px; border-radius: 50%; display: inline-block;
}

.footer {
    text-align: center;
    color: #555;
    font-size: 0.8rem;
    padding: 2rem 0 1rem 0;
    font-family: 'Noto Sans KR', sans-serif;
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# 데이터
# ──────────────────────────────────────────────
responses = [
    {"학교": "당곡고", "이름": "김한별", "1위": "Claude", "2위": "Gemini", "3위": "ChatGPT"},
    {"학교": "당곡고", "이름": "변시현", "1위": "Claude", "2위": "Gemini", "3위": "ChatGPT"},
    {"학교": "수도여고", "이름": "신연서", "1위": "Claude", "2위": "ChatGPT", "3위": "Gemini"},
    {"학교": "당곡고", "이름": "이마루", "1위": "Gemini", "2위": "Claude", "3위": "ChatGPT"},
    {"학교": "수도여고", "이름": "최윤영", "1위": "Gemini", "2위": "Claude", "3위": "ChatGPT"},
    {"학교": "당곡고", "이름": "이지훈", "1위": "Claude", "2위": "Gemini", "3위": "ChatGPT"},
    {"학교": "수도여고", "이름": "조윤서", "1위": "Claude", "2위": "Gemini", "3위": "ChatGPT"},
    {"학교": "당곡고", "이름": "김도연", "1위": "Claude", "2위": "Gemini", "3위": "ChatGPT"},
    {"학교": "수도여고", "이름": "이서영", "1위": "Claude", "2위": "ChatGPT", "3위": "Gemini"},
    {"학교": "당곡고", "이름": "이한규", "1위": "Claude", "2위": "Gemini", "3위": "ChatGPT"},
    {"학교": "당곡고", "이름": "김준영", "1위": "Claude", "2위": "Gemini", "3위": "ChatGPT"},
]

df = pd.DataFrame(responses)
AI_LIST = ["Claude", "Gemini", "ChatGPT"]
RANK_COLS = ["1위", "2위", "3위"]
total = len(df)

COLORS = {"Claude": "#E07B39", "Gemini": "#4285F4", "ChatGPT": "#10A37F"}
COLORS_RGBA_FILL = {
    "Claude": "rgba(224,123,57,0.13)",
    "Gemini": "rgba(66,133,244,0.13)",
    "ChatGPT": "rgba(16,163,127,0.13)",
}
AI_EMOJI = {"Claude": "🟠", "Gemini": "🔵", "ChatGPT": "🟢"}
SCHOOL_DOT = {"당곡고": "#6366F1", "수도여고": "#EC4899"}

first_counts = df["1위"].value_counts().reindex(AI_LIST, fill_value=0)

rank_map = {ai: [] for ai in AI_LIST}
for _, row in df.iterrows():
    for rank_idx, col in enumerate(RANK_COLS, 1):
        rank_map[row[col]].append(rank_idx)
avg_ranks = {ai: sum(v) / len(v) for ai, v in rank_map.items()}

scores = {ai: 0 for ai in AI_LIST}
for _, row in df.iterrows():
    scores[row["1위"]] += 3
    scores[row["2위"]] += 2
    scores[row["3위"]] += 1
sorted_ai = sorted(scores.items(), key=lambda x: x[1], reverse=True)

# ──────────────────────────────────────────────
# 헤더
# ──────────────────────────────────────────────
st.markdown("""
<div class="main-title">
    <h1>🏆 AI BATTLE ROYALE 🏆</h1>
    <p>당곡고 × 수도여고 — 최고의 AI를 가려라!</p>
</div>
""", unsafe_allow_html=True)

dangok = len(df[df["학교"] == "당곡고"])
sudo = len(df[df["학교"] == "수도여고"])

st.markdown(f"""
<div class="metric-row">
    <div class="metric-card">
        <div class="num">{total}</div>
        <div class="label">⚔️ 총 참전 용사</div>
    </div>
    <div class="metric-card">
        <div class="num">{dangok}</div>
        <div class="label">🔮 당곡고</div>
    </div>
    <div class="metric-card">
        <div class="num">{sudo}</div>
        <div class="label">💎 수도여고</div>
    </div>
    <div class="metric-card">
        <div class="num">{sorted_ai[0][1]}</div>
        <div class="label">👑 최고 점수</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# 🏆 포디움 + 리더보드
# ──────────────────────────────────────────────
st.markdown('<div class="section-title">🏆 FINAL STANDINGS</div>', unsafe_allow_html=True)

rank_emojis = ["👑", "🥈", "🥉"]
rank_colors_name = ["#f9d423", "#c0c0c0", "#cd7f32"]

order = [1, 0, 2]
podium_html = '<div class="podium-container">'
for idx in order:
    ai_name, score = sorted_ai[idx]
    medal_class = ["gold", "silver", "bronze"][idx]
    podium_class = f"podium-{idx+1}"
    podium_html += f"""
    <div class="podium-item">
        <div class="podium-avatar {medal_class}">{rank_emojis[idx]}</div>
        <div class="podium-name" style="color:{rank_colors_name[idx]}">{ai_name}</div>
        <div class="podium-votes">{score}pts · 1위 {first_counts.get(ai_name, 0)}표</div>
        <div class="podium-base {podium_class}">{idx+1}</div>
    </div>
    """
podium_html += '</div>'
st.markdown(podium_html, unsafe_allow_html=True)

max_score = sorted_ai[0][1]
lb_html = '<div class="leaderboard">'
for idx, (ai_name, score) in enumerate(sorted_ai):
    pct = (score / max_score) * 100
    bar_color = COLORS[ai_name]
    lb_html += f"""
    <div class="lb-row rank-{idx+1}">
        <div class="lb-rank r{idx+1}">{rank_emojis[idx]}</div>
        <div class="lb-icon">{AI_EMOJI[ai_name]}</div>
        <div class="lb-name">{ai_name}</div>
        <div class="lb-bar-bg">
            <div class="lb-bar-fill" style="width:{pct}%; background:linear-gradient(90deg, {bar_color}, {bar_color}aa);"></div>
        </div>
        <div class="lb-score">{score}pts</div>
    </div>
    """
lb_html += '</div>'
st.markdown(lb_html, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# 🍩 도넛 + 🕸️ 레이더
# ──────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.markdown('<div class="section-title">🍩 1위 득표 점유율</div>', unsafe_allow_html=True)

    fig_donut = go.Figure(data=[go.Pie(
        labels=first_counts.index.tolist(),
        values=first_counts.values.tolist(),
        hole=0.6,
        marker=dict(
            colors=[COLORS[ai] for ai in first_counts.index],
            line=dict(color="#0a0a1a", width=3),
        ),
        textinfo="label+percent",
        textfont=dict(size=14, family="Orbitron, sans-serif", color="white"),
        hovertemplate="<b>%{label}</b><br>%{value}표 (%{percent})<extra></extra>",
        pull=[0.05 if ai == sorted_ai[0][0] else 0 for ai in first_counts.index],
    )])
    fig_donut.update_layout(
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=420,
        margin=dict(t=20, b=20, l=20, r=20),
        annotations=[dict(
            text=f"<b>{sorted_ai[0][0]}</b><br>👑 WINNER",
            x=0.5, y=0.5, font=dict(size=18, color="#f9d423", family="Orbitron"),
            showarrow=False,
        )],
    )
    st.plotly_chart(fig_donut, use_container_width=True)

with col_right:
    st.markdown('<div class="section-title">🕸️ AI 역량 레이더</div>', unsafe_allow_html=True)

    categories = ["1위 득표", "평균 순위", "종합 점수", "2위 이상 비율", "압도적 지지"]

    def normalize(val, min_v, max_v):
        if max_v == min_v:
            return 50
        return ((val - min_v) / (max_v - min_v)) * 100

    radar_data = {}
    for ai in AI_LIST:
        first_v = first_counts.get(ai, 0)
        score_v = scores[ai]
        top2 = sum(1 for _, row in df.iterrows() if row["1위"] == ai or row["2위"] == ai)
        top2_pct = top2 / total * 100
        dominant = first_v / total * 100

        radar_data[ai] = [
            normalize(first_v, 0, max(first_counts.values)),
            normalize(3 - avg_ranks[ai], 0, 2),
            normalize(score_v, min(scores.values()), max(scores.values())),
            top2_pct,
            dominant,
        ]

    fig_radar = go.Figure()
    for ai in AI_LIST:
        vals = radar_data[ai] + [radar_data[ai][0]]
        cats = categories + [categories[0]]
        fig_radar.add_trace(go.Scatterpolar(
            r=vals, theta=cats,
            fill="toself",
            fillcolor=COLORS_RGBA_FILL[ai],
            line=dict(color=COLORS[ai], width=2.5),
            marker=dict(size=6, color=COLORS[ai]),
            name=ai,
            hovertemplate=f"<b>{ai}</b><br>" + "%{theta}: %{r:.0f}<extra></extra>",
        ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.08)", tickfont=dict(size=9, color="#555")),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.1)", tickfont=dict(size=11, color="#aaa", family="Noto Sans KR")),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=420,
        margin=dict(t=30, b=30, l=60, r=60),
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5,
            font=dict(size=12, color="#ccc", family="Orbitron"), bgcolor="rgba(0,0,0,0)",
        ),
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# ──────────────────────────────────────────────
# ⚔️ 학교 대항전 + 🗺️ 히트맵
# ──────────────────────────────────────────────
col_b1, col_b2 = st.columns(2)

with col_b1:
    st.markdown('<div class="section-title">⚔️ 학교 대항전</div>', unsafe_allow_html=True)

    school_ai = df.groupby(["학교", "1위"]).size().reset_index(name="count")
    school_colors_list = {"당곡고": "#6366F1", "수도여고": "#EC4899"}
    patterns = {"당곡고": "", "수도여고": "x"}

    fig_battle = go.Figure()
    for school in ["당곡고", "수도여고"]:
        sub = school_ai[school_ai["학교"] == school].set_index("1위").reindex(AI_LIST, fill_value=0).reset_index()
        fig_battle.add_trace(go.Bar(
            x=sub["1위"], y=sub["count"], name=school,
            marker=dict(color=school_colors_list[school], pattern_shape=patterns[school], line=dict(width=0)),
            text=sub["count"].apply(lambda v: f"{v}표" if v > 0 else ""),
            textposition="outside",
            textfont=dict(size=13, color="white", family="Noto Sans KR"),
            hovertemplate=f"<b>{school}</b><br>" + "%{x}: %{y}표<extra></extra>",
        ))
    fig_battle.update_layout(
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(title="", gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#888"), range=[0, school_ai["count"].max() + 2]),
        xaxis=dict(tickfont=dict(size=13, color="#ccc", family="Orbitron")),
        height=420, margin=dict(t=20, b=40, l=40, r=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=12, color="#ccc"), bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig_battle, use_container_width=True)

with col_b2:
    st.markdown('<div class="section-title">🗺️ 순위 분포 맵</div>', unsafe_allow_html=True)

    heat_data = pd.DataFrame(0, index=AI_LIST, columns=RANK_COLS)
    for _, row in df.iterrows():
        for col in RANK_COLS:
            heat_data.loc[row[col], col] += 1

    fig_heat = go.Figure(data=go.Heatmap(
        z=heat_data.values,
        x=heat_data.columns.tolist(),
        y=heat_data.index.tolist(),
        text=[[f"{v}표" for v in row] for row in heat_data.values],
        texttemplate="%{text}",
        textfont=dict(size=18, family="Orbitron", color="white"),
        colorscale=[[0.0, "#0a0a1a"], [0.15, "#1a0a2e"], [0.4, "#4a1942"], [0.7, "#e94560"], [1.0, "#f9d423"]],
        hovertemplate="<b>%{y}</b> → %{x}<br>%{text}<extra></extra>",
        showscale=True,
        colorbar=dict(title=dict(text="표", font=dict(color="#aaa", size=11)), tickfont=dict(color="#888"), bgcolor="rgba(0,0,0,0)"),
    ))
    fig_heat.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=420, margin=dict(t=20, b=40, l=80, r=20),
        xaxis=dict(tickfont=dict(size=14, color="#ccc", family="Orbitron"), side="bottom"),
        yaxis=dict(tickfont=dict(size=13, color="#ccc", family="Orbitron"), autorange="reversed"),
    )
    st.plotly_chart(fig_heat, use_container_width=True)

# ──────────────────────────────────────────────
# 🎮 PLAYERS
# ──────────────────────────────────────────────
st.markdown('<div class="section-title">🎮 PLAYERS</div>', unsafe_allow_html=True)

chips_html = '<div class="voter-grid">'
for _, row in df.iterrows():
    dot_color = SCHOOL_DOT[row["학교"]]
    chips_html += f"""
    <div class="voter-chip">
        <span class="school-dot" style="background:{dot_color};"></span>
        <span>{row['이름']}</span>
        <span style="color:#666;">|</span>
        <span>{AI_EMOJI[row['1위']]} {row['1위']}</span>
    </div>
    """
chips_html += '</div>'
st.markdown(chips_html, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# RAW DATA
# ──────────────────────────────────────────────
with st.expander("📋 RAW DATA"):
    st.dataframe(df.reset_index(drop=True), use_container_width=True, hide_index=True)

st.markdown("""
<div class="footer">
    ⚡ AI BATTLE ROYALE · 2025.03.26 수업 중 실시간 설문 · Streamlit + Plotly ⚡
</div>
""", unsafe_allow_html=True)
