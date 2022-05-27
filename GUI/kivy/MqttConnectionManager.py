import paho.mqtt.client
import json
from threading import Thread, Event
from kivy.event import EventDispatcher
from kivy.logger import Logger

from Constants import (
    MQTT_HOSTNAME,
    MQTT_PORT,
    MACHINE_ID,
    TOPIC_SENDER,
    TOPIC_RECEIVER,
    MACHINE_ID
)

class MqttConnectionManager(EventDispatcher):

    def __init__(self, manager, **kwargs):
        super(MqttConnectionManager, self).__init__(**kwargs)
        self.TAG = "MqttConnectionManager"
        self.manager = manager
        self.client = paho.mqtt.client.Client(client_id=f'Hometion', clean_session=False)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_disconnect = self.on_disconnect
        

        try:
            self.client.connect(host=MQTT_HOSTNAME, port=MQTT_PORT)
            self.client.loop_start()
        except Exception as e:
            Logger.critical(f'error: {e}')
    

    def on_publish(self,client, userdata, result, *args):
        Logger.debug(f'{self.TAG}: {client}  userdata: {userdata}  result: {result} ')
        pass


    def on_disconnect(self):
        Logger.debug(f'{self.TAG}: Client disconnected')


    def on_connect(self, client, userdate, flags, rc, *args):
        try:
            Logger.debug(f'{self.TAG}: Connected ')
            self.client.subscribe([(TOPIC_RECEIVER, 0)])
        except Exception as e:
            Logger.critical(f'{self.TAG}: error: {e}')


    def on_message(self, client, userdata, message, *args):
        #todo: Create functions to do an activity  acording with the message received

        try:
            self.message_handler(message.payload)
            # data = json.loads(message.payload)
            Logger.debug(f"{self.TAG}: Topic: {message.topic} | Message: {message.payload} ")
            
        except Exception as e:
            # Logger.critical(f'{self.TAG}: Invalid message')
            Logger.critical(f'{self.TAG}: error: {e}')

#--------MISCELLANEUOS FUNCTIONS-----------------------------

    def publish(self, topic, message):
        try:
            self.client.publish(topic, message, 1)
        except Exception as e:
            Logger.critical(f'{self.TAG}: error: {e}')



    def message_handler(self, message):
        
        print(f"El mensaje es:{message} ")
