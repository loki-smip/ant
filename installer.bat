@echo off
:: Define the target directory in the user's Documents folder
set "TARGET_DIR=%USERPROFILE%\Documents\Hacker Antivirus"


set "GITHUB_REPO=https://github.com/loki-smip/ant"

:: Check if Git is installed
echo Checking for Git...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git is not installed. Please install Git and try again.
    pause
    exit /b
)

:: Check if Python is installed
echo Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and try again.
    pause
    exit /b
)

:: Create the target directory if it doesn't exist
if not exist "%TARGET_DIR%" (
    echo Creating Hacker Antivirus folder...
    mkdir "%TARGET_DIR%"
)

:: Navigate to the target directory
cd /d "%TARGET_DIR%"

:: Clone the GitHub repository
echo Cloning the antivirus program from GitHub...
git clone %GITHUB_REPO% . >nul 2>&1
if %errorlevel% neq 0 (
    echo Failed to clone the repository. Please check the GitHub URL and try again.
    pause
    exit /b
)

:: Install required Python libraries
echo Installing required Python libraries...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo Failed to install required libraries. Ensure pip is properly installed and try again.
    pause
    exit /b
)

:: Log the installation success
echo Installation completed successfully on %DATE% at %TIME% >> install_log.txt
echo Installation log created at %TARGET_DIR%\install_log.txt

:: Notify the user
echo Hacker Antivirus has been successfully installed in your Documents folder!
echo Run the program by navigating to %TARGET_DIR% and executing the script.
pause
