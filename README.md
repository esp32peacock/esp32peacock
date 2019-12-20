![ESP32Peacock_logo](https://github.com/esp32peacock/esp32peacock/blob/master/ESP32Peacock.png?raw=true)
![ESP32Peacock_preload_board](https://github.com/esp32peacock/esp32peacock/blob/master/ESP32Peacock_V_small.png?raw=true)
# esp32peacock

Project ESP32Peacock is a development kit for Micropython on ESP32. It allows for users to write code through the webserver on the ESP board.

It is a binary one time upload type that allows for writing MicroPython code through the web without using USB connections. In addition, the display for terminal print and error code can be shown on the web as well.

The whole operation relies on javascript interval web load for running code. While running code in the loop section,  in intervals, the program will check for return values of the print terminal or different error messages.

# Install
To use this code you need DFRobot uPyCraft <a href='https://github.com/DFRobot/uPyCraft'>https://github.com/DFRobot/uPyCraft</a>

Flash ESP32 with lastest MicroPython bin download from <a href='http://micropython.org/download'>http://micropython.org/download</a> at 0x1000

Connect ESP32 by click Serial button and Link drag and drop file on this Git to ESP32

# License
MIT License

Copyright (c) 2020 Bunnavit Sawangpiriyakij


<IMG src="https://github.com/esp32peacock/esp32peacock/blob/master/ESP32Peacock_Screen2%20(1).jpg?raw=true" width="30%"><IMG src="https://github.com/esp32peacock/esp32peacock/blob/master/ESP32Peacock_Screen2%20(2).jpg?raw=true" width="30%">
