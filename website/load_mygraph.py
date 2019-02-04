# Create a sepera load script so it only need to run once.
# Model file was loaded as graph and label file was loaded as labels

import tensorflow as tf

def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file,"rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph

def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label

def load_mygraph():
  model_file = "static/model/retrained_graph.pb"
  label_file = "static/model/retrained_labels.txt"
  graph = load_graph(model_file)
  labels = load_labels(label_file)
  return(graph, labels)


