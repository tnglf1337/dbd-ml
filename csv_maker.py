import os
import csv
import numpy as np
from PIL import Image

def create_csv_from_perks(image_folder, output_csv, image_size=(28, 28)):
    with open(output_csv, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)

        # Header: pixel_0, pixel_1, ..., pixel_783, label
        num_pixels = image_size[0] * image_size[1]
        header = [f"pixel_{i}" for i in range(num_pixels)] + ["label"]
        writer.writerow(header)

        for filename in os.listdir(image_folder):
            if filename.lower().endswith(".png"):
                label = filename.removesuffix(".png")
                filepath = os.path.join(image_folder, filename)

                try:
                    img = Image.open(filepath).convert("L").resize(image_size)
                    flat = np.array(img).flatten() / 255.0  # Normalisiert
                    writer.writerow(list(flat) + [label])
                    print(f"Gespeichert: {filename} → Label: {label}")
                except Exception as e:
                    print(f"Fehler bei {filename}: {e}")

    print(f"\n✅ CSV-Datei erstellt: {output_csv}")
