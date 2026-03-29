import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ──────────────────────────────────────────────
# 페이지 설정
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="AI 선호도 조사 결과",
    page_icon="🤖",
    layout="wide",
)

# ──────────────────────────────────────────────
# 데이터 정의
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

# 색상 팔레트
COLORS = {
    "Claude": "#E07B39",   # 앤트로픽 오렌지
    "Gemini": "#4285F4",   # 구글 블루
    "ChatGPT": "#10A37F",  # OpenAI 그린
}

SCHOOL_COLORS = {
    "당곡고": "#6366F1",   # 인디고
    "수도여고": "#EC4899", # 핑크
}

# ──────────────────────────────────────────────
# 헤더
# ──────────────────────────────────────────────
st.markdown(
    """
    <div style='text-align:center; padding: 1.5rem 0 0.5rem 0;'>
        <h1 style='margin-bottom:0.2rem;'>🤖 AI 선호도 조사 결과</h1>
        <p style='color:gray; font-size:1.1rem;'>당곡고 × 수도여고 학생 설문 · 2025년 3월 26일</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# 요약 메트릭
total = len(df)
dangok = len(df[df["학교"] == "당곡고"])
sudo = len(df[df["학교"] == "수도여고"])

col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("전체 응답자", f"{total}명")
col_m2.metric("당곡고", f"{dangok}명")
col_m3.metric("수도여고", f"{sudo}명")

st.divider()

# ──────────────────────────────────────────────
# 1) 1위 득표수 막대그래프
# ──────────────────────────────────────────────
st.subheader("① 1위 득표수")

first_counts = df["1위"].value_counts().reindex(AI_LIST, fill_value=0)

fig1 = go.Figure()
fig1.add_trace(go.Bar(
    x=first_counts.index,
    y=first_counts.values,
    marker_color=[COLORS[ai] for ai in first_counts.index],
    text=first_counts.values,
    textposition="outside",
    textfont=dict(size=18, color="white"),
    hovertemplate="<b>%{x}</b><br>1위 득표: %{y}표<extra></extra>",
))
fig1.update_layout(
    yaxis=dict(title="득표수 (표)", range=[0, first_counts.max() + 2]),
    xaxis=dict(title=""),
    template="plotly_dark",
    height=400,
    margin=dict(t=30, b=40),
)
st.plotly_chart(fig1, use_container_width=True)

# ──────────────────────────────────────────────
# 2) AI별 평균 순위 비교
# ──────────────────────────────────────────────
st.subheader("② AI별 평균 순위 (낮을수록 선호)")

rank_map = {ai: [] for ai in AI_LIST}
for _, row in df.iterrows():
    for rank_idx, col in enumerate(RANK_COLS, 1):
        rank_map[row[col]].append(rank_idx)

avg_ranks = {ai: sum(v) / len(v) for ai, v in rank_map.items()}
avg_df = pd.DataFrame({
    "AI": list(avg_ranks.keys()),
    "평균 순위": list(avg_ranks.values()),
}).sort_values("평균 순위")

fig2 = go.Figure()
fig2.add_trace(go.Bar(
    x=avg_df["AI"],
    y=avg_df["평균 순위"],
    marker_color=[COLORS[ai] for ai in avg_df["AI"]],
    text=[f"{v:.2f}" for v in avg_df["평균 순위"]],
    textposition="outside",
    textfont=dict(size=16, color="white"),
    hovertemplate="<b>%{x}</b><br>평균 순위: %{y:.2f}<extra></extra>",
))
fig2.update_layout(
    yaxis=dict(title="평균 순위", range=[0, 3.5], autorange="reversed"),
    xaxis=dict(title=""),
    template="plotly_dark",
    height=400,
    margin=dict(t=30, b=40),
    annotations=[dict(
        text="⬆ 위쪽일수록 선호도 높음",
        xref="paper", yref="paper",
        x=0.98, y=0.02, showarrow=False,
        font=dict(size=12, color="gray"),
    )],
)
st.plotly_chart(fig2, use_container_width=True)

# ──────────────────────────────────────────────
# 3) 학교별 선호도 비교 (그룹 막대)
# ──────────────────────────────────────────────
st.subheader("③ 학교별 1위 선호도 비교")

school_ai = (
    df.groupby(["학교", "1위"])
    .size()
    .reset_index(name="count")
)

fig3 = go.Figure()
for school in ["당곡고", "수도여고"]:
    sub = school_ai[school_ai["학교"] == school].set_index("1위").reindex(AI_LIST, fill_value=0).reset_index()
    fig3.add_trace(go.Bar(
        x=sub["1위"],
        y=sub["count"],
        name=school,
        marker_color=SCHOOL_COLORS[school],
        text=sub["count"],
        textposition="outside",
        textfont=dict(size=14),
        hovertemplate=f"<b>{school}</b><br>" + "%{x}: %{y}표<extra></extra>",
    ))

fig3.update_layout(
    barmode="group",
    yaxis=dict(title="득표수 (표)", range=[0, school_ai["count"].max() + 2]),
    xaxis=dict(title=""),
    template="plotly_dark",
    height=400,
    margin=dict(t=30, b=40),
    legend=dict(
        orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
        font=dict(size=14),
    ),
)
st.plotly_chart(fig3, use_container_width=True)

# ──────────────────────────────────────────────
# 4) 전체 순위 분포 히트맵
# ──────────────────────────────────────────────
st.subheader("④ 전체 순위 분포 히트맵")

heat_data = pd.DataFrame(0, index=AI_LIST, columns=RANK_COLS)
for _, row in df.iterrows():
    for col in RANK_COLS:
        heat_data.loc[row[col], col] += 1

fig4 = go.Figure(data=go.Heatmap(
    z=heat_data.values,
    x=heat_data.columns.tolist(),
    y=heat_data.index.tolist(),
    text=heat_data.values,
    texttemplate="%{text}표",
    textfont=dict(size=18),
    colorscale=[
        [0.0, "#1a1a2e"],
        [0.3, "#16213e"],
        [0.5, "#0f3460"],
        [0.7, "#e94560"],
        [1.0, "#ff6b6b"],
    ],
    hovertemplate="<b>%{y}</b> — %{x}<br>%{text}표<extra></extra>",
    showscale=True,
    colorbar=dict(title="표 수"),
))
fig4.update_layout(
    template="plotly_dark",
    height=350,
    margin=dict(t=30, b=40),
    yaxis=dict(autorange="reversed"),
)
st.plotly_chart(fig4, use_container_width=True)

# ──────────────────────────────────────────────
# 5) 원본 데이터 테이블
# ──────────────────────────────────────────────
with st.expander("📋 원본 응답 데이터 보기"):
    st.dataframe(
        df.reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
    )

# 푸터
st.markdown(
    "<p style='text-align:center; color:gray; padding-top:2rem; font-size:0.85rem;'>"
    "데이터 출처: 2025.03.26 수업 중 실시간 설문 | Streamlit + Plotly"
    "</p>",
    unsafe_allow_html=True,
)
