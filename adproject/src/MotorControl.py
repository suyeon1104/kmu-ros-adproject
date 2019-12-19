import serial

class MotorControl:
  def __init__(self,offset):
    self.seridev = serial.Serial('/dev/ttyMOTOR',115200)
    self.offset = offset
  def __del__(self):
    self.seridev.write('R,90,90')
  def drive(self,speed,angle):
    self.seridev.write('R,{},{}'.format(int(angle+self.offset),int(speed)))
