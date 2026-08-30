"""
Insight Flow — Dynamic CSS Design System v3
Generates theme-aware CSS from theme_engine definitions.
"""
from theme_engine import get_theme

def get_custom_css(theme_name='Default'):
    t = get_theme(theme_name)
    c = t['css']
    is_glass = t.get('glass', False)

    glass_extras = """
        .retro-window, .header-bar, .empty-state, .kpi-card, .period-card,
        .ai-insight-box, .chat-container, .dataset-info {
            backdrop-filter: blur(14px) saturate(140%) !important;
            -webkit-backdrop-filter: blur(14px) saturate(140%) !important;
        }
        .retro-body { background: rgba(255,255,255,0.10) !important; }
        .kpi-body { background: rgba(255,255,255,0.20) !important; }
    """ if is_glass else ""

    bg_style = (
        "background: linear-gradient(135deg, #E8D5F0 0%, #D0E8F0 35%, #F0E0D0 70%, #D8E0F8 100%) !important;"
        if is_glass
        else f"background-color: {c['bg-main']} !important;"
    )

    chat_a_bg = "rgba(255,253,231,0.5)" if is_glass else (
        "#3D3D3D" if c['bg-main'] == '#1E1E1E' else "#fffde7"
    )

    btn_hover = "rgba(255,255,255,0.35)" if is_glass else (
        "#3A3A3A" if c['bg-main'] == '#1E1E1E' else "rgba(0,0,0,0.06)"
    )

    dl_bg = "rgba(184,230,184,0.5)" if is_glass else (
        "#2E5E2E" if c['bg-main'] == '#1E1E1E' else "#b8e6b8"
    )

    sb_track = c['bg-panel'] if not is_glass else "rgba(255,255,255,0.1)"
    sb_thumb = c.get('border-light', '#888')

    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=VT323&family=IBM+Plex+Mono:wght@400;500;600;700&family=Share+Tech+Mono&display=swap');

        :root {{ 
            --bg-main: {c['bg-main']};
            --bg-panel: {c['bg-panel']};
            --bg-inner: {c['bg-inner']};
            --bg-white: {c['bg-white']};
            --titlebar: {c['titlebar']};
            --titlebar-light: {c['titlebar-light']};
            --titlebar-dark: {c['titlebar-dark']};
            --border: {c['border']};
            --border-mid: {c['border-mid']};
            --border-light: {c['border-light']};
            --text-dark: {c['text-dark']};
            --text-body: {c['text-body']};
            --text-mid: {c['text-mid']};
            --text-muted: {c['text-muted']};
            --accent-green: {c['accent-green']};
            --accent-red: {c['accent-red']};
            --accent-blue: {c['accent-blue']};
            --shadow: 3px 3px 0px {c['border']};
            --shadow-sm: 2px 2px 0px {c['border']};
            --shadow-inset: inset 1px 1px 3px rgba(0,0,0,0.12);
            --font-display: 'VT323', monospace;
            --font-body: 'IBM Plex Mono', 'Courier New', monospace;
            --font-mono: 'Share Tech Mono', monospace;
            --radius: 2px;
        }} 

        * {{  font-family: var(--font-body); }} 

        .stApp {{  {bg_style} }} 

        #MainMenu, footer {{  visibility: hidden; }} 
        header[data-testid="stHeader"] {{  background: transparent !important; }} 

        /* ==================== RETRO WINDOW ==================== */
        .retro-window {{ 
            background: var(--bg-inner);
            border: 2.5px solid var(--border);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            margin-bottom: 12px;
            overflow: hidden;
        }} 
        .retro-titlebar {{ 
            background: linear-gradient(180deg, var(--titlebar-light) 0%, var(--titlebar) 50%, var(--titlebar-dark) 100%);
            border-bottom: 2px solid var(--border);
            padding: 4px 10px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            min-height: 26px;
        }} 
        .retro-titlebar-text {{ 
            font-family: var(--font-display);
            font-size: 1.1rem;
            color: #ffffff;
            letter-spacing: 1.5px;
            text-shadow: 1px 1px 0px rgba(0,0,0,0.4);
        }} 
        .retro-wc {{ 
            display: flex; gap: 3px;
        }} 
        .retro-wc-btn {{ 
            width: 16px; height: 16px;
            border: 1.5px solid var(--border);
            background: var(--bg-panel);
            font-size: 9px;
            display: flex; align-items: center; justify-content: center;
            color: var(--border); line-height: 1; cursor: default;
        }} 
        .retro-body {{ 
            padding: 12px;
        }} 

        /* ==================== HEADER ==================== */
        .header-bar {{ 
            background: var(--bg-inner);
            border: 2.5px solid var(--border);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            overflow: hidden;
            margin-bottom: 12px;
        }} 
        .header-content {{ 
            padding: 10px 14px;
            display: flex; align-items: center; gap: 10px;
        }} 
        .header-title {{ 
            font-family: var(--font-display);
            font-size: 2rem; color: var(--titlebar);
            margin: 0; letter-spacing: 2px; line-height: 1;
        }} 
        .header-subtitle {{ 
            font-family: var(--font-body);
            font-size: 0.7rem; color: var(--text-muted);
            margin: 2px 0 0 0;
        }} 

        /* ==================== STATUS BADGES ==================== */
        .status-badge {{ 
            display: inline-flex; align-items: center; gap: 5px;
            padding: 3px 10px;
            border: 2px solid var(--border);
            font-family: var(--font-display);
            font-size: 0.95rem; letter-spacing: 1px;
            box-shadow: var(--shadow-sm);
        }} 
        .status-connected {{  background: #b8e6b8; color: #1a5c1a; }} 
        .status-disconnected {{  background: #f5b8b8; color: #8b1a1a; }} 
        .status-disabled {{  background: var(--bg-panel); color: var(--text-muted); }} 

        /* ==================== KPI CARDS ==================== */
        .kpi-card {{ 
            background: var(--bg-white);
            border: 2.5px solid var(--border);
            border-radius: var(--radius);
            box-shadow: var(--shadow-sm);
            overflow: hidden;
        }} 
        .kpi-header {{ 
            background: linear-gradient(180deg, var(--titlebar-light) 0%, var(--titlebar) 100%);
            border-bottom: 2px solid var(--border);
            padding: 2px 8px;
            font-family: var(--font-display);
            font-size: 0.9rem; color: #fff;
            letter-spacing: 1.5px;
            text-shadow: 1px 1px 0px rgba(0,0,0,0.3);
        }} 
        .kpi-body {{ 
            padding: 8px 10px;
            background: var(--bg-white);
        }} 
        .kpi-value {{ 
            font-family: var(--font-display);
            font-size: 1.55rem; color: var(--text-dark);
            letter-spacing: 1px; line-height: 1.2;
        }} 
        .kpi-delta {{ 
            font-family: var(--font-body);
            font-size: 0.68rem; font-weight: 600;
            margin-top: 2px; display: block;
        }} 
        .kpi-delta.positive {{  color: var(--accent-green); }} 
        .kpi-delta.negative {{  color: var(--accent-red); }} 
        .kpi-delta.neutral {{  color: var(--text-muted); }} 

        /* ==================== PERIOD CARDS ==================== */
        .period-card {{ 
            background: var(--bg-inner);
            border: 2.5px solid var(--border);
            border-radius: var(--radius);
            box-shadow: var(--shadow-sm);
            overflow: hidden;
        }} 
        .period-header {{ 
            background: linear-gradient(180deg, var(--titlebar-light) 0%, var(--titlebar) 100%);
            border-bottom: 2px solid var(--border);
            padding: 2px 8px;
            font-family: var(--font-display);
            font-size: 0.9rem; color: #fff;
            letter-spacing: 1.5px;
        }} 
        .period-body {{ 
            padding: 8px 10px;
        }} 
        .period-value {{ 
            font-family: var(--font-display);
            font-size: 1.2rem; letter-spacing: 1px;
            color: var(--text-dark); line-height: 1.3;
        }} 
        .period-detail {{ 
            font-family: var(--font-body);
            font-size: 0.72rem; color: var(--text-mid);
            margin-top: 2px;
        }} 

        /* ==================== AI INSIGHT BOX ==================== */
        .ai-insight-box {{ 
            background: var(--bg-white);
            border: 2px solid var(--border-mid);
            border-radius: var(--radius);
            padding: 10px 12px;
            margin: 6px 0;
            box-shadow: var(--shadow-inset);
        }} 
        .ai-insight-box p, .ai-insight-box li {{ 
            color: var(--text-body) !important;
            font-family: var(--font-body) !important;
            font-size: 0.78rem !important;
            line-height: 1.65 !important;
            margin: 0 !important;
        }} 

        /* ==================== CHAT ==================== */
        .chat-container {{ 
            max-height: 260px;
            overflow-y: auto;
            padding: 4px;
            background: var(--bg-white);
            border: 2px solid var(--border-mid);
            border-radius: var(--radius);
            box-shadow: var(--shadow-inset);
        }} 
        .chat-q {{ 
            background: var(--bg-panel);
            border: 1.5px solid var(--border-light);
            border-radius: var(--radius);
            padding: 6px 10px; margin: 4px 0;
            font-family: var(--font-body);
            font-size: 0.76rem; color: var(--text-dark);
        }} 
        .chat-a {{ 
            background: {chat_a_bg};
            border: 1.5px solid var(--border-light);
            border-radius: var(--radius);
            padding: 6px 10px; margin: 4px 0;
            font-family: var(--font-body);
            font-size: 0.76rem; color: var(--text-body);
            line-height: 1.5;
        }} 

        /* ==================== SIDEBAR ==================== */
        section[data-testid="stSidebar"] {{ 
            background: var(--bg-panel) !important;
            border-right: 2.5px solid var(--border) !important;
        }} 
        section[data-testid="stSidebar"] .stMarkdown h3,
        .sidebar-heading {{ 
            font-family: var(--font-display) !important;
            font-size: 1.05rem !important;
            color: var(--titlebar) !important;
            letter-spacing: 1.5px !important;
            text-transform: uppercase !important;
            border-bottom: 2px solid var(--border-light) !important;
            padding-bottom: 3px !important;
            margin-bottom: 6px !important;
            margin-top: 10px !important;
        }} 

        /* ==================== BUTTONS ==================== */
        .stButton > button {{ 
            font-family: var(--font-display) !important;
            font-size: 0.95rem !important;
            letter-spacing: 1px !important;
            border: 2px solid var(--border) !important;
            border-radius: var(--radius) !important;
            background: var(--bg-panel) !important;
            color: var(--text-dark) !important;
            box-shadow: var(--shadow-sm) !important;
            padding: 2px 4px !important;
            min-height: 30px !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            transition: all 0.05s ease !important;
        }} 
        .stButton > button:hover {{ 
            background: {btn_hover} !important;
        }} 
        .stButton > button:active {{ 
            box-shadow: inset 2px 2px 0px rgba(0,0,0,0.2) !important;
            transform: translate(1px, 1px) !important;
        }} 

        /* Sidebar buttons — smaller font */
        section[data-testid="stSidebar"] .stButton > button {{ 
            font-size: 0.82rem !important;
            padding: 2px 3px !important;
            min-height: 28px !important;
            letter-spacing: 0.5px !important;
        }} 

        /* Primary button = active selection */
        .stButton > button[kind="primary"],
        .stButton > button[data-testid="stBaseButton-primary"] {{ 
            background: var(--titlebar) !important;
            color: #fff !important;
            border: 2px solid var(--border) !important;
            box-shadow: inset 2px 2px 0px rgba(0,0,0,0.15) !important;
            text-shadow: 1px 1px 0px rgba(0,0,0,0.2);
        }} 
        .stButton > button[kind="primary"]:hover,
        .stButton > button[data-testid="stBaseButton-primary"]:hover {{ 
            background: var(--titlebar-dark) !important;
            color: #fff !important;
        }} 

        /* ==================== INPUTS ==================== */
        .stTextInput > div > div > input {{ 
            font-family: var(--font-body) !important;
            font-size: 0.78rem !important;
            border: 2px solid var(--border) !important;
            border-radius: var(--radius) !important;
            background: var(--bg-white) !important;
            color: var(--text-dark) !important;
            box-shadow: var(--shadow-inset) !important;
        }} 

        /* ==================== EMPTY STATE ==================== */
        .empty-state {{ 
            text-align: center; padding: 36px 20px;
            background: var(--bg-inner);
            border: 2.5px solid var(--border);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
        }} 
        .empty-state-icon {{  font-size: 2.5rem; margin-bottom: 6px; }} 
        .empty-state-text {{ 
            font-family: var(--font-display);
            font-size: 1.6rem; color: var(--titlebar);
            letter-spacing: 2px; margin-bottom: 4px;
        }} 
        .empty-state-hint {{ 
            font-family: var(--font-body);
            font-size: 0.78rem; color: var(--text-mid);
        }} 

        /* ==================== DATASET INFO ==================== */
        .dataset-info {{ 
            background: var(--bg-white);
            border: 2px solid var(--border-mid);
            border-radius: var(--radius);
            padding: 8px 10px;
            box-shadow: var(--shadow-inset);
        }} 
        .ds-row {{ 
            display: flex; justify-content: space-between;
            padding: 3px 0;
            border-bottom: 1px dashed var(--border-light);
            font-size: 0.76rem;
        }} 
        .ds-row:last-child {{  border-bottom: none; }} 
        .ds-label {{  color: var(--text-muted); font-weight: 500; }} 
        .ds-value {{  color: var(--text-dark); font-weight: 700; }} 

        /* ==================== DISCLAIMER ==================== */
        .disclaimer {{ 
            font-family: var(--font-body); font-size: 0.62rem;
            color: var(--text-muted); font-style: italic;
            padding: 3px 0; line-height: 1.4;
        }} 

        /* ==================== FOOTER ==================== */
        .retro-footer {{ 
            text-align: center; padding: 10px 0 6px;
            border-top: 2px solid var(--border-light);
            margin-top: 12px;
        }} 
        .retro-footer p {{ 
            font-family: var(--font-body);
            font-size: 0.65rem; color: var(--text-muted); margin: 0;
        }} 

        /* ==================== METRIC WIDGET ==================== */
        div[data-testid="stMetric"] {{ 
            background: var(--bg-inner);
            border: 2px solid var(--border);
            border-radius: var(--radius);
            padding: 6px; box-shadow: var(--shadow-sm);
        }} 

        /* ==================== DOWNLOAD BUTTON ==================== */
        .stDownloadButton > button {{ 
            font-family: var(--font-display) !important;
            font-size: 0.95rem !important;
            letter-spacing: 1px !important;
            border: 2px solid var(--border) !important;
            border-radius: var(--radius) !important;
            background: {dl_bg} !important;
            color: var(--text-dark) !important;
            box-shadow: var(--shadow-sm) !important;
        }} 

        /* ==================== EXPANDER ==================== */
        .streamlit-expanderHeader {{ 
            font-family: var(--font-display) !important;
            font-size: 1rem !important;
            letter-spacing: 1px;
            border: 2px solid var(--border) !important;
            border-radius: var(--radius) !important;
            background: var(--bg-panel) !important;
            color: var(--text-dark) !important;
        }} 

        /* ==================== SCROLLBAR ==================== */
        ::-webkit-scrollbar {{  width: 12px; }} 
        ::-webkit-scrollbar-track {{  background: {sb_track}; border-left: 1px solid var(--border-light); }} 
        ::-webkit-scrollbar-thumb {{  background: {sb_thumb}; border: 1px solid var(--border); }} 

        /* ==================== RADIO FIX ==================== */
        .stRadio > div > label {{ 
            font-family: var(--font-body) !important;
            font-size: 0.78rem !important;
            color: var(--text-dark) !important;
        }} 

        /* ==================== FILE UPLOADER ==================== */
        section[data-testid="stFileUploader"] {{ 
            border: 2px dashed var(--border-light) !important;
            border-radius: var(--radius) !important;
            background: var(--bg-inner) !important;
        }} 

        /* ==================== SEPARATOR ==================== */
        .retro-sep {{ 
            border: none;
            border-top: 2px solid var(--border-light);
            margin: 8px 0;
        }} 

        /* ==================== THEME SELECTOR ==================== */
        .theme-card {{ 
            display: flex; align-items: center; gap: 8px;
            padding: 4px 6px;
            border: 2px solid var(--border);
            border-radius: var(--radius);
            background: var(--bg-inner);
            margin-bottom: 4px;
            cursor: pointer;
        }} 
        .theme-card.active {{ 
            background: var(--titlebar);
            border-color: var(--border);
        }} 
        .theme-swatch {{ 
            width: 12px; height: 12px;
            border: 1px solid var(--border);
            display: inline-block;
        }} 

        {glass_extras}

        /* ==================== RESPONSIVE — TABLETS (≤1024px) ==================== */
        @media screen and (max-width: 1024px) {{
            .header-title {{ font-size: 1.5rem !important; letter-spacing: 1px !important; }}
            .header-subtitle {{ font-size: 0.65rem !important; }}
            .kpi-value {{ font-size: 1.25rem !important; }}
            .kpi-header {{ font-size: 0.8rem !important; padding: 2px 6px !important; }}
            .period-value {{ font-size: 1rem !important; }}
            .retro-titlebar-text {{ font-size: 0.95rem !important; }}
            .ai-insight-box p, .ai-insight-box li {{ font-size: 0.72rem !important; }}
            .chat-q, .chat-a {{ font-size: 0.7rem !important; }}
            .retro-body {{ padding: 8px !important; }}
        }}

        /* ==================== RESPONSIVE — PHONES (≤768px) ==================== */
        @media screen and (max-width: 768px) {{
            .header-bar .header-content {{ flex-direction: column; align-items: flex-start; gap: 4px; padding: 8px 10px !important; }}
            .header-title {{ font-size: 1.3rem !important; }}
            .header-subtitle {{ font-size: 0.6rem !important; }}
            .kpi-card {{ margin-bottom: 8px; }}
            .kpi-value {{ font-size: 1.1rem !important; }}
            .kpi-delta {{ font-size: 0.6rem !important; }}
            .period-card {{ margin-bottom: 8px; }}
            .period-value {{ font-size: 0.95rem !important; }}
            .period-detail {{ font-size: 0.65rem !important; }}
            .retro-titlebar {{ padding: 3px 6px !important; min-height: 22px !important; }}
            .retro-titlebar-text {{ font-size: 0.85rem !important; letter-spacing: 0.8px !important; }}
            .retro-wc-btn {{ width: 13px !important; height: 13px !important; font-size: 7px !important; }}
            .retro-body {{ padding: 6px !important; }}
            .status-badge {{ font-size: 0.75rem !important; padding: 2px 6px !important; }}
            .ai-insight-box {{ padding: 6px 8px !important; }}
            .ai-insight-box p, .ai-insight-box li {{ font-size: 0.68rem !important; line-height: 1.5 !important; }}
            .chat-container {{ max-height: 180px !important; }}
            .chat-q, .chat-a {{ font-size: 0.66rem !important; padding: 4px 6px !important; }}
            .ds-row {{ font-size: 0.68rem !important; }}
            .retro-footer p {{ font-size: 0.55rem !important; }}
            .disclaimer {{ font-size: 0.55rem !important; }}
            .stButton > button {{ font-size: 0.78rem !important; min-height: 26px !important; padding: 1px 3px !important; }}
            section[data-testid="stSidebar"] .stButton > button {{ font-size: 0.72rem !important; min-height: 24px !important; }}
        }}

        /* ==================== RESPONSIVE — SMALL PHONES (≤480px) ==================== */
        @media screen and (max-width: 480px) {{
            .header-title {{ font-size: 1.1rem !important; }}
            .kpi-value {{ font-size: 0.95rem !important; }}
            .retro-titlebar-text {{ font-size: 0.75rem !important; }}
            .chat-container {{ max-height: 140px !important; }}
        }}

        /* ==================== RESPONSIVE — LARGE / ULTRA-WIDE (≥1600px) ==================== */
        @media screen and (min-width: 1600px) {{
            .header-title {{ font-size: 2.4rem !important; }}
            .kpi-value {{ font-size: 1.8rem !important; }}
            .retro-titlebar-text {{ font-size: 1.2rem !important; }}
            .ai-insight-box p, .ai-insight-box li {{ font-size: 0.85rem !important; }}
            .chat-q, .chat-a {{ font-size: 0.82rem !important; }}
        }}
    </style>
    """
