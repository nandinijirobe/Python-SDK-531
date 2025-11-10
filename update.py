from mistyPy.GenerateRobot import RobotGenerator
from mistyPy.Robot import Robot


def mt5_question1 ():
        for i in range (10):
                pitch_no = 0.0
                misty.speak(text= "I spy with my little eye", pitch= pitch_no)
                pitch_no += 0.1


if __name__ == "__main__":
        ip_address = "192.168.0.41"
        # Create an instance of a robot
        misty = Robot(ip_address)
        mt5_question1()

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