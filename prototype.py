
words = set([
    "flirt", 
    "eat", 
    "smile", 
    "talk", 
    "fight", 
    "cry", 
    "wake", 
    "run", 
    "work", 
    "sleep",
    "dream",
    "browse"
])
combos = {}

# Variable Inputs
combos.update({ (x, "cry")     : ("You %s, resulting in crying")  % x for x in words})
combos.update({ (x, "smile")   : ("You %s, resulting in smiling") % x for x in words})

combos.update({ ("dream", x)   : ("You dream about " + x) for x in words})
combos.update({ ("smile", x)   : ("You smile about " + x) for x in words})

combos.update({("sleep" , x, "wake") : "You dream about " + gerundOfword(x)  for x in words})



static_combos = {
    # Two Input
    ("run", "work")    : "You went to work",
    ("work", "run")    : "You quit your job",
    ("eat", "fight")   : "You have a food fight",
    ("browse", "smile"): "You find some dank memes",
    ("fight", "run")   : "You ran away from a fight",
    ("cry", "talk")    : "You cry but decide to talk it out",
    ("fight", "talk")  : "You fight but decide to talk it out",
    ("browse", "flirt"): "You decide to go on Tinder",
    ("flirt", "browse"): "You decide to go on Tinder",
    ("browse", "talk") : "You go on social media",
    ("talk", "browse") : "You go on social media",
    
    # Three Input
    ("sleep" , "wake", "work") : "You're late for work",
    ("work" , "fight", "run") : "You're fired from work",
    ("work" , "sleep", "wake") : "You pull all-nighter",
}
combos.update(static_combos)


def parse(words):
    for i in range(len(words)-1):
        # Check two 
        elif (words[i], words[i+1]) in combos:
            print(combos[(words[i], words[i+1])])
        # Check three
        elif (i == len(words)-2):
            continue # To avoid an index out of range error
        elif (words[i], words[i+1], words[i+2]) in combos:
            print(combos[(words[i], words[i+1], words[i+2])])
    
def gerundOfword(x):
    # Gives the -ing for of a word
    return x[:-1]+(x[-1] if x[-1] != 'e' else '') +"ing"


response = []
count = 1
print(words)
while True:
    # Take in user input
    user = input(str(count)+":");
    if user in words:
        words.remove(user)
        print(words)
        response.append(user)
        count+=1;
    else:
        print("Not in list")
    # End and show players their story
    if len(words) == 0:
        parse(response)
        break;
