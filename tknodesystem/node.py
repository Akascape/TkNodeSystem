class Node:
    def __init__(self, canvas, width=50, height=50, border_color='white', border_width=0,
                 fg_color='#37373D', center=(100,50), text='', text_color='white', corner_radius=25,
                 font=("",10), click_command=None, highlightcolor='#52d66c', hover=True):
        
        self.canvas = canvas
        self.width = width 
        self.height = height 
        self.node_outline_color = border_color
        self.node_outline_thickness = border_width
        self.node_color = fg_color
        self.text_color = text_color
        self.corner_radius = corner_radius
        self.font = font
        self.text = text
        self.center = center
        self.click_command = click_command
        self.auxlist = []
        self.signal = False
        self.hover = hover
        self.hover_color = highlightcolor
        
        self.create()
       
    def create(self):
        """ create round rectangular frame with text """
        
        self.ID = self.create_round_rectangle(self.center[0]-self.width*0.5, self.center[1]-self.height*0.5,
                                              self.center[0]+self.width*0.5, self.center[1]+self.height*0.5,
                                              radius=self.corner_radius, outline=self.node_outline_color, fill=self.node_color,
                                              width=self.node_outline_thickness)
        
        self.IDtext = self.canvas.create_text(self.center, fill=self.text_color, justify="center", font=self.font, text=self.text)
        self.allIDs = [self.ID, self.IDtext]
        self.auxlist = [self.ID, self.IDtext]

        for i in self.auxlist:
            self.canvas.tag_bind(i, "<Button-1>", self.getpos, add="+")
            self.canvas.tag_bind(i, '<Enter>', self.enter_node)
            self.canvas.tag_bind(i, '<Leave>', self.leave_node)
        
    def create_round_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1, x2,
                  y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2,
                  x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2, x1,
                  y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]

        return self.canvas.create_polygon(points, **kwargs, smooth=True)
        
    def getpos(self, event):
        """ bind click command and raise the node"""
        self.xy_set = (event.x, event.y)
        
        if self.click_command: self.click_command()

        for id_ in self.allIDs:
            self.canvas.tag_raise(id_)
        
    def bind_all_to_movement(self):
        """ bind the node items to motion """
        
        for id_ in self.auxlist:
            self.canvas.tag_bind(id_, '<B1-Motion>', self.mouse_mov)
            
    def mouse_mov(self, event):
        """ place the node items based one the motion of mouse """

        for id_ in self.allIDs:
            self.canvas.move(id_, event.x-self.xy_set[0], event.y-self.xy_set[1]) 
            self.canvas.tag_raise(id_)
            
        self.xy_set = (event.x, event.y)
        
    def move(self, x, y):
        for id_ in self.allIDs:
            self.canvas.move(id_, x, y) 
            self.canvas.tag_raise(id_)
    
    def enter_node(self, event):
        if self.hover:
            self.canvas.itemconfigure(self.ID, outline=self.hover_color, width=self.node_outline_thickness+1)
        self.signal = True
        
    def leave_node(self, event):
        if self.hover:
            self.canvas.itemconfigure(self.ID, outline=self.node_outline_color, width=self.node_outline_thickness)
        self.signal = False
    
    def destroy(self):
        self.canvas.delete(self.ID, self.IDtext)
        
    def configure(self, **kwargs):
        """ configure options """
        
        if "fg_color" in kwargs:
            self.canvas.itemconfig(self.ID, fill=kwargs.pop("fg_color"))
        if "highlightcolor" in kwargs:
            self.hover_color = kwargs.pop("highlightcolor")
        if "hover" in kwargs:
            self.hover = kwargs.pop("hover")
        if "text" in kwargs:
            self.canvas.itemconfig(self.IDtext, text=kwargs.pop("text"))
        if "text_color" in kwargs:
            self.canvas.itemconfig(self.IDtext, fill=kwargs.pop("text_color"))
        if "font" in kwargs:
            self.canvas.itemconfig(self.IDtext, font=kwargs.pop("font"))
        if len(kwargs)>0:
            raise ValueError("This option is not configurable:" + list(kwargs.keys())[0])
