# encoding: utf8

# A script that runs the console and shows the state tree.
#
# Source:
# https://github.com/raysearchlabs/scripting
#
# Tested for RayStation version: 6.0.

import os, sys, System, statetree
from connect import *

statetree.RunStateTree()

ipyInstallPath = System.IO.Path.GetDirectoryName(System.Environment.GetCommandLineArgs()[0])
scriptInstallPath = System.IO.Path.GetDirectoryName(sys.argv[0])
os.chdir(scriptInstallPath)

ironpython = r'\"' + ipyInstallPath + r'\ipy.exe\"'
ironpythonargs = '-X:TabCompletion -X:ColorfulConsole -X:AutoIndent -X:Frames'

setenv1 = 'set IRONPYTHONSTARTUP=console_startup.py'
setenv2 = 'set RAYSTATION_PID="{0}"'.format(sys.argv[1])

title = 'RayStation Command Console'
exitCmd = 'exit()'

consolecmd = 'Tools\Console2\Console.exe -w "{0}" -r "/k {1} & {2} & ({3} {4}) & {5}"'.format(title, setenv1, setenv2, ironpython, ironpythonargs, exitCmd)
os.system(consolecmd)
