"""
Greetings & Small Talk - Smooth Switch
Introduces the human teammate and hands over conversation
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

def execute_greet_smoothswitch():
    """Execute smooth switch to human teammate sequence"""
    ip_address = "192.168.0.73"
    misty = Robot(ip_address)
    
    print("=== GREETINGS - SMOOTH SWITCH ===")
    
    # Stop any existing audio first
    misty.stop_audio()
    
    # Use the smoothswitch.mp3 file
    import os
    audio_file = os.path.join(os.path.dirname(__file__), "smoothswitch.mp3")
    
    if os.path.exists(audio_file):
        print(f"Found audio file: {audio_file}")
        
        # Upload using the proven method (False, True parameters)
        misty.save_audio("greet_smoothswitch.mp3", convert_to_byte(audio_file), False, True)
        
        # "Hi! Welcome" - both arms up, joy, yellow light
        misty.display_image(fileName="e_Joy.jpg")
        misty.change_led(255, 255, 0)  # Yellow light
        misty.move_arms(30, 30, 50)  # Both arms up
        
        # Play audio with proven approach
        feedback1 = misty.play_audio(fileName="greet_smoothswitch.mp3", volume=80)
        time.sleep(2)  # Time for "Hi! Welcome"
        
        # "I'm here to help my human teammate talk about our club!" - arms down
        misty.move_arms(90, 90, 50)  # Arms down
        time.sleep(3)  # Time for explanation
        
        # "Let me introduce him to you real quick" - moves back and head turns left, lift left arm up
        misty.drive_time(linearVelocity=-30, angularVelocity=0, timeMs=1000)  # Move back (like listen function)
        time.sleep(1)  # Wait for movement to complete
        misty.move_head(pitch=0, roll=0, yaw=45)  # Head turn left (yaw positive = left turn)
        misty.move_arms(60, 90, 50)  # Left arm up, right arm down (looking at collaborator)
        time.sleep(2)  # Time for "Let me introduce him" + gesture
        
        # "This is Bob" - arms down
        misty.move_arms(90, 90, 50)  # Arms down
        time.sleep(2)  # Time for "This is Bob"
        
        # After audio ends, bring head back to normal position
        misty.move_head(pitch=0, roll=0, yaw=0)  # Head back to center/normal
        
        return True, "✨ Smooth switch to human teammate completed"
    else:
        return False, f"❌ smoothswitch.mp3 file not found in {os.path.dirname(__file__)}"

if __name__ == "__main__":
    execute_greet_smoothswitch()