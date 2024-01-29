# Author: Akash Bora
# License: MIT

import customtkinter
from tknodesystem import *
from ctk_spinbox import CTkSpinbox
from tkinter.colorchooser import askcolor
from render_engine import ThreeDFrame
import sv_ttk
from tkinter import ttk, filedialog
import math

customtkinter.set_appearance_mode("Dark")

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    
def to_points(node, x):
    for i in x:
        if len(i)!=3:
            node.toggle(1)
        if type(i) is list:
            x[x.index(i)] = tuple(i)
    node.configure(text=f"SIDE \npoints: {len(x)}")
    return x, hex_to_rgb(node.node_color)

def angle(v1, v2):
    dot = v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]
    mag1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2 + v1[2] ** 2)
    mag2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2 + v2[2] ** 2)

    return math.acos(dot / (mag1 * mag2))

def sort_points(points):
    # sort angles based on the right hand rule
    origin = points[0]
    ref = (1, 0, 0)
    angles = []
    for point in points[1:]:
        vector = (point[0] - origin[0], point[1] - origin[1], point[2] - origin[2])
        theta = angle(vector, ref)
        angles.append((point, theta))
        angles.sort(key=lambda x: x[1])
        sorted_points = [origin]
    for i in angles:
        sorted_points.append(i[0])
    return sorted_points

def join_coords(values):
    
    geo_data = []
    for i in values:
        geo_data.append(i[0])
        
    coords_data = []
    all_points = set()
    
    for side in geo_data:
        for points in side:
            all_points.add(points)
            
    num = 0

    coords_data.append(list(all_points))
    for side in geo_data:

        side = sort_points(side) 
        anti_side = side[::-1] 

        connections = []
        
        for i in side:
            connections.append(list(all_points).index(i))
         
        connections.append(values[num][1])

        coords_data.append([connections])
        
        connections = []
        
        for i in anti_side:
            connections.append(list(all_points).index(i))
         
        connections.append(values[num][1])
        
        coords_data.append([connections])
        num +=1

    for i in coords_data:
        if i==[]:
            return

    try:
        geo[notebook.index(notebook.select())+1].configure(coords=coords_data)
    except:
        pass
        
