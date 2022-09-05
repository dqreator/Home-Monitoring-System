from ast import Pass
from email.mime import image
from xmlrpc.client import Boolean
import paho.mqtt.client
import json

from Images import ICON_DOOR_CLOSED, ICON_DOOR_OPEN, ICON_MOTION, ICON_NO_IMAGE
from kivy.event import EventDispatcher
from kivy.logger import Logger
from kivy.clock import Clock
from functools import partial
from Images import(
    ICON_LIGHT_OFF,
    ICON_LIGHT_ON
)
from kivy.properties import BooleanProperty

from Constants import (
    MQTT_HOSTNAME,
    MQTT_PORT,
    TOPIC_LIGHT_1,
    TOPIC_LIGHT_2,
    TOPIC_HUMIDITY_1,
    TOPIC_HUMIDITY_2,
    TOPIC_TEMPERATURE_1,
    TOPIC_TEMPERATURE_2,
    TOPIC_DOOR_1,
    TOPIC_MOTION_1,
    TOPIC_MOTION_2,
    degree_sign
)

class MqttConnectionManager(EventDispatcher):
    """Class that cares of all functionalities of mqtt connection.

    Args:
        EventDispatcher (_type_): _description_
    """
    light1_status = BooleanProperty(False)
    light2_status = BooleanProperty(False)

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
            self.client.subscribe([(TOPIC_HUMIDITY_1, 0)])
            self.client.subscribe([(TOPIC_TEMPERATURE_1, 0)])
            self.client.subscribe([(TOPIC_LIGHT_1, 0)])
            self.client.subscribe([(TOPIC_DOOR_1, 0)])
            self.client.subscribe([(TOPIC_MOTION_1, 0)])

            self.client.subscribe([(TOPIC_HUMIDITY_2, 0)])
            self.client.subscribe([(TOPIC_TEMPERATURE_2, 0)])
            self.client.subscribe([(TOPIC_LIGHT_2, 0)])
            self.client.subscribe([(TOPIC_MOTION_2, 0)])
        except Exception as e:
            Logger.critical(f'{self.TAG}: error: {e}')


    def on_message(self, client, userdata, message, *args):

        try:
            self.message_handler(message)
            data = json.loads(message.payload)
            Logger.debug(f"{self.TAG}: Topic: {message.topic} | Message: {message.payload} ")

        except Exception as e:
            Logger.critical(f'{self.TAG}: error: {e} {message.topic}')

#--------MISCELLANEUOS FUNCTIONS-----------------------------

    def publish(self, topic, message):
        try:
            self.client.publish(topic, message, 1)
        except Exception as e:
            Logger.critical(f'{self.TAG}: error: {e}')
            

    def message_handler(self, message):
        """ Function that handles the message and make changes in the UI and 
        update the values of the variables.
        """
        
        def change_icon(Button, Image, *largs):
            Button.source = Image

        # Set temperature values to labels
        if(message.topic == TOPIC_TEMPERATURE_1):
                self.manager.get_screen("home").temp1_label.text = message.payload.decode("utf-8")+degree_sign
        if(message.topic == TOPIC_TEMPERATURE_2):

            self.manager.get_screen("home").temp2_label.text = message.payload.decode("utf-8")+degree_sign

        # Set Humidity values to labels
        if(message.topic == TOPIC_HUMIDITY_1):
            self.manager.get_screen("home").hum1_label.text = message.payload.decode("utf-8")+" %"
        if(message.topic == TOPIC_HUMIDITY_2):
            self.manager.get_screen("home").hum2_label.text = message.payload.decode("utf-8")+" %"

        # Change light_1 icon 
        if(message.topic == TOPIC_LIGHT_1):
            if(message.payload.decode("utf-8") == "0"):
                button = self.manager.get_screen("home").light_1_icon
                image = ICON_LIGHT_OFF
                Clock.schedule_interval(partial(change_icon, button, image),0)
                self.light1_status = False
            else:
                button = self.manager.get_screen("home").light_1_icon
                image = ICON_LIGHT_ON
                Clock.schedule_interval(partial(change_icon, button, image),0)
                self.light1_status = True


        # Change light_2 icon 
        if(message.topic == TOPIC_LIGHT_2):
            if(message.payload.decode("utf-8") == "0"):
                button = self.manager.get_screen("home").light_2_icon
                image = ICON_LIGHT_OFF
                Clock.schedule_interval(partial(change_icon, button, image),0)
                self.light2_status = False

            else:
                button = self.manager.get_screen("home").light_2_icon
                image = ICON_LIGHT_ON
                Clock.schedule_interval(partial(change_icon, button, image),0)
                self.light2_status = True


        # Change door_1 icon 
        if(message.topic == TOPIC_DOOR_1):
            if(message.payload.decode("utf-8") == "1"):
                button = self.manager.get_screen("home").door_icon
                image = ICON_DOOR_OPEN
                Clock.schedule_interval(partial(change_icon, button, image),0)
                Logger.debug(f"{self.TAG}: The door is open")
            else:
                button = self.manager.get_screen("home").door_icon
                image = ICON_DOOR_CLOSED
                Clock.schedule_interval(partial(change_icon, button, image),0)
                Logger.debug(f"{self.TAG}: The door is closed")

        # Detect motion_1
        if(message.topic == TOPIC_MOTION_1):
            if(message.payload.decode("utf-8") == "0"):
                button = self.manager.get_screen("home").motion_1_icon
                image = ICON_NO_IMAGE
                Clock.schedule_interval(partial(change_icon, button, image),0)
                Logger.debug(f"{self.TAG}: No motion_1")

            else:
                button = self.manager.get_screen("home").motion_1_icon
                image = ICON_MOTION
                Clock.schedule_interval(partial(change_icon, button, image),0)
                Logger.debug(f"{self.TAG}: Motion_1")


        # Detect motion_2
        if(message.topic == TOPIC_MOTION_2):
            if(message.payload.decode("utf-8") == "0"):
                button = self.manager.get_screen("home").motion_2_icon
                image = ICON_NO_IMAGE
                Clock.schedule_interval(partial(change_icon, button, image),0)
                Logger.debug(f"{self.TAG}: No motion_2")
            else:
                button = self.manager.get_screen("home").motion_2_icon
                image = ICON_MOTION
                Clock.schedule_interval(partial(change_icon, button, image),0)
                Logger.debug(f"{self.TAG}: Motion_2")

