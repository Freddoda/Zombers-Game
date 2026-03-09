import pygame
import numpy as np
import random
import Zombers_sound as audio


def edit_display(boss_info,centrex,centrey,screen,screen_w,screen_h):
    pygame.draw.rect(screen,(255,255,255),pygame.Rect((boss_info[1]-screen_w/2)/5+centrex,(boss_info[2]-screen_h/2)/5+centrey,screen_w/5,70/5))
    pygame.draw.rect(screen,(255,255,255),pygame.Rect(((boss_info[1])-screen_w/2)/5+centrex,((boss_info[2]+screen_h-70)-screen_h/2)/5+centrey,screen_w/5,70/5))
    pygame.draw.rect(screen,(255,255,255),pygame.Rect((boss_info[1]-screen_w/2)/5+centrex,(boss_info[2]-screen_h/2)/5+centrey,70/5,(screen_h/2-150)/5))
    pygame.draw.rect(screen,(255,255,255),pygame.Rect((boss_info[1]-screen_w/2)/5+centrex,((boss_info[2]+screen_h/2+150)-screen_h/2)/5+centrey,70/5,(screen_h/2-150)/5))
    pygame.draw.rect(screen,(255,255,255),pygame.Rect(((boss_info[1]+screen_w-70)-screen_w/2)/5+centrex,(boss_info[2]-screen_h/2)/5+centrey,70/5,(screen_h/2-150)/5))
    pygame.draw.rect(screen,(255,255,255),pygame.Rect(((boss_info[1]+screen_w-70)-screen_w/2)/5+centrex,((boss_info[2]+screen_h/2+150)-screen_h/2)/5+centrey,70/5,(screen_h/2-150)/5))
    nofbossfrfr = (pygame.font.SysFont('consolas', 40)).render(str(boss_info[0]),True,(255,255,255))
    screen.blit(nofbossfrfr,((boss_info[1])/5+centrex-nofbossfrfr.get_width()/2,(boss_info[2])/5+centrey-nofbossfrfr.get_height()/2))

def setup(bosses,blocks,screen_w,screen_h,screen):
    for n in range(len(bosses)):
        bossnum,arenax,arenay=bosses[n]
        blocks.append((arenax,arenay,screen_w,70,0))
        blocks.append((arenax,arenay+screen_h-70,screen_w,70,0))
        blocks.append((arenax,arenay,70,screen_h/2-150,0))
        blocks.append((arenax,arenay+screen_h/2+150,70,screen_h/2-150,0))
        blocks.append((arenax+screen_w-70,arenay,70,screen_h/2-150,0))
        blocks.append((arenax+screen_w-70,arenay+screen_h/2+150,70,screen_h/2-150,0))
        blocks.append((arenax+screen_w-70,arenay+screen_h/2-150,70,300,0))
        if bossnum==0:
            boss_health=1500
            bossX=random.randint(arenax+70+160,arenax+screen_w-70-160)
            bossY=random.randint(arenay+70+160,arenay+screen_h-70-160)
            state=0
            misc_val=[]
        elif bossnum==1:
            boss_health=2000
            bossX=arenax+screen_w-70-396
            bossY=arenay+70
            state=0
            misc_val=[]
        elif bossnum==2:
            boss_health=5000
            bossX=arenax+screen_w+1500 #radius is 2000 let's say
            bossY=arenay+screen_h/2
            state=0
            misc_val=[1400] #why don't we use this as radius? misc_val[0]
        bosses[n]=bossnum,arenax,arenay,boss_health,bossX,bossY,state,misc_val
    

