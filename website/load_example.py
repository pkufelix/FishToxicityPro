# pre-trained example information

def load_example(num):
    if num == 1:
    	result = [["salmon","74%"],
        	   ["trout","22%"],
                   ["shad"," 3%"],
                   ["white seabass"," 1%"],
                   ["channel catfish"," 0%"]]
    	line2 = "Having 2 servings per week may be OK."
    	line1 = "Mercury level (PPM): 0.022."
    if num == 2:
        result = [["trout","93%"],
                   ["rockfish"," 4%"],
                   ["largemouth bass"," 1%"],
                   ["channel catfish"," 1%"],
                   ["walleye"," 0%"]]
        line2 = "Having 2 servings per week may be OK."
        line1 = "Mercury level (PPM): 0.071."
    if num == 3:
        result = [["perch","75%"],
                  ["carp","12%"],
                  ["walleye"," 5%"],
                  ["trout"," 3%"],
                  ["largemouth bass"," 2%"]]
        line2 = "Not recommended to eat more than 1 serving per a week."
        line1 = "Mercury level (PPM): 0.150."
    return result,line1,line2
