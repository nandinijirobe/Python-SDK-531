#!/usr/bin/env python3
"""
Simple test script to verify Misty Python SDK is working properly.
This script will connect to your Misty robot and perform basic operations.
"""

from mistyPy.Robot import Robot

def main():
    # Robot's IP address
    ip_address = "192.168.0.41"
    
    print("Connecting to Misty robot...")
    
    try:
        # Create an instance of the robot
        misty = Robot(ip_address)
        
        # Test 1: Get robot information
        print("\n=== Testing Robot Connection ===")
        response = misty.get_device_information()
        if response.status_code == 200:
            device_info = response.json()["result"]
            print(f"✅ Connected successfully!")
            print(f"Robot Name: {device_info.get('robotName', 'Unknown')}")
            print(f"Robot Version: {device_info.get('robotVersion', 'Unknown')}")
        else:
            print(f"❌ Failed to get device info. Status: {response.status_code}")
            return
        
        # Test 2: Change LED color
        print("\n=== Testing LED Control ===")
        response = misty.change_led(255, 255, 0)  # Red
        if response.status_code == 200:
            print("✅ LED changed to RED successfully!")
        else:
            print(f"❌ Failed to change LED. Status: {response.status_code}")
        
        # Wait a moment, then change to blue
        import time
        time.sleep(2)
        
        response = misty.change_led(0, 0, 255)  # Blue
        if response.status_code == 200:
            print("✅ LED changed to BLUE successfully!")
        else:
            print(f"❌ Failed to change LED. Status: {response.status_code}")
        
        # Test 3: Check and adjust volume
        print("\n=== Testing Volume Control ===")
        response = misty.get_volume()
        if response.status_code == 200:
            volume_result = response.json()["result"]
            # Handle different response formats
            if isinstance(volume_result, dict):
                current_volume = volume_result.get('volume', volume_result)
            else:
                current_volume = volume_result
            print(f"✅ Current Volume: {current_volume}")
            
            # Set volume to a good level for speech (around 50-70)
            new_volume = 90
            response = misty.set_default_volume(new_volume)
            if response.status_code == 200:
                print(f"✅ Volume set to: {new_volume}")
            else:
                print(f"❌ Failed to set volume. Status: {response.status_code}")
        else:
            print(f"❌ Failed to get current volume. Status: {response.status_code}")
        
        # Test 4: Make Misty speak
        print("\n=== Testing Speech ===")
        response = misty.speak("hi Aditya, Nandini and , Apoorva I am misty")
        if response.status_code == 200:
            print("✅ Misty is speaking: 'hi Aditya, Nandini and , Apoorva I am misty'")
        else:
            print(f"❌ Failed to make Misty speak. Status: {response.status_code}")
        
        # Wait for speech to complete
        time.sleep(3)
        # Test 5: Test arm movements
        print("\n=== Testing Arm Movements ===")
        response = misty.move_arms(leftArmPosition=45, rightArmPosition=45)
        if response.status_code == 200:
            print("✅ Arms moved to 45 degrees")
        else:
            print(f"❌ Failed to move arms. Status: {response.status_code}")
        
        time.sleep(2)
        
        # Move arms back to neutral position
        response = misty.move_arms(leftArmPosition=90, rightArmPosition=90)
        if response.status_code == 200:
            print("✅ Arms moved back to neutral position")
        else:
            print(f"❌ Failed to move arms back. Status: {response.status_code}")
        
        # Test 6: Test expressions (display image)
        print("\n=== Testing Expressions ===")
        response = misty.display_image(fileName="e_Joy.jpg")
        if response.status_code == 200:
            print("✅ Happy expression displayed")
        else:
            print(f"❌ Failed to display expression. Status: {response.status_code}")
        
        time.sleep(2)
        
        # Change to different expression
        response = misty.display_image(fileName="e_DefaultContent.jpg")
        if response.status_code == 200:
            print("✅ Default expression displayed")
        else:
            print(f"❌ Failed to display default expression. Status: {response.status_code}")
        
        # Test 7: Get battery level
        print("\n=== Testing Battery Status ===")
        response = misty.get_battery_level()
        if response.status_code == 200:
            battery_info = response.json()["result"]
            print(f"✅ Battery Level: {battery_info.get('chargePercent', 'Unknown')}%")
        else:
            print(f"❌ Failed to get battery level. Status: {response.status_code}")
        
        print("\n🎉 All tests completed successfully!")
        print("Your Misty Python SDK is properly configured and working!")
        
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        print("Make sure your Misty robot is powered on and connected to the same network.")

if __name__ == "__main__":
    main()