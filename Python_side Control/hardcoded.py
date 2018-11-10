from src.simulation import *
from src.compute_directions import *
import sys
import time

def get_next_peg(peg_list):
    if not peg_list:
        return False, 0
    return True, peg_list.pop(0)


peg_list = [20, 25]


peg_num = 48
string_thickness = 1
max_string = 2000
real_radius = 1
max_overlap = 2
window_size = [1200, 800]
baudRate = 9600

arduinoComPort = "COM6"
pygame.init()

stringomatic = System(window_size, peg_num = peg_num, string_thickness = string_thickness)

half_step = 180/peg_num
current_location = [0,0] #r, theta (degrees)
peg_locations = list([360/peg_num* i for i in range(peg_num)])

Set up serial port and send initialization message
serial_port = serial.Serial(arduinoComPort, baudRate, timeout=1)
msg_send = "Initializing"
msg_send = msg_send.encode() #'utf-8'
serial_port.write(msg_send)
time.sleep(1)

check = True #checks if string art is complete
done = False #checks if pygame window should be open
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.image.save(stringomatic.screen, "hardcoded_result.jpeg")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            elif event.key == pygame.K_SPACE:
                check = not check

    if check:
        check, next_peg = get_next_peg(peg_list)
        print("Next peg index: {}".format(next_peg))
        if check:
            stringomatic.draw_line_to(next_peg)
            stringomatic.update_window()
            peg_loc = peg_locations[next_peg]
            print("Projected peg location: {}".format(next_peg))
            current_location, commands = loop_around_peg(current_location, peg_loc, half_step, real_radius)
            print("Projected commands: {}".format(commands))
            print("Projected final location: {}".format(current_location))
            for command in commands:
                print("Sent: {}".format(command))
                send_command_and_receive_response(command, serial_port)




    else:
        sleep(.1)
