class Args():
    """ This class is used to remove default arguments in order to reduce the size of the export file """
    
    def value_args(args):        
        default_args = {'width': 100, 'height': 50, 'value': 0, 'border_color': 'white', 'text': None, 
                        'corner_radius': 25, 'border_width': 0, 'fg_color': '#37373D', 'text_color': 'white',
                        'font': ('', 10), 'socket_radius': 8, 'socket_hover': True, 'socket_color': 'green',
                        'socket_hover_color': 'grey50', 'highlightcolor': '#52d66c', 'hover': True, 'fixed': False,
                        'click_command': None, 'side': 'right', 'x': None, 'y': None, 'num': None, 'justify': 'center'}

        args.pop("canvas")
        args.pop("self")
        args.pop("__class__")
        args.pop("x")
        args.pop("y")
        args.pop("click_command")
        args.pop("num")
        new_args = {}
        
        for i in args.keys():
            if default_args.get(i)!=args.get(i):
                new_args.update({i:args.get(i)})

        return new_args
    
    def func_args(args):
        default_args = {'width': 100, 'height': 80, 'inputs': 2, 'border_color': '#37373D', 'text': None, 'socket_radius': 8,
                        'corner_radius': 25, 'border_width': 0, 'fg_color': '#37373D', 'text_color': 'white', 'font': ('', 10),
                        'highlightcolor': '#52d66c', 'hover': True, 'socket_color': 'green', 'socket_hover_color': 'grey50', 'pass_node_id': False,
                        'x': None, 'y': None, 'multiside': False, 'output_socket_color': 'green', 'click_command': None, 'fixed': False,
                        'socket_hover': True, 'num': None, 'none_inputs': False, 'justify': 'center', 'hover_text': None, 'multiple_connection': False}

        args.pop("canvas")
        args.pop("self")
        args.pop("__class__")
        args.pop("command")
        args.pop("x")
        args.pop("y")
        args.pop("click_command")
        args.pop("num")
        new_args = {}
        
        for i in args.keys():
            if default_args.get(i)!=args.get(i):
                new_args.update({i:args.get(i)})

        return new_args

    def compile_args(args):
        default_args = {'width': 100, 'height': 50, 'border_color': '#37373D', 'text': 'Compile', 'socket_radius': 8, 'justify': 'center', 'pass_node_id': False,
                        'corner_radius': 25, 'x': None, 'y': None, 'border_width': 0, 'fg_color': '#37373D', 'text_color': 'white', 'multiple_connection': False,
                        'font': ('', 10), 'highlightcolor': '#52d66c', 'hover': True, 'socket_hover': True, 'socket_color': 'green', 'fixed': False,
                        'socket_hover_color': 'grey50', 'show_value': True, 'command': None, 'click_command': None, 'side': 'left', 'num': None}
        
        args.pop("canvas")
        args.pop("self")
        args.pop("__class__")
        args.pop("command")
        args.pop("x")
        args.pop("y")
        args.pop("click_command")
        args.pop("num")
        new_args = {}
        
        for i in args.keys():
            if default_args.get(i)!=args.get(i):
                new_args.update({i:args.get(i)})

        return new_args
