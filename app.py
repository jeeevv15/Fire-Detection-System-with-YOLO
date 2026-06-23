"""
app.py — FireDet | Streamlit Frontend
Run with: streamlit run app.py
"""

import streamlit as st
import plotly.graph_objects as go
import tempfile
import os

st.set_page_config(
    page_title="FireDet | Fire Detection System",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

:root {
    --yellow:  #fbcc0a;
    --purple:  #743a6d;
    --red:     #e63552;
    --bg:      #0d0916;
    --surface: #160d22;
    --card:    #1e1230;
    --border:  #2e1f45;
    --text:    #f0eaf8;
    --muted:   #9b8ab0;
}

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text);
}
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
section[data-testid="stSidebar"] { display: none; }

/* ── TOP NAVBAR ── */
.navbar {
    width: 100%;
    background: rgba(13, 9, 22, 0.95);
    border-bottom: 1px solid var(--border);
    padding: 0 3rem;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(12px);
}
.navbar-brand {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.4rem;
    font-weight: 700;
    background: linear-gradient(90deg, var(--yellow), var(--red), var(--purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.5px;
}
.navbar-links {
    display: flex;
    gap: 2rem;
    font-size: 0.85rem;
    color: var(--muted);
    font-weight: 500;
}
.navbar-badge {
    background: linear-gradient(135deg, var(--red), var(--purple));
    color: white;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.08em;
}

/* ── HERO ── */
.hero {
    width: 100%;
    padding: 5rem 3rem 4rem 3rem;
    background:
        radial-gradient(ellipse 80% 60% at 50% -10%, rgba(116,58,109,0.35) 0%, transparent 70%),
        radial-gradient(ellipse 50% 40% at 80% 100%, rgba(230,53,82,0.2) 0%, transparent 60%),
        radial-gradient(ellipse 40% 30% at 20% 100%, rgba(251,204,10,0.12) 0%, transparent 60%),
        var(--bg);
    text-align: center;
    border-bottom: 1px solid var(--border);
}
.hero-eyebrow {
    display: inline-block;
    background: rgba(251,204,10,0.1);
    border: 1px solid rgba(251,204,10,0.3);
    color: var(--yellow);
    font-size: 0.75rem;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.35rem 1rem;
    border-radius: 999px;
    margin-bottom: 1.5rem;
}
.hero-title {
    font-size: 4rem;
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -2px;
    background: linear-gradient(135deg,
        var(--yellow) 0%,
        #f4925a 30%,
        var(--red) 60%,
        var(--purple) 100%
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
}
.hero-sub {
    font-size: 1.1rem;
    color: var(--muted);
    max-width: 540px;
    margin: 0 auto 2.5rem auto;
    line-height: 1.7;
}
.hero-pills {
    display: flex;
    gap: 0.75rem;
    justify-content: center;
    flex-wrap: wrap;
}
.pill {
    background: var(--card);
    border: 1px solid var(--border);
    color: var(--muted);
    font-size: 0.8rem;
    padding: 0.4rem 1rem;
    border-radius: 999px;
    font-family: 'JetBrains Mono', monospace;
}

/* ── MAIN CONTENT AREA ── */
.main-content {
    max-width: 1100px;
    margin: 0 auto;
    padding: 3rem 2rem;
}

/* ── SECTION LABEL ── */
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--red);
    margin-bottom: 0.5rem;
}
.section-heading {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 1.5rem;
}

/* ── UPLOAD CARD ── */
.upload-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.upload-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--yellow), var(--red), var(--purple));
}

/* ── RESULT CARDS ── */
.result-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}

