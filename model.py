import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
from PIL import ImageEnhance

def preprocess_image(pil_img, size=(28, 28)):
    """
    Wandelt ein PIL-Bild in einen normalisierten Graustufen-Vektor um.

    :param pil_img: PIL.Image Objekt
    :param size: gewünschte Zielgröße für das Bild (Default: 28x28)
    :return: 1D NumPy-Array (Vektor mit Werten zwischen 0 und 1)
    """
    # Alpha-Kanal entfernen, falls vorhanden
    if pil_img.mode == "RGBA":
        pil_img = pil_img.convert("RGB")

    # In Graustufen umwandeln
    pil_img = pil_img.convert("L")

    pil_img = adjust_contrast(pil_img)

    pil_img = adjust_brightness(pil_img)

    # Auf Zielgröße skalieren (optional)
    pil_img = pil_img.resize(size)

    # In NumPy-Array umwandeln
    arr = np.array(pil_img)

    # Normalisieren (Werte zwischen 0 und 1)
    arr = arr / 255.0

    # In Vektor umwandeln (flatten)
    vec = arr.flatten()

    return vec

def model_fit_transform(perks):
    df = pd.read_csv("killer_perks.csv")

    y = df["perk"].values
    X = df.drop(columns=["perk"]).values

    # k-NN-Modell erstellen (k=1, weil wir nur 1 Sample pro Klasse haben)
    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(X, y)

    labels = knn.predict(perks)

    return labels

def print_compare(expected):
    actual = pd.read_csv("killer_perks.csv")
    actual = actual[actual["perk"] == 'barbecue-chili']
    actual = actual.drop(columns=["perk"])

    # In NumPy-Array umwandeln und reshapen
    actual_img = actual.values[0].reshape(28, 28)
    expected_img = expected.reshape(28, 28)

    plt.subplot(1, 2, 1)
    plt.title("Actual perk")
    plt.imshow(actual_img, cmap="gray")

    plt.subplot(1, 2, 2)
    plt.title("Expected perk")
    plt.imshow(expected_img, cmap="gray")
    plt.show()

def print_processed(expected):
    """
    Zeigt das erwartete Bild in Graustufen an.

    :param expected: 1D NumPy-Array (Vektor mit Werten zwischen 0 und 1)
    """
    expected_img = expected.reshape(28, 28)
    plt.imshow(expected_img, cmap="gray")
    plt.title("Processed Image")
    plt.axis('off')
    plt.show()

def adjust_brightness(pil_img, factor=0.7):
    enhancer = ImageEnhance.Brightness(pil_img)
    return enhancer.enhance(factor)  # < 1 dunkler, > 1 heller

def adjust_contrast(pil_img, factor=4.4):
    enhancer = ImageEnhance.Contrast(pil_img)
    return enhancer.enhance(factor)  # > 1 = mehr Kontrast

