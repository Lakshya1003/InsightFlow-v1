"""
Insight Flow — Theme Engine
Centralized theme configuration with CSS variable generation and Plotly sync.
"""

THEMES = {
    'Default': {
        'name': 'Default', 'icon': '🟠',
        'swatches': ['#d4b896', '#e8832a', '#1a1a1a'],
        'css': {
            'bg-main': '#d4b896', 'bg-panel': '#f0e6d3', 'bg-inner': '#faf5ee',
            'bg-white': '#ffffff', 'titlebar': '#e8832a', 'titlebar-light': '#f5a623',
            'titlebar-dark': '#cc6d1a', 'border': '#1a1a1a', 'border-mid': '#5a4a3a',
            'border-light': '#8b7355', 'text-dark': '#1a1a1a', 'text-body': '#2d2013',
            'text-mid': '#4a3728', 'text-muted': '#6b5d4e',
            'accent-green': '#2d8b4e', 'accent-red': '#c23b22', 'accent-blue': '#3a6ea5',
        },
        'plotly': {
            'paper': '#faf5ee', 'plot': '#ffffff', 'font': '#1a1a1a',
            'grid': '#e8e0d4', 'axis': '#1a1a1a', 'tick': '#4a3728',
            'hover_bg': '#faf5ee', 'hover_border': '#1a1a1a',
            'colors': ['#3a6ea5', '#e8832a', '#2d8b4e', '#c23b22', '#7c3aed',
                        '#0d9488', '#d97706', '#6366f1', '#ec4899', '#14b8a6'],
        },
        'glass': False,
    },
    'Vintage Blue': {
        'name': 'Vintage Blue', 'icon': '🔵',
        'swatches': ['#D8E2EC', '#4A6A8A', '#1F2F3F'],
        'css': {
            'bg-main': '#D8E2EC', 'bg-panel': '#E8EEF4', 'bg-inner': '#F4F7FA',
            'bg-white': '#ffffff', 'titlebar': '#4A6A8A', 'titlebar-light': '#5E82A2',
            'titlebar-dark': '#3A5670', 'border': '#1F2F3F', 'border-mid': '#3D5060',
            'border-light': '#7A98B0', 'text-dark': '#13202B', 'text-body': '#1A2D3A',
            'text-mid': '#2E4555', 'text-muted': '#5A7388',
            'accent-green': '#3A8A5C', 'accent-red': '#A04040', 'accent-blue': '#4A6A8A',
        },
        'plotly': {
            'paper': '#F4F7FA', 'plot': '#ffffff', 'font': '#13202B',
            'grid': '#D8E2EC', 'axis': '#1F2F3F', 'tick': '#2E4555',
            'hover_bg': '#F4F7FA', 'hover_border': '#1F2F3F',
            'colors': ['#4A6A8A', '#6E8FAF', '#3A8A5C', '#A04040', '#5E82A2',
                        '#2E7D6E', '#7A98B0', '#4682B4', '#5B9BD5', '#2F5496'],
        },
        'glass': False,
    },
    'Royal Gold': {
        'name': 'Royal Gold', 'icon': '👑',
        'swatches': ['#D9C2A7', '#D67B00', '#2D1A00'],
        'css': {
            'bg-main': '#D9C2A7', 'bg-panel': '#EEDCC8', 'bg-inner': '#F6E7D8',
            'bg-white': '#FFF8F0', 'titlebar': '#D67B00', 'titlebar-light': '#E8940A',
            'titlebar-dark': '#B06600', 'border': '#2D1A00', 'border-mid': '#5A3D20',
            'border-light': '#9A7B55', 'text-dark': '#2A1700', 'text-body': '#3D2A15',
            'text-mid': '#5A4230', 'text-muted': '#7A6545',
            'accent-green': '#4A8040', 'accent-red': '#B03020', 'accent-blue': '#6A7A4A',
        },
        'plotly': {
            'paper': '#F6E7D8', 'plot': '#FFF8F0', 'font': '#2A1700',
            'grid': '#EEDCC8', 'axis': '#2D1A00', 'tick': '#5A4230',
            'hover_bg': '#F6E7D8', 'hover_border': '#2D1A00',
            'colors': ['#D67B00', '#F2B544', '#4A8040', '#B03020', '#8B6914',
                        '#C4933A', '#6A4E23', '#D4A550', '#9A7530', '#B8860B'],
        },
        'glass': False,
    },
    'Dark Matte': {
        'name': 'Dark Matte', 'icon': '⬛',
        'swatches': ['#1E1E1E', '#3A3A3A', '#F5F5F5'],
        'css': {
            'bg-main': '#1E1E1E', 'bg-panel': '#252525', 'bg-inner': '#2A2A2A',
            'bg-white': '#333333', 'titlebar': '#3A3A3A', 'titlebar-light': '#484848',
            'titlebar-dark': '#2C2C2C', 'border': '#000000', 'border-mid': '#444444',
            'border-light': '#555555', 'text-dark': '#F5F5F5', 'text-body': '#E0E0E0',
            'text-mid': '#BBBBBB', 'text-muted': '#888888',
            'accent-green': '#4CAF50', 'accent-red': '#EF5350', 'accent-blue': '#64B5F6',
        },
        'plotly': {
            'paper': '#2A2A2A', 'plot': '#333333', 'font': '#F5F5F5',
            'grid': '#444444', 'axis': '#888888', 'tick': '#BBBBBB',
            'hover_bg': '#3A3A3A', 'hover_border': '#666666',
            'colors': ['#64B5F6', '#FFB74D', '#4CAF50', '#EF5350', '#CE93D8',
                        '#4DD0E1', '#FFD54F', '#90CAF9', '#F48FB1', '#80CBC4'],
        },
        'glass': False,
    },
    'Slate': {
        'name': 'Slate', 'icon': '🩶',
        'swatches': ['#BCC7D1', '#607D94', '#243746'],
        'css': {
            'bg-main': '#BCC7D1', 'bg-panel': '#D5DCE3', 'bg-inner': '#E7EDF2',
            'bg-white': '#F2F5F8', 'titlebar': '#607D94', 'titlebar-light': '#7A9AB0',
            'titlebar-dark': '#4A6578', 'border': '#243746', 'border-mid': '#3D5565',
            'border-light': '#7A95A8', 'text-dark': '#18242D', 'text-body': '#22333F',
            'text-mid': '#3A5060', 'text-muted': '#607D94',
            'accent-green': '#3D8B5A', 'accent-red': '#B04545', 'accent-blue': '#4A7A9A',
        },
        'plotly': {
            'paper': '#E7EDF2', 'plot': '#F2F5F8', 'font': '#18242D',
            'grid': '#D5DCE3', 'axis': '#243746', 'tick': '#3A5060',
            'hover_bg': '#E7EDF2', 'hover_border': '#243746',
            'colors': ['#607D94', '#879FB2', '#3D8B5A', '#B04545', '#4A7A9A',
                        '#5D8AA8', '#87CEEB', '#4682B4', '#6B8E9B', '#2C5F7C'],
        },
        'glass': False,
    },
    'Glassmorphism': {
        'name': 'Glassmorphism', 'icon': '🪟',
        'swatches': ['#E8D5F0', '#FF8C00', '#111111'],
        'css': {
            'bg-main': '#C8B8D8', 'bg-panel': 'rgba(255,255,255,0.25)',
            'bg-inner': 'rgba(255,255,255,0.30)', 'bg-white': 'rgba(255,255,255,0.40)',
            'titlebar': 'rgba(255,140,0,0.75)', 'titlebar-light': 'rgba(255,160,40,0.80)',
            'titlebar-dark': 'rgba(200,110,0,0.80)', 'border': 'rgba(0,0,0,0.55)',
            'border-mid': 'rgba(0,0,0,0.35)', 'border-light': 'rgba(0,0,0,0.20)',
            'text-dark': '#111111', 'text-body': '#1A1A1A',
            'text-mid': '#333333', 'text-muted': '#555555',
            'accent-green': '#2d8b4e', 'accent-red': '#c23b22', 'accent-blue': '#3a6ea5',
        },
        'plotly': {
            'paper': 'rgba(255,255,255,0.3)', 'plot': 'rgba(255,255,255,0.5)',
            'font': '#111111', 'grid': 'rgba(0,0,0,0.08)', 'axis': '#333333',
            'tick': '#444444', 'hover_bg': 'rgba(255,255,255,0.9)',
            'hover_border': '#333333',
            'colors': ['#FF8C00', '#3a6ea5', '#2d8b4e', '#c23b22', '#7c3aed',
                        '#0d9488', '#d97706', '#6366f1', '#ec4899', '#14b8a6'],
        },
        'glass': True,
    },
}

DEFAULT_THEME = 'Default'

def get_theme(name):
    return THEMES.get(name, THEMES[DEFAULT_THEME])

def get_theme_names():
    return list(THEMES.keys())

def get_plotly_config(theme_name):
    """Return Plotly layout defaults for the given theme."""
    t = get_theme(theme_name)['plotly']
    return {
        'paper_bgcolor': t['paper'],
        'plot_bgcolor': t['plot'],
        'font_color': t['font'],
        'grid_color': t['grid'],
        'axis_color': t['axis'],
        'tick_color': t['tick'],
        'hover_bg': t['hover_bg'],
        'hover_border': t['hover_border'],
        'colors': t['colors'],
    }
