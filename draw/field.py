class Field:
    def __init__(self,arr,w=None,h=None):
        if h is None:
            h=len(arr)-1
        if w is None:
            w=len(arr[0])-1
        self.w=w
        self.h=h
        self.arr=arr
    def __getitem__(self,item):
        return self.arr[item]

    def __setitem__(self,item,v):
        self.arr[item]=v
    def copy(self,where):
        for y in range(self.h):
            for x in range(self.w):
                where[x,y]=self.arr[y][x]
    def __len__(self):
        return len(self.arr)
    def __eq__(self,i):
        return i== self.arr
def createfield(w,h,val=0):
    r=[]

    for _ in range(h):
        ri=[]
        for __ in range(w):
            ri.append(val)
        r.append(ri)
    return Field(r)
