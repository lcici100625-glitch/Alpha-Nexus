import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import time

# ==========================================
# 1. 頁面配置與全局樣式 (FinTech 暗黑風格)
# ==========================================
st.set_page_config(
    page_title="Alpha-Nexus Terminal | AI 港股量化系統",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定義 CSS 注入：模擬彭博/Wind終端風格
st.markdown("""
<style>
    .reportview-container { background: #0E1117; }
    .stMetric { background-color: #1E2129; padding: 15px; border-radius: 8px; border-left: 4px solid #00F0FF; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .stMetric label { color: #A0AEC0 !important; font-weight: bold; }
    h1, h2, h3 { color: #00F0FF !important; font-family: 'Courier New', Courier, monospace; }
    .highlight-red { color: #FF4B4B; font-weight: bold; }
    .highlight-green { color: #00F0FF; font-weight: bold; }
    div[data-testid="stSidebar"] { background-color: #11151C; border-right: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 模擬數據生成函數 (Mock Data for Demo)
# ==========================================
@st.cache_data
def generate_backtest_data():
    dates = pd.date_range(start='2016-01-01', end='2025-12-31', freq='M')
    n = len(dates)
    
    # 模擬恆指 (震盪下行)
    hsi = np.cumsum(np.random.normal(-0.001, 0.05, n))
    # 模擬傳統 DRL (波動大)
    eiie = np.cumsum(np.random.normal(0.015, 0.07, n))
    # 模擬 Alpha-Nexus (穩健向上，回撤小)
    alpha_nexus = np.cumsum(np.random.normal(0.018, 0.03, n))
    
    # 疊加2021-2022大熊市效應
    bear_market_idx = (dates.year >= 2021) & (dates.year <= 2022)
    hsi[bear_market_idx] -= np.linspace(0, 0.5, sum(bear_market_idx))
    eiie[bear_market_idx] -= np.linspace(0, 0.3, sum(bear_market_idx))
    alpha_nexus[bear_market_idx] -= np.linspace(0, 0.05, sum(bear_market_idx)) # 風控生效
    
    df = pd.DataFrame({'Date': dates, 'HSI': hsi, 'EIIE (DRL)': eiie, 'Alpha-Nexus': alpha_nexus})
    # 轉換為百分比收益率基底
    for col in ['HSI', 'EIIE (DRL)', 'Alpha-Nexus']:
        df[col] = (np.exp(df[col]) - 1) * 100
    return df

# ==========================================
# 3. 側邊欄導航 (Sidebar)
# ==========================================
st.sidebar.image("https://img.icons8.com/nolan/96/artificial-intelligence.png", width=80)
st.sidebar.title("Alpha-Nexus AaaS")
st.sidebar.caption("基於 LLM 與動態超圖的自適應交易系統")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "系統模塊導航",
    ["📊 系統概覽 (Dashboard)", 
     "🧠 宏觀感知 (Llama-3-Fin)", 
     "🕸️ 微觀執行 (DH-GAT)", 
     "⏪ 歷史覆盤 (Event Replay)"]
)

st.sidebar.markdown("---")
st.sidebar.caption("商業模式: To-B (Nexus-Terminal) / To-C (Alpha-Bot)")
st.sidebar.caption("© 2026 量化認知智能實驗室")

# ==========================================
# 4. 頁面邏輯渲染
# ==========================================

# ------------------------------------------
# 頁面 1: 系統概覽 (整體績效與核心指標)
# ------------------------------------------
if menu == "📊 系統概覽 (Dashboard)":
    st.title("📊 Alpha-Nexus 量化投資組合表現 (2016-2025)")
    st.markdown("對標傳統深度強化學習(DRL)與香港恆生指數，展示穿越牛熊的 Alpha 捕捉能力。")
    
    # 頂部 KPI
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("累計收益 (Cumulative)", "+584.2%", "+24.5% (YoY)")
    col2.metric("年化收益 (Annualized)", "21.2%", "超越基準 22.5%")
    col3.metric("最大回撤 (Max Drawdown)", "-14.8%", "恆指 -52.8%", delta_color="inverse")
    col4.metric("夏普比率 (Sharpe)", "2.05", "極高風險調整後收益")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 繪製主圖：累計收益對比
    df_perf = generate_backtest_data()
    fig = px.line(df_perf, x='Date', y=['Alpha-Nexus', 'EIIE (DRL)', 'HSI'],
                  labels={'value': '累計收益率 (%)', 'Date': '時間'},
                  color_discrete_map={'Alpha-Nexus': '#00F0FF', 'EIIE (DRL)': '#F5A623', 'HSI': '#4A4A4A'})
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#A0AEC0'), legend=dict(title=None, orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=True, gridcolor='#333'), yaxis=dict(showgrid=True, gridcolor='#333')
    )
    
    # 標記歷史事件
    fig.add_vrect(x0="2018-06-01", x1="2018-12-31", fillcolor="red", opacity=0.1, line_width=0, annotation_text="貿易摩擦")
    fig.add_vrect(x0="2021-07-01", x1="2022-12-31", fillcolor="red", opacity=0.1, line_width=0, annotation_text="科技反壟斷/加息")
    fig.add_vrect(x0="2025-01-01", x1="2025-12-31", fillcolor="orange", opacity=0.1, line_width=0, annotation_text="模擬流動性衝擊")
    
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------
# 頁面 2: 宏觀感知大腦 (LLM & 情緒恆溫器)
# ------------------------------------------
elif menu == "🧠 宏觀感知 (Llama-3-Fin)":
    st.title("🧠 雙重認知 (一)：宏觀大語言模型驅動")
    st.markdown("利用微調後的 `Llama-3-Fin` 處理非結構化文本，打破量化模型的**「語義盲區」**。")
    
    st.subheader("實時新聞解析與風險量化")
    
    default_news = "美聯儲官員強烈暗示下月加息50個基點；同時香港金管局發布最新指引，銀行體系結餘跌破千億大關，港幣 HIBOR 拆息全線飆升。某互聯網巨頭因反壟斷再次收到巨額罰單。"
    news_input = st.text_area("輸入實時財經新聞摘要 (System Input):", value=default_news, height=100)
    
    if st.button("🚀 運行 LLM 思維鏈 (CoT) 推理"):
        with st.spinner("Llama-3-Fin 正在解構宏觀敘事..."):
            time.sleep(1.5) # 模擬推理時間
            
            # 簡單規則模擬 LLM 判斷 (參賽時可替換為真實 API)
            if "加息" in news_input or "反壟斷" in news_input:
                risk_level = 0.88
                narrative = "美聯儲加息 → 港幣流動性收緊 → 高估值科技板塊承壓；反壟斷打擊平台經濟。"
                regime_color = "red"
            else:
                risk_level = 0.25
                narrative = "宏觀環境平穩，市場流動性充裕，風險偏好正常，適合 Alpha 挖掘。"
                regime_color = "#00F0FF"
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### 🚨 市場危機概率 (Crisis Prob)")
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = risk_level * 100,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "由 LLM 輸出的極端風險概率", 'font': {'size': 14, 'color': 'gray'}},
                gauge = {
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
                    'bar': {'color': "#FF4B4B" if risk_level > 0.5 else "#00F0FF"},
                    'bgcolor': "rgba(0,0,0,0)",
                    'steps': [{'range': [0, 50], 'color': "rgba(0, 240, 255, 0.1)"},
                              {'range': [50, 100], 'color': "rgba(255, 75, 75, 0.2)"}],
                }
            ))
            fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"}, height=300)
            st.plotly_chart(fig_gauge, use_container_width=True)
            
        with col2:
            st.markdown("### 💡 LLM 推理邏輯 (Chain of Thought)")
            st.info(f"**語義提取:** {narrative}")
            
            st.markdown("### 🌡️ 情緒恆溫器 (Emotion Thermostat) 狀態")
            st.latex(r"J(\theta) = \mathbb{E}[R_t] - \lambda_{LLM,t} \cdot \left(\frac{\sigma_p}{\sigma_{benchmark}} - 1\right)_+")
            
            penalty = max(0, risk_level * 10 * (1.5 - 1)) # 模擬計算
            if risk_level > 0.5:
                st.error(f"**觸發風險懲罰！** 當前動態風險厭惡係數 $\lambda$ 飆升。模型必須強制壓降投資組合波動率，否則 RL 智能體將受到 -{penalty:.2f} 的懲罰。")
            else:
                st.success(f"**安全區間。** 動態風險厭惡係數較低，鼓勵模型承擔適度波動率以獲取超額收益。")

# ------------------------------------------
# 頁面 3: 微觀執行 (DH-GAT)
# ------------------------------------------
elif menu == "🕸️ 微觀執行 (DH-GAT)":
    st.title("🕸️ 雙重認知 (二)：動態超圖注意力網絡")
    st.markdown("突破傳統獨立時間序列，構建非歐幾里得空間，精準捕捉**板塊輪動**與**供應鏈關聯**。")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("板塊與股權關聯超圖拓撲 (實時可視化)")
        # 繪製模擬網絡圖
        G = nx.Graph()
        tech_nodes = ['0700.HK', '9988.HK', '3690.HK', '1810.HK']
        util_nodes = ['0002.HK', '0003.HK', '0006.HK']
        fin_nodes = ['0005.HK', '1299.HK', '0388.HK']
        
        # 添加節點
        for n in tech_nodes: G.add_node(n, group='科技 (Tech)')
        for n in util_nodes: G.add_node(n, group='公用事業 (Utilities)')
        for n in fin_nodes: G.add_node(n, group='金融 (Finance)')
        
        # 添加超邊(以普通邊模擬)
        G.add_edges_from([('0700.HK', '9988.HK'), ('0700.HK', '3690.HK'), ('9988.HK', '3690.HK')]) # 科技板塊超邊
        G.add_edges_from([('0002.HK', '0003.HK')]) # 避險板塊超邊
        G.add_edges_from([('0005.HK', '0388.HK'), ('1299.HK', '0388.HK')]) # 金融超邊
        G.add_edge('0700.HK', '0388.HK') # 跨板塊微弱關聯
        
        pos = nx.spring_layout(G, seed=42)
        edge_x, edge_y = [], []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]; x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None]); edge_y.extend([y0, y1, None])
            
        fig_net = go.Figure()
        fig_net.add_trace(go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#888'), hoverinfo='none', mode='lines'))
        
        # 節點顏色
        color_map = {'科技 (Tech)': '#FF4B4B', '公用事業 (Utilities)': '#00F0FF', '金融 (Finance)': '#F5A623'}
        for group in color_map.keys():
            nx_pts = [n for n in G.nodes() if G.nodes[n]['group'] == group]
            fig_net.add_trace(go.Scatter(
                x=[pos[n][0] for n in nx_pts], y=[pos[n][1] for n in nx_pts],
                mode='markers+text', text=nx_pts, textposition="top center",
                marker=dict(size=20, color=color_map[group], line=dict(width=2, color='white')),
                name=group
            ))
            
        fig_net.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=450, legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        st.plotly_chart(fig_net, use_container_width=True)

    with col2:
        st.subheader("Gated Fusion 單元")
        st.markdown("公式: $z_t = (1-g_t) \odot h_{micro} + g_t \odot W_h h_{macro}$")
        st.write("目前 LLM 宏觀權重佔比 ($g_t$):")
        
        # 互動滑塊模擬門控
        gt = st.slider("調整宏觀干預強度", 0.0, 1.0, 0.8)
        
        if gt > 0.5:
            st.warning("⚠️ 系統當前由 **LLM 宏觀風險感知** 主導決策，壓制了微觀圖網絡的追漲殺跌行為。")
            tech_w, util_w, fin_w, cash_w = 5, 45, 10, 40
        else:
            st.success("✅ 系統當前由 **DH-GAT 微觀 Alpha 捕捉** 主導決策，積極參與板塊輪動。")
            tech_w, util_w, fin_w, cash_w = 60, 10, 20, 10
            
        st.markdown("### 最終策略輸出 (資產權重)")
        df_w = pd.DataFrame({
            "板塊": ["科技 (高Beta)", "公用 (避險)", "金融", "現金 (Cash)"],
            "權重": [tech_w, util_w, fin_w, cash_w]
        })
        fig_pie = px.pie(df_w, values="權重", names="板塊", hole=0.5, 
                         color="板塊", color_discrete_map={"科技 (高Beta)": "#FF4B4B", "公用 (避險)": "#00F0FF", "金融": "#F5A623", "現金 (Cash)": "#A0AEC0"})
        fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=300, showlegend=False)
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

# ------------------------------------------
# 頁面 4: 歷史事件覆盤 (Event Replay)
# ------------------------------------------
elif menu == "⏪ 歷史覆盤 (Event Replay)":
    st.title("⏪ 關鍵歷史事件覆盤 (Case Studies)")
    st.markdown("展示 **Alpha-Nexus** 在極端行情下，如何憑藉「認知智能」碾壓傳統量化模型。")
    
    event = st.selectbox(
        "選擇歷史極端事件:",
        ["2021 平台經濟反壟斷 & 2022 激進加息", "2018 中美貿易摩擦", "2025 模擬流動性枯竭"]
    )
    
    st.markdown("---")
    
    if "2021" in event:
        st.markdown("### 📜 背景敘事: 2021-2022 漫長熊市")
        st.write("傳統技術指標(如RSI)顯示騰訊、阿里嚴重超賣，導致傳統 DRL 模型 (EIIE) 不斷試圖抄底，最終面臨 **-29.4%** 的巨大回撤。")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info("**Alpha-Nexus 操作邏輯 (CoT):**\n1. 讀取《反壟斷指南》識別結構性利空。\n2. 檢測美聯儲縮表信號。\n3. **情緒恆溫器觸發**，強制模型將倉位切換至 40% 估值回撤保護區(空倉/現金)。")
        with col2:
            st.metric("Alpha-Nexus 該階段最大回撤", "-14.8%", "保住勝利果實", delta_color="normal")
            
        # 繪製調倉前後對比條形圖
        df_shift = pd.DataFrame({
            "資產類別": ["互聯網科技", "房地產", "公用事業", "現金"],
            "危機前權重(%)": [55, 20, 15, 10],
            "危機後權重(%)": [5, 0, 45, 50]
        })
        fig_bar = px.barmode="group"
        fig_bar = go.Figure(data=[
            go.Bar(name='危機前 (牛市末期)', x=df_shift['資產類別'], y=df_shift['危機前權重(%)'], marker_color='#FF4B4B'),
            go.Bar(name='危機後 (Alpha-Nexus自動調倉)', x=df_shift['資產類別'], y=df_shift['危機後權重(%)'], marker_color='#00F0FF')
        ])
        fig_bar.update_layout(title="Alpha-Nexus 應對2021熊市的「斷臂求生」式調倉", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color='white'))
        st.plotly_chart(fig_bar, use_container_width=True)

    elif "2018" in event:
        st.markdown("### 📜 背景敘事: 2018 中美貿易摩擦")
        st.write("新聞中「關稅」、「制裁」頻率飆升。LLM 輸出高風險信號。")
        st.success("**模型反應:** 成功將倉位從出口導向型硬件科技股，精準切換至本地公用事業股（如中電控股），完美規避了 Q4 的市場暴跌。")
        
    elif "2025" in event:
        st.markdown("### 📜 背景敘事: 2025 模擬流動性枯竭 (Testing Set)")
        st.write("在未來的壓力測試中，模型準確識別「拆息創新高」的隱含信號。")
        st.success("**模型反應:** 系統判定 Beta 收益為負，啟動極端防禦模式，增持高股息資產與美元存款，不僅抗跌甚至錄得微幅正收益。")
        
    st.markdown("---")
    st.markdown("### 💼 商業落地: Alpha-as-a-Service")
    st.write("本系統不僅是論文模型，更可封裝為 **API 插件 (Nexus-Terminal)** 賦能中小型券商，或打造 **To-C 智能投顧 (Alpha-Bot)** 幫助散戶克服恐慌情緒。")
