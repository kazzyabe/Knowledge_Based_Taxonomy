RULES = [
    (#1 If has spine, vertebrate. Necessary?:"is-invertebrate ?animal False"
        "has-spine-implies-vertebrate", 
        ["has-spine ?animal True"], 
        ["is-vertebrate ?animal True"]
    ),
    (#2 If has no spine, not vertebrate. (invertebrate) Necessary?:"is-invertebrate ?animal True"
        "has-no-spine-implies-invertebrate",
        ["has-spine ?animal False"],
        ["is-vertebrate ?animal False"]
    ),
    (#3 if can control body temp, warm blooded
        "can-control-body-temp-implies-warm-blooded",
        ["can-control-body-temp ?animal True"],
        ["is-warm-blooded ?animal True",
             "is-amphibian ?animal False", "is-fish ?animal False", "is-reptile ?animal False"
        ]
    ),
    (#4 if cannnot control body temp, not warm blooded (cold blooded)
        "cannot-control-body-tmp-implies-cold-blooded",
        ["can-control-body-temp ?animal False"],
        ["is-warm-blooded ?animal False"
            "is-bird ?animal False", "is-mammal ?animal False",
        ]
    ),
    (#5 if born from egg, oviparous(animals born from egg) (includes amphibian, fish, reptiles,birds)
        "born-from-egg-implies-oviparous",
        ["born-from-egg ?animal True"],
        ["is-oviparous ?animal True"]
    ),
    (#6 if born as live, viviparous (animals give birth to live offsprings) (includes mammals)
        "not-born-from-egg-implies-viviparous",
        ["born-from-egg ?animal False"],
        ["is-oviparous ?animal False"]
    ),
    (#7 if breath throughout gills at some point in a life, gill-breathing
        "breath-through-gill-implies-gill-breathing",
        ["breath-through-gill ?animal True"],
        ["gill-breathing ?animal True"]
    ),
    (#7b if not breath throughout gills at some point in a life, gill-breathing false
        "not-breath-through-gill-implies-gill-breathing",
        ["breath-through-gill ?animal False"],
        ["gill-breathing ?animal False"]
    ),
    (#8 if breath throughout lungs at some point in a life, lung-breathing
        "breath-through-lung-implies-lung-breathing",
        ["breath-through-lung ?animal True"],
        ["lung-breathing ?animal True"]
    ),
    (#8b if not breath throughout lungs at some point in a life, lung-breathing false
        "not-breath-through-lung-implies-lung-breathing",
        ["breath-through-lung ?animal False"],
        ["lung-breathing ?animal False"]
    ),
    (#9 if breath throughout skin at some point in a life, skin-breathing
        "breath-through-skin-implies-skin-breathing",
        ["breath-through-skin ?animal True"],
        ["skin-breathing ?animal True"]
    ),
    (#10 if vertebrate, warm-blooded, viviparous (not oviparous), then mammals
        "vertebrate-warm-blooded-viviparous-imply-mammal",
        ["is-vertebrate ?animal True", "is-warm-blooded ?animal True", "is-oviparous ?animal False"],
        ["is-mammal ?animal True"]
    ),
    (#11 if vertebrate, warm-blooded, oviparous, then bird
        "vertebrate-warm-blooded-oviparous-imply-bird",
        ["is-vertebrate ?animal True", "is-warm-blooded ?animal True", "is-oviparous ?animal True"],
        ["is-bird ?animal True"]
    ),
    (#12 if vertebrate, cold-blooded, gills, not lung, then fish
        "vertebrate-cold-blooded-gills-not-lung-imply-fish",
        [
            "is-vertebrate ?animal True", 
            "is-warm-blooded ?animal False", 
            "gill-breathing ?animal True",
            "lung-breathing ?animal False"
        ],
        ["is-fish ?animal True"]
    ),
    (#12 if vertebrate, cold-blooded, not gills, lung, then reptile
        "vertebrate-cold-blooded-not-gills-lung-imply-reptile",
        [
            "is-vertebrate ?animal True", 
            "is-warm-blooded ?animal False", 
            "gill-breathing ?animal False",
            "lung-breathing ?animal True"
        ],
        ["is-reptile ?animal True"]
    ),
    (#12 if vertebrate, cold-blooded, gills, lung, skin, then amphibian
        "vertebrate-cold-blooded-gills-lung-imply-reptile",
        [
            "is-vertebrate ?animal True", 
            "is-warm-blooded ?animal False", 
            "gill-breathing ?animal True",
            "lung-breathing ?animal True"
        ],
        ["is-amphibian ?animal True"]
    )
]

def run_ps(wm, rules):
    """
    Input:
        wm: working memory
        rules: a list of rules
    """

def substitute(subs, pattern):
    """
    Input 
        substitution: 
            eg. [('?y', 'mary'), ('?x', 'john')] 
        pattern: 
            eg. '?x gave (son-of ?y) ?z' 
    Output: 
        eg. 'john gave (son-of mary) ?z
    """
    pattern = pattern.split()
    for s in subs:
        i = 0
        while i < len(pattern):
            if pattern[i] == s[0]:
                pattern[i] = s[1]
            i += 1
    
    return " ".join(pattern)
        
