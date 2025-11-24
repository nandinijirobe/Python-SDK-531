from mistyPy.GenerateRobot import RobotGenerator
from mistyPy.Robot import Robot
import json
import time


def mt5_quiz_session():

        misty_voice = "en-us-x-sfg-local"
        # how user will come to booth, user permission
        
        # load quiz data from JSON file
        quiz_data = {}
        with open('mt5_quiz.json') as f:
                quiz_data = json.load(f)

        # start quiz session
        print("Starting MT5 Quiz Session...")
        question_no = 0

        # ask if participants wants to start the quiz
        misty.speak(quiz_data["questions"][question_no], voice = misty_voice )
        user_input = int(input()) # 1 if yes, 0 if no
        if user_input == 1:
                misty.speak(quiz_data["correct_feedback"][question_no], voice = misty_voice )
                misty.speak(quiz_data["transitions"][question_no], voice = misty_voice )
                question_no += 1
        else:
                misty.speak(quiz_data["incorrect_feedback"][question_no], voice = misty_voice )
                print("Quiz session ended because participant refused to play.")
                return
        
        # begin quiz
        # TODO: add to while loop condition a way to exit the quiz early, and also a way to end the quiz after all questions have been asked
        # TODO: Make voice sound more natural and also add behaviors to make it more human like 

        print("Starting to ask participant questions...")
        while user_input != "-1":
                misty.speak(quiz_data["questions"][question_no], voice = misty_voice )
                user_input = int(input())
                if user_input == 1:
                        misty.speak(quiz_data["correct_feedback"][question_no], voice = misty_voice )
                        misty.speak(quiz_data["transitions"][question_no], voice = misty_voice )
                        question_no += 1
                else:
                        misty.speak(quiz_data["incorrect_feedback"][question_no], voice = misty_voice )
                        misty.speak(quiz_data["transitions"][question_no], voice = misty_voice )


def convert_to_byte(filename):
        import base64
        with open(filename, "rb") as f:
                encoded_bytes = base64.b64encode(f.read())

        base64_string = encoded_bytes.decode("utf-8")
        return base64_string


def audio_finished(message):
    misty.play_audio("crit3_pauseint_p2.mp3", 80)


if __name__ == "__main__":
        ip_address = "192.168.0.41"

        # Create an instance of a robot
        misty = Robot(ip_address)

        misty.save_audio("crit3_pauseint_p1.mp3", convert_to_byte("crit3_pauseint_p1.mp3"), False, True)
        misty.save_audio("crit3_pauseint_p2.mp3", convert_to_byte("crit3_pauseint_p2.mp3"), False, True)
        
        misty.move_head(pitch= 0, roll= 36, yaw= 0)
        misty.move_head(pitch= -21, roll= 36, yaw= 0)
        
        feedback1 = misty.play_audio(fileName= "crit3_pauseint_p1.mp3",volume= 80)
        time.sleep(2)
        misty.move_head(pitch= -21, roll= 0, yaw= 0)
        # time.sleep(2)
        misty.move_head(pitch= 0, roll= 0, yaw= 0)
        time.sleep(1)
        misty.move_head(pitch= 0, roll= 0, yaw= -24)
        feedback2 = misty.play_audio(fileName= "crit3_pauseint_p2.mp3",volume= 80)
        time.sleep(2)
        misty.move_arm(arm= "both", position= -90)
        print(feedback1)
        # print(feedback2)

        
        