/* ── STAT GRID ── */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
}
.stat-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.25rem;
    text-align: center;
}
.stat-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.2rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 0.4rem;
}
.stat-name {
    font-size: 0.75rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
}
.num-yellow { color: var(--yellow); }
.num-red    { color: var(--red); }
.num-purple { color: var(--purple); }
.num-green  { color: #4ade80; }

/* ── ALERT ── */
.alert-fire {
    background: linear-gradient(135deg, rgba(230,53,82,0.15), rgba(116,58,109,0.15));
    border: 1px solid var(--red);
    border-radius: 16px;
    padding: 1.75rem 2rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    margin-bottom: 1.5rem;
}
.alert-icon-wrap {
    font-size: 2.5rem;
    flex-shrink: 0;
}
.alert-fire-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--red);
    margin-bottom: 0.3rem;
}
.alert-fire-body { color: #c9919e; font-size: 0.9rem; line-height: 1.5; }

.alert-safe {
    background: rgba(74,222,128,0.08);
    border: 1px solid rgba(74,222,128,0.4);
    border-radius: 16px;
    padding: 1.75rem 2rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    margin-bottom: 1.5rem;
}
.alert-safe-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.2rem;
    font-weight: 700;
    color: #4ade80;
    margin-bottom: 0.3rem;
}
.alert-safe-body { color: #7bbf95; font-size: 0.9rem; line-height: 1.5; }

/* ── FILE INFO ── */
.file-pill {
    display: inline-flex;
    align-items: center;
    gap: 1rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.5rem 1.2rem;
    font-size: 0.82rem;
    color: var(--muted);
    margin-bottom: 1.25rem;
    font-family: 'JetBrains Mono', monospace;
}

/* ── BUTTON ── */
div.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, var(--yellow) 0%, #f4925a 40%, var(--red) 70%, var(--purple) 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.85rem 2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.95rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    transition: opacity 0.2s, transform 0.15s;
    cursor: pointer;
    margin-top: 0.5rem;
}
div.stButton > button:hover {
    opacity: 0.88;
    transform: translateY(-2px);
}
div.stButton > button:disabled {
    opacity: 0.35;
    cursor: not-allowed;
    transform: none;
}

/* ── SLIDERS ── */
[data-testid="stSlider"] > div > div > div > div {
    background: linear-gradient(90deg, var(--yellow), var(--red));
}

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {
    background: var(--surface);
    border-radius: 14px;
    border: 2px dashed var(--border);
    padding: 1rem;
    transition: border-color 0.2s;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--red);
}
[data-testid="stFileDropzone"] {
    background: transparent !important;
}

/* ── PROGRESS ── */
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, var(--yellow), var(--red), var(--purple));
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    background: var(--surface);
    border-radius: 12px;
    border: 1px solid var(--border);
}

/* ── DIVIDER ── */
hr { border-color: var(--border) !important; margin: 2rem 0; }

/* ── IMAGE ── */
.stImage img { border-radius: 14px; border: 1px solid var(--border); }

/* ── FOOTER ── */
.site-footer {
    border-top: 1px solid var(--border);
    padding: 2rem 3rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: var(--muted);
    font-size: 0.8rem;
}
.footer-brand {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    background: linear-gradient(90deg, var(--yellow), var(--red));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* Fix streamlit white backgrounds */
.stSpinner > div { color: var(--red) !important; }
[data-baseweb="select"] { background: var(--card) !important; }
</style>
""", unsafe_allow_html=True)


# ── NAVBAR ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
    <div class="navbar-brand">🔥 FireDet</div>
    <div class="navbar-links">
        <span>Detection</span>
        <span>Analytics</span>
        <span>Docs</span>
    </div>
    <div class="navbar-badge">YOLOv8 · Live</div>
</div>
""", unsafe_allow_html=True)


# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">🔥 AI-Powered Safety System</div>
    <div class="hero-title">Fire & Smoke<br>Detection</div>
    <div class="hero-sub">
        Upload surveillance footage or a photo and let YOLOv8 scan
        every frame for fire and smoke — with a full timeline report.
    </div>
    <div class="hero-pills">
        <div class="pill">⚡ YOLOv8n</div>
        <div class="pill">🎞️ Video & Image</div>
        <div class="pill">📊 Timeline Graph</div>
        <div class="pill">📋 Frame Report</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── MAIN CONTENT ──────────────────────────────────────────────────────────────
st.markdown('<div class="main-content">', unsafe_allow_html=True)


