import xml.etree.ElementTree as eltree


def parse_cplex_sol_file(sol_path):
    tree = eltree.parse(sol_path)
    root = tree.getroot()

    # Containers for mapping results
    values = {}

    for variable in root.iter("variable"):
        name = variable.attrib["name"]
        value = float(variable.attrib["value"])
        values[name] = value

    # Parse back deltaA and deltaB
    selected_A = [int(name.split("_")[1]) for name, val in values.items()
                  if name.startswith("deltaA_") and val > 0.5]
    selected_B = [int(name.split("_")[1]) for name, val in values.items()
                  if name.startswith("deltaB_") and val > 0.5]

    return selected_A, selected_B


def parse_plaintext_sol_file(file_path):
    selected_A = []
    selected_B = []

    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):  # Skip comments or empty lines
                continue
            parts = line.split()
            if len(parts) != 2:
                continue
            var_name, value = parts
            if float(value) > 0.5:
                if var_name.startswith("deltaA_"):
                    index = int(var_name.split("_")[1])
                    selected_A.append(index)
                elif var_name.startswith("deltaB_"):
                    index = int(var_name.split("_")[1])
                    selected_B.append(index)

    return selected_A, selected_B
