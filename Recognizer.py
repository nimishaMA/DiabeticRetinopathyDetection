import numpy as np
import tensorflow as tf

from label_image import load_graph, read_tensor_from_image_file, load_labels

MODEL_FILE = 'train_model/output_graph.pb'
LABEL_FILE = 'train_model/output_labels.txt'
INPUT_HEIGHT = 299
INPUT_WIDTH = 299
INPUT_MEAN = 0
INPUT_STD = 255
INPUT_LAYER = "Placeholder"
OUTPUT_LAYER = "final_result"


class Recognizer:

    def __init__(self):
        self.sess = None

    def recognize(self, file_name, graph):
        t = read_tensor_from_image_file(
            file_name,
            input_height=INPUT_HEIGHT,
            input_width=INPUT_WIDTH,
            input_mean=INPUT_MEAN,
            input_std=INPUT_STD)

        input_name = "import/" + INPUT_LAYER
        output_name = "import/" + OUTPUT_LAYER
        input_operation = graph.get_operation_by_name(input_name)
        output_operation = graph.get_operation_by_name(output_name)

        results = self.sess.run(output_operation.outputs[0], {
            input_operation.outputs[0]: t
        })
        results = np.squeeze(results)

        top_k = results.argsort()[-5:][::-1]
        labels = load_labels(LABEL_FILE)
        # for i in top_k:
        #     print(labels[i], results[i])
        k = top_k[0]
        return labels[k]

    def recognize_disease(self, img):

        graph = load_graph(MODEL_FILE)

        with tf.Session(graph=graph) as self.sess:
            disease = self.recognize(img, graph)

        return disease