def fight(bosses,blocks,bullets,zombers,playerX,playerY,centrex,centrey,screen_w,screen_h,bossmode,playerHP,screen,sound):
    for n in range(len(bosses)):
        bossnum,arenax,arenay,boss_health,bossX,bossY,state,misc_val=bosses[n]
        
        if bossnum==0:
            if state==0 and boss_health>0:
                if playerX>arenax+120 and playerX<arenax+screen_w-120 and playerY>arenay+120 and playerY<arenay+screen_h-120:
                    state=1
                    bossmode=True
                    centrex=screen_w/2-arenax
                    centrey=screen_h/2-arenay
                    blocks.append((arenax,arenay+screen_h/2-150,70,300,0))
                    misc_val.append(0)
                    misc_val.append(0)
                    misc_val.append(0)
            if state>0:
                if boss_health<=0:
                    if sound:
                        audio.b1death1.play()
                        audio.b1death2.play()
                    state=0
                    bossmode=False
                    centrex=screen_w-playerX
                    centrey=screen_h-playerY
                    blocks.pop(blocks.index((arenax+screen_w-70,arenay+screen_h/2-150,70,300,0)))
                if boss_health>0:
                    bossmode=True
                    centrex=screen_w/2-arenax
                    centrey=screen_h/2-arenay
                    
                    if state==1:
                        misc_val[0]=np.arcsin((playerX-bossX)/((np.sqrt((playerX-bossX)**2+(playerY-bossY)**2))))
                        misc_val[1]=np.arcsin((playerY-bossY)/((np.sqrt((playerX-bossX)**2+(playerY-bossY)**2))))
                        misc_val[2]+=1
                        if misc_val[2]==200:
                            state=2
                            misc_val[2]=1
                            misc_val.append(0)
                            misc_val.append(0)
                        elif misc_val[2]==700:
                            state=3
                            misc_val[2]=0
                            
                    elif state==2:
                        if misc_val[3]==0:
                            bossX+=misc_val[2]*np.sin(misc_val[0])
                        elif misc_val[3]==1:
                            bossX-=misc_val[2]*np.sin(misc_val[0])
                        if misc_val[4]==0:
                            bossY+=misc_val[2]*np.sin(misc_val[1])
                        elif misc_val[4]==1:
                            bossY-=misc_val[2]*np.sin(misc_val[1])
                        if misc_val[3]==0 and misc_val[4]==0:
                            misc_val[2]+=0.3
                            if sound:
                                audio.charging.play()
                        else:
                            misc_val[2]-=1.2
                        if bossX<70+160+arenax or bossX>screen_w-70-160+arenax:
                            if sound:
                                audio.crash1.play()
                                audio.crash2.play()
                            misc_val[3]=1
                        if bossY<70+160+arenay or bossY>screen_h-70-160+arenay:
                            if sound:
                                audio.crash1.play()
                                audio.crash2.play()
                            misc_val[4]=1
                        if misc_val[2]<=0:
                            state=1
                            misc_val[2]=random.randint(450,550)
                            misc_val.pop(4)
                            misc_val.pop(3)

                    elif state==3:
                        misc_val[2]+=1
                        if misc_val[2]==30:
                            misc_val[2]=0
                            misc_val[0]=np.arcsin((playerX-bossX)/((np.sqrt((playerX-bossX)**2+(playerY-bossY)**2))))
                            misc_val[1]=np.arcsin((playerY-bossY)/((np.sqrt((playerX-bossX)**2+(playerY-bossY)**2))))
                            misc_val.append((bossX,bossY,misc_val[0],misc_val[1]))
                            if sound:
                                audio.spit.play()
                        n2=3
                        while n2<len(misc_val):
                            (px,py,pxa,pya)=misc_val[n2]
                            px+=30*np.sin(pxa)
                            py+=30*np.sin(pya)
                            pygame.draw.circle(screen,(106,13,173),(px-screen_w/2+centrex,py-screen_h/2+centrey),12)
                            if np.sqrt((playerX-px)**2+(playerY-py)**2) <= 45+12:
                                py+=1000000
                                playerHP-=10
                                if sound:
                                    audio.bite.play()
                            elif np.sqrt((playerX-px-30*np.sin(pxa))**2+(bossY-py-30*np.sin(pya))**2) <= 45+12:
                                px+=1000000
                                playerHP-=10
                                if sound:
                                    audio.bite.play()
                            misc_val[n2]=px,py,pxa,pya
                            n2+=1
                        if len(misc_val)>=10:
                            state=1
                            misc_val[2]=random.randint(-50,50)
                            while len(misc_val)>3:
                                misc_val.pop(3)
                    n2=0
                    while n2<len(bullets):
                        (x2,y2,angle2,dmg2,size2,speed2) = bullets[n2]
                        if np.sqrt((bossX-x2)**2+(bossY-y2)**2) <= 160+size2:
                            bullets.pop(n2)
                            boss_health-=dmg2
                            if sound:
                                audio.zomhit2.play()
                        elif np.sqrt((bossX-x2-(speed2/2)*np.sin(np.deg2rad(angle2)))**2+(bossY-y2-(speed2/2)*np.cos(np.deg2rad(angle2)))**2) <= 160+size2:
                            bullets.pop(n2)
                            boss_health-=dmg2
                            if sound:
                                audio.zomhit2.play()
                        else:
                            n2+=1
                        
                    if np.sqrt((playerX-bossX)**2+(playerY-bossY)**2)<160+45:
                        playerHP-=1
                        if sound:
                            audio.bite.play()
                    pygame.draw.circle(screen, (108,19,20),(bossX-screen_w/2+centrex,bossY-screen_h/2+centrey),160)
                    pygame.draw.circle(screen, (255,255,255),((bossX-screen_w/2+centrex)+110*np.sin(misc_val[0]),(bossY-screen_h/2+centrey)+110*np.sin(misc_val[1])),38)
                    otherboss=False
                    for n2 in range(n):
                        if bosses[n2][6]>0:
                            otherboss=True
                    if otherboss==False:
                        pygame.draw.rect(screen,(255,0,0),pygame.Rect(arenax+centrex-400,arenay+centrey+10-screen_h/2,800,50))
                        pygame.draw.rect(screen,(0,255,0),pygame.Rect(arenax+centrex-400,arenay+centrey+10-screen_h/2,800*(boss_health/1500),50))
                    elif otherboss==True:
                        pygame.draw.rect(screen,(255,0,0),pygame.Rect(arenax+centrex-400,arenay+centrey+65-screen_h/2,800,50))
                        pygame.draw.rect(screen,(0,255,0),pygame.Rect(arenax+centrex-400,arenay+centrey+65-screen_h/2,800*(boss_health/1500),50))
            else:
                pygame.draw.circle(screen, (108,19,20),(bossX-screen_w/2+centrex,bossY-screen_h/2+centrey),160)
                if boss_health<=0:
                    pygame.draw.circle(screen, (0,0,0),((bossX-screen_w/2+centrex)+110*np.sin(misc_val[0]),(bossY-screen_h/2+centrey)+110*np.sin(misc_val[1])),38)



        elif bossnum==1:
            Bwidth=396
            if state==0 and boss_health>0:
                if playerX>arenax+120 and playerX<arenax+screen_w-120 and playerY>arenay+120 and playerY<arenay+screen_h-120:
                    state=1
                    bossmode=True
                    centrex=screen_w/2-arenax
                    centrey=screen_h/2-arenay
                    blocks.append((arenax,arenay+screen_h/2-150,70,300,0))
                    misc_val.append(0) #counter until state changes
                    misc_val.append(0) #direction
                pygame.draw.rect(screen,(0,255,0),pygame.Rect(arenax+centrex+screen_w/2-70-396,arenay+centrey-screen_h/2+70,Bwidth,Bwidth))
            if state>0:
                if boss_health<=0:
                    if sound:
                        audio.b2death.play()
                    state=0
                    bossmode=False
                    centrex=screen_w-playerX
                    centrey=screen_h-playerY
                    blocks.pop(blocks.index((arenax+screen_w-70,arenay+screen_h/2-150,70,300,0)))
                elif boss_health>0:
                    bossmode=True
                    centrex=screen_w/2-arenax
                    centrey=screen_h/2-arenay

                    if state==1:
                        misc_val[0]+=1
                        if misc_val[0]==100:
                            misc_val[0]=0
                            misc_val.append(0) #speed
                            misc_val.append(0) #recharge timer
                            state=2
                        if misc_val[0]==300: #this starts at 200
                            misc_val[0]=1 #cooldown timer which will be functioning as length
                            misc_val.append(0) #speed
                            misc_val.append(0) #finish attack check
                            misc_val.append(random.randint(1,2)) #vertical or horizontal
                            state=3

                    elif state==2:
                        if misc_val[2]==0:
                            if misc_val[3]==30:
                                misc_val[2]+=0.6
                                misc_val[0]+=1
                                misc_val[3]=0
                                if misc_val[0]<6:
                                    if bossX==arenax+screen_w-70-Bwidth:
                                        if bossY==arenay+70:
                                            misc_val[1]=random.choice((2,3))
                                        elif bossY==arenay+screen_h-70-Bwidth:
                                            misc_val[1]=random.choice((0,3))
                                    elif bossX==arenax+70:
                                        if bossY==arenay+70:
                                            misc_val[1]=random.choice((2,1))
                                        elif bossY==arenay+screen_h-70-Bwidth:
                                            misc_val[1]=random.choice((0,1))
                            else:
                                misc_val[3]+=1
                        elif misc_val[0]==6:
                            state=1
                            misc_val.pop(3)
                            misc_val.pop(2)
                            misc_val[0]=200
                        else:
                            if sound:
                                audio.charging.play()
                            misc_val[2]+=0.6
                            if misc_val[1]==0:
                                bossY-=misc_val[2]
                                if bossY<=arenay+70:
                                    misc_val[2]=0
                                    bossY=arenay+70
                                    if sound:
                                        audio.crash3.play()
                            elif misc_val[1]==2:
                                bossY+=misc_val[2]
                                if bossY>=arenay+screen_h-70-Bwidth:
                                    misc_val[2]=0
                                    bossY=arenay+screen_h-70-Bwidth
                                    if sound:
                                        audio.crash3.play()
                            if misc_val[1]==3:
                                bossX-=misc_val[2]
                                if bossX<=arenax+70:
                                    misc_val[2]=0
                                    bossX=arenax+70
                                    if sound:
                                        audio.crash3.play()
                            elif misc_val[1]==1:
                                bossX+=misc_val[2]
                                if bossX>=arenax+screen_w-70-Bwidth:
                                    misc_val[2]=0
                                    bossX=arenax+screen_w-70-Bwidth
                                    if sound:
                                        audio.crash3.play()

                    elif state==3:
                        if misc_val[0]<=0:
                            misc_val[0]=0
                            state=1
                            misc_val.pop(4)
                            misc_val.pop(3)
                            misc_val.pop(2)
                        else:
                            if misc_val[4]==1:
                                if bossY==arenay+70:
                                    pygame.draw.rect(screen,(0,180,0),pygame.Rect(arenax+70-screen_w/2+centrex,arenay+screen_h/2+centrey-70-434,misc_val[0],434))
                                    pygame.draw.rect(screen,(0,180,0),pygame.Rect(arenax-70+screen_w/2+centrex-misc_val[0],arenay+screen_h/2+centrey-70-434,misc_val[0],434))
                                    if playerY+20>arenay+screen_h-70-434:
                                        if playerX-45<arenax+70+misc_val[0]:
                                            playerX=arenax+70+45+misc_val[0]
                                            if playerX+45>arenax+screen_w-70-misc_val[0]:
                                                playerHP-=100
                                        elif playerX+45>arenax+screen_w-70-misc_val[0]:
                                            playerX=arenax+screen_w-70-misc_val[0]-45
                                    elif playerY+45>arenay+screen_h-70-434 and (playerX<arenax+70+misc_val[0] or playerX>arenax+screen_w-70-misc_val[0]):
                                        playerY=arenay+screen_h-70-434-45
                                elif bossY==arenay+screen_h-70-Bwidth:
                                    pygame.draw.rect(screen,(0,180,0),pygame.Rect(arenax+70-screen_w/2+centrex,arenay-screen_h/2+centrey+70,misc_val[0],434))
                                    pygame.draw.rect(screen,(0,180,0),pygame.Rect(arenax-70+screen_w/2+centrex-misc_val[0],arenay-screen_h/2+centrey+70,misc_val[0],434))
                                    if playerY-20>arenay+70+434:
                                        if playerX-45<arenax+70+misc_val[0]:
                                            playerX=arenax+70+45+misc_val[0]
                                            if playerX+45>arenax+screen_w-70-misc_val[0]:
                                                playerHP-=100
                                        elif playerX+45>arenax+screen_w-70-misc_val[0]:
                                            playerX=arenax+screen_w-70-misc_val[0]-45
                                    elif playerY-45<arenay+70+434 and (playerX<arenax+70+misc_val[0] or playerX>arenax+screen_w-70-misc_val[0]):
                                        playerY=arenay+70+434+45
                                if misc_val[0]>=690:
                                    if sound:
                                        audio.crash1.play()
                                        audio.crash2.play()
                                    misc_val[3]=1
                            elif misc_val[4]==2:
                                if bossX==arenax+70:
                                    pygame.draw.rect(screen,(0,180,0),pygame.Rect(arenax-70+screen_w/2+centrex-700,arenay-screen_h/2+centrey+70,700,misc_val[0]))
                                    pygame.draw.rect(screen,(0,180,0),pygame.Rect(arenax-70+screen_w/2+centrex-700,arenay+screen_h/2+centrey-70-misc_val[0],700,misc_val[0]))
                                    if playerX+20>arenax+screen_w-70-700:
                                        if playerY-45<arenay+70+misc_val[0]:
                                            playerY=arenay+70+45+misc_val[0]
                                            if playerY+45>arenay+screen_h-70-misc_val[0]:
                                                playerHP-=100
                                        elif playerY+45>arenay+screen_h-70-misc_val[0]:
                                            playerY=arenay+screen_h-70-misc_val[0]-45
                                    elif playerX+45>arenax+screen_w-70-700 and (playerY<arenay+70+misc_val[0] or playerY>arenay+screen_w-70-misc_val[0]):
                                        playerX=arenax+screen_w-70-700-45
                                elif bossX==arenax+screen_w-70-Bwidth:
                                    pygame.draw.rect(screen,(0,180,0),pygame.Rect(arenax+70-screen_w/2+centrex,arenay-screen_h/2+centrey+70,700,misc_val[0]))
                                    pygame.draw.rect(screen,(0,180,0),pygame.Rect(arenax+70-screen_w/2+centrex,arenay+screen_h/2+centrey-70-misc_val[0],700,misc_val[0]))
                                    if playerX-20<arenax+70+700:
                                        if playerY-45<arenay+70+misc_val[0]:
                                            playerY=arenay+70+45+misc_val[0]
                                            if playerY+45>arenay+screen_h-70-misc_val[0]:
                                                playerHP-=100
                                        elif playerY+45>arenay+screen_h-70-misc_val[0]:
                                            playerY=arenay+screen_h-70-misc_val[0]-45
                                    elif playerX-45<arenax+70+700 and (playerY<arenay+70+misc_val[0] or playerY>arenay+screen_w-70-misc_val[0]):
                                        playerX=arenax+70+700+45
                                if misc_val[0]>=440:
                                    if sound:
                                        audio.crash1.play()
                                        audio.crash2.play()
                                    misc_val[3]=1

                            if misc_val[3]==0:
                                misc_val[2]+=0.65
                                misc_val[0]+=misc_val[2]
                                if sound:
                                    audio.crushing.play()
                            elif misc_val[3]==1:
                                misc_val[0]-=5

                        
                    #collision between player and boss
                    if playerX>bossX-45 and playerX<bossX+Bwidth/2 and playerY>bossY and playerY<bossY+Bwidth:
                        playerX-=playerX-bossX+45
                        if playerX<arenax+70+45:
                            playerHP-=100
                    elif playerX>bossX and playerX<bossX+Bwidth and playerY>bossY-45 and playerY<bossY+Bwidth/2:
                        playerY-=playerY-bossY+45
                        if playerY<arenay+70+45:
                            playerHP-=100
                    elif playerX>bossX+Bwidth/2 and playerX<bossX+Bwidth+45 and playerY>bossY and playerY<bossY+Bwidth:
                        playerX+=45-playerX+bossX+Bwidth
                        if playerX>arenax+screen_w-70-45:
                            playerHP-=100
                    elif playerX>bossX and playerX<bossX+Bwidth and playerY>bossY+Bwidth/2 and playerY<bossY+Bwidth+45:
                        playerY+=45-playerY+bossY+Bwidth
                        if playerY>arenay+screen_h-70-45:
                            playerHP-=100
                    elif np.sqrt((playerX-bossX)**2+(playerY-bossY)**2)<=45:
                        playerX2=playerX
                        playerX2-=(45-np.sqrt((playerX-bossX)**2+(playerY-bossY)**2))/np.sqrt((playerX-bossX)**2+(playerY-bossY)**2)*(bossX-playerX)
                        playerY-=(45-np.sqrt((playerX-bossX)**2+(playerY-bossY)**2))/np.sqrt((playerX-bossX)**2+(playerY-bossY)**2)*(bossY-playerY)
                        playerX=playerX2
                        if playerX<arenax+70+45 or playerY<arenay+70+45:
                            playerHP-=20
                            if sound:
                                audio.bite.play()
                    elif np.sqrt((playerX-(bossX+Bwidth))**2+(playerY-bossY)**2)<=45:
                        playerX2=playerX
                        playerX2-=(45-np.sqrt((playerX-(bossX+Bwidth))**2+(playerY-bossY)**2))/np.sqrt((playerX-(bossX+Bwidth))**2+(playerY-bossY)**2)*((bossX+Bwidth)-playerX)
                        playerY-=(45-np.sqrt((playerX-(bossX+Bwidth))**2+(playerY-bossY)**2))/np.sqrt((playerX-(bossX+Bwidth))**2+(playerY-bossY)**2)*(bossY-playerY)
                        playerX=playerX2
                        if playerX>arenax+screen_w-70-45 or playerY<arenay+70+45:
                            playerHP-=20
                            if sound:
                                audio.bite.play()
                    elif np.sqrt((playerX-bossX-Bwidth)**2+(playerY-(bossY+Bwidth))**2)<=45:
                        playerX2=playerX
                        playerX2-=(45-np.sqrt((playerX-(bossX+Bwidth))**2+(playerY-bossY-Bwidth)**2))/np.sqrt((playerX-(bossX+Bwidth))**2+(playerY-bossY-Bwidth)**2)*((bossX+Bwidth)-playerX)
                        playerY-=(45-np.sqrt((playerX-(bossX+Bwidth))**2+(playerY-bossY-Bwidth)**2))/np.sqrt((playerX-(bossX+Bwidth))**2+(playerY-bossY-Bwidth)**2)*(bossY+Bwidth-playerY)
                        playerX=playerX2
                        if playerX>arenax+screen_w-70-45 or playerY>arenay+screen_h-70-45:
                            playerHP-=20
                            if sound:
                                audio.bite.play()
                    elif np.sqrt((playerX-(bossX))**2+(playerY-(bossY+Bwidth))**2)<=45:
                        playerX2=playerX
                        playerX2-=(45-np.sqrt((playerX-bossX)**2+(playerY-bossY-Bwidth)**2))/np.sqrt((playerX-(bossX))**2+(playerY-bossY-Bwidth)**2)*(bossX-playerX)
                        playerY-=(45-np.sqrt((playerX-bossX)**2+(playerY-bossY-Bwidth)**2))/np.sqrt((playerX-(bossX))**2+(playerY-bossY-Bwidth)**2)*(bossY+Bwidth-playerY)
                        playerX=playerX2
                        if playerX<arenax+70+45 or playerY>arenay+screen_h-70-45:
                            playerHP-=20
                            if sound:
                                audio.bite.play()
                    #bullets
                    n2=0
                    while n2<len(bullets):
                        (x2,y2,angle2,dmg2,size2,speed2) = bullets[n2]
                        if x2+size2>bossX and x2-size2<bossX+Bwidth and y2+size2>bossY and y2-size2<bossY+Bwidth:
                            bullets.pop(n2)
                            boss_health-=dmg2
                            if sound:
                                audio.zomhit2.play()
                        else:
                            n2+=1

                #boss drawing
                pygame.draw.rect(screen,(0,255,0),pygame.Rect(bossX-screen_w/2+centrex,bossY-screen_h/2+centrey,Bwidth,Bwidth))
                if misc_val[1]==0:
                    pygame.draw.rect(screen,(155,0,0),pygame.Rect(bossX-screen_w/2+centrex+Bwidth/2-50-20,bossY-screen_h/2+centrey+30,20,20))
                    pygame.draw.rect(screen,(155,0,0),pygame.Rect(bossX-screen_w/2+centrex+Bwidth/2+50,bossY-screen_h/2+centrey+30,20,20))
                if misc_val[1]==2:
                    pygame.draw.rect(screen,(155,0,0),pygame.Rect(bossX-screen_w/2+centrex+Bwidth/2-50-20,bossY-screen_h/2+centrey+Bwidth-30,20,20))
                    pygame.draw.rect(screen,(155,0,0),pygame.Rect(bossX-screen_w/2+centrex+Bwidth/2+50,bossY-screen_h/2+centrey+Bwidth-30,20,20))
                if misc_val[1]==1:
                    pygame.draw.rect(screen,(155,0,0),pygame.Rect(bossX-screen_w/2+centrex+Bwidth-30,bossY-screen_h/2+centrey+Bwidth/2-50-20,20,20))
                    pygame.draw.rect(screen,(155,0,0),pygame.Rect(bossX-screen_w/2+centrex+Bwidth-30,bossY-screen_h/2+centrey+Bwidth/2+50,20,20))
                if misc_val[1]==3:
                    pygame.draw.rect(screen,(155,0,0),pygame.Rect(bossX-screen_w/2+centrex+30,bossY-screen_h/2+centrey+Bwidth/2-50-20,20,20))
                    pygame.draw.rect(screen,(155,0,0),pygame.Rect(bossX-screen_w/2+centrex+30,bossY-screen_h/2+centrey+Bwidth/2+50,20,20))
                #healthbar
                pygame.draw.rect(screen,(255,0,0),pygame.Rect(arenax+centrex-400,arenay+centrey+10-screen_h/2,800,50))
                pygame.draw.rect(screen,(0,255,0),pygame.Rect(arenax+centrex-400,arenay+centrey+10-screen_h/2,800*(boss_health/2000),50))
            

        elif bossnum==2:
            if state==0 and boss_health>0:
                if playerX>arenax+120 and playerX<arenax+screen_w-120 and playerY>arenay+120 and playerY<arenay+screen_h-120:
                    state=1
                    bossmode=True
                    centrex=screen_w/2-arenax
                    centrey=screen_h/2-arenay
                    blocks.append((arenax,arenay+screen_h/2-150,70,300,0))
                    misc_val.append(0) #state timer

            elif state>=1:
                if boss_health<=0:
                    if misc_val[0]==1400:
                        while len(misc_val)>1:
                            misc_val.pop(1)
                        misc_val.append(0)
                    pygame.draw.circle(screen,(220,220,0),(bossX-screen_w/2+centrex,bossY-screen_h/2+centrey),misc_val[0])
                    misc_val[1]+=4
                    misc_val[0]+=misc_val[1]
                    if sound:
                        audio.b3death1.play()
                    if misc_val[0]>4000:
                        if sound:
                            audio.b3death2.play()
                        bossmode=False
                        centrex=screen_w-playerX
                        centrey=screen_h-playerY
                        state=0
                        while len(zombers)>0:
                            zombers.pop(0)
                        for i in range(3):
                            blocks.pop(blocks.index([(arenax+screen_w-70,arenay,70,screen_h/2-150,0),(arenax+screen_w-70,arenay+screen_h/2+150,70,screen_h/2-150,0),(arenax+screen_w-70,arenay+screen_h/2-150,70,300,0)][i])) 
                elif state==1:
                    if bossX>arenax+screen_w+1000:
                        if sound:
                            audio.crushing.play()
                        bossX-=3.5
                    else:
                        misc_val[1]+=1
                        if misc_val[1]==100:
                            state=2
                            misc_val[1]=0
                            misc_val.append(0)
                        elif misc_val[1]==700:
                            state=3
                            misc_val[1]=0
                            misc_val.append(0)
                        elif misc_val[1]==1100:
                            state=4
                            misc_val[1]=0
                            misc_val.append(0)
                        elif misc_val[1]==1800:
                            state=5
                            misc_val[1]=0
                            misc_val.append(0)
                elif state==2:
                    misc_val[2]+=1
                    if misc_val[2]==25:
                        spawn_list=[(bossX-1100, bossY, 400, 40, 160, [0, 0, 0], 1, 0, 2000),(bossX-1100, bossY, 100, 10, 100, [0, 100, 0], 2, 0, 2000),(bossX-1100, bossY, 100, 10, 100, [0, 100, 0], 2, 0, 2000)]
                        zombers.append(spawn_list[random.randint(0,2)])
                        if sound:
                            audio.spawn1.play()
                        misc_val[2]=0
                        misc_val[1]+=1
                    if misc_val[1]==4:
                        state=1
                        misc_val[1]=500
                        misc_val.pop(2)
                elif state==3:
                    misc_val[1]+=1
                    if misc_val[1]==30 and misc_val[2]<10:
                        misc_val.append((bossX+((playerX-bossX)/np.sqrt((playerX-bossX)**2+(playerY-bossY)**2))*1300,bossY+((playerY-bossY)/np.sqrt((playerX-bossX)**2+(playerY-bossY)**2))*1300,np.arcsin((playerX-bossX)/np.sqrt((playerX-bossX)**2+(playerY-bossY)**2)),30,14,22,playerY>arenay+screen_h/2))
                        #x,y,angle,dmg,speed,size,vert checker cause np trig sucks
                        misc_val[2]+=1
                        misc_val[1]=0
                        if sound:
                            audio.spit.play()
                    elif misc_val[1]==150:
                        while len(misc_val)>2:
                            misc_val.pop(2)
                        misc_val[1]=1000
                        state=1
                    n2=3
                    while n2<len(misc_val):
                        x2,y2,angle2,dmg2,speed2,size2,vertcheck=misc_val[n2]
                        if np.sqrt((playerX-x2)**2+(playerY-y2)**2)<45+size2:
                            playerHP-=dmg2
                            misc_val.pop(n2)
                            if sound:
                                audio.bite.play()
                        else:
                            x2+=(speed2/2)*np.sin(angle2)
                            if vertcheck==True:
                                y2+=(speed2/2)*np.cos(angle2)
                            else:
                                y2-=(speed2/2)*np.cos(angle2)
                            if np.sqrt((playerX-x2)**2+(playerY-y2)**2)<45+size2:
                                playerHP-=dmg2
                                misc_val.pop(n2)
                                if sound:
                                    audio.bite.play()
                            else:
                                x2+=(speed2/2)*np.sin(angle2)
                                if vertcheck==True:
                                    y2+=(speed2/2)*np.cos(angle2)
                                else:
                                    y2-=(speed2/2)*np.cos(angle2)
                                pygame.draw.circle(screen,(125,0,125),(x2-screen_w/2+centrex,y2-screen_h/2+centrey),size2)
                                misc_val[n2]=x2,y2,angle2,dmg2,speed2,size2,vertcheck
                                n2+=1
                elif state==4:
                    misc_val[1]+=1
                    spawn_list=[[(bossX-1100, bossY+3*screen_h/8, 50, 2, 45, [0, 255, 0], 3, 0, 2000),(bossX-1100, bossY-3*screen_h/8, 50, 2, 45, [0, 255, 0], 3, 0, 2000)],[(bossX-1100, bossY+3*screen_h/8, 20, 1, 30, [144, 238, 144], 5, 0, 2000),(bossX-1100, bossY-3*screen_h/8, 20, 1, 30, [144, 238, 144], 5, 0, 2000)]]
                    if misc_val[1]==30:
                        zombers.append(spawn_list[random.randint(0,1)][0])
                        if sound:
                            audio.spawn2.play()
                    elif misc_val[1]==60:
                        zombers.append(spawn_list[random.randint(0,1)][1])
                        if sound:
                            audio.spawn2.play()
                        misc_val[1]=0
                        misc_val[2]+=1
                    if misc_val[2]==4:
                        state=1
                        misc_val[1]=1500
                        misc_val.pop(2)
                elif state==5:
                    if sound:
                        if misc_val[1]==0:
                            audio.spit2.play()
                    misc_val[1]+=15
                    if misc_val[2]!=1:
                        for i in range(5):
                            projrect=pygame.Rect(arenax+screen_w-misc_val[1],arenay+screen_h/2-25-400+200*i,200,40)
                            pygame.draw.rect(screen,(125,0,125),pygame.Rect(arenax+screen_w/2+centrex-misc_val[1],arenay+centrey-25-400+200*i,200,40))
                            if projrect.colliderect(pygame.Rect(playerX-45,playerY-45,90,90)):
                                playerHP-=2
                                if sound:
                                    audio.bite.play()
                        if misc_val[1]>=screen_w+200:
                            misc_val[1]=0
                            if misc_val[2]==0:
                                misc_val[2]=1
                            else:
                                misc_val.pop(2)
                                misc_val[1]=0
                                state=1
                    elif misc_val[2]==1:
                        for i in range(4):
                            projrect=pygame.Rect(arenax+screen_w-misc_val[1],arenay+screen_h/2-25-300+200*i,200,40)
                            pygame.draw.rect(screen,(125,0,125),pygame.Rect(arenax+screen_w/2+centrex-misc_val[1],arenay+centrey-25-300+200*i,200,40))
                            if projrect.colliderect(pygame.Rect(playerX-45,playerY-45,90,90)):
                                playerHP-=2
                                if sound:
                                    audio.bite.play()
                        if misc_val[1]>=screen_w+200:
                            misc_val[2]=2
                            misc_val[1]=0

                if boss_health>0:
                    #bullet detection
                    n2=0
                    while n2<len(bullets):
                        (x2,y2,angle2,dmg2,size2,speed2) = bullets[n2]
                        if np.sqrt((x2-bossX)**2+(y2-bossY)**2)<size2+misc_val[0]:
                            boss_health-=dmg2
                            bullets.pop(n2)
                            if sound:
                                audio.zomhit2.play()
                        else:
                            n2+=1                        
                    #ts the open wall
                    pygame.draw.rect(screen,(0,0,0),pygame.Rect(arenax+screen_w/2+centrex-70,arenay+70-screen_h/2+centrey,70,screen_h-140))
                    #boss drawing
                    pygame.draw.circle(screen,(220,220,0),(bossX-screen_w/2+centrex,bossY-screen_h/2+centrey),misc_val[0])
                    pygame.draw.circle(screen,(255,0,0),((bossX-screen_w/2+centrex)-(misc_val[0]-85)*np.sin(np.arccos((bossY-playerY)/((np.sqrt((playerX-bossX)**2+(playerY-bossY)**2))))+np.deg2rad(15)),(bossY-screen_h/2+centrey)-(misc_val[0]-85)*np.cos(np.arccos((bossY-playerY)/((np.sqrt((playerX-bossX)**2+(playerY-bossY)**2))))+np.deg2rad(15))),45)
                    pygame.draw.circle(screen,(255,0,0),((bossX-screen_w/2+centrex)-(misc_val[0]-85)*np.sin(np.arccos((bossY-playerY)/((np.sqrt((playerX-bossX)**2+(playerY-bossY)**2))))-np.deg2rad(15)),(bossY-screen_h/2+centrey)-(misc_val[0]-85)*np.cos(np.arccos((bossY-playerY)/((np.sqrt((playerX-bossX)**2+(playerY-bossY)**2))))-np.deg2rad(15))),45)
                    #healthbar
                    pygame.draw.rect(screen,(255,0,0),pygame.Rect(arenax+centrex-400,arenay+centrey+10-screen_h/2,800,50))
                    pygame.draw.rect(screen,(0,255,0),pygame.Rect(arenax+centrex-400,arenay+centrey+10-screen_h/2,800*(boss_health/5000),50))
                    #collision
                    if np.sqrt((playerX-bossX)**2+(playerY-bossY)**2)<misc_val[0]+45:
                        playerX2=playerX
                        playerX2-=((misc_val[0]+45)-np.sqrt((playerX-bossX)**2+(playerY-bossY)**2))/np.sqrt((playerX-bossX)**2+(playerY-bossY)**2)*(bossX-playerX)
                        playerY-=((misc_val[0]+45)-np.sqrt((playerX-bossX)**2+(playerY-bossY)**2))/np.sqrt((playerX-bossX)**2+(playerY-bossY)**2)*(bossY-playerY)
                        playerX=playerX2
        bosses[n]=bossnum,arenax,arenay,boss_health,bossX,bossY,state,misc_val
    return centrex,centrey,bossmode,playerHP,playerX,playerY
                    

        
