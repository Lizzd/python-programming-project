"""Class to display video inside GUI canvas"""

import time
import tkinter as tk
import PIL.Image
import PIL.ImageTk
import cv2


# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
# pylint: disable=too-many-instance-attributes

class GUIVideo:
    """handles the video display inside gui canvas"""

    def set_params(self, bottom_window):
        """Set all live parameters visually"""

        com = self.interface.command_object

        self.checkboxes = []
        self.texts = {"classifier_model": com.classifier,
                      "apply_ocr": com.ocr_and_trans, "show_src_string": com.ocr_and_trans,
                      "show_trans": com.ocr_and_trans, "continues_mode": com.logic,
                      "bounding_box": com.visualizer, "show_strings": com.visualizer}
        keys = self.texts.keys()

        # Create 8 checkboxes for boolean parameters and save var in list
        for i, text in enumerate(keys):
            check = tk.IntVar(value=0)
            box = tk.Checkbutton(bottom_window, text=text,
                                 variable=check, onvalue=1, anchor=tk.W,
                                 offvalue=0, height=5, width=20, bg="azure2", selectcolor="white",
                                 font=("Arial", 10))
            if i % 2 == 0:
                box.place(x=480, y=10 + i // 2 * 53)
            else:
                box.place(x=480 + 200, y=10 + i // 2 * 53)
            self.checkboxes.append(check)

        # Create 4 sliders for params
        ranges = [[0, 2], [1, 5], [0, 4], [1, 5]]
        start_values = [0, 1, 1, 1]
        self.sliders = []
        for i in range(4):
            var = tk.IntVar(value=start_values[i])
            tk.Scale(bottom_window, from_=ranges[i][0], to=ranges[i][1], variable=var,
                     bg="white").place(x=50 + 100*i, y=75)
            self.sliders.append(var)

        # Name sliders
        texts = ["preprocessor", "max_class", "frame_index", "nr_of_patches"]

        for i in range(4):
            tk.Label(bottom_window, text=[texts[i]], bg="white",
                     foreground="black", font=("Arial", 10)).place(x=30 + i * 100, y=40)

    def __init__(self, params, interface, events=None):
        if events is None:
            events = {"has_started": None,
                      "run_pipeline": None,
                      "run_gui": None}
        window, canvas, bottom_window, right_window, recorder = params
        self.window = window
        self.bottom_window = bottom_window
        self.right_window = right_window
        self.recorder = recorder
        self.pillow_patch_list = []

        if interface.is_image is False:
            self.delay = 15

        self.canvas = canvas
        self.photo = 0

        self.interface = interface
        self.set_params(bottom_window)

        # Threading
        self.events = events

    def run(self, interface):
        """Is called to start the Video"""
        self.events["has_started"].set()
        self.update_command_object()
        if self.interface.is_image is False:

            while self.events["has_started"].is_set() and not self.events["pause"].is_set():
                self.events["run_pipeline"].set()
                self.events["run_gui"].wait(4)
                self.update(interface)
                self.events["run_gui"].clear()
            if self.events["pause"].is_set():
                self.events["pause"].clear()

        else:
            self.events["run_pipeline"].set()
            self.events["run_gui"].wait()
            self.update(interface)
            self.events["run_gui"].clear()

    def update(self, interface):
        """Get a frame from the video source"""
        self.update_command_object()

        frame = interface.visualization_object.final_annotated_frame

        # Resize image to canvas size
        res = cv2.resize(frame, (960, 540))

        # Check if recording
        if self.recorder.is_recording:
            self.recorder.write(res)

        # Display frame
        res = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(res))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        # Call and display trafficsigns with descriptions etc. from visualizer
        list_of_patches = self.interface.visualization_object.get_patches_and_icons()
        self.pillow_patch_list = []
        for i, arr in enumerate(list_of_patches):
            icon_size = 125
            arr = cv2.resize(arr, (2 * icon_size, icon_size))
            img = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(arr))
            self.pillow_patch_list.append(img)
            self.right_window.create_image(icon_size + 25, (icon_size + 5) * i
                                           + icon_size // 2 + 25, image=self.pillow_patch_list[i])

        # Update Window
        self.window.update_idletasks()
        self.window.update()

        if self.interface.is_image is True:
            time.sleep(2)

    def update_command_object(self):
        """
        update command object
        Returns:

        """
        keys = self.texts.keys()

        for i, current in enumerate(keys):
            self.texts[current][current] = self.checkboxes[i].get()
        com = self.interface.command_object
        com.preprocessor["features_extractor"] = self.sliders[0].get()
        com.classifier["max_class"] = self.sliders[1].get()
        com.visualizer["index_of_frame_dict"] = self.sliders[2].get()
        com.visualizer["nr_of_patches"] = self.sliders[3].get()
