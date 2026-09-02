import cv2
import numpy as np

class Camera:
    def __init__(self, port=0, width=None, height=None):
        self.port = port
        self.cap = cv2.VideoCapture(port, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open camera {port}")

        if width is not None:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)

        if height is not None:
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        self.aruco = cv2.aruco
        self.aruco_dictionary = self.aruco.getPredefinedDictionary(
            self.aruco.DICT_4X4_50
        )

        self.aruco_parameter = self.aruco.DetectorParameters()
        self.aruco_detector = self.aruco.ArucoDetector(
            self.aruco_dictionary,
            self.aruco_parameter
        )
        
        self.marker_realpos = np.float32([
            [0,0],      # top-left          all in mm (x,y) 
            [30,0],     # top-right         all in mm (x,y)
            [30,30],    # bottom-right      all in mm (x,y)
            [0,30],     # bottom-left       all in mm (x,y)
        ])

    def read(self):
        ret, frame = self.cap.read()
        frame_with_marker = self.marker_calibration(frame)
        return [ret, frame_with_marker]

    def isOpened(self):
        return self.cap.isOpened()

    def release(self):
        if self.cap.isOpened():
            self.cap.release()

    def reconnect(self):
        self.release()
        self.cap = cv2.VideoCapture(self.port)
        if self.cap.isOpened():
            return True
            
        return False

    def marker_calibration(self, frame):
        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        corners, ids, rejected = self.aruco_detector.detectMarkers(
            gray
        )

        if ids is None:
            return frame

        marker_centers = {}

        for corner, marker_id in zip(corners, ids.flatten()):

            marker_id = int(marker_id)

            if marker_id in [0, 1, 2, 3]:

                center = self.get_marker_center(corner)

                marker_centers[marker_id] = center

        self.aruco.drawDetectedMarkers(
            frame,
            corners,
            ids
        )

        if not all(
            marker_id in marker_centers
            for marker_id in [0, 1, 2, 3]
        ):
            return frame

        src = np.float32([
            marker_centers[0],
            marker_centers[1],
            marker_centers[2],
            marker_centers[3]
        ])

        dst = np.float32([
            [0, 0],
            [1920, 0],
            [1920, 1080],
            [0, 1080]
        ])

        H, status = cv2.findHomography(
            src,
            dst
        )

        if H is None:
            return frame

        warped = cv2.warpPerspective(
            frame,
            H,
            (1920, 1080),
            flags=cv2.INTER_CUBIC
        )

        return warped

    def get_marker_center(self, corner):
        pts = corner.reshape(4, 2)
        center = pts.mean(axis=0)
        return center

