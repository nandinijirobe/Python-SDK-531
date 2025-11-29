#!/usr/bin/env python3
"""
Streamlit GUI for Misty WOZ Controller
Main application file - imports modular components
"""

import streamlit as st
from styles.style_manager import apply_styles, get_style_classes
from woz_modules.audio_manager import auto_stop_audio, set_volume_on_misty, test_robot_connection
from woz_modules.robot_control import reset_misty_body, get_marketing_scripts, misty_listen
from woz_modules.ui_components import render_script_section

def main():
    st.set_page_config(
        page_title="Misty WOZ Controller",
        page_icon="🤖",
        layout="wide"
    )
    
    # Auto-stop any playing audio when page loads/refreshes
    if 'page_loaded' not in st.session_state:
        auto_stop_audio()
        st.session_state.page_loaded = True
    
    # Apply CSS styles
    apply_styles()
    styles = get_style_classes()
    
    st.title("🤖 Misty WOZ Controller")
    st.write("Control Misty robot for marketing scenarios using MP3 files")
    
    # Sidebar for configuration
    st.sidebar.header("⚙️ Configuration")
    volume = st.sidebar.slider("Volume", 0, 100, 100)
    
    # Connection test
    if st.sidebar.button("🔍 Test Robot Connection", help="Check if Misty robot is accessible"):
        success, message = test_robot_connection()
        if success:
            st.sidebar.success(message)
        else:
            st.sidebar.error(message)
    
    # Body reset section in sidebar
    st.sidebar.header("🔄 Body Control")
    
    # Create two columns for buttons
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("🔄 Body Reset", help="Reset Misty's body to normal position"):
            success, message = reset_misty_body()
            if success:
                st.sidebar.success(message)
            else:
                st.sidebar.error(message)
    
    with col2:
        if st.button("👂 Listen", help="Misty nods and shows curious expression"):
            success, message = misty_listen()
            if success:
                st.sidebar.success(message)
            else:
                st.sidebar.error(message)
    
    # Real-time volume control
    if 'last_volume' not in st.session_state:
        st.session_state.last_volume = 100
    
    # Check if volume changed and update Misty
    if volume != st.session_state.last_volume:
        success, message = set_volume_on_misty(volume)
        if success:
            st.sidebar.success(f"🔊 {volume}%")
        else:
            st.sidebar.error("Volume failed")
        st.session_state.last_volume = volume
    
    # Create tabs for different marketing scripts
    scripts = get_marketing_scripts()
    script_names = list(scripts.keys())
    
    if script_names:
        tabs = st.tabs(script_names)
        
        for i, (script_name, script_key) in enumerate(scripts.items()):
            with tabs[i]:
                render_script_section(script_name, script_key, volume)
    
    # Add help section
    with st.expander("ℹ️ How to Use"):
        st.markdown("""
        **Steps:**
        1. **Upload MP3 files** in each marketing script tab
        2. **Adjust volume** using the sidebar slider (real-time)
        3. **Play audio** using ▶️ buttons (auto-uploads to Misty if needed)
        4. **Control playback** with pause ⏸️ and stop ⏹️ buttons
        4. **Quick Controls**: Use LED buttons for immediate visual feedback
        
        **WOZ Marketing Scripts:**
        - **Attracting Customers**: Purple LED + audio
        - **Greeting**: Happy face + audio  
        - **Product Info**: Arm movements + audio
        - **Closing**: Cyan LED + audio
        
        **Files Status:**
        - ✅ Green = File is on Misty robot (ready to play)
        - ⚠️ Yellow = File is only local (needs upload)
        """)

if __name__ == "__main__":
    main()