"""An example of creating a Bittle instance and communicating with it.

Three examples are provided, three of them consist in creating a Bittle
instance and connect to it through WiFi or Serial.
If connection is successful, send 'khi' and 'd' commands to check whether
Bittle receives and replies to them.
"""

import os
import sys
import time

sys.path.append(os.path.join(sys.path[0], '..'))

from pyBittle import bittleManager  # noqa: E402


__author__ = "EnriqueMoran"


greet = bittleManager.Command.GREETING  # khi command
rest = bittleManager.Command.REST  # d command
sit = bittleManager.Command.SIT  # ksit command


def test_wifi(bittle):
    """Connect to Bittle through WiFi and send 'khi' and 'd' commands.

    Parameters:
            bittle (bittleManager.Bittle) : Bittle instance.
    """
    bittle.wifiManager.ip = input("Enter Bittle IP address: ")
    print("Connecting to Bittle through WiFi...")
    if bittle.has_wifi_connection():
        print(f"Bittle found, REST API address: "
              f"{bittle.wifiManager.http_address}")
        print("Sending command: 'GREETING'...")
        response = bittle.send_command_wifi(greet)
        print(f"Received message: {response}, expected: 200")
        time.sleep(6)
        print("Sending command: 'REST'...")
        response = bittle.send_command_wifi(rest)
        print(f"Received message: {response}, expected: 200")
        time.sleep(6)
        print("Connection closed")
    else:
        print("Can't connect to Bittle")

def test_serial(bittle):
    """Connect to Bittle through Serial and send 'ksit' and 'd' commands.

    Parameters:
            bittle (bittleManager.Bittle) : Bittle instance.
    """
    print("Connecting to Bittle through Serial...")
    isConnected = bittle.connect_serial()
    print(f"Connected: {isConnected}")
    if isConnected:
        print("Sending command: 'SIT'...")
        bittle.send_command_serial(sit)
        received = bittle.receive_msg_serial()
        decoded_msg = received.decode("utf-8")
        decoded_msg = decoded_msg.replace('\r\n', '')
        print(f"Received message: {decoded_msg}, expected: k")
        time.sleep(6)
        print("Sending command: 'REST'...")
        bittle.send_command_serial(rest)
        received = bittle.receive_msg_serial()
        decoded_msg = received.decode("utf-8")
        decoded_msg = decoded_msg.replace('\r\n', '')
        print(f"Received message: {decoded_msg}, expected: d")
        time.sleep(5)
        print("Closing Serial connection...")
        bittle.disconnect_serial()
        print("Connection closed")
    else:
        print("Bittle not found")


if __name__ == "__main__":
    connection = int(input("Select test (2 -> WiFi, 3 -> Serial): "))
    if connection != 2 and connection != 3:
        print("Wrong value.")
    else:
        bittle = bittleManager.Bittle()
        print("Bittle instance created")
        if connection == 2:
            test_wifi(bittle)
        elif connection == 3:
            test_serial(bittle)
    print("Bittle data:\n {!s}".format(bittle))
