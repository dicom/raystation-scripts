import os, sys, System, platform, statetree
from connect import *
statetree.RunStateTree()

scriptInstallPath = System.IO.Path.GetDirectoryName(sys.argv[0])
os.chdir(scriptInstallPath)

command = r'\"' + sys.executable + r'\"'
if platform.python_implementation() == "IronPython":
    args = '-X:TabCompletion -X:ColorfulConsole -X:AutoIndent -X:Frames'
    setenv1 = 'set IRONPYTHONSTARTUP=console_startup.py'
else:
    args = ''
    setenv1 = 'set PYTHONSTARTUP=console_startup.py'

setenv2 = 'set RAYSTATION_PID="{0}"'.format(sys.argv[1])
title = 'RayStation Command Console'
exitCmd = 'exit()'

consolecmd = 'Tools\Console2\Console.exe -w "{0}" -r "/k {1} & {2} & ({3} {4}) & {5}"'.format(title, setenv1, setenv2, command, args, exitCmd)
os.system(consolecmd)
