"""
Insight Flow — PDF Report Generator v2
Professional executive-style PDF reports with AI conversation history.
Always uses ALL-TIME date range regardless of current dashboard filter.
"""
import io
import logging
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, Image, PageBreak, HRFlowable)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

BRAND_BLUE = colors.HexColor('#2563eb')
BRAND_DARK = colors.HexColor('#1e293b')
BRAND_GRAY = colors.HexColor('#64748b')
BRAND_LIGHT = colors.HexColor('#f8fafc')
BRAND_BORDER = colors.HexColor('#e2e8f0')
BRAND_ORANGE = colors.HexColor('#e8832a')
BRAND_CREAM = colors.HexColor('#faf5ee')

logger = logging.getLogger(__name__)

def plotly_figure_to_png(fig):
    """
    Export a Plotly figure to a PNG ByteIO buffer robustly.
    
    This helper exists because Streamlit Community Cloud often lacks a Google Chrome 
    installation, which Kaleido v1+ requires to render images. Older Kaleido (0.2.1) 
    bundles Chromium but can still be unstable in headless Linux environments. 
    This function catches RuntimeError, ChromeNotFoundError, and generic exceptions
    and provides a graceful fallback rather than crashing the PDF generator.
    """
    try:
        
        img_bytes = fig.to_image(format="png", width=800, height=400, scale=2, engine="kaleido")
        return io.BytesIO(img_bytes)
    except Exception as e:
        logger.error(f"Plotly image export failed: {e}", exc_info=True)
        return None

def _get_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='ReportTitle', fontName='Helvetica-Bold',
        fontSize=22, textColor=BRAND_DARK, spaceAfter=6, alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='ReportSubtitle', fontName='Helvetica',
        fontSize=10, textColor=BRAND_GRAY, spaceAfter=20, alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='SectionHead', fontName='Helvetica-Bold',
        fontSize=13, textColor=BRAND_BLUE, spaceBefore=16, spaceAfter=8))
    styles.add(ParagraphStyle(name='BodyText2', fontName='Helvetica',
        fontSize=9.5, textColor=BRAND_DARK, leading=14, spaceAfter=6))
    styles.add(ParagraphStyle(name='SmallGray', fontName='Helvetica',
        fontSize=8, textColor=BRAND_GRAY, alignment=TA_CENTER))
    
    styles.add(ParagraphStyle(name='ChatSectionHead', fontName='Helvetica-Bold',
        fontSize=13, textColor=BRAND_ORANGE, spaceBefore=16, spaceAfter=10))
    styles.add(ParagraphStyle(name='ChatQuestion', fontName='Helvetica-Bold',
        fontSize=9.5, textColor=BRAND_DARK, leading=13, spaceAfter=2,
        leftIndent=6))
    styles.add(ParagraphStyle(name='ChatAnswer', fontName='Helvetica',
        fontSize=9, textColor=colors.HexColor('#334155'), leading=13,
        spaceAfter=4, leftIndent=14))
    styles.add(ParagraphStyle(name='ChatLabel', fontName='Helvetica-Bold',
        fontSize=8.5, textColor=BRAND_GRAY, spaceAfter=1))
    return styles

def _safe_text(text):
    """Escape HTML entities for ReportLab paragraphs."""
    if not text:
        return ""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def _build_chat_section(elements, styles, chat_history):
    """Add AI conversation history section to the PDF."""
    if not chat_history:
        return

    elements.append(PageBreak())
    elements.append(Paragraph("AI Analytics Conversation History", styles['ChatSectionHead']))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=BRAND_ORANGE))
    elements.append(Spacer(1, 10))

    pairs = []
    i = 0
    while i < len(chat_history):
        role, msg = chat_history[i]
        if role == 'user':
            question = msg
            answer = ""
            if i + 1 < len(chat_history) and chat_history[i + 1][0] == 'ai':
                answer = chat_history[i + 1][1]
                i += 2
            else:
                i += 1
            pairs.append((question, answer))
        else:
            
            pairs.append(("", msg))
            i += 1

    for idx, (question, answer) in enumerate(pairs):
        q_num = idx + 1

        qa_data = []

        if question:
            safe_q = _safe_text(question)
            qa_data.append([
                Paragraph(f"<b>Question {q_num}:</b>", styles['ChatLabel']),
            ])
            qa_data.append([
                Paragraph(f'"{safe_q}"', styles['ChatQuestion']),
            ])

        if answer:
            safe_a = _safe_text(answer)
            qa_data.append([
                Paragraph("<b>AI Response:</b>", styles['ChatLabel']),
            ])
            
            for line in safe_a.split('\n'):
                line = line.strip()
                if line:
                    line = line.lstrip('*-– ')
                    qa_data.append([
                        Paragraph(line, styles['ChatAnswer']),
                    ])

        if qa_data:
            qa_table = Table(qa_data, colWidths=[460])

            bg_color = BRAND_LIGHT if idx % 2 == 0 else colors.white

            table_style = [
                ('BACKGROUND', (0, 0), (-1, -1), bg_color),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (0, 0), 8),
                ('BOTTOMPADDING', (0, -1), (-1, -1), 8),
                ('BOX', (0, 0), (-1, -1), 0.8, BRAND_BORDER),
            ]

            if question:
                table_style.append(
                    ('LINEBEFOREDECOR', (0, 0), (0, -1), 3, BRAND_ORANGE)
                )

            qa_table.setStyle(TableStyle(table_style))
            elements.append(qa_table)
            elements.append(Spacer(1, 8))

    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        f"Total conversations: {len(pairs)} Q&amp;A exchanges",
        styles['SmallGray']))

