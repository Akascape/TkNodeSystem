import __main__
from .node import Node
from .node_socket import NodeSocket
from .node_args import Args

class NodeValue(Node):
    def __init__(self, canvas, width=100, height=50, value=0, border_color='white', text=None, corner_radius=25,
                 border_width=0, fg_color='#37373D', text_color='white', font=("",10), socket_radius=8, socket_hover=True,
                 socket_color="green", socket_hover_color="grey50", highlightcolor='#52d66c', hover=True,
                 click_command=None, side="right", x=0, y=0, num=None):

        self.text = text
        self.canvas = canvas
        
        self.args = Args.value_args(locals())
        
        if click_command:
            if click_command!="<lambda>":
                if type(click_command) is str:
                    click_command = getattr(__main__, click_command)
                self.args.update({"click_command": click_command.__name__})
            else:
                click_command = None
                print("Warning: currently <lamba function> cannot be saved and loaded, please use local function instead")
            
        if self.text is None:
            self.text = f"Input{self.canvas.input_num}"
            
        self.canvas.input_num +=1
        self.connected_func = set()
        self.value = value
        self.type = 'NodeValue'
        
        if border_width==0:
            border_color = fg_color

        
        super().__init__(canvas=canvas, width=width, height=height, center=(width,height), text=str(self.text),
                         border_width=border_width, border_color=border_color, fg_color=fg_color, corner_radius=corner_radius,
                         text_color=text_color, font=font, highlightcolor=highlightcolor, hover=hover,
                         click_command=click_command)

        if side=="left":
            center = (width-(width/2),height)
        else:
            center = (width+(width/2),height)
            
        self.output_ = NodeSocket(canvas, value=value, radius=socket_radius, center=center,
                                  fg_color=socket_color, hover_color=socket_hover_color, border_width=border_width,
                                  border_color=border_color, hover=socket_hover, socket_num=num)
        
        self.allIDs = self.allIDs + [self.output_.ID]

        self.bind_all_to_movement()
        self.canvas.tag_bind(self.output_.ID, '<Button-1>', self.connect_output)
        self.canvas.bind_all("<Delete>", lambda e: self.destroy() if self.signal else None, add="+")
        self.socket_nums = self.output_.socket_num
        
        for j in range(self.canvas.gain_in):
            for i in self.allIDs:
                self.canvas.scale(i, 0, 0, 1.1, 1.1)

        for j in range(abs(self.canvas.gain_out)):
            for i in self.allIDs:
                self.canvas.scale(i, 0, 0, 0.9, 0.9)
                
        if x or y:
            super().move(x,y)
     
        self.canvas.obj_list.add(self)

    def get(self):
        """ get the current value of node """
        return self.output_.value
        
    def connect_output(self, event):
        """ connect output socket """
        
        self.canvas.clickcount += 1
        self.canvas.outputcell = self

        if self.canvas.clickcount == 2:
            self.canvas.clickcount = 0
 
        self.output_.connect_wire()
        
    def destroy(self):
        if self.ID not in self.canvas.find_all(): return

        self.output_.value = None
        for i in self.allIDs:
            self.canvas.delete(i)
            
        self.canvas.obj_list.remove(self)
        super().destroy()
        
        for i in self.connected_func:
            i.update()
                
    def exists(self):
        if self.ID in self.canvas.find_all():
            return True
        else:
            return False
        
    def configure(self, **kwargs):
        """ configure options """
        
        if "value" in kwargs:
            self.output_.value = kwargs.pop("value")
            if not self.text:
                super().configure(text=kwargs.pop("text"))
            for i in self.connected_func:
                i.update()
        if "text" in kwargs:
            self.text = kwargs.pop("text")
            super().configure(text=self.text)
        if "fg_color" in kwargs:
            super().configure(fg_color=kwargs.pop("fg_color"))
        if "text_color" in kwargs:
            super().configure(text_color=kwargs.pop("text_color"))
        if "font" in kwargs:
            super().configure(font=kwargs.pop("font"))
        if "highlightcolor" in kwargs:
            super().configure(highlightcolor=kwargs.pop("highlightcolor"))
        if "socket_color" in kwargs:
            self.output_.configure(fg_color=kwargs.pop("socket_color"))
        if "socket_hover_color" in kwargs:
            self.output_.configure(hover_color=kwargs.pop("socket_hover_color"))
        if "hover" in kwargs:
            super().configure(hover=kwargs.pop("hover"))
        if "socket_hover" in kwargs:
            self.output_.configure(hover=kwargs.pop("socket_hover"))
                                  
        if len(kwargs)>0:
            raise ValueError("This option is not configurable:" + list(kwargs.keys())[0])

