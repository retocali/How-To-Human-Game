from random import randint
dateStuff = ["run","cry","fight"]
sleepStuff = ["sleep","dream"]

def gerundOfword(x):
    # Gives the -ing for of a word
    return x[:-1]+(x[-1] if x[-1] != 'e' else '') +"ing"


def parse(words):
    first_part = set()
    for i in range(len(words)):
        # Check for non-adjacent combos
        if words[i] in non_adjacent_combos:
            first_part.add(words[i])
        for word in first_part:
            if non_adjacent_combos[word][0] == words[i]:
                print(non_adjacent_combos[word][1])
        # Check for two inputs
        if (i == len(words)-1):
            continue # To avoid an index out of range error
        if (words[i], words[i+1]) in combos:
            print(combos[(words[i], words[i+1])])
        # Check for three inputs
        elif (i == len(words)-2):
            continue # To avoid an index out of range error
        elif (words[i], words[i+1], words[i+2]) in combos:
            print(combos[(words[i], words[i+1], words[i+2])])



words = set([
    "flirt",      "eat", 
    "smile",     "talk", 
    "fight",      "cry", 
     "wake",      "run", 
     "work",    "sleep",
    "dream",   "browse",
])
combos = {}

# Variable Inputs
combos.update({ (x, "cry")     : ("You %s, resulting in crying")  % x for x in words})
combos.update({ (x, "smile")   : ("You %s, resulting in smiling") % x for x in words})

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
    ("fight", "run")   : "You run away from a fight",
    ("cry", "talk")    : "You cry but decide to talk it out",
    ("fight", "talk")  : "You fight but decide to talk it out",
    ("browse", "fights") : "You get into a heated argument through Facebook",
    ("sleep", "wake")  : "You take a nap",

    #Adjacent but no order ones
    ("eat", "wake")    : "You wake up, trying to eat your pillow",
    ("wake", "eat")    : "You wake up, trying to eat your pillow",
    ("browse", "flirt"): "You decide to go on Tinder",
    ("flirt", "browse"): "You decide to go on Tinder",
    ("browse", "talk") : "You go on social media",
    ("talk", "browse") : "You go on social media",
    ("flirt", "eat")   : "You go on a date",
    ("eat", "flirt")   : "You go on a date",
    ("sleep", "cry")   : "You cry yourself to sleep",
    ("cry", "sleep")   : "You cry yourself to sleep",
    
    # Three Input
    ("sleep" , "wake", "work") : "You're late for work",
    ("work" , "fight", "run")  : "You're fired from work",
    ("work" , "sleep", "wake") : "You pull all-nighter",

    # Random Ones
    ("work", "flirt") : "You flirt with your " + "coworker" if randint(0,5) > 2 else "boss"
    
}

non_adjacent_combos = {
   # First  >  Second = Result
    "sleep" : ("wake", "You wake up and realize, it was all a dream")

}
combos.update(static_combos)


response = []
count = 1
print("\n Welcome to How to Human\n"+"-"*25,"\n\n - Please Select 10 words\n   to see how well you can\n   make your day\n")

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
