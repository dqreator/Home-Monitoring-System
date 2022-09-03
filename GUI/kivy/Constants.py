"""Constants that don't have to be any kind of property are defined here
"""
MACHINE_ID = 1
SOFTWARE_VERSION = "1.0.0"


# * UI related constants
OPACITY_ON = 1.0
OPACITY_FULL = 1.0
OPACITY_OFF = 0.333
OPACITY_WARNING = 0.25
OPACITY_ZERO = 0

SPINNER_HEIGHT = 64
SPINNER_WIDTH = 928

BUTTON_CONTENT_SPACING = 20
BUTTON_ADDITIONAL_TOUCH_AREA = 80
REMOVE_BUTTON_LAYOUT_MAX_WIDTH = 170
REMOVE_BUTTON_LAYOUT_BOTTOM_PADDING = 4
SCREEN_SWITCH_TIME = 1


# < UI Colors
_616161 = [0, 0.25, 0.38, 0.7]
_E6E6E6 = [0.90, 0.90, 0.90, 1]

TRANSPARENT_COLOR = [0.90, 0.90, 0.90, 0]




#$ MQTT  BROKER DATA 
MQTT_HOSTNAME = 'broker.hivemq.com'
MQTT_PORT = 1883


# Topic names 
TOPIC_SENDER_1 = f'DQReator/home/room1/message'
TOPIC_SENDER_1 = f'DQReator/home/room2/message'

TOPIC_LIGHT_1 = f'DQReator/home/room1/Ligth'
TOPIC_LIGHT_2 = f'DQReator/home/room2/Ligth'

TOPIC_LIGHT_1_C = f'DQReator/home/room1/LigthC'
TOPIC_LIGHT_2_C = f'DQReator/home/room2/LigthC'

TOPIC_HUMIDITY_1 = f'DQReator/home/room1/Humidity'
TOPIC_HUMIDITY_2 = f'DQReator/home/room2/Humidity'

TOPIC_TEMPERATURE_1 = f'DQReator/home/room1/Temperature'
TOPIC_TEMPERATURE_2 = f'DQReator/home/room2/Temperature'

TOPIC_DOOR_1 = f'DQReator/home/room1/Door'


TOPIC_MOTION_1 = f'DQReator/home/room1/Motion'
TOPIC_MOTION_2 = f'DQReator/home/room2/Motion'

TOPIC_BUZZER_1 = f'DQReator/home/room1/Buzzer'
TOPIC_BUZZER_2 = f'DQReator/home/room2/Buzzer'

degree_sign = u'\N{DEGREE SIGN}'



# ^ Symbols:
CM3 = " cm\u00b3"
DEG_C = " \u00b0C"


LANGUAGES = {
    "en": {
        "en": "English",
        "pl": "Angielski",
    },
    "pl": {
        "en": "Polish",
        "pl": "Polski",
    },
}