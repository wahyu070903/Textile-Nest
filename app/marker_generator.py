import cv2
import numpy as np

aruco = cv2.aruco 
dictionary = cv2.aruco.getPredefinedDictionary(
    aruco.DICT_4X4_50
)

for marker_id in range(4):
    marker = aruco.generateImageMarker(
        dictionary,
        marker_id,
        300
    )

    cv2.imwrite(
        f"marker/aruco_{marker_id}.png",
        marker
    )