#!/usr/bin/python3

import smbus
import paho.mqtt.client as mqtt
import yaml
import math

# Initial volume for devices that don't override this in their config:
default_volume = 0.8

# Generic class to control audio volumes
class VolumeControl:

  def __init__(self, device_id):
    self.id = device_id
    self.volume_topic = config['mqtt']['prefix'] + '/sensor/' + self.id + '/volume'
    self.mute_topic = config['mqtt']['prefix'] + '/binary_sensor/' + self.id + '/mute'
    self.muted = 'OFF'
    if default_volume in config['devices'][self.id]:
      self.volume_set(config['devices'][self.id]['default_volume'])
    else:
      self.volume_set(default_volume)

  # def discovery(self):
  
  def volume_set(self,volume):
    self.volume = volume
    if self.muted == 'ON':
      self.mute('OFF')
    mqttc.publish(self.volume_topic, self.volume)

  def volume_up(self):
    volume = self.volume + 0.1
    if volume > 1:
      volume = 1
    self.volume_set(volume)

  def volume_down(self):
    volume = self.volume - 0.1
    if volume < 0.1:
      volume = 0.1
    self.volume_set(volume)

  def mute(self, muted):
    self.muted = muted
    mqttc.publish(self.mute_topic, self.muted)

class PT2259VolumeControl(VolumeControl):
  
  def __init__(self, device_id):
    self.bus = smbus.SMBus(config['devices'][device_id]['i2c_bus'])
    self.bus.write_byte(0x44,0xF0) 
    super().__init__(device_id)

  def volume_set(self, volume):
    super().volume_set(volume)
    self.volume_control()

  def mute(self, muted):
    super().mute(muted)
    self.volume_control()
    
  def volume_control(self):
    # Convert volume gain to db
    volume_db = abs(int(25*math.log2(self.volume)))
    if volume_db > 79:
      volume_db = 79
    print('setting volume to ' + str(self.volume) + ' as a value of ' + str(volume_db) + 'db')
    # db to pt2259 values
    muted_cmd = 0x74
    if self.muted == 'ON':
      muted_cmd = muted_cmd + 3
    volume_cmd1 = 0xE0 + volume_db // 10**1 % 10
    volume_cmd2 = 0xD0 + volume_db // 10**0 % 10
    self.bus.write_i2c_block_data(0x44,muted_cmd,[volume_cmd1,volume_cmd2])

class AlsaVolumeControl(VolumeControl):
  
  def __init__(self,id):
    super().__init__(id)

def load_config():
  # Read the configuration file
  config_file = open('configuration.yaml', 'r')
  # Parse the configuration into a dictionary
  config = yaml.safe_load(config_file)
  config_file.close
  return config

def on_message(client, userdata, message):
  payload = str(message.payload.decode("utf-8"))
  topic = message.topic
  if topic == vc_set_topic:
    vc_set(payload)

## Main routine ##

# Load the configuration file
config = load_config()

# Initialize the mqtt client
mqttc = mqtt.Client()

# Populate the device list
devices = {}
for device_id, device_config in config['devices'].items():
  if device_config['platform'] == 'pt2259':
    devices[device_id] = PT2259VolumeControl(device_id)
  if device_config['platform'] == 'alsa':
    devices[device_id] = AlsaVolumeControl(device_id)
  # devices[device_id].connect()

# Loop


# import smbus
# bus = smbus.SMBus(1)
# bus.write_byte(0x44,0xF0)
# >>> bus.write_i2c_block_data(0x44,0x74,[0xE2,0xD0])
# >>> bus.write_i2c_block_data(0x44,0x74,[0xE0,0xD0])
# bus.write_i2c_block_data(0x44,0xF0,[0x74,0xE0,0xD0])
