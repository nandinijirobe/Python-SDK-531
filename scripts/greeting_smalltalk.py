# Greeting + small talk [human]
from mistyPy.Robot import Robot

def run_script():
    import time
    misty = Robot("192.168.0.41")
    
    # Set volume for speech
    misty.set_default_volume(90)
    
    print("🤖 Misty: Hi! Nice to meet you! How are you doing today?")
    response = misty.speak("Hi! Nice to meet you! How are you doing today?")
    if response.status_code == 200:
        print("✅ Speech command sent successfully")
    time.sleep(4)  # Wait for speech to complete
    
    misty.display_image(fileName="e_Joy.jpg")
    
    print("🤖 Misty: What brings you to our booth?")
    response = misty.speak("What brings you to our booth?")
    if response.status_code == 200:
        print("✅ Speech command sent successfully")
    time.sleep(3)  # Wait for speech to complete

if __name__ == "__main__":
    run_script()