"""Traffic Cam"""
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from .gui_video_handler import GUIVideo
from .recorder import Recorder


# from PIL import Image, ImageTk
# pylint: disable=too-many-statements, too-many-instance-attributes


class GUIVisual(tk.Frame):  # pylint: disable=too-many-ancestors
    """Handles all visible parts of the GUI"""

    def __init__(self, interface_object, events=None, test_mode=False):
        """

        Args:
            interface_object:
            events:
        """
        if events is None:
            events = {"has_started": None,
                      "run_pipeline": None,
                      "run_gui": None}

        self.master = tk.Toplevel() if test_mode else tk.Tk()
        super().__init__(self.master)
        self.interface = interface_object

        # THREADING
        self.events = events

        # Define global button size
        button_size = [80, 30]

        self.path = ""

        # MAIN WINDOW
        self.master.title("Street Analyser")
        self.master.geometry('1480x940')
        self.master.resizable(False, False)
        self.master.configure(bg='gray')
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        # TITLE
        lable_title = tk.Label(self.master, text="Street Analyser", fg="Black",
                               font="Times 26 bold")
        lable_title.place(x=640 - lable_title.winfo_width() / 2, y=30)
        lable_title.config(bg="gray")

        # LABELS
        self.label_text = tk.StringVar()
        self.label = tk.Label(self.master, textvariable=self.label_text)
        self.label_text.set("None Selected")
        self.label.place(x=40, y=140 + 3 * button_size[1])
        self.label.config(bg="gray")

        self.label_recording = tk.StringVar()
        self.label = tk.Label(self.master, textvariable=self.label_recording)
        self.label_recording.set("Rec. not started")
        self.label.place(x=40, y=390 + 1 * (button_size[1] + 10))
        self.label.config(bg="gray")

        # BUTTONS
        texts = ["Quit", "Save Video", "Start", "Pause", "Stop", "Browse", "Record", "Camera"]
        commands = [self.on_closing, self.b_save_callback, self.b_start_callback,
                    self.b_pause_callback, self.b_stop_callback, self.browse_button,
                    self.b_record, self.b_camera]
        positions = [[40, 380 + 6 * (button_size[1] + 10)], [40, 370 + 3 * (button_size[1] + 10)],
                     [40, 130], [40 + button_size[0] // 2, 130], [40, 130 + button_size[1]],
                     [40, 130 + 2 * button_size[1]], [40, 380 + 2 * (button_size[1] + 10)],
                     [40, 380 - 2 * (button_size[1] + 10)]]
        widths = [button_size[0], button_size[0], button_size[0]//2, button_size[0]//2,
                  button_size[0], button_size[0], button_size[0], button_size[0]]

        for i in range(8):
            button = tk.Button(self.master, text=texts[i], command=commands[i], compound="c")
            button.place(width=widths[i], height=button_size[1], x=positions[i][0],
                         y=positions[i][1])

        # Video CANVAS
        self.canvas_vid = tk.Canvas(self.master, bg="black", height=540, width=960)
        self.canvas_vid.place(x=170, y=100)

        # Description CANVAS 1
        self.canvas_desc = tk.Canvas(self.master, bg="azure3", height=260, width=960)
        self.canvas_desc.place(x=170, y=650)

        # Description CANVAS 2
        self.canvas_desc_2 = tk.Canvas(self.master, bg="gray51", height=810, width=290)
        self.canvas_desc_2.place(x=1140, y=100)

        # Recorder
        self.recorder = Recorder()

        # Test Mode
        self.test_mode = test_mode

        # Video GUI
        params = (self.master, self.canvas_vid,
                  self.canvas_desc, self.canvas_desc_2, self.recorder)
        self.gui = GUIVideo(params, self.interface, self.events)

    def run(self):
        """Run the GUI visuals"""
        if self.test_mode:
            self.b_start_callback()

        else:
            self.mainloop()

    def on_closing(self):
        """Ask if user really wants to close when clicking the X"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.master.destroy()

    # Start the video display by calling GUI_VIDEO method
    def b_start_callback(self):
        '''callback for start button'''
        # self.has_started.acquire()
        if self.path == "":
            messagebox.showwarning(title="Warning",
                                   message="You need to specify a MP4 file to analyse first!")
        else:
            self.interface.command_object.command_info["path"] = self.path
            self.gui.run(self.interface)
            if self.recorder.is_recording:
                self.b_save_callback()

    def browse_button(self):
        '''callback for browse button'''
        filename = filedialog.askopenfile(initialdir="data/", title="Select file", )
        self.path = filename.name
        self.interface.is_image = not self.path.lower().endswith(".mp4")
        self.label_text.set("File Selected")
        return filename

    def b_record(self):
        '''callback for record button'''
        self.recorder.start_recording(self.path)
        self.label_recording.set("Recording...")

    def b_save_callback(self):
        '''callback for save button'''
        self.recorder.save()
        self.label_recording.set("Rec. Saved!")

    def b_camera(self):
        '''callback for start camera button'''
        self.path = 0
        self.b_start_callback()

    def b_pause_callback(self):
        '''callback for stop button'''
        self.events["pause"].set()

    def b_stop_callback(self):
        '''callback for stop button'''
        self.events["stop"].set()
