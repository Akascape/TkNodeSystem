from tknodesystem import *
import tkinter

root = tkinter.Tk()

# Node Canvas
canvas = NodeCanvas(root)
canvas.pack(fill="both", expand=True)

# Node Types
NodeValue(canvas, x=0, y=10)
NodeOperation(canvas, x=150, y=1)
NodeCompile(canvas, x=300, y=10)

# Node Menu
menu = NodeMenu(canvas) # right click or press <space> to spawn the node menu
menu.add_node(label="NodeValue", command=lambda: NodeValue(canvas))
menu.add_node(label="NodeOperation", command=lambda: NodeOperation(canvas))
menu.add_node(label="NodeCompile", command=lambda: NodeCompile(canvas))

root.mainloop()
