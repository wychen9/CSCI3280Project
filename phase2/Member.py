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
    