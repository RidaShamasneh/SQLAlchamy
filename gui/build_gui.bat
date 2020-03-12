call ..\common.bat INIT
set RESOURCES_DIR=resources
set LIBS_DIR=..\libs
set WHEEL_DIR=..\3rd_party_libs
set PYTHONPATH=%LIBS_DIR%

call ..\common.bat COLOR_ECHO %Green% "Info: Building GUI"
call ..\common.bat BUILD_TOOLS_CHECK && exit /b
call ..\common.bat PACKAGES_CHECK && exit /b
call ..\common.bat PREPARE_BUILD
call :GENERATE_RESOURCES
call ..\common.bat BUILD_EXE
call :COPY_FILES
call :CLEAN_UP
exit /B 0

:GENERATE_RESOURCES
    call ..\common.bat COLOR_ECHO %Green% "Info: Generating Resources file"
	cd %RESOURCES_DIR%
    call generate_resources.bat
	cd ..
exit /B

:COPY_FILES
call ..\common.bat COLOR_ECHO %Green% "Info: Copy GUI INI files"
    if exist config.ini (
        copy config.ini "%cd%\%DIST_DIR%"
    )
call ..\common.bat COLOR_ECHO %Green% "Info: Copy SQL Migration Script"
    if exist ..\migration_scripts\migration_0.0.2_to_0.0.3.sql (
        copy ..\migration_scripts\migration_0.0.2_to_0.0.3.sql "%cd%\%DIST_DIR%"
    )
    if exist ..\migration_scripts\migration_0.0.4_to_0.0.5.sql (
        copy ..\migration_scripts\migration_0.0.4_to_0.0.5.sql "%cd%\%DIST_DIR%"
    )
exit /B

:CLEAN_UP
    call ..\common.bat COLOR_ECHO %Green% "Info: Clean up"
	if exist %BUILD_DIR% (
		rmdir %BUILD_DIR% /s /q
	)
	call ..\common.bat COLOR_ECHO %Green% "Info: Done, output directory is %cd%\%DIST_DIR%"
exit /B