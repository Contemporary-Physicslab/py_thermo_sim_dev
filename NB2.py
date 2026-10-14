# This file is used to automatically test python functions and code in students' work for NB1.

def check_ex7(namespace, plots):
    assert len(plots) == 1, f"Expected 1 plot, found {len(plots)}."
    plot = plots[0]
    assert plot.get_xlabel() != "" and plot.get_ylabel() != "", "Plot must have x and y labels."
    assert len(plot.lines) > 0, "Plot must not be empty."