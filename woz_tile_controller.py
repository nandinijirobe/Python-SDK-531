#!/usr/bin/env python3
"""
Simplified Tile-based WOZ Controller
Based on teammates' audio + expression integration approach
"""

import streamlit as st
import os
import importlib.util
import sys
from pathlib import Path
from mistyPy.Robot import Robot
import time
import base64
import random

# Import styles
from styles.style_manager import apply_styles

# Configuration
ROBOT_IP = "192.168.0.73"
ROOT_DIR = Path(__file__).parent

def convert_to_byte(filename):
    """Convert audio file to base64 for Misty"""
    with open(filename, "rb") as f:
        encoded_bytes = base64.b64encode(f.read())
    return encoded_bytes.decode("utf-8")

def get_available_categories():
    """Get all category folders from root directory"""
    categories = []
    for item in ROOT_DIR.iterdir():
        if item.is_dir() and item.name not in ['mistyPy', 'Examples', 'styles', 'woz_modules', '.git', '.conda', 'scripts']:
            # Check if it has subdirectories with Python files
            if any(subdir.is_dir() and any(subdir.glob('*.py')) for subdir in item.iterdir() if subdir.is_dir()):
                categories.append(item.name)
    return categories

def get_category_actions(category):
    """Get all action subdirectories in a category"""
    category_path = ROOT_DIR / category
    actions = []
    if category_path.exists():
        for item in category_path.iterdir():
            if item.is_dir() and any(item.glob('*.py')):
                actions.append(item.name)
    return actions

def execute_combined_action(category, action):
    """Execute the Python file that combines audio + expression"""
    try:
        action_path = ROOT_DIR / category / action
        py_files = list(action_path.glob('*.py'))
        
        if not py_files:
            return False, "No Python file found"
        
        # Use the first Python file found and actually execute it
        py_file = py_files[0]
        
        # Import and execute the specific behavior module
        import importlib.util
        spec = importlib.util.spec_from_file_location("behavior_module", py_file)
        behavior_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(behavior_module)
        
        # Execute the main function based on naming convention
        if hasattr(behavior_module, 'execute_closing_direct'):
            success, message = behavior_module.execute_closing_direct()
        # Try various attract function patterns
        elif hasattr(behavior_module, 'execute_attract_direct'):
            success, message = behavior_module.execute_attract_direct()
        elif hasattr(behavior_module, 'execute_attract_playful'):
            success, message = behavior_module.execute_attract_playful()
        elif hasattr(behavior_module, 'execute_attract_joke'):
            success, message = behavior_module.execute_attract_joke()
        else:
            # Fallback: try to find any execute_ function
            execute_functions = [attr for attr in dir(behavior_module) if attr.startswith('execute_')]
            if execute_functions:
                func = getattr(behavior_module, execute_functions[0])
                success, message = func()
            else:
                return False, "No execute function found in Python file"
        
        if success:
            return True, f"✨ {category} → {action}: {message}"
        else:
            return False, f"❌ {category} → {action}: {message}"
            
    except Exception as e:
        return False, f"Error executing {category} → {action}: {str(e)}"

def reset_misty_body():
    """Reset Misty to neutral position and default expression only"""
    try:
        misty = Robot(ROBOT_IP)
        
        # Stop any movement and audio
        misty.stop()
        misty.stop_audio()
        time.sleep(0.5)
        
        # Default expression ONLY
        misty.display_image(fileName="e_DefaultContent.jpg")
        
        # White LED
        misty.change_led(255, 255, 255)
        
        # Head straight, arms neutral
        misty.move_head(pitch=0, roll=0, yaw=0)
        misty.move_arms(90, 90, 50)
        
        return True, "🔄 Reset complete - default expression only"
    except Exception as e:
        return False, f"Reset error: {str(e)}"

def misty_listen():
    """Make Misty back up in an arc and look up attentively with timed expression exchange"""
    try:
        misty = Robot(ROBOT_IP)
        
        # Set cyan LED for listening
        misty.change_led(0, 255, 255)
        
        # Start with Joy expression
        misty.display_image(fileName="e_Joy.jpg")
        
        # Look up gently - single movement
        misty.move_head(pitch=-12, roll=0, yaw=45)  # One smooth movement - more to the left
        
        # Timed expression exchange for exactly 10 seconds
        start_time = time.time()
        while time.time() - start_time < 10.0:
            # Show Joy for 2.5 seconds
            misty.display_image(fileName="e_Joy.jpg")
            time.sleep(2.5)
            
            # Check if 10 seconds is up
            if time.time() - start_time >= 10.0:
                break
                
            # Show ContentLeft for 2.5 seconds
            misty.display_image(fileName="e_ContentLeft.jpg")
            time.sleep(2.5)
        
        # End on default expression after 10 seconds
        misty.display_image(fileName="e_DefaultContent.jpg")
        
        return True, "👂😊 Misty listened for 10 seconds with expression exchange!"
    except Exception as e:
        return False, f"❌ Listen error: {str(e)}"

def move_forward():
    """Move Misty forward to return to original position"""
    try:
        misty = Robot(ROBOT_IP)
        
        # Move forward with same gentler values as listen button but reversed
        misty.drive(linearVelocity=15, angularVelocity=-8)  # Match Listen speeds
        time.sleep(0.6)  # Match Listen duration
        misty.stop()
        time.sleep(0.5)  # Wait for robot to settle
        
        return True, "🔄 Moved forward to original position"
    except Exception as e:
        return False, f"❌ Move forward error: {str(e)}"

