'''def f(x) -> myclass:
    return myclass()'''

class myclass():
    def __init__(self):
        self.me = 1
        return 5
    
print(myclass())