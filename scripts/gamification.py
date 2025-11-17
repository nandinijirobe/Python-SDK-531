# Gamification [human + misty]
from mistyPy.Robot import Robot
import time

def run_script():
    misty = Robot("192.168.0.41")
    import time
    
    # Set volume for speech
    misty.set_default_volume(90)
    
    print("🤖 Misty: Let's play a fun game together!")
    response = misty.speak("Let's play a fun game together!")
    if response.status_code == 200:
        print("✅ Speech command sent successfully")
    time.sleep(3)  # Wait for speech to complete
    
    misty.change_led(0, 255, 0)  # Green LED for game mode
    
    print("🤖 Misty: Can you guess what color my LED will turn next?")
    response = misty.speak("Can you guess what color my LED will turn next?")
    if response.status_code == 200:
        print("✅ Speech command sent successfully")
    time.sleep(4)  # Wait for speech to complete
    
    time.sleep(2)  # Pause for guessing
    misty.change_led(255, 255, 0)  # Yellow
    
    print("🤖 Misty: Great job playing with me!")
    response = misty.speak("Great job playing with me!")
    if response.status_code == 200:
        print("✅ Speech command sent successfully")
    time.sleep(3)  # Wait for speech to complete

if __name__ == "__main__":
    run_script()