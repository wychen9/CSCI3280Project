from soundplayer import AudioPlayer


def control(command):
    global player, start_percentage, stop_percentage, set_flag
    words = command.split(' ')
    if words[0] == 'load':
        path = words[1]
        player = AudioPlayer(path)
        start_percentage = 0
        stop_percentage = 100.0
        set_flag=False
    elif words[0] == 'set':
        start_percentage = float(words[1])
        if len(words) > 2:
            stop_percentage = float(words[2])
        else:
            stop_percentage = 100.0
        if player.play_obj is None or player.play_obj.is_playing() == False:
            set_flag=True
        else:
            player.play(start_percentage, stop_percentage)
    elif words[0] == 'play':
        if set_flag:
            set_flag=False
            player.play(start_percentage, stop_percentage)
        else:
            player.play()
    elif words[0] == 'speed':
        speed = words[1]
        player.set_speed(speed)
    elif command == 'pause':
        player.pause()
    elif command == 'resume':
        if set_flag:
            set_flag=False
            player.play(start_percentage, stop_percentage)
        else:
            player.resume()
    elif command == 'stop':
        player.stop()
    elif command == 'quit':
        player.stop()
    else:
        print("Invalid command, please re-enter.")

"""
if __name__ == "__main__":
    while True:
        command = input("Please enter the command (load/play/pause/resume/speed/progress/stop/quit)：")
        control(command)
        if command == 'quit':
            break
"""
