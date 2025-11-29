"""
UI Components Module
Handles Streamlit UI components and display logic
"""

import streamlit as st
import glob
from .file_storage import get_script_files, add_script_file, remove_script_file
from .audio_manager import upload_mp3_to_misty, get_misty_audio_files, play_mp3_on_misty, pause_audio_on_misty, resume_audio_on_misty, stop_audio_on_misty, auto_stop_audio

def get_mp3_files():
    """Get all MP3 files in the root directory"""
    mp3_files = glob.glob("*.mp3")
    return mp3_files

def render_script_section(script_name, script_key, volume):
    """Render UI section for a marketing script"""
    st.header(f"📁 {script_name}")
    
    # File upload section
    uploaded_files = st.file_uploader(
        f"Upload MP3 files for {script_name}",
        type=["mp3"],
        accept_multiple_files=True,
        key=f"upload_{script_key}"
    )
    
    # Process uploaded files
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if uploaded_file.name not in get_script_files(script_key):
                # Save file locally
                with open(uploaded_file.name, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                # Add to script files
                add_script_file(script_key, uploaded_file.name)
                st.success(f"✅ Added: {uploaded_file.name}")
    
    # Display current files for this script
    script_files = get_script_files(script_key)
    misty_files = get_misty_audio_files()
    
    if script_files:
        # Create count badge
        count_badge = f'<span class="audio-count-badge">{len(script_files)}</span>'
        st.markdown(f"**Files ({len(script_files)})** {count_badge}", unsafe_allow_html=True)
        
        cols = st.columns(min(3, len(script_files)))
        for idx, filename in enumerate(script_files):
            with cols[idx % 3]:
                # Check if file exists on Misty
                is_on_misty = filename in misty_files
                status_color = "🟢" if is_on_misty else "🟡"
                
                with st.container():
                    st.markdown(f'<div class="file-card">', unsafe_allow_html=True)
                    st.markdown(f"**{status_color} {filename}**")
                    
                    # Add upload button for files not on Misty
                    if not is_on_misty:
                        if st.button("📤 Upload to Misty", key=f"upload_{script_key}_{filename}", help="Upload to robot"):
                            with st.spinner(f"Uploading {filename}..."):
                                success, msg = upload_mp3_to_misty(filename, filename)
                                if success:
                                    st.success(msg)
                                    st.rerun()
                                else:
                                    st.error(msg)
                    
                    # Control buttons
                    button_cols = st.columns([1, 1, 1])
                    
                    with button_cols[0]:
                        # Single Play/Pause toggle button
                        is_playing_key = f"playing_{script_key}_{filename}"
                        is_playing = st.session_state.get(is_playing_key, False)
                        
                        if is_playing:
                            button_text = "⏸️"
                            button_help = "Pause audio"
                        else:
                            button_text = "▶️"
                            button_help = "Play/Resume audio"
                        
                        if st.button(button_text, key=f"playpause_{script_key}_{filename}", help=button_help):
                            if is_playing:
                                # Currently playing, so pause
                                success, message = pause_audio_on_misty()
                                if success:
                                    st.session_state[is_playing_key] = False
                                    st.write("⏸️")
                                else:
                                    st.write("❌")
                            else:
                                # Currently paused/stopped, so play/resume
                                success, message = resume_audio_on_misty()
                                if not success:
                                    # If resume failed, try to upload and play from beginning
                                    if not is_on_misty:
                                        with st.spinner(f"Uploading {filename}..."):
                                            upload_success, upload_msg = upload_mp3_to_misty(filename, filename)
                                            if not upload_success:
                                                st.error(upload_msg)
                                                return
                                            is_on_misty = True
                                    
                                    # Play from beginning
                                    success, message = play_mp3_on_misty(filename, volume)
                                
                                if success:
                                    st.session_state[is_playing_key] = True
                                    st.write("🎵")
                                else:
                                    st.write("❌")
                    
                    with button_cols[1]:
                        if st.button("⏹️", key=f"stop_{script_key}_{filename}", help="Stop (reset to beginning)"):
                            success, message = stop_audio_on_misty()
                            if success:
                                st.session_state[f"playing_{script_key}_{filename}"] = False  # Reset playing state
                                st.write("⏹️")
                            else:
                                st.write("❌")
                    
                    with button_cols[2]:
                        if st.button("🗑️", key=f"delete_{script_key}_{filename}", help="Delete"):
                            # Auto-stop before deletion
                            auto_stop_audio()
                            # Remove from script
                            remove_script_file(script_key, filename)
                            # Delete local file
                            try:
                                import os
                                if os.path.exists(filename):
                                    os.remove(filename)
                            except:
                                pass
                            st.success(f"🗑️ Deleted: {filename}")
                            st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info(f"No files uploaded for {script_name} yet.")