import streamlit as st
import textwrap

def render_info_page():
    
    WC = '<div class="retro-wc"><div class="retro-wc-btn">─</div><div class="retro-wc-btn">□</div><div class="retro-wc-btn">✕</div></div>'

    def render_panel(title, icon, content_html):
        clean_html = textwrap.dedent(content_html)
        html = f"""<div class="retro-window">
<div class="retro-titlebar">
<span class="retro-titlebar-text">{icon} {title}</span>{WC}
</div>
<div class="retro-body" style="padding: 24px; color: var(--text-body);">
{clean_html}
</div>
</div>
<div style="margin-bottom: 20px;"></div>"""
        st.markdown(html, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="header-bar">
        <div class="retro-titlebar">
            <span class="retro-titlebar-text">ℹ️ SYSTEM DOCUMENTATION TERMINAL</span>
            <div style="display:flex;align-items:center;gap:8px;">
                {WC}
            </div>
        </div>
        <div class="header-content" style="padding: 30px;">
            <span style="font-size:2.5rem; margin-right: 20px;">🎓</span>
            <div>
                <p class="header-title" style="font-size:2rem; margin-bottom: 5px;">WELCOME TO INSIGHT FLOW</p>
                <p class="header-subtitle" style="font-size:1.1rem; opacity: 0.9;">AI-Assisted Conversational Analytics Workstation</p>
            </div>
        </div>
    </div>
    <div style="margin-bottom: 20px;"></div>
    """, unsafe_allow_html=True)

    cc1, cc2, cc3 = st.columns([1, 2, 1])
    with cc2:
        if st.button("🔙 RETURN TO WORKSTATION", use_container_width=True, type="primary"):
            st.session_state['show_info_page'] = False
            st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])

    with c1:
        
        render_panel("WHAT THIS SOFTWARE DOES", "⚙️", """
        <p><b>Insight Flow</b> is a lightweight analytical utility designed to reduce time spent in spreadsheets. It enables you to:</p>
        <ul style="margin-left: 20px; line-height: 1.6;">
            <li>Generate visual analytics instantly.</li>
            <li>Interact with structured data conversationally using AI.</li>
            <li>Explore KPIs, trends, and growth metrics.</li>
            <li>Export AI-assisted PDF executive reports.</li>
        </ul>
        <p style="margin-top: 15px;"><b>Note:</b> This is a temporary session workflow. There is no permanent storage.</p>
        
        <div style="padding: 12px; border-left: 4px solid var(--titlebar); background: var(--bg-inner); margin-top: 15px; border-radius: 4px; color: var(--text-dark);">
            <b>IMPORTANT:</b> This software is designed for lightweight exploratory analytical visualization, not enterprise-scale forecasting.
        </div>
        """)

        render_panel("AI SYSTEM LIMITATIONS", "🤖", """
        <p>The integrated Gemini AI operates under strict boundary conditions:</p>
        <ul style="margin-left: 20px; line-height: 1.6;">
            <li><b>Dataset-Constrained:</b> AI responses are isolated to the scope of your uploaded CSV.</li>
            <li><b>Rejection Protocol:</b> Unsupported questions (e.g., weather, sports, politics, general knowledge) will be rejected.</li>
            <li><b>No External Web Access:</b> The AI does not browse the unrestricted internet to answer queries.</li>
        </ul>

        <div style="padding: 12px; border-left: 4px solid var(--accent-red); background: var(--bg-inner); margin-top: 15px; border-radius: 4px; color: var(--text-dark);">
            <b>CRITICAL:</b> Gemini assists in interpretation but does NOT replace deterministic mathematical analytics calculations. Always verify critical business insights.
        </div>
        """)

        render_panel("DATA PRIVACY & API KEY ADVISORY", "🔐", """
        <p>When you use Insight Flow, your dataset metadata and queries are sent to Google's Gemini API for AI-powered analysis. The level of data confidentiality depends on the type of API key you use:</p>
        <ul style="margin-left: 20px; line-height: 1.8;">
            <li><b>Free-Tier API Key:</b> Google may use your prompts and data to improve its AI models. This means fragments of your business data could potentially be used for model training.</li>
            <li><b>Paid API Key (Recommended):</b> Under Google's paid API terms of service, your data is <b>not</b> used for model training or improvement. Your prompts and responses remain confidential.</li>
        </ul>
        <div style="padding: 12px; border-left: 4px solid var(--accent-blue); background: var(--bg-inner); margin-top: 15px; border-radius: 4px; color: var(--text-dark);">
            <b>RECOMMENDATION:</b> If your dataset contains sensitive, proprietary, or confidential business information, we strongly recommend using a <b>paid Gemini API key</b> to ensure your data is never used for AI training or model improvement. Your privacy is your responsibility.
        </div>
        """)

        render_panel("STATELESS PRIVACY ARCHITECTURE", "🛡️", """
        <p>Insight Flow is built on a strict privacy-first foundation:</p>
        <ul style="margin-left: 20px; line-height: 1.6;">
            <li><b>No Permanent Storage:</b> Uploaded datasets remain entirely temporary and in-memory.</li>
            <li><b>Ephemeral Sessions:</b> All data, API keys, and AI conversations disappear immediately after a browser refresh or session end.</li>
            <li><b>Local API Keys:</b> Your Gemini API key is used strictly for the active session and is not stored in any database.</li>
        </ul>
        <p style="margin-top: 15px;">This architecture ensures absolute business privacy and security for your sensitive data logs.</p>
        """)

        render_panel("SOFTWARE LIMITATIONS", "⚠️", """
        <ul style="margin-left: 20px; line-height: 1.6;">
            <li>Designed for lightweight, exploratory analytics.</li>
            <li><b>Not</b> enterprise-scale data infrastructure.</li>
            <li><b>Not</b> a real-time streaming platform.</li>
            <li><b>Not</b> a predictive forecasting engine.</li>
            <li><b>Not</b> a replacement for full-scale Enterprise BI systems (e.g., Tableau, PowerBI).</li>
        </ul>
        """)

    with c2:
        
        render_panel("CSV REQUIREMENTS & FORMATTING", "📄", """
        <p>For the system to automatically extract KPIs and build dashboards, your CSV must meet these structural requirements:</p>

        <p style="margin-top:15px;"><b>Required Columns:</b></p>
        <ol style="margin-left: 20px; line-height: 1.6;">
            <li>At least one <b>Date</b> column.</li>
            <li>At least one <b>Numeric</b> column (e.g., Revenue, Quantity).</li>
        </ol>

        <p style="margin-top:15px;"><b>Recommended Columns:</b></p>
        <ul style="margin-left: 20px; line-height: 1.6;">
            <li>Categorical columns (e.g., Region, Product, Status) for breakdown views.</li>
        </ul>

        <p style="margin-top:15px;"><b>Supported Date Formats:</b><br>
        The system automatically attempts flexible parsing for:<br>
        <code style="background: var(--bg-inner); padding: 2px 6px; border-radius: 4px; color: var(--text-dark);">YYYY-MM-DD</code> | 
        <code style="background: var(--bg-inner); padding: 2px 6px; border-radius: 4px; color: var(--text-dark);">MM/DD/YYYY</code> | 
        <code style="background: var(--bg-inner); padding: 2px 6px; border-radius: 4px; color: var(--text-dark);">DD-MM-YYYY</code></p>

        <p style="margin-top:15px;"><b>Example Valid Structure:</b></p>
        <div style="overflow-x:auto; margin-top:10px; margin-bottom:15px;">
            <table style="width:100%; border-collapse:collapse; font-family:monospace; font-size:0.9rem; background:var(--bg-white); border: 2px solid var(--border); color: var(--text-dark);">
                <thead>
                    <tr style="background:var(--bg-inner); border-bottom:2px solid var(--border);">
                        <th style="padding:8px; border-right:1px solid var(--border-light); text-align:left;">Date</th>
                        <th style="padding:8px; border-right:1px solid var(--border-light); text-align:left;">Region</th>
                        <th style="padding:8px; border-right:1px solid var(--border-light); text-align:left;">Product</th>
                        <th style="padding:8px; border-right:1px solid var(--border-light); text-align:right;">Revenue</th>
                        <th style="padding:8px; text-align:right;">Qty</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="border-bottom:1px solid var(--border-light);">
                        <td style="padding:8px; border-right:1px solid var(--border-light);">2023-01-15</td>
                        <td style="padding:8px; border-right:1px solid var(--border-light);">North</td>
                        <td style="padding:8px; border-right:1px solid var(--border-light);">Software</td>
                        <td style="padding:8px; border-right:1px solid var(--border-light); text-align:right;">1500.50</td>
                        <td style="padding:8px; text-align:right;">10</td>
                    </tr>
                    <tr style="border-bottom:1px solid var(--border-light);">
                        <td style="padding:8px; border-right:1px solid var(--border-light);">2023-01-16</td>
                        <td style="padding:8px; border-right:1px solid var(--border-light);">South</td>
                        <td style="padding:8px; border-right:1px solid var(--border-light);">Hardware</td>
                        <td style="padding:8px; border-right:1px solid var(--border-light); text-align:right;">850.00</td>
                        <td style="padding:8px; text-align:right;">5</td>
                    </tr>
                    <tr>
                        <td style="padding:8px; border-right:1px solid var(--border-light);">2023-01-17</td>
                        <td style="padding:8px; border-right:1px solid var(--border-light);">North</td>
                        <td style="padding:8px; border-right:1px solid var(--border-light);">Hardware</td>
                        <td style="padding:8px; border-right:1px solid var(--border-light); text-align:right;">1200.00</td>
                        <td style="padding:8px; text-align:right;">8</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <p><b>✅ Supported Data:</b> Sales datasets, E-commerce logs, Business KPIs, Website analytics, Time-series data.</p>
        <p><b>❌ Unsupported Data:</b> Unstructured text, PDFs, Images, Scanned documents, Corrupted CSV files.</p>
        """)

        render_panel("TERMS & CONDITIONS", "⚖️", """
        <p>By using Insight Flow, you agree to the following lightweight software terms:</p>
        <ul style="margin-left: 20px; line-height: 1.6;">
            <li><b>As-Is Provision:</b> This tool is provided "as-is" without any warranty or performance guarantees.</li>
            <li><b>Verification:</b> Analytical and AI-generated results should be independently verified before making critical business decisions.</li>
            <li><b>User Responsibility:</b> You are solely responsible for the legality and content of the datasets you upload.</li>
            <li><b>API Usage:</b> You are responsible for any external billing related to your personal Gemini API key.</li>
            <li><b>Compliance:</b> Users must comply with applicable data protection laws.</li>
        </ul>
        """)

    st.markdown("<br>", unsafe_allow_html=True)
    render_panel("BEFORE YOU CONTINUE CHECKLIST", "✅", """
    <div style="font-family: monospace; font-size: 1.1rem; line-height: 1.8;">
        ☑ My dataset contains a Date column.<br>
        ☑ My dataset contains numerical metrics.<br>
        ☑ I understand sessions are temporary and disappear upon refresh.<br>
        ☑ I understand Gemini API usage is my responsibility.<br>
        ☑ I understand unsupported non-dataset queries may be rejected.
    </div>
    """)

    cc1, cc2, cc3 = st.columns([1, 2, 1])
    with cc2:
        if st.button("🚀 I UNDERSTAND — CONTINUE TO INSIGHT FLOW", use_container_width=True, type="primary"):
            st.session_state['show_info_page'] = False
            st.rerun()

    st.markdown(f"""<div class="retro-footer" style="margin-top: 30px;"><p>
    Insight Flow v1.0 — System Documentation & Onboarding Utility
    </p></div>""", unsafe_allow_html=True)
