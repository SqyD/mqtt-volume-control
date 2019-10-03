#!/usr/bin/python3

import smbus
import paho.mqtt.client as mqtt

# Initial volume:
default_volume: 0.8

# MQTT configuration
broker = '192.168.178.5'
user = 'username'
password = 'yoursecret'
topic_prefix = 'homeassistant'

# i2c configuration

class VolumeControl:

  def __init__(self, id):
    self.id = id
    self.volume = default_volume
    self.muted = 'OFF'
    self.volume_topic = topic_prefix + '/sensor/' + self.id + '/volume'
    self.mute_topic = topic_prefix + '/binary_sensor/' + self.id + '/mute'
    self.publish()

  def discovery(self):
  
  def publish(self):
    # publish current volume level
    mqttc.publish(self.volume_topic, self.volume)
    mqttc.publish(self.mute_topic, self.muted)

class PT2259VolumeControl(VolumeControl):

def on_message(client, userdata, message):
  payload = str(message.payload.decode("utf-8"))
  topic = message.topic
  if topic == vc_set_topic:
    vc_set(payload)

def vc_set(volume):

# import smbus
# bus = smbus.SMBus(1)
# bus.write_byte(0x44,0xF0)
# >>> bus.write_i2c_block_data(0x44,0x74,[0xE2,0xD0])
# >>> bus.write_i2c_block_data(0x44,0x74,[0xE0,0xD0])
# bus.write_i2c_block_data(0x44,0xF0,[0x74,0xE0,0xD0])
