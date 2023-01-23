# One dice combos
one_combos = {("d1") : 100, ("d5") : 50}

# Two dice combos
two_combos = {("d1", "d1") : 200, ("d1", "d5") : 100, ("d5", "d5") : 100}

# Three dice combos
three_combos = {("d1", "d1", "d1") : 1000, ("d2", "d2", "d2") : 200, ("d3", "d3", "d3") : 300, ("d4", "d4", "d4") : 400, ("d5", "d5", "d5") : 500, ("d6", "d6", "d6") : 600}

# Four dice combos
four_combos = {k + (k[0],): 1000 for (k,v) in three_combos.items()}

# Five dice combos
five_combos = {k + (k[0],): 2000 for (k,v) in three_combos.items()}

