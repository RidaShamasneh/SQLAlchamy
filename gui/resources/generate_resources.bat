@echo off

@setlocal
pushd "%~dp0"

set site=
for /f "delims=" %%A in ('python -c "import site; print site.getsitepackages()[1]+\"\PyQt4\""') do set "site=%%A"
rem set PATH=%PATH%;%site%

%site%\pyrcc4.exe -py2 -o gui_resources.py resources.qrc

popd
@endlocal