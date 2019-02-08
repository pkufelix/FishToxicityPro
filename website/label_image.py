# Use retrained model to predict uploaded image
# return the probability matrix and strings back to html

import numpy as np
import math
import tensorflow as tf
import cv2
import os
from read_tensor_from_image_file import read_tensor_from_image_file

def label_image(filename, graph, labels):

    # Save a scaled image at static/images/test.jpg for later test
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

    # FDA mecury data
    mercury = {'salmon': 'Mercury level (PPM): 0.022.', \
    'trout': 'Mercury level (PPM): 0.071.', \
    'white seabass': 'Mercury level (PPM): 0.354.', \
    'rockfish': 'Mercury level (PPM): 0.167.', \
    'tuna': 'Mercury level (PPM): 0.386.', \
    'largemouth bass': 'Mercury level (PPM): 0.167.', \
    'walleye': 'Methylmercury level (PPM): 0.16.', \
    'channel catfish': 'Mercury level (PPM): 0.024.', \
    'perch': 'Mercury level (PPM): 0.150.', \
    'carp': 'Mercury level (PPM): 0.110.', \
    'lake whitefish': 'Mercury level (PPM): 0.089.', \
    'shad': 'Mercury level (PPM): 0.038.'
    }
    sugg = {'salmon': 'Having 2 servings per week may be OK.', \
    'trout': 'Having 2 servings per week may be OK.', \
    'white seabass': 'Not recommended to eat more than 1 serving per a week.', \
    'rockfish': 'Not recommended to eat more than 1 serving per a week.', \
    'tuna': 'Women who are or may become pregnant, nursing mothers, and young children should NOT eat.', \
    'largemouth bass': 'Not recommended to eat more than 1 serving per a week.', \
    'walleye': 'Having 2 servings per week may be OK.', \
    'channel catfish': 'Having 2 servings per week may be OK.', \
    'perch': 'Not recommended to eat more than 1 serving per a week.', \
    'carp': 'Not recommended to eat more than 1 serving per a week.', \
    'lake whitefish': 'Not recommended to eat more than 1 serving per a week.', \
    'shad': 'Having 2 servings per week may be OK.'
    }
    
    
    file_name = filename
    #model_file = "static/model/retrained_graph.pb"
    #label_file = "static/model/retrained_labels.txt"
    input_layer = "Placeholder"
    output_layer = "final_result"
                        
    input_height = 299
    input_width = 299
    input_mean = 0
    input_std = 255

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
    sess.close()
    del sess
    results = np.squeeze(results)
    top_k = results.argsort()[-5:][::-1]
    outputs = []
    for i in top_k:
        outputs.append([labels[i],"%2d%%" % math.floor(results[i]*100)])
    print(outputs)
    return(outputs,mercury[outputs[0][0]],sugg[outputs[0][0]])
