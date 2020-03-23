rm -rf dist
pyinstaller -y "C:/Users/david2004kang_i7/Documents/YAV_ADIO_GUI/YAV_ADIO_GUI.py"
cp ADIO64.dll dist\YAV_ADIO_GUI\.
cp gain.txt dist\YAV_ADIO_GUI\.
cd dist
rm -rf YAV_ADIO_GUI\certifi
rm -rf YAV_ADIO_GUI\etc
rm -rf YAV_ADIO_GUI\gevent
rm -rf YAV_ADIO_GUI\gevent-1.4.0-py2.7.egg-info
del YAV_ADIO_GUI\gevent*
del YAV_ADIO_GUI\_hashlib.*
del YAV_ADIO_GUI\_scandir.*
del YAV_ADIO_GUI\_sqlite3.*
del YAV_ADIO_GUI\PIL.*
del YAV_ADIO_GUI\zmq.*
del YAV_ADIO_GUI\mfc90u.dll
del YAV_ADIO_GUI\mpl-data\images\*.pdf
del YAV_ADIO_GUI\select.pyd
del YAV_ADIO_GUI\msvcr90.dll
del YAV_ADIO_GUI\msvcp90.dll
del YAV_ADIO_GUI\sqlite3.dll
del YAV_ADIO_GUI\win32ui.pyd
del YAV_ADIO_GUI\mfc90.dll
del YAV_ADIO_GUI\_bsddb.pyd
del YAV_ADIO_GUI\_msvcm90.dll
del YAV_ADIO_GUI\libzmq.pyd
del YAV_ADIO_GUI\win32com.shell.shell.pyd
del YAV_ADIO_GUI\_msvcm90.dll
rm -rf YAV_ADIO_GUI\importlib_metadata-1.5.0-py2.7.egg-info
rm -rf YAV_ADIO_GUI\Include
rm -rf YAV_ADIO_GUI\IPython
rm -rf YAV_ADIO_GUI\jsonschema
rm -rf YAV_ADIO_GUI\jsonschema-3.2.0-py2.7.egg-info
rm -rf YAV_ADIO_GUI\nbconvert
rm -rf YAV_ADIO_GUI\nbconvert-5.6.1-py2.7.egg-info
rm -rf YAV_ADIO_GUI\nbformat
rm -rf YAV_ADIO_GUI\notebook
rm -rf YAV_ADIO_GUI\pytz
rm -rf YAV_ADIO_GUI\share
rm -rf YAV_ADIO_GUI\mpl-data\fonts
rm -rf YAV_ADIO_GUI\tcl\encoding
rm -rf YAV_ADIO_GUI\tcl\tzdata
rm -rf YAV_ADIO_GUI\tcl\http1.0
rm -rf YAV_ADIO_GUI\tcl\msgs
rm -rf YAV_ADIO_GUI\tcl\opt0.4
rm -rf YAV_ADIO_GUI\mpl-data\sample_data
rm -rf YAV_ADIO_GUI\tk\images
rm -rf YAV_ADIO_GUI\tk\msgs
7z a -tzip YAV_ADIO_GUI.zip YAV_ADIO_GUI
cd ..
