from extractor import read_screenshot, extract_img, clean
from model import preprocess_image, model_fit_transform, print_compare
from csv_maker import create_csv_from_perks
from locations import *

#create_csv_from_perks("dpd-killer-perks/png", "killer_perks.csv")

screens = read_screenshot()

for (filename, data) in screens.items():
    perk_1 = extract_img(data, PERK_1_LOC)
    perk_2 = extract_img(data, PERK_2_LOC)
    perk_3 = extract_img(data, PERK_3_LOC)
    perk_4 = extract_img(data, PERK_4_LOC)

    unlabeled_1 = preprocess_image(perk_1)
    unlabeled_2 = preprocess_image(perk_2)
    unlabeled_3 = preprocess_image(perk_3)
    unlabeled_4 = preprocess_image(perk_4)

    print_compare(unlabeled_1.reshape(1,-1))

    perks_data = [unlabeled_1, unlabeled_2, unlabeled_3, unlabeled_4]

    labels = model_fit_transform(perks_data)

    for i in range(0, len(labels)):
        print(f"Perk {str(i+1)} predicted as: {labels[i]}")











