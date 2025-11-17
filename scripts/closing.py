# Closing [human + misty]
from mistyPy.Robot import Robot
import time

def run_script():
    misty = Robot("192.168.0.41")
    import time
    
    # Set volume for speech
    misty.set_default_volume(90)
    
    print("🤖 Misty: So, are you ready to take the next step?")
    response = misty.speak("So, are you ready to take the next step?")
    if response.status_code == 200:
        print("✅ Speech command sent successfully")
    time.sleep(4)  # Wait for speech to complete
    
    misty.move_arms(leftArmPosition=90, rightArmPosition=90)  # Neutral position
    
    print("🤖 Misty: Thank you so much for visiting our booth today!")
    response = misty.speak("Thank you so much for visiting our booth today!")
    if response.status_code == 200:
        print("✅ Speech command sent successfully")
    time.sleep(4)  # Wait for speech to complete
    
    misty.change_led(0, 255, 255)  # Cyan LED for farewell
    
    print("🤖 Misty: I hope to see you again soon!")
    response = misty.speak("I hope to see you again soon!")
    if response.status_code == 200:
        print("✅ Speech command sent successfully")
    time.sleep(3)  # Wait for speech to complete

if __name__ == "__main__":
    run_script()