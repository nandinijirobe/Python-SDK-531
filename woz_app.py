#!/usr/bin/env python3
"""
Streamlit GUI for Misty WOZ Controller
Handles MP3 playback and script execution for marketing scenarios
"""

import streamlit as st
import time
from pathlib import Path
from mistyPy.Robot import Robot
import glob
import os
import requests
import base64
import json
from styles.style_manager import apply_styles, get_style_classes

# Configuration
ROBOT_IP = "192.168.0.41"
SCRIPTS_DIR = Path(__file__).parent / "scripts"

def get_mp3_files():
    """Get all MP3 files in the root directory"""
    mp3_files = glob.glob("*.mp3")
    return mp3_files

def load_script_files():
    """Load script files from persistent storage"""
    try:
        with open('script_files.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_script_files(script_files):
    """Save script files to persistent storage"""
    with open('script_files.json', 'w') as f:
        json.dump(script_files, f, indent=2)

def get_script_files(script_name):
    """Get files for a specific marketing script"""
    script_files = load_script_files()
    return script_files.get(script_name, [])

def add_script_file(script_name, filename):
    """Add a file to a specific marketing script"""
    script_files = load_script_files()
    if script_name not in script_files:
        script_files[script_name] = []
    if filename not in script_files[script_name]:
        script_files[script_name].append(filename)
    save_script_files(script_files)

def remove_script_file(script_name, filename):
    """Remove a file from a specific marketing script"""
    script_files = load_script_files()
    if script_name in script_files and filename in script_files[script_name]:
        script_files[script_name].remove(filename)
        save_script_files(script_files)
        # Auto-stop any playing audio when deleting file
        auto_stop_audio()

def upload_audio_to_misty(file_content, filename):
    """Upload audio file directly to Misty robot"""
    try:
        # Encode file content to base64
        file_base64 = base64.b64encode(file_content).decode('utf-8')
        
        # Prepare the request
        url = f"http://{ROBOT_IP}/api/audio"
        
        payload = {
            "FileName": filename,
            "Data": file_base64,
            "ImmediatelyApply": True,
            "OverwriteExisting": True
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Send POST request to upload
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            return True, f"✅ Successfully uploaded: {filename}"
        else:
            return False, f"❌ Upload failed. Status: {response.status_code}"
            
    except Exception as e:
        return False, f"❌ Upload error: {str(e)}"

def get_misty_audio_files():
    """Get list of audio files currently on Misty robot"""
    try:
        response = requests.get(f"http://{ROBOT_IP}/api/audio/list")
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "Success":
                files = [item["name"] for item in data.get("result", [])]
                return files
        return []
    except:
        return []

def play_mp3_on_misty(filename, volume=90):
    """Play MP3 file on Misty robot"""
    try:
        misty = Robot(ROBOT_IP)
        
        # ==== VOLUME BOOST CONTROL ====
        # Adjust this value to match TTS loudness:
        # 1.0 = no boost (same as slider)
        # 0.8 = 20% quieter than slider
        # 1.2 = 20% louder than slider
        VOLUME_BOOST = 1.9  # ← CHANGE THIS VALUE TO TEST LOUDNESS
        # ===============================   
        
        mp3_volume = min(100, int(volume * VOLUME_BOOST))
        
        # Set volume first
        misty.set_default_volume(mp3_volume)
        
        # Play the audio file
        response = misty.play_audio(fileName=filename, volume=mp3_volume)
        
        if response.status_code == 200:
            return True, f"✅ Playing: {filename} (slider:{volume} → actual:{mp3_volume})"
        elif response.status_code == 500:
            return False, f"❌ Audio file '{filename}' not found on Misty. Please upload it first."
        else:
            return False, f"❌ Failed to play audio. Status: {response.status_code}"
            
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def pause_audio_on_misty():
    """Pause audio playback on Misty robot (can be resumed)"""
    try:
        misty = Robot(ROBOT_IP)
        response = misty.pause_audio()
        
        if response.status_code == 200:
            return True, "⏸️ Audio paused"
        else:
            # If pause doesn't work, try stop as fallback
            response = misty.stop_audio()
            if response.status_code == 200:
                return True, "⏸️ Audio paused (stopped)"
            return False, f"❌ Failed to pause audio. Status: {response.status_code}"
            
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def resume_audio_on_misty():
    """Resume paused audio on Misty robot"""
    try:
        misty = Robot(ROBOT_IP)
        response = misty.resume_audio()
        
        if response.status_code == 200:
            return True, "▶️ Audio resumed"
        else:
            return False, f"❌ Failed to resume audio. Status: {response.status_code}"
            
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def stop_audio_on_misty():
    """Stop audio and reset to beginning (00:00) on Misty robot"""
    try:
        misty = Robot(ROBOT_IP)
        response = misty.stop_audio()
        
        if response.status_code == 200:
            return True, "⏹️ Audio stopped (reset to 00:00)"
        else:
            return False, f"❌ Failed to stop audio. Status: {response.status_code}"
            
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def auto_stop_audio():
    """Silently stop any playing audio (for cleanup)"""
    try:
        misty = Robot(ROBOT_IP)
        misty.stop_audio()
        return True
    except:
        return False

def set_volume_on_misty(volume):
    """Set volume on Misty robot in real-time"""
    try:
        misty = Robot(ROBOT_IP)
        misty.set_default_volume(volume)
        return True, f"🔊 Volume set to {volume}%"
    except Exception as e:
        return False, f"❌ Volume error: {str(e)}"

def get_marketing_scripts():
    """Get available marketing scripts"""
    scripts = {
        "Attracting Customers": "attract_customers",
        "Greeting & Small Talk": "greeting", 
        "Product Info & Q&A": "product_info",
        "Gamification": "gamification",
        "Social Proof": "social_proof",
        "Closing": "closing"
    }
    return scripts

def run_misty_actions(script_type, mp3_file, volume):
    """Run Misty actions based on script type"""
    try:
        misty = Robot(ROBOT_IP)
        
        # Set volume
        misty.set_default_volume(volume)
        
        # Script-specific actions (following existing patterns)
        if script_type == "attract_customers":
            st.info("🤖 Attracting customers...")
            misty.change_led(255, 0, 255)  # Purple LED
            response = misty.play_audio(fileName=mp3_file)
            time.sleep(4)  # Wait for audio
            
        elif script_type == "greeting":
            st.info("🤖 Greeting customers...")
            misty.display_image(fileName="e_Joy.jpg")
            response = misty.play_audio(fileName=mp3_file)
            time.sleep(4)
            
        elif script_type == "product_info":
            st.info("🤖 Sharing product information...")
            misty.move_arms(leftArmPosition=45, rightArmPosition=45)
            response = misty.play_audio(fileName=mp3_file)
            time.sleep(4)
            misty.move_arms(leftArmPosition=90, rightArmPosition=90)
            
        elif script_type == "gamification":
            st.info("🤖 Running gamification...")
            misty.change_led(0, 255, 0)  # Green LED
            response = misty.play_audio(fileName=mp3_file)
            time.sleep(4)
            misty.change_led(255, 255, 0)  # Yellow LED
            
        elif script_type == "social_proof":
            st.info("🤖 Sharing social proof...")
            misty.display_image(fileName="e_DefaultContent.jpg")
            response = misty.play_audio(fileName=mp3_file)
            time.sleep(4)
            
        elif script_type == "closing":
            st.info("🤖 Closing conversation...")
            response = misty.play_audio(fileName=mp3_file)
            time.sleep(4)
            misty.change_led(0, 255, 255)  # Cyan LED
            
        return response.status_code == 200, response.status_code
        
    except Exception as e:
        return False, str(e)

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
    
    st.sidebar.write(f"Robot IP: {ROBOT_IP}")
    st.sidebar.write(f"Current Volume: {volume}%")
    
    # Marketing Scripts in sidebar
    st.sidebar.divider()
    st.sidebar.header("🎭 Marketing Scripts")
    

    
    scripts = get_marketing_scripts()
    
    # Create script options with count badges
    script_options = []
    for script_name in scripts.keys():
        file_count = len(get_script_files(script_name))
        script_options.append(f"{script_name}")
    
    selected_script = st.sidebar.selectbox(
        "Select Marketing Script:", 
        script_options,
        key="marketing_script_selector"
    )
    
    # Store selected script in session state
    st.session_state.selected_script = selected_script
    
    # Display script counts with badges
    st.sidebar.write("**Audio File Counts:**")
    for script_name in scripts.keys():
        file_count = len(get_script_files(script_name))
        badge_class = styles['audio_count_badge']
        if script_name == selected_script:
            st.sidebar.markdown(f"✨ **{script_name}** <span class='{badge_class}'>{file_count}</span>", unsafe_allow_html=True)
        else:
            st.sidebar.markdown(f"• {script_name} <span class='{badge_class}'>{file_count}</span>", unsafe_allow_html=True)
    
    # Main interface
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.header("🎵 MP3 Management & Playback")
        
        # File upload section
        st.subheader("📤 Upload MP3 to Misty")
        uploaded_file = st.file_uploader("Choose MP3 file", type=['mp3'])
        
        if uploaded_file is not None:
            st.info(f"Selected file: {uploaded_file.name}")
            
            # Get current selected script from sidebar
            current_script = st.session_state.get('selected_script', 'Attracting Customers')
            
            if st.button(f"⬆️ Upload to {current_script}", type="secondary"):
                with st.spinner(f"Uploading to Misty for {current_script}..."):
                    file_content = uploaded_file.read()
                    success, message = upload_audio_to_misty(file_content, uploaded_file.name)
                    
                if success:
                    add_script_file(current_script, uploaded_file.name)  # Track for current script
                    st.success(f"✅ {uploaded_file.name} added to {current_script}!")
                    st.rerun()  # Refresh to show new file
                else:
                    st.error(message)
        
        st.divider()
        
        # Audio files on Misty
        st.subheader("🎵 Play Audio from Misty")
        
        # Get current script and its files
        current_script = st.session_state.get('selected_script', 'Attracting Customers')
        script_files = get_script_files(current_script)
        
        if not script_files:
            st.warning(f"📎 No audio files for {current_script} yet! Upload an MP3 file above.")
            return
            
        st.subheader(f"🎧 {current_script} Audio Files")
        
        # Display files as cards and let user select one
        selected_mp3 = st.selectbox(
            f"Select audio for {current_script}:",
            script_files,
            key=f"audio_select_{current_script}"
        )
        
        # Display file cards with status and delete option
        for i, filename in enumerate(script_files):
            with st.container():
                col_file, col_delete = st.columns([4, 1])
                
                with col_file:
                    # Check if file is on Misty
                    misty_files = get_misty_audio_files()
                    status_icon = "✅" if filename in misty_files else "❌"
                    
                    # Highlight selected file
                    if filename == selected_mp3:
                        st.success(f"{status_icon} **▶️ {filename}** (Selected)")
                    else:
                        st.write(f"{status_icon} **{filename}**")
                    
                    if filename in misty_files:
                        st.caption("🚀 Ready on Misty")
                    else:
                        st.caption("⚠️ Re-upload needed")
                
                with col_delete:
                    if st.button("🗑️", key=f"delete_{current_script}_{i}", help="Delete file"):
                        remove_script_file(current_script, filename)
                        st.rerun()
            
        # Audio control buttons: Play/Pause toggle and Stop
        col_play_pause, col_stop = st.columns(2)
        
        # Track playing state
        if 'is_playing' not in st.session_state:
            st.session_state.is_playing = False
        
        with col_play_pause:
            # Toggle button for play/pause
            if st.session_state.is_playing:
                button_text = "⏸️ Pause"
                button_type = "secondary"
            else:
                button_text = "▶️ Play"
                button_type = "primary"
            
            if st.button(button_text, type=button_type, key="play_pause_toggle"):
                if selected_mp3:
                    if st.session_state.is_playing:
                        # Currently playing, so pause
                        success, message = pause_audio_on_misty()
                        if success:
                            st.session_state.is_playing = False
                            st.success(message)
                        else:
                            st.error(message)
                    else:
                        # Currently paused/stopped, so play/resume
                        success, message = resume_audio_on_misty()
                        if not success:
                            # If resume failed, start playing from beginning
                            with st.spinner("Playing audio on Misty..."):
                                success, message = play_mp3_on_misty(selected_mp3, volume)
                        
                        if success:
                            st.session_state.is_playing = True
                            st.success(message)
                        else:
                            st.error(message)
                else:
                    st.warning("Please select an audio file first!")
        
        with col_stop:
            if st.button("⏹️ Stop", type="secondary"):
                success, message = stop_audio_on_misty()
                if success:
                    st.session_state.is_playing = False  # Reset playing state
                    st.success(message)
                else:
                    st.error(message)
    
    with col2:
        st.header("🤖 Misty WOZ Controller")
        
        if selected_script:
            st.success(f"🎯 Active Script: **{selected_script}**")
            
            # Show script details
            script_data = scripts[selected_script]
            st.write(f"📝 **Description:** {script_data}")
            
            st.info("🚀 Use the Play/Stop controls on the left to run this marketing script with your selected audio!")
        else:
            st.info("📎 Select a marketing script from the sidebar to get started")
    
    # Status section
    st.header("📊 Status")
    
    # Quick actions
    col3, col4, col5 = st.columns(3)
    
    with col3:
        if st.button("🔴 Red LED"):
            try:
                misty = Robot(ROBOT_IP)
                misty.change_led(255, 0, 0)
                st.success("LED changed to red!")
            except:
                st.error("Failed to change LED")
    
    with col4:
        if st.button("🟢 Green LED"):
            try:
                misty = Robot(ROBOT_IP)
                misty.change_led(0, 255, 0)
                st.success("LED changed to green!")
            except:
                st.error("Failed to change LED")
    
    with col5:
        if st.button("🔵 Blue LED"):
            try:
                misty = Robot(ROBOT_IP)
                misty.change_led(0, 0, 255)
                st.success("LED changed to blue!")
            except:
                st.error("Failed to change LED")
    
    # Instructions
    st.header("📋 Instructions")
    
    st.write("""
    **How to use this GUI:**
    1. **Upload**: Use the file uploader to upload MP3 files directly to Misty
    2. **Play**: Select any audio file and play it on Misty
    3. **WOZ Scripts**: Run complete marketing scenarios with audio + actions
    4. **Quick Controls**: Use LED buttons for immediate visual feedback
    
    **WOZ Marketing Scripts:**
    - **Attracting Customers**: Purple LED + audio
    - **Greeting**: Happy face + audio  
    - **Product Info**: Arm movements + audio
    - **Gamification**: LED color changes + audio
    - **Social Proof**: Default face + audio
    - **Closing**: Cyan LED + audio
    
    **Files Status:**
    - ✅ Green = File is on Misty robot (ready to play)
    - ⚠️ Yellow = File is only local (needs upload)
    """)

if __name__ == "__main__":
    main()