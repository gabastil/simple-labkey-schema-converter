@echo off
rem Bash script to run converter from command line

SET ERROR="No filename specified. Please specify a filename to convert (e.g., resource/schema.txt)."
SET INVALID_PATH="Specified path does not exist."

if [%1%]==[] (
    echo %ERROR%
    exit
) else (
    if not exist %1% (
        echo %INVALID_PATH%
        exit
    )
)

SET DIRNAME=%~dp1%
SET BASENAME=%~n1%
SET OUTPUT=%2%

if  [%OUTPUT%]==[] SET OUTPUT="%DIRNAME%%BASENAME%.json"

echo Converting %1 to %~n1%.json
echo Saving output to %OUTPUT%

python -m main -f %1 -o %OUTPUT%
