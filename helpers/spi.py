import Adafruit_GPIO.SPI as SPI
import time

GET_SENSOR_5 = 0xff
GET_SENSOR_4 = 0xfe
GET_SENSOR_3 = 0xfd
GET_SENSOR_2 = 0xfc
GET_SENSOR_1 = 0xfb

GET_TICKS_L = 0xfa
GET_TICKS_R = 0xf9

SET_ANGULAR_VELOCITY_L = 0xf8
SET_ANGULAR_VELOCITY_R = 0xf7

SET_OBJECTS = 0xf6

SET_K_P_CONST = 0xf5
SET_K_I_CONST = 0xf4
SET_K_D_CONST = 0xf3


RESET_ARDUINO = 0xf2

MOCK_SENSOR_DISTANCES = [30, 30, 30, 30, 30]

def milliseconds():
    return int(round(time.time() * 1000))


class SpiMaster:
    __slots__ = ['spi']

    def __init__(self):
        self.spi = SPI.SpiDev(0, 0, max_speed_hz=1000)
        
    def reset(self):
        self._send_value(RESET_ARDUINO, 0)
##        self.send_command(RESET_ARDUINO)
        time.sleep(2.5)
        
    def set_objects(self):
        self._send_value(SET_OBJECTS, 0)
##        self.send_command(SET_OBJECTS)
        print("postavljeni objekti")
        time.sleep(1)
        
    def send_PID_consts(self, k_p_const, k_i_const, k_d_const):
        k_p_const *= 10000
        k_i_const *= 10000
        k_d_const *= 10000
        self._send_value(SET_K_P_CONST, int(k_p_const))
        print("poslan k_p: " + str(k_p_const))
##        time.sleep(0.05)
        self._send_value(SET_K_I_CONST, int(k_i_const))
        print("poslan k_i: " + str(k_i_const))
##        time.sleep(0.05)
        self._send_value(SET_K_D_CONST, int(k_d_const))
        print("poslan k_d: " + str(k_d_const))
        time.sleep(1)

    def send_velocities(self, left, right):
        left *= 1000
        right *= 1000
##        print(int(left), int(right))
        self._send_value(SET_ANGULAR_VELOCITY_L, int(left))
##        time1 = milliseconds()
        self._send_value(SET_ANGULAR_VELOCITY_R, int(right))
##        time2 = milliseconds()
##        print(time2, time1)

    def get_ticks(self):
        ticks_left = self._read_value(GET_TICKS_L)
        ticks_right = self._read_value(GET_TICKS_R)
        #print(ticks_left, ticks_right)
        return ticks_left, ticks_right

    def get_sensors(self):
        sensor_distances = 5 * [0.0]
        for i in range(5):
            sensor_distances[i] = self.get_sensor(i) / 100.0
        print(sensor_distances)
        return sensor_distances
##        return MOCK_SENSOR_DISTANCES
            
    def get_sensor(self, i):
        if i == 0:
            command = GET_SENSOR_1
        elif i == 1:
            command = GET_SENSOR_2
        elif i == 2:
            command = GET_SENSOR_3
        elif i == 3:
            command = GET_SENSOR_4
        elif i == 4:
            command = GET_SENSOR_5
        return self._read_value(command)

    def _send_value(self, command: int, value: int):
        self.spi.write([command])
##        time.sleep(0.005)
        for i in [value >> i & 0xff for i in (24, 16, 8, 0)]:
            self.spi.write([i])

    def _read_value(self, command: int):
        self.spi.write([command])
        if command != GET_TICKS_L and command != GET_TICKS_R:
            time.sleep(0.005)
        byte_array = bytearray()
        for i in range(4):
            byte_array += self.spi.read(1)
        value = int.from_bytes(byte_array, byteorder='little', signed=True)
        return value
    
    def send_command(self, command: int):
        self.spi.write([command])
        time.sleep(6)


if __name__ == '__main__':
    master = SpiMaster()
##    master.reset()
##    time.sleep(6)
##    master.send_velocities(0, 0)
##    time.sleep(2)
##    master.send_velocities(9, 10)
##    time.sleep(5)
##    master.send_velocities(-10, -13)
##    time.sleep(5)
##    master.send_PID_consts(2.1, 120.0, 0.5)
##    master.set_objects()
##    master.reset()
##    time.sleep(5)
##    master.send_velocities(9, 10)
##    time.sleep(5)
##    master.send_velocities(-10, -13)
##    time.sleep(5)
##    master.send_PID_consts(2.1, 120.0, 0.5)
##    master.set_objects()
##    master.reset()
    while(True):
##      print(master.get_ticks())
      print(master.get_sensors())
##      print(master.ticks_left)
##      print(master.ticks_right)

