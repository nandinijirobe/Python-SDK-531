"""
Rejection behavior
Sad rejection sequence with head tilt down and arm gesture
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mistyPy.Robot import Robot
import base64
import time
import random

def convert_to_byte(filename):
    """Convert audio file to base64 for Misty"""
    with open(filename, "rb") as f:
        encoded_bytes = base64.b64encode(f.read())
    return encoded_bytes.decode("utf-8")

def execute_rejection():
    """Execute rejection sequence: Aww...okay [arms down, head tilt down indicating sad], 
    head comes back up to normal, come back later if you are still curious 
    [Sadness, Blue Light, one arm halfway up and then back down once]"""
    ip_address = "192.168.0.41"
    misty = Robot(ip_address)
    
    print("=== EXECUTING REJECTION BEHAVIOR ===")
    
    # Stop any existing audio first
    misty.stop_audio()
    
    # Use the Rejection.mp3 file
    import os
    audio_file = os.path.join(os.path.dirname(__file__), "Rejection.mp3")
    
    if os.path.exists(audio_file):
        print(f"Found audio file: {audio_file}")
        
        # Upload using the proven method (False, True parameters)
        misty.save_audio("rejection.mp3", convert_to_byte(audio_file), False, True)
        
        # "Aww...okay" - arms down, head tilt down indicating sad, Sadness expression, Blue Light
        misty.display_image(fileName="e_Sadness.jpg")
        misty.change_led(0, 0, 255)  # Blue light
        misty.move_arms(90, 90, 50)  # Arms down
        misty.move_head(pitch=20, roll=0, yaw=0)  # Head tilt down indicating sad
        
        # Play audio with proven approach
        feedback1 = misty.play_audio(fileName="rejection.mp3", volume=80)
        time.sleep(1)  # Time for "Aww" only
        
        # Head comes back up to normal position (during "okay" part)
        misty.move_head(pitch=0, roll=0, yaw=0)  # Head back to normal
        time.sleep(1)  # Time for "okay" and transition
        
        # "come back later if you are still curious" - one arm up higher and then back down once
        misty.move_arms(90, 30, 50)  # Right arm higher up (45 instead of 60)
        time.sleep(1.5)  # Hold arm up briefly
        misty.move_arms(90, 90, 50)  # Right arm back down
        time.sleep(2)  # Time for final phrase
        
        # Return to neutral
        misty.move_head(pitch=0, roll=0, yaw=0)
        misty.change_led(0, 255, 255)  # Back to cyan
        
        return True, "✨ Rejection sequence completed"
    else:
        return False, f"❌ Rejection.mp3 file not found in {os.path.dirname(__file__)}"

if __name__ == "__main__":
    execute_rejection()