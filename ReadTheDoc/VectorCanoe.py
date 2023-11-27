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

# class

class Canoe:
  """Main class to control the CANoe application."""

  def __init__(self):
    """Constructor"""
    self.App = win32com.client.Dispatch(CANOE_APPLICATION)

  def getApplication(self):
    """Get the current CANoe application COM object instance.
    """
    return(self.App)
  
  def isMeasurementRunning(self) -> bool:
    """Verify if the Canoe measurement is running or not.

    Returns:
      bool: Measurement running or not
    """
    if(self.App.Measurement.Running):
      return True
    else:
      return False
  
  def stopMeasurement(self):
    """Stop the Canoe measurement if running."""
    if(self.isMeasurementRunning() == True):
      self.App.Measurement.Stop()

  def startMeasurement(self):
    """Start the Canoe measurement if not running."""
    if(self.isMeasurementRunning() == False):
      self.App.Measurement.Start()
  
  def writeMessage(self, message: str):
    """Write a message on the CANoe messages console.

    Args:
      message (str): Message to write
    """
    self.App.UI.Write.Output(message)

  def ClearMessage(self):
    """Clear the CANoe message messages console."""
    self.App.UI.Write.Clear()

  def listSystemVariables(self, namespace: str) -> list[str]:
    """List the CANoe system variables names belonging to the given namespace.

    Args:
      namespace (str): Namespace name

    Returns:
      list[str]: List of system variables names
    """
    systemVariables = []
    systemCAN = self.App.System.Namespaces
    try:
      systemNamespace = systemCAN(namespace)
      systemNamespaceVariables = systemNamespace.Variables
      for systemNamespaceVariable in systemNamespaceVariables:
        name = systemNamespaceVariable.Name
        systemVariables.append(name)
    except:
      print("Cannot read the %s namespace variables !" % namespace)
    return(systemVariables)

  def addSystemVariablesFile(self, systemVariablesFile: str) -> bool:
    """Add the given system variable file (*.vsysvar) to the CANoe simulation

    Args:
    systemVariablesFile (str): File name and path

    Returns:
    bool: Command accepted or not
    """
    ok = False 
    if(os.path.exists(systemVariablesFile) and os.path.splitext(systemVariablesFile)[1] == ".vsysvar"):
      variablesFiles = self.App.System.VariablesFiles
      variablesFiles.Add(systemVariablesFile)
      ok = True
    return(ok)

class EnvironmentVariable():
  "Class to access an environment variable"
  
  def __init__(self, canoe, name: str):
    """Constructor

    Args:
        canoe (Canoe): Canoe instance
        name (str): Environment variable name
    """
    self.canoe = canoe
    self.name = name
    try:
      self.variable = self.canoe.App.Environment.GetVariable(self.name)
    except:
      print("EnvironmentVariable '%s' exception ! " % name)
  
  def set(self, value: Union[int, float, str]):
    """Set the environment variable value.

    Args:
        value (Union[int, float, str]): Value to set
    """
    ok = False
    try:
      self.variable.Value = value
      ok = True
    except:
      print("Incorrect value type !")
    return(ok)
  
  def get(self) -> Union[int, float, str]:
    """Get the environment variable value.

    Returns:
        Union[int, float, str]: Environment variable value
    """
    return(self.variable.Value)

class SystemVariable():
  "Class to access a simple system variable"
  
  def __init__(self, canoe, nameSpace: str, name: str):
    """Constructor

    Args:
        canoe (Canoe): Canoe instance
        nameSpace (str): System variable nameSpace
        name (str): System variable name
    """
    self.canoe = canoe
    self.name = name
    self.nameSpace = nameSpace
    try:
      systemCAN = self.canoe.App.System.Namespaces
      sys_namespace = systemCAN(nameSpace)
      self.variable = sys_namespace.Variables(name)
    except:
      print("SystemVariable '%s' '%s' exception ! " % (nameSpace, name))
  
  def get(self) -> Union[int, float, str]:
    """Get the system variable value.

    Returns:
      Union[int, float, str]: system variable value
    """
    return(self.variable.Value)

  def set(self, value: Union[int, float, str]) -> bool:
    """Get the system variable value.

    Args:
      value (Union[int, float, str]): Value to set

    Returns:
      bool: Operation performed or not.
    """
    ok = False
    try:
      self.variable.Value = value
      ok = True
    except:
      print("Incorrect value type !")
    return(ok)

class SystemArrayVariable():
  "Class to access an array system variable"
  
  def __init__(self, canoe, nameSpace: str, name: str):
    """Constructor.

    Args:
        canoe (Canoe): Canoe instance
        nameSpace (str): system variable nameSpace
        name (str): system variable name
    """
    self.canoe = canoe
    self.name = name
    try:
      systemCAN = self.canoe.App.System.Namespaces
      sys_namespace = systemCAN(nameSpace)
      self.variable = sys_namespace.Variables(name)
    except:
      print("EnvironmentVariable '%s' exception ! " % name)
  
  def get(self):
    """Get the system variable array values.

    Args:
        self (_type_): System variable array values
    
    Returns:
      List(Union[int, float, str]: Variable array values
    """
    return(self.variable.Value)

  def set(self, values) -> bool:
    """Set the system variable array values.

    Args:
      values (List(Union[int, float, str]): Array values

    Returns:
      bool: Operation performed or not.
    """
    ok = False
    try:
      if(type(values) == list or type(values) == tuple):
        buffer = list(self.get())
        n = len(buffer)
        if(len(values) <= n):
          n=len(values)
        for i in range(n):
          buffer[i] = values[i]
        self.variable.Value = buffer
        ok = True
    except:
      print("EnvironmentVariable '%s' write exception ! " % self.name)
    return(ok)
