"""
Insight Flow — AI-Assisted Business Analytics Dashboard
Retro Desktop Edition v3 — Theme engine + AI chat PDF export.
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from theme_engine import get_theme, get_theme_names, THEMES, DEFAULT_THEME
from styles import get_custom_css
from data_processor import DataProcessor, DataValidationError
from analytics_engine import AnalyticsEngine
from chart_builder import (bar_chart, line_chart, area_chart, pie_chart, donut_chart,
                           scatter_plot, stacked_bar, histogram, heatmap,
                           CHART_REGISTRY, set_chart_theme)
from gemini_handler import GeminiHandler
from pdf_generator import generate_pdf_report
from info_page import render_info_page

st.set_page_config(page_title="Insight Flow — Business Analytics", page_icon="📊",
                   layout="wide", initial_sidebar_state="expanded")

DEFAULTS = {
    'gemini_handler': GeminiHandler(), 'data_processor': DataProcessor(),
    'df': None, 'metadata': None, 'analytics_engine': None,
    'selected_chart': 'Bar', 'date_range_mode': 'All',
    'custom_start': None, 'custom_end': None,
    'ai_summary': None, 'chat_history': [],
    'selected_metric': None, 'selected_category': None,
    'env_auto_connected': False,
    'active_theme': DEFAULT_THEME,
    'show_info_page': False,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

active_theme = st.session_state['active_theme']
st.markdown(get_custom_css(active_theme), unsafe_allow_html=True)
set_chart_theme(active_theme)

WC = '<div class="retro-wc"><div class="retro-wc-btn">─</div><div class="retro-wc-btn">□</div><div class="retro-wc-btn">✕</div></div>'

def rwin_open(title, icon=""):
    return f'<div class="retro-window"><div class="retro-titlebar"><span class="retro-titlebar-text">{icon} {title}</span>{WC}</div><div class="retro-body">'

def rwin_close():
    return '</div></div>'

def kpi_html(label, value, delta=""):
    return f'<div class="kpi-card"><div class="kpi-header">▸ {label}</div><div class="kpi-body"><div class="kpi-value">{value}</div>{delta}</div></div>'

def period_html(title, icon, value, detail):
    return f'<div class="period-card"><div class="period-header">{icon} {title}</div><div class="period-body"><div class="period-value">{value}</div><div class="period-detail">{detail}</div></div></div>'

def get_gemini():
    return st.session_state['gemini_handler']

if not st.session_state['env_auto_connected']:
    st.session_state['env_auto_connected'] = True

def status_html():
    g = get_gemini()
    if g.connected:
        return '<span class="status-badge status-connected">■ CONNECTED</span>'
    elif g.api_key:
        return '<span class="status-badge status-disconnected">■ INVALID KEY</span>'
    return '<span class="status-badge status-disabled">□ OFFLINE</span>'

def btn_group(options, key, cols_per_row=3):
    """Render a retro button-group selector with CSS-highlighted active button."""
    current = st.session_state.get(key, options[0])
    rows = [options[i:i+cols_per_row] for i in range(0, len(options), cols_per_row)]
    for row in rows:
        cols = st.columns(len(row))
        for i, opt in enumerate(row):
            with cols[i]:
                is_active = (opt == current)
                btn_type = "primary" if is_active else "secondary"
                if st.button(opt, key=f"{key}_{opt}", use_container_width=True,
                             type=btn_type):
                    st.session_state[key] = opt
                    st.rerun()
    return st.session_state.get(key, options[0])

with st.sidebar:
    
    if st.button("ℹ️ INFO BEFORE YOU START", use_container_width=True, type="secondary"):
        st.session_state['show_info_page'] = True
        st.rerun()

    st.markdown('<hr style="border:1px solid rgba(0,0,0,0.15);margin:6px 0;">', unsafe_allow_html=True)

    st.markdown("### 🎨 Appearance")
    current_theme = st.session_state['active_theme']

    for tname in get_theme_names():
        tdata = THEMES[tname]
        is_active = (tname == current_theme)
        swatches = tdata['swatches']

        swatch_html = ''.join(
            f'<span style="display:inline-block;width:11px;height:11px;'
            f'background:{c};border:1px solid #333;margin-right:2px;"></span>'
            for c in swatches
        )

        btn_type = "primary" if is_active else "secondary"
        label = f"{tdata['icon']} {tname}"

        tc1, tc2 = st.columns([1, 4])
        with tc1:
            st.markdown(f'<div style="padding-top:6px;">{swatch_html}</div>',
                        unsafe_allow_html=True)
        with tc2:
            if st.button(label, key=f"theme_{tname}", use_container_width=True,
                         type=btn_type):
                st.session_state['active_theme'] = tname
                st.rerun()

    st.markdown('<hr style="border:1px solid rgba(0,0,0,0.15);margin:6px 0;">', unsafe_allow_html=True)

    st.markdown("### 🔑 Gemini API")
    api_key = st.text_input("Key", type="password", placeholder="Enter API key",
                            label_visibility="collapsed", value=get_gemini().api_key or "")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Connect", use_container_width=True):
            if api_key.strip():
                with st.spinner("Validating..."):
                    ok, msg = get_gemini().connect(api_key.strip())
                if ok:
                    st.success("✓ " + msg)
                else:
                    st.error(msg)
            else:
                st.warning("Enter a key.")
    with c2:
        if st.button("Disconnect", use_container_width=True):
            get_gemini().disconnect()
            st.session_state['ai_summary'] = None
            st.info("Disconnected.")
    st.markdown('<p class="disclaimer">Users are responsible for monitoring usage associated with their own Gemini API credentials.</p>', unsafe_allow_html=True)

    st.markdown("### 📂 Upload Dataset")
    uploaded = st.file_uploader("CSV", type=['csv'], label_visibility="collapsed")
    if uploaded is not None:
        if st.session_state.get('last_file_name') != uploaded.name:
            try:
                dp = DataProcessor()
                df = dp.validate_and_load(uploaded)
                st.session_state.update({
                    'data_processor': dp, 'df': df,
                    'metadata': dp.get_metadata(),
                    'analytics_engine': AnalyticsEngine(
                        df, dp.get_metadata()['primary_date_column'],
                        dp.get_metadata()['numeric_columns'],
                        dp.get_metadata()['categorical_columns']),
                    'selected_metric': dp.get_metadata()['numeric_columns'][0],
                    'selected_category': (dp.get_metadata()['categorical_columns'][0]
                                          if dp.get_metadata()['categorical_columns'] else None),
                    'ai_summary': None, 'chat_history': [],
                    'last_file_name': uploaded.name, 'date_range_mode': 'All',
                })
                st.success(f"✓ Loaded {len(df):,} records")
            except DataValidationError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state['df'] is not None:
        meta = st.session_state['metadata']

        st.markdown("### 📅 Date Range")
        date_opts = ['All', 'Month', '6 Mo', 'Week', 'Custom']
        btn_group(date_opts, 'date_range_mode', cols_per_row=3)

        if st.session_state['date_range_mode'] == 'Custom':
            dmin = pd.Timestamp(meta['date_range_start'])
            dmax = pd.Timestamp(meta['date_range_end'])
            cc1, cc2 = st.columns(2)
            with cc1:
                st.session_state['custom_start'] = st.date_input("From", value=dmin.date(),
                    min_value=dmin.date(), max_value=dmax.date())
            with cc2:
                st.session_state['custom_end'] = st.date_input("To", value=dmax.date(),
                    min_value=dmin.date(), max_value=dmax.date())

        st.markdown("### 📊 Chart Type")
        chart_opts = ['Bar', 'Line', 'Area', 'Pie', 'Donut', 'Scatter', 'Stack', 'Histo', 'Heat']
        btn_group(chart_opts, 'selected_chart', cols_per_row=3)

        st.markdown("### 📈 Metric")
        btn_group(meta['numeric_columns'], 'selected_metric', cols_per_row=3)

        if meta['categorical_columns']:
            st.markdown("### 🏷️ Category")
            btn_group(meta['categorical_columns'], 'selected_category', cols_per_row=3)

def get_filtered_df():
    df = st.session_state['df']
    meta = st.session_state['metadata']
    dc = meta['primary_date_column']
    mode = st.session_state['date_range_mode']
    dmax = df[dc].max()
    if mode == 'All': return df
    elif mode == 'Week': start = dmax - timedelta(days=7)
    elif mode == 'Month': start = dmax - timedelta(days=30)
    elif mode == '6 Mo': start = dmax - timedelta(days=182)
    elif mode == 'Custom':
        start = pd.Timestamp(st.session_state.get('custom_start', df[dc].min()))
        dmax = pd.Timestamp(st.session_state.get('custom_end', dmax))
    else: return df
    if mode != 'Custom':
        start = pd.Timestamp(start)
    filtered = df[(df[dc] >= start) & (df[dc] <= dmax)]
    if filtered.empty:
        st.warning("Selected date range unavailable in dataset.")
        return df
    return filtered

CHART_MAP = {
    'Bar': 'Bar Chart', 'Line': 'Line Chart', 'Area': 'Area Chart',
    'Pie': 'Pie Chart', 'Donut': 'Donut Chart', 'Scatter': 'Scatter Plot',
    'Stack': 'Stacked Bar Chart', 'Histo': 'Histogram', 'Heat': 'Heatmap',
}

if st.session_state['show_info_page']:
    render_info_page()
    st.stop()

st.markdown(f"""
<div class="header-bar">
    <div class="retro-titlebar">
        <span class="retro-titlebar-text">📊 Insight Flow v1.0</span>
        <div style="display:flex;align-items:center;gap:8px;">
            {status_html()} {WC}
        </div>
    </div>
    <div class="header-content">
        <span style="font-size:1.6rem;">📊</span>
        <div>
            <p class="header-title">Insight Flow</p>
            <p class="header-subtitle">AI-assisted business analytics dashboard for CSV datasets</p>
        </div>
    </div>
