'''Runs console and StateTree GUI (typically used for debugging purposes).
'''

# Import system libraries:
import os, sys, System, platform

# Import RayStation packages:
from connect import *
import statetree

# Run state tree:
statetree.RunStateTree()

# Change path:
scriptInstallPath = System.IO.Path.GetDirectoryName(sys.argv[0])
os.chdir(scriptInstallPath)

# Settings for console:
command = r'\"' + sys.executable + r'\"'
args = ''
setenv1 = 'set PYTHONSTARTUP=console_startup.py'
setenv2 = 'set RAYSTATION_PID="{0}"'.format(sys.argv[1])
title = 'RayStation Command Console'
exitCmd = 'exit()'

# Build console command:
consolecmd = 'Tools\Console2\Console.exe -w "{0}" -r "/k {1} & {2} & ({3} {4}) & {5}"'.format(title, setenv1, setenv2, command, args, exitCmd)

# Run console:
os.system(consolecmd)
