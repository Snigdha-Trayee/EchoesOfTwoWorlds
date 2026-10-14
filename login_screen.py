import pygame, sys, subprocess
from pathlib import Path
from harini_quiz_data import HARINI_QUIZZES
pygame.init()
BASE=Path(__file__).resolve().parent
W,H=1280,720
screen=pygame.display.set_mode((W,H)); pygame.display.set_caption('Echoes of Two Worlds')
clock=pygame.time.Clock(); FONT=pygame.font.Font(None,30); SMALL=pygame.font.Font(None,24); TITLE=pygame.font.Font(None,58)
WHITE=(245,245,255); GOLD=(255,215,120); PANEL=(18,15,48); CYAN=(110,235,255)
def load(name):
 p=BASE/'assets'/'harini'/name
 try:
  im=pygame.image.load(str(p)).convert(); return pygame.transform.smoothscale(im,(W,H))
 except Exception: return None
background=load('background.png')
clue_imgs=[load('clues1.png'),load('clues2.png'),load('clues3.png')]
portal_img=load('portal.png')
def draw_text(txt,y,font=FONT,color=WHITE):
 s=font.render(txt,True,color); screen.blit(s,s.get_rect(center=(W//2,y)))
def button(text,rect,mouse):
 hover=rect.collidepoint(mouse); pygame.draw.rect(screen,(64,51,112) if hover else (31,28,75),rect,border_radius=14); pygame.draw.rect(screen,GOLD,rect,2,border_radius=14); draw=FONT.render(text,True,WHITE); screen.blit(draw,draw.get_rect(center=rect.center))
 return rect
def option_button(text, rect, mouse):
    hover = rect.collidepoint(mouse)

    pygame.draw.rect(
        screen,
        (64, 51, 112) if hover else (31, 28, 75),
        rect,
        border_radius=14
    )
    pygame.draw.rect(screen, GOLD, rect, 2, border_radius=14)

    max_width = rect.width - 30
    max_height = rect.height - 6

    # Automatically find a font size that fits the option.
    for size in range(30, 13, -1):
        font = pygame.font.Font(None, size)
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = (current_line + " " + word).strip()

            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        if len(lines) <= 2 and len(lines) * font.get_linesize() <= max_height:
            break

    # Display the option text centred inside the button.
    line_height = font.get_linesize()
    total_height = len(lines) * line_height
    start_y = rect.centery - total_height // 2

    for i, line in enumerate(lines):
        rendered = font.render(line, True, WHITE)
        text_rect = rendered.get_rect(
            center=(rect.centerx, start_y + i * line_height + line_height // 2)
        )
        screen.blit(rendered, text_rect)

    return rect
screen_name='title'; username=''; password=''; focus='user'; error=''; clue_i=0; quiz_q=0; selected=-1; feedback=''; quiz_done=False
quiz_names=list(HARINI_QUIZZES); MAX_OPTIONS=max(len(q[1]) for rune in HARINI_QUIZZES.values() for q in rune['questions']); btns=[pygame.Rect(390,350+i*52,500,44) for i in range(MAX_OPTIONS)]; submit_rect=pygame.Rect(440,570,400,48)
running=True
while running:
 mouse=pygame.mouse.get_pos()
 for e in pygame.event.get():
  if e.type==pygame.QUIT: running=False
  if e.type==pygame.KEYDOWN:
   if e.key==pygame.K_ESCAPE:
    if screen_name in ('login','welcome','portal','clue','quiz'): screen_name='title'
    else: running=False
   elif screen_name=='login':
    if e.key==pygame.K_TAB: focus='pass' if focus=='user' else 'user'
    elif e.key==pygame.K_BACKSPACE:
     if focus=='user': username=username[:-1]
     else: password=password[:-1]
    elif e.key==pygame.K_RETURN:
     if len(username.strip())>=3 and len(password)>=4: screen_name='welcome'; error=''
     else: error='Username needs 3+ characters; password needs 4+.'
    elif e.unicode.isprintable():
     if focus=='user': username+=e.unicode
     else: password+=e.unicode
   elif screen_name=='quiz':
    if e.key in (pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4): selected=e.key-pygame.K_1
    elif e.key==pygame.K_RETURN and selected>=0:
     q=HARINI_QUIZZES[quiz_names[clue_i]]['questions'][quiz_q]
     if selected==q[2]: feedback='Correct! '+('Next question →' if quiz_q<2 else 'Rune restored! Press N.')
     else: feedback='Not quite — try again.'
     if selected==q[2]: quiz_done=True
    elif e.key==pygame.K_n and quiz_done:
     quiz_done=False; feedback=''; selected=-1
     if quiz_q<2: quiz_q+=1
     elif clue_i<2: clue_i+=1; quiz_q=0; screen_name='clue'
     else: screen_name='restored'
  if e.type==pygame.MOUSEBUTTONDOWN and e.button==1:
   if screen_name=='title':
    if pygame.Rect(440,420,400,65).collidepoint(e.pos): screen_name='login'
   elif screen_name=='login':
    if pygame.Rect(360,350,560,48).collidepoint(e.pos): focus='user'
    elif pygame.Rect(360,430,560,48).collidepoint(e.pos): focus='pass'
    elif pygame.Rect(440,520,400,55).collidepoint(e.pos):
     if len(username.strip())>=3 and len(password)>=4: screen_name='welcome'; error=''
     else: error='Username needs 3+ characters; password needs 4+.'
   elif screen_name=='welcome':
    if pygame.Rect(440,460,400,65).collidepoint(e.pos): screen_name='portal'
   elif screen_name=='portal':
    if pygame.Rect(440,550,400,60).collidepoint(e.pos): clue_i=0; screen_name='clue'
   elif screen_name=='clue':
    if pygame.Rect(440,570,400,60).collidepoint(e.pos): screen_name='quiz'; quiz_q=0; selected=-1; feedback=''; quiz_done=False
   elif screen_name=='quiz':
    for i,r in enumerate(btns):
     if r.collidepoint(e.pos): selected=i
    if submit_rect.collidepoint(e.pos) and selected>=0:
     q=HARINI_QUIZZES[quiz_names[clue_i]]['questions'][quiz_q]
     if selected==q[2]: feedback='Correct! Press N to continue.'; quiz_done=True
     else: feedback='Not quite — try again.'
   elif screen_name=='restored':
    if pygame.Rect(440,520,400,60).collidepoint(e.pos):
     subprocess.Popen([sys.executable,str(BASE/'main.py')],cwd=str(BASE)); running=False
 if background: screen.blit(background,(0,0))
 else: screen.fill((18,20,50))
 shade=pygame.Surface((W,H),pygame.SRCALPHA); shade.fill((5,6,25,120)); screen.blit(shade,(0,0))
 if screen_name=='title':
  draw_text('ECHOES OF TWO WORLDS',175,TITLE,GOLD); draw_text('TWO REALMS • ONE TRUTH',230,SMALL); button('BEGIN THE GAME',pygame.Rect(440,420,400,65),mouse); draw_text('Explore  •  Solve  •  Uncover',650,SMALL)
 elif screen_name=='login':
  draw_text('ENTER YOUR REALM',170,TITLE,GOLD); draw_text('Adventurer Name (click field, then type)',285); pygame.draw.rect(screen,PANEL,(360,350,560,48),border_radius=8); draw_text(username or 'Type username...',374,SMALL,CYAN if focus=='user' else WHITE); draw_text('Secret Passphrase',410); pygame.draw.rect(screen,PANEL,(360,430,560,48),border_radius=8); draw_text(('•'*len(password)) or 'Type password...',454,SMALL,CYAN if focus=='pass' else WHITE); button('ENTER THE WORLD',pygame.Rect(440,520,400,55),mouse); draw_text(error,600,SMALL,(255,140,150))
 elif screen_name=='welcome': draw_text('WELCOME, '+username.strip().upper(),250,TITLE,GOLD); draw_text('Your journey through the two worlds awaits.',325); button('CONTINUE TO PORTAL',pygame.Rect(440,460,400,65),mouse)
 elif screen_name=='portal':
  draw_text('THE PORTAL AWAKENS',200,TITLE,GOLD); draw_text('Three ancient runes guard the memories of two worlds.',300); button('DISCOVER THE RUNES',pygame.Rect(440,550,400,60),mouse)
 elif screen_name=='clue':
  name=quiz_names[clue_i]; qdata=HARINI_QUIZZES[name]; img=clue_imgs[clue_i]
  if img: screen.blit(pygame.transform.smoothscale(img,(330,220)),(475,245))
  draw_text(name.upper(),125,TITLE,GOLD); draw_text(qdata['description'],190); draw_text(f'Rune {clue_i+1} of 3',500,SMALL); button('START RUNE CHALLENGE',pygame.Rect(440,570,400,60),mouse)
 elif screen_name=='quiz':
  name=quiz_names[clue_i]; q=HARINI_QUIZZES[name]['questions'][quiz_q]; draw_text(name.upper()+' CHALLENGE',70,TITLE,GOLD); draw_text(f'Question {quiz_q+1} of 3',130,SMALL); 
  for i,line in enumerate([q[0][j:j+72] for j in range(0,len(q[0]),72)]): draw_text(line,190+i*32,FONT)
  for i,opt in enumerate(q[1]):
    option_button(f'{i+1}. {opt}', btns[i], mouse)
  button('SUBMIT ANSWER',submit_rect,mouse); draw_text(feedback,635,SMALL,GOLD); draw_text('Choose an option, click Submit, then press N after a correct answer.',675,SMALL)
 elif screen_name=='restored':
  draw_text('THE RUNES ARE RESTORED!',230,TITLE,GOLD); draw_text('Moon, Sun and Star memories are united.',310); button('START PYGAME ADVENTURE',pygame.Rect(440,520,400,60),mouse)
 pygame.display.flip(); clock.tick(60)
pygame.quit()