</div>""", unsafe_allow_html=True)

if st.session_state['df'] is None:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">📊</div>
        <p class="empty-state-text">Welcome to Insight Flow</p>
        <p class="empty-state-hint">Upload a CSV dataset from the sidebar to begin analytics.</p>
        <p class="empty-state-hint" style="margin-top:4px;">Connect your Gemini API key for AI-powered insights.</p>
    </div>""", unsafe_allow_html=True)
    st.stop()

fdf = get_filtered_df()
meta = st.session_state['metadata']
engine = st.session_state['analytics_engine']
dc = meta['primary_date_column']
sel_metric = st.session_state['selected_metric']
sel_cat = st.session_state['selected_category']
chart_short = st.session_state['selected_chart']
chart_type = CHART_MAP.get(chart_short, 'Bar Chart')

kpis = engine.compute_kpis(fdf)
growth = engine.compute_growth(fdf, sel_metric)
periods = engine.best_worst_periods(fdf, sel_metric)

st.markdown(rwin_open("KEY PERFORMANCE INDICATORS", "📊"), unsafe_allow_html=True)

kpi_cols = st.columns(min(len(meta['numeric_columns'][:5]), 5))
for i, col in enumerate(meta['numeric_columns'][:5]):
    with kpi_cols[i]:
        v = kpis[col]
        delta = ""
        if i == 0 and growth:
            g = growth['growth_pct']
            cls = 'positive' if g > 0 else ('negative' if g < 0 else 'neutral')
            arr = '▲' if g > 0 else ('▼' if g < 0 else '►')
            delta = f'<span class="kpi-delta {cls}">{arr} {abs(g)}% vs prior</span>'
        st.markdown(kpi_html(col, f"{v['total']:,.2f}", delta), unsafe_allow_html=True)

