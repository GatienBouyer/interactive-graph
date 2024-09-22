"""
Start the tkinter app.
"""

import tkinter

from interactive_graph.app import App

if __name__ == "__main__":
    root = tkinter.Tk()
    App(root)
    root.mainloop()
