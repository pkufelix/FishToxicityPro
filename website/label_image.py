import numpy as np
import tensorflow as tf
import cv2
import os

def load_graph(model_file):
    graph = tf.Graph()
    graph_def = tf.GraphDef()
    with open(model_file, "rb") as f:
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

def read_tensor_from_image_file(file_name,
                                input_height=299,
                                input_width=299,
                                input_mean=0,
                                input_std=255):
    input_name = "file_reader"
    output_name = "normalized"
    file_reader = tf.read_file(file_name, input_name)
    if file_name.endswith(".png"):
        image_reader = tf.image.decode_png(file_reader, channels=3, name="png_reader")
    elif file_name.endswith(".gif"):
        image_reader = tf.squeeze(tf.image.decode_gif(file_reader, name="gif_reader"))
    elif file_name.endswith(".bmp"):
        image_reader = tf.image.decode_bmp(file_reader, name="bmp_reader")
    else:
        image_reader = tf.image.decode_jpeg(file_reader, channels=3, name="jpeg_reader")
    float_caster = tf.cast(image_reader, tf.float32)
    dims_expander = tf.expand_dims(float_caster, 0)
    resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
    normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
    sess = tf.Session()
    result = sess.run(normalized)
    sess.graph.finalize()
    return result

def label_image(filename):

    img = cv2.imread(filename)
    rows = img.shape[0]
    cols = img.shape[1]
    if rows > cols:
        rows = 400
        cols = 300
    else:
        rows = 300
        cols = 400
    img = cv2.resize(img,(cols,rows))
    basepath = os.path.dirname(__file__)
    cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)
    mercury = {'salmon': 'Mercury level (PPM): 0.022.', \
    'trout': 'Mercury level (PPM): 0.071.', \
    'white seabass': 'Mercury level (PPM): 0.354', \
    'rockfish': 'Mercury level (PPM): 0.167', \
    'tuna': 'Mercury level (PPM): 0.386', \
    'largemouth bass': 'Mercury level (PPM): 0.167', \
    'walleye': 'Methylmercury level (PPM): 0.16', \
    'channel catfish': 'Mercury level (PPM): 0.024', \
    'perch': 'Mercury level (PPM): 0.150', \
    'carp': 'Mercury level (PPM): 0.110', \
    'lake whitefish': 'Mercury level (PPM): 0.089', \
                'shad': 'Mercury level (PPM): 0.038'
    }
    sugg = {'salmon': 'Having 2 servings per week may be OK', \
    'trout': 'Having 2 servings per week may be OK', \
    'white seabass': 'Not suggested to eat more than 1 serving per a week', \
    'rockfish': 'Not suggested to eat more than 1 serving per a week', \
    'tuna': 'Women who are or may become pregnant, nursing mothers, and young children should NOT eat', \
    'largemouth bass': 'Not suggested to eat more than 1 serving per a week', \
    'walleye': 'Having 2 servings per week may be OK', \
    'channel catfish': 'Having 2 servings per week may be OK', \
    'perch': 'Not suggested to eat more than 1 serving per a week', \
    'carp': 'Not suggested to eat more than 1 serving per a week', \
    'lake whitefish': 'Not suggested to eat more than 1 serving per a week', \
    'shad': 'Having 2 servings per week may be OK'
    }
    
    
    file_name = filename
    model_file = "static/model/retrained_graph.pb"
    label_file = "static/model/retrained_labels.txt"
    input_layer = "Placeholder"
    output_layer = "final_result"
                        
    input_height = 299
    input_width = 299
    input_mean = 0
    input_std = 255
                                        
    graph = load_graph(model_file)
    labels = load_labels(label_file)
                                        
    t = read_tensor_from_image_file(
        file_name,
        input_height=input_height,
        input_width=input_width,
        input_mean=input_mean,
        input_std=input_std)
                                            
    input_name = "import/" + input_layer
    output_name = "import/" + output_layer
    input_operation = graph.get_operation_by_name(input_name)
    output_operation = graph.get_operation_by_name(output_name)

    with tf.Session(graph=graph) as sess:
        results = sess.run(output_operation.outputs[0], {input_operation.outputs[0]: t})
    results = np.squeeze(results)
    top_k = results.argsort()[-5:][::-1]
    outputs = []
    for i in top_k:
        outputs.append([labels[i],"%.3f" % (results[i])])
    return(outputs,mercury[outputs[0][0]],sugg[outputs[0][0]])
