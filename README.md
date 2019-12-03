![ESP32Peacock_logo](https://github.com/esp32peacock/esp32peacock/blob/master/ESP32Peacock_sqaure.jpg?raw=true)
# esp32peacock

Project ESP32Peacock is a development kit for Micropython on ESP32. It allows for users to write code through the webserver on the ESP board.

It is a binary one time upload type that allows for writing MicroPython code through the web without using USB connections. In addition, the display for terminal print and error code can be shown on the web as well.

The whole operation relies on javascript interval web load for running code. While running code in the loop section,  in intervals, the program will check for return values of the print terminal or different error messages.
