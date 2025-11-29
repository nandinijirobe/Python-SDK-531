"""
Robot Control Module
Handles direct robot actions and body control
"""

import time
from mistyPy.Robot import Robot

ROBOT_IP = "192.168.0.73"

def reset_misty_body():
    """Reset Misty's arms to normal position"""
    try:
        misty = Robot(ROBOT_IP)
        # Raise both arms up (90 degrees)
        response = misty.move_arms(90, 90, 100)  # left_arm, right_arm, velocity
        # Reset to default expression and LED
        misty.display_image(fileName="e_DefaultContent.jpg")  # Default expression
        misty.change_led(255, 255, 255)  # White LED for default expression
        if response.status_code == 200:
            return True, "🔄😊 Body and face reset complete"
        else:
            return False, f"❌ Body reset failed. Status: {response.status_code}"
    except Exception as e:
        return False, f"❌ Body reset error: {str(e)}"

def misty_listen():
    """Make Misty nod up and down with curious/joy expression for 5 seconds"""
    try:
        misty = Robot(ROBOT_IP)
        
        # Set curious/joyful expression and LED
        misty.display_image(fileName="e_Joy.jpg")  # Joy expression
        misty.change_led(0, 255, 255)  # Cyan LED for curiosity/joy
        
        # Nod up and down for 5 seconds
        start_time = time.time()
        while time.time() - start_time < 5:
            # Nod down
            misty.move_head(pitch=-10, roll=0, yaw=0, velocity=50)
            time.sleep(0.5)
            # Nod up
            misty.move_head(pitch=10, roll=0, yaw=0, velocity=50)
            time.sleep(0.5)
        
        # Reset head to center position
        misty.move_head(pitch=0, roll=0, yaw=0, velocity=30)
        
        return True, "👂😊 Misty is listening!"
    except Exception as e:
        return False, f"❌ Listen error: {str(e)}"

def get_marketing_scripts():
    """Get available marketing scripts"""
    scripts = {
        "Attracting Customers": "attract_customers",
        "Greeting & Small Talk": "greeting", 
        "Product Info & Q&A": "product_info",
        "Closing": "closing"
    }
    return scripts

def run_misty_actions(script_type, mp3_file, volume):
    """Run Misty actions based on script type"""
    try:
        misty = Robot(ROBOT_IP)
        
        # Set volume
        misty.set_default_volume(volume)
        
        # Script-specific actions (following existing patterns)
        if script_type == "attract_customers":
            misty.change_led(255, 0, 255)  # Purple LED
            response = misty.play_audio(fileName=mp3_file)
            time.sleep(4)
            
        elif script_type == "greeting":
            misty.display_image(fileName="e_Joy.jpg")  # Happy face
            response = misty.play_audio(fileName=mp3_file)
            time.sleep(4)
            
        elif script_type == "product_info":
            misty.move_arms(leftArmPosition=45, rightArmPosition=45)
            response = misty.play_audio(fileName=mp3_file)
            time.sleep(4)
            misty.move_arms(leftArmPosition=90, rightArmPosition=90)
            
        elif script_type == "closing":
            response = misty.play_audio(fileName=mp3_file)
            time.sleep(4)
            misty.change_led(0, 255, 255)  # Cyan LED
            
        return response.status_code == 200, response.status_code
        
    except Exception as e:
        return False, str(e)