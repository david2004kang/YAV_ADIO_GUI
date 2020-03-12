#!"C:\Python27\python.exe"
# -*- coding: utf-8 -*-
from Tkinter import *
from logging_define import *
import threading
import psutil
import glob
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import ctypes

__author__ = 'David Kang'
import numpy as np
from Tkinter import *
import matplotlib.pyplot as plt


class ADIO_dll_wrapper:
    _ADIO_path = os.getcwd() + "\\ADIO64.dll"
    _LENGHT = 64
    output_data = [0 for x in range(_LENGHT)]
    value_1 = 0.0
    value_2 = 0.0

    @logger
    def __init__(self):
        self._thread_handler = threading
        self.testing_thread = threading.Thread(target=self.thread_run_task)
        self.testing_thread.setDaemon(True)
        self.testing_thread.start()

    @logger
    def __iter__(self):
        return self.output_data

    @logger
    def thread_run_task(self):
        logging.debug("loading ADIO64.dll...")
        _kernel32 = ctypes.WinDLL('kernel32')
        _kernel32.LoadLibraryW.restype = ctypes.c_void_p
        _dll_handler = _kernel32.LoadLibraryW(unicode(self._ADIO_path))
        _my_dll = ctypes.WinDLL(self._ADIO_path, handle=_dll_handler)
        adb_buffer = (ctypes.c_uint32 * 4096)()
        yav_param = (ctypes.c_int * 10)()
        cnt_buffer = (ctypes.c_int * 2)()
        dio_buffer = (ctypes.c_int * 2)()
        num = ctypes.c_uint32()
        num.value = self._LENGHT

        while True:
            _return = _my_dll.GetYavData(0, adb_buffer, num, yav_param, cnt_buffer, dio_buffer)
            if _return > 0:
                _temp_list = [adb_buffer[index] for index in xrange(len(self.output_data))]
                _temp1_list = _temp_list[::2]
                self.value_1 = sum(_temp1_list) / len(_temp1_list)
                _temp2_list = _temp_list[1::2]
                self.value_2 = sum(_temp2_list) / len(_temp2_list)


class YAV_ADIO_GUI:
    _VERSION = '1.1.0.2020_03_10'
    _WIDTH = 800
    _HEIGHT = 700
    _data_source = None

    @logger
    def __init__(self):
        self._data_source = ADIO_dll_wrapper()
        self.root = Tk()
        _ico_list = glob.glob(os.getcwd() + "\\*.ico")
        if len(_ico_list) > 0:
            self.root.iconbitmap(_ico_list[0])
        self.root.title("YAV ADIO data displayer (GUI) " + self._VERSION)
        frame1 = Frame(self.root, height=20)
        frame1.pack(side=TOP, padx=5, pady=5, fill=X)
        self.l1 = Label(frame1, text="Voltage: 0 V, Current: 0 A")
        self.l1.config(font=("Courier", 14))
        self.l1.pack(side=LEFT, pady=5, padx=5)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.fig_time_array = np.arange(100)
        self.fig_voltage1_array = np.sin(self.fig_time_array * 2.7 * np.pi) + 20
        self.fig_voltage2_array = np.cos(self.fig_time_array * 1.3 * np.pi) + 17
        self.subplot1 = self.fig.add_subplot(211)
        self.subplot1.set_xlabel("time(Sec.)")
        self.subplot1.set_ylabel("voltage(V)")
        self.subplot1.text(10, 10, "Vol1:{} V \nVol2:{} V".format(self.fig_voltage1_array[-1],
                                                                  self.fig_voltage2_array[-1]))
        self.subplot1.plot(self.fig_time_array, self.fig_voltage1_array, label="voltage 1")
        self.subplot1.plot(self.fig_time_array, self.fig_voltage2_array, color='red',
                           linewidth=1.0, linestyle='--', label="voltage 2")
        self.subplot2 = self.fig.add_subplot(212, sharex=self.subplot1)
        self.subplot2.set_xlabel("time(Sec.)")
        self.subplot2.set_ylabel("current(A)")
        self.subplot2.plot(self.fig_time_array, self.fig_voltage1_array)
        self.fig.legend()

        canvas = FigureCanvasTkAgg(self.fig, master=self.root)  # A tk.DrawingArea.
        self.ani = animation.FuncAnimation(self.fig, self.animate, interval=1000)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, self.root)
        toolbar.update()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        logging.debug("width: {}, height: {}".format(self._WIDTH, self._HEIGHT))
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.resizable(0, 0)
        size = "{}x{}+{}+{}".format(self._WIDTH, self._HEIGHT,
                                    (self.root.winfo_screenwidth() - self._WIDTH) / 2,
                                    (self.root.winfo_screenheight() - self._HEIGHT) / 2 - 20)
        logging.debug(size)
        self.root.geometry(size)

        mainloop()

    @staticmethod
    def array_pop_push(array, value=20):
        _temp_list = list(array)
        del _temp_list[0]
        _temp_list.append(value)
        return np.array(_temp_list)

    def animate(self, _index):
        if self._data_source is None:
            return
        _temp_val1 = self._data_source.value_1
        _temp_val2 = self._data_source.value_2
        self.fig_time_array = self.array_pop_push(self.fig_time_array, self.fig_time_array[-1] + 1)
        self.fig_voltage1_array = self.array_pop_push(self.fig_voltage1_array, _temp_val1 * 50.0 / 4096)
        self.fig_voltage2_array = self.array_pop_push(self.fig_voltage2_array, _temp_val2 * 50.0 / 4096)
        self.l1['text'] = "Voltage: {} V, Current: {} A".format(
            _temp_val1 * 50.0 / 4096, abs(_temp_val1 - _temp_val2) * 5000.0 / 4096
        )

        self.subplot2.clear()
        self.subplot1.clear()
        self.subplot2.plot(self.fig_time_array, self.fig_voltage1_array)
        self.subplot1.plot(self.fig_time_array, self.fig_voltage1_array, label="voltage 1")
        self.subplot1.plot(self.fig_time_array, self.fig_voltage2_array, color='red',
                           linewidth=1.0, linestyle='--', label="voltage 2")


if __name__ == "__main__":
    logging.debug("YAV_ADIO_GUI executed")

    process_counter = 0
    process_name = psutil.Process(os.getpid()).name()
    for _process in psutil.process_iter():
        try:
            if process_name.lower() in _process.name().lower():
                process_counter += 1
                if process_counter >= 2:
                    sys.exit()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    try:
        gui_handle = YAV_ADIO_GUI()
    except Exception as E:
        logging.exception(E)

