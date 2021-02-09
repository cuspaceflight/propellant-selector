"""
Takes an input NIST file and a Propellant, and creates polynomials for all the \
relevant variables
"""
from numpy import polyfit, poly1d
from phase import Phase
import numpy as np
import os.path
import warnings
import csv

warnings.simplefilter('ignore', np.RankWarning)

POLY_DEG = 10


def get_data(filename):
    rel_path = f"{filename}.csv"
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path) as csvfile:
        split_data = list(csv.reader(csvfile))
    return split_data[1:]


def get_fit(data, position, degree):
    temperatures = []
    values = []

    for row in data:
        if len(row) <= position:
            continue
        if row[0] == "undefined":
            continue
        if row[position] == "undefined":
            continue
        temperatures.append(float(row[0]))
        values.append(float(row[position]))

    if len(temperatures) == 0:
        return None
    if degree > len(temperatures):
        coeffs = polyfit(temperatures, values, len(temperatures))
    else:
        coeffs = polyfit(temperatures, values, degree)

    return poly1d(coeffs)


def propellant_data(propellant, filename):
    # "I don't like this being a function with side effects but I don't want to
    # refactor it so I'll let it slide" - Tim Clifford, unsatisfied code reviewer
    split_data = get_data(f"prop-data/{filename}")

    # values for position of each data type are hard coded and manually read
    # from file
    if propellant.phase == Phase.TWO_PHASE:
        propellant.F_pressure       = get_fit(split_data, 1, POLY_DEG)
        propellant.F_density_liquid = get_fit(split_data, 2, POLY_DEG)
        propellant.F_density_vapour = get_fit(split_data, 14, POLY_DEG)
    elif propellant.phase == Phase.LIQUID:
        propellant.F_pressure       = get_fit(split_data, 1, POLY_DEG)
        propellant.F_density_liquid = get_fit(split_data, 2, POLY_DEG)


def combo_data(propellant_mix, filename):
    split_data = get_data(f"combo-data/{filename}")

    data = []
    for row in split_data:
        if row[0] == propellant_mix.oxidiser_name and row[1] == propellant_mix.fuel_name:
            data = row
            break
    propellant_mix.ISP_sea_level  = float(row[3])
    propellant_mix.OF_molar_ratio = float(row[2])
    propellant_mix.chamber_temp   = float(row[4])
    propellant_mix.exhaust_temp   = float(row[5])
