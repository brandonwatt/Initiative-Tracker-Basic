'''
Created on Jan 22, 2020

@author: Brandon
'''

from Back_End.TemporaryModifier import ModDict

class InitTracker(object):
    
    def __init__(self):
        self.charaList = []
        self.turn = 0
        self.round = 1
        
        
    def initCmp(self, first, second):
        if first.initiative > second.initiative:
            return True
        else:
            return False
        
    def addChara(self, chara):
        
        added = False
        for pos in range(0, len(self.charaList)):
            if self.charaList[pos].initiative < chara.initiative:
                self.charaList.insert(pos, chara)
                added = True
                
                '''
                Advance the turn position if a character has been added ahead of the current
                players turn. This keeps the turn order advancing properly.
                This prevents the GUI from actively updating the current turn character to
                the character with the highest initiative when the list of characters is 
                initially being built. This may be changed in a later version.
                '''
                if pos <= self.turn:
                    self.turn += 1
                
                break
        if not added:
            self.charaList.append(chara)
    
    def removeChara(self, chara):
        
        if self.charaList[self.turn].initiative < chara.initiative:
            '''
            Decrease the turn position if a character before the current players turn
            has been removed. This keeps the turn order advancing properly.
            '''    
            if self.turn > 0:
                self.turn -= 1  
          
        self.charaList.remove(chara)
        
        if self.turn >= len(self.charaList):
            self.turn = 0            
    
    def adjustInit(self, chara, newInit):
        '''
        Removes the given character form the initiative list, changes their initiative, and then
        places them back into the list at their new initiative position.
        '''
        self.removeChara(chara)
        chara.initiative = newInit
        self.addChara(chara)
        
    def nextTurn(self):
        
        # Check that the character list is not empty.
        if len(self.charaList) > 0 and self.turn < len(self.charaList):
            self.charaList[self.turn].mods.endOfRound()
            
            '''
            Currently removed in favor of users removing characters themselves,
            since there is not enough information (Con score) to determine when exactly 
            a character would die.
            # Automatically removes characters below 0 health from the initiative
            # list.
            if self.charaList[self.turn].health < 0:
                self.charaList.remove(self.charaList[self.turn])
                if self.turn >= len(self.charaList):
                    self.turn = 0
            '''
            if self.turn + 1 >= len(self.charaList):
                self.turn = 0
                self.round += 1
            else:
                self.turn += 1

        elif self.turn >= len(self.charaList):
            self.turn = 0
            self.round += 1
            

    def __str__(self):
        
        tempStr = ""
        for chara in self.charaList:
            tempStr += chara.listDisplay()
            tempStr += " "
            
        return tempStr
        

class CharaBasic(object):
    '''
    A basic representation of a character made in the Pathfinder system. Primarily created to 
    track character status during combat.
    '''


    def __init__(self, theName = "", theInit = 0, theHealth = 0, theMods= None):
        '''
        theName: The name the character will be assigned. Expecting a String value.
        theInit: The initiative value the character will be assigned. Expecting an Integer value.
        theHealth: The health value assigned to the character. Expecting an Integer value.
        theMods: The modifier dictionary holding a character's current modifiers. Expects an
                 object of the ModDict class, will accept a None value.
        
        '''
        # The characters name.
        self.charaName = theName
        # The character's initiative, determining when they're turn is in a round.
        self.initiative = theInit
        # The health value of the character. 
        self.health = theHealth
        # A modifier dictionary holding all the temporary modifiers currently affecting the 
        # character. 
        self.mods = ModDict(theMods)
        
    def damage(self, dmg):
        '''
        Decriments the characters health value by the passed value dmg.
        '''
        self.health -= dmg
        
    
    def listDisplay(self):
        '''
        Returns a simple string representation of a character and their initiative.
        The string has the format of: character name - initiative
        '''
        return self.charaName + " - " + str(self.initiative)
     
      
        
        
        
        