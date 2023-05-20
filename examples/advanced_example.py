# Advanced Example of TkNodeSystem
# Author: Akash Bora
# License: MIT

from PIL import ImageEnhance, Image # pip install pillow
import customtkinter
from tknodesystem import *
import tkinter

root = customtkinter.CTk()
root.title("Image Enhancement")

frame_left = customtkinter.CTkFrame(root)
frame_left.pack(expand=True, fill="both", padx=10, pady=10, side="left")

frame_right = customtkinter.CTkFrame(root)
frame_right.pack(expand=True, fill="both", padx=10, pady=10, side="right")

image_label = customtkinter.CTkLabel(frame_right, corner_radius=20, width=600, height=400, text="")
image_label.pack(expand=True, fill="both", padx=5, pady=10)

label = customtkinter.CTkLabel(frame_right, text="Image Viewer")
label.pack(expand=True, fill="both", padx=5, pady=0)

canvas = NodeCanvas(frame_left, bg=frame_left._fg_color[1], width=800, height=500)
canvas.pack(expand=True, fill="both", padx=5, pady=5)

sliders = {}
x = 1
img = None

def show_current_slider(node, num):
    """ command when a node is clicked, places only the required slider """
    for i in sliders.values():
        i.pack_forget()

    sliders[num].pack(expand=True, fill="x", padx=20, pady=5, side="bottom")
    label.configure(text=node.text)
    
def add_slider(num, node):
    """ add some sliders when a new node is placed """
    def update(e):
        node.update()
        label.configure(text=f"{node.text}: {round(e,2)}")
                               
    sliders[num] = customtkinter.CTkSlider(frame_right, from_=0, to=10, command=lambda e: update(e))
    sliders[num].pack(expand=True, fill="x", padx=20, pady=5, side="bottom")
    sliders[num].set(1)
    
def input_media():
    """ input node which contains a file data """
    file = tkinter.filedialog.askopenfilename(filetypes =[('Images', ['*.png','*.jpg','*.jpeg','*.bmp','*webp']),('All Files', '*.*')])
    if file:
        NodeValue(canvas, value=Image.open(file), text="MediaIn")
        
def add_effect(effect):
    """ node operations """
    global x
    def image_modify(img, value):
        try:
            if effect=="Brightness":
                mode = ImageEnhance.Brightness(img)
            elif effect=="Contrast":
                mode = ImageEnhance.Contrast(img)
            elif effect=="Sharpness":
                mode = ImageEnhance.Sharpness(img)
            elif effect=="Color":
                mode = ImageEnhance.Color(img)

            return mode.enhance(sliders[value].get())
        except AttributeError: None
            
    value = x 
    node = NodeOperation(canvas, inputs=1,  text=effect, command=lambda img: image_modify(img, value),
                         click_command=lambda: show_current_slider(node, value))
    label.configure(text=node.text)
    add_slider(value, node)
    x += 1
    
def show_image(output):
    """ compile operation: shows the output image """

    global img
    label_height = 400
    ratio = output.size[1]/output.size[0]
    if ratio>1.5: ratio = 1.5
    if ratio<0.5: ratio = 0.5
    img = customtkinter.CTkImage(output, size=(label_height, label_height*ratio))
    image_label.configure(image=img)
    
menu = NodeMenu(canvas) # right click or press <space> to spawn the node menu
menu.add_node(label="Media Import", command=input_media)
menu.add_node(label="Media Out", command=lambda: NodeCompile(canvas, text="MediaOut", show_value=None, command=show_image))
menu.add_node(label="Brightness", command=lambda: add_effect("Brightness"))
menu.add_node(label="Contrast", command=lambda: add_effect("Contrast"))
menu.add_node(label="Color", command=lambda: add_effect("Color"))
menu.add_node(label="Sharpness", command=lambda: add_effect("Sharpness"))

root.mainloop()
