# Product info dump with Q&A [misty + human (takes care of uncommon questions only)]
from mistyPy.Robot import Robot

def run_script():
    import time
    misty = Robot("192.168.0.41")
    
    # Set volume for speech
    misty.set_default_volume(90)
    
    print("🤖 Misty: Let me tell you about our incredible product features!")
    response = misty.speak("Let me tell you about our incredible product features!")
    if response.status_code == 200:
        print("✅ Speech command sent successfully")
    time.sleep(4)  # Wait for speech to complete
    
    misty.move_arms(leftArmPosition=45, rightArmPosition=45)
    
    print("🤖 Misty: This product will revolutionize your daily life!")
    response = misty.speak("This product will revolutionize your daily life!")
    if response.status_code == 200:
        print("✅ Speech command sent successfully")
    time.sleep(4)  # Wait for speech to complete
    
    print("🤖 Misty: Do you have any questions about what I just explained?")
    response = misty.speak("Do you have any questions about what I just explained?")
    if response.status_code == 200:
        print("✅ Speech command sent successfully")
    time.sleep(4)  # Wait for speech to complete

if __name__ == "__main__":
    run_script()