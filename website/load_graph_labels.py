# Load retrained model .pb file and retrained labels
# In Flask, only load mode and labels once to avoid memory leakage

import tensorflow as tf

def load_graph_labels():
    model_file = "static/model/retrained_graph.pb"
    label_file = "static/model/retrained_labels.txt"

    graph = tf.Graph()
    graph_def = tf.GraphDef()
    with open(model_file, "rb") as f:
        graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def)

    label = []
    proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
    for l in proto_as_ascii_lines:
        label.append(l.rstrip())
    del graph_def
    return graph, label
