# Author: Akash Bora (Akascape)
# License: MIT

import customtkinter
import tkinter
from typing import Union, Callable

class CTkSpinbox(customtkinter.CTkFrame):
         
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 number_of_steps: int = 1,
                 from_: int = 0,
                 to: int = 1000,
                 value: int = None,
                 button_color: str = None,
                 button_width: int = 25,
                 button_hover_color: str = None,
                 entry_color: str = None,
                 text_color: str = None,
                 border_color: str = None,
                 command: Callable = None,
                 border_width: int = 0,
                 corner_radius: int = 5,
                 font = None,
                 **kwargs):
        
        super().__init__(*args, height=height, **kwargs)
        
        self.step_size = number_of_steps
        self.max_value = to
        self.min_value = from_
        self.command = command
        self.validation = self.register(self.only_numbers)
        self.value = value
        
        self.grid_columnconfigure((0, 2), weight=0) 
        self.grid_columnconfigure(1, weight=1)
        
        self.button_color = customtkinter.ThemeManager.theme["CTkButton"]["fg_color"] if button_color is None else button_color
        self.button_hover = customtkinter.ThemeManager.theme["CTkButton"]["hover_color"] if button_hover_color is None else button_hover_color
        self.entry_color = customtkinter.ThemeManager.theme["CTkEntry"]["fg_color"] if entry_color is None else entry_color
        self.border_color = customtkinter.ThemeManager.theme["CTkEntry"]["border_color"] if border_color is None else border_color
        self.text_color = customtkinter.ThemeManager.theme["CTkEntry"]["text_color"] if text_color is None else text_color
        self.border_width = border_width
        self.corner_radius = corner_radius
        self.button_width = button_width
        self.font = font
        
        super().configure(border_color=self.border_color)

        self.subtract_button = customtkinter.CTkButton(self, text="-", width=self.button_width, height=height-6, corner_radius=self.corner_radius,
                                                       border_color=self.border_color, text_color=self.text_color, font=self.font,
                                                       command=self.subtract_button_callback, fg_color=self.button_color,
                                                       hover_color=self.button_hover, border_width=self.border_width)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)
    
        self.text = tkinter.StringVar()
        self.text.set(self.min_value)

        self.entry = customtkinter.CTkEntry(self, width=width, height=height-6, textvariable=self.text, font=self.font,
                                            fg_color=self.entry_color, border_width=self.border_width+2,
                                            placeholder_text=str(self.min_value), justify="center", validate='key',
                                            border_color=self.border_color, corner_radius=self.corner_radius,
                                            validatecommand=(self.validation, '%P'), text_color=self.text_color)       
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = customtkinter.CTkButton(self, text="+", width=self.button_width, height=height-6, corner_radius=self.corner_radius,
                                                  border_color=self.border_color, text_color=self.text_color, font=self.font,
                                                  command=self.add_button_callback, fg_color=self.button_color,
                                                  hover_color=self.button_hover, border_width=self.border_width)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)
        self.entry.bind("<MouseWheel>", self.on_mouse_wheel)

        if self.value is None:
            self.set(self.min_value)
        else:
            self.set(self.value)
            
    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.add_button_callback()
        else:
            self.subtract_button_callback()
            
    def add_button_callback(self):
        if self.entry.get()=="":
            self.set(0)
            return
        
        self.set(int(self.entry.get()) + self.step_size)

        if self.command is not None:
            self.command()
            
    def subtract_button_callback(self):
        if self.entry.get()=="":
            self.set(0)
            return
        
        self.set(int(self.entry.get()) - self.step_size)

        if self.command is not None:
            self.command()
            
    def configure(self, **kwargs):
        
        if "state" in kwargs:
            if kwargs["state"]=="disabled":
                self.entry.unbind("<MouseWheel>")
            else:
                self.entry.bind("<MouseWheel>", self.on_mouse_wheel)
            super().configure(state=kwargs["state"])
            
        if "width" in kwargs:
            self.entry.configure(width=kwargs.pop("width"))
        if "fg_color" in kwargs:
            super().configure(fg_color=kwargs.pop("fg_color"))
        if "corner_radius" in kwargs:
            self.corner_radius = kwargs["corner_radius"]
        if "border_width" in kwargs:
            self.border_width = kwargs.pop("border_width")
            self.entry.configure(border_width=self.border_width+2)
            self.add_button.configure(border_width=self.border_width)
            self.subtract_button.configure(border_width=self.border_width)
        if "button_width" in kwargs:
            self.button_width = kwargs.pop("button_width")
            self.add_button.configure(width=self.button_width)
            self.subtract_button.configure(width=self.button_width)
        if "border_color" in kwargs:
            self.border_color = kwargs["border_color"]
        if "button_color" in kwargs:
            self.button_color = kwargs.pop("button_color")
            self.add_button.configure(fg_color=self.button_color)
            self.subtract_button.configure(fg_color=self.button_color)
        if "button_hover_color" in kwargs:
            self.button_hover = kwargs.pop("button_hover_color")
            self.add_button.configure(hover_color=self.button_hover)
            self.subtract_button.configure(hover_color=self.button_hover)
        if "entry_color" in kwargs:
            self.entry_color = kwargs.pop("entry_color")
            self.entry.configure(fg_color=self.entry_color)
        if "text_color" in kwargs:
            self.text_color = kwargs["text_color"]
        if "value" in kwargs:
            self.values = kwargs.pop("value")
            self.set(self.values)
        if "from_" in kwargs:
            self.min_value = kwargs.pop("from_")
            if int(self.value)<self.min_value:
                self.set(self.min_value)
        if "to" in kwargs:
            self.max_value = kwargs.pop("to")
            if int(self.value)>self.max_value:
                self.set(self.max_value)
        if "number_of_steps" in kwargs:
            self.step_size = kwargs.pop("number_of_steps")
        if "command" in kwargs:
            self.command = kwargs.pop("command")
        if "font" in kwargs:
            self.font = kwargs["font"]
            
        self.entry.configure(**kwargs)
        self.add_button.configure(**kwargs)
        self.subtract_button.configure(**kwargs)
        
    def cget(self, param):
        if param=="width":
            return self.entry.winfo_width()
        if param=="height":
            return super().winfo_height()
        if param=="corner_radius":
            return self.corner_radius 
        if param=="border_width":
            return self.border_width
        if param=="button_width":
            return self.button_width
        if param=="border_color":
            return self.border_color 
        if param=="button_color":
            return self.button_color
        if param=="button_hover_color":
            return self.button_hover 
        if param=="entry_color":
            return self.entry_color
        if param=="text_color":
            return self.text_color 
        if param=="value":
            return int(self.entry.get())
        if param=="from_":
            return self.min_value
        if param=="to":
            return self.max_value
        if param=="number_of_steps":
            return self.step_size
        if param=="font":
            return self.font
        return super().cget(param)
        
    def only_numbers(self, char):
        if (char.isdigit() or (char=="")):
            if (len(str(self.max_value))-1)==str(self.max_value).count("0"):
                if (len(char)<=len(str(self.max_value))-1) or int(char)==self.max_value:
                    return True
                else:
                    return False
            else:
                if (len(char)<=len(str(self.max_value))):
                    return True
                else:
                    return False
        else:
            return False
        
    def get(self) -> Union[int, None]:
        if self.entry.get()=="":
            return 0
        try:
            return int(self.text.get())
        except ValueError:
            return None

    def set(self, value: int):
        if int(value)>self.max_value:
            self.set(self.max_value)
            return
        if int(value)<self.min_value:
            self.set(self.min_value)
            return

        if str(value).isdigit():
            self.text.set(int(value))
            
        self.text.set(int(value))
        self.value = value

    def bind(self, sequence=None, command=None, add="+"):
        super().bind(sequence, command, add)
        self.entry.bind(sequence, command, add)
        self.add_button.bind(sequence, command, add)
        self.subtract_button.bind(sequence, command, add)
        
    def unbind(self, sequence=None):
        super().unbind(sequence)
        self.entry.unbind(sequence)
        self.add_button.unbind(sequence)
        self.subtract_button.unbind(sequence)
        
