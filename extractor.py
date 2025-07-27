import os
import numpy as np
import cv2
from PIL import Image

screen_path = r"C:\Users\Timo\Pictures\Screenshots"

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
                # bild.show()
                return screens
            except Exception as e:
                print(f"Fehler beim Laden von {dateiname}: {e}")

def crop_rotated_rect(pil_img, box_points):
    """
    Schneidet aus einem PIL-Image einen rotierten rechteckigen Bereich aus.
    :param pil_img: PIL.Image.Image
    :param box_points: np.array mit 4 Punkten (x, y), z.B. von cv2.boxPoints(rect)
                       Die Reihenfolge: 4 Eckpunkte des Polygons
    :return: ausgeschnittener PIL.Image-Bereich (gerade)
    """
    # Konvertiere PIL zu OpenCV Bild (numpy array)
    img = np.array(pil_img)
    # Falls Bild RGBA ist, nur RGB (OpenCV erwartet BGR, aber wir bleiben bei RGB)
    if img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

    # Sortiere die Punkte in konsistenter Reihenfolge (tl, tr, br, bl)
    rect = order_points(box_points)

    # Breite und Höhe des Ziel-Rechtecks berechnen
    widthA = np.linalg.norm(rect[2] - rect[3])
    widthB = np.linalg.norm(rect[1] - rect[0])
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.linalg.norm(rect[1] - rect[2])
    heightB = np.linalg.norm(rect[0] - rect[3])
    maxHeight = max(int(heightA), int(heightB))

    # Zielpunkte (gerades Rechteck)
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]
    ], dtype="float32")

    # Perspektivische Transformationsmatrix
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(img, M, (maxWidth, maxHeight))

    # Zurück zu PIL Image
    gerade = Image.fromarray(warped)
    return gerade.rotate(58, expand=True)

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
                dateiname = dateiname.removesuffix(".webp")
                zielpfad = os.path.join(r"C:\Users\Timo\Desktop\dpd-killer-perks\png", f"{dateiname}.png")
                bild.save(zielpfad, "PNG")
            except Exception as e:
                print(f"Fehler beim Laden von {dateiname}: {e}")