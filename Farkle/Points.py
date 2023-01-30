# One dice combos
one_combos = {("d1",) : 100, ("d5",) : 50}

# Two dice combos
two_combos = {("d1", "d1") : 200, ("d1", "d5") : 150, ("d5", "d5") : 100}

# Three dice combos
three_combos = {("d1", "d1", "d1") : 300, ("d2", "d2", "d2") : 200, ("d3", "d3", "d3") : 300, ("d4", "d4", "d4") : 400, ("d5", "d5", "d5") : 500, ("d6", "d6", "d6") : 600}

# Four dice combos
four_combos = {k + (k[0],): 1000 for k in three_combos.keys()}

# Five dice combos
five_combos = {k + (k[0],): 2000 for k in four_combos.keys()}

# Six dice combos
pair_tuples = [("d1", "d1"), ("d2", "d2"), ("d3", "d3"), ("d4", "d4"), ("d5", "d5"), ("d6", "d6")]
sixes = {k + (k[0],): 3000 for k in five_combos.keys()}
triplets = {}
for k in three_combos.keys():
    for v in three_combos.keys():
        if int(k[0][1]) < int(v[0][1]):
            triplets[k + v] = 2500
three_pairs = {}
for k in pair_tuples:
    for v in pair_tuples:
        for i in pair_tuples:
            if int(k[0][1]) < int(v[0][1]) < int(i[0][1]):
                three_pairs[k + v + i] = 1500
four_plus_pair = {}
for k in four_combos.keys():
    for v in pair_tuples:
        if k[0] != v[0]:
            four_plus_pair[k + v] = 1500
straights = {("d1", "d2", "d3", "d4", "d5", "d6") : 1500}
six_combos = {}
six_combos.update(triplets)
six_combos.update(three_pairs)
six_combos.update(four_plus_pair)
six_combos.update(straights)
six_combos.update(sixes)

def keeping(selected, one, two, three, four, five, six):
    """Determines if the selected list is in any of the points dictionaries"""
    sorted_selected = sorted(selected[:])
    index_dic = {1 : one, 2 : two, 3 : three, 4 : four, 5 : five, 6 : six}
    points = 0
    x = 0
    if selected == []:
        return False, points
    while len(sorted_selected) > 0:
        if len(sorted_selected) - x == 0:
            points = 0
            break
        for i in index_dic[len(sorted_selected) - x].keys():
            temp = sorted(i)
            if check_sublist(sorted_selected, temp):
                points += index_dic[len(sorted_selected) - x][i]
                for r in temp:
                    sorted_selected.remove(r)
                x = 0
                break
        else:
            x += 1

    return False if sorted_selected != [] else True, points

def check_sublist(list, sublist):
    """checks if sublist is a sublist of list"""
    a = list[:]
    b = sublist[:]
    for item in sublist:
        if item in a:
            b.remove(item)
            a.remove(item)
        else:
            return False
        if b == []:
            return True

def super_list(x):
    """Creates a list of all sublists of x"""
    result = []
    length = len(x)
    for r in range(length):
        for l in range(length):
            if length - l > r:
                result.append(x[r:length - l])
    return result

def has_farkled(super_set):
    for i in super_set:
        if keeping(i, one_combos, two_combos, three_combos, four_combos, five_combos, six_combos)[0]:
            return False
    return True