def stop_audio():
    """Stop any currently playing audio"""
    try:
        misty = Robot(ROBOT_IP)
        misty.stop_audio()
        return True, "⏹️ Audio stopped"
    except Exception as e:
        return False, f"❌ Stop error: {str(e)}"

def set_misty_volume(volume):
    """Set Misty's volume level"""
    try:
        misty = Robot(ROBOT_IP)
        misty.set_default_volume(volume)
        return True, f"🔊 Volume set to {volume}"
    except Exception as e:
        return False, f"❌ Volume error: {str(e)}"

def execute_rejection_behavior():
    """Execute the rejection behavior from Rejection folder"""
    try:
        import importlib.util
        import sys
        
        # Load the rejection module
        rejection_path = os.path.join(os.getcwd(), "Rejection", "rejection.py")
        spec = importlib.util.spec_from_file_location("rejection", rejection_path)
        rejection_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(rejection_module)
        
        # Execute the rejection behavior
        success, message = rejection_module.execute_rejection()
        return success, message
        
    except Exception as e:
        return False, f"Error executing rejection: {str(e)}"

def main():
    st.set_page_config(page_title="Misty WOZ - Tile Controller", layout="wide")
    
    # Apply CSS styles from styles directory
    apply_styles()
    
    # Header
    st.title("🤖 Misty WOZ - Tile Controller")
    st.markdown("*Integrated Audio + Expression Control*")
    
    # Sidebar controls
    st.sidebar.header("🎛️ Controls")
    
    # Control buttons in columns
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("🔄 Reset", help="Reset to neutral position"):
            success, message = reset_misty_body()
            if success:
                st.sidebar.success(message)
            else:
                st.sidebar.error(message)
    
    with col2:
        if st.button("👂 Listen", help="Back up and listen attentively"):
            success, message = misty_listen()
            if success:
                st.sidebar.success(message)
            else:
                st.sidebar.error(message)
    
    # Movement buttons
    col3, col4 = st.sidebar.columns(2)
    
    with col3:
        if st.button("⬆️ Forward", help="Move forward to original position"):
            success, message = move_forward()
            if success:
                st.sidebar.success(message)
            else:
                st.sidebar.error(message)
    
    with col4:
        if st.button("⏹️ Stop Audio", help="Stop any playing audio"):
            success, message = stop_audio()
            if success:
                st.sidebar.success(message)
            else:
                st.sidebar.error(message)
    
    # Rejection button (full width)
    if st.sidebar.button("😢 Rejection", help="Execute sad rejection behavior"):
        success, message = execute_rejection_behavior()
        if success:
            st.sidebar.success(message)
        else:
            st.sidebar.error(message)
    
    # Volume Controls
    st.sidebar.markdown("---")
    st.sidebar.header("🔊 Volume Control")
    
    # Volume slider
    volume_level = st.sidebar.slider("Volume Level", min_value=0, max_value=100, value=80, step=5)
    
    # Volume buttons
    vol_col1, vol_col2, vol_col3 = st.sidebar.columns(3)
    
    with vol_col1:
        if st.button("🔇 Mute", help="Set volume to 0"):
            success, message = set_misty_volume(0)
            if success:
                st.sidebar.success(message)
            else:
                st.sidebar.error(message)
    
    with vol_col2:
        if st.button(f"🔊 Set {volume_level}", help=f"Set volume to {volume_level}"):
            success, message = set_misty_volume(volume_level)
            if success:
                st.sidebar.success(message)
            else:
                st.sidebar.error(message)
    
    with vol_col3:
        if st.button("🔊 Max", help="Set volume to 100"):
            success, message = set_misty_volume(100)
            if success:
                st.sidebar.success(message)
            else:
                st.sidebar.error(message)
    
    # Main content area
    categories = get_available_categories()
    
    if not categories:
        st.warning("No category folders found! Make sure you have folders like 'Closing', 'AttractingCustomers', etc.")
        return
    
    # Category selection
    selected_category = st.selectbox("📁 Select Category", categories)
    
    if selected_category:
        st.subheader(f"📂 {selected_category}")
        actions = get_category_actions(selected_category)
        
        if actions:
            # Create action tiles
            cols = st.columns(min(len(actions), 4))  # Max 4 tiles per row
            
            for i, action in enumerate(actions):
                with cols[i % 4]:
                    # Check if this is a non-functional action
                    is_non_functional = ((selected_category == "Greetings&SmallTalk" and 
                                        action.lower() in ["pauseinterruption", "buttingin"]) or
                                       (selected_category == "ProductInfo" and 
                                        action.lower() in ["smoothswitch"]))
                    
                    if is_non_functional:
                        # Create grey/disabled looking button
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
                            color: #adb5bd;
                            border: 2px solid rgba(108, 117, 125, 0.3);
                            border-radius: 12px;
                            padding: 18px 25px;
                            text-align: center;
                            margin: 8px;
                            min-height: 60px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-size: 18px;
                            font-weight: 600;
                            opacity: 0.6;
                            cursor: not-allowed;
                        ">
                            🚧 {action.title()}
                        </div>
                        """, unsafe_allow_html=True)
                        st.caption("⚠️ Not functional yet")
                    else:
                        # Create normal functional button
                        if st.button(f"▶️ {action.title()}", key=f"{selected_category}_{action}", help=f"Execute {action} with audio + expression"):
                            with st.spinner(f"Executing {action}..."):
                                success, message = execute_combined_action(selected_category, action)
                            
                            if success:
                                st.success(message)
                            else:
                                st.error(message)
        else:
            st.info(f"No actions found in {selected_category}. Add subdirectories with Python files.")
    
    # Footer
    st.markdown("---")
    st.markdown("*Tiles represent combined audio + expression sequences*")

if __name__ == "__main__":
    main()