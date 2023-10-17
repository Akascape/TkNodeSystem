class NodeWire():
    def __init__(self, canvas, firstcell, secondcell, wire_color='white', wire_width=3,
                 dash=True, wire_hover_color="red"):

        self.canvas = canvas
        self.firstcell = firstcell # output socket
        self.secondcell = secondcell # input socket
        self.IDc = self.canvas.IDc
        self.wire_color = wire_color
        self.wire_width = wire_width
        self.canvas.line_ids.add(self)
        self.dash = (2,4) if dash else ()
        self.hover_color = wire_hover_color
        self.connected = True
        
        if self.firstcell:
            self.create()
            self.update()

    def create(self):
        """ creates the line from output-->input sockets """
        
        self.firstcell.line = self
        self.x1, self.y1 = self.firstcell.output_.center

        if self.canvas.IDc == 'input1':
            self.input_num = self.secondcell.input_1
            self.secondcell.line1 = self

        if self.canvas.IDc == 'input2':
            self.input_num = self.secondcell.input_2
            self.secondcell.line2 = self

        if self.canvas.IDc == 'input3':
            self.input_num = self.secondcell.input_3
            self.secondcell.line3 = self

        if self.canvas.IDc == 'input4':
            self.input_num = self.secondcell.input_4
            self.secondcell.line4 = self

        if self.canvas.IDc == 'input5':
            self.input_num = self.secondcell.input_5
            self.secondcell.line5 = self
            
        self.x2,self.y2 = self.input_num.center
        self.firstcell.output_.delete_wire()
        self.ID = self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, dash=self.dash, width=self.wire_width,
                                          activefill=self.hover_color, fill=self.wire_color, activewidth=self.wire_width)
        self.canvas.tag_lower(self.ID)
        self.canvas.tag_lower(self.canvas.grid_bg)
        self.inputs = self.canvas.IDc
        self.canvas.tag_bind(self.ID, "<Double-Button-1>", lambda e: self.delete_line(self.inputs))

    def delete_line(self, input_num):
        """ delete the line when disconnected """
        self.canvas.delete(self.ID)
        self.canvas.line_ids.remove(self)
        self.firstcell.output_.live_connection = True
        self.firstcell.connect_output(None)
        self.firstcell.output_.live_connection = False
        self.canvas.clickcount = 0
        if self.secondcell.type=="NodeOperation":
            self.secondcell.connect_input(self.ID, input_num)
        else:
            self.secondcell.connect_input(None)
            
    def update(self):
        """ update the coordinates of line based on the socket position """
        all_items = self.canvas.find_all()
        if self.firstcell.ID not in all_items or self.secondcell.ID not in all_items:
            self.canvas.delete(self.ID)
            self.connected = False
        if self.ID not in all_items: return
        self.x1, self.y1 = self.firstcell.output_.center
        if self.IDc == 'input1': self.x2, self.y2 = self.secondcell.input_1.center
        if self.IDc == 'input2': self.x2, self.y2 = self.secondcell.input_2.center
        if self.IDc == 'input3': self.x2, self.y2 = self.secondcell.input_3.center
        if self.IDc == 'input4': self.x2, self.y2 = self.secondcell.input_4.center
        if self.IDc == 'input5': self.x2, self.y2 = self.secondcell.input_5.center
        self.canvas.coords(self.ID, self.x1, self.y1, self.x2, self.y2)

    def configure(self, **kwargs):
        if "wire_color" in kwargs:
            self.canvas.itemconfig(self.ID, fill=kwargs.pop("wire_color"))
        if "wire_width" in kwargs:
            self.canvas.itemconfig(self.ID, width=kwargs.pop("wire_width"))
        if "dash" in kwargs:
            self.dash = kwargs.pop("dash") 
            self.canvas.itemconfig(self.ID, dash=self.dash if self.dash else ())
        if "wire_hover_color" in kwargs:
            self.canvas.itemconfig(self.ID, activefill=kwargs.pop("wire_hover_color"))

        if len(kwargs)>0:
            raise ValueError("This option is not configurable:" + list(kwargs.keys())[0])
        
