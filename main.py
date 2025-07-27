import numpy as np
from extractor import read_screenshot, crop_rotated_rect, clean
from csv_maker import create_csv_from_perks

create_csv_from_perks("dpd-killer-perks/png", "killer_perks.csv")



