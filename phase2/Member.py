class Member:
    def __init__(self, name):
        self.id = None
        self.name = name
    
    def setID(self, id):
        self.id = id
    
    def getID(self):
        return self.id

    def getName(self):
        return self.name

memberList = [] 
for i in range(0,10):
    member = Member('User ' + str(i))
    member.setID(str(i))
    memberList.append(member)