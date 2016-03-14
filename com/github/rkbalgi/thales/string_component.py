

counter = 0


class StringComponent:
    
    def __init__(self):
        self.data = None
    
    @classmethod
    def withData(cls, data):
        comp = StringComponent();
        comp.data = data
        return comp    
  
    def hasData(self):
        return self.data!=None
    
    def setValue(self,data):
        self.data=data
       
    def getValue(self):
        return self.data
    
    