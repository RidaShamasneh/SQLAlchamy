@ECHO OFF

SET argc=0
FOR %%c IN (%*) DO SET /A argc+=1

IF %argc% GTR 2 GOTO USAGE

IF "%1"=="" GOTO BUILD_DEFAULT

FOR %%p IN (%*) DO (
    IF /I "%%p"=="--help" (
        GOTO USAGE
    ) ELSE (
        IF /I "%%p"=="--packages" (
            call :INSTALL_PACKAGES
        ) ELSE (
                IF /I "%%p"=="--gui" (
                    call :BUILD_GUI
        ) ELSE (
                IF /I "%%p"=="--default" (
                    call :BUILD_DEFAULT
        ) ELSE (
                GOTO USAGE
                        )
                    )
                )
            )
        )

EXIT /B 0

:BUILD_DEFAULT
    call :BUILD_GUI
EXIT /B 0

:BUILD_GUI
    call common.bat INIT
    cd gui
    call build_gui.bat
    cd ..

    call common.bat COLOR_ECHO %Green% "Info: Copy GUI dist"
    xcopy /s /y "%GUI_DIR%\%DIST_DIR%" "%cd%\%DIST_DIR%"
EXIT /B 0

:INSTALL_PACKAGES
    call common.bat INIT
    call common.bat BUILD_TOOLS_CHECK && exit /b
    call common.bat PACKAGES_CHECK && exit /b
EXIT /B 0

:USAGE
    ECHO Crystal Ball Builder v1.0
    ECHO build.bat [arg1] [arg2]
    ECHO.
    ECHO Usage: --help        Show this message.
    ECHO        --packages    Install python dependencies to libs folder.
    ECHO        --gui         Build GUI
    ECHO        --default     Build GUI
    ECHO.
    ECHO Notes: * Running the script without arguments will call --default
    ECHO        * Dist folder includes binaries.
    ECHO.
EXIT /B 0