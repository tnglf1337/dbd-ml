import numpy as np

y_offset = 900
x_offset_perk_2 = 74
x_offset_perk_3 = x_offset_perk_2 * 2
x_offset_perk_4 = x_offset_perk_2 * 3 - 2

PERK_1_LOC = np.array([
    [250, 150+y_offset],
    [224, 185+y_offset],
    [290, 210+y_offset],
    [224, 215+y_offset]
], dtype="float32")

PERK_2_LOC = np.array([
    [250 + x_offset_perk_2, 150 + y_offset],
    [224 + x_offset_perk_2, 185 + y_offset],
    [290 + x_offset_perk_2, 210 + y_offset],
    [224 + x_offset_perk_2, 215 + y_offset]
], dtype="float32")

PERK_3_LOC = np.array([
    [250 + x_offset_perk_3, 150 + y_offset],
    [224 + x_offset_perk_3, 185 + y_offset],
    [290 + x_offset_perk_3, 210 + y_offset],
    [224 + x_offset_perk_3, 215 + y_offset]
], dtype="float32")

PERK_4_LOC = np.array([
    [250 + x_offset_perk_4, 150 + y_offset],
    [224 + x_offset_perk_4, 185 + y_offset],
    [290 + x_offset_perk_4, 210 + y_offset],
    [224 + x_offset_perk_4, 215 + y_offset]
], dtype="float32")