def is_var (string):
    """check if the string is a variable"""
    if (string[0] == '?'):
        return True
    return False

def unify(pattern1, pattern2, subs):
    """
    Input:
        two patterns and a substitution 
    Output:
        subs: an updated substitution (possibly the empty list) or False.
    
    example: 
        subs = []
        pattern1 = "has-spine ?animal True"
        pattern2 = "has-spine dog True"

        subs = unify(pattern1,pattern2,subs)
        (subs =  [('?animal', 'dog')])

    """
    pattern1 = pattern1.split()
    pattern2 = pattern2.split()

    var = [] # a list for recording variable positions
    matching = True # a flag for checking if the two patterns matching

    if len(pattern1) == len(pattern2):
        for i in range(len(pattern1)):
            if is_var(pattern1[i]) or is_var(pattern2[i]):
                var.append(i)
            else:
                if pattern1[i] != pattern2[i]:
                    matching = False
        
        if matching:
            for i in var:
                if is_var(pattern1[i]) and (not is_var(pattern2[i])):
                    subs.append((pattern1[i],pattern2[i]))
                elif is_var(pattern2[i]) and (not is_var(pattern1[i])):
                    subs.append((pattern2[i],pattern1[i]))
                else:
                    subs = False
        else:
            subs = False
    
    return subs

def match_antecedent(anteceds, wm, sub):
    """
    Input:
        anteceds: a list of antecedents still to be matched
        wm: a working memory
        subs: substitution
    Output:
        all possible new states (a list of remaining antecedents and a substition) which can be reached by matching the first antecedent in the list
    
    * uses unify() to attempt to match the antecedent against each pattern in the wm
    """
    antec = anteceds[0]

    def ma_helper(states, wm_left):
        # print("---------- ma_helper --------")
        # print("states = ", states)
        # print("sub = ", sub)
        if wm_left == []: # If wm_left is empty return states.
            # print("end case: ", states)
            return states
        else: # Otherwise attempt to unify antec with next pattern in wm_left in the context of sub.
            wm_head = wm[0]
            possible_subs = unify(antec,wm_head, sub)

            if possible_subs == False: # If unification fails, call ma_helper on the same list of states and the rest of wm_left.
                ma_helper(states, wm_left[1:])
            else: # If unification succeeds, call ma_helper with the new state combined onto states and the rest of wm_left.
                for s in possible_subs: # update sub
                    if s not in sub:
                        sub.append(s)
                
                new_state = substitute(sub, antec) #(The new state includes the remaining antecedents and whatever new substitution resulted from the unification.)
                states.append(new_state)

                # to take care of len(wm_left) == 1
                if len(wm_left) > 2:
                    wm_left = wm_left[1:]
                else:
                    wm_left = []
                return ma_helper(states, wm_left)
    return ma_helper([], wm)

def execute(subs,patterns,wm):
    """
    Input:
        subs: a list of substitutions
        patterns: a list of patterns (RHS of the rules)
        wm: working memory
    Output:
        an acuumulated list of new patterns derived from substitution
    """
    res = [] 

    for p in patterns:
        tmp = substitute(subs, p)
        if tmp not in wm:
            res.append(tmp)
    
    return res

def update_wm(wm, updates):
    for u in updates:
        wm.append(u)
    return wm

# def match_rule (name, lhs, rhs, wm):
#       #print some useful messages here
#       def mr_helper (queue, new_wm):
#            # Each state in queue is
#            # (anteceds-left, subs)
#                         # if the queue is empty, return new_wm

 

#                         # else examine the first item in the queue (call it state1)

#                         #      If state1 has no antecedents, state1 is a goal state (the rule is matched);

#                         #      call "execute" on rhs using the substitution in state1

 

#                         #            But don't stop here (this is exhaustive):

#                         #            return  mr_helper applied to the rest of the queue, appending

#                         #            whatever new WM assertions "execute" returned.

 

#                         #      Else if state1 has antecedents, apply "match_antecedent" to them

#                         #      along with wm and the substitutions in state1.

       

#                         #            If "match_antecedent" returns no new states, return mr_helper on rest of

#                         #            the queue without changing states.

 

#                         #            Else return mr_helper on the updated queue,

#                         #            i.e., the old one with the new states found

#                         #            by "match_antecedent" replacing state1

#     return mr_helper (match_antecedent (lhs, wm ,[]), [])



if __name__ == "__main__":
    subs = []
    wm = ["has-spine dog True"]

    anteceds = RULES[0][1]
    print("anteceds = ", anteceds)
    matched = match_antecedent(anteceds, wm, subs)
    print("matched = ", matched)
    print("subs = ", subs)

    # pattern1 = "has-spine ?animal True"
    # pattern2 = "has-spine dog True"

    # subs = unify(pattern1,pattern2,subs)
    # print("subs = ", subs)

    # updates = execute(subs,RULES[2][2], wm)
    # wm = update_wm(wm, updates)
    # print("wm = ",wm)

    # updates = execute(subs,RULES[2][2], wm)
    # print("updates = ", updates)
    # wm = update_wm(wm, updates)
    # print("wm = ",wm)
