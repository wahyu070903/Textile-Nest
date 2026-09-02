import cv2
import numpy as np


class CannyMethod:
    def __init__(self):
        self.lower_threshold = 50
        self.upper_threshold = 150

    def process(self, image):

        if image is None:
            return None, 0, None

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        edges = cv2.Canny(blur, self.lower_threshold, self.upper_threshold)

        kernel = np.ones((5, 5), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(
            edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        result = np.zeros_like(edges)
        area = 0
        contour = None

        if contours:
            contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(contour)
            cv2.drawContours(result, [contour], -1, 255, 2)

        return result, area, contour