st.markdown(rwin_close(), unsafe_allow_html=True)

p1, p2 = st.columns(2)
with p1:
    st.markdown(period_html("BEST PERFORMING", "🏆",
        periods['best'], f"{sel_metric}: {periods['best_value']:,.2f}"), unsafe_allow_html=True)
with p2:
    st.markdown(period_html("LOWEST PERFORMING", "📉",
        periods['worst'], f"{sel_metric}: {periods['worst_value']:,.2f}"), unsafe_allow_html=True)

st.markdown(rwin_open("DATA VISUALIZATION", "📊"), unsafe_allow_html=True)

vc1, vc2 = st.columns(2)

current_figs = []

with vc1:
    try:
        fig1 = None
        if chart_type == 'Heatmap':
            corr = engine.correlation_matrix(fdf)
            if corr is not None:
                fig1 = heatmap(corr)
            else:
                st.info("Need ≥2 numeric columns.")
        elif chart_type in ('Pie Chart', 'Donut Chart'):
            if sel_cat:
                cd = engine.category_breakdown(fdf, sel_metric, sel_cat)
                if cd is not None:
                    fn = pie_chart if chart_type == 'Pie Chart' else donut_chart
                    fig1 = fn(cd.head(10), names=sel_cat, values=sel_metric,
                        title=f"{sel_metric} by {sel_cat}")
            else:
                st.info("Select a category.")
        elif chart_type == 'Histogram':
            fig1 = histogram(fdf, x=sel_metric,
                title=f"{sel_metric} Distribution")
        elif chart_type == 'Scatter Plot':
            other = [c for c in meta['numeric_columns'] if c != sel_metric]
            y_col = other[0] if other else sel_metric
            fig1 = scatter_plot(fdf, x=sel_metric, y=y_col, color=sel_cat,
                title=f"{sel_metric} vs {y_col}")
        elif chart_type == 'Stacked Bar Chart':
            if sel_cat:
                m = fdf.copy()
                m['_m'] = m[dc].dt.to_period('M').astype(str)
                g2 = m.groupby(['_m', sel_cat])[sel_metric].sum().reset_index()
                fig1 = stacked_bar(g2, x='_m', y=sel_metric, color=sel_cat,
                    title=f"{sel_metric} by {sel_cat}")
            else:
                st.info("Select a category.")
        else:
            monthly = engine.monthly_aggregation(fdf, sel_metric)
            fn = CHART_REGISTRY.get(chart_type, bar_chart)
            fig1 = fn(monthly, x='month_label', y=sel_metric,
                title=f"{sel_metric} — Monthly Trend")
        
        if fig1 is not None:
            st.plotly_chart(fig1, use_container_width=True)
            current_figs.append(fig1)
    except Exception as e:
        st.error(f"Chart error: {e}")

