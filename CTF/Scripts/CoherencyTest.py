# Copyright (C) 2007 Khronos Group
# Available only to Khronos members.
# Distribution of this file or its content is strictly prohibited.

import os
import os.path
import subprocess

import Core.Common.FUtils as FUtils
from Core.Logic.FSettingEntry import *
from Core.Common.FConstants import *
from Scripts.FApplication import *

class CoherencyTest (FApplication):
    """ Introduces the Coherency Test into the testing framework

        This script doubles as a framework for error logging, command line applications.
    """
    __SCRIPT_EXTENSION = ".py"
    
    __VALIDATE_OPTIONS = [
            ("Check Schema", "SCHEMA", "True"),
            ("Check for Circular References", "CIRCULR_REFERENCE", "True"),
            ("Check for Unique IDs", "UNIQUE_ID", "True"),
            ("Check Counts", "COUNTS", "True"),
            ("Check Files", "FILES", "True"),
            ("Check Floats", "FLOAT_ARRAY", "True"),
            ("Check Links", "LINKS", "True"),
            ("Check Skin Usage", "SKIN", "True"),
            ("Check Texture Usage", "TEXTURE", "True")
            ]
    
    
    def __init__(self, configDict):
        """__init__() -> CoherencyChecker"""
        FApplication.__init__(self, configDict)
        
        self.__workingDir = None
        self.__testCount = 0
    
    def GetPrettyName(self):
        """GetPrettyName() -> str
        
        Implements FApplication.GetPrettyName()
        
        """
        return "Coherency Test 1.0"
    
    def GetOperationsList(self):
        """GetOperationsList() -> list_of_str
        
        Implements FApplication.GetOperationsList()
        
        """
        return [VALIDATE]
    
    def GetSettingsForOperation(self, operation):
        """GetSettingsForOperation(operation) -> list_of_FSettingEntry
        
        Implements FApplication.GetSettingsForOperation()
        
        """
        if (operation == VALIDATE):
            options = []
            for entry in CoherencyTest.__VALIDATE_OPTIONS:
                options.append(FSettingEntry(*entry))
            return options
        else:
            return []
    
    def BeginScript(self, workingDir):
        """BeginScript(workingDir) -> None
        
        Implements FApplication.BeginScript()
        
        """
        filename = ("script" + str(self.applicationIndex) + 
                CoherencyTest.__SCRIPT_EXTENSION)
        self.__script = open(os.path.join(workingDir, filename) , "w")
        
        self.WriteCrashDetectBegin(self.__script)
        
        self.__testCount = 0
        self.__workingDir = workingDir
    
    def EndScript(self):
        """EndScript() -> None
        
        Implements FApplication.EndScript()
        
        """
        self.__script.close()
    
    def RunScript(self):
        """RunScript() -> None
        
        Implements FApplication.RunScript()
        
        """
        if (not os.path.isfile(self.configDict["coherencyPath"])):
            print "Coherency Test 1.0 does not exist"
            return True
        
        print ("start running " + os.path.basename(self.__script.name))
        
        command = ("\"" + self.configDict["pythonExecutable"] + "\" " +
                   "\"" + self.__script.name + "\"")
        
        returnValue = subprocess.call(command)
        
        if (returnValue == 0):
            print "finished running " + os.path.basename(self.__script.name)
        else:
            print "crashed running " + os.path.basename(self.__script.name)
        
        return (returnValue == 0)
    
    def WriteValidate(self, filename, logname, outputDir, settings, isAnimated):
        """WriteImport(filename, logname, outputDir, settings, isAnimated) -> list_of_str
        
        Implements FApplication.WriteValidate()
        
        """

        # Change the working directory to the file's directory (so executable runs correctly)
        change_dir_string = "os.chdir(r\""+os.path.dirname(filename)+"\")\n"
        self.__script.write(change_dir_string)

        # Write the executing command: >>CoherencyTestPath file
        command = ("\"" + self.configDict["coherencyPath"]+ "\" ")
        command = (command + "\"" + os.path.basename(filename) + "\"")
        
        ignore_all = True
        
        for setting in settings:
            flag = setting.GetValue().strip()
            
            try:
                flag = eval(flag.capitalize())
            except NameError, SyntaxError: # Use default if user inputs incorrect values
                flag = eval(self.FindDefault(CoherencyTest.__VALIDATE_OPTIONS, 
                                         setting.GetPrettyName()))
                    
            if flag:
                if ignore_all:
                    command = (command + " -check")
                    ignore_all = False
                command = (command + " " + setting.GetCommand())
        
        if ignore_all:
            command = (command + " -ignore")
            for setting in settings:
                command = (command + " " + setting.GetCommand())
                
        command = (command + " -ctf \"" + logname + "\" -q")
        
        # Write the above command, along with crash detection
        self.WriteCrashDetect(self.__script, command, logname)
        

        self.__testCount = self.__testCount + 1
        
        return [os.path.basename(logname),]
            
    def WriteImport(self, logname, outputDir, settings, isAnimated):
        """WriteRender(logname, outputDir, settings, isAnimated) -> list_of_str
        
        Implements FApplication.WriteImport(). Coherency Checker has no import.
        
        """
        pass
    
    def WriteRender(self, logname, outputDir, settings, isAnimated):
        """WriteRender(logname, outputDir, settings, isAnimated) -> list_of_str
        
        Implements FApplication.WriteRender(). Coherency Checker has no render.
        
        """
        pass
    
    def WriteExport(self, logname, outputDir, settings, isAnimated):
        """WriteImport(logname, outputDir, settings, isAnimated) -> list_of_strImplements FApplication.WriteExport(). Feeling Viewer has no export.

        Implements FApplication.WriteExport(). Coherency Checker has no export.

        """
        pass


