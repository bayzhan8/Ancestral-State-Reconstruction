output = []
count = 0
correct = 0
zero_state = 0
not_present = 0
num_trees = 0

difference = defaultdict(int)
true_leaf_labels = [j.label for j in true_tree.taxon_namespace]

### Going over all trees in "reconstructed" folder
path  = 'reconstructed'
os.chdir(path)
for file_name in os.listdir():
    num_trees += 1
    file_path = f"{file_name}"
    with open(file_path, 'r') as f:
        lines = f.readlines()
    fake_treeS =  lines[2:-2]

#     ### If <0> is present, then 
#     stop = False
#     for j in fake_treeS:
#         if "<0>" in j:
#             zero_state += 1
#             stop = True
#             break
#     if stop:
#         continue
            
            
    for i in range(len(fake_treeS)): 
        print("Tree ", num_trees, ": ", i/len(fake_treeS)*100, "%")
        tree_i_FamilyID, tree_i = fake_treeS[i].split(" = ")
        tree_i = tree_i[:-1]
        tree_i_FamilyID = tree_i_FamilyID[7:]
        fake_tree_i = dendropy.Tree.get_from_string(tree_i, "newick")

        ### Map from true_tree leaves labels to fake_tree leaves labels
        fake_tree_labels = [j.label for j in fake_tree_i.taxon_namespace]
        mapping = defaultdict(int)
        for k in true_leaf_labels:
            for j in fake_tree_labels:
                if k in j:
                    mapping[k] = j

        ### For each particular internal node in the true tree, find its leaves
        for node in true_tree.internal_nodes()[1:]:
            leaves = node.leaf_nodes()
            fake_leaves_labels = [mapping[i.taxon.label] for i in leaves]
            fake_node = fake_tree_i.mrca(taxon_labels = fake_leaves_labels)
            ### Check if they have the same leaves
            fake_leaves_labels.sort()
            all_leaves_fake_node = [i.taxon.label for i in fake_node.leaf_nodes()]
            all_leaves_fake_node.sort()
            if all_leaves_fake_node == fake_leaves_labels:
                count += 1

                ### Compare
                arr = true_states[true_states["Family ID"] == tree_i_FamilyID].copy(deep=True)
                node_state = arr.reset_index().at[0, node.label]

                fake_node_label, fake_state = fake_node.label.split()
                fake_state = int(fake_state)

                if fake_state == node_state:
                    correct += 1

                difference[node_state - fake_state] += 1 
            else:
                not_present += 1

path = ".."
os.chdir(path)
