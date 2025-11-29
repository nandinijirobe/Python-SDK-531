"""
Audio Management Module
Handles MP3 file operations and audio playback on Misty robot
"""

import requests
import base64
import time
from mistyPy.Robot import Robot

ROBOT_IP = "192.168.0.73"

def upload_mp3_to_misty(file_path, filename):
    """Upload MP3 file to Misty robot using SDK"""
    try:
        # Read the MP3 file
        with open(file_path, 'rb') as audio_file:
            audio_content = audio_file.read()
        
        # Encode to base64
        audio_base64 = base64.b64encode(audio_content).decode('utf-8')
        
        # Use Misty SDK to upload
        misty = Robot(ROBOT_IP)
        response = misty.save_audio(
            fileName=filename,
            data=audio_base64,
            immediatelyApply=False,
            overwriteExisting=True
        )
        
        if response.status_code == 200:
            return True, f"✅ Successfully uploaded: {filename}"
        else:
            # More detailed error info
            try:
                error_data = response.json()
                error_msg = error_data.get('error', f'HTTP {response.status_code}')
                return False, f"❌ Upload failed: {error_msg}"
            except:
                return False, f"❌ Upload failed. Status: {response.status_code}"
            
    except FileNotFoundError:
        return False, f"❌ File not found: {file_path}"
    except Exception as e:
        return False, f"❌ Upload error: {str(e)}"

def test_robot_connection():
    """Test if Misty robot is accessible"""
    try:
        misty = Robot(ROBOT_IP)
        response = misty.get_device_information()
        if response.status_code == 200:
            device_info = response.json().get("result", {})
            robot_name = device_info.get("robotName", "Unknown")
            return True, f"✅ Connected to {robot_name} at {ROBOT_IP}"
        else:
            return False, f"❌ Robot responded with status {response.status_code}"
    except Exception as e:
        return False, f"❌ Cannot reach robot at {ROBOT_IP}: {str(e)}"

def get_misty_audio_files():
    """Get list of audio files currently on Misty robot"""
    try:
        misty = Robot(ROBOT_IP)
        response = misty.get_audio_list()
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "Success":
                files = [item["name"] for item in data.get("result", [])]
                return files
        return []
    except:
        return []

def play_mp3_on_misty(filename, volume=90):
    """Play MP3 file on Misty robot"""
    try:
        misty = Robot(ROBOT_IP)
        
        # ==== VOLUME BOOST CONTROL ====
        # Adjust this value to match TTS loudness:
        # 1.0 = no boost (same as slider)
        # 0.8 = 20% quieter than slider
        # 1.2 = 20% louder than slider
        VOLUME_BOOST = 1.9  # ← CHANGE THIS VALUE TO TEST LOUDNESS
        # ===============================   
        
        mp3_volume = min(100, int(volume * VOLUME_BOOST))
        
        # Set volume first
        misty.set_default_volume(mp3_volume)
        
        # Play the file
        response = misty.play_audio(fileName=filename)
        
        if response.status_code == 200:
            return True, f"🎵 Playing: {filename} at volume {mp3_volume}"
        else:
            return False, f"❌ Failed to play {filename}. Status: {response.status_code}"
            
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def pause_audio_on_misty():
    """Pause audio on Misty robot (preserves playback position)"""
    try:
        misty = Robot(ROBOT_IP)
        response = misty.pause_audio()  # Use actual pause method
        
        if response.status_code == 200:
            return True, "⏸️ Audio paused"
        return False, f"❌ Failed to pause audio. Status: {response.status_code}"
            
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def resume_audio_on_misty():
    """Resume paused audio from where it was paused"""
    try:
        misty = Robot(ROBOT_IP)
        # Use direct API call since resume_audio doesn't exist in SDK
        response = misty.post_request("audio/resume")
        
        if response.status_code == 200:
            return True, "▶️ Audio resumed"
        return False, f"❌ Failed to resume audio. Status: {response.status_code}"
            
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def stop_audio_on_misty():
    """Stop audio and reset to beginning (00:00) on Misty robot"""
    try:
        misty = Robot(ROBOT_IP)
        response = misty.stop_audio()
        
        if response.status_code == 200:
            return True, "⏹️ Audio stopped (reset to 00:00)"
        else:
            return False, f"❌ Failed to stop audio. Status: {response.status_code}"
            
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def auto_stop_audio():
    """Silently stop any playing audio (for cleanup)"""
    try:
        misty = Robot(ROBOT_IP)
        misty.stop_audio()
        return True
    except:
        return False

def set_volume_on_misty(volume):
    """Set volume on Misty robot in real-time"""
    try:
        misty = Robot(ROBOT_IP)
        misty.set_default_volume(volume)
        return True, f"🔊 Volume set to {volume}%"
    except Exception as e:
        return False, f"❌ Volume error: {str(e)}"