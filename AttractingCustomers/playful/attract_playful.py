"""
Attracting Customers - Playful approach
Combines audio and expression for playful customer attraction
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

def execute_attract_playful():
    """Execute playful customer attraction sequence using same pattern as direct"""
    ip_address = "192.168.0.73"
    misty = Robot(ip_address)
    
    print("=== ATTRACTING CUSTOMERS - PLAYFUL APPROACH ===")
    
    # Stop any existing audio first
    misty.stop_audio()
    
    # Use your custom playful audio file exactly like the working direct approach
    import os
    audio_file = os.path.join(os.path.dirname(__file__), "Playful.mp3")
    
    if os.path.exists(audio_file):
        print(f"Found audio file: {audio_file}")
        
        # Upload using the proven method (False, True parameters)
        misty.save_audio("attract_playful.mp3", convert_to_byte(audio_file), False, True)
        
        # "First time meeting a robot, huh?" - contempt expression with upward gaze and right tilt
        misty.display_image(fileName="e_Contempt.jpg")
        misty.change_led(255, 255, 0)  # Yellow light
        misty.move_head(pitch=-12, roll=15, yaw=15)  # Upward gaze, head tilt right, slightly left
        
        # Play audio with proven approach
        feedback1 = misty.play_audio(fileName="attract_playful.mp3", volume=80)
        time.sleep(2)  # Time for "First time meeting a robot, huh?"
        
        # "I promise I won't bite!" - admiration expression, maintain upward and left gaze
        misty.display_image(fileName="e_Admiration.jpg")
        misty.move_head(pitch=-12, roll=0, yaw=15)  # Maintain upward angle and left gaze
        time.sleep(3)  # Time for middle phrase + extra time for nice admiration face
        
        # "Wanna come check out our booth?" - joy expression with upward and left gaze
        misty.display_image(fileName="e_Joy.jpg")
        misty.move_head(pitch=-12, roll=-10, yaw=15)  # Upward angle with slight left tilt and left gaze
        time.sleep(2)  # Time for final phrase
        
        return True, "✨ Playful attract with same timing completed"
    else:
        return False, f"❌ Playful.mp3 file not found in {os.path.dirname(__file__)}"

if __name__ == "__main__":
    execute_attract_playful()