from mistyPy.GenerateRobot import RobotGenerator
from mistyPy.Robot import Robot
import json


def mt5_quiz_session():
        # load quiz data from JSON file
        quiz_data = {}
        with open('mt5_quiz.json') as f:
                quiz_data = json.load(f)

        # start quiz session
        print("Starting MT5 Quiz Session...")
        question_no = 0

        # ask if participants wants to start the quiz
        misty.speak(quiz_data["questions"][question_no])
        user_input = int(input()) # 1 if yes, 0 if no
        if user_input == 1:
                misty.speak(quiz_data["correct_feedback"][question_no])
                misty.speak(quiz_data["transitions"][question_no])
                question_no += 1
        else:
                misty.speak(quiz_data["incorrect_feedback"][question_no])
                print("Quiz session ended because participant refused to play.")
                return
        
        # begin quiz
        print("Starting to ask participant questions...")
        while user_input != "-1":
                misty.speak(quiz_data["questions"][question_no])
                user_input = int(input())
                if user_input == 1:
                        misty.speak(quiz_data["correct_feedback"][question_no])
                        misty.speak(quiz_data["transitions"][question_no])
                        question_no += 1
                else:
                        misty.speak(quiz_data["incorrect_feedback"][question_no])
                        misty.speak(quiz_data["transitions"][question_no])


if __name__ == "__main__":
        ip_address = "192.168.0.41"
        # Create an instance of a robot
        misty = Robot(ip_address)
        mt5_quiz_session()



        # current_response = misty.move_arms(30, 20)
        # current_response = misty.move_head(-40, 0, 0, 80)

        # print(current_response)
        # print(current_response.status_code)
        # print(current_response.json())

        # current_response = misty.get_log_level()
        # print(current_response)
        # print(current_response.status_code)
        # print(current_response.json())
        # print(current_response.json()["result"])