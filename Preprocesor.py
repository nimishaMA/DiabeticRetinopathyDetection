import os

import cv2
import numpy as np

from Exudates import ExtractExudates


class Preprocessor:

    def process(self, img):
        img = self.extract_features(img)
        return self.find_components(img)

    def extract_features(self, img):
        exudates_processor = ExtractExudates()
        exudates_processor.setImage(img)
        exudates_processor.greenComp()
        img = exudates_processor.getImage()
        self.show_img("green component", img)
        exudates_processor.applyCLAHE()
        img = exudates_processor.getImage()
        self.show_img("Histogram Equalized", img)
        exudates_processor.applyDilation()
        img = exudates_processor.getImage()
        self.show_img("Dilation", img)
        exudates_processor.applyThreshold()
        img = exudates_processor.getImage()
        self.show_img("Threshold", img)
        exudates_processor.applyMedianFilter()
        img = exudates_processor.getImage()
        self.show_img("MedianFilter", img)
        return img

    def find_components(self, img):
        ret, labels = cv2.connectedComponents(img)
        print(ret, labels)
        label_hue = np.uint8(179 * labels / np.max(labels))
        blank_ch = 255 * np.ones_like(label_hue)
        labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

        # cvt to BGR for display
        labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

        # set bg label to black
        labeled_img[label_hue == 0] = 0

        labeled_img = cv2.resize(labeled_img, (822, 612))
        # cv2.waitKey()
        return labeled_img

    def show_img(self, name, img):
        try:
            img = cv2.resize(img, (822, 612))
            cv2.imshow(name, img)
        except Exception as ex:
            print(ex)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    base_path = r'C:\Users\User\Documents\Retinopathy\diabetic retinopathy images'
    img_dir = "Normal"
    train_dir = "train_data"
    dir_img_dir = train_dir + "/" + img_dir
    if not os.path.exists(dir_img_dir):
        os.makedirs(dir_img_dir)
    prepros = Preprocessor()
    index = 1
    path = os.path.join(base_path, img_dir)
    for img_f in os.listdir(path):
        img_f = os.path.join(path, img_f)
        img = cv2.imread(img_f)
        labeled_img = prepros.process(img)
        cv2.imwrite(os.path.join(dir_img_dir, 'labeled_' + str(index) + '.png'), labeled_img)
        index += 1
