@echo off
call:%*
exit /B

:INIT
    set PACKAGES=enum configparser py2exe sqlalchemy mysql sqlalchemy_utils lxml

    set enum=enum34-1.1.6-py2-none-any.whl
    set configparser=configparser-3.5.0.tar.gz
    set py2exe=pyparsing-2.4.0-py2.py3-none-any.whl packaging-19.0-py2.py3-none-any.whl appdirs-1.4.3-py2.py3-none-any.whl py2exe-0.6.10a1-cp27-none-win_amd64.whl
    set PyQt4=PyQt4-4.11.4-cp27-cp27m-win_amd64.whl
    set sqlalchemy=SQLAlchemy-1.3.11.tar.gz
    set mysql=mysql_connector_python-8.0.18-py2.py3-none-any.whl
    set sqlalchemy_utils=SQLAlchemy-Utils-0.35.0.tar.gz
    set lxml=lxml-4.2.5-cp27-cp27m-win_amd64.whl

    set WHEEL_DIR=3rd_party_libs
    set LIBS_DIR=libs
    set BUILD_DIR=build
    set DIST_DIR=dist
    set GUI_DIR=gui
    set PYTHONPATH=%LIBS_DIR%

    set ESC=
    set Red=%ESC%[31m
    set Green=%ESC%[32m
    set Yellow=%ESC%[33m
    set Blue=%ESC%[34m
    set Magenta=%ESC%[95m
    set White=%ESC%[37m

    call :COLOR_ECHO %Green% "Info: Init system variables"
exit /B

:PREPARE_BUILD
	call :COLOR_ECHO %Green% "Info: Prepare build"
	if exist %DIST_DIR% (
		rmdir %DIST_DIR% /s /q
	)
exit /B

:BUILD_EXE
    call :COLOR_ECHO %Green% "Building..."
	python setup.py py2exe
exit /B

::COLOR_ECHO color_enum string
:COLOR_ECHO
    echo %~1%~2%White%
exit /B

:BUILD_TOOLS_CHECK
	call :COLOR_ECHO %Green% "Info: Check for build tools Installation"

	python --version 2>NUL 1>NUL
	if errorlevel 1 (
		call :COLOR_ECHO %Red% "Error: Python27 not installed"
		exit /B 0
	)

	pip --version 2>NUL 1>NUL
	if errorlevel 1 (
	    call :COLOR_ECHO %Red% "Error: Pip not installed"
		call :COLOR_ECHO %Red% "       To install pip, do one of the following:"
		call :COLOR_ECHO %Red% "       Note: You possibly need an administrator command prompt to do this."
		call :COLOR_ECHO %Red% "       - Install pycharm: https://www.jetbrains.com/pycharm/download/#section=windows"
		call :COLOR_ECHO %Red% "       - . download https://bootstrap.pypa.io/get-pip.py"
		call :COLOR_ECHO %Red% "         . python get-pip.py"
		call :COLOR_ECHO %Red% "         . Add [drive:]\Python27\Scripts to system environment"
		exit /B 0
	)
exit /B 1

::INSTALL_PACKAGE package_name installation_path
:PIP_INSTALL
    if "%~2" == "" (
        pip install %WHEEL_DIR%\%~1 --no-cache-dir --no-dependencies --upgrade 2>NUL
    ) else (
        pip install %WHEEL_DIR%\%~1 --no-cache-dir --no-dependencies --upgrade -t %~2 2>NUL
    )
exit /B

::CHECK_PACKAGE package_name package_location
:CHECK_PACKAGE
	if "%~2" == "" (
		python -c "import %~1" 2>NUL
	) else (
		python -c "import sys, os; sys.path.insert(0, '%~2'); import %~1; ret=os.path.basename('%LIBS_DIR%') in %~1.__file__; exit(not ret)"  2>NUL
	)
exit /B

:PATCH_PACKAGE
    call :COLOR_ECHO %Green% "Info: Patch packages"
	type NUL > %LIBS_DIR%\__init__.py
	type NUL > %LIBS_DIR%\backports\__init__.py
exit /B

:PACKAGES_CHECK
    call :COLOR_ECHO %Green% "Info: Check for Python packages"
    if not exist %LIBS_DIR% (
        mkdir %LIBS_DIR%
    )

    ::special case, install on system site-packages
    call :CHECK_PACKAGE PyQt4
    if errorlevel 1 (
        call :COLOR_ECHO %Magenta% "Warning: package `PyQt4` is not installed. Attempt to install."
        call :PIP_INSTALL %PyQt4%
        if errorlevel 1 (
            call :COLOR_ECHO %Red% "Error: `PyQt4` encourage installation problems."
            exit /B 0
        )
    )

    SetLocal EnableDelayedExpansion
        for %%p in (%PACKAGES%) do (
            set package=%%p

            call :CHECK_PACKAGE !package! %LIBS_DIR%
            if errorlevel 1 (
                call :COLOR_ECHO %Magenta% "Warning: package `%%p` is not installed. Attempt to install."
                for %%w in (!!%%p!!) do (
                    call :PIP_INSTALL %%w %LIBS_DIR%
                    if errorlevel 1 (
                        call :COLOR_ECHO %Red% "Error: `%%w` encourage installation problems."
                        exit /B 0
                    )
                )
            )
        )
    SetLocal DisableDelayedExpansion

    call :PATCH_PACKAGE
exit /B 1
