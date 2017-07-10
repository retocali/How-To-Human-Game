from random import randint

dateStuff = ["run","cry","fight"]
sleepStuff = ["sleep","dream"]

persons = ["significant other", "boss", "coworker"]
places  = ["your home", "your workplace", "the streets", "a restaurant"]

personCount = 0
placeCount = 0

def gerundOfword(x):
    # Gives the -ing for of a word
    return x[:-1]+(x[-1] if x[-1] != 'e' else '') +"ing"


def parse(words):
    
    first_part = set()
    for i in range(len(words)):
        # Update persons and places
        placeCount  += singles.get(words[i])[1][0]
        personCount += singles.get(words[i])[1][1]
        singles, combos, non_adjacent_combos = setup();

        # Single Inputs
        print(singles.get(words[i], "")[0])

        # Check for non-adjacent combos
        if words[i] in non_adjacent_combos:
            first_part.add(words[i])
        for word in first_part:
            if non_adjacent_combos[word][0] == words[i]:
                print(non_adjacent_combos[word][1])

        # Check for two inputs
        if (i == len(words)-1):
            continue # To avoid an index out of range error
        print(combos.get((words[i], words[i+1]), ""))

        # Check for three inputs
        if (i == len(words)-2):
            continue # To avoid an index out of range error
        print(combos.get((words[i], words[i+1], words[i+2]), ""))
        



words = set([
    "flirt",      "eat", 
    "smile",     "talk", 
    "fight",      "cry", 
     "wake",      "run", 
     "work",    "sleep",
    "dream",   "browse",
])

def setup():
    # Single Inputs
    singles = {
    #   word    : standard output                         change in places/persons
        "flirt" : ("You flirt with your " + persons[personCount], (0,0)),
        "smile" : ("You smile with your " + persons[personCount], (0,1)),
        "fight" : ("You fight with your " + persons[personCount], (0,1)),
        "wake"  : ("You wake up",                                 (0,0)),
        "work"  : ("You work with your " + persons[personCount],  (1,1)),
        "dream" : ("You dream about random things for a while",   (0,0)),
        "eat"   : ("You are eating at " + places[placeCount],     (0,0)),
        "talk"  : ("You talk with your " + persons[personCount],  (0,0)),
        "cry"   : ("You are crying",                              (0,0)),
        "run"   : ("You run to " + places[placeCount],            (1,0)),
        "sleep" : ("You sleep at " + places[placeCount],          (0,0)),
        "browse": ("You go on the internet",                      (0,0))
    }
    
    # Variable Inputs
    combos = {}
    combos.update({ (x, "cry")     : ("You %s, resulting in you crying")  % x for x in words})
    combos.update({ (x, "smile")   : ("You %s, resulting in you smiling") % x for x in words})

    combos.update({ ("dream", x)   : ("You dream about " + gerundOfword(x)) for x in words})
    combos.update({ ("smile", x)   : ("You smile because you are " + gerundOfword(x)) for x in words})

    combos.update({("sleep" , x, "wake") : "You dream about " + gerundOfword(x)  for x in words})

    combos.update({ ("flirt", "eat", x)   : ("Your date got ruined") for x in dateStuff})
    combos.update({ (x, "run")   : ("You sleepwalk") for x in sleepStuff})

    combos.update({ ("sleep", "talk", x)   : ("You sleeptalk about " + gerundOfword(x)) for x in sleepStuff})
    combos.update({ ("dream", "talk", x)   : ("You sleeptalk about " + gerundOfword(x)) for x in sleepStuff})

    static_combos = {
        # Two Input
        ("run", "work")    : "You go to work",
        ("work", "run")    : "You quit your job",
        ("eat", "fight")   : "You start a food fight",
        ("work", "browse")  : "You go on reddit and pretend to do work",
        ("browse", "smile"): "You find some dank memes",
        ("fight", "run")   : "You run away from a fight with your "+persons[personCount] + " to " + places[placeCount],
        ("cry", "talk")    : "You cry but decide to talk it out with your "+persons[personCount],
        ("fight", "talk")  : "You fight but decide to talk it out with your "+persons[personCount],
        ("browse", "fights") : "You get into a heated argument through Facebook with your "+persons[personCount],
        ("sleep", "wake")  : "You take a nap at " + places[placeCount],
        ("dream", "wake")  : "You wake up from a nightmare",
        ("work", "eats")  : "You eat at your desk",
        ("cry", "work")    : "You get frustrated during work and start crying.",
        ("run", "smile")   : "You feel good because you're exercising",
        ("sleep", "dream") : "You fell asleep and are beginning to dream",
        ("browse", "eat")  : "You order interesting food online from Grubhub"
        

        #Adjacent but no order ones
        ("eat", "wake")    : "You wake up, trying to eat your pillow",
        ("wake", "eat")    : "You wake up, trying to eat your pillow",
        ("browse", "flirt"): "You decide to go on Tinder",
        ("flirt", "browse"): "You decide to go on Tinder",
        ("browse", "talk") : "You go on social media",
        ("talk", "browse") : "You go on social media",
        ("flirt", "eat")   : "You go on a date with your "+persons[personCount],
        ("eat", "flirt")   : "You go on a date with your "+persons[personCount],
        ("sleep", "cry")   : "You cry yourself to sleep",
        ("cry", "sleep")   : "You cry yourself to sleep",
        ("cry", "smile")   : "You cry tears of joy",
        ("smile", "cry")   : "You cry tears of joy",
    
        
        # Three Input
        ("sleep" , "wake", "work") : "You're late for work",
        ("work" , "fight", "run")  : "You're fired from work",
        ("work" , "sleep", "wake") : "You pull an all-nighter",

        
    }

    non_adjacent_combos = {
    # First  >  Second = Result
        "sleep" : ("wake", "You wake up and realize, it was all a dream")

    }
    combos.update(static_combos)
    return singles, combos, non_adjacent_combos


response = []
count = 1
print("\n Welcome to How to Human\n"+"-"*25,"\n\n - Please Select 10 words\n   to see how well you can\n   make your day.\n")

print("Words Left:",words)

while True:
    # Take in user input
    user = input(str(count)+":");
    if user in words:
        if user == "end":
            parse(response)
            break
        words.remove(user)
        print("Words Left:",words)
        response.append(user)
        count+=1;

    else:
        print("Not in list\n")
    # End and show players their story
    if len(response) == 10:
        print("\n Story \n-------")
        parse(response)
        break;