class NodeOperation(Node):
    def __init__(self, canvas, width=100, height=None, inputs=2, border_color='white', text=None,
                 socket_radius=8, corner_radius=25, border_width=0, fg_color='#37373D', text_color='white', font=("",10),
                 highlightcolor='#52d66c', hover=True, socket_color="green", socket_hover_color="grey50", x=0, y=0,
                 multiside=False, command=None, output_socket_color="green", click_command=None, socket_hover=True, num=None):

        self.text = text
        self.canvas = canvas
        self.type = 'NodeOperation'
        
        if self.text is None:
            self.text = f"Function{self.canvas.operation_num}"
            
        self.canvas.operation_num +=1

        if border_width==0:
            border_color = fg_color
            
        self.args = Args.func_args(locals())
        
        if command:
            if command!="<lambda>":            
                if type(command) is str:
                    command = getattr(__main__, command)
                self.args.update({"command": command.__name__})
            else:
                command = None
                print("Warning: currently <lamba function> cannot be saved and loaded, please use local function instead")
        if click_command:
            if click_command!="<lambda>":
                if type(click_command) is str:
                    click_command = getattr(__main__, click_command)
                self.args.update({"click_command": click_command.__name__})
            else:
                click_command = None
                print("Warning: currently <lamba function> cannot be saved and loaded, please use local function instead")
                
        self.command = command
        
        if height is None:
            height = 50 + (inputs*10)
            
        super().__init__(canvas=canvas, width=width, height=height, center=(width,height), 
                         border_width=border_width, fg_color=fg_color, border_color=border_color,
                         text_color=text_color, font=font, click_command=click_command, corner_radius=corner_radius,
                         highlightcolor=highlightcolor, text=str(self.text), hover=hover)

        self.line1 = None
        self.line2 = None
        self.line3 = None
        self.line4 = None
        self.line5 = None
        self.socket_colors = []
        self.connected_node = set()
        self.connected_node_first = None
        x_pos = x
        y_pos = y
            
        if type(socket_color) is list:
            self.socket_colors = socket_color
        else:
            for i in range(5):
                self.socket_colors.append(socket_color)

        self.inputs = inputs
    
        if self.inputs>3 and self.height<=80:
            multiside=True
            
        if multiside:
            z = self.inputs-1
        else:
            z = self.inputs+1

        if z==0:
            z = 2
            
        y = height/z
        x = 1
        if self.inputs==2 and multiside:
            x = 1/2

        self.cellinput1 = None
        self.cellinput2 = None
        self.cellinput3 = None
        self.cellinput4 = None
        self.cellinput5 = None
        self.celloutput = None
        self.socket_nums = []
        
        self.output_ = NodeSocket(canvas, radius=socket_radius, center=(width+(width/2),height),
                                  fg_color=output_socket_color, hover_color=socket_hover_color, socket_num=num[0] if num else None,
                                  border_width=border_width, border_color=border_color, hover=socket_hover)
        self.canvas.tag_bind(self.output_.ID, '<Button-1>', self.connect_output)
        self.socket_nums.append(self.output_.socket_num)
        
        center = (width/2, y * x + height/2)     
        self.input_1 = NodeSocket(canvas, radius=socket_radius, center=center, fg_color=self.socket_colors[0],
                                  hover_color=socket_hover_color, border_width=border_width,
                                  border_color=border_color, socket_num=num[1] if num else None)
        
        id_list = [self.output_.ID, self.input_1.ID]
        self.canvas.tag_bind(self.input_1.ID, '<Button-1>', lambda e: self.connect_input(self.line1,'input1'))
        self.socket_nums.append(self.input_1.socket_num)
        
        if self.inputs>=2:
            if not multiside:
                x+=1
                center = (width/2,y * x +height/2)
            else:
                center = (width, height/2)
                
            self.input_2 = NodeSocket(canvas, radius=socket_radius, center=center, fg_color=self.socket_colors[1],
                                      hover_color=socket_hover_color, border_width=border_width, hover=socket_hover,
                                      border_color=border_color, socket_num=num[2] if num else None)
            id_list.append(self.input_2.ID)
            self.canvas.tag_bind(self.input_2.ID, '<Button-1>', lambda e: self.connect_input(self.line2,'input2'))
            self.socket_nums.append(self.input_2.socket_num)
            
        if self.inputs>=3:
            if not multiside:
                x+=1
                center = (width/2,y * x +height/2)
            else:
                center = (width, height*1.5)
            self.input_3 = NodeSocket(canvas, radius=socket_radius, center=center, fg_color=self.socket_colors[2],
                                      hover_color=socket_hover_color, border_width=border_width, hover=socket_hover,
                                      border_color=border_color, socket_num=num[3] if num else None)
            self.canvas.tag_bind(self.input_3.ID, '<Button-1>', lambda e: self.connect_input(self.line3,'input3'))
            id_list.append(self.input_3.ID)
            self.socket_nums.append(self.input_3.socket_num)
            
        if self.inputs>=4:
            x+=1
            center = (width/2,y * x +height/2)
            self.input_4 = NodeSocket(canvas, radius=socket_radius, center=center, fg_color=self.socket_colors[3],
                                      hover_color=socket_hover_color, border_width=border_width, hover=socket_hover,
                                      border_color=border_color, socket_num=num[4] if num else None)
            self.canvas.tag_bind(self.input_4.ID, '<Button-1>', lambda e: self.connect_input(self.line4,'input4'))
            id_list.append(self.input_4.ID)
            self.socket_nums.append(self.input_4.socket_num)
            
        if self.inputs>=5:
            x+=1
            center = (width/2,y * x +height/2)
            self.input_5 = NodeSocket(canvas, radius=socket_radius, center=center, fg_color=self.socket_colors[4],
                                      hover_color=socket_hover_color, border_width=border_width, hover=socket_hover,
                                      border_color=border_color, socket_num=num[5] if num else None)
            self.canvas.tag_bind(self.input_5.ID, '<Button-1>', lambda e: self.connect_input(self.line5, 'input5'))
            id_list.append(self.input_5.ID)
            self.socket_nums.append(self.input_5.socket_num)
            
        self.allIDs = self.allIDs + id_list
        self.bind_all_to_movement()
        self.id_list = id_list
        self.canvas.bind_all("<Delete>", lambda e: self.destroy() if self.signal else None, add="+")
   
        for j in range(self.canvas.gain_in):
            for i in self.allIDs:
                self.canvas.scale(i, 0, 0, 1.1, 1.1)

        for j in range(abs(self.canvas.gain_out)):
            for i in self.allIDs:
                self.canvas.scale(i, 0, 0, 0.9, 0.9)
                
        if x_pos or y_pos:
            super().move(x_pos,y_pos)
            
        self.canvas.obj_list.add(self)
        
    def connect_output(self, event):
        """ connect output socket """

        self.canvas.clickcount += 1
        self.canvas.outputcell = self

        if self.canvas.clickcount == 2:
            self.canvas.clickcount = 0
            
        self.output_.connect_wire()
 
    def connect_input(self, line_id, input_id):
        """ connect input sockets """
        if self.canvas.outputcell is None:
            return
        if self.canvas.outputcell in self.connected_node:
            return
        if self.canvas.outputcell==self:
            return
 
        m = self.connected_node_first

        for i in range(self.canvas.operation_num):
            if m is None:
                break
            if m.type=="NodeOperation":
                if self.canvas.outputcell in m.connected_node:
                    return
            m = m.connected_node_first
        
        try: self.canvas.delete(line_id.ID)
        except: None
        
        self.canvas.clickcount += 1
        self.canvas.IDc = input_id
        self.canvas.inputcell = self
        
        if self.canvas.clickcount == 2:
            self.canvas.clickcount = 0
            self.canvas.conectcells()
            if self.canvas.outputcell.type=="NodeValue":
                self.canvas.outputcell.connected_func.add(self)
            elif self.canvas.outputcell.type=="NodeOperation":
                self.canvas.outputcell.connected_node.add(self)
                self.canvas.outputcell.connected_node_first = self
            try:
                if input_id=="input1":
                    for x in self.canvas.line_list:
                        if x[1]==self.input_1.socket_num:
                            self.canvas.line_list.remove(x)
                            break
                    l = (self.canvas.outputcell.output_.socket_num, self.canvas.inputcell.input_1.socket_num)
                    self.canvas.line_list.add(l)
                if input_id=="input2":
                    for x in self.canvas.line_list:
                        if x[1]==self.input_2.socket_num:
                            self.canvas.line_list.remove(x)
                            break
                    l = (self.canvas.outputcell.output_.socket_num, self.canvas.inputcell.input_2.socket_num)
                    self.canvas.line_list.add(l)                    
                if input_id=="input3":
                    for x in self.canvas.line_list:
                        if x[1]==self.input_3.socket_num:
                            self.canvas.line_list.remove(x)
                            break
                    l = (self.canvas.outputcell.output_.socket_num, self.canvas.inputcell.input_3.socket_num)
                    self.canvas.line_list.add(l)
                if input_id=="input4":
                    for x in self.canvas.line_list:
                        if x[1]==self.input_4.socket_num:
                            self.canvas.line_list.remove(x)
                            break
                    l = (self.canvas.outputcell.output_.socket_num, self.canvas.inputcell.input_4.socket_num)
                    self.canvas.line_list.add(l)
                if input_id=="input5":
                    for x in self.canvas.line_list:
                        if x[1]==self.input_5.socket_num:
                            self.canvas.line_list.remove(x)
                            break
                    l = (self.canvas.outputcell.output_.socket_num, self.canvas.inputcell.input_5.socket_num)
                    self.canvas.line_list.add(l)
            except AttributeError: None
        else:
            if self.canvas.outputcell.type=="NodeValue":
                try: self.canvas.outputcell.connected_func.remove(self)
                except KeyError: None
            elif self.canvas.outputcell.type=="NodeOperation":
                try:
                    self.canvas.outputcell.connected_node.remove(self)
                    self.canvas.outputcell.connected_node_first = None
                except KeyError: None
            try:
                if input_id=="input1":
                    self.cellinput1 = None
                    self.canvas.line_list.remove((self.canvas.outputcell.output_.socket_num, self.canvas.inputcell.input_1.socket_num))
                if input_id=="input2":
                    self.cellinput2 = None
                    self.canvas.line_list.remove((self.canvas.outputcell.output_.socket_num, self.canvas.inputcell.input_2.socket_num))
                if input_id=="input3":
                    self.cellinput3 = None
                    self.canvas.line_list.remove((self.canvas.outputcell.output_.socket_num, self.canvas.inputcell.input_3.socket_num))
                if input_id=="input4":
                    self.cellinput4 = None
                    self.canvas.line_list.remove((self.canvas.outputcell.output_.socket_num, self.canvas.inputcell.input_4.socket_num))
                if input_id=="input5":
                    self.cellinput5 = None
                    self.canvas.line_list.remove((self.canvas.outputcell.output_.socket_num, self.canvas.inputcell.input_5.socket_num))
            except AttributeError: None
            except KeyError: None
  
            self.update()
       
    def update(self):
        """ update the output values """
        arguments = [self.cellinput1,
                     self.cellinput2,
                     self.cellinput3,
                     self.cellinput4,
                     self.cellinput5]
        values_args = []
        if self.command:
            for i in arguments[0:self.inputs]:
                if i is None:
                    self.output_.value = None
                    break
                else:
                    self.output_.value = 1
                    values_args.append(i.output_.value)
                    
            if self.output_.value:
                for i in values_args:
                    if i is None:
                        self.output_.value = None
                        break
                    else:
                        self.output_.value = 1
                        
                if self.output_.value:
                    self.output_.value = self.command(*values_args[0:self.inputs])
        else:
            self.output_.value = None

        if len(self.connected_node)>0:
            for i in self.connected_node:
                i.update()
        
    def get(self):
        """ get the current value of node """
        return self.output_.value
    
    def destroy(self):
        if self.ID not in self.canvas.find_all(): return
        self.output_.value = None
        for i in self.id_list:
            self.canvas.delete(i)

        self.canvas.obj_list.remove(self)
        super().destroy()
        
        if len(self.connected_node)>0:
            for i in self.connected_node:
                i.update()
                
    def exists(self):
        if self.ID in self.canvas.find_all():
            return True
        else:
            return False
        
    def configure(self, **kwargs):
        """ configure options """
        
        if "text" in kwargs:
            self.text = kwargs.pop("text")
            super().configure(text=self.text)
        if "fg_color" in kwargs:
            super().configure(fg_color=kwargs.pop("fg_color"))
        if "text_color" in kwargs:
            super().configure(text_color=kwargs.pop("text_color"))
        if "font" in kwargs:
            super().configure(font=kwargs.pop("font"))
        if "highlightcolor" in kwargs:
            super().configure(highlightcolor=kwargs.pop("highlightcolor"))
        if "socket_color" in kwargs:
            socket_color = kwargs.pop("socket_color")
            self.output_.configure(fg_color=socket_color)
            try:
                self.input_1.configure(fg_color=socket_color)
                self.input_2.configure(fg_color=socket_color)
                self.input_3.configure(fg_color=socket_color)
                self.input_4.configure(fg_color=socket_color)
                self.input_5.configure(fg_color=socket_color)
            except: None  
        if "socket_hover_color" in kwargs:
            socket_hover_color = kwargs.pop("socket_hover_color")
            self.output_.configure(hover_color=socket_hover_color)
            try:
                self.input_1.configure(hover_color=socket_hover_color)
                self.input_2.configure(hover_color=socket_hover_color)
                self.input_3.configure(hover_color=socket_hover_color)
                self.input_4.configure(hover_color=socket_hover_color)
                self.input_5.configure(hover_color=socket_hover_color)
            except: None
            
        if "socket_color_1" in kwargs:
            self.input_1.configure(fg_color=kwargs.pop("socket_color_1"))
        if "socket_color_2" in kwargs:
            self.input_2.configure(fg_color=kwargs.pop("socket_color_2"))
        if "socket_color_3" in kwargs:
            self.input_3.configure(fg_color=kwargs.pop("socket_color_3"))
        if "socket_color_4" in kwargs:
            self.input_4.configure(fg_color=kwargs.pop("socket_color_4"))
        if "socket_color_5" in kwargs:
            self.input_5.configure(fg_color=kwargs.pop("socket_color_5"))
            
        if "output_socket_color" in kwargs:
            self.output_.configure(fg_color=kwargs.pop("output_socket_color"))
        if "hover" in kwargs:
            super().configure(hover=kwargs.pop("hover"))
        if "socket_hover" in kwargs:
            hover = kwargs.pop("socket_hover")
            self.output_.configure(hover=hover)
            try:
                self.input_1.configure(hover=hover)
                self.input_2.configure(hover=hover)
                self.input_3.configure(hover=hover)
                self.input_4.configure(hover=hover)
                self.input_5.configure(hover=hover)
            except: None
                                  
        if len(kwargs)>0:
            raise ValueError("This option is not configurable:" + list(kwargs.keys())[0])
        
