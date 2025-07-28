import os
import numpy as np
import cv2
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import platform
import pytesseract

screen_path = str()

system = platform.system()

if system == "Windows":
    screen_path = r"C:\Users\Timo\Pictures\Screenshots"
elif system == "Darwin":
    screen_path = r"/Users/timoneske/Documents/myrepo/dbd-ml/dpd-killer-perks/screens"

print(screen_path)

def read_screenshot():
    """
    Liest Screenshots aus einem angegebenen Verzeichnis und gibt eine Liste von PIL Image-Objekten zurück.
    :param path: Der Path zu den DBD-Screenshots
    :return: Liste von PIL Image-Objekten
    """
    screens = {}
    for dateiname in os.listdir(screen_path):
        if dateiname.lower().endswith(".png"):
            bildpfad = os.path.join(screen_path, dateiname)
            try:
                bild = Image.open(bildpfad)
                screens[dateiname] = bild
                print(f"{dateiname} geladen – Größe: {bild.size}, Format: {bild.format}")
                #bild.show()
            except Exception as e:
                print(f"Fehler beim Laden von {dateiname}: {e}")
    return screens

def extract_img(pil_img, box_points):
    """
    Schneidet aus einem PIL-Image einen rotierten rechteckigen Bereich aus.
    :param pil_img: PIL.Image.Image
    :param box_points: np.array mit 4 Punkten (x, y), z.B. von cv2.boxPoints(rect)
                       Die Reihenfolge: 4 Eckpunkte des Polygons
    :return: ausgeschnittener PIL.Image-Bereich (gerade)
    """
    # Konvertiere PIL zu OpenCV Bild (numpy array)
    x_coords = [p[0] for p in box_points]
    y_coords = [p[1] for p in box_points]
    min_x, max_x = int(min(x_coords)), int(max(x_coords))
    min_y, max_y = int(min(y_coords)), int(max(y_coords))

    # Crop-Bereich definieren (left, upper, right, lower)
    crop_box = (min_x, min_y, max_x, max_y)

    # Bild ausschneiden
    return pil_img.crop(crop_box)

def extract_raw_killer_name(name_section):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    name_section = ImageEnhance.Contrast(name_section).enhance(2)
    name_section = name_section.convert("L")
    name_section = name_section.filter(ImageFilter.MedianFilter())
    name_section = name_section.point(lambda p: 255 if p > 140 else 0)

    text = pytesseract.image_to_string(name_section, lang='deu')

    return text

def extract_killer_name(name_section):
    raw_text = extract_raw_killer_name(name_section)
    raw_text = raw_text.strip()
    print("Raw: ", raw_text)

    if raw_text.startswith("THE"):
        return raw_text.split(" ")[1].lower()
    else:
        trimmed_text = raw_text.split(" ")[1:]
        return ' '.join(trimmed_text).lower()

    return raw_text

def order_points(pts):
    # sortiere Punkte: zuerst links oben, rechts oben, rechts unten, links unten
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]  # links oben
    rect[2] = pts[np.argmax(s)]  # rechts unten

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # rechts oben
    rect[3] = pts[np.argmax(diff)]  # links unten

    return rect

def clean(filename):
    os.remove(f"{screen_path}\\{filename}")

def toPng():
    for dateiname in os.listdir(r"C:\Users\Timo\Desktop\dpd-killer-perks"):
        if dateiname.lower().endswith((".png", ".webp")):
            bildpfad = os.path.join(r"C:\Users\Timo\Desktop\dpd-killer-perks", dateiname)
            try:
                bild = Image.open(bildpfad)

                padding = (0, 10, 0, 10)
                bild = ImageOps.expand(bild, border=padding, fill=0)

                dateiname = dateiname.removesuffix(".webp")
                zielpfad = os.path.join(r"C:\Users\Timo\Documents\myrepos\dbd-ml\dpd-killer-perks\png", f"{dateiname}.png")
                bild.save(zielpfad, "PNG")
            except Exception as e:
                print(f"Fehler beim Laden von {dateiname}: {e}")
