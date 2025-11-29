"""
Attracting Customers - Joke approach
Combines audio and expression for humorous customer attraction
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

def execute_attract_joke():
    """Execute joke-based customer attraction sequence with continuous waving"""
    ip_address = "192.168.0.73"
    misty = Robot(ip_address)
    
    print("=== ATTRACTING CUSTOMERS - JOKE APPROACH ===")
    
    # Stop any existing audio first
    misty.stop_audio()
    
    # Use your custom joke audio file exactly like the working approach
    import os
    audio_file = os.path.join(os.path.dirname(__file__), "Joke.mp3")
    
    if os.path.exists(audio_file):
        print(f"Found audio file: {audio_file}")
        
        # Upload using the proven method (False, True parameters)
        misty.save_audio("attract_joke.mp3", convert_to_byte(audio_file), False, True)
        
        # Initial setup - default expression with upward gaze
        misty.move_head(pitch=-12, roll=-5, yaw=15)  # Look up, slight tilt, a little left
        misty.display_image(fileName="e_DefaultContent.jpg")
        misty.change_led(255, 255, 0)  # Yellow light
        
        # Play audio with proven approach
        feedback1 = misty.play_audio(fileName="attract_joke.mp3", volume=80)
        
        # Continuous waving for 3 seconds - half-high arms up and down continuously
        print("Starting continuous wave...")
        wave_duration = 3.0
        wave_speed = 0.3  # Time between waves
        wave_count = int(wave_duration / wave_speed)
        
        for i in range(wave_count):
            if i % 2 == 0:
                misty.move_arms(90, 0, 30)  # Right arm highest (0), left arm down (90)
            else:
                misty.move_arms(90, 60, 30)  # Right arm mid-way (60), left arm down (90)
            time.sleep(wave_speed)
        
        # Give time for waving to end properly
        time.sleep(0.5)
        
        # "I am not programmed to wave constantly!" - arms down, EcstacyHilarious expression
        misty.move_arms(90, 90, 50)  # Both arms down
        misty.display_image(fileName="e_EcstacyHilarious.jpg")
        time.sleep(2)  # Time for middle phrase
        
        # "But I am programmed to invite you over! Come over to learn more" - both arms up high
        misty.move_arms(30, 30, 50)  # Both arms up high
        time.sleep(3)  # Time for final phrase
        
        # After audio ends, show joy expression for 3 seconds
        misty.display_image(fileName="e_Joy.jpg")
        time.sleep(3)  # Joy expression for 3 seconds
        
        # Arms down but keep head position
        misty.move_arms(90, 90, 50)  # Arms down
        
        return True, "✨ Joke attract with continuous waving completed"
    else:
        return False, f"❌ Joke.mp3 file not found in {os.path.dirname(__file__)}"

if __name__ == "__main__":
    execute_attract_joke()