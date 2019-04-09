import math
import time
from threading import Thread

# from plot.plot import DynamicPlot

from controllers.go_to_goal import GoToGoal, Goal
from controllers.follow_wall import FollowWall
from controllers.avoid_obstacles import AvoidObstacles

from helpers.body import State
from robots.mathbot import Mathbot, Specs

from controllers.params import Params
from supervisor.full_supervisor import Supervisor as FullSupervisor
from supervisor.supervisor import Supervisor as GTGSupervisor
from supervisor.switching_supervisor import Supervisor as AOSupervisor

from helpers.spi import SpiMaster

from server import Server
import json

# Robot specification
wheel_radius = 0.02
base_length = 0.1
cpr = 984.0
min_rpm = 10
max_rpm = 165
v_max = 2 * math.pi / 60 * max_rpm * wheel_radius

# goal
goal= None

# params
k_p = 10
k_i = 0.2
k_d = 2

# motors params
k_p_const = 24.89
k_i_const = 0.1851
k_d_const = 0.0914

#port
TCP_PORT = 4200


def milliseconds():
    return int(round(time.time() * 1000))


last_time = milliseconds()
current_time = milliseconds()
dt = 0


def server_callback(body):
    dictionary = json.loads(body)
    run(float(dictionary['x']), float(dictionary['y']))


def server_thread():
    server = Server(TCP_PORT, server_callback)
    print("Start server")


def watch_time():
    global last_time, current_time, dt
    last_time = current_time
    current_time = milliseconds()
    diff = current_time - last_time
    if diff == 0:
        diff = 1
        time.sleep(0.1)
    dt = diff / 1000


mathbot = None
supervisor = None
spi = None


def simulation():
    global mathbot, supervisor
    mathbot = Mathbot(State(0, 0, 0), Specs(wheel_radius, base_length, cpr, v_max, min_rpm, max_rpm))

    go_to_goal_ctrl = GoToGoal(Params(k_p, k_i, k_d), Goal(x_goal, y_goal))

    ao_ctrl = AvoidObstacles(Params(k_p, k_i, k_d), mathbot)

    fw_ctrl = FollowWall(Params(k_p, k_i, k_d), mathbot)

    supervisor = FullSupervisor(mathbot, go_to_goal_ctrl, fw_ctrl, ao_ctrl)

    global last_time, current_time
    last_time = milliseconds()
    current_time = milliseconds()
    global change
    while not supervisor.to_stop:
        watch_time()
        supervisor.execute(dt)
        change = True
    global to_stop
    to_stop = True

def initialize():
    print("Inicijalizacija")
    global mathbot, supervisor, spi, goal
    spi = SpiMaster()

    print("reset \n")
    spi.reset()

    mathbot = Mathbot(State(0, 0, 0), Specs(wheel_radius, base_length, cpr, v_max, min_rpm, max_rpm), spi)

    goal = Goal(0, 0)

    go_to_goal_ctrl = GoToGoal(Params(k_p, k_i, k_d), goal)

    ao_ctrl = AvoidObstacles(Params(k_p, k_i, k_d), mathbot)

    fw_ctrl = FollowWall(Params(k_p, k_i, k_d), mathbot)

    ##    supervisor = FullSupervisor(mathbot, go_to_goal_ctrl, fw_ctrl, ao_ctrl)
    ##    supervisor = GTGSupervisor(mathbot, go_to_goal_ctrl)
    supervisor = AOSupervisor(mathbot, go_to_goal_ctrl, ao_ctrl)

    time.sleep(1)

    print("ticks: " + str(spi.get_ticks()))

    time.sleep(1)

    print("Start")

def run(x_coord, y_coord):
    ##    print("send PID consts")
    ##    spi.send_PID_consts(k_p_const, k_i_const, k_d_const)

    ##    print("posatvljanje objekata")
    ##    spi.set_objects()
    supervisor.to_stop = True
    spi.reset()
    goal.x = x_coord
    goal.y = y_coord
    print(goal)
    supervisor.estimated_state = State(0, 0, 0)
    supervisor.to_stop = False

def loop():
    try:
        global last_time, current_time
        last_time = milliseconds()
        current_time = milliseconds()
        while True:
            if not supervisor.to_stop:
                watch_time()
                supervisor.execute(dt)
                time.sleep(0.005)

    except KeyboardInterrupt:
        print("End")


if __name__ == '__main__':
    # sim = Thread(target=simulation)
    # sim.start()
    # if mathbot is None:
    #     while True:
    #         if mathbot is not None:
    #             break
    # if supervisor is None:
    #     while True:
    #         if supervisor is not None:
    #             break

    # d = DynamicPlot(mathbot, supervisor, "#FF8C00")
    # while not False:
    #     d.on_running()
    #     time.sleep(0.02)
    #     change = False
    # print("End")

    ser = Thread(target=server_thread)

    ser.start()
    initialize()

    loop()