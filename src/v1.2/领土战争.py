import pygame,math,random,time
print("默认配置：棋盘范围20*20，四个国家，炮台位置：第一国[4,4]，第二国[4,15]，第三国[15,4]，第四国[15,15]")
default=""
while True:
    default=input("使用默认配置？（Y是（使用默认配置），N否（使用GameConfig.txt中的配置）），注意必须大写")
    if default=="Y":
        xScale=20
        yScale=20
        blocksize=12
        colors=[pygame.Color(255,0,0),pygame.Color(0,255,0),pygame.Color(0,0,255),pygame.Color(255,255,0)]
        towers=[[[4,4]],[[4,15]],[[15,4]],[[15,15]]]
        break
    elif default=="N":
        file=open("GameConfig.txt","r")
        lines=file.readlines()
        xScale=int(lines[0])
        yScale=int(lines[1])
        blocksize=int(lines[2])
        countries=int(lines[3])
        colors=[]
        towers=[]
        for g in range(countries):
            colors.append(eval(lines[g+4]))
            towers.append(eval(lines[g+countries+4]))
        break
    else:
        continue
center=[xScale//2,yScale//2]
map2d=[[-1 for i in range(xScale)] for j in range(yScale)]
shells=[]
pygame.init()
screen=pygame.display.set_mode([min(1920,max(640,xScale*blocksize)),min(1920,max(640,yScale*blocksize))])
def throw_shells():
    for k in range(len(towers)):
        for l in towers[k]:
            shells.append([l[0],l[1],k,1*math.cos(xScale*random.random()*math.pi),1*math.sin(yScale*random.random()*math.pi)])
def changeblock(m):
    if m[2]!=map2d[min(xScale-1,max(0,math.floor(m[0])))][min(yScale-1,max(0,math.floor(m[1])))]:
        for q in towers:
            for r in q:
                if [min(xScale-1,max(0,math.floor(m[0]))),min(yScale-1,max(0,math.floor(m[1])))]==r and map2d[math.floor(m[0])][math.floor(m[1])]>0:
                    q.remove(r)
        map2d[min(xScale-1,max(0,math.floor(m[0])))][min(yScale-1,max(0,math.floor(m[1])))]=m[2]
        shells.remove(m)
def shells_move():
    for n in shells:
        n[0]+=n[3]
        n[1]+=n[4]
        if n[0]<0:
            n[3]=-n[3]
        elif n[0]>=xScale-1:
            n[3]=-n[3]
        if n[1]<0:
            n[4]=-n[4]
        elif n[1]>=yScale-1:
            n[4]=-n[4]
        changeblock(n)
while True:
    timea=time.time()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit()
        elif event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                blocksize+=1
            elif event.button==3:
                blocksize=max(blocksize-1,1)
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                center[1]-=1
            elif event.key==pygame.K_LEFT:
                center[0]-=1
            elif event.key==pygame.K_DOWN:
                center[1]+=1
            elif event.key==pygame.K_RIGHT:
                center[0]+=1
    screen.fill(pygame.Color(127,127,127))
    for t in range(xScale):
        for u in range(yScale):
            if map2d[t][u]<0:
                pygame.draw.rect(screen,pygame.Color(0,0,0),[pygame.display.get_surface().get_width()//2+blocksize*(t-center[0]),pygame.display.get_surface().get_height()//2+blocksize*(u-center[1]),blocksize,blocksize],0)
            else:
                pygame.draw.rect(screen,colors[map2d[t][u]],[pygame.display.get_surface().get_width()//2+blocksize*(t-center[0]),pygame.display.get_surface().get_height()//2+blocksize*(u-center[1]),blocksize,blocksize],0)
    for v in shells:
        pygame.draw.circle(screen,pygame.Color(0,0,0),[pygame.display.get_surface().get_width()//2+math.floor(blocksize*(v[0]-center[0])),pygame.display.get_surface().get_height()//2+math.floor(blocksize*(v[1]-center[1]))],2,0)
    throw_shells()
    shells_move()
    pygame.display.flip()
    timeb=time.time()
    pygame.display.set_caption("领土战争 V1.2: "+str(1/(timeb-timea))+" FPS")
