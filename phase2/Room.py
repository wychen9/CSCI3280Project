class Room:
    def __init__(self, roomName):
        self.roomName = roomName
        self.members = []
        self.count = 0
    
    def joinMember(self, member):
        self.count += 1
        self.members.append(member)
    
    def leaveMember(self, member):
        self.count += 1
        self.members.remove(member)
        
    def isEmpty(self):
        return len(self.members) == 0
    
    def current_cnt(self):
        return len(self.members)