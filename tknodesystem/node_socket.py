import tkinter

class NodeSocket:
    def __init__(self, canvas, radius=10, center=(50,50), value=0, border_color='white',
                 border_width=1, fg_color='green', hover_color='red', hover=True, socket_num=None):

        self.canvas = canvas
        self.radius = radius
        self.center = center
        self.value = value
        self.fg_color = fg_color
        self.hover_color = hover_color
        self.hover = hover
        self.hover_message = False
        self.live_connection = False
        
        self.create(border_color, border_width, self.fg_color)
        self.canvas.socket_num +=1
        if socket_num:
            self.socket_num = socket_num
            self.canvas.socket_num = socket_num
        else:
            self.socket_num = self.canvas.socket_num
  
        self.msg = tkinter.StringVar()
        self.hover_text = tkinter.Message(self.canvas, textvariable=self.msg, aspect=1000,
                                          highlightthickness=0, borderwidth=0, bg="grey20", fg="white")
        
        self.update()
        
    def create(self, border_color, border_width, connecter_color):
        """ create a circle which will act as a node socket """
        
        self.ID = self.canvas.create_oval(
            (self.center[0]-self.radius, self.center[1]-self.radius),
            (self.center[0]+self.radius, self.center[1]+self.radius),
            outline=border_color, width=border_width, fill=connecter_color)
        
        self.canvas.tag_bind(self.ID, '<Enter>', self.enter_socket)
        self.canvas.tag_bind(self.ID, '<Leave>', self.leave_socket)
        
    def update(self):
        """ update the coordinates of socket """
        try:
            self.cords = self.canvas.coords(self.ID)
            self.center = (self.cords[0]+self.cords[2])/2, (self.cords[1]+self.cords[3])/2
        except: None
        
    def enter_socket(self, event):
        if self.hover: self.canvas.itemconfigure(self.ID, fill=self.hover_color)
        if self.hover_message:
            x_pos = self.cords[0]-self.hover_text.winfo_reqwidth()-3
            y_pos = self.center[1]-self.hover_text.winfo_reqheight()/2
            self.hover_text.place(x=x_pos, y=y_pos)
            
    def leave_socket(self, event):
        if self.hover: self.canvas.itemconfigure(self.ID, fill=self.fg_color)
        if self.hover_message: self.hover_text.place_forget()
            
    def hide(self):
        self.canvas.itemconfigure(self.ID, state="hidden")
        
    def show(self):
        self.canvas.itemconfigure(self.ID, state="normal")

    def connect_wire(self):
        """ make a dummy wire """
        if self.live_connection: return
      
        self.x1, self.y1 = self.center
        self.x2, self.y2 = self.center
        self.wire_exist = True
        self.wireID = self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, dash=self.canvas.dash,
                                              width=self.canvas.wire_width, fill=self.canvas.wire_color)
        self.canvas.tag_lower(self.wireID)
        self.canvas.tag_lower(self.canvas.grid_bg)
        self.canvas.tag_bind(self.ID, "<ButtonPress>", lambda e: self.mouse_move(), add="+")
        self.canvas.tag_bind(self.wireID, "<Button-1>", lambda e: self.delete_wire(), add="+")
        if self.canvas.connect_wire: self.mouse_move()
        
    def delete_wire(self):
        """ delete the dummy wire """
        self.canvas.delete(self.wireID)
        self.wire_exist = False
        self.live_connection = False
        
    def mouse_move(self):
        """ connect the dummy wire with mouse """
        if self.ID not in self.canvas.find_all():
            self.delete_wire()
        self.canvas.connect_wire = False
        if (self.x1, self.y1)!=self.center:
            self.delete_wire()
        x = self.canvas.master.winfo_pointerx()
        y = self.canvas.master.winfo_pointery()
        abs_coord_x = self.canvas.master.winfo_pointerx() - self.canvas.winfo_rootx()
        abs_coord_y = self.canvas.master.winfo_pointery() - self.canvas.winfo_rooty()
        
        self.canvas.coords(self.wireID, self.x1, self.y1, abs_coord_x, abs_coord_y)
        if self.wire_exist:
            self.canvas.after(50, self.mouse_move)
            self.live_connection = True
        else:
            self.live_connection = False
            self.canvas.connect_wire = True
    
    def configure(self, **kwargs):
        """ configure options """
        
        if "fg_color" in kwargs:
            self.fg_color = kwargs.pop("fg_color")
            self.canvas.itemconfig(self.ID, fill=self.fg_color)
        if "hover_color" in kwargs:
            self.hover_color = kwargs.pop("hover_color")
        if "hover" in kwargs:
            self.hover = kwargs.pop("hover")
            
        if len(kwargs)>0:
            raise ValueError("This option is not configurable:" + list(kwargs.keys())[0])
        
