import pygame, math
pygame.init()


### SETUP

# Supports: 1, 2, 3
n_circles = 3

to_label = [ # Set to True if you want the circle to be labelled
  ["c1", True],
  ["c2", True],
  ["c3", False],
  ["c1c2", False],
  ["c1c3", False],
  ["c2c3", False],
  ["c1c2c3", True],
] 

# Set the text to be displayed by the key, set to None for no text
key_label = " = selected area"

# Size of the window
WIN_WIDTH = 1600
WIN_HEIGHT = 1600

# Choose between 'sharp' and 'fast' - sharp will run fast unless using a high screen resolution ~1440p or 2160p onwards
draw_mode = 'sharp'


### END SETUP





win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT)   )
clock = pygame.time.Clock()

def dist(p1:tuple, p2:tuple):
  x = (p1[0] - p2[0])**2
  y = (p1[1] - p2[1])**2
  return math.sqrt(x+y)

class VennDiagram:
  def __init__(self, sets=2, fill_states=None, label=True, key_text=None) -> None:
    if sets < 1 or sets > 3 :
      raise ValueError("Please enter a number of sets between 1 and 3")
    if WIN_HEIGHT >= WIN_WIDTH:
      self.circleradius = 0.2*WIN_WIDTH
    else:
      self.circleradius = 0.2*WIN_HEIGHT
    self.key_text = key_text
    if draw_mode == 'fast':
      self.drawpixelsize = 8
      self.circle_width_size = int(2.5*self.drawpixelsize)
    else:
      self.drawpixelsize = 4
      self.circle_width_size = int(2.5*self.drawpixelsize)
    self.circle_radius_extra = 5
    self.circles_count = sets
    self.nothing_rect_border = pygame.Rect(50, 50, WIN_WIDTH-100, WIN_HEIGHT-100)
    self.nothing_rect = pygame.Rect(75, 75, WIN_WIDTH-150, WIN_HEIGHT-150)
    if fill_states != None:
      self.fillstates = fill_states
    else:
      self.fillstates = {
        "c1":False,
        "c2":False,
        "c3":False,
        "c1c2":False,
        "c1c3":False,
        "c2c3":False,
        "c1c2c3":False,
        "rect":False
      }
      self.truecolour = (0, 255, 0)
    self.falsecolour = (255, 255, 255)
    
    self.c2pos = None
    self.c3pos = None
    if self.circles_count == 1:
      self.c1pos = (WIN_WIDTH / 2, WIN_HEIGHT/2)
    if self.circles_count == 2:
      self.c1pos = (WIN_WIDTH / 2 - 0.5*self.circleradius, WIN_HEIGHT / 2)
      self.c2pos = (WIN_WIDTH / 2 + 0.5*self.circleradius, WIN_HEIGHT / 2)
    if self.circles_count == 3:
      offset = 40
      theta = 60 / (2 * math.pi / 360)
      self.c1pos = (WIN_WIDTH/2 - self.circleradius * math.cos(theta), WIN_HEIGHT/2 - self.circleradius * math.sin(theta) + offset)
      self.c2pos = (WIN_WIDTH/2 + self.circleradius * math.cos(theta), WIN_HEIGHT/2 - self.circleradius * math.sin(theta) + offset)
      self.c3pos = (WIN_WIDTH/2, WIN_HEIGHT/2 + self.circleradius/2 + offset)

    self.fonts = {
      "big":pygame.font.Font("NotoSansMath-Regular.ttf", 48),
      "small":pygame.font.Font("NotoSansMath-Regular.ttf", 30)
    }
    
    if self.circles_count == 1:
      self.textpos = {
        "c1":self.c1pos,
        "c2":None,
        "c3":None,
        "c1c2":None,
        "c1c3":None,
        "c2c3":None,
        "c1c2c3":None
      }
    elif self.circles_count == 2:
      self.textpos = {
        "c1":(self.c1pos[0] - self.circleradius*0.25, self.c1pos[1]),
        "c2":(self.c2pos[0] + self.circleradius*0.25, self.c2pos[1]),
        "c3":None,
        "c1c2":( (self.c1pos[0]+self.c2pos[0])/2, (self.c1pos[1]+self.c2pos[1])/2),
        "c1c3":None,
        "c2c3":None,
        "c1c2c3":None
      }
    elif self.circles_count == 3:
      self.textpos = {
        "c1":self.c1pos,
        "c2":self.c2pos,
        "c3":self.c3pos,
        "c1c2":( (self.c1pos[0]+self.c2pos[0])/2, (self.c1pos[1]+self.c2pos[1])/2),
        "c1c3":( (self.c1pos[0]+self.c3pos[0])/2, (self.c1pos[1]+self.c3pos[1])/2),
        "c2c3":( (self.c2pos[0]+self.c3pos[0])/2, (self.c2pos[1]+self.c3pos[1])/2),
        "c1c2c3":(WIN_WIDTH / 2, WIN_HEIGHT / 2 - 55  )
      }
    self.text_display = {
      "c1":"A",
      "c2":"B",
      "c3":"C",
      "c1c2":"A∩B",
      "c1c3":"A∩C",
      "c2c3":"B∩C",
      "c1c2c3":"A∩B∩C"
    }
    
    self.labels = label
    if self.labels != None and self.labels != False and type(self.labels) != list:
      if self.labels == True:
        if self.circles_count == 1:
          self.labels = ["c1"]
      if self.circles_count == 2:
        self.labels = ["c1", "c2", "c1c2"]
      if self.circles_count == 3:
        self.labels = ["c1", "c2", "c3", "c1c2", "c1c3", "c2c3", "c1c2c3"]
    
  def handle_input(self, mpos) -> None:
    

    r_c1 = dist(mpos, self.c1pos) < self.circleradius
    r_c2 = None 
    r_c3 = None

    if self.circles_count >= 2:
      r_c2 = dist(mpos, self.c2pos) < self.circleradius
    if self.circles_count == 3:
      r_c3 = dist(mpos, self.c3pos) < self.circleradius

    #rect_hit = self.nothing_rect.collidepoint(mpos)
    #if rect_hit and not r_c1 and not r_c2 and not r_c3:
    #  self.fillstates["rect"] = False if self.fillstates["rect"] else True

    if self.circles_count == 1:
      if r_c1:
        self.fillstates["c1"] = False if self.fillstates["c1"] else True

    if self.circles_count == 2:
      if r_c1 and r_c2:
        self.fillstates["c1c2"] = False if self.fillstates["c1c2"] else True
      elif r_c1:
        self.fillstates["c1"] = False if self.fillstates["c1"] else True
      elif r_c2:
        self.fillstates["c2"] = False if self.fillstates["c2"] else True
    
    if self.circles_count == 3:
      if r_c1 and r_c2 and r_c3:
        self.fillstates["c1c2c3"] = False if self.fillstates["c1c2c3"] else True
      if r_c1 and r_c2 and not r_c3:
        self.fillstates["c1c2"] = False if self.fillstates["c1c2"] else True
      if r_c1 and not r_c2 and r_c3:
        self.fillstates["c1c3"] = False if self.fillstates["c1c3"] else True
      if not r_c1 and r_c2 and r_c3:
        self.fillstates["c2c3"] = False if self.fillstates["c2c3"] else True
      if r_c1 and not r_c2 and not r_c3:
        self.fillstates["c1"] = False if self.fillstates["c1"] else True
      if not r_c1 and r_c2 and not r_c3:
        self.fillstates["c2"] = False if self.fillstates["c2"] else True
      if not r_c1 and not r_c2 and r_c3:
        self.fillstates["c3"] = False if self.fillstates["c3"] else True
      #print(self.fillstates)
  def render(self, window) -> None:
    window.fill((255, 255, 255))

    pygame.draw.rect(win, (0, 0, 0), self.nothing_rect_border)
    
    if self.fillstates["rect"]:
      pygame.draw.rect(win, self.truecolour, self.nothing_rect)
    else:
      pygame.draw.rect(win, self.falsecolour, self.nothing_rect)
      
    if self.circles_count == 1:
      n1 = int(self.c1pos[0] - self.circleradius)
      n2 = int(self.c1pos[1] - self.circleradius)
      n3 = int(2*self.circleradius)
      n4 = int(2*self.circleradius)
      for px in range(n1, n1+n3, self.drawpixelsize):
        for py in range(n2, n2+n4, self.drawpixelsize):
          p_draw = dist((px, py), self.c1pos) < self.circleradius
          if self.fillstates["c1"] and p_draw:
            pygame.draw.rect(win, self.truecolour, pygame.Rect(px, py, self.drawpixelsize, self.drawpixelsize))

      
    if self.circles_count == 2:
      n1 = int(self.c1pos[0] - self.circleradius)
      n2 = int(self.c1pos[1] - self.circleradius)
      n3 = int(self.c2pos[0] - self.c1pos[0] + 2*self.circleradius)
      n4 = int(2*self.circleradius)

      for px in range(n1, n1+n3, self.drawpixelsize):
        for py in range(n2, n2+n4, self.drawpixelsize):
          r_c1 = dist((px, py), self.c1pos) < self.circleradius
          r_c2 = dist((px, py), self.c2pos) < self.circleradius
          if self.fillstates["c1c2"] and r_c1 and r_c2:
            pygame.draw.rect(win, self.truecolour, pygame.Rect(px, py, self.drawpixelsize, self.drawpixelsize))
          elif self.fillstates["c1"] and r_c1 and not r_c2:
            pygame.draw.rect(win, self.truecolour, pygame.Rect(px, py, self.drawpixelsize, self.drawpixelsize))
          elif self.fillstates["c2"] and r_c2 and not r_c1:
            pygame.draw.rect(win, self.truecolour, pygame.Rect(px, py, self.drawpixelsize, self.drawpixelsize))
        
      

    if self.circles_count == 3:
      n1 = int(self.c1pos[0] - self.circleradius)
      n2 = int(self.c1pos[1] - self.circleradius)
      n3 = int(self.c2pos[0] - self.c1pos[0] + 2*self.circleradius)
      n4 = int(self.c3pos[1] - self.c1pos[1] + 2*self.circleradius)

      for px in range(n1, n1+n3, self.drawpixelsize):
        for py in range(n2, n2+n4, self.drawpixelsize):
          r_c1 = dist((px, py), self.c1pos) < self.circleradius
          r_c2 = dist((px, py), self.c2pos) < self.circleradius
          r_c3 = dist((px, py), self.c3pos) < self.circleradius
          if not r_c1 and not r_c2 and not r_c3:
            pass
          elif r_c1 and r_c2 and r_c3 and self.fillstates["c1c2c3"]:
            pygame.draw.rect(win, self.truecolour, pygame.Rect(px, py, self.drawpixelsize, self.drawpixelsize))
          elif r_c1 and r_c2 and not r_c3 and self.fillstates["c1c2"]:
            pygame.draw.rect(win, self.truecolour, pygame.Rect(px, py, self.drawpixelsize, self.drawpixelsize))
          elif r_c1 and not r_c2 and r_c3 and self.fillstates["c1c3"]:
            pygame.draw.rect(win, self.truecolour, pygame.Rect(px, py, self.drawpixelsize, self.drawpixelsize))
          elif not r_c1 and r_c2 and r_c3 and self.fillstates["c2c3"]:
            pygame.draw.rect(win, self.truecolour, pygame.Rect(px, py, self.drawpixelsize, self.drawpixelsize))
          elif r_c1 and not r_c2 and not r_c3 and self.fillstates["c1"]:
            pygame.draw.rect(win, self.truecolour, pygame.Rect(px, py, self.drawpixelsize, self.drawpixelsize))
          elif not r_c1 and r_c2 and not r_c3 and self.fillstates["c2"]:
            pygame.draw.rect(win, self.truecolour, pygame.Rect(px, py, self.drawpixelsize, self.drawpixelsize))
          elif not r_c1 and not r_c2 and r_c3 and self.fillstates["c3"]:
            pygame.draw.rect(win, self.truecolour, pygame.Rect(px, py, self.drawpixelsize, self.drawpixelsize))
            
    if self.circles_count >= 1:
      pygame.draw.circle(win, (0, 0, 0), self.c1pos, self.circleradius+self.circle_radius_extra, width=self.circle_width_size)
    if self.circles_count >= 2:
      pygame.draw.circle(win, (0, 0, 0), self.c2pos, self.circleradius+self.circle_radius_extra, width=self.circle_width_size)
    if self.circles_count == 3:
      pygame.draw.circle(win, (0, 0, 0), self.c3pos, self.circleradius+self.circle_radius_extra, width=self.circle_width_size)
   
    
    for td in self.labels:
      if td in ["c1", "c2", "c3"]:
        f = self.fonts["big"]
      else:
        f = self.fonts["small"]
      text = f.render(self.text_display[td], True, (0, 0, 0))
      text_rect = text.get_rect(center=self.textpos[td])
      win.blit(text, text_rect)
    
    if self.key_text != None:
      key_text = self.fonts["big"].render(self.key_text, True, (0, 0, 0))
      text_pos = (300, WIN_HEIGHT-161)
      pygame.draw.rect(win, self.truecolour, pygame.Rect(100, WIN_HEIGHT-150, 200, 50))
      win.blit(key_text, text_pos)


    pygame.display.flip()





to_label_list = []
for i in to_label:
  if i[1]:
    if (i[0] in ["c3", "c1c3", "c2c3", "c1c2c3"] and n_circles == 3) or (i[0] in ["c2", "c1c2", "c1c2"] and n_circles >= 2) or (i[0] in ["c1"]):
      to_label_list.append(i[0])
  

vd = VennDiagram(n_circles, label=to_label_list, key_text=key_label) 

origin = (WIN_WIDTH / 2, WIN_HEIGHT/2)

running = True
while running:

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.MOUSEBUTTONDOWN:
      mouse_pos = pygame.mouse.get_pos()
      vd.handle_input(mouse_pos)
  
  vd.render(win)

  clock.tick(20)