class NodeCompile(Node):
    def __init__(self, canvas, width=100, height=50, border_color='white', text="Compile", socket_radius=8, corner_radius=25, x=0, y=0,
                 border_width=0, fg_color='#37373D',text_color='white', font=("",10), highlightcolor='#52d66c', hover=True, socket_hover=True,
                 socket_color="green", socket_hover_color="grey50", show_value=True, command=None, click_command=None, side="left", num=None):

        self.canvas = canvas
        self.text = text
        self.type = 'NodeCompile'
        
        if border_width==0:
            border_color = fg_color

        self.canvas.compile_num +=1
        
        self.args = Args.compile_args(locals())
        
        if command:
            if command!="<lambda>":            
                if type(command) is str:
                    command = getattr(__main__, command)
                self.args.update({"command": command.__name__})
            else:
                command = None
                print("Warning: currently <lamba function> cannot be saved and loaded, please use local function instead")
        if click_command:
            if click_command!="<lambda>":
                if type(click_command) is str:
                    click_command = getattr(__main__, click_command)
                self.args.update({"click_command": click_command.__name__})
            else:
                click_command = None
                print("Warning: currently <lamba function> cannot be saved and loaded, please use local function instead")
                
        super().__init__(canvas=canvas, width=width, height=height, center=(width,height), text=str(text), corner_radius=corner_radius,
                         border_width=border_width, fg_color=fg_color, border_color=border_color, hover=hover,
                         text_color=text_color, font=font, click_command=click_command, highlightcolor=highlightcolor)

        self.line1 = None
        self.line2 = None
        self.cellinput1 = None
        self.cellinput2 = None
        self.celloutput = None
        self.show_value = show_value
        self.previous_value = None
        self.command = command
        
        if side=="left":
            center = (width-(width/2),height)
        else:
            center = (width+(width/2),height)
            
        self.input_1 = NodeSocket(canvas, radius=socket_radius, center=center, border_width=border_width,
                                  fg_color=socket_color, hover_color=socket_hover_color, border_color=border_color, 
                                  hover=socket_hover, socket_num=num[0] if num else None)
        
        self.output_ = NodeSocket(canvas, radius=socket_radius, center=(width+(width/2),height),
                                  fg_color=socket_color, hover_color=socket_hover_color, border_width=border_width,
                                  border_color=border_color, hover=socket_hover, socket_num=num[1] if num else None)
        self.output_.hide()
        self.socket_nums = [self.input_1.socket_num, self.output_.socket_num]
        self.allIDs = self.allIDs + [self.output_.ID, self.input_1.ID] 
        self.fixed = True
        self.bind_all_to_movement()
        self.canvas.tag_bind(self.input_1.ID, '<Button-1>', self.connect_input)
        self.canvas.bind_all("<Delete>", lambda e: self.destroy() if self.signal else None, add="+")
        
        for j in range(self.canvas.gain_in):
            for i in self.allIDs:
                self.canvas.scale(i, 0, 0, 1.1, 1.1)

        for j in range(abs(self.canvas.gain_out)):
            for i in self.allIDs:
                self.canvas.scale(i, 0, 0, 0.9, 0.9)
                
        if x or y:
            super().move(x,y)
            
        self.canvas.obj_list.add(self)
        
    def connect_input(self, event):
        """ connect input sockets """
        
        try: self.canvas.delete(self.line1.ID)
        except: None

        self.canvas.clickcount += 1
        self.canvas.IDc = 'input1'
        self.canvas.inputcell = self

        if self.canvas.clickcount == 2:
            self.canvas.clickcount = 0
            self.canvas.conectcells()
            self.fixed = False
            try:
                if self.canvas.outputcell.type=="NodeValue":
                    self.canvas.outputcell.connected_func.add(self)
                for x in self.canvas.line_list:
                    if x[1]==self.input_1.socket_num:
                        self.canvas.line_list.remove(x)
                        break
                self.canvas.line_list.add((self.canvas.outputcell.output_.socket_num, self.canvas.inputcell.input_1.socket_num))
            except AttributeError: None
        else:
            self.fixed = True
            try:
                if self.canvas.outputcell.type=="NodeValue":
                    try: self.canvas.outputcell.connected_func.remove(self)
                    except KeyError: None
                self.canvas.line_list.remove((self.canvas.outputcell.output_.socket_num, self.canvas.inputcell.input_1.socket_num))
            except AttributeError: None
            except KeyError: None
            
    def get(self):
        """ get the current value of node """
        return self.output_.value
    
    def update(self):
        """ update the output values """
        
        self.output_.value = self.cellinput1.output_.value if not self.fixed else None
        if self.previous_value!=self.output_.value:
            if self.show_value:
                self.canvas.itemconfigure(self.IDtext, text=str(self.output_.value))
            if self.output_.value is not None:
                if self.command: self.command(self.output_.value)
        self.previous_value = self.output_.value

        if self.ID in self.canvas.find_all():
            self.canvas.after(50, self.update)
            
    def destroy(self):
        if self.ID not in self.canvas.find_all(): return
        self.output_.value = None
        for i in self.allIDs:
            self.canvas.delete(i)
            
        self.canvas.obj_list.remove(self)
        super().destroy()
        
    def exists(self):
        if self.ID in self.canvas.find_all():
            return True
        else:
            return False
        
    def configure(self, **kwargs):
        """ configure options """
        
        if "text" in kwargs:
            self.text = kwargs.pop("text")
            super().configure(text=self.text)
        if "fg_color" in kwargs:
            super().configure(fg_color=kwargs.pop("fg_color"))
        if "text_color" in kwargs:
            super().configure(text_color=kwargs.pop("text_color"))
        if "font" in kwargs:
            super().configure(font=kwargs.pop("font"))
        if "highlightcolor" in kwargs:
            super().configure(highlightcolor=kwargs.pop("highlightcolor"))
        if "socket_color" in kwargs:
            self.input_1.configure(fg_color=kwargs.pop("socket_color"))
        if "socket_hover_color" in kwargs:
            self.input_1.configure(hover_color=kwargs.pop("socket_hover_color"))
        if "hover" in kwargs:
            super().configure(hover=kwargs.pop("hover"))
        if "socket_hover" in kwargs:
            self.input_1.configure(hover=kwargs.pop("socket_hover"))
        if "show_value" in kwargs:
            self.show_value = kwargs.pop("show_value")
            
        if len(kwargs)>0:
            raise ValueError("This option is not configurable:" + list(kwargs.keys())[0])