# ── UPLOAD SECTION ────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-label">Step 01</div>
<div class="section-heading">Upload Your File</div>
""", unsafe_allow_html=True)

st.markdown('<div class="upload-card">', unsafe_allow_html=True)

col_up, col_gap, col_cfg = st.columns([3, 0.2, 1.5])

with col_up:
    uploaded = st.file_uploader(
        "Drop a video or image file here",
        type=["mp4", "png", "jpg", "jpeg"],
        label_visibility="visible",
    )

with col_cfg:
    st.markdown("**Detection Settings**")
    conf_threshold = st.slider("Confidence threshold", 0.10, 0.90, 0.25, 0.05,
                                help="Higher = fewer but more certain detections")
    if uploaded and uploaded.type.startswith("video"):
        sample_fps = st.slider("Analysis FPS", 1, 10, 2,
                               help="Frames per second to analyse. Lower = faster.")
    else:
        sample_fps = 2

st.markdown('</div>', unsafe_allow_html=True)

# File info pill
if uploaded:
    size_mb = round(uploaded.size / 1_048_576, 2)
    ftype = "🎞️ Video" if uploaded.type.startswith("video") else "🖼️ Image"
    st.markdown(f"""
    <div class="file-pill">
        <span>{ftype}</span>
        <span>📄 {uploaded.name}</span>
        <span>💾 {size_mb} MB</span>
        <span style="color:#4ade80;">✓ Ready</span>
    </div>
    """, unsafe_allow_html=True)

# Run button
col_btn, col_r = st.columns([1, 2])
with col_btn:
    run = st.button("🔥 Start Detection →", disabled=(uploaded is None))


# ── DETECTION LOGIC ───────────────────────────────────────────────────────────
if run and uploaded:
    from detector import detect_video, detect_image

    suffix = os.path.splitext(uploaded.name)[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded.read())
        tmp_path = tmp.name

    is_video = uploaded.type.startswith("video")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-label">Step 02</div>
    <div class="section-heading">Processing</div>
    """, unsafe_allow_html=True)

    if is_video:
        progress_bar = st.progress(0, text="Scanning frames…")
        def update_progress(p):
            progress_bar.progress(min(p, 1.0), text=f"Scanning frames… {int(p*100)}%")
        with st.spinner("YOLOv8 is analysing your video…"):
            result = detect_video(tmp_path, conf=conf_threshold,
                                  sample_fps=sample_fps,
                                  progress_callback=update_progress)
        progress_bar.progress(1.0, text="Analysis complete ✓")
    else:
        with st.spinner("YOLOv8 is analysing your image…"):
            result = detect_image(tmp_path, conf=conf_threshold)

    os.unlink(tmp_path)

    # ── RESULTS ──────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-label">Step 03</div>
    <div class="section-heading">Results</div>
    """, unsafe_allow_html=True)

    # Alert / safe banner
    if result["fire_detected"]:
        if is_video:
            msg = (f"Fire or smoke found in <strong>{result['frames_with_fire']}</strong> out of "
                   f"<strong>{result['total_frames']}</strong> analysed frames "
                   f"({result['detection_rate']}% detection rate). Scroll down for the full timeline.")
        else:
            cls = ", ".join(result.get("classes", ["fire"])) or "fire"
            msg = f"Detected: <strong>{cls}</strong> &nbsp;·&nbsp; Confidence: <strong>{result['confidence']*100:.1f}%</strong>"
        st.markdown(f"""
        <div class="alert-fire">
            <div class="alert-icon-wrap">🚨</div>
            <div>
                <div class="alert-fire-title">FIRE DETECTED</div>
                <div class="alert-fire-body">{msg}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert-safe">
            <div class="alert-icon-wrap">✅</div>
            <div>
                <div class="alert-safe-title">ALL CLEAR</div>
                <div class="alert-safe-body">No fire or smoke was detected in this footage.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── STATS ─────────────────────────────────────────────────────────────────
    if is_video:
        rate_cls = "num-red" if result["fire_detected"] else "num-green"
        status_txt = "ALERT" if result["fire_detected"] else "SAFE"
        status_cls = "num-red" if result["fire_detected"] else "num-green"

        st.markdown(f"""
        <div class="stat-grid">
            <div class="stat-box">
                <div class="stat-num num-yellow">{result['total_frames']}</div>
                <div class="stat-name">Frames Analysed</div>
            </div>
            <div class="stat-box">
                <div class="stat-num num-red">{result['frames_with_fire']}</div>
                <div class="stat-name">Frames with Fire</div>
            </div>
            <div class="stat-box">
                <div class="stat-num {rate_cls}">{result['detection_rate']}%</div>
                <div class="stat-name">Detection Rate</div>
            </div>
            <div class="stat-box">
                <div class="stat-num {status_cls}">{status_txt}</div>
                <div class="stat-name">Status</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── TIMELINE CHART ────────────────────────────────────────────────────────
    if is_video and len(result["frame_data"]) >= 2:
        st.markdown("""
        <div class="section-label" style="margin-top:2rem;">Analytics</div>
        <div class="section-heading">Detection Timeline</div>
        """, unsafe_allow_html=True)

        fd = result["frame_data"]
        times  = [f["timestamp"] for f in fd]
        values = [1 if f["fire_detected"] else 0 for f in fd]
        confs  = [f["confidence"] for f in fd]

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=times, y=values, mode="none",
            fill="tozeroy",
            fillcolor="rgba(230,53,82,0.18)",
            showlegend=False, hoverinfo="skip",
        ))
        fig.add_trace(go.Scatter(
            x=times, y=values, mode="lines",
            line=dict(color="#e63552", width=2.5, shape="hv"),
            name="Fire Detected",
            customdata=list(zip([f["frame_number"] for f in fd], confs)),
            hovertemplate=(
                "<b>⏱ Time:</b> %{x:.1f}s<br>"
                "<b>🎞 Frame:</b> %{customdata[0]}<br>"
                "<b>📊 Confidence:</b> %{customdata[1]:.0%}<extra></extra>"
            ),
        ))
        fig.add_trace(go.Scatter(
            x=times, y=confs, mode="lines",
            line=dict(color="#fbcc0a", width=1.5, dash="dot"),
            name="Confidence", yaxis="y2", hoverinfo="skip",
        ))

        fig.update_layout(
            paper_bgcolor="#0d0916",
            plot_bgcolor="#160d22",
            margin=dict(l=0, r=0, t=20, b=0),
            height=300,
            font=dict(family="JetBrains Mono, monospace", color="#9b8ab0", size=11),
            xaxis=dict(title="Time (seconds)", gridcolor="#2e1f45", showline=False, zeroline=False),
            yaxis=dict(
                title="Status", tickvals=[0, 1], ticktext=["Safe", "🔥 Fire"],
                gridcolor="#2e1f45", showline=False, zeroline=False, range=[-0.1, 1.4],
            ),
            yaxis2=dict(
                title="Confidence", overlaying="y", side="right",
                range=[0, 1], showgrid=False, tickformat=".0%", zeroline=False,
            ),
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02,
                xanchor="right", x=1, bgcolor="rgba(0,0,0,0)",
            ),
            hovermode="x unified",
        )

        for f in fd:
            if f["fire_detected"]:
                fig.add_vrect(
                    x0=f["timestamp"] - 0.15, x1=f["timestamp"] + 0.15,
                    fillcolor="rgba(230,53,82,0.1)", line_width=0, layer="below",
                )

        st.plotly_chart(fig, use_container_width=True)

    # ── ANNOTATED IMAGE ───────────────────────────────────────────────────────
    if not is_video and "annotated_image" in result:
        st.markdown("""
        <div class="section-label" style="margin-top:2rem;">Output</div>
        <div class="section-heading">Annotated Image</div>
        """, unsafe_allow_html=True)
        col_img, col_pad = st.columns([2, 1])
        with col_img:
            st.image(result["annotated_image"], use_container_width=True)

    # ── FRAME LOG TABLE ───────────────────────────────────────────────────────
    if is_video:
        fire_frames = [f for f in result["frame_data"] if f["fire_detected"]]
        if fire_frames:
            st.markdown("""
            <div class="section-label" style="margin-top:2rem;">Full Log</div>
            <div class="section-heading">Fire Frame Report</div>
            """, unsafe_allow_html=True)
            import pandas as pd
            df = pd.DataFrame(fire_frames)[["frame_number", "timestamp", "classes", "confidence"]]
            df.columns = ["Frame #", "Timestamp (s)", "Classes", "Confidence"]
            df["Classes"] = df["Classes"].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)
            st.dataframe(df, use_container_width=True, hide_index=True)


st.markdown('</div>', unsafe_allow_html=True)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="site-footer">
    <div class="footer-brand">🔥 FireDet</div>
    <div>YOLOv8n · Fine-tuned for fire & smoke detection</div>
    <div>Built by Jeevika Kambli</div>
</div>
""", unsafe_allow_html=True) 