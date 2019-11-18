import cv2
import numpy as np


class ExtractExudates:
    jpegImg = 0
    grayImg = 0
    curImg = 0

    def setImage(self, img):
        self.jpegImg = img
        self.curImg = np.array(img)

    def getImage(self):
        return self.curImg

    def greenComp(self):
        gcImg = self.curImg[:, :, 1]
        self.curImg = gcImg

    def applyCLAHE(self):
        clahe = cv2.createCLAHE()
        clImg = clahe.apply(self.curImg)
        self.curImg = clImg

    def applyDilation(self):
        strEl = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))

        dilateImg = cv2.dilate(self.curImg, strEl)
        self.curImg = dilateImg

    def applyThreshold(self):
        retValue, threshImg = cv2.threshold(self.curImg, 220, 220, cv2.THRESH_BINARY)
        self.curImg = threshImg

    def applyMedianFilter(self):
        medianImg = cv2.medianBlur(self.curImg, 5)
        self.curImg = medianImg
