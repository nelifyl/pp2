import pygame
from datetime import datetime
from tools import draw_shape, flood_fill

pygame.init()

W, H, TH = 900, 650, 50
screen = pygame.display.set_mode((W, H))

canvas = pygame.Surface((W, H - TH))
canvas.fill((255, 255, 255))

clock = pygame.time.Clock()

font_small = pygame.font.SysFont("Arial", 13)
font = pygame.font.SysFont("Arial", 22)

TOOLS = ["pencil","line","rect","circle","square","rtriangle","etriangle","rhombus","eraser","fill","text"]
COLORS = [(0,0,0),(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,165,0),(128,0,128),(255,255,255),(165,42,42)]
BSIZES = [2,5,10,15,20]

tool = "pencil"
color = (0,0,0)
bi = 0

drawing = False
sp = None
lp = None

ta = False
tp = None
tb = ""

preview_pos = None

# ================= UI STATE =================
show_picker = False
hover_tool = None
hover_color = None
hover_size = None

# ================= UNDO =================
undo_stack = []
redo_stack = []

def save_state():
    undo_stack.append(canvas.copy())
    if len(undo_stack) > 30:
        undo_stack.pop(0)

def undo():
    global canvas
    if undo_stack:
        redo_stack.append(canvas.copy())
        canvas = undo_stack.pop()

def redo():
    global canvas
    if redo_stack:
        undo_stack.append(canvas.copy())
        canvas = redo_stack.pop()

# ================= HELPERS =================
def cp(pos): return (pos[0], pos[1] - TH)
def on_cv(pos): return pos[1] >= TH

def toolbar():
    global hover_tool, hover_color, hover_size

    mx,my = pygame.mouse.get_pos()

    pygame.draw.rect(screen, (45,45,45), (0,0,W,TH))

    # ===== TOOLS =====
    for i,t in enumerate(TOOLS):
        x = 5 + i*58
        rect = pygame.Rect(x,5,54,20)

        hover = rect.collidepoint(mx,my)
        col = (140,140,240) if tool==t else (110,110,110)
        if hover:
            col = (180,180,255)

        pygame.draw.rect(screen, col, rect, border_radius=3)
        screen.blit(font_small.render(t[:4],True,(255,255,255)),(x+5,7))

        if hover:
            hover_tool = t

    # ===== BRUSH SLIDER =====
    slider_x = len(TOOLS)*58 + 10
    pygame.draw.rect(screen,(80,80,80),(slider_x,10,120,10),border_radius=5)

    max_b = len(BSIZES)-1
    knob_x = slider_x + int((bi/max_b)*120)
    pygame.draw.circle(screen,(255,255,255),(knob_x,15),6)

    # ===== COLORS =====
    for i,c in enumerate(COLORS):
        x = W - (len(COLORS)-i)*24 - 5
        rect = pygame.Rect(x,5,20,38)

        hover = rect.collidepoint(mx,my)
        if hover:
            pygame.draw.rect(screen,(255,255,255),rect,2)

        pygame.draw.rect(screen,c,rect)
        if c==color:
            pygame.draw.rect(screen,(255,255,255),rect,2)

# ================= MAIN =================
running = True

while running:
    for e in pygame.event.get():

        if e.type == pygame.QUIT:
            running = False

        # ================= KEY =================
        elif e.type == pygame.KEYDOWN:

            if ta:
                if e.key == pygame.K_RETURN:
                    canvas.blit(font.render(tb,True,color),tp)
                    ta=False; tb=""
                elif e.key == pygame.K_BACKSPACE:
                    tb = tb[:-1]
                elif e.unicode:
                    tb += e.unicode
                continue

            if e.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                undo()

            if e.key == pygame.K_y and pygame.key.get_mods() & pygame.KMOD_CTRL:
                redo()

            if e.key == pygame.K_m:
                show_picker = not show_picker

            for k,t in [
                (pygame.K_p,"pencil"),
                (pygame.K_l,"line"),
                (pygame.K_r,"rect"),
                (pygame.K_c,"circle"),
                (pygame.K_e,"eraser"),
                (pygame.K_f,"fill"),
                (pygame.K_t,"text")
            ]:
                if e.key == k:
                    tool = t

        # ================= MOUSE =================
        elif e.type == pygame.MOUSEBUTTONDOWN:

            mx,my = e.pos

            # ===== EYEDROPPER (RIGHT CLICK) =====
            if e.button == 3 and on_cv(e.pos):
                color = canvas.get_at(cp(e.pos))[:3]

            # ===== SLIDER =====
            if my < TH:
                slider_x = len(TOOLS)*58 + 10
                if slider_x <= mx <= slider_x+120 and 10 <= my <= 25:
                    bi = int(((mx-slider_x)/120)*len(BSIZES))
                    bi = max(0,min(bi,len(BSIZES)-1))

            # ===== TOOL / COLOR =====
            if my < TH:

                for i,t in enumerate(TOOLS):
                    x = 5 + i*58
                    if x <= mx <= x+54 and 5 <= my <= 25:
                        tool = t

                for i,c in enumerate(COLORS):
                    x = W - (len(COLORS)-i)*24 - 5
                    if x <= mx <= x+20 and 5 <= my <= 43:
                        color = c

                continue

            if not on_cv(e.pos):
                continue

            save_state()

            p = cp(e.pos)

            if tool == "fill":
                flood_fill(canvas,p,color)

            elif tool == "text":
                ta=True
                tp=p
                tb=""

            else:
                drawing=True
                sp=p
                lp=p

        elif e.type == pygame.MOUSEBUTTONUP:
            if drawing and on_cv(e.pos):
                draw_shape(canvas,tool,sp,cp(e.pos),color,BSIZES[bi])
            drawing=False
            preview_pos=None

        elif e.type == pygame.MOUSEMOTION:
            if drawing and on_cv(e.pos):
                p = cp(e.pos)

                if tool == "pencil":
                    pygame.draw.line(canvas,color,lp,p,BSIZES[bi])
                    lp=p

                elif tool == "eraser":
                    pygame.draw.line(canvas,(255,255,255),lp,p,BSIZES[bi]*3)
                    lp=p

                else:
                    preview_pos=p

    # ================= RENDER =================
    screen.fill((0,0,0))

    if drawing and preview_pos and tool not in ("pencil","eraser"):
        temp = canvas.copy()
        draw_shape(temp,tool,sp,preview_pos,color,BSIZES[bi])
        screen.blit(temp,(0,TH))
    else:
        screen.blit(canvas,(0,TH))

    if ta:
        screen.blit(font.render(tb+"|",True,color),(tp[0],tp[1]+TH))

    toolbar()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()