def add_content(tab, tab_num):
    global dialog_box

    def open_color_dialog(node):
        global global_side_color
        color = askcolor(title="Choose Side Color")
        if color[1]:
            node.configure(fg_color=color[1], text_color="black")
            global_side_color = color[1]
            node.update()
        
    def open_config_dialog(node):
        global dialog_box

        if dialog_box:
            dialog_box.destroy()
        
        def configure_value_node():
            value = (x.get(), y.get(), z.get())
            node.configure(text=str(value), value=value)
        
        dialog_box = customtkinter.CTkToplevel(root)
        dialog_box.resizable(False, False)
        dialog_box.transient(root)
        dialog_box.attributes("-alpha", 0.9)
        dialog_box.title("Configure XYZ")

        customtkinter.CTkLabel(dialog_box, text="X Coordinate").pack(padx=5, pady=10)
        x = CTkSpinbox(dialog_box, from_=-20, to=20, command=configure_value_node)
        x.pack(expand=True, fill="x", padx=5)
        x.set(node.get()[0])
        
        customtkinter.CTkLabel(dialog_box, text="Y Coordinate").pack(padx=5, pady=10)
        y = CTkSpinbox(dialog_box, from_=-20, to=20, command=configure_value_node)
        y.pack(expand=True, fill="x", padx=5)
        y.set(node.get()[1])
        
        customtkinter.CTkLabel(dialog_box, text="Z Coordinate").pack(padx=5, pady=10)
        z = CTkSpinbox(dialog_box, from_=-20, to=20, command=configure_value_node)
        z.pack(expand=True, fill="x", padx=5, pady=(0,10))
        z.set(node.get()[2])

        spawn_x = int(root.winfo_width() * .5 + root.winfo_x() - .5 * dialog_box.winfo_width() + 7)
        spawn_y = int(root.winfo_height() * .5 + root.winfo_y() - .5 * dialog_box.winfo_height() + 20)
        dialog_box.geometry(f"+{spawn_x}+{spawn_y}")

    def add_point():
        point_node = NodeValue(canvas, text=f"(0, 0, 0)", value=(0,0,0))
        point_node.bind("<Double-1>", lambda e: open_config_dialog(point_node))

    def add_side():
        side_node = NodeOperation(canvas, text=f"SIDE", inputs=1, multiple_connection=True,
                                  command=to_points, pass_node_id=True)
        side_node.bind("<Double-1>", lambda e: open_color_dialog(side_node))
        if global_side_color:
            side_node.configure(fg_color=global_side_color, text_color="black")
            
    def load_canvas():
        if open_file := filedialog.askopenfilename(filetypes=[
                            ("JSON", ["*.json"]),
                            ("All Files", "*.*")]):
            canvas.load(open_file)

            for i in canvas.node_list:
                if type(i) is NodeOperation:
                    i.bind("<Double-1>", lambda e, n=i: open_color_dialog(n))
                elif type(i) is NodeValue:
                    i.bind("<Double-1>", lambda e, n=i: open_config_dialog(n))
                    
    def save_canvas():
        save_file = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[('json', ['*.json']),('All Files', '*.*')])
        if save_file:
             canvas.save(save_file)
            
    frame_left = customtkinter.CTkFrame(tab)
    frame_left.pack(expand=True, fill="both", padx=10, pady=10, side="left")

    frame_right = customtkinter.CTkFrame(tab, width=500)
    frame_right.pack(fill="y", padx=(0,10), pady=10, side="right")
    
    geo[tab_num] = ThreeDFrame(frame_right, bg=frame_right.cget("fg_color")[1], 
                    coords=default_pyramid)
    geo[tab_num].pack(fill="both", expand=True)

    label = customtkinter.CTkLabel(frame_right, text="3D Viewer")
    label.pack(fill="x", pady=0)
    
    scale = customtkinter.CTkSlider(frame_right,
                                    from_=0,
                                    to=100,
                                    command=lambda e: geo[tab_num].configure(size=int(e)))
    scale.pack(padx=5, fill="x")
    scale.set(100)

    open_button = customtkinter.CTkButton(frame_right, text="OPEN", width=200, command=load_canvas)
    open_button.pack(fill="x", padx=(10,5), pady=10, side="left")

    save_button = customtkinter.CTkButton(frame_right, text="SAVE", width=200, command=save_canvas)
    save_button.pack(fill="x", padx=(5,10), pady=10, side="left")

    canvas = NodeCanvas(frame_left, bg=frame_left._fg_color[1], width=800, height=500)
    canvas.pack(expand=True, fill="both", padx=5, pady=5)
        
    comp = NodeCompile(canvas, fixed=True, text="Render",
                       multiple_connection=True, show_value=False,
                       command=join_coords)

    canvas.rowconfigure(0, weight=1)

    button_1 = customtkinter.CTkButton(canvas, text="Add Point", width=80, command=add_point)
    button_1.grid(pady=10, padx=10, sticky="se")

    button_2 = customtkinter.CTkButton(canvas, text="Add Side", width=80, command=add_side)
    button_2.grid(pady=10, padx=10, sticky="se")

def add_tab():
    global tab_num
    if tab_num>9:
        add_tab_button.configure(state="disabled")
        return
    tab_num +=1
    tab = ttk.Frame(notebook, takefocus=0)
    notebook.add(tab, text=f"Tab {tab_num}")
    add_content(tab, tab_num)

tab_num = 1
root = customtkinter.CTk()
root.title("3D Geometry Viewer")
root.geometry("1200x550")
root.resizable(False, False)
sv_ttk.set_theme("dark")
geo = {}
dialog_box = None
global_side_color = "#ffffff"
notebook = ttk.Notebook(root, takefocus=False)
notebook.pack(expand=True, fill="both")

default_pyramid = [[(0, 1, 0), (-1, -1, -1), (1, -1, 1), (-1, -1, 1), (1, -1, -1)],
                   [[2, 4, 1, 3, (255, 255, 255)]], [[3, 1, 4, 2, (255, 255, 255)]],
                   [[2, 0, 3, (255, 255, 255)]], [[3, 0, 2, (255, 255, 255)]],
                   [[2, 4, 0, (255, 255, 255)]], [[0, 4, 2, (255, 255, 255)]],
                   [[1, 4, 0, (255, 255, 255)]], [[0, 4, 1, (255, 255, 255)]],
                   [[3, 0, 1, (255, 255, 255)]], [[1, 0, 3, (255, 255, 255)]]]

tab_1 = ttk.Frame(notebook, takefocus=0)
notebook.add(tab_1, text=f"Tab 1")

add_content(tab_1, 1)

style = ttk.Style()

style.layout("Tab", [('Notebook.tab', {'sticky': 'nswe', 'children':
   [('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children':
      [('Notebook.label', {'side': 'top', 'sticky': ''})],
   })],
})]
)

add_tab_button = customtkinter.CTkButton(notebook, width=30, text="+",
                                         bg_color="#2f2f2f", command=add_tab)
add_tab_button.pack(anchor="ne", pady=5, padx=10)

root.mainloop()
