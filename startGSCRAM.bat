chcp 65001
set PYTHONIOENCODING=UTF-8
echo off
title G.roundSpace C.ounter R.ocket A.rtillary and M.ortar                startGSCRAM.bat
:loop
cd \GSCRAM
python -i \GSCRAM\startGSCRAM.py
goto loop
