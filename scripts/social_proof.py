# Social Proof [human]
from mistyPy.Robot import Robot

def run_script():
    import time
    misty = Robot("192.168.0.41")
    
    # Set volume for speech
    misty.set_default_volume(90)
    
    print("🤖 Misty: Did you know that over 10,000 customers love our product?")
    response = misty.speak("Did you know that over 10,000 customers love our product?")
    if response.status_code == 200:
        print("✅ Speech command sent successfully")
    time.sleep(4)  # Wait for speech to complete
    
    misty.display_image(fileName="e_DefaultContent.jpg")
    
    print("🤖 Misty: Just yesterday, someone said it was the best purchase they ever made!")
    response = misty.speak("Just yesterday, someone said it was the best purchase they ever made!")
    if response.status_code == 200:
        print("✅ Speech command sent successfully")
    time.sleep(5)  # Wait for speech to complete
    
    print("🤖 Misty: You'll be joining a community of very satisfied customers!")
    response = misty.speak("You'll be joining a community of very satisfied customers!")
    if response.status_code == 200:
        print("✅ Speech command sent successfully")
    time.sleep(4)  # Wait for speech to complete

if __name__ == "__main__":
    run_script()