# -*- coding: utf-8 -*-
from PIL import Image
from .field import createfield,Field
import numpy as np
import math
import sys
def get_line(x1, y1, x2, y2):
    points = []
    issteep = abs(y2-y1) > abs(x2-x1)
    if issteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    rev = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        rev = True
    deltax = x2 - x1
    deltay = abs(y2-y1)
    error = int(deltax / 2)
    y = y1
    ystep = None
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    for x in range(x1, x2 + 1):
        if issteep:
            points.append((y, x))
        else:
            points.append((x, y))
        error -= deltay
        if error < 0:
            y += ystep
            error += deltax
    if rev:
        points.reverse()
    return points
class Canvas:
    def __init__(self,w,h,bg=(255,255,255)):
        self.width=w
        self.height=h
        self.bg=bg
        self.image=Image.new('RGB',(w,h))
        self.colormap=createfield(w+1,h+1,bg)
        self.imagemap=self.image.load()
        self.colormap.copy(self.imagemap)
    def _update(self):
        self.colormap.copy(self.imagemap)
    def _draw_field(self,x,y,f):
        for a in range(y,y+len(f)):
            for b in range(x,x+len(f[0])):
                try:
                    self.colormap[a][b]=tuple(f[a-y][b-x])
                except IndexError:
                    self._update()
                    return
        self._update()
    def slice(self,x,y,w,h):
        sl=[]
        for a in range(h+1):
            inner=[]
            for b in range(w+1):
                inner.append(self.colormap[y+a][x+b])
            sl.append(inner)
        return sl
    def draw_rectangle(self,x,y,w,h,color=(0,0,0),fill=True,border=1,border_color=None):
        if border_color is None:
            border_color=color
        if fill:
            rect=createfield(w,h,color)
            self._draw_field(x,y,rect)
        
        for j in range(w+border-1):
            for pn in range(border):
                self.colormap[y+pn][x+j]=border_color
                self.colormap[y+h+pn][x+j]=border_color

        for i in range(h+border-1):
            for pn in range(border):
                try:
                    self.colormap[y+i][x+pn]=border_color
                    self.colormap[y+i][x+w+pn]=border_color
                except IndexError:pass
        self._update()
    def draw_image(self,x,y,image):
        if isinstance(image,str):
            image=Image.open(image)
        arr=np.asarray(image)
        self._draw_field(x,y,arr)
    def draw_arc(self,posx,posy,radius,color=(0,0,0),angle=math.pi*2,anglestart=0,border=1,border_color=None,fill=False,update=True):
        rang=np.arange(anglestart,angle+anglestart,0.001)
        rng=[[round(math.sin(θ)*radius)+posy,round(math.cos(θ)*radius)+posx] for θ in rang]
        if border_color is None:
            border_color=color

        for y,x in rng:
            try:
                self.colormap[y][x]=border_color
            except IndexError:
                pass
        rad=radius
        if fill:
            while rad>=0:
                rng=[[round(math.sin(θ)*rad)+posy,round(math.cos(θ)*rad)+posx] for θ in rang]
                for y,x in rng:
                    try:
                        self.colormap[y][x]=color
                    except IndexError:
                        pass
                rad-=1


        rad=radius
        if border>1:
            for a in range(border-1):
                if rad<0:
                    break
                self.draw_arc(posx,posy,rad,color,angle,anglestart,1,border_color,False,False)

                rad-=1
        if update:
            self._update()
    def draw_line(self,start,end,color=(0,0,0),width=1,update=True):
        xs,ys=start
        xe,ye=end
        line=get_line(xs,ys,xe,ye)
        distance=[xe-xs,ye-ys]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        direction= [round(distance[0] / norm), round(distance[1] / norm)]
        xch=direction[0]>=direction[1]
        ych=direction[1]>=direction[0]
        if direction[0]==0:
            xch=True
            ych=False
        if direction[1]==0:
            ych=True
            xch=False

        for x,y in line:
            for a in range(width):
                try:
                    self.colormap[y+a*direction[0]*ych][x+a*direction[1]*xch]=color
                except IndexError:
                    pass
        if update:
            self._update()
    def draw_polygon(self,*points,border=1,color=(0,0,0),fill=False):
        index=0
        f=len(points)-1
        for p in points:
            if index==f:
                nextpoint=points[0]
            else:
                nextpoint=points[index+1]
            self.draw_line(p,nextpoint,color=color,width=border,update=False)
            index+=1
        self._update()
    def show(self):
        self.image.show()
    def clear(self):
        self.colormap=createfield(self.width+1,self.height+1,self.bg)
        self._update()
    def save(self,*args,**kwargs):
        self.image.save(*args,**kwargs)
        
