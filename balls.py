import pygame
import numpy as np

class ball(object):
    theballs=[]
    carriedarray=[]
    selectedarray=[]
    HEIGHT=500
    WIDTH=500
    SURFACE=0
    FRICTION=0.999
    COEF=100
    MASSCOEF=10
    border="wrap"
    def __init__(self,x,y,radius,vx=0,vy=0,ax=0,ay=0):
        self.x=x
        self.y=y
        self.radius=radius
        self.vx=vx
        self.vy=vy
        self.ax=ax
        self.ay=ay
        self.mv=0
        self.uvx=0
        self.uvy=0
        self.ma=0
        self.uax=0
        self.uay=0
        self.carried=False
        self.applied=False
        self.offx=0
        self.offy=0

    def wrap(self):
        if ball.border=="wrap":
            if self.x>ball.WIDTH:
                self.x=0
            if self.y>ball.HEIGHT:
                self.y=0
            if self.x<0:
                self.x=ball.WIDTH
            if self.y<0:
                self.y=ball.HEIGHT
        elif ball.border=="wall":
            if self.x>ball.WIDTH:
                self.x=ball.WIDTH
                self.vx*=-1
            if self.x<0:
                self.x=0
                self.vx*=-1
            if self.y>ball.HEIGHT:
                self.y=ball.HEIGHT
                self.vy*=-1
            if self.y<0:
                self.y=0
                self.vy*=-1
    def draw(self,mx,my):
        self.unify()
        x=int(self.x)
        y=int(self.y)
        uvx=int(self.uvx*self.radius)
        uvy=int(self.uvy*self.radius)
        uax=int(self.uax*self.radius)
        uay=int(self.uay*self.radius)
        width=1
        if self.carried:
            width=0
        pygame.draw.circle(ball.SURFACE,(255,255,255),(x,y),self.radius,width)#draw circle
        if ((uvx!=0) or (uvy!=0)):
            pygame.draw.line(ball.SURFACE,(0,0,255),(x,y),(x+uvx,y+uvy),1)#draw speed
        if ((uax!=0) or (uay!=0)):
            pygame.draw.line(ball.SURFACE,(255,0,0),(x,y),(x+uax,y+uay),1)#draw acceleration
        if self.applied:
            pygame.draw.line(ball.SURFACE,(0,255,0),(self.x,self.y),(mx,my),3)

    def push(self):

        for i in ball.theballs:
            if i !=self:
                distance = np.sqrt((self.x-i.x)*(self.x-i.x)+(self.y-i.y)*(self.y-i.y))
                if distance<(self.radius+i.radius):
                    pygame.draw.line(ball.SURFACE,(255,0,255),(self.x,self.y),(i.x,i.y))
                    #static collision
                    overlap = 0.5*(distance-i.radius-self.radius)
                    i.x-=overlap*(i.x-self.x)/distance
                    self.x-=overlap*(self.x-i.x)/distance
                    i.y-=overlap*(i.y-self.y)/distance
                    self.y-=overlap*(self.y-i.y)/distance
                    distance = np.sqrt((self.x-i.x)*(self.x-i.x)+(self.y-i.y)*(self.y-i.y))
                    #dynamic collision
                    kx = (i.vx-self.vx)
                    ky = (i.vy-self.vy)
                    nx = (self.x-i.x)/(distance)
                    ny = (self.y-i.y)/(distance)
                    p = 2*((nx*kx+ny*ky)/(ball.MASSCOEF*(i.radius+self.radius)))
                    i.vx = i.vx-(p*self.radius*ball.MASSCOEF*nx)
                    i.vy = i.vy-(p*self.radius*ball.MASSCOEF*ny)
                    self.vx = self.vx+(p*i.radius*ball.MASSCOEF*nx)
                    self.vy = self.vy+(p*i.radius*ball.MASSCOEF*ny)

    def apply(self):
        if not self.carried:
            self.vx+=self.ax
            self.vy+=self.ay
            self.ax=0
            self.ay=0
            if self.vx>1:
                self.vx=1
            if self.vy>1:
                self.vy=1
            self.vx*=ball.FRICTION
            self.x+=self.vx
            self.vy*=ball.FRICTION
            self.y+=self.vy
            self.wrap()
    def selectforce(self,mx,my):
        distance = np.sqrt((self.x-mx)*(self.x-mx)+(self.y-my)*(self.y-my))
        if distance<self.radius:
            self.applied=True
            ball.selectedarray.append(self)
            pygame.draw.line(ball.SURFACE,(0,255,0),(self.x,self.y),(mx,my),3)
    def forceselected(self,mx,my):
        if self.applied:
            self.applied=False
            ball.selectedarray.remove(self)
            self.ax+=(mx-self.x)/ball.COEF
            self.ay+=(my-self.y)/ball.COEF

    def unify(self):
        self.mv = np.sqrt((self.vx*self.vx)+(self.vy*self.vy))
        if (self.mv!=0):
            self.uvx=self.vx/self.mv
            self.uvy=self.vy/self.mv
        else:
            self.uvx=0
            self.uvy=0
        self.ma = np.sqrt((self.ax*self.ax)+(self.ay*self.ay))
        if self.ma!=0:
            self.uax=self.ax/self.ma
            self.uay=self.ay/self.ma
        else:
            self.uax=0
            self.uay=0
    def beingcarried(self,mx,my):
        if self.carried==True:
            self.x=mx+self.offx
            self.y=my+self.offy

    def placeback(self):
        if self.carried==True:
            ball.carriedarray.remove(self)
            self.carried=False
    def pickup(self,mx,my):
        distance = np.sqrt((self.x-mx)*(self.x-mx)+(self.y-my)*(self.y-my))
        if distance<self.radius:
            ball.carriedarray.append(self)
            self.carried=True
            self.offx=self.x-mx
            self.offy=self.y-my
    @staticmethod
    def rpopulate(x):
        for i in range(x):
            ball.theballs.append(ball(np.random.randint(0,ball.WIDTH),np.random.randint(0,ball.HEIGHT),np.random.randint(10,80)))
    @staticmethod
    def drawall(mx,my):
        for i in ball.theballs:
            i.push()
            i.apply()
            i.draw(mx,my)
    @staticmethod
    def checkpickup(mx,my):
        for i in ball.theballs:
            i.pickup(mx,my)
    @staticmethod
    def checkforapplied(mx,my):
        for i in ball.theballs:
            i.selectforce(mx,my)
    @staticmethod
    def checkforletgo(mx,my):
        for i in ball.selectedarray:
            i.forceselected(mx,my)
    @staticmethod
    def putback():
        for i in ball.carriedarray:
            i.placeback()
    @staticmethod
    def checkforcarried(mx,my):
        for i in ball.carriedarray:
            i.beingcarried(mx,my)

