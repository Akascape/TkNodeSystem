import tkinter
import platform
import os
import json
import sys
from .node_wire import NodeWire
from .node_types import NodeValue, NodeOperation, NodeCompile

class NodeCanvas(tkinter.Canvas):
    def __init__(self, master, bg="grey10", width=500, height=500, wire_color="white", wire_width=3,
                 grid_image="lines", zoom=True, wire_dash=True, move=True, wire_hover_color="red", **kwargs):
        
        super().__init__(master, bg=bg, width=width, height=height, bd=0, highlightthickness=0, **kwargs)

        self.wire_color = wire_color
        self.wire_width = wire_width
        self.wire_hover_color = wire_hover_color
        self.dash = wire_dash
        self.bg = bg
        self.inputcell = None
        self.outputcell = None
        self.clickcount = 0
        self.IDc = None
        self.operation_num = 0
        self.input_num = 0
        self.compile_num = 0
        self.socket_num = 0
        self.connect_wire = True
        self.line_list = set()
        self.obj_list = set()
        self.line_ids = set()
        self.node_list = set()
        self.gain_in = 1
        self.gain_out = 1
        self.set_grid_image(grid_image)
        
        if move:
            if sys.platform.startswith("darwin"):
                self.tag_bind(self.grid_bg, '<ButtonPress-3>', lambda e: self.getpos(e, 1))
                self.tag_bind(self.grid_bg, '<ButtonRelease-3>', lambda e: self.getpos(e, 0))
                self.tag_bind(self.grid_bg, "<B3-Motion>", self.move_grid)
            else:
                self.tag_bind(self.grid_bg, '<ButtonPress-2>', lambda e: self.getpos(e, 1))
                self.tag_bind(self.grid_bg, '<ButtonRelease-2>', lambda e: self.getpos(e, 0))
                self.tag_bind(self.grid_bg, "<B2-Motion>", self.move_grid)
        
        if zoom:
            self.bind("<MouseWheel>", self.do_zoom)
            self.tag_bind(self.grid_bg, "<Button-4>", lambda e: self.do_zoom(e, 120))
            self.tag_bind(self.grid_bg, "<Button-5>", lambda e: self.do_zoom(e, -120))
            
    def set_grid_image(self, grid_image):
        """ set the grid image for the canvas """
        
        # default grids: ['dots', 'lines', None]
        base_path = os.path.dirname(os.path.abspath(__file__))
        if grid_image=="dots":
            self.image = tkinter.PhotoImage(file=os.path.join(base_path, "grid_images", "grid_dot.png"))
        elif grid_image=="lines":
            self.image = tkinter.PhotoImage(file=os.path.join(base_path, "grid_images", "grid_lines.png"))
        elif not grid_image:
            self.image = tkinter.PhotoImage(file=os.path.join(base_path, "grid_images", "no_grid.png"))
        else:
            self.image = tkinter.PhotoImage(file=grid_image)
                           
        self.image = self.image.subsample(1,1)
        try:
            self.delete(self.grid_bg)
        except: None
        self.grid_bg = self.create_image(self.image.width()/2, self.image.height()/2, image = self.image)   
        self.tag_lower(self.grid_bg)
        
    def getpos(self, event, cursor):
        """ get the mouse position and change cursor style """
        
        self.xy_set = (event.x, event.y)
  
        if cursor:
            self.config(cursor="fleur", width=self.winfo_reqwidth(), height=self.winfo_reqheight())
        else:
            self.config(cursor="arrow", width=self.winfo_reqwidth(), height=self.winfo_reqheight())
        
    def move_grid(self, event):
        """ move the contents of the canvas except the grid image """
        
        self.all_items = list(self.find_all())
        self.all_items.pop(self.all_items.index(self.grid_bg))
        
        for i in self.all_items:
            self.move(i, event.x-self.xy_set[0], event.y-self.xy_set[1])        
        self.xy_set = (event.x, event.y)

        for i in self.node_list:
            i.update_sockets()
            
    def do_zoom(self, event, delta=None):
        """ zoom in/out the canvas by changing the coordinates of all canvas items """
        
        self.all_items = list(self.find_all())
        self.all_items.pop(self.all_items.index(self.grid_bg))

        if not delta:
            delta = event.delta
        
        if delta>0:
            for i in self.all_items:
                self.scale(i, event.x, event.y, 1.1, 1.1)
            self.gain_in +=1
        else:
            for i in self.all_items:
                self.scale(i, event.x, event.y, 0.9, 0.9)
            self.gain_out +=1

        for i in self.node_list:
            i.update_sockets()
            
    def conectcells(self):
        """ connection data for the inputs of any operation node """
        
        if self.IDc == 'input1': self.inputcell.cellinput1 = self.outputcell
        if self.IDc == 'input2': self.inputcell.cellinput2 = self.outputcell
        if self.IDc == 'input3': self.inputcell.cellinput3 = self.outputcell
        if self.IDc == 'input4': self.inputcell.cellinput4 = self.outputcell
        if self.IDc == 'input5': self.inputcell.cellinput5 = self.outputcell
        
        if self.inputcell is None or self.outputcell is None:
            return
        if self.inputcell.ID!=self.outputcell.ID:
            self.line = NodeWire(self, self.outputcell, self.inputcell, wire_color=self.wire_color,
                                 wire_width=self.wire_width, dash=self.dash, wire_hover_color=self.wire_hover_color)
            self.inputcell.update()
            
    def clear(self):
        """ clear the canvas except the grid image """
        
        self.all_items = list(self.find_all())
        self.all_items.pop(self.all_items.index(self.grid_bg))
        
        for i in self.all_items:
            self.delete(i)

        self.node_num = 0
        self.input_num = 0
        self.compile_num = 0
        self.socket_num = 0
        self.line_list = set()
        self.obj_list = set()
        self.line_ids = set()
        self.node_list = set()
        
    def configure(self, **kwargs):
        """ configure options """
        
        if "wire_color" in kwargs:
            self.wire_color = kwargs.pop("wire_color")
            for i in self.line_ids:
                i.configure(wire_color=self.wire_color)
        if "wire_width" in kwargs:
            self.wire_width = kwargs.pop("wire_width")
            for i in self.line_ids:
                i.configure(wire_width=self.wire_width)
        if "wire_dash" in kwargs:
            self.dash = kwargs.pop("wire_dash")
            for i in self.line_ids:
                i.configure(dash=self.dash)
        if "wire_hover_color" in kwargs:
            self.wire_hover_color = kwargs.pop("wire_hover_color")
            for i in self.line_ids:
                i.configure(wire_hover_color=self.wire_hover_color)      
        if "grid_image" in kwargs:
            self.set_grid_image(kwargs.pop("grid_image"))

        super().config(**kwargs)
        
    def save(self, filename):
        """ save the node tree to a file """
        if os.path.exists(filename):
            os.remove(filename)

        x = []
        sorted_obj_list = []
        for i in self.obj_list:
            x.append(i.ID)
 
        for i in sorted(x):
            for x in self.obj_list:
                if i==x.ID:
                    sorted_obj_list.append(x)
        
        with open(filename, 'w') as file:
            obj_dict = {f'{obj.type} {id}': (obj.args, round(obj.output_.center[0]-obj.width,2),
                                             round(obj.output_.center[1]-obj.height,2), obj.socket_nums) for id, obj in enumerate(sorted_obj_list)}
            obj_dict.update({"Lines" : list(self.line_list)})
            json.dump(obj_dict, file)

    def load(self, filename):
        """ load the node tree back to the canvas """

        if not os.path.exists(filename):
            raise FileNotFoundError("No such file found: " + str(filename))
  
        self.clear()
        self.connect_wire = False
        
        obj_type_dict = {'NodeValue': NodeValue,
                         'NodeOperation': NodeOperation,
                         'NodeCompile': NodeCompile}
        
        with open(filename) as file:
            obj_dict = json.load(file)
            value_nodes = []
            func_nodes = []
            comp_nodes = []
            self.obj_list = set()

        for obj_type, attributes in obj_dict.items():
            if obj_type.split()[0]=="Lines":
                line_list = attributes
                continue
       
            obj = obj_type_dict[obj_type.split()[0]](self, **attributes[0], x=attributes[1], y=attributes[2], num=attributes[3])
            if obj_type.split()[0]=="NodeValue":
                value_nodes.append(obj)
            elif obj_type.split()[0]=="NodeOperation":
                func_nodes.append(obj)
            elif obj_type.split()[0]=="NodeCompile":
                comp_nodes.append(obj)
            self.obj_list.add(obj)

        for nodes in [value_nodes, func_nodes, comp_nodes]:
            for i in nodes:
                i.connect_output(None)
                for j in func_nodes:
                    try:
                        if [self.outputcell.output_.socket_num, j.input_1.socket_num] in line_list:
                            self.clickcount = 1
                            j.connect_input(j.line1, 'input1')
                        if [self.outputcell.output_.socket_num, j.input_2.socket_num] in line_list:
                            self.clickcount = 1
                            j.connect_input(j.line2, 'input2')
                        if [self.outputcell.output_.socket_num, j.input_3.socket_num] in line_list:
                            self.clickcount = 1
                            j.connect_input(j.line3, 'input3')
                        if [self.outputcell.output_.socket_num, j.input_4.socket_num] in line_list:
                            self.clickcount = 1
                            j.connect_input(j.line4, 'input4')
                        if [self.outputcell.output_.socket_num, j.input_5.socket_num] in line_list:
                            self.clickcount = 1
                            j.connect_input(j.line5, 'input5')
                    except AttributeError: None
                for j in comp_nodes:
                    if [self.outputcell.output_.socket_num, j.input_1.socket_num] in line_list:
                        self.clickcount = 1
                        j.connect_input(None)
                    

        self.connect_wire = True    

