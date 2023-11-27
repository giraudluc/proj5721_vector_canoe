"""This Python module is dedicated to the control of the CANoe application.
CANoe is a development and testing software tool from Vector informatik.
The CANoe automation is done via the win32com.client (COM automation) Python module.
This module can only be used on the Windows OS.

The module contains the following classes:

- Canoe Main Class to control the CANoe application.
- EnvironmentVariable Class to access the environment variables
- SystemVariable  Class to access the simple system variables
- SystemArrayVariable Class to access the array system variables
"""

# import 

import os, sys
import win32com.client
from typing import Union


# const

# Application COM name 
CANOE_APPLICATION = "CANoe.Application"

