class EventManager:
    def __init__(self):
        self.handlers={}
    def on(self,event,func):
        if event not in self.handlers:self.handlers[event]=[]
        self.handlers[event].append(func)
    def emit(self,event,*args):
        if event in self.handlers:
            for h in self.handlers[event]:h(*args)    