with vc2:
    try:
        fig2 = None
        monthly2 = engine.monthly_aggregation(fdf, sel_metric)
        if chart_type != 'Line Chart':
            fig2 = line_chart(monthly2, x='month_label', y=sel_metric,
                title=f"{sel_metric} — Trend Line")
        else:
            fig2 = bar_chart(monthly2, x='month_label', y=sel_metric,
                title=f"{sel_metric} — Bar View")
        
        if fig2 is not None:
            st.plotly_chart(fig2, use_container_width=True)
            current_figs.append(fig2)
    except Exception as e:
        st.error(f"Chart error: {e}")

if sel_cat:
    cc1, cc2 = st.columns(2)
    cd = engine.category_breakdown(fdf, sel_metric, sel_cat)
    if cd is not None and len(cd) > 0:
        with cc1:
            fig3 = bar_chart(cd.head(15), x=sel_cat, y=sel_metric,
                title=f"{sel_metric} by {sel_cat}")
            st.plotly_chart(fig3, use_container_width=True)
            current_figs.append(fig3)
        with cc2:
            fig4 = donut_chart(cd.head(10), names=sel_cat, values=sel_metric,
                title=f"{sel_cat} Distribution")
            st.plotly_chart(fig4, use_container_width=True)
            current_figs.append(fig4)

st.markdown(rwin_close(), unsafe_allow_html=True)

sum_col, chat_col = st.columns(2)

with sum_col:
    st.markdown(rwin_open("EXECUTIVE SUMMARY", "📋"), unsafe_allow_html=True)
    if get_gemini().connected:
        if st.session_state['ai_summary'] is None:
            with st.spinner("Generating..."):
                st.session_state['ai_summary'] = get_gemini().generate_summary(
                    engine.generate_summary_text(fdf), meta)
        if st.session_state['ai_summary']:
            summary = st.session_state['ai_summary']
            safe = summary.replace('<', '&lt;').replace('>', '&gt;')
            st.markdown(f'<div class="ai-insight-box"><p>{safe}</p></div>', unsafe_allow_html=True)
        if st.button("🔄 REGENERATE SUMMARY", use_container_width=True):
            with st.spinner("Regenerating..."):
                st.session_state['ai_summary'] = get_gemini().generate_summary(
                    engine.generate_summary_text(fdf), meta)
            st.rerun()
    else:
        st.markdown('<div class="ai-insight-box"><p>🔒 AI offline. Connect Gemini API key in sidebar.</p></div>', unsafe_allow_html=True)
    st.markdown(rwin_close(), unsafe_allow_html=True)