def generate_pdf_report(df, date_col, numeric_cols, categorical_cols,
                        kpis, analytics_summary, ai_summary,
                        chart_figures=None, chat_history=None):
    """Generate a professional PDF report with optional AI chat history.
    
    Args:
        chat_history: List of (role, message) tuples from session state.
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
        leftMargin=25*mm, rightMargin=25*mm, topMargin=20*mm, bottomMargin=20*mm)
    styles = _get_styles()
    elements = []

    elements.append(Spacer(1, 40))
    elements.append(Paragraph("Insight Flow", styles['ReportTitle']))
    elements.append(Paragraph("AI-Assisted Business Analytics Report", styles['ReportSubtitle']))
    elements.append(HRFlowable(width="100%", thickness=1, color=BRAND_BORDER))
    elements.append(Spacer(1, 12))

    date_min = df[date_col].min().strftime('%B %d, %Y')
    date_max = df[date_col].max().strftime('%B %d, %Y')
    gen_date = datetime.now().strftime('%B %d, %Y at %I:%M %p')

    meta_data = [
        ['Report Type', 'All-Time Business Analytics'],
        ['Analysis Period', f'{date_min} — {date_max}'],
        ['Total Records', f'{len(df):,}'],
        ['Generated On', gen_date],
    ]
    if chat_history:
        n_pairs = sum(1 for r, _ in chat_history if r == 'user')
        meta_data.append(['AI Conversations', f'{n_pairs} Q&A exchanges included'])

    meta_table = Table(meta_data, colWidths=[120, 340])
    meta_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('TEXTCOLOR', (0,0), (0,-1), BRAND_GRAY),
        ('TEXTCOLOR', (1,0), (1,-1), BRAND_DARK),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Executive Summary", styles['SectionHead']))
    if ai_summary:
        for line in ai_summary.split('\n'):
            line = line.strip()
            if line:
                line = _safe_text(line)
                line = line.lstrip('*-– ')
                elements.append(Paragraph(f"  {line}", styles['BodyText2']))
    else:
        elements.append(Paragraph("AI summary not available. Connect Gemini API for insights.", styles['BodyText2']))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Key Performance Indicators", styles['SectionHead']))
    kpi_rows = [['Metric', 'Total', 'Average', 'Min', 'Max']]
    for col, vals in kpis.items():
        kpi_rows.append([col, f"{vals['total']:,.2f}", f"{vals['mean']:,.2f}",
                         f"{vals['min']:,.2f}", f"{vals['max']:,.2f}"])

    kpi_table = Table(kpi_rows, colWidths=[100, 95, 95, 85, 85])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BRAND_BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('TEXTCOLOR', (0,1), (-1,-1), BRAND_DARK),
        ('ALIGN', (1,0), (-1,-1), 'RIGHT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, BRAND_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BRAND_LIGHT]),
    ]))
    elements.append(kpi_table)
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Detailed Analytics", styles['SectionHead']))
    for line in analytics_summary.split('\n'):
        line = line.strip()
        if line:
            line = _safe_text(line)
            elements.append(Paragraph(line, styles['BodyText2']))
    elements.append(Spacer(1, 10))

    if chart_figures:
        elements.append(PageBreak())
        elements.append(Paragraph("Visual Analytics", styles['SectionHead']))
        for i, fig in enumerate(chart_figures):
            img_buf = plotly_figure_to_png(fig)
            if img_buf is not None:
                img = Image(img_buf, width=460, height=230)
                elements.append(img)
                elements.append(Spacer(1, 14))
            else:
                logger.warning(f"Chart {i+1} failed to export. Inserting placeholder.")
                elements.append(Paragraph(
                    f"<i>[Chart {i+1} could not be rendered due to a server-side image export limitation.]</i>", 
                    styles['BodyText2']
                ))
                elements.append(Spacer(1, 14))

    if chat_history:
        _build_chat_section(elements, styles, chat_history)

    elements.append(Spacer(1, 30))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=BRAND_BORDER))
    footer_text = f"Generated by Insight Flow Analytics  {gen_date}  All-Time Analysis"
    if chat_history:
        footer_text += "  (includes AI conversation history)"
    elements.append(Paragraph(footer_text, styles['SmallGray']))

    doc.build(elements)
    buf.seek(0)
    return buf
