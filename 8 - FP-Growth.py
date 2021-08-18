# read dataset
dataset_file = open('./dataset.txt', 'r')
data_set = [line.strip().split(' ') for line in dataset_file.readlines()]
dataset_file.close()

data_set = data_set[:200]

# create the items tree
def create_tree(data_set):
    tree = {'itemset':{}}
    items_set = set()
    for transaction in data_set:
        node = tree

        for item in transaction:

            items_set.add(item)

            if item in node['itemset']:
                node['itemset'][item]['count'] += 1
                node = node['itemset'][item]

            else:
                node['itemset'][item] = {'count':1, 'itemset':{}}
                node = node['itemset'][item]
    return tree, items_set


def print_tree(t,s):
    if not isinstance(t,dict) and not isinstance(t,list):
        print ("--"*s+str(t))
    else:
        for key in t:
            print ("--"*s+str(key))
            if not isinstance(t,list):
                print_tree(t[key],s+1)


# check if all of the members of first list are in second list
# Ex1: first_list = [1,2] & second_list=[1,2,3,4,5] -> return True
# Ex2: first_list = [1,2] & second_list=[2,3,4,5] -> return False
def is_it_in(first_list, second_list):
    for i in first_list:
        if i not in second_list:
            return False
    
    return True


def conditional_fp(condition_patterns, main_item, min_freq):
    
    this_items_set = []

    # find items sets and show given paths
    # print('given path: ')
    for cp in condition_patterns:
        cp[0].remove(main_item)
        # print(cp[0],'-->',cp[1])
        for item in cp[0]:
            if item not in this_items_set:
                this_items_set.append(item)


    all_item_set_pos = {}
    item_set_code = 0
    for i in range(len(this_items_set)):
        for j in range(i,len(this_items_set)):
            # print(this_items_set[i:j+1])
            all_item_set_pos[item_set_code] = this_items_set[i:j+1]
            item_set_code += 1


    # print("find each pattern freq: ")
    item_set_freq_dic = {}
    for cp in condition_patterns:
        # print(cp[0],'-->',cp[1])
        for itset_code in all_item_set_pos:
            if is_it_in(all_item_set_pos[itset_code], cp[0]):

                if itset_code in item_set_freq_dic:
                    item_set_freq_dic[itset_code]['freq'] += cp[1]
                else:
                    item_set_freq_dic[itset_code] = {'it_set': all_item_set_pos[itset_code], 'freq': cp[1]}
                    # item_set_freq_dic[itset_code]['freq'] = cp[1]


    all_it_codes = [it_set_code for it_set_code in item_set_freq_dic]
    # print(all_it_codes)
    for it in all_it_codes:
        if item_set_freq_dic[it]['freq'] < min_freq:
            del item_set_freq_dic[it]


    return item_set_freq_dic

    
def dfs(tree, node_name, item, path, cand_patt):
    
    if node_name == item:
        cand_patt.append([path.copy(),tree['count']])
        return cand_patt

    else:
        for node in tree['itemset']:
            path.append(node)
            cand_patt = dfs(tree['itemset'][node], node, item, path, cand_patt)            
            path.pop()

    return cand_patt



def poss_patt(old_dataset, pair_num):
    # old_dataset = [['3','2'], ['5','8'], ['6','9']]
    # print(old_dataset,end='\n\n')
    
    pair_num = pair_num - 1

    if pair_num == 0:
        new_dataset = [[item] for item in old_dataset ]
        return new_dataset
        

    # get itemset
    all_itemset = []
    for item in old_dataset:
        # for item in i:
        if item not in all_itemset:
            all_itemset.append(item)

    # print(all_itemset,end='\n\n')
    new_dataset = []

    # make dataset with needed pairnumber
    for i in range(len(all_itemset)-pair_num):
        k = i+1
        for j in range(len(all_itemset)-i-pair_num):
            temp = [all_itemset[i]]
            for item in all_itemset[k:k+pair_num]:
                temp.append(item)
            
            new_dataset.append(temp)
            
            k += 1

    # print(new_dataset)
    return new_dataset



tree, items_set = create_tree(data_set)
# print_tree(tree,1)

total_count = len(items_set)
counter = 1
print('Items Number: ', total_count)


all_freq_itemsets = []
for item in items_set:
    print('Item: ', item, ':', counter,'of',total_count)
    
    counter += 1

    condition_patterns = dfs(tree, 'null', item, [], [])


    min_freq = 5
    item_set_freq_dic = conditional_fp(condition_patterns,item, min_freq)


    if len(item_set_freq_dic) > 0:
        
        for key in item_set_freq_dic:
            itemset = item_set_freq_dic[key]['it_set']
            
            if itemset not in all_freq_itemsets:
                all_freq_itemsets.append(itemset)
             
    print('-'*50)



for fq in all_freq_itemsets:
    freq_itemset = fq

    # for each frequent itemsets we calculate support and confidence
    if len(freq_itemset) == 1:
        continue


    for i in range(len(freq_itemset)):
        pos_patt = poss_patt(freq_itemset, i+1)

        for patt in pos_patt:
            temp_freq_itemset = freq_itemset.copy()

            # remove pattern from temp freq itemset
            for item in patt:
                
                temp_freq_itemset.remove(item)

            # Now we get the association rules
            if len(temp_freq_itemset) > 0:

                # print(patt,'-> ', temp_freq_itemset)

                contain_freq_itemset = 0
                contain_freq_itemset_and_patt = 0
                
                for trans in data_set:
                    if is_it_in(temp_freq_itemset, trans):
                        contain_freq_itemset += 1
                        if is_it_in(patt, trans):
                            contain_freq_itemset_and_patt += 1

                confidence = contain_freq_itemset_and_patt / contain_freq_itemset

                
                rule = [patt,temp_freq_itemset, confidence]

                # alert rules with confidence more than 0.8
                
                if confidence > 0.8:
                    print(set(rule[0]), '=>', set(rule[1]), '  Support = ', rule[2], '\t', '<---- More Likely ')
                else:
                    print(set(rule[0]), ' => ', set(rule[1]), '  Support = ', rule[2])
    print('*'*50)