with chat_col:
    st.markdown(rwin_open("ASK YOUR DATA", "💬"), unsafe_allow_html=True)
    if get_gemini().connected:
        user_q = st.text_input("Question", placeholder="Type your question about your dataset...",
                               label_visibility="collapsed", key="chat_input")
        if st.button("ASK", key="ask_btn"):
            if user_q and user_q.strip():
                with st.spinner("Analyzing..."):
                    answer = get_gemini().ask_question(user_q.strip(),
                        engine.generate_summary_text(fdf), meta)
                st.session_state['chat_history'].append(('user', user_q.strip()))
                st.session_state['chat_history'].append(('ai', answer))

        if st.session_state['chat_history']:
            chat_html = '<div class="chat-container">'
            for role, msg in st.session_state['chat_history']:
                safe = msg.replace('<', '&lt;').replace('>', '&gt;')
                if role == 'user':
                    chat_html += f'<div class="chat-q"><b>Q:</b> {safe}</div>'
                else:
                    chat_html += f'<div class="chat-a"><b>A:</b> {safe}</div>'
            chat_html += '</div>'
            st.markdown(chat_html, unsafe_allow_html=True)

            if st.button("CLEAR CHAT", key="clear_chat", use_container_width=True):
                st.session_state['chat_history'] = []
                st.rerun()
    else:
        st.markdown('<div class="ai-insight-box"><p>🔒 Connect Gemini to ask questions.</p></div>', unsafe_allow_html=True)
    st.markdown(rwin_close(), unsafe_allow_html=True)

with st.expander("📋 Dataset Inspector", expanded=False):
    d1, d2 = st.columns(2)
    with d1:
        st.markdown(f"""<div class="dataset-info">
            <div class="ds-row"><span class="ds-label">Rows</span><span class="ds-value">{meta['total_rows']:,}</span></div>
            <div class="ds-row"><span class="ds-label">Columns</span><span class="ds-value">{meta['total_columns']}</span></div>
            <div class="ds-row"><span class="ds-label">Date Col</span><span class="ds-value">{meta['primary_date_column']}</span></div>
            <div class="ds-row"><span class="ds-label">Range</span><span class="ds-value">{meta['date_range_start']} to {meta['date_range_end']}</span></div>
            <div class="ds-row"><span class="ds-label">Span</span><span class="ds-value">{meta['date_span_days']} days</span></div>
        </div>""", unsafe_allow_html=True)
    with d2:
        st.markdown(f"**Numeric:** {', '.join(meta['numeric_columns'])}")
        st.markdown(f"**Categorical:** {', '.join(meta['categorical_columns']) if meta['categorical_columns'] else 'None'}")
    st.dataframe(st.session_state['df'].head(), use_container_width=True)

st.markdown(rwin_open("REPORT EXPORT", "📄"), unsafe_allow_html=True)
re1, re2 = st.columns([3, 1])
with re1:
    chat_count = sum(1 for r, _ in st.session_state['chat_history'] if r == 'user')
    chat_note = f" + {chat_count} AI conversations" if chat_count else ""
    st.markdown(f'<p style="font-size:0.8rem;color:var(--text-body);margin:0;">Generate a professional PDF report with all-time analysis{chat_note}.</p>', unsafe_allow_html=True)
with re2:
    if st.button("📄 GENERATE PDF REPORT", use_container_width=True, key="pdf_btn"):
        with st.spinner("Generating..."):
            try:
                full_df = st.session_state['df']
                all_kpis = engine.compute_kpis(full_df)
                all_summary = engine.generate_summary_text(full_df)
                ai_sum = st.session_state.get('ai_summary', '')
                
                chat_hist = st.session_state.get('chat_history', [])
                pdf_buf = generate_pdf_report(
                    full_df, dc, meta['numeric_columns'],
                    meta['categorical_columns'], all_kpis, all_summary, ai_sum, current_figs,
                    chat_history=chat_hist if chat_hist else None)
                st.download_button("⬇️ Download", data=pdf_buf,
                    file_name=f"InsightFlow_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf", use_container_width=True)
                st.success("✓ Report ready!")
            except Exception as e:
                st.error(f"PDF failed: {e}")
st.markdown(rwin_close(), unsafe_allow_html=True)

st.markdown(f"""<div class="retro-footer"><p>
Insight Flow v1.0 — AI-Assisted Business Analytics Dashboard<br>
Built with Streamlit • Pandas • Plotly • Gemini AI • ReportLab<br>
Theme: {active_theme}
</p></div>""", unsafe_allow_html=True)
