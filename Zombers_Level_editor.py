import pygame
import numpy as np
import Zombers_bosses as boss_code

LEVEL='Test_level.txt'
edit=True

pygame.init()
pygame.display.set_caption('Zombers level editor')
screen_h=1003
screen_w=1504
screen = pygame.display.set_mode((screen_w,screen_h),pygame.SCALED|pygame.RESIZABLE)
clock = pygame.time.Clock()
centrex=screen_w//2
centrey=screen_h//2
quit_release=0
switch_timer=0
block=0
zomber=0
boss=0
factor='block'
blocks=[]
zombers=[]
bosses=[]
with open(LEVEL) as file:
    L='blocks'
    for line in file:
        RGB=[]
        if line[:-1]=='change':
            L='zombers'
        elif line[:-1]=='boss':
            L='boss'
        else:
            line=(line[:-1])
            line=line.split(',')
            newline=[]
            colour=False
            for item in line:
                try:
                    item=eval(item)
                    if colour==True:
                        RGB.append(int(item))
                except:
                    if colour==False:
                        colour=True
                        try:
                            RGB.append(int(item[2:]))
                        except:
                            RGB.append(int(item[1:]))
                    else:
                        colour=False
                        RGB.append(int(item[:-1]))
                        item=RGB
                        RGB=[]
                if colour==False:
                    newline.append(item)
            if L=='blocks':
                blocks.append((newline))
            elif L=='zombers':
                zombers.append((newline))
            elif L=='boss':
                bosses.append((newline))
