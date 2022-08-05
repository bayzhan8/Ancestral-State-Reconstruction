## RECONSTRUCTING TREES

import os
import subprocess

### Reading the trees file
with open('trees.newick') as f:
    lines = f.readlines()
trees = lines[0].split("__")
trees.pop()

### Iterating over trees 
for i in range(0, 150, 30):
    ### Scaling the tree[i] by 1000 and saving as temp_tree.txt
    tree = trees[i]
    new_tree = ''
    i = 0
    while(i < len(tree)):
        if tree[i] == ":":
            new_tree += tree[i]
            num = ''
            i+=1
            while tree[i] != "," and tree[i] != ")":
                num += tree[i]
                i+=1
            new_tree += str(1000*float(num))
        new_tree += tree[i]
        i+=1

    with open("temp_tree.txt", "w") as new:
        new.write(new_tree)
    
    ### Reconstructing the states for tree[i] and moving to a different folder
    subprocess.run(["cafe5", "-i", "leaves_states.txt", "-t", "temp_tree.txt"])
    new_name = "reconstructed/tree_" + str(i) + ".tre"
    shutil.move("results/Base_asr.tre", new_name)