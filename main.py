from model import preprocess_image, model_fit_transform, print_compare, print_processed
from csv_maker import create_csv_from_perks
from locations import *
from extractor import *
import pandas as pd

#create_csv_from_perks("dpd-killer-perks/png", "killer_perks.csv")
screens = read_screenshot()
match_data = pd.read_excel("match_data.xlsx")

j = 1
for (filename, data) in screens.items():
    killer_name_section = extract_img(data, KILLER_NAME_LOC)
    extracted_killer_name = extract_killer_name(killer_name_section)

    perk_1 = extract_img(data, PERK_1_LOC)
    perk_2 = extract_img(data, PERK_2_LOC)
    perk_3 = extract_img(data, PERK_3_LOC)
    perk_4 = extract_img(data, PERK_4_LOC)

    unlabeled_1 = preprocess_image(perk_1)
    unlabeled_2 = preprocess_image(perk_2)
    unlabeled_3 = preprocess_image(perk_3)
    unlabeled_4 = preprocess_image(perk_4)

    print_processed(unlabeled_1.reshape(1,-1))

    perks_data = [unlabeled_1, unlabeled_2, unlabeled_3, unlabeled_4]

    labels = model_fit_transform(perks_data)

    print(f"Prediction for Screenshot {j} '{filename}':")
    for i in range(0, len(labels)):
        print(f"Perk {str(i+1)} predicted as: {labels[i]}")
    j+=1











