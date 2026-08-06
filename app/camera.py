import cv2


class Camera:
    def __init__(self, port=0, width=None, height=None):
        self.port = port
        self.cap = cv2.VideoCapture(port)

        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open camera {port}")

        if width is not None:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)

        if height is not None:
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def read(self):
        return self.cap.read()

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