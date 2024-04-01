class Room:
    def __init__(self, roomName):
        self.roomName = roomName
        self.members = []
        self.count = 0
    
    def joinMember(self, member):
        self.count += 1
        member.setID(self.count)
        self.members.append(member)
    
    def leaveMember(self, member):
        member.setID(None)
        self.members.remove(member)