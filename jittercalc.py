import subprocess
import platform
import tkinter as tk
from tkinter import ttk
import threading
import pkg_resources.py2_warn
from PIL import ImageTk, Image


class MyApplication(tk.Tk):
    """Hello World Main Application"""

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.title("Jitter Calculator")
        # self.iconbitmap('jittercalc.icns')
        #img = ImageTk.PhotoImage(Image.open("jittercalc.icns"))
        #self.iconphoto(True, img)
        #self.call('wm', 'iconphoto', self._w, img)
        #self.geometry("400x300")
        self.resizable(width=False, height=False)
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.fr = FirstFrame(self, bg="White")
        self.fr.grid(padx=5, pady=10, sticky=tk.E + tk.W + tk.N + tk.S)
        self.columnconfigure(0, weight=1)


    def on_exit(self):
        from tkinter import messagebox
        from time import sleep
        """When you click to exit, this function is called"""
        if str(self.fr.stop['state']) != tk.DISABLED:
            messagebox.showinfo(title="Alert",message="First stop the running jobs!")
            return
        self.destroy()

class FirstFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # create the theme and styles
        self.black_white = 'F2.TLabel'
        self.white_black = 'F1.TLabel'
        self.white_green = 'F3.TLabel'
        self.white_red = 'F4.TLabel'
        self.white_black_btn = 'F1.TButton'
        self.white_black_input = 'F1.TEntry'
        self.white_black_spin = 'F1.TSpinbox'
        style = ttk.Style(self)
        style.theme_use('classic')
        style.configure(self.white_black, background='white',
                        font="Lato 12", padding="5", width="18",
                        borderwidth="0", bordercolor="black", relief="groove")
        style.configure(self.black_white, background='black', foreground="white",
                        font="Lato 12 bold", padding="5", width="40",
                        borderwidth="2", bordercolor="white", relief="groove")
        style.configure(self.white_green, background='white', foreground="green",
                        font="Lato 12", padding="5", width="8",
                        borderwidth="2", bordercolor="black", relief="groove")
        style.configure(self.white_red, background='white', foreground="red",
                        font="Lato 12", padding="5", width="8",
                        borderwidth="2", bordercolor="black", relief="groove")
        style.configure(self.white_black_btn, background='white',font="Lato 12 bold")
        style.configure(self.white_black_input, foreground = "black", font="Lato 12 bold")
        style.configure(self.white_black_spin, foreground="black", background="white",font="Lato 12 bold")

        self.input_ip = tk.StringVar()
        self.input_ip.set('192.168.1.1')
        self.external = tk.StringVar()
        self.external.set('google.com')
        self.jitters = []
        self.jitters2 = []
        self.threads = []
        self.cont = True
        self.frame_details()


    def frame_details(self):
        # gateway
        lbl_iphost = ttk.Label(self, text="Gateway IP", style=self.white_black)
        lbl_iphost.grid(row=0, column=1, sticky=tk.W)
        ent_iphost = ttk.Entry(self, style=self.white_black_input, textvariable=self.input_ip)
        ent_iphost.grid(row=0, column=2, sticky=tk.W)
        # external ip host
        lbl_ext = ttk.Label(self, text="External Hostname", style=self.white_black)
        lbl_ext.grid(row=1, column=1, sticky=tk.W)
        ent_ext = ttk.Entry(self, style=self.white_black_input, textvariable=self.external)
        ent_ext.grid(row=1, column=2, sticky=tk.W)

        self.buttonframe = tk.Frame(self)
        self.buttonframe.grid(padx=0, pady=5, row=2, column=1, sticky=tk.W)
        self.calc = ttk.Button(self.buttonframe, text="Start", style=self.white_black_btn, command=self.calc_jitter_threads)
        self.calc.grid(padx=5, row=0, column=1, sticky=tk.W)
        self.stop = ttk.Button(self.buttonframe, text="Stop", style=self.white_black_btn, command=self.stop_calc, state='disabled')
        self.stop.grid(row=0, column=3, sticky=tk.W)

        self.canvas = tk.Canvas(self, width=800, height=500, bg='white')
        self.canvas.grid(row=3, column=0, columnspan=4, sticky=tk.W)
        # self.img = ImageTk.PhotoImage(Image.open('test.jpg'))
        self.jitter_plot()


    def jitter_plot(self):
        self.img = self.img = ImageTk.PhotoImage(self.get_image())
        self.canvas.create_image((10, 10), anchor=tk.NW, image=self.img)

    def cleanup_memory(self):
        if len(self.jitters) >= 100:
            self.jitters = self.jitters[-50:]
        if len(self.jitters2) >= 100:
            self.jitters2 = self.jitters2[-50:]

    def get_image(self):
        from matplotlib import pyplot as plt
        from io import BytesIO
        from PIL import Image
        import matplotlib
        matplotlib.use('Agg')

        self.cleanup_memory()
        # create a line chart, years on x-axis, gdp on y-axis
        plt.figure(figsize=(8.4, 4.8))
        plt.plot(self.jitters[-50:], color='green', marker='o', linestyle='solid', label='gateway')
        plt.plot(self.jitters2[-50:], color='red', marker='o', linestyle='solid', label='external')
        # add a title
        plt.legend()
        plt.title("Jitter Graph")

        # add a label to the y-axis
        plt.ylabel("Jitter Value (ms)")
        buffer = BytesIO()
        plt.savefig(buffer, format='jpg')
        buffer.seek(0)
        plt.close()
        return Image.open(buffer)

    def stop_calc(self):
        self.cont = False

    def calc_jitter_threads(self):
        self.cont = True
        self.thread1 = threading.Thread(target=self.calc_jitter, args=(), kwargs={'ip':self.input_ip.get(),'gateway':True})
        self.thread1.start()
        self.threads.append(self.thread1)
        self.thread2 = threading.Thread(target=self.calc_jitter, args=(), kwargs={'ip': self.external.get(), 'gateway':False})
        self.thread2.start()
        self.threads.append(self.thread2)
        self.calc['state'] = 'disabled'
        self.stop['state'] = 'normal'


    def calc_jitter(self, ip: str, gateway: bool):
        from decimal import Decimal
        from time import sleep
        while self.cont:
            results = self.ping_results(ip)
            total = 0
            for i in range(len(results[:-1])):
                diff = abs(Decimal(results[i+1])-Decimal(results[i]))
                total += diff
            if results == []:
                jitter = -10
                sleep(5)
            else:
                jitter = total/len(results)
            print("IP/Host: {} Jitter: {}".format(ip, jitter))
            if gateway:
                self.jitters.append(jitter)
            else:
                self.jitters2.append(jitter)
                self.jitter_plot()

        print("Stopped...")
        self.calc['state'] = 'normal'
        self.stop['state'] = 'disabled'


    def ping_results(self,ip: str) -> []:
        import re


        count = 5
        if platform.system() == 'Windows':
            count_parameter = '-n'
            start = 2
            regex_text = "(?<=time=)(\d)"
        else:
            count_parameter = '-c'
            start = 1
            regex_text = "(?<=time=)(\w+.\w+)"
        ping_result = subprocess.run(['ping', ip, count_parameter, str(count)],
                                     stdout=subprocess.PIPE).stdout.decode('utf-8')

        lines = ping_result.split('\n')

        try:
            times = [re.findall(regex_text,x)[0] for x in lines[start:count+1]]
        except:
            times = []
        return times


myapp = MyApplication()
myapp.mainloop()

# TO-DO on exit stop all running threads