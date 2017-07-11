from random import randint


dateStuff = ["run","cry","fight"]
sleepStuff = ["sleep","dream"]

persons = ["significant other", "boss", "coworker"]
places  = ["your home", "your workplace", "the streets", "a restaurant"]


def gerundOfword(x):
    # Gives the -ing for of a word
    return x[:-1]+(x[-1] if x[-1] != 'e' else '') +"ing"


def parse(words):
    personCount = 0
    placeCount = 0

    time = 6
    singles, combos, non_adjacent_combos = setup(personCount, placeCount);
    first_part = set()
    phrases = []
    for i in range(len(words)):
        # Calculate Time
        current_time = ""
        if (time % 12 == 0):
            current_time += "12:00"
        else:
            current_time += str(time % 12)+":00"
        if (time//12):
            current_time += "PM: "
        else:
            current_time += "AM: "
        time += 2
        

        # Update persons and places
        placeCount, personCount = singles.get(words[i])[1]
        singles, combos, non_adjacent_combos = setup(personCount, placeCount);

        # Single Inputs
        phrases.append(current_time+singles.get(words[i], "")[0])

        # Check for non-adjacent combos
        if words[i] in non_adjacent_combos:
            first_part.add(words[i])
        for word in first_part:
            if non_adjacent_combos[word][0] == words[i]:
                phrases.append(non_adjacent_combos[word][1])

        # Check for two inputs
        if (i == len(words)-1):
            continue # To avoid an index out of range error
        phrases.append(combos.get((words[i], words[i+1]), ""))

        # Check for three inputs
        if (i == len(words)-2):
            continue # To avoid an index out of range error
        phrases.append(combos.get((words[i], words[i+1], words[i+2]), ""))
    return phrases



def setup(personCount, placeCount):
    # Single Inputs
    p = personCount
    a = placeCount
    singles = {
    #   word    : standard output                         change in places/persons
        "flirt" : ("You flirt with your " + persons[personCount],  ( a , p )),
        "smile" : ("You smile with your " + persons[personCount],  ( a , p )),
        "fight" : ("You get mad at your " + persons[personCount],  ( a ,p+1)),
        "wake"  : ("Your eyes start to open",                      ( a , p )),
        "work"  : ("You work with your " + persons[personCount],   ( 2 , p )),
        "dream" : ("You dream about random things for a while",    ( a , p )),
        "eat"   : ("You are eating at " + places[placeCount],      ( a , p )),
        "talk"  : ("You talk with your " + persons[personCount],   ( a , p )),
        "cry"   : ("Tears start to fall down your face",           ( a , p )),
        "run"   : ("You run to " + places[placeCount],             (a+1,p+1)),
        "sleep" : ("You sleep at " + places[placeCount],           ( a , p )),
        "browse": ("You go on the internet",                       ( a , p ))
    }
    
    # Variable Inputs
    combos = {}
    combos.update({ (x, "cry")     : ("You %s, resulting in you crying")  % x for x in words})
    combos.update({ (x, "smile")   : ("You %s, resulting in you smiling") % x for x in words})
    combos.update({ (x, "run")   : ("You sleepwalk") for x in sleepStuff})

    combos.update({ ("dream", x)   : ("You dream about " + gerundOfword(x)) for x in words})
    combos.update({ ("smile", x)   : ("You smile because you are " + gerundOfword(x)) for x in words})

    combos.update({("sleep" , x, "wake") : "You dream about " + gerundOfword(x)  for x in words})

    combos.update({ ("flirt", "eat" , x)   : ("Your date got ruined") for x in dateStuff})
    combos.update({ ("sleep", "talk", x)   : ("You sleeptalk about " + gerundOfword(x)) for x in sleepStuff})
    combos.update({ ("dream", "talk", x)   : ("You sleeptalk about " + gerundOfword(x)) for x in sleepStuff})

    static_combos = {
        # Two Input
        ("run", "work")    : "You go to work",
        ("work", "run")    : "You quit your job",
        ("eat", "fight")   : "You start a food fight",
        ("work", "browse") : "You go on reddit and pretend to do work",
        ("browse", "smile"): "You find some dank memes",
        ("fight", "run")   : "You run away from a fight with your " + persons[personCount] + " to " + places[placeCount],
        ("cry", "talk")    : "You cry but decide to talk it out with your " + persons[personCount],
        ("fight", "talk")  : "You fight but decide to talk it out with your " + persons[personCount],
        ("browse", "fights"):"You get into a heated argument through Facebook with your " + persons[personCount],
        ("sleep", "wake")  : "You take a nap at " + places[placeCount],
        ("dream", "wake")  : "You wake up from a nightmare",
        ("work", "eats")   : "You eat at your desk",
        ("cry", "work")    : "You get frustrated during work and start crying.",
        ("run", "smile")   : "You feel good because you're exercising",
        ("sleep", "dream") : "You fall asleep and are beginning to dream",
        ("browse", "eat")  : "You order interesting food online from Grubhub",
        ("dream", "cry")   : "You have a nightmare and feel scared",


        # Adjacent but no order ones
        ("eat", "wake")    : "You are trying to eat your pillow in your sleep",
        ("wake", "eat")    : "You are trying to eat your pillow in your sleep",
        ("browse", "flirt"): "You decide to go on Tinder",
        ("flirt", "browse"): "You decide to go on Tinder",
        ("browse", "talk") : "You go on social media",
        ("talk", "browse") : "You go on social media",
        ("flirt", "eat")   : "You go on a date with your " + persons[personCount],
        ("eat", "flirt")   : "You go on a date with your " + persons[personCount],
        ("sleep", "cry")   : "You cry yourself to sleep",
        ("cry", "sleep")   : "You cry yourself to sleep",
        ("cry", "smile")   : "You cry tears of joy",
        ("smile", "cry")   : "You cry tears of joy",
        ("smile", "fight") : "You playfight with " + persons[personCount],
        ("fight", "smile") : "You playfight with " + persons[personCount],
        
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

def reset():
    response = []
    count = 6
    words = set([
        "flirt",      "eat", 
        "smile",     "talk", 
        "fight",      "cry", 
        "wake",      "run", 
        "work",    "sleep",
        "dream",   "browse",
    ])
    print("\n Welcome to How to Human\n"+"-"*25,"\n\n - Please type in 10 words\n Press enter after typing each word.\n   to see if you can\n   get the following line:\n")
    print("Line: ",random_line, "\n")
    print("Words Left:",words)
    return response, count, words



random_line = "You're fired from work"
done = False
response, count, words = reset()

while not done:
    current_time = ""
    if (count % 12 == 0):
        current_time += "12:00"
    else:
        current_time += str(count % 12)+":00"
    if (count//12):
        current_time += "PM: "
    else:
        current_time += "AM: "
    # Take in user input
    user = input(current_time);
    if user in words:
        if user == "end":
            parse(response)
            break
        words.remove(user)
        print("Words Left:",words)
        response.append(user)
        count += 2;

    else:
        print("Not in list\n")
    # End and show players their story
    if len(response) == 10:
        print("\n Story \n-------")
        phrases = parse(response)
        for line in phrases:
            print(line)
            if random_line == line:
                done = True
        print("-"*10)
        if not done:
            print("\nThe line was not found\nTry again")
            response, count, words = reset()
        else:
            print("-"*12,"\n- You win! -\n"+("-"*12))
        
