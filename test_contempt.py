from mistyPy.Robot import Robot
import time

# Test contempt expression
misty = Robot("192.168.0.73")

print("Testing if e_Contempt.jpg exists...")
try:
    result = misty.display_image(fileName="e_Contempt.jpg")
    print("✅ e_Contempt.jpg exists!")
    print(f"Result: {result}")
    time.sleep(2)
    
    # Reset to default
    misty.display_image(fileName="e_DefaultContent.jpg")
except Exception as e:
    print(f"❌ e_Contempt.jpg not found: {e}")
    print("\nTrying alternative names...")
    
    # Try other possible contempt variations
    alternatives = ["e_contempt.jpg", "e_Disgust.jpg", "e_disgust.jpg", "e_Anger.jpg", "e_anger.jpg"]
    
    for alt in alternatives:
        try:
            print(f"Trying {alt}...")
            result = misty.display_image(fileName=alt)
            print(f"✅ {alt} exists!")
            time.sleep(1)
            break
        except:
            print(f"❌ {alt} not found")
    
    # Reset to default
    misty.display_image(fileName="e_DefaultContent.jpg")