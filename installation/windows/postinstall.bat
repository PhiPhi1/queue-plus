echo off
set python_folder=%~1

"%python_folder%\Scripts\pip.exe" install -r .\installation\windows\requirements.txt
"%python_folder%\Scripts\pip.exe" install .\installation\windows\Twisted-19.2.0-cp37-cp37m-win32.whl
"%python_folder%\Scripts\pip.exe" install quarry

mkdir .\data
Powershell.exe -executionpolicy remotesigned -File  .\installation\windows\copy_data.ps1

echo echo off > ".\start.bat"
echo echo ########################################################## >> ".\start.bat"
echo echo ##                                                      ## >> ".\start.bat"
echo echo ##                  CTRL + C to Exit                    ## >> ".\start.bat"
echo echo ##                                                      ## >> ".\start.bat"
echo echo ########################################################## >> ".\start.bat"
echo %python_folder%\python.exe start.py >> ".\start.bat"

rmdir .\installation /q /s
del /f .\requirements.txt