running = True
while running:
    screen.fill((0,0,0))
    keys = pygame.key.get_pressed()
    mpos = pygame.mouse.get_pos()
    mclick = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if ( keys[pygame.K_q] ):
        quit_release=1
    else:
        if quit_release==1:
            running = False

    pygame.draw.circle(screen,(255,255,255),(centrex,centrey),9)
    
    for i in blocks:
        (x,y,w,h,mode) = i
        if mode==1:
            pygame.draw.rect(screen,(255,255,0),pygame.Rect((x-screen_w//2)/5+centrex,(y-screen_h//2)/5+centrey,w//5,h//5),mode)
        else:
            pygame.draw.rect(screen,(255,255,255),pygame.Rect((x-screen_w//2)/5+centrex,(y-screen_h//2)/5+centrey,w//5,h//5),mode)
    for i in zombers:
        (x,y,hp,dmg,size,colour,speed,dmg_timer,eyerange) = i
        if colour==[0,0,0]:
            pygame.draw.circle(screen,(255,255,255),((x-screen_w//2)//5+centrex,(y-screen_h//2)//5+centrey),size//5)
            pygame.draw.circle(screen,(255,255,255),((x-screen_w//2)//5+centrex,(y-screen_h//2)//5+centrey),eyerange//5,1)
        else:
            pygame.draw.circle(screen,colour,((x-screen_w//2)//5+centrex,(y-screen_h//2)//5+centrey),size//5)
            pygame.draw.circle(screen,colour,((x-screen_w//2)//5+centrex,(y-screen_h//2)//5+centrey),eyerange//5,1)
    for i in bosses:
        boss_code.edit_display(i,centrex,centrey,screen,screen_w,screen_h)
        
        
    if keys[pygame.K_UP]:
        centrey+=2
    if keys[pygame.K_DOWN]:
        centrey-=2
    if keys[pygame.K_LEFT]:
        centrex+=2
    if keys[pygame.K_RIGHT]:
        centrex-=2

    if switch_timer<30:
        switch_timer+=1
    if switch_timer==30 and keys[pygame.K_r]:
        blocks=[]
        zombers=[]
        with open(LEVEL) as file:
            L='blocks'
            for line in file:
                RGB=[]
                if line[:-1]=='change':
                    L='zombers'
                elif line[:-1]=='boss':
                    L='boss'
                else:
                    line=(line[:-1])
                    line=line.split(',')
                    newline=[]
                    colour=False
                    for item in line:
                        try:
                            item=eval(item)
                            if colour==True:
                                RGB.append(int(item))
                        except:
                            if colour==False:
                                colour=True
                                try:
                                    RGB.append(int(item[2:]))
                                except:
                                    RGB.append(int(item[1:]))
                            else:
                                colour=False
                                RGB.append(int(item[:-1]))
                                item=RGB
                                RGB=[]
                        if colour==False:
                            newline.append(item)
                    if L=='blocks':
                        blocks.append((newline))
                    elif L=='zombers':
                        zombers.append((newline))
                    elif L=='boss':
                        bosses.append((newline))

    #editing blocks
    if edit==True and factor=='block':
        if switch_timer==30:
            if keys[pygame.K_p]:
                block+=1
                switch_timer=0
                if block==len(blocks):
                    block=0
            if keys[pygame.K_o]:
                block-=1
                switch_timer=0
                if block==-1:
                    block=len(blocks)-1
        if block<len(blocks):
            (x,y,w,h,mode) = blocks[block]
            pygame.draw.rect(screen,(255,0,255),pygame.Rect((x-screen_w//2)/5+centrex,(y-screen_h//2)/5+centrey,w//5,h//5),1)
            if keys[pygame.K_LSHIFT]:
                if keys[pygame.K_w]:
                    h-=5
                if keys[pygame.K_s]:
                    h+=5
                if keys[pygame.K_a]:
                    w-=5
                if keys[pygame.K_d]:
                    w+=5
            else:
                if keys[pygame.K_w]:
                    y-=5
                if keys[pygame.K_s]:
                    y+=5
                if keys[pygame.K_a]:
                    x-=5
                if keys[pygame.K_d]:
                    x+=5
            if switch_timer==30 and keys[pygame.K_l]:
                switch_timer=0
                if mode==1:
                    mode=0
                else:
                    mode=1
            if switch_timer==30 and keys[pygame.K_n]:
                switch_timer=0
                blocks.append((x,y,50,50,0))
                block=len(blocks)-1
                w=50
                h=50
            if switch_timer==30 and keys[pygame.K_m]:
                switch_timer=0
                blocks.pop(block)
                if block>=len(blocks):
                    block=len(blocks)-1

            else:
                blocks[block]=(x,y,w,h,mode)
        if switch_timer==30:
            if keys[pygame.K_n] and len(blocks)==0:
                switch_timer=0
                blocks.append((screen_w//2,screen_h//2,50,50,0))
            if keys[pygame.K_BACKSLASH]:
                switch_timer=0
                factor='zomber'

    #editing zombers                
    if edit==True and factor=='zomber':
        if switch_timer==30:
            if keys[pygame.K_p]:
                zomber+=1
                switch_timer=0
                if zomber==len(zombers):
                    zomber=0
            if keys[pygame.K_o]:
                zomber-=1
                switch_timer=0
                if zomber==-1:
                    zomber=len(zombers)-1
        if switch_timer==30:
            if keys[pygame.K_n] and len(zombers)==0:
                switch_timer=0
                zombers.append((screen_w//2,screen_h//2,50,2,45,[0,255,0],3,0,1000))
            if keys[pygame.K_BACKSLASH]:
                switch_timer=0
                factor='boss'
                boss=0
        if zomber<len(zombers):
            (x,y,hp,dmg,size,colour,speed,dmg_timer,eyerange) = zombers[zomber]
            pygame.draw.circle(screen,(255,0,255),((x-screen_w//2)//5+centrex,(y-screen_h//2)//5+centrey),size//5,1)
            if switch_timer==30:
                if keys[pygame.K_1]:
                    switch_timer=0
                    (hp,dmg,size,colour,speed)=(50,2,45,[0,255,0],3)
                if keys[pygame.K_2]:
                    switch_timer=0
                    (hp,dmg,size,colour,speed)=(100,10,100,[0,100,0],2)
                if keys[pygame.K_3]:
                    switch_timer=0
                    (hp,dmg,size,colour,speed)=(400,40,160,[0,0,0],1)
                if keys[pygame.K_4]:
                    switch_timer=0
                    (hp,dmg,size,colour,speed)=(20,1,30,[144, 238, 144],5)
            if keys[pygame.K_LSHIFT]:
                if keys[pygame.K_w]:
                    eyerange+=5
                if keys[pygame.K_s]:
                    eyerange-=5
            else:
                if keys[pygame.K_w]:
                    y-=5
                if keys[pygame.K_s]:
                    y+=5
                if keys[pygame.K_a]:
                    x-=5
                if keys[pygame.K_d]:
                    x+=5
            if switch_timer==30 and keys[pygame.K_n]:
                switch_timer=0
                zombers.append((x,y,50,2,45,(0,255,0),3,0,1000))
                zomber=len(zombers)-1
                
            if switch_timer==30 and keys[pygame.K_m]:
                switch_timer=0
                zombers.pop(zomber)
                if zomber>=len(zombers):
                    zomber=len(zombers)-1
            else:
                zombers[zomber]=(x,y,hp,dmg,size,colour,speed,dmg_timer,eyerange)

    if edit==True and factor=='boss':
        if switch_timer==30:
            if keys[pygame.K_BACKSLASH]:
                switch_timer=0
                factor='block'
                block=0
            elif keys[pygame.K_p]:
                boss+=1
                switch_timer=0
                if boss==len(bosses):
                    boss=0
            elif keys[pygame.K_o]:
                boss-=1
                switch_timer=0
                if boss==-1:
                    boss=len(bosses)-1
            elif keys[pygame.K_n]:
                switch_timer=0
                bosses.append((0,screen_w//2,screen_h//2))
                boss=len(bosses)-1
        if boss<len(bosses):
            num,x,y=bosses[boss]
            pygame.draw.rect(screen,(255,0,255),pygame.Rect((x-screen_w//2)/5+centrex,(y-screen_h//2)/5+centrey,screen_w//5,screen_h//5),1)
            if keys[pygame.K_LSHIFT]:
                if switch_timer==30:
                    if keys[pygame.K_w]:
                        num+=1
                        switch_timer=0
                    if keys[pygame.K_s]:
                        num-=1
                        switch_timer=0
            else:
                if keys[pygame.K_w]:
                    y-=5
                if keys[pygame.K_s]:
                    y+=5
                if keys[pygame.K_a]:
                    x-=5
                if keys[pygame.K_d]:
                    x+=5
            if keys[pygame.K_m] and switch_timer==30:
                switch_timer=0
                bosses.pop(boss)
            else:
                bosses[boss]=num,x,y

            
    if edit==True:
        if mclick[0]:
            for i in range(len(blocks)):
                (x,y,w,h,mode) = blocks[i]
                if mpos[0]>(x-screen_w//2)/5+centrex and mpos[0]<(x-screen_w//2)/5+centrex+w/5 and mpos[1]>(y-screen_h//2)/5+centrey and mpos[1]<(y-screen_h//2)/5+centrey+h/5:
                    factor='block'
                    block=i
            for i in range(len(zombers)):
                (x,y,hp,dmg,size,colour,speed,dmg_timer,eyerange) = zombers[i]
                if np.sqrt((mpos[0]-((x-screen_w//2)//5+centrex))**2+(mpos[1]-((y-screen_h//2)//5+centrey))**2)<size/5:
                    factor='zomber'
                    zomber=i
                
            
        if switch_timer==30:
            if keys[pygame.K_6]:
                switch_timer=0
                with open(LEVEL, 'w') as file:
                    for i in blocks:
                        file.write(str(i)[1:-1]+'\n')
                    file.write('change\n')
                    for i in zombers:
                        file.write(str(i)[1:-1]+'\n')
                    file.write('boss\n')
                    for i in bosses:
                        file.write(str(i)[1:-1]+'\n')
                    file.write('changey')
                
        
        
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
