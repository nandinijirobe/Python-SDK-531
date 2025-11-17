# Attracting customers to the booth [Misty]
from mistyPy.Robot import Robot

def run_script():
    import time
    misty = Robot("192.168.0.41")
    
    # Set volume for speech
    misty.set_default_volume(90)
    
    print("🤖 Misty: Hello there! Come check out our amazing product!")
    response = misty.speak("Hello there! Come check out our amazing product!")
    if response.status_code == 200:
        print("✅ Speech command sent successfully")
    time.sleep(3)  # Wait for speech to complete
    
    misty.change_led(255, 0, 255)  # Purple LED to attract attention
    
    print("🤖 Misty: I'm so excited to show you what we have!")
    response = misty.speak("I'm so excited to show you what we have!")
    if response.status_code == 200:
        print("✅ Speech command sent successfully")
    time.sleep(3)  # Wait for speech to complete

if __name__ == "__main__":
    run_script()