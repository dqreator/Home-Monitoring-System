# Home-Monitoring-System
Project of a Home monitoring system

The graphical interface was composed by two different screens, the Splash screen  and the Home screen. The first one will be displayed when  the program is loading, and the home screen displays the dashboard for the user.

The Graphical interface has the functionality to change between dark mode and light mode, displays the values of Temperature and Humidity from two different rooms, displays if there is motion in one of them, and detects if the door is open or closed. Additionally, It was implemented  a button that sends a signal to the microcontroller to toggle a light in each room.

To handle the communication between the sensors and the Graphical Interface was implemented the MQTT protocol in a ESP-32 board.
