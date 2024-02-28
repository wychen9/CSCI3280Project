from player_control import control

if __name__ == "__main__":
    while True:
        command = input("Please enter the command (load/play/pause/resume/speed/progress/stop/quit)：")
        control(command)
        if command == 'quit':
            break
