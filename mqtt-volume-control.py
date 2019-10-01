#!/usr/bin/python3

import smbus
import paho.mqtt.client as mqtt

# Initial volume:
default_volume: 0.8

# MQTT configuration
broker = '192.168.178.5'
user = 'username'
password = 'yoursecret'

# i2c configuration


topic_prefix = 'living/'
# vc_state =  'tv/volume'
# vc_set_topic 'tv/volume/set
# vc_up_topic: 'tv/volume/up
# vc_down_topic: 'tv/volume/down'
# vc_muted_state: 'tv/volume/muted'
# vc_mute_set: 'tv/volume/mute/set

class VolumeControl:

  def __init__(self, id):
    self.volume = default_volume
    self.muted = 'OFF'
    self.publish()

  def publish(self):
    # publish current volume level
    mqttc.publish(topic_prefix + self.id + '/volume', self.volume)
    mqttc.publish(topic_prefix + self.id + '/muted', self.muted)

class PT2259VolumeControl(VolumeControl):


def on_message(client, userdata, message):
  payload = str(message.payload.decode("utf-8"))
  topic = message.topic
  if topic == vc_set_topic:
    vc_set(payload)

def vc_set(volume):




# bus.write_byte(0x44,0xF0)
# >>> bus.write_i2c_block_data(0x44,0x74,[0xE2,0xD0])
# >>> bus.write_i2c_block_data(0x44,0x74,[0xE0,0xD0])
# bus.write_i2c_block_data(0x44,0xF0,[0x74,0xE0,0xD0])
