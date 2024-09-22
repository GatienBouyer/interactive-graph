# Demo for an interactive graph application

![Exeample of what the interactive graph looks like](exeample.png)

## Requirements

This project uses Python3.11 features.

You need to have [Graphviz](https://graphviz.org/) installed on your machine.

```
sudo apt install graphviz graphviz-dev
```

## Tech stack

-   Python
    -   [Tkinter](https://docs.python.org/3/library/tkinter.html)
    -   [NetworkX](https://networkx.org/)
-   Visualization
    -   [Graphviz](https://graphviz.org/)

## Quick start

Install the application

```sh
pip install -e .
```

To also install development dependencies

```sh
pip install -e .[dev]
```

Launch the tkinter application

```sh
python -m interactive_graph
```
