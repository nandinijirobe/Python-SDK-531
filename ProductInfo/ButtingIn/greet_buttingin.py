"""
Greetings & Small Talk - Butting In
Handles interruption situations during conversation
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

def execute_greet_buttingin():
    """Execute butting in sequence with two-part audio"""
    ip_address = "192.168.0.73"
    misty = Robot(ip_address)
    
    print("=== GREETINGS - BUTTING IN ===")
    
    # Stop any existing audio first
    misty.stop_audio()
    
    # Check for both audio files
    import os
    audio_file_80members = os.path.join(os.path.dirname(__file__), "80 members.mp3")
    audio_file_continues = os.path.join(os.path.dirname(__file__), "alsomistycontinues.mp3")
    
    if os.path.exists(audio_file_80members) and os.path.exists(audio_file_continues):
        print(f"Found both audio files: 80 members.mp3 and alsomistycontinues.mp3")
        
        # Upload both audio files using the proven method (False, True parameters)
        misty.save_audio("buttin_80members.mp3", convert_to_byte(audio_file_80members), False, True)
        misty.save_audio("buttin_continues.mp3", convert_to_byte(audio_file_continues), False, True)
        time.sleep(1)  # Wait for uploads
        
        # Part 1: "80 members!" - turns and looks at collaborator + raises arms + joy eyes
        misty.display_image(fileName="e_Joy.jpg")
        misty.change_led(255, 255, 0)  # Yellow light
        misty.move_head(pitch=-12, roll=0, yaw=45)  # Turn to look at collaborator with raised head
        misty.move_arms(30, 30, 50)  # Raise both arms
        
        # Play first part
        feedback1 = misty.play_audio(fileName="buttin_80members.mp3", volume=80)
        time.sleep(2)  # Time for "80 members!"
        
        # Pause for human interruption: "Yeah, take it away from here, Misty!"
        print("Pausing for human interruption...")
        time.sleep(2)  # Wait for human to speak
        
        # Part 2: Turn to human customer, hands down, joy face
        misty.move_head(pitch=-12, roll=0, yaw=15)  # Turn back to face client with raised head and left gaze
        misty.move_arms(90, 90, 50)  # Hands down
        misty.display_image(fileName="e_Joy.jpg")  # Joy face
        
        # Continue with longer explanation
        feedback2 = misty.play_audio(fileName="buttin_continues.mp3", volume=80)
        time.sleep(3)  # Time for "Sure! Each month, we run fun challenges..."
        
        # Expression changes during the longer speech
        misty.display_image(fileName="e_Joy2.jpg")  # Joy2 eyes for "You also get access"
        time.sleep(4)  # More time for Discord explanation
        
        misty.display_image(fileName="e_Joy.jpg")  # Back to Joy for "Our Running Club"
        time.sleep(2)
        
        # Final: "is for everyone" - admiration eyes, both arms up
        misty.display_image(fileName="e_Admiration.jpg")  # Admiration eyes
        misty.move_arms(30, 30, 50)  # Both arms up
        time.sleep(3)  # Time for final phrase
        
        # Keep raised and left position - no head reset
        misty.move_arms(90, 90, 50)  # Arms down
        
        # Final gesture for remaining audio - arms up once and down
        misty.move_arms(30, 30, 50)  # Both arms up
        time.sleep(2)  # Hold arms up
        misty.move_arms(90, 90, 50)  # Arms back down
        
        # Separate gesture - pause then raise hands and down again
        time.sleep(2)  # 2 second pause
        misty.move_arms(90, 30, 50)  # Raise hands up
        time.sleep(2)  # Brief hold
        misty.move_arms(90, 90, 50)  # Arms back down
        
        misty.change_led(0, 255, 255)  # Back to cyan
        
        return True, "✨ Butting in sequence completed"
    else:
        return False, f"❌ Audio files not found. Need both '80 members.mp3' and 'alsomistycontinues.mp3'"

if __name__ == "__main__":
    execute_greet_buttingin()