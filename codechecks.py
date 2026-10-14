from pathlib import Path
import nbformat
import html
import numpy as np
from types import SimpleNamespace
import jupytext 
from scripts.checker import CodeChecker


from NB1 import (
    check_doorlopende_doos,
    check_harde_wanden,
    check_botsingsvoorwaarde,
    check_eindantwoord,
)

from NB2 import check_ex7

# def get_tagged_cell(notebook_path, tag):
#     nb = jupytext.read(notebook_path)

#     for cell in nb.cells:
#         if cell.cell_type != "code":
#             continue

#         if tag in cell.metadata.get("tags", []):
#             return cell.source

#     raise ValueError(f"Geen codecel gevonden met tag {tag!r}")

# CODE BELOW FOR .IPYNB NOTEBOOKS, NOT FOR .MD FILES
# def get_tagged_cell(notebook_path, tag):
#     nb = nbformat.read(notebook_path, as_version=4)

#     for cell in nb.cells:
#         if tag in cell.metadata.get("tags", []):
#             return cell.source

#     raise ValueError(f"Geen cel gevonden met tag {tag!r}")

results = []


def check_cell(name, notebook_path, test_function, with_previous_cells=False):

    try:
        checker = CodeChecker(notebook_path)

        plots, namespace = checker.checkWithTag(name, run_previous_cells=with_previous_cells)

        # Run the corresponding test from NB1.py
        test_function(namespace, plots)

        results.append((name, True, ""))
        print(f"PASS: {name}")

    except Exception as exc:
        results.append((name, False, str(exc)))
        print(f"FAIL: {name}: {exc}")


# Run all checks
notebook_1 = "simulations/NB1_deeltjesmodel.md"
notebook_2 = "simulations/NB2_brownianmotion.md"

check_cell("NB1_doorlopendedoos", notebook_1, check_doorlopende_doos)

check_cell("NB1_hardewand", notebook_1, check_harde_wanden)

check_cell("NB1_botsingsvoorwaarde", notebook_1, check_botsingsvoorwaarde)

check_cell("NB1_eindantwoord", notebook_1, check_eindantwoord)

check_cell("NB2_ex7", notebook_2, check_ex7, with_previous_cells=True)


##### GENERATE MARKDOWN REPORT #####
output = Path("codechecks.md")
output.parent.mkdir(parents=True, exist_ok=True)

with output.open("w") as f:
    f.write("# Notebook checks\n\n")
    f.write("| Check | Status | Details |\n")
    f.write("|-------|--------|---------|\n")

    for name, passed, message in results:
        status = "✅ PASS" if passed else "❌ FAIL"

        # Keep exception messages inside one Markdown table cell
        details = str(message).replace("|", r"\|").replace("\n", "<br>")

        f.write(f"| {name} | {status} | {details} |\n")
