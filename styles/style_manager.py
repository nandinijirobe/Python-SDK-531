"""
CSS Style Manager for Misty WOZ Controller
Handles loading and applying CSS styles from the styles directory
"""

import streamlit as st
from pathlib import Path

def load_css_file(css_file_path):
    """Load CSS content from a file"""
    try:
        with open(css_file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        st.warning(f"CSS file not found: {css_file_path}")
        return ""

def apply_styles():
    """Apply all CSS styles to the Streamlit app"""
    
    # Define styles directory (current directory since we're in styles/)
    styles_dir = Path(__file__).parent
    
    # List of CSS files to load
    css_files = [
        "badges.css",      # Circular count badges
        "cards.css",       # File card styling  
        "layout.css",      # Layout and spacing
        "buttons.css"      # Button styling
    ]
    
    # Combine all CSS content
    combined_css = "/* Misty WOZ Controller Styles */\n\n"
    
    for css_file in css_files:
        css_path = styles_dir / css_file
        css_content = load_css_file(css_path)
        if css_content:
            combined_css += f"/* {css_file} */\n{css_content}\n\n"
    
    # Apply combined CSS to Streamlit
    st.markdown(f"<style>{combined_css}</style>", unsafe_allow_html=True)

def get_style_classes():
    """Return dictionary of CSS class names for easy reference"""
    return {
        # Badge classes
        'audio_count_badge': 'audio-count-badge',
        
        # Card classes  
        'file_card': 'file-card',
        'file_card_selected': 'file-card selected',
        'file_status_ready': 'file-status-ready',
        'file_status_missing': 'file-status-missing',
        
        # Layout classes
        'sidebar_section': 'sidebar-section',
        'main_content': 'main-content', 
        'content_divider': 'content-divider',
        'control_columns': 'control-columns',
        'flex_center': 'flex-center',
        
        # Button classes
        'audio_controls': 'audio-controls',
        'play_button': 'play-button',
        'stop_button': 'stop-button'
    }