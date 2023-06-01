import customtkinter
import sys
import time

customtkinter.set_appearance_mode("Dark") 

class NodeMenu(customtkinter.CTkToplevel):
    
    def __init__(self, attach, button_color=None, height: int = 300, width: int = 250, text_color=None,
                 fg_color=None, button_height: int = 30, justify="center", scrollbar_button_color=None,
                 scrollbar=True, scrollbar_button_hover_color=None, frame_border_width=2,
                 command=None, alpha: float = 0.97, frame_corner_radius=20, label="Search Nodes", 
                 resize=True, border_color=None, **kwargs):
        
        super().__init__(takefocus=1)
        
        self.focus()
        self.alpha = alpha
        self.attributes('-alpha', 0)
        self.corner = frame_corner_radius

        self.attach = attach
        self.height = height
        self.width = width
        self.command = command
        self.fade = False
        self.resize = resize
        self.button_num = 0
        self.node = {}
        self.padding = 0
        self.focus_something = False
        
        self.withdraw()
        if sys.platform.startswith("win"):
            self.overrideredirect(True)
            self.transparent_color = self._apply_appearance_mode(self._fg_color)
            self.attributes("-transparentcolor", self.transparent_color)
            self.attach.bind("<Double-Button-3>", self.popup, add="+")
            self.bind("<FocusOut>", lambda e: self._withdraw())
        elif sys.platform.startswith("darwin"):
            self.overrideredirect(True)
            self.transparent_color = 'systemTransparent'
            self.attributes("-transparent", True)
            self.transient(self.master)
            self.attach.bind("<Button-1>", lambda e: self._withdraw(), add="+")
            self.attach.bind("<Double-Button-2>", self.popup, add="+")
            self.focus_something = True
        else:
            self.attributes("-type", "splash")
            self.transparent_color = '#000001'
            self.corner = 0
            self.padding = 20
            self.attach.bind("<Double-Button-3>", self.popup, add="+")
            self.bind("<FocusOut>", lambda e: self._withdraw())

        self.fg_color = customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"] if fg_color is None else fg_color
        self.scroll_button_color = customtkinter.ThemeManager.theme["CTkScrollbar"]["button_color"] if scrollbar_button_color is None else scrollbar_button_color
        self.scroll_hover_color = customtkinter.ThemeManager.theme["CTkScrollbar"]["button_hover_color"] if scrollbar_button_hover_color is None else scrollbar_button_hover_color
        self.border_color = customtkinter.ThemeManager.theme["CTkFrame"]["border_color"] if border_color is None else border_color
        self.button_color = customtkinter.ThemeManager.theme["CTkFrame"]["top_fg_color"] if button_color is None else button_color
        self.text_color = customtkinter.ThemeManager.theme["CTkLabel"]["text_color"] if text_color is None else text_color
        
        if scrollbar is False:
            self.scroll_button_color = self.fg_color
            self.scroll_hover_color = self.fg_color

        self.frame_top = customtkinter.CTkFrame(self, bg_color=self.transparent_color, fg_color=self.fg_color,
                                  corner_radius=self.corner, border_width=frame_border_width,
                                  border_color=self.border_color)
        
        self.frame_top.pack(expand=True, fill="both")

        self.var = customtkinter.StringVar()
        self.var.trace_add('write', self.search)
        
        self.label = customtkinter.CTkLabel(self.frame_top, text=label)
        self.label.pack(fill="x", pady=10, padx=20)
        
        self.search_entry = customtkinter.CTkEntry(self.frame_top, fg_color=self.button_color, border_color=self.border_color,
                                     textvariable=self.var, **kwargs)
        
        self.search_entry.pack(fill="x", pady=0, padx=20)
        self.search_entry.bind("<FocusIn>", lambda e: self.attach.unbind_all("<space>"))
        
        self.frame = customtkinter.CTkScrollableFrame(self.frame_top, fg_color=self.fg_color,
                                        scrollbar_button_hover_color=self.scroll_hover_color,
                                        corner_radius=self.corner, scrollbar_button_color=self.scroll_button_color,)
        
        self.frame._scrollbar.grid_configure(padx=3)
        
        if self.padding:
            frame_padding = 10
        else:
            frame_padding = (0,6)
            
        self.frame.pack(expand=True, fill="both", padx=8, pady=frame_padding)
        self.no_match = customtkinter.CTkLabel(self.frame, text="No Match")
        
        if justify.lower()=="left":
            self.justify = "w"
        elif justify.lower()=="right":
            self.justify = "e"
        else:
            self.justify = "c"
            
        self.button_height = button_height
        
        self.resizable(width=False, height=False)
        self.disable = False
    
        self.attach.bind_all("<space>", self.popup)
        
        self.update_idletasks()
        self.attach.focus_set()

    def _withdraw(self):
        if not self.disable:
            self.withdraw() 
            self.attach.bind_all("<space>", self.popup)
            
    def fade_out(self):
        for i in range(100,0,-10):
            if not self.winfo_exists():
                break
            self.attributes("-alpha", i/100)
            self.update()
            time.sleep(1/100)
            
    def fade_in(self):
        for i in range(0,100,10):
            if not self.winfo_exists():
                break
            self.attributes("-alpha", i/100)
            self.update()
            time.sleep(1/100)
            
    def search(self, a,b,c):
        self.live_update(self.var.get())
        
    def add_node(self, label, command, **button_kwargs):                         
        self.node[self.button_num] = customtkinter.CTkButton(self.frame,
                                                             text=label,
                                                             text_color=self.text_color,
                                                             height=self.button_height,
                                                             fg_color=self.button_color,
                                                             anchor=self.justify, 
                                                             command=lambda: self._attach_key_press(command), **button_kwargs)
        self.node[self.button_num].pack(fill="x", pady=5, padx=(self.padding,0))
        self.button_num +=1

    def destroy_popup(self):
        self.destroy()
        self.disable = True

    def place_dropdown(self, x=None, y=None):
        self.geometry('{}x{}+{}+{}'.format(self.width, self.height, x, y))
        self.fade_in()
        self.attributes('-alpha', self.alpha)
        
    def _iconify(self, x=None, y=None):
        self.focus_set()
        self._deiconify()
        if self.focus_something: self.node[0].focus_set()
        self.search_entry.focus_set()
        self.place_dropdown(x,y)

    def _attach_key_press(self, command):
        self.fade_out()
        self.withdraw()
        command()
        
    def live_update(self, string=None):
        if self.disable: return
        if self.fade: return
        if string:
            i=1
            for key in self.node.keys():
                s = self.node[key].cget("text").lower()
                if not s.startswith(string.lower()):
                    self.node[key].pack_forget()
                else:
                    self.node[key].pack(fill="x", pady=5, padx=(self.padding,0))
                    i+=1
                    
            if i==1:
                self.no_match.pack(fill="x", pady=2, padx=(self.padding,0))
            else:
                self.no_match.pack_forget()
            self.button_num = i
            
        else:
            self.no_match.pack_forget()
            for key in self.node.keys():
                self.node[key].pack(fill="x", pady=5, padx=(self.padding,0))
        self.frame._parent_canvas.yview_moveto(0.0)
        
    def _deiconify(self):
        if self.button_num>0:
            self.deiconify()
        
    def popup(self, event):
        if self.disable: return
        self._iconify(event.x_root, event.y_root)
        
    def configure(self, **kwargs):
        if "height" in kwargs:
            self.height = kwargs.pop("height")
            
        if "alpha" in kwargs:
            self.alpha = kwargs.pop("alpha")
            
        if "width" in kwargs:
            self.width = kwargs.pop("width")
            
        if "fg_color" in kwargs:
            self.frame.configure(fg_color=kwargs.pop("fg_color"))
                    
        if "button_color" in kwargs:
            for key in self.node.keys():
                self.node[key].configure(fg_color=kwargs.pop("button_color"))
                
        for key in self.node.keys():
            self.node[key].configure(**kwargs)
