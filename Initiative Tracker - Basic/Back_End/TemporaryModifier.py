'''
Created on Jan 29, 2018

@author: brandon
'''

class ModDict(object):
    '''
    Holds and manages all the modifiers a character is currently affected by.
    '''
    
    def __init__(self, theOrigDict = None):
        '''
        Creates a new ModDict object that starts with an empty dictionary or deep copies a passed
        dictionary/ModDict object.
        theOrigDict: Either a ModDict object or a dictionary holding TempModifiers that the
                     constructor will deep copy.
        '''
        # Create an empy dictionary to hold and organize the mods.
        self.myDict = {}
        if theOrigDict != None:
            try:
                # Assumes the object passed is a ModDict, and performs a deep copy.    
                for mod in list(theOrigDict.myDict):
                    temp = TempModifier(theOrigMod = theOrigDict.myDict[mod])
                    self.addMod(temp)
            
            except AttributeError:
                # If the object is not a ModDict, assume it's a dictionary and deep copies it.
                for mod in list(theOrigDict):
                    temp = TempModifier(theOrigMod= theOrigDict[mod])
                    self.addMod(temp)
                
    
    def addMod(self, mod):
        '''
        Takes the passed modifier and then adds it to the dictionary if a modifier with the same 
        name isn't already in the dictionary. If there is a modifier of the same name already in 
        the dictionary increase it's duration by the added modifier.
        mod: A passed TempModifier object who is to be added to the dictionary.
        '''
        if mod.title not in self.myDict:
            self.myDict[mod.title] = mod
        else:
            self.myDict[mod.title].changeDuration(mod.duration)
    
    def removeMod(self, theMod):
        '''
        '''
        if theMod in self.myDict.keys():
            del self.myDict[theMod]
    
    def removeAllMods(self, modList):
        '''
        '''
        for mod in modList:
            del self.myDict[mod]
    
    def endOfRound(self):
        '''
        '''
        toBeRemovedList = []
        
        for mod in self.myDict.keys():
            temp = self.myDict[mod]
            temp.duration -= 1
        
            if temp.duration <= 0:
                toBeRemovedList.append(temp.title)
        
        self.removeAllMods(toBeRemovedList)
    
    def __str__(self):
        '''
        '''
        tempStr = ''
        
        for mod in self.myDict.keys():
            tempStr += str(self.myDict[mod])
            
        return tempStr
    
class TempModifier(object):
    '''
    A basic representation of a temporary modifier in the Pathfinder system. 
    '''

    def __init__(self, theDuration = 1, theTitle = '', theDesc = '', theOrigMod=None):
        '''
        duration: The passed value of how many turns the modifier lasts. Expects an Integer 
        value.
        title: The passed value of what the modifier is called. Expects a String value.
        theDesc: The passed description of what the modifier does. Expects a String value.
        theOrigMod: A TempModifier that will be deep copied by the constructor. This will override
        the other assignments. Expects an object of the TempModifier type.
        '''
        
        # If a mod is passed perform a deep copy of it. 
        if theOrigMod == None:
            self.duration = theDuration
            self.title = theTitle
            self.desc = theDesc
        # If there is no modifier to copy, instantiate the mod with the passed/default values.
        else:
            self.duration = theOrigMod.duration
            self.title = theOrigMod.title
            self.desc = theOrigMod.desc
    
    def changeDuration(self, theChange):
        '''
        Changes the duration of the modifier for a number of rounds given.
        The duration will increase if the value is positive and decrease if it is negative.
        '''
        self.duration += theChange
    
    def __str__(self):
        '''
        Returns a string version of the modifier.
        The string will have the following format:
        Title: Description
        Duration: X
        '''
        tempString = self.title + ': ' + self.desc + '\nDuration: ' + str(self.duration) + '\n'
        return tempString

    
        
if __name__ == '__main__':
    sickened = TempModifier(1, 'sickened','-2 to attack and ability mods')
    fatigued = TempModifier(2, 'fatigued','-2 to attack and ability mods')
    haste = TempModifier(2, 'haste','double move speed and one additional attack')
    
    adict = {sickened.title:sickened, fatigued.title:fatigued, 
             haste.title:haste}
    
    emptyDict = ModDict()
    testDict = ModDict(adict)
    copyDict = ModDict(testDict)
    
    print("The original")
    print(str(testDict))
    print("\nThe Copy")
    print(str(copyDict))
    
    testDict.endOfRound()
    testDict.endOfRound()
    testDict.endOfRound()
    
    print(str(testDict))
    print("\nThe Copy")
    print(str(copyDict))
    
    copyDict.addMod(haste)
    print("\nThe Copy")
    print(str(copyDict))
    
    print(sickened.__dict__)
    print(copyDict.__dict__)
    
    testStat = TempModifier(**sickened.__dict__)
    
    print(str(testStat))
    
    