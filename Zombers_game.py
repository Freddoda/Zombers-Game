import pygame
import numpy as np
import random as rand
import Zombers_bosses as boss_code
import Zombers_sound as audio
import time
import os

#setup
pygame.init()
pygame.display.set_caption('Zombers')
screen_h=1003
screen_w=1504
screen = pygame.display.set_mode((screen_w,screen_h),pygame.SCALED|pygame.RESIZABLE)
clock = pygame.time.Clock()

#initial variables
quit_release=0
quit_click=False
play_click=False
test_click=False
lev1_click=False
lev2_click=False
lev3_click=False
lev4_click=False
lev5_click=False
lev6_click=False
lev7_click=False
lev8_click=False
lev9_click=False
lev10_click=False
lev11_click=False
lev12_click=False

sound=True
mute_timer=60

#define functions

def lev_button(text,File,LevFile,Level_click,click_check,x,y,size,toggle=True):
    font = pygame.font.SysFont('consolas', size)
    if toggle==True:
        lev_button=font.render(text,True,(200,200,200),(160,0,0))
        if mousex >=x and mousex <= x+lev_button.get_width():
            if mousey >= y and mousey<=y+lev_button.get_height():
                lev_button=font.render(text,True,(255,255,255),(200,0,0))
                if click[0] == True:
                    lev_button=font.render(text,True,(175,175,175),(120,0,0))
                    if click_check==False and sound:
                        audio.button_press.play()
                    click_check=True
                if click[0] == False and click_check:
                    if sound:
                        audio.button_rel.play()
                    Level_click=True
                    LevFile=File
                    click_check=False
    else: lev_button=font.render(text,True,(175,175,175),(120,0,0))
    screen.blit(lev_button,(x,y))
    return Level_click,click_check,LevFile

#game
running = True
Game_state='Start'
while running:
    startTime : int = int(time.time()*1000)

    keys = pygame.key.get_pressed()
    mousex,mousey = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    screen.fill((0,0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if ( keys[pygame.K_q] ):
        quit_release=1
    else:
        if quit_release==1:
            running = False

    if keys[pygame.K_m] and mute_timer>=60:
        mute_timer=0
        if sound==True:
            sound=False
            pygame.mixer.stop()
        else:
            sound=True
    if mute_timer<60:
        mute_timer+=1
            
    if Game_state=='Start':
        font = pygame.font.SysFont('consolas', 25)
        quit_button=font.render("quit",True,(200,200,200),(160,0,0))
        if mousex >=0 and mousex <=quit_button.get_width():
            if mousey >= 0 and mousey <= quit_button.get_height():
                quit_button=font.render("quit",True,(255,255,255),(200,0,0))
                if click[0] == True:
                    quit_button=font.render("quit",True,(175,175,175),(120,0,0))
                    if quit_click==False and sound:
                        audio.button_press.play()
                    quit_click=True
                if quit_click and click[0]==False:
                    if sound:
                        pygame.mixer.stop()
                        audio.button_rel.play()
                    running=False
        screen.blit(quit_button,(0,0))

        font = pygame.font.SysFont('consolas', 340)
        title = font.render("Zombers",True,(255,255,255),(0,0,0))
        screen.blit(title,(screen_w//2-title.get_width()//2,screen_h//2.8-title.get_height()//2))

        #game start
        font = pygame.font.SysFont('consolas', 180)
        play_button=font.render("Arcade",True,(200,200,200),(160,0,0))
        if mousex >=screen_w//2-play_button.get_width()//2 and mousex <=screen_w//2+play_button.get_width()//2:
            if mousey >= screen_h//1.65-play_button.get_height()//2 and mousey <= screen_h//1.65+play_button.get_height()//2:
                play_button=font.render("Arcade",True,(255,255,255),(200,0,0))
                if click[0] == True:
                    play_button=font.render("Arcade",True,(175,175,175),(120,0,0))
                    if play_click==False and sound:
                        audio.button_press.play()
                    play_click=True
                if click[0] == False and play_click:
                    if sound:
                        pygame.mixer.stop()
                        audio.button_rel.play()
                    Game_state='Arcade'
                    #setting stuff up for the actual game
                    playerX=screen_w//2
                    playerY=screen_h//2
                    playerDeg=0
                    playerHP=100
                    zombers=[]
                    bullets=[]
                    score=0
                    gun='1'
                    b_cooldown=0
                    heal_timer=0                        
        screen.blit(play_button,(screen_w//2-play_button.get_width()//2,screen_h//1.65-play_button.get_height()//2))

        play_button=font.render("Campaign",True,(200,200,200),(160,0,0))
        if mousex >=screen_w//2-play_button.get_width()//2 and mousex <=screen_w//2+play_button.get_width()//2:
            if mousey >= screen_h//1.65+play_button.get_height()//2+15 and mousey <= screen_h//1.65+play_button.get_height()*1.5+15:
                play_button=font.render("Campaign",True,(255,255,255),(200,0,0))
                if click[0] == True:
                    play_button=font.render("Campaign",True,(175,175,175),(120,0,0))
                    if play_click==False and sound:
                        audio.button_press.play()
                    play_click=True
                if click[0] == False and play_click:
                    if sound:
                        pygame.mixer.stop()
                        audio.button_rel.play()
                    Game_state='Level_menu'
                    back_click=False
                    Level_click=False
                    LevFile="null"
        screen.blit(play_button,(screen_w//2-play_button.get_width()//2,screen_h//1.65+play_button.get_height()//2+15))

    #Arcade mode ------------------------------------------------------------------------------------------------------------------------------------------------------------
    if Game_state=='Arcade':
        pygame.draw.rect(screen,(255,255,255), pygame.Rect(70,70,screen_w-140,screen_h-140),  2)
        
        #movement
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if keys[pygame.K_LSHIFT]:
                playerDeg-=3
            else:
                playerDeg-=6
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if keys[pygame.K_LSHIFT]:
                playerDeg+=3
            else:
                playerDeg+=6
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            playerX+=4*np.sin(np.deg2rad(playerDeg))
            playerY+=4*np.cos(np.deg2rad(playerDeg))
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            playerX-=6*np.sin(np.deg2rad(playerDeg))
            playerY-=6*np.cos(np.deg2rad(playerDeg))

        #outer collision
        while playerX<120:
            playerX+=1
        while playerX>screen_w-120:
            playerX-=1
        while playerY<120:
            playerY+=1
        while playerY>screen_h-120:
            playerY-=1

        if keys[pygame.K_SPACE]:
            if sound:
                audio.bullet_charge.play()
            b_cooldown+=1
            if gun=='1':
                if b_cooldown>=60:
                    if sound:
                        audio.bullet1.play()
                    bullets.append((playerX,playerY,playerDeg,100,13,60))
                    b_cooldown=0
            elif gun=='2':
                if b_cooldown>=30:
                    if sound:
                        audio.bullet2.play()
                    bullets.append((playerX,playerY,playerDeg+8,8,7,16))
                    bullets.append((playerX,playerY,playerDeg-8,8,7,16))
                    bullets.append((playerX,playerY,playerDeg-24,8,7,16))
                    bullets.append((playerX,playerY,playerDeg+24,8,7,16))
                    bullets.append((playerX,playerY,playerDeg-40,8,7,16))
                    bullets.append((playerX,playerY,playerDeg+40,8,7,16))
                    b_cooldown=0
            elif gun=='3':
                if b_cooldown>=5:
                    if sound:
                        audio.bullet3.play()
                    bullets.append((playerX,playerY,playerDeg+rand.randint(0,32)-16,5,6,16))
                    b_cooldown=0
        else:
            b_cooldown=0


        font = pygame.font.SysFont('consolas', 35)
        if gun=='1':
            bullettext=font.render("bullet charge="+str(b_cooldown)+"/60",True,(255,255,255),(0,0,0))
        elif gun=='2':
            bullettext=font.render("bullet charge="+str(b_cooldown)+"/30",True,(255,255,255),(0,0,0))
        elif gun=='3':
            bullettext=font.render("bullet charge="+str(b_cooldown)+"/5",True,(255,255,255),(0,0,0))

        #drawing bullets
        n=0
        while n<len(bullets):
            (x,y,angle,dmg,size,speed) = bullets[n]

            x-=speed*np.sin(np.deg2rad(angle))
            y-=speed*np.cos(np.deg2rad(angle))
            pygame.draw.circle(screen,(180,180,180),(x,y),size)

            if x>-50 and x<screen_w+50 and y>-50 and y<screen_h+50:
                bullets[n] = (x,y,angle,dmg,size,speed)
                n+=1
            else:
                bullets.pop(n)

        pygame.draw.circle(screen,(255,255,255),(playerX,playerY),45)
        pygame.draw.circle(screen,(0,0,0),(playerX-30*np.sin(np.deg2rad(playerDeg-30))//1,playerY-30*np.cos(np.deg2rad(playerDeg-30))//1),10)
        pygame.draw.circle(screen,(0,0,0),(playerX-30*np.sin(np.deg2rad(playerDeg+30))//1,playerY-30*np.cos(np.deg2rad(playerDeg+30))//1),10)

        #the zombers
        n=0
        while n<len(zombers):
            (x,y,hp,dmg,size,colour,speed,dmg_timer,value) = zombers[n]

            n2=0
            while n2<len(bullets) and hp>0:
                (x2,y2,angle2,dmg2,size2,speed2) = bullets[n2]
                if np.sqrt((x-x2)**2+(y-y2)**2) <= size+size2:
                    bullets.pop(n2)
                    if sound:
                        audio.zomhit2.play()
                    hp-=dmg2
                else:
                    n2+=1

            if np.sqrt((playerX-x)**2+(playerY-y)**2) <= 45+size:
                if dmg_timer==30:
                    if sound:
                        audio.bite.play()
                    playerHP-=dmg
                    dmg_timer=0
                    heal_timer=-286
            if dmg_timer<30:
                dmg_timer+=1

            if np.sqrt((playerX-x)**2+(playerY-y)**2) >= 45+size-10:
                x+= speed/np.sqrt((playerX-x)**2+(playerY-y)**2)*(playerX-x)
                y+= speed/np.sqrt((playerX-x)**2+(playerY-y)**2)*(playerY-y)

        
            if hp<=0:
                zombers.pop(n)
                score+=value
                if sound:
                    audio.zomhit1.play()
            else:
                zombers[n] = (x,y,hp,dmg,size,colour,speed,dmg_timer,value)
                n+=1
                pygame.draw.circle(screen,colour,(x,y),size)
                if playerY<y:
                    pygame.draw.circle(screen,(255,0,0),(x-(size-15)*np.sin(np.arcsin((x-playerX)/((np.sqrt((playerX-x)**2+(playerY-y)**2))))+np.deg2rad(30)),y-(size-15)*np.cos(np.arcsin((x-playerX)/((np.sqrt((playerX-x)**2+(playerY-y)**2))))+np.deg2rad(30))),10)
                    pygame.draw.circle(screen,(255,0,0),(x-(size-15)*np.sin(np.arcsin((x-playerX)/((np.sqrt((playerX-x)**2+(playerY-y)**2))))-np.deg2rad(30)),y-(size-15)*np.cos(np.arcsin((x-playerX)/((np.sqrt((playerX-x)**2+(playerY-y)**2))))-np.deg2rad(30))),10)
                else:
                    pygame.draw.circle(screen,(255,0,0),(x-(size-15)*np.sin(np.arcsin((x-playerX)/((np.sqrt((playerX-x)**2+(playerY-y)**2))))+np.deg2rad(30)),y+(size-15)*np.cos(np.arcsin((x-playerX)/((np.sqrt((playerX-x)**2+(playerY-y)**2))))+np.deg2rad(30))),10)
                    pygame.draw.circle(screen,(255,0,0),(x-(size-15)*np.sin(np.arcsin((x-playerX)/((np.sqrt((playerX-x)**2+(playerY-y)**2))))-np.deg2rad(30)),y+(size-15)*np.cos(np.arcsin((x-playerX)/((np.sqrt((playerX-x)**2+(playerY-y)**2))))-np.deg2rad(30))),10)

        if playerHP<=0 or keys[pygame.K_k]:
            pygame.mixer.stop()
            Game_state='Death'
            return_click=False
            highscorefile=open(os.path.dirname(os.path.abspath(__file__)) +'/Zombers_highscore.txt','r')
            highscore=int(highscorefile.read())
            if score>highscore:
                if sound:
                    audio.win1.play()
                    audio.win2.play()
                    audio.win3.play()
                highscorefile=open(os.path.dirname(os.path.abspath(__file__)) +'/Zombers_highscore.txt','w')
                highscorefile.write(str(score))
            elif sound:
                audio.death1.play()
                audio.death2.play()
                audio.death3.play()
            highscorefile.close()

        if playerHP<100 and heal_timer==30:
            playerHP+=1
            heal_timer=0
        if heal_timer<30:
            heal_timer+=1

        #spawning   
        if len(zombers)<8:
            if rand.randint(1,300)==1:
                zombspawn=rand.randint(1,4)
                if zombspawn==1:
                    zombers.append((-50,rand.randint(-50,screen_h+50),50,2,45,(0,255,0),3,0,2))
                elif zombspawn==2:
                    zombers.append((screen_w+50,rand.randint(-50,screen_h+50),50,2,45,(0,255,0),3,0,2))
                elif zombspawn==3:
                    zombers.append((rand.randint(-50,screen_w+50),-50,50,2,45,(0,255,0),3,0,2))
                elif zombspawn==4:
                    zombers.append((rand.randint(-50,screen_w+50),screen_h+50,50,2,45,(0,255,0),3,0,2))
            if rand.randint(1,600)==1:
                zombspawn=rand.randint(1,4)
                if zombspawn==1:
                   zombers.append((-100,rand.randint(-100,screen_h+100),100,10,100,(0,100,0),2,0,5))
                elif zombspawn==2:
                    zombers.append((screen_w+100,rand.randint(-100,screen_h+100),100,10,100,(0,100,0),2,0,5))
                elif zombspawn==3:
                    zombers.append((rand.randint(-100,screen_w+100),-100,100,10,100,(0,100,0),2,0,5))
                elif zombspawn==4:
                    zombers.append((rand.randint(-100,screen_w+100),screen_h+100,100,10,100,(0,100,0),2,0,5))
            if score>70:
                if rand.randint(1,900)==1:
                    zombspawn=rand.randint(1,4)
                    if zombspawn==1:
                        zombers.append((-160,rand.randint(-160,screen_h+160),400,40,160,(0,1,0),1,0,10))
                    elif zombspawn==2:
                        zombers.append((screen_w+160,rand.randint(-160,screen_h+160),400,40,160,(0,1,0),1,0,10))
                    elif zombspawn==3:
                        zombers.append((rand.randint(-160,screen_w+160),-160,400,40,160,(0,1,0),1,0,10))
                    elif zombspawn==4:
                        zombers.append((rand.randint(-160,screen_w+160),screen_h+160,400,40,160,(0,1,0),1,0,10))
                if rand.randint(1,400)==1:
                    zombspawn=rand.randint(1,4)
                    if zombspawn==1:
                        zombers.append((-20,rand.randint(-20,screen_h+20),20,1,30,(144, 238, 144),5,0,1))
                    elif zombspawn==2:
                        zombers.append((screen_w+20,rand.randint(-20,screen_h+20),20,1,30,(144, 238, 144),5,0,1))
                    elif zombspawn==3:
                        zombers.append((rand.randint(-20,screen_w+20),-20,20,1,30,(144, 238, 144),5,0,1))
                    elif zombspawn==4:
                        zombers.append((rand.randint(-20,screen_w+20),screen_h+20,20,1,30,(144, 238, 144),5,0,1))

        pygame.draw.rect(screen,(180,0,0),pygame.Rect(screen_w-270,screen_h-60,200,50))
        pygame.draw.rect(screen,(0,180,0),pygame.Rect(screen_w-270,screen_h-60,2*playerHP,50))
        font = pygame.font.SysFont('consolas', 50)
        HP_text=font.render("HP:"+str(playerHP),True,(255,255,255),(0,0,0))
        screen.blit(bullettext,(screen_w//2-bullettext.get_width()//2,screen_h-bullettext.get_height()))
        screen.blit(HP_text,(screen_w-270-HP_text.get_width(),screen_h-35-HP_text.get_height()//2))
        score_text=font.render("Score:"+str(score),True,(255,255,255),(0,0,0))
        screen.blit(score_text,(70,35-score_text.get_height()//2))
        font = pygame.font.SysFont('consolas', 25)
        quit_button=font.render("quit",True,(200,200,200),(160,0,0))
        if mousex >=0 and mousex <=quit_button.get_width():
            if mousey >= 0 and mousey <= quit_button.get_height():
                quit_button=font.render("quit",True,(255,255,255),(200,0,0))
                if click[0] == True:
                    quit_button=font.render("quit",True,(175,175,175),(120,0,0))
                    if quit_click==False and sound:
                        audio.button_press.play()
                    quit_click=True
                if quit_click and click[0]==False:
                    if sound:
                        pygame.mixer.stop()
                        audio.button_rel.play()
                    running=False
        screen.blit(quit_button,(0,0))
        guntext=font.render("guns:",True,(255,255,255),(0,0,0))
        screen.blit(guntext,(screen_w//2-guntext.get_width()//2,0))
        font = pygame.font.SysFont('consolas', 30)
        text1=font.render('1',True,(200,200,200),(160,0,0))
        if gun =='1':
            text1=font.render('1',True,(175,175,175),(120,0,0))
        else:
            if mousex>=screen_w//2-guntext.get_width()//2 and mousex<=screen_w//2+text1.get_width()-guntext.get_width()//2:
                if mousey>=guntext.get_height() and mousey<=guntext.get_height()+text1.get_height():
                    text1=font.render('1',True,(255,255,255),(200,0,0))
                    if click[0]:
                        if gun!='1' and sound:
                            audio.button_rel.play()
                        gun='1'
            if keys[pygame.K_1]:
                if gun!='1' and sound:
                    audio.button_rel.play()
                gun='1'
        screen.blit(text1,(screen_w//2-guntext.get_width()//2,guntext.get_height()))
        text2=font.render('2',True,(200,200,200),(160,0,0))
        if gun =='2':
            text2=font.render('2',True,(175,175,175),(120,0,0))
        else:
            if mousex>=screen_w//2-guntext.get_width()//2+text1.get_width() and mousex<=screen_w//2+text2.get_width()+text1.get_width()-guntext.get_width()//2:
                if mousey>=guntext.get_height() and mousey<=guntext.get_height()+text2.get_height():
                    text2=font.render('2',True,(255,255,255),(200,0,0))
                    if click[0]:
                        if gun!='2' and sound:
                            audio.button_rel.play()
                        gun='2'
            if keys[pygame.K_2]:
                if gun!='2' and sound:
                    audio.button_rel.play()
                gun='2'
        screen.blit(text2,(screen_w//2-guntext.get_width()//2+text1.get_width(),guntext.get_height()))
        text3=font.render('3',True,(200,200,200),(160,0,0))
        if gun =='3':
            text3=font.render('3',True,(175,175,175),(120,0,0))
        else:
            if mousex>=screen_w//2-guntext.get_width()//2+text1.get_width()+text2.get_width() and mousex<=screen_w//2+text3.get_width()-guntext.get_width()//2+text1.get_width()+text2.get_width():
                if mousey>=guntext.get_height() and mousey<=guntext.get_height()+text3.get_height():
                    text3=font.render('3',True,(255,255,255),(200,0,0))
                    if click[0]:
                        if gun!='3' and sound:
                            audio.button_rel.play()
                        gun='3'
            if keys[pygame.K_3]:
                if gun!='3' and sound:
                    audio.button_rel.play()
                gun='3'
        screen.blit(text3,(screen_w//2-guntext.get_width()//2+text1.get_width()+text2.get_width(),guntext.get_height()))
                
      
    #Death ------------------------------------------------------------------------------------------------------------------------------------------------
    if Game_state=='Death':
        font = pygame.font.SysFont('consolas', 140)
        title = font.render("You Died!",True,(255,255,255),(0,0,0))
        screen.blit(title,(screen_w//2-title.get_width()//2,screen_h//5-title.get_height()//2))
        title = font.render("Your score was:"+str(score),True,(255,255,255),(0,0,0))
        screen.blit(title,(screen_w//2-title.get_width()//2,screen_h//2-title.get_height()//2-180))
        if score<=highscore: #type: ignore
            title = font.render("Highscore:"+str(highscore),True,(255,255,255),(0,0,0))
        else:
            title = font.render("NEW HIGH SCORE",True,(255,255,255),(0,0,0))
        screen.blit(title,(screen_w//2-title.get_width()//2,screen_h//2-title.get_height()//2-60))

        font = pygame.font.SysFont('consolas', 25)
        quit_button=font.render("quit",True,(200,200,200),(160,0,0))
        if mousex >=0 and mousex <=quit_button.get_width():
            if mousey >= 0 and mousey <= quit_button.get_height():
                quit_button=font.render("quit",True,(255,255,255),(200,0,0))
                if click[0] == True:
                    quit_button=font.render("quit",True,(175,175,175),(120,0,0))
                    if quit_click==False and sound:
                        audio.button_press.play()
                    quit_click=True
                if quit_click and click[0]==False:
                    if sound:
                        pygame.mixer.stop()
                        audio.button_rel.play()
                    running=False
        screen.blit(quit_button,(0,0))

        font = pygame.font.SysFont('consolas', 180)
        play_button=font.render("Return",True,(200,200,200),(180,0,0))
        if mousex >=screen_w//2-play_button.get_width()//2 and mousex <=screen_w//2+play_button.get_width()//2:
            if mousey >= screen_h//1.4-play_button.get_height()//2 and mousey <= screen_h//1.4+play_button.get_height()//2:
                play_button=font.render("Return",True,(255,255,255),(200,0,0))
                if click[0]:
                    if return_click==False and sound:
                        audio.button_press.play()
                    return_click=True
                    play_button=font.render("Return",True,(175,175,175),(120,0,0))
                if click[0] == False and return_click:
                    if sound:
                        pygame.mixer.stop()
                        audio.button_rel.play()
                    Game_state='Start'
                    play_click=False
        screen.blit(play_button,(screen_w//2-play_button.get_width()//2,screen_h//1.4-play_button.get_height()//2))

    #Level_menu ----------------------------------------------------------------------------------------------
    if Game_state=='Level_menu':
        font = pygame.font.SysFont('consolas', 100)
        select_text=font.render('Select',True,(255,255,255),(0,0,0))
        screen.blit(select_text,(screen_w//2-select_text.get_width()//2,20))

        font = pygame.font.SysFont('consolas', 25)
        quit_button=font.render("quit",True,(200,200,200),(160,0,0))
        if mousex >=0 and mousex <=quit_button.get_width():
            if mousey >= 0 and mousey <= quit_button.get_height():
                quit_button=font.render("quit",True,(255,255,255),(200,0,0))
                if click[0] == True:
                    quit_button=font.render("quit",True,(175,175,175),(120,0,0))
                    if quit_click==False and sound:
                        audio.button_press.play()
                    quit_click=True
                if quit_click and click[0]==False:
                    if sound:
                        pygame.mixer.stop()
                        audio.button_rel.play()
                    running=False
        screen.blit(quit_button,(0,0))
        back_button=font.render("back",True,(200,200,200),(160,0,0))
        if mousex >=screen_w-back_button.get_width() and mousex <=screen_w:
            if mousey >= 0 and mousey <= back_button.get_height():
                back_button=font.render("back",True,(255,255,255),(200,0,0))
                if click[0] == True:
                    back_button=font.render("back",True,(175,175,175),(120,0,0))
                    if back_click==False and sound:
                        audio.button_press.play()
                    back_click=True
                if back_click and click[0]==False:
                    if sound:
                        pygame.mixer.stop()
                        audio.button_rel.play()
                    play_click=False
                    Game_state='Start'
        screen.blit(back_button,(screen_w-back_button.get_width(),0))

        #Level buttons
        Level_click,test_click,LevFile = lev_button("Test",os.path.dirname(os.path.abspath(__file__)) +'/Test_level.txt',LevFile,Level_click,test_click,0,screen_h-25,25,False)
        Level_click,lev1_click,LevFile = lev_button("Level 1",os.path.dirname(os.path.abspath(__file__)) +'/Levels/Level_1.txt',LevFile,Level_click,lev1_click,200,150,80)
        Level_click,lev2_click,LevFile = lev_button("Level 2",os.path.dirname(os.path.abspath(__file__)) +'/Levels/Level_2.txt',LevFile,Level_click,lev2_click,600,150,80)
        Level_click,lev3_click,LevFile = lev_button("Level 3",os.path.dirname(os.path.abspath(__file__)) +'/Levels/Level_3.txt',LevFile,Level_click,lev3_click,1000,150,80)
        Level_click,lev4_click,LevFile = lev_button("Level 4",os.path.dirname(os.path.abspath(__file__)) +'/Levels/Level_4.txt',LevFile,Level_click,lev4_click,200,270,80)
        Level_click,lev5_click,LevFile = lev_button("Level 5",os.path.dirname(os.path.abspath(__file__)) +'/Levels/Level_5.txt',LevFile,Level_click,lev5_click,600,270,80)
        Level_click,lev6_click,LevFile = lev_button("Level 6",os.path.dirname(os.path.abspath(__file__)) +'/Levels/Level_6.txt',LevFile,Level_click,lev6_click,1000,270,80)
        Level_click,lev7_click,LevFile = lev_button("Level 7",os.path.dirname(os.path.abspath(__file__)) +'/Levels/Level_7.txt',LevFile,Level_click,lev7_click,200,390,80)
        Level_click,lev8_click,LevFile = lev_button("Level 8",os.path.dirname(os.path.abspath(__file__)) +'/Levels/Level_8.txt',LevFile,Level_click,lev8_click,600,390,80)
        Level_click,lev9_click,LevFile = lev_button("Level 9",os.path.dirname(os.path.abspath(__file__)) +'/Levels/Level_9.txt',LevFile,Level_click,lev9_click,1000,390,80)
        Level_click,lev10_click,LevFile = lev_button("Level 10",os.path.dirname(os.path.abspath(__file__)) +'/Levels/Level_10.txt',LevFile,Level_click,lev10_click,179,510,80)
        Level_click,lev11_click,LevFile = lev_button("Level 11",os.path.dirname(os.path.abspath(__file__)) +'/Levels/Level_11.txt',LevFile,Level_click,lev11_click,579,510,80)
        Level_click,lev12_click,LevFile = lev_button("Level 12",os.path.dirname(os.path.abspath(__file__)) +'/Levels/Level_12.txt',LevFile,Level_click,lev12_click,979,510,80)

        #setup and unpacking
        if Level_click==True:
            Level_click=False
            Game_state='Campaign'
            playerX=screen_w//2
            playerY=screen_h//2
            centrex=screen_w/2
            centrey=screen_h/2
            playerDeg=0
            bullets=[]
            blocks=[]
            zombers=[]
            bosses=[]
            with open(LevFile) as file:
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
            gun='1'
            b_cooldown=0
            playerHP=100
            heal_timer=0
            boss_code.setup(bosses,blocks,screen_w,screen_h,screen)
            bossmode=False

        

    #campaign, level loader -------------------------------------------------------------------------------------------
    if Game_state=='Campaign':
        pygame.draw.circle(screen,(255,255,255),(playerX-screen_w/2+centrex,playerY-screen_h/2+centrey),45)
        pygame.draw.circle(screen,(0,0,0),(playerX-screen_w/2+centrex-30*np.sin(np.deg2rad(playerDeg-30))//1,playerY-screen_h/2+centrey-30*np.cos(np.deg2rad(playerDeg-30))//1),10)
        pygame.draw.circle(screen,(0,0,0),(playerX-screen_w/2+centrex-30*np.sin(np.deg2rad(playerDeg+30))//1,playerY-screen_h/2+centrey-30*np.cos(np.deg2rad(playerDeg+30))//1),10)
        font = pygame.font.SysFont('consolas', 25)
        quit_button=font.render("quit",True,(200,200,200),(160,0,0))
        if mousex >=0 and mousex <=quit_button.get_width():
            if mousey >= 0 and mousey <= quit_button.get_height():
                quit_button=font.render("quit",True,(255,255,255),(200,0,0))
                if click[0] == True:
                    quit_button=font.render("quit",True,(175,175,175),(120,0,0))
                    if quit_click==False and sound:
                        audio.button_press.play()
                    quit_click=True
                if quit_click and click[0]==False:
                    if sound:
                        pygame.mixer.stop()
                        audio.button_rel.play()
                    running=False
        guntext=font.render("guns:",True,(255,255,255),(0,0,0))
        font = pygame.font.SysFont('consolas', 30)
        text1=font.render('1',True,(200,200,200),(160,0,0))
        if gun =='1':
            text1=font.render('1',True,(175,175,175),(120,0,0))
        else:
            if mousex>=screen_w//2-guntext.get_width()//2 and mousex<=screen_w//2+text1.get_width()-guntext.get_width()//2:
                if mousey>=guntext.get_height() and mousey<=guntext.get_height()+text1.get_height():
                    text1=font.render('1',True,(255,255,255),(200,0,0))
                    if click[0]:
                        if gun!='1' and sound:
                            audio.button_rel.play()
                        gun='1'
            if keys[pygame.K_1]:
                if gun!='1' and sound:
                    audio.button_rel.play()
                gun='1'
        screen.blit(text1,(screen_w//2-guntext.get_width()//2,guntext.get_height()))
        text2=font.render('2',True,(200,200,200),(160,0,0))
        if gun =='2':
            text2=font.render('2',True,(175,175,175),(120,0,0))
        else:
            if mousex>=screen_w//2-guntext.get_width()//2+text1.get_width() and mousex<=screen_w//2+text2.get_width()+text1.get_width()-guntext.get_width()//2:
                if mousey>=guntext.get_height() and mousey<=guntext.get_height()+text2.get_height():
                    text2=font.render('2',True,(255,255,255),(200,0,0))
                    if click[0]:
                        if gun!='2' and sound:
                            audio.button_rel.play()
                        gun='2'
            if keys[pygame.K_2]:
                if gun!='2' and sound:
                    audio.button_rel.play()
                gun='2'
        screen.blit(text2,(screen_w//2-guntext.get_width()//2+text1.get_width(),guntext.get_height()))
        text3=font.render('3',True,(200,200,200),(160,0,0))
        if gun =='3':
            text3=font.render('3',True,(175,175,175),(120,0,0))
        else:
            if mousex>=screen_w//2-guntext.get_width()//2+text1.get_width()+text2.get_width() and mousex<=screen_w//2+text3.get_width()-guntext.get_width()//2+text1.get_width()+text2.get_width():
                if mousey>=guntext.get_height() and mousey<=guntext.get_height()+text3.get_height():
                    text3=font.render('3',True,(255,255,255),(200,0,0))
                    if click[0]:
                        if gun!='3' and sound:
                            audio.button_rel.play()
                        gun='3'
            if keys[pygame.K_3]:
                if gun!='3' and sound:
                    audio.button_rel.play()
                gun='3'
        screen.blit(text3,(screen_w//2-guntext.get_width()//2+text1.get_width()+text2.get_width(),guntext.get_height()))
        font = pygame.font.SysFont('consolas', 35)
        if gun=='1':
            bullettext=font.render("bullet charge="+str(b_cooldown)+"/60",True,(255,255,255),(0,0,0))
        elif gun=='2':
            bullettext=font.render("bullet charge="+str(b_cooldown)+"/30",True,(255,255,255),(0,0,0))
        elif gun=='3':
            bullettext=font.render("bullet charge="+str(b_cooldown)+"/5",True,(255,255,255),(0,0,0))

        #movement
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if keys[pygame.K_LSHIFT]:
                playerDeg-=3
            else:
                playerDeg-=6
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if keys[pygame.K_LSHIFT]:
                playerDeg+=3
            else:
                playerDeg+=6
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            playerX+=4*np.sin(np.deg2rad(playerDeg))
            playerY+=4*np.cos(np.deg2rad(playerDeg))
            if bossmode==False:
                centrex-=4*np.sin(np.deg2rad(playerDeg))
                centrey-=4*np.cos(np.deg2rad(playerDeg))
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            playerX-=6*np.sin(np.deg2rad(playerDeg))
            playerY-=6*np.cos(np.deg2rad(playerDeg))
            if bossmode==False:
                centrex+=6*np.sin(np.deg2rad(playerDeg))
                centrey+=6*np.cos(np.deg2rad(playerDeg))

        for i in range(len(blocks)):
            (x,y,w,h,mode)=blocks[i]
            if mode==0:
                if (x-screen_w/2+centrex>-200 or x+w-screen_w/2+centrex>-200) and (y-screen_h/2+centrey>-200 or y+h-screen_h/2+centrey>-200) and (y-screen_h/2+centrey<screen_h+200 or y+h-screen_h/2+centrey<screen_h+200) and (x-screen_w/2+centrex<screen_w+200 or x+w-screen_w/2+centrex<screen_w+200):
                    if playerX>x-45 and playerX<x+w and playerY>y and playerY<y+h:
                        if bossmode==False:
                            centrex+=playerX-x+45
                        playerX-=playerX-x+45
                    elif playerX>x and playerX<x+w+45 and playerY>y and playerY<y+h:
                        if bossmode==False:
                            centrex-=x+w+45-playerX
                        playerX+=x+w+45-playerX
                    elif playerX>x and playerX<x+w and playerY>y-45 and playerY<y+h:
                        if bossmode==False:
                            centrey+=playerY-y+45
                        playerY-=playerY-y+45
                    elif playerX>x and playerX<x+w and playerY>y and playerY<y+h+45:
                        if bossmode==False:
                            centrey-=y+h+45-playerY
                        playerY+=y+h+45-playerY
                    elif np.sqrt((playerX-x)**2+(playerY-y)**2)<=45:
                        if bossmode==False:
                            centrex+=(45-np.sqrt((playerX-x)**2+(playerY-y)**2))/np.sqrt((playerX-x)**2+(playerY-y)**2)*(x-playerX)
                            centrey+=(45-np.sqrt((playerX-x)**2+(playerY-y)**2))/np.sqrt((playerX-x)**2+(playerY-y)**2)*(y-playerY)
                        playerX2=playerX
                        playerX2-=(45-np.sqrt((playerX-x)**2+(playerY-y)**2))/np.sqrt((playerX-x)**2+(playerY-y)**2)*(x-playerX)
                        playerY-=(45-np.sqrt((playerX-x)**2+(playerY-y)**2))/np.sqrt((playerX-x)**2+(playerY-y)**2)*(y-playerY)
                        playerX=playerX2
                    elif np.sqrt((playerX-(x+w))**2+(playerY-y)**2)<=45:
                        if bossmode==False:
                            centrex+=(45-np.sqrt((playerX-(x+w))**2+(playerY-y)**2))/np.sqrt((playerX-(x+w))**2+(playerY-y)**2)*((x+w)-playerX)
                            centrey+=(45-np.sqrt((playerX-(x+w))**2+(playerY-y)**2))/np.sqrt((playerX-(x+w))**2+(playerY-y)**2)*(y-playerY)
                        playerX2=playerX
                        playerX2-=(45-np.sqrt((playerX-(x+w))**2+(playerY-y)**2))/np.sqrt((playerX-(x+w))**2+(playerY-y)**2)*((x+w)-playerX)
                        playerY-=(45-np.sqrt((playerX-(x+w))**2+(playerY-y)**2))/np.sqrt((playerX-(x+w))**2+(playerY-y)**2)*(y-playerY)
                        playerX=playerX2
                    elif np.sqrt((playerX-x-w)**2+(playerY-(y+h))**2)<=45:
                        if bossmode==False:
                            centrex+=(45-np.sqrt((playerX-(x+w))**2+(playerY-y-h)**2))/np.sqrt((playerX-(x+w))**2+(playerY-y-h)**2)*((x+w)-playerX)
                            centrey+=(45-np.sqrt((playerX-(x+w))**2+(playerY-y-h)**2))/np.sqrt((playerX-(x+w))**2+(playerY-y-h)**2)*(y+h-playerY)
                        playerX2=playerX
                        playerX2-=(45-np.sqrt((playerX-(x+w))**2+(playerY-y-h)**2))/np.sqrt((playerX-(x+w))**2+(playerY-y-h)**2)*((x+w)-playerX)
                        playerY-=(45-np.sqrt((playerX-(x+w))**2+(playerY-(y+h))**2))/np.sqrt((playerX-(x+w))**2+(playerY-y-h)**2)*(y+h-playerY)
                        playerX=playerX2
                    elif np.sqrt((playerX-(x))**2+(playerY-(y+h))**2)<=45:
                        if bossmode==False:
                            centrex+=(45-np.sqrt((playerX-x)**2+(playerY-y-h)**2))/np.sqrt((playerX-(x))**2+(playerY-y-h)**2)*(x-playerX)
                            centrey+=(45-np.sqrt((playerX-x)**2+(playerY-y-h)**2))/np.sqrt((playerX-(x))**2+(playerY-y-h)**2)*(y+h-playerY)
                        playerX2=playerX
                        playerX2-=(45-np.sqrt((playerX-x)**2+(playerY-y-h)**2))/np.sqrt((playerX-(x))**2+(playerY-y-h)**2)*(x-playerX)
                        playerY-=(45-np.sqrt((playerX-x)**2+(playerY-y-h)**2))/np.sqrt((playerX-(x))**2+(playerY-y-h)**2)*(y+h-playerY)
                        playerX=playerX2
                    n=0
                    while n<len(bullets):
                        (x2,y2,angle2,dmg2,size2,speed2) = bullets[n]
                        if x2+size2>x and x2-size2<x+w and y2+size2>y and y2-size2<y+h:
                            bullets.pop(n)
                            if sound:
                                audio.wallhit.play()
                        elif (x2-(speed2/2)*np.sin(np.deg2rad(angle2)))+size2>x and (x2-(speed/2)*np.sin(np.deg2rad(angle2)))-size2<x+w and (y2-(speed2/2)*np.cos(np.deg2rad(angle2)))+size2>y and (y2-(speed2/2)*np.cos(np.deg2rad(angle2)))-size2<y+h:
                            bullets.pop(n)
                            if sound:
                                audio.wallhit.play()
                        else:
                            n+=1
            if mode==1:
                #player win
                pygame.draw.rect(screen,(255,255,0),pygame.Rect(x-screen_w/2+centrex,y-screen_h/2+centrey,w,h),mode)
                if playerX>x-45 and playerX<x+w+45 and playerY>y-45 and playerY<y+h+45:
                    Game_state='Win'
                    if sound:
                        pygame.mixer.stop()
                        audio.win1.play()
                        audio.win2.play()
                        audio.win3.play()
                    #add a text file later to keep track of levels won
        for i in blocks:
            (x,y,w,h,mode)=i
            if mode==1 and (x-screen_w/2+centrex>-200 or x+w-screen_w/2+centrex>-200) and (y-screen_h/2+centrey>-200 or y+h-screen_h/2+centrey>-200) and (y-screen_h/2+centrey<screen_h+200 or y+h-screen_h/2+centrey<screen_h+200) and (x-screen_w/2+centrex<screen_w+200 or x+w-screen_w/2+centrex<screen_w+200):
                pygame.draw.rect(screen,(255,255,0),pygame.Rect(x-screen_w/2+centrex,y-screen_h/2+centrey,w,h),mode)
            else:
                pygame.draw.rect(screen,(255,255,255),pygame.Rect(x-screen_w/2+centrex,y-screen_h/2+centrey,w,h),mode)

                
                        
        if keys[pygame.K_SPACE]:
            if sound:
                audio.bullet_charge.play()
            b_cooldown+=1
            if gun=='1':
                if b_cooldown>=60:
                    if sound:
                        audio.bullet1.play()
                    bullets.append((playerX,playerY,playerDeg,100,13,60))
                    b_cooldown=0
            elif gun=='2':
                if b_cooldown>=30:
                    if sound:
                        audio.bullet2.play()
                    bullets.append((playerX,playerY,playerDeg+8,8,7,16))
                    bullets.append((playerX,playerY,playerDeg-8,8,7,16))
                    bullets.append((playerX,playerY,playerDeg-24,8,7,16))
                    bullets.append((playerX,playerY,playerDeg+24,8,7,16))
                    bullets.append((playerX,playerY,playerDeg-40,8,7,16))
                    bullets.append((playerX,playerY,playerDeg+40,8,7,16))
                    b_cooldown=0
            elif gun=='3':
                if b_cooldown>=5:
                    if sound:
                        audio.bullet3.play()
                    bullets.append((playerX,playerY,playerDeg+rand.randint(0,32)-16,5,6,16))
                    b_cooldown=0
        else:
            b_cooldown=0

        #drawing bullets
        n=0
        while n<len(bullets):
            (x,y,angle,dmg,size,speed) = bullets[n]

            x-=speed*np.sin(np.deg2rad(angle))
            y-=speed*np.cos(np.deg2rad(angle))
            pygame.draw.circle(screen,(180,180,180),(x-screen_w/2+centrex,y-screen_h/2+centrey),size)

            if x-screen_w/2+centrex>-screen_w and x-screen_w/2+centrex<2*screen_w and y-screen_h/2+centrey>-screen_h and y-screen_h/2+centrey<2*screen_h:
                bullets[n] = (x,y,angle,dmg,size,speed)
                n+=1
            else:
                bullets.pop(n)

        #zombie stuff
        n=0
        while n<len(zombers):
            (x,y,hp,dmg,size,colour,speed,dmg_timer,eyerange) = zombers[n]
            if (x+size-screen_w/2+centrex>-200) and (y+size-screen_h/2+centrey>-200) and (y-size-screen_h/2+centrey<screen_h+200) and (x-size-screen_w/2+centrex<screen_w+200):
                if np.sqrt((playerY-y)**2+(playerX-x)**2)<eyerange:
                    if np.sqrt((playerX-x)**2+(playerY-y)**2) >= 45+size-10:
                        x+= speed/np.sqrt((playerX-x)**2+(playerY-y)**2)*(playerX-x)
                        y+= speed/np.sqrt((playerX-x)**2+(playerY-y)**2)*(playerY-y)
                for i in blocks:
                    (x2,y2,w2,h2,mode2) = i
                    if mode2==0 and x>x2-size and x<x2+size+w2 and y>y2-size and y<y2+size+h2:
                        if (x-screen_w/2+centrex>-200 or x+w-screen_w/2+centrex>-200) and (y-screen_h/2+centrey>-200 or y+h-screen_h/2+centrey>-200) and (y-screen_h/2+centrey<screen_h+200 or y+h-screen_h/2+centrey<screen_h+200) and (x-screen_w/2+centrex<screen_w+200 or x+w-screen_w/2+centrex<screen_w+200):
                            if x>x2-size and x<x2+w2 and y>y2 and y<y2+h2:
                               x-=x-x2+size
                            elif x>x2 and x<x2+w2+size and y>y2 and y<y2+h2:
                                x-=x-x2-w2-size
                            elif x>x2 and x<x2+w2 and y>y2-size and y<y2+h2:
                                y-=y-y2+size
                            elif x>x2 and x<x2+w2 and y>y2 and y<y2+h2+size:
                                y-=y-y2-h2-size
                            elif np.sqrt((x-x2)**2+(y-y2)**2)<=size:
                                x-=(size-np.sqrt((x-x2)**2+(y-y2)**2))/np.sqrt((x-x2)**2+(y-y2)**2)*(x2-x)
                                y-=(size-np.sqrt((x-x2)**2+(y-y2)**2))/np.sqrt((x-x2)**2+(y-y2)**2)*(y2-y)
                            elif np.sqrt((x-x2-w2)**2+(y-y2)**2)<=size:
                                x-=(size-np.sqrt((x-x2-w2)**2+(y-y2)**2))/np.sqrt((x-x2-w2)**2+(y-y2)**2)*(x2+w2-x)
                                y-=(size-np.sqrt((x-x2-w2)**2+(y-y2)**2))/np.sqrt((x-x2-w2)**2+(y-y2)**2)*(y2-y)
                            elif np.sqrt((x-x2-w2)**2+(y-y2-h2)**2)<=size:
                                x-=(size-np.sqrt((x-x2-w2)**2+(y-y2-h2)**2))/np.sqrt((x-x2-w2)**2+(y-y2-h2)**2)*(x2+w2-x)
                                y-=(size-np.sqrt((x-x2-w2)**2+(y-y2-h2)**2))/np.sqrt((x-x2-w2)**2+(y-y2-h2)**2)*(y2+h2-y)
                            elif np.sqrt((x-x2)**2+(y-y2-h2)**2)<=size:
                                x-=(size-np.sqrt((x-x2)**2+(y-y2-h2)**2))/np.sqrt((x-x2)**2+(y-y2-h2)**2)*(x2-x)
                                y-=(size-np.sqrt((x-x2)**2+(y-y2-h2)**2))/np.sqrt((x-x2)**2+(y-y2-h2)**2)*(y2+h2-y)
                        
                n2=0
                while n2<len(bullets) and hp>0:
                    (x2,y2,angle2,dmg2,size2,speed2) = bullets[n2]
                    if np.sqrt((x-x2)**2+(y-y2)**2) <= size+size2:
                        bullets.pop(n2)
                        if sound:
                            audio.zomhit2.play()
                        hp-=dmg2
                    elif np.sqrt((x-x2-(speed2/2)*np.sin(np.deg2rad(angle2)))**2+(y-y2-(speed2/2)*np.cos(np.deg2rad(angle2)))**2) <= size+size2:
                        bullets.pop(n2)
                        if sound:
                            audio.zomhit2.play()
                        hp-=dmg2
                    else:
                        n2+=1

                if np.sqrt((playerX-x)**2+(playerY-y)**2) <= 45+size:
                    if dmg_timer==30:
                        if sound:
                            audio.bite.play()
                        playerHP-=dmg
                        dmg_timer=0
                        heal_timer=-286
                if dmg_timer<30:
                    dmg_timer+=1
            
                if hp<=0:
                    zombers.pop(n)
                    if sound:
                        audio.zomhit1.play()
                else:
                    zombers[n] = (x,y,hp,dmg,size,colour,speed,dmg_timer,eyerange)
                    n+=1
                    pygame.draw.circle(screen,colour,(x-screen_w/2+centrex,y-screen_h/2+centrey),size)
                    if np.sqrt((playerX-x)**2+(playerY-y)**2) <= eyerange:
                        if playerY<y:
                            pygame.draw.circle(screen,(255,0,0),((x-screen_w/2+centrex)-(size-15)*np.sin(np.arcsin((x-playerX)/((np.sqrt((playerX-x)**2+(playerY-y)**2))))+np.deg2rad(30)),(y-screen_h/2+centrey)-(size-15)*np.cos(np.arcsin((x-playerX)/((np.sqrt((playerX-x)**2+(playerY-y)**2))))+np.deg2rad(30))),10)
                            pygame.draw.circle(screen,(255,0,0),((x-screen_w/2+centrex)-(size-15)*np.sin(np.arcsin((x-playerX)/((np.sqrt((playerX-x)**2+(playerY-y)**2))))-np.deg2rad(30)),(y-screen_h/2+centrey)-(size-15)*np.cos(np.arcsin((x-playerX)/((np.sqrt((playerX-x)**2+(playerY-y)**2))))-np.deg2rad(30))),10)
                        else:
                            pygame.draw.circle(screen,(255,0,0),((x-screen_w/2+centrex)-(size-15)*np.sin(np.arcsin((x-playerX)/((np.sqrt((playerX-x)**2+(playerY-y)**2))))+np.deg2rad(30)),(y-screen_h/2+centrey)+(size-15)*np.cos(np.arcsin((x-playerX)/((np.sqrt((playerX-x)**2+(playerY-y)**2))))+np.deg2rad(30))),10)
                            pygame.draw.circle(screen,(255,0,0),((x-screen_w/2+centrex)-(size-15)*np.sin(np.arcsin((x-playerX)/((np.sqrt((playerX-x)**2+(playerY-y)**2))))-np.deg2rad(30)),(y-screen_h/2+centrey)+(size-15)*np.cos(np.arcsin((x-playerX)/((np.sqrt((playerX-x)**2+(playerY-y)**2))))-np.deg2rad(30))),10)        
                    else:
                        pygame.draw.circle(screen,(0,0,0),(x-screen_w/2+centrex-size+15,y-screen_h/2+centrey),10)
                        pygame.draw.circle(screen,(0,0,0),(x-screen_w/2+centrex+size-15,y-screen_h/2+centrey),10)
            else:
                n+=1
            #zombie stuff

        centrex,centrey,bossmode,playerHP,playerX,playerY=boss_code.fight(bosses,blocks,bullets,zombers,playerX,playerY,centrex,centrey,screen_w,screen_h,bossmode,playerHP,screen,sound)

        if playerHP<100 and heal_timer==30:
            playerHP+=1
            heal_timer=0
        if heal_timer<30:
            heal_timer+=1

        if playerHP<=0 or keys[pygame.K_k]:
            Game_state='Level_Death'
            pygame.mixer.stop()
            if sound:
                audio.death1.play()
                audio.death2.play()
                audio.death3.play()
            Lreturn_click=False

        screen.blit(bullettext,(screen_w//2-bullettext.get_width()//2,screen_h-bullettext.get_height()))
        screen.blit(guntext,(screen_w//2-guntext.get_width()//2,0))
        screen.blit(quit_button,(0,0))
        screen.blit(text1,(screen_w//2-guntext.get_width()//2,guntext.get_height()))
        screen.blit(text2,(screen_w//2-guntext.get_width()//2+text2.get_width(),guntext.get_height()))
        screen.blit(text3,(screen_w//2-guntext.get_width()//2+text1.get_width()+text2.get_width(),guntext.get_height()))
        pygame.draw.rect(screen,(180,0,0),pygame.Rect(screen_w-205,screen_h-60,200,50))
        pygame.draw.rect(screen,(0,180,0),pygame.Rect(screen_w-205,screen_h-60,2*playerHP,50))
        font = pygame.font.SysFont('consolas', 50)
        HP_text=font.render("HP:"+str(playerHP),True,(255,255,255),(0,0,0))
        screen.blit(HP_text,(screen_w-205-HP_text.get_width(),screen_h-35-HP_text.get_height()//2))

    #Level death ----------------------------------------------------------------------------------------------------------------------
    if Game_state=='Level_Death':
        font = pygame.font.SysFont('consolas', 280)
        title = font.render("You Died!",True,(255,255,255),(0,0,0))
        screen.blit(title,(screen_w//2-title.get_width()//2,screen_h//2-title.get_height()//2))

        font = pygame.font.SysFont('consolas', 25)
        quit_button=font.render("quit",True,(200,200,200),(160,0,0))
        if mousex >=0 and mousex <=quit_button.get_width():
            if mousey >= 0 and mousey <= quit_button.get_height():
                quit_button=font.render("quit",True,(255,255,255),(200,0,0))
                if click[0] == True:
                    quit_button=font.render("quit",True,(175,175,175),(120,0,0))
                    if quit_click==False and sound:
                        audio.button_press.play()
                    quit_click=True
                if quit_click and click[0]==False:
                    if sound:
                        pygame.mixer.stop()
                        audio.button_rel.play()
                    running=False
        screen.blit(quit_button,(0,0))
        back_button=font.render("back",True,(200,200,200),(160,0,0))
        if mousex >=screen_w-back_button.get_width() and mousex <=screen_w:
            if mousey >= 0 and mousey <= back_button.get_height():
                back_button=font.render("back",True,(255,255,255),(200,0,0))
                if click[0] == True:
                    back_button=font.render("back",True,(175,175,175),(120,0,0))
                    if back_click==False and sound:
                        audio.button_press.play()
                    back_click=True
                if back_click and click[0]==False:
                    if sound:
                        pygame.mixer.stop()
                        audio.button_rel.play()
                    play_click=False
                    back_click=False
                    Game_state='Level_menu'
        screen.blit(back_button,(screen_w-back_button.get_width(),0))

    #level win -----------------------------------------------------------------------------------------------------------
    if Game_state=='Win':
        font = pygame.font.SysFont('consolas', 280)
        title = font.render("You Won!",True,(255,255,255),(0,0,0))
        screen.blit(title,(screen_w//2-title.get_width()//2,screen_h//2-title.get_height()//2))

        font = pygame.font.SysFont('consolas', 25)
        quit_button=font.render("quit",True,(200,200,200),(160,0,0))
        if mousex >=0 and mousex <=quit_button.get_width():
            if mousey >= 0 and mousey <= quit_button.get_height():
                quit_button=font.render("quit",True,(255,255,255),(200,0,0))
                if click[0] == True:
                    quit_button=font.render("quit",True,(175,175,175),(120,0,0))
                    if quit_click==False and sound:
                        audio.button_press.play()
                    quit_click=True
                if quit_click and click[0]==False:
                    if sound:
                        pygame.mixer.stop()
                        audio.button_rel.play()
                    running=False
        screen.blit(quit_button,(0,0))
        back_button=font.render("back",True,(200,200,200),(160,0,0))
        if mousex >=screen_w-back_button.get_width() and mousex <=screen_w:
            if mousey >= 0 and mousey <= back_button.get_height():
                back_button=font.render("back",True,(255,255,255),(200,0,0))
                if click[0] == True:
                    back_button=font.render("back",True,(175,175,175),(120,0,0))
                    if back_click==False and sound:
                        audio.button_press.play()
                    back_click=True
                if back_click and click[0]==False:
                    if sound:
                        pygame.mixer.stop()
                        audio.button_rel.play()
                    play_click=False
                    back_click=False
                    Game_state='Level_menu'
        screen.blit(back_button,(screen_w-back_button.get_width(),0))

            
 
    pygame.display.flip()

    endTime : int = int(time.time()*1000)
    print(endTime-startTime)

    clock.tick(60)

pygame.quit()
