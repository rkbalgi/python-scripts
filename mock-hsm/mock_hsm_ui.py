import Tkinter
from Tkinter import Menu
import tkMessageBox as tk_msg_box
import tkSimpleDialog as tk_simple_dialog
import tkFont
import hsm_listener

hsm_started = 0
hsm_port = 0
hsm_listener_thread = None


class MockHsmUi:
    def __init__(self):
        print 'using tk version -' + str(Tkinter.TkVersion)
        self.top = Tkinter.Tk()
        self.top.configure(width=600, height=400)
        self.font = tkFont.Font(family='Calibri', size=10);

        self.init_components()

    def init_components(self):
        menu_bar = Menu(self.top, font=self.font)

        self.top.configure(menu=menu_bar)
        # self.top.attributes('-fullscreen', True)
        self.top.geometry('{0}x{1}+0+0'.format(self.top.winfo_screenwidth() - 200, self.top.winfo_screenheight() - 200))

        file_menu = Menu(menu_bar, tearoff=0, font=self.font)

        file_menu.add_command(label="Start Hsm", command=self.start_hsm)
        file_menu.add_command(label="Stop Hsm", command=self.stop_hsm)

        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit)

        menu_bar.add_cascade(label="File", menu=file_menu, font=self.font)

    def show(self):
        self.top.mainloop()

    def start_hsm(self):
        global hsm_started

        if hsm_started == 1:

            tk_msg_box.showerror('Error', 'Hsm already running.', parent=self.top)
            return
        else:
            global hsm_port
            hsm_port = tk_simple_dialog.askinteger('Supply Hsm Port', 'Port', parent=self.top)
            print 'hsm port =', hsm_port
            hsm_started = 1
            global hsm_listener_thread
            hsm_listener_thread = hsm_listener.HsmListenerThread(hsm_port)
            hsm_listener_thread.start()

    def stop_hsm(self):
        global hsm_started, hsm_listener_thread
        hsm_started = 0
        hsm_listener_thread.stop_hsm()

        return

    def exit(self):
        self.top.destroy()
        self.top.quit()
        quit()
