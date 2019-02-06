# pre-trained example information

def load_example(num):
    if num == 1:
    	result = [["salmon","0.739"],
        	   ["trout","0.217"],
                   ["shad","0.029"],
                   ["white seabass","0.007"],
                   ["channel catfish","0.002"]]
    	line2 = "Having 2 servings per week may be OK."
    	line1 = "Mercury level (PPM): 0.022."
    if num == 2:
        result = [["trout","0.931"],
                   ["rockfish","0.038"],
                   ["largemouth bass","0.011"],
                   ["channel catfish","0.005"],
                   ["walleye","0.004"]]
        line2 = "Having 2 servings per week may be OK."
        line1 = "Mercury level (PPM): 0.071."
    if num == 3:
        result = [["perch","0.748"],
                  ["carp","0.116"],
                  ["walleye","0.047"],
                  ["trout","0.033"],
                  ["largemouth bass","0.019"]]
        line2 = "Not recommended to eat more than 1 serving per a week."
        line1 = "Mercury level (PPM): 0.150."
    return result,line1,line2
