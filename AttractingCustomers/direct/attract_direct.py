"""
Attracting Customers - Direct approach
Combines audio and expression like teammates' approach
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from mistyPy.Robot import Robot
import base64
import time
import random

def convert_to_byte(filename):
    """Convert audio file to base64 for Misty"""
    with open(filename, "rb") as f:
        encoded_bytes = base64.b64encode(f.read())
    return encoded_bytes.decode("utf-8")

def execute_attract_direct():
    """Execute attract direct sequence: Hi [one arm wave, yellow light, joy eyes], 
    I noticed you looking our way. [lift both hands halfway] 
    Would you like to learn more about our booth [hands down, tilt head slightly left]"""
    ip_address = "192.168.0.73"
    misty = Robot(ip_address)
    
    print("=== STARTING ATTRACT DIRECT BEHAVIOR ===")
    
    # Stop any existing audio first
    misty.stop_audio()
    
    # Use your custom Direct.mp3 file exactly like their working approach
    import os
    audio_file = os.path.join(os.path.dirname(__file__), "Direct.mp3")
    
    if os.path.exists(audio_file):
        print(f"Found audio file: {audio_file}")
        
        # Upload using their exact method (False, True parameters)
        misty.save_audio("attract_direct.mp3", convert_to_byte(audio_file), False, True)
        
        # Initial setup - Joy expression, yellow light, and upward gaze with slight tilt
        misty.move_head(pitch=-12, roll=-5, yaw=15)  # Look up, slight tilt, a little left
        misty.display_image(fileName="e_Joy.jpg")
        misty.change_led(255, 255, 0)  # Yellow light
        
        # "Hi" - raise right hand higher, yellow light, joy eyes (already set above)
        misty.move_arms(90, 30, 50)  # Right arm higher for "Hi" (30 instead of 45)
        
        # Play audio with their exact approach
        feedback1 = misty.play_audio(fileName="attract_direct.mp3", volume=80)
        time.sleep(2)  # Time for "Hi" + pause
        
        # "I noticed you looking our way" + pause - lift both hands halfway
        misty.move_arms(60, 60, 50)  # Both arms lifted halfway
        time.sleep(3)  # Time for middle phrase + pause
        
        # "Would you like to learn more about our booth" - hands down, tilt head left with raised angle
        misty.move_arms(90, 90, 50)  # Arms down
        misty.move_head(pitch=-12, roll=-25, yaw=0)  # Head TILT left with upward angle
        time.sleep(3)  # Time for final phrase
        
        return True, "✨ Direct attract with perfect timing completed"
    else:
        return False, f"❌ Direct.mp3 file not found in {os.path.dirname(__file__)}"

if __name__ == "__main__":
    execute_attract_direct()