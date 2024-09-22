import tkinter

from interactive_graph import visualization, work


class App:
    frame: tkinter.Frame
    canvas: None | tkinter.Canvas

    def __init__(self, root: tkinter.Misc) -> None:
        if isinstance(root, tkinter.Wm):
            root.wm_title("Demo app")
            root.geometry("600x400")
        self.frame = tkinter.Frame(root, name="mainframe", padx=10, pady=10)
        self.frame.pack(expand=True, fill="both")
        tkinter.Label(self.frame, name="title", text="Demo app",
                      justify="center").pack(padx=5, pady=5)
        tkinter.Button(self.frame, name="generateButton", command=self.generate,
                       text="Generate").pack(padx=5, pady=5)
        self.canvas = None
        self.refresh()

        self.frame.nametowidget("generateButton").invoke()

    def refresh(self) -> None:
        self.draw_graph()
        self.frame.after(1000, self.refresh)

    def generate(self) -> None:
        button: tkinter.Misc = self.frame.nametowidget("generateButton")
        button.destroy()
        self.canvas = tkinter.Canvas(self.frame, name="canvas", bg="white")
        self.canvas.pack(expand=True, fill="both")

    def draw_graph(self) -> None:
        if self.canvas is None:
            return
        self.canvas.delete("all")
        script = visualization.generate_tk_graph(work.graph)
        widget_pathname = self.canvas.winfo_pathname(self.canvas.winfo_id())
        self.canvas.tk.eval(f"set c {widget_pathname}")
        node_id = None
        for line in script.splitlines():
            if line.startswith("#"):
                node_id = line.split(" ")[1]
                if not node_id in work.graph.nodes():
                    node_id = None
                continue
            element_id = self.canvas.tk.eval(line)
            if node_id is not None:
                self.canvas.tag_bind(
                    element_id,
                    "<Button-1>",
                    lambda _, node_id=node_id: self.run(node_id),  # type: ignore[misc]
                )

    def run(self, node_id: str) -> None:
        work.do_operation(node_id)
