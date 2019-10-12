from typing import List, Any
import math
import pygame
import random
pygame.init()
pygame.font.init()
menufont1 = pygame.font.Font('Pokemon GB.ttf', 24)
menufont2 = pygame.font.Font('Emulogic-zrEw.ttf', 24)
menufont3 = pygame.font.Font('Emulogic-zrEw.ttf', 12)
menufont4 = pygame.font.Font('Emulogic-zrEw.ttf', 18)
actorfont = pygame.font.Font('Emulogic-zrEw.ttf', 8)

tan = (235, 215, 150)
grey = (200, 200, 200)
green = (215, 225, 150)
white = (255, 255, 255)
black = (0, 0, 0)

GAME_SIZE = 7
OFFSET = 5
MENU_COORD_X = 5
MENU_COORD_Y = GAME_SIZE * 55
MSG_TIME = 20
MSG_DISP = False
MSG_RECT = pygame.Rect(0, 0, 400, 600)
MSG = pygame.Surface((400, 600))
SET_FOR_RESTATE = 0
MAP_FINISHED = False
READY_TO_START = False
ANIMATING = -1
ANIM_COORD_1 = (0, 0)
ANIM_COORD_2 = (0, 0)
LINEAR_PARAM_X = lambda t, x1, x2: ((1 - float(t)) * x1 + (float(t) * x2))
LINEAR_PARAM_Y = lambda t, y1, y2: ((1 - float(t)) * y1 + (float(t) * y2))
ENEMY_NAMES = ["Ricardo", "Marie Gemini Marie-Damon", "The Silent Thunder", "Noah of Ark"]


colors = [tan, grey, green] #may add more colors
tiles = []
targeted = []

screen = pygame.display.set_mode((400, 600))
DAMAGE_surface = pygame.Surface(screen.get_size())
DAMAGE_surface.fill((255, 40, 20))
DAMAGE_surface = DAMAGE_surface.convert()
menu_surface = pygame.Surface((GAME_SIZE * 55, 200))
menu_surface.fill((50, 75, 125))
menu_surface = menu_surface.convert()
background = pygame.Surface(screen.get_size())
background.fill(black)
background = background.convert()
game_finished_surface = pygame.Surface(screen.get_size())
game_finished_surface.fill((150, 75, 200))
game_finished_surface.convert()
main_menu_surface = pygame.Surface(screen.get_size())
main_menu_surface.fill((50, 50, 50))
main_menu_surface.convert()

highlight_pos = 0
map_highlight_rects = [pygame.Rect(MENU_COORD_X + 5, MENU_COORD_Y + 25, 40, 40),  # FIGHT select button
                   pygame.Rect(MENU_COORD_X + 200, MENU_COORD_Y + 25, 40, 40),  # ITEM select button
                   pygame.Rect(MENU_COORD_X + 5, MENU_COORD_Y + 100, 40, 40),  # STATS select button
                   pygame.Rect(MENU_COORD_X + 200, MENU_COORD_Y + 100, 40, 40),  # MENU select button
                   pygame.Rect(MENU_COORD_X + 10, MENU_COORD_Y + 60, 40, 40),   # ATTACK 1 select button
                   pygame.Rect(MENU_COORD_X + 10, MENU_COORD_Y + 110, 40, 40),   # ATTACK 2 select button
                   pygame.Rect(MENU_COORD_X + 5, MENU_COORD_Y + 30, 40, 40), # top-left inventory space
                   pygame.Rect(MENU_COORD_X + 205, MENU_COORD_Y + 30, 40, 40), # top-right inventory space
                   pygame.Rect(MENU_COORD_X + 5, MENU_COORD_Y + 80, 40, 40), # mid-left inventory space
                   pygame.Rect(MENU_COORD_X + 205, MENU_COORD_Y + 80, 40, 40), # mid-right inventory space
                   pygame.Rect(MENU_COORD_X + 5, MENU_COORD_Y + 130, 40, 40), # bot-left inventory space
                   pygame.Rect(MENU_COORD_X + 205, MENU_COORD_Y + 130, 40, 40), # bot-right inventory space
                   pygame.Rect(MENU_COORD_X + 75, MENU_COORD_Y - 45, 40, 40),  #  "Use_Or_Throw" Use selection
                   pygame.Rect(MENU_COORD_X + 200, MENU_COORD_Y - 45, 40, 40), # _ "Use_Or_Throw" Throw selection
                   pygame.Rect(MENU_COORD_X - 10, MENU_COORD_Y + 90, 40, 40),  #  |
                   pygame.Rect(MENU_COORD_X + 65, MENU_COORD_Y + 90, 40, 40),  #  |
                   pygame.Rect(MENU_COORD_X + 135, MENU_COORD_Y + 90, 40, 40), #  | These 5 are for leveling up
                   pygame.Rect(MENU_COORD_X + 210, MENU_COORD_Y + 90, 40, 40), #  |
                   pygame.Rect(MENU_COORD_X + 280, MENU_COORD_Y + 90, 40, 40), # _|
                   pygame.Rect(25, 130, 40, 40), # These 3 are for post-map menu choices
                   pygame.Rect(25, 180, 40, 40),
                   pygame.Rect(25, 230, 40, 40)
                   ]



# highlight positions are as follows:
# 0 = nothing
# 1 = "Fight"
# 2 = "Pack"
# 3 = "Stats"
# 4 = "Menu"
# 5 = "Move 1"
# 6 = "Move 2"
# 7 = aim mode -- no highlights
# 8 = level up mode -- menu change and skill point prompt




screen.blit(background, (0, 0))
potion_img = pygame.image.load("potion_graphic.png")
bomb_img = pygame.image.load("bomb_graphic.png")
bomb_mini_img = pygame.image.load("bomb_graphic_mini.png")
tgt_icon = pygame.image.load("tgt_icon.png")
aim_highlight = pygame.image.load("Target-Overlay.png")
highlight_arrow = pygame.image.load("menu_highlight.png")
level_up_overlay = pygame.image.load("level_up_overlay.png")
grass_tile = pygame.image.load("grassland-tile.png")
desert_tile = pygame.image.load("desert-tile.png")
ocean_tile = pygame.image.load("ocean-tile.png")
mountain_tile = pygame.image.load("mountain-tile.png")
forest_tile = pygame.image.load("forest-tile.png")
blaze_overlay = pygame.image.load("blaze_overlay.png")
weighted_tile_types = [blaze_overlay, ocean_tile, grass_tile, forest_tile, mountain_tile, desert_tile]
throwable_imgs = [bomb_mini_img]


class Move:
    def __init__(self, actor, name, target, desc, range):
        self.actor = actor
        self.name = name
        self.target = target
        self.desc = desc
        self.range = range

    def execute(self):
        global MSG_DISP
        global MSG_TIME
        global MSG_RECT
        global MSG
        self.target.hitpoints = self.target.hitpoints + self.desc
        if self.target.hitpoints <= 0:
            print("Defeated enemy: + " + str(self.target.xp_on_death) + " xp")
            self.actor.add_xp(self.target.xp_on_death)
            print("Current Player xp: " + str(self.actor.curr_xp) + " / " + str(self.actor.next_lvl_xp))
        self.target = NULL_TGT
        #self.target.msg = str(self.desc) + " hp"


class Tile:
    def __init__(self, occupied, terr_type, rect, tx, ty):
        self.occupied = occupied
        self.terrain = terr_type
        self.seed_val = 0
        self.aimed_at = False
        self.rect = rect
        self.tx = tx
        self.ty = ty


    def change_occ(self):
        self.occupied = not self.occupied

    def set_occ(self, bool):
        self.occupied = bool

    def set_terr(self, seed_val):
        self.seed_val = seed_val
        self.terrain = weighted_tile_types[seed_val]

    def aim_at(self):
        self.aimed_at = True

    def dist_to(self, other_tile):
        otx = other_tile.tx
        oty = other_tile.ty
        dist = math.sqrt((otx - self.tx)**2 + (oty - self.ty)**2)
        return dist


class Item:
    def __init__(self, id, ix, iy, owner, desc):
        self.id = id
        self.ix = ix
        self.iy = iy
        self.owner = owner
        self.desc = desc

    def item_lookup(self):
        item_dict = {"Potion": add_health(25),
                     "HI Potion": add_health(50),
                     "Bomb": explode(50),
                     "Big Bomb": explode(100)}
        return item_dict.get(self.id, lambda: 'Invalid')

    def use_item(self):
        fn = self.item_lookup()
        fn(self.owner)


class Fake_Tile(Tile):
    def __init__(self, tx, ty):
        self.tx = tx
        self.ty = ty
        super().__init__(False, weighted_tile_types[0], pygame.Rect(tx, ty, 50, 50), tx, ty)


class Actor:
    def __init__(self, px, py, hp, max_hp, move_list, name, level, xp_on_death, item_list):
        self.x_pos = px
        self.y_pos = py
        self.state = 0
        self.locked = False
        self.hitpoints = hp
        self.max_hp = max_hp
        self.curr_xp = 0
        self.next_lvl_xp = 25
        self.level = level
        self.Strength = 5
        self.Defense = 5
        self.Agility = 5
        self.Dexterity = 5
        self.Luck = 5
        self.move_list = move_list
        self.msg = ""
        self.name = name
        self.alive = True
        self.xp_on_death = xp_on_death
        self.item_list = item_list
        self.throw_aim = Fake_Tile(px, py)
        self.item_sel = Item("none", self.x_pos, self.y_pos, self, "null")



    def move_actor(self, direction):
        global GAME_SIZE
        global LEVEL_MAP
        py = self.y_pos
        px = self.x_pos
        sx = LEVEL_MAP.scr_x
        sy = LEVEL_MAP.scr_y
        terrain = LEVEL_MAP.curr_screen.tile_map
        if not self.locked:
            if direction == 8:
                if (py - 1) >= 0 and check_tile_okay(terrain, px, py - 1):
                    old_tile = terrain[py][px]
                    old_tile.occupied = False
                    tile = terrain[py-1][px]
                    tile.occupied = True
                    self.y_pos = self.y_pos - 1
                elif (py - 1) < 0 and (LEVEL_MAP.scr_y >= 1):
                    print("\n-----------------\nDETECTING AN UP TRANSITION\n--------------------\n")
                    old_tile = terrain[py][px]
                    old_tile.occupied = False
                    old_terr = LEVEL_MAP.curr_screen
                    LEVEL_MAP.change_screen(self, sx, sy - 1)
                    terrain = LEVEL_MAP.curr_screen.tile_map
                    tile = terrain[GAME_SIZE - 1][px]
                    tile.occupied = True
                    self.y_pos = GAME_SIZE - 1
            elif direction == 2:
                if (py + 1) < GAME_SIZE and check_tile_okay(terrain, px, py + 1):
                    old_tile = terrain[py][px]
                    old_tile.occupied = False
                    tile = terrain[py+1][px]
                    tile.occupied = True
                    self.y_pos = self.y_pos + 1
                elif (py + 1) >= GAME_SIZE and (sy < LEVEL_MAP.map_height - 1):
                    print("\n-----------------\nDETECTING A DOWN TRANSITION\n--------------------\n")
                    old_tile = terrain[py][px]
                    old_tile.occupied = False
                    old_terr = LEVEL_MAP.curr_screen
                    LEVEL_MAP.change_screen(self, sx, sy + 1)
                    terrain = LEVEL_MAP.curr_screen.tile_map
                    tile = terrain[0][px]
                    tile.occupied = True
                    self.y_pos = 0
            elif direction == 4:
                if (px - 1) >= 0 and check_tile_okay(terrain, px - 1, py):
                    old_tile = terrain[py][px]
                    old_tile.occupied = False
                    tile = terrain[py][px - 1]
                    tile.occupied = True
                    self.x_pos = self.x_pos - 1
                elif (px - 1) < 0 and (sx > 0):
                    print("We're correctly detecting a left screen transition")
                    old_tile = terrain[py][px]
                    old_tile.occupied = False
                    old_terr = LEVEL_MAP.curr_screen
                    LEVEL_MAP.change_screen(self, sx - 1, sy)
                    terrain = LEVEL_MAP.curr_screen.tile_map
                    tile = terrain[py][GAME_SIZE - 1]
                    tile.occupied = True
                    self.x_pos = GAME_SIZE - 1
            elif direction == 6:
                if (px + 1) < GAME_SIZE and check_tile_okay(terrain, px + 1, py):
                    old_tile = terrain[py][px]
                    old_tile.occupied = False
                    tile = terrain[py][px + 1]
                    tile.occupied = True
                    self.x_pos = self.x_pos + 1
                elif (px + 1) >= GAME_SIZE and (sx < LEVEL_MAP.map_width - 1):
                    print("We're correctly detecting a right screen transition")
                    old_tile = terrain[py][px]
                    old_tile.occupied = False
                    old_terr = LEVEL_MAP.curr_screen
                    LEVEL_MAP.change_screen(self, sx + 1, sy)
                    terrain = LEVEL_MAP.curr_screen.tile_map
                    tile = terrain[py][0]
                    tile.occupied = True
                    self.x_pos = 0
            elif direction == 1:
                if (px - 1) >= 0 and (py + 1) < GAME_SIZE and check_tile_okay(terrain, px - 1, py + 1):
                    old_tile = terrain[py][px]
                    old_tile.occupied = False
                    tile = terrain[py + 1][px - 1]
                    tile.occupied = True
                    self.x_pos = self.x_pos - 1
                    self.y_pos = self.y_pos + 1
            elif direction == 3:
                if (px + 1) < GAME_SIZE and (py + 1) < GAME_SIZE and check_tile_okay(terrain, px + 1, py + 1):
                    old_tile = terrain[py][px]
                    old_tile.occupied = False
                    tile = terrain[py + 1][px + 1]
                    tile.occupied = True
                    self.x_pos = self.x_pos + 1
                    self.y_pos = self.y_pos + 1
            elif direction == 7:
                if (px - 1) >= 0 and (py - 1) >= 0 and check_tile_okay(terrain, px - 1, py - 1):
                    old_tile = terrain[py][px]
                    old_tile.occupied = False
                    tile = terrain[py - 1][px - 1]
                    tile.occupied = True
                    self.x_pos = self.x_pos - 1
                    self.y_pos = self.y_pos - 1
            elif direction == 9:
                if (px + 1) < GAME_SIZE and (py - 1) >= 0 and check_tile_okay(terrain, px + 1, py - 1):
                    old_tile = terrain[py][px]
                    old_tile.occupied = False
                    new_tile = terrain[py - 1][px + 1]
                    new_tile.occupied = True
                    self.x_pos = self.x_pos + 1
                    self.y_pos = self.y_pos - 1

    def move_to(self, tile):
        terrain = LEVEL_MAP.curr_screen.tile_map
        old_tile = terrain[self.y_pos][self.x_pos]
        old_tile.occupied = False
        self.x_pos = tile.tx
        self.y_pos = tile.ty
        tile.occupied = True

    def target(self):
        global MSG_TIME
        global MSG_DISP
        if not (self in targeted):
            targeted.append(self)

    def throw_item(self, itm_sel, target):
        if itm_sel.id == "none":
            print("Invalid thrown item")
        else:
            range = self.Strength
            dist = math.sqrt((target.x_pos - self.x_pos)**2 + (target.y_pos - self.y_pos)**2)
            if range >= dist:
                i = itm_sel
                i.owner = target
                i.ix = target.x_pos
                i.iy = target.y_pos
                i.use_item()
            if target.hitpoints <= 0:
                for e in targeted:
                    if e.hitpoints <= 0:
                        print("Defeated enemy: + " + str(target.xp_on_death) + " xp")
                        self.add_xp(target.xp_on_death)
                        print("Current Player xp: " + str(self.curr_xp) + " / " + str(self.next_lvl_xp))


    def add_xp(self, xp):
        print("Old XP: " + str(self.curr_xp))
        self.curr_xp = self.curr_xp + xp
        print("New XP: " + str(self.curr_xp))
        print("XP needed for Level: " + str(self.next_lvl_xp))
        # Right now, level will just go up and points will loop over
        if self.curr_xp >= self.next_lvl_xp:
            print("Hit the level cap!")
            self.curr_xp = self.curr_xp % self.next_lvl_xp
            print("Xp after levelling up: " + str(self.curr_xp))
            if isinstance(self, Player):
                print("Hey, this noticed that you're the player!")
                self.level_up()


    def print_stats(self, up_code):
        strgth = "Strength: " + str(self.Strength)
        aglty = "Agility: " + str(self.Agility)
        dex = "Dexterity: " + str(self.Dexterity)
        luck = "Luck: " + str(self.Luck)
        if up_code == 0:
            strgth = strgth + "  +1"
        elif up_code == 1:
            aglty = aglty + "  +1"
        elif up_code == 2:
            dex = dex + "  +1"
        elif up_code == 3:
            luck = luck + "  +1"
        print(strgth)
        print(aglty)
        print(dex)
        print(luck)


NULL_TGT = Actor(-1, -1, 0, 100, [], "none", 0, 0, [])


class Player(Actor):
    def __init__(self, px, py, inv_disp_start):
        self.image = pygame.image.load("Player1-Overlay_small.png")
        self.locked = False
        self.aiming = False
        self.inv_disp_start = inv_disp_start
        # Stats for Player
        self.perks = []
        rifle_move = Move(self, "Rifle (3 spc)", NULL_TGT, -10, 3)
        knife_move = Move(self, "Knife (1 spc)", NULL_TGT, -15, 1)
        potion_item = Item("Potion", px, py, self, "Heals target for 25 HP")
        bomb_item = Item("Bomb", px, py, self, "Throwable. Damaged Surrounding 8 tiles for 50 HP")
        item_list = [potion_item, bomb_item]
        move_list = [rifle_move, knife_move]
        self.move_choice = 0
        self.leveling = False
        super().__init__(px, py, 100, 100, move_list, "Player", 1, 100, item_list)

    def move_player(self, direction):
        self.move_actor(direction)


    def level_up(self):
        global MSG
        global MSG_RECT
        global MSG_DISP
        global MSG_TIME
        global SET_FOR_RESTATE
        global highlight_pos
        self.state = 8
        self.leveling = True
        highlight_pos = 15
        self.level = self.level + 1
        level_up_screen(self)

    def attr_up(self, attr_code):
        code = attr_code
        if code == 0:
            self.Strength = self.Strength + 1
        elif code == 1:
            self.Defense = self.Defense + 1
        elif code == 2:
            self.Agility = self.Agility + 1
        elif code == 3:
            self.Dexterity = self.Dexterity + 1
        elif code == 4:
            self.Luck = self.Luck + 1
        else:
            print("wrong attribute code")


NULL_PLAYER = Player(-1, -1, 0)
CONTINUING_PLAYER = NULL_PLAYER


class Enemy(Actor):
    def __init__(self, type, ex, ey, name, screen):
        enemy_imgs = [pygame.image.load("ricardo_overlay.png"),
                      pygame.image.load("MGM-D_overlay.png"),
                      pygame.image.load("Player2-Overlay_small.png")]
        self.type = type
        self.image = enemy_imgs[self.type]
        knife_move = Move(self, "Knife (1 spc)", NULL_TGT, -15, 1)
        move_list = [knife_move]
        self.path = []
        self.visited_tiles_check = []
        self.which_screen = screen
        terrain = self.which_screen.tile_map
        self.last_seen_player = terrain[NULL_TGT.y_pos][NULL_TGT.x_pos]
        super().__init__(ex, ey, 25, 25, move_list, name, 1, 15, [])


class MapScreen:
    def __init__(self, tile_map, index, enemies):
        self.tile_map = tile_map
        self.index = index
        self.enemies = enemies

    def display_screen(self, player):
        global GAME_SIZE
        self.fix_seeded_tiles()
        draw_grid(self.tile_map, GAME_SIZE, player, self.enemies)

    def fix_seeded_tiles(self):
        for r in self.tile_map:
            for c in r:
                # print("seed val: " + str(c.seed_val))
                c.set_terr(c.seed_val % len(weighted_tile_types))

    def init_enemies(self):
        for i in self.tile_map:
            for j in i:
                for e in self.enemies:
                    if e.x_pos == j.tx and e.y_pos == j.ty:
                        j.set_occ(True)
                        continue

    def wipe_screen(self):
        for r in self.tile_map:
            for c in r:
                c.set_occ(False)

    def init_scr_enemies(self, num_enemies=3, enemytypes=[0, 0, 0]):
        global GAME_SIZE
        for i in range(num_enemies):
            ex = random.randint(0, GAME_SIZE)
            ey = random.randint(0, GAME_SIZE)
            while not check_tile_okay(self.tile_map, ey, ex):
                ex = random.randint(0, GAME_SIZE)
                ey = random.randint(0, GAME_SIZE)
            etile = self.tile_map[ey][ex]
            etile.set_occ(True)
            self.enemies.append(Enemy(enemytypes[i], ex, ey, 'Test', self))

    def output_tiles(self, output_str):
        out_str = ""
        print("length of this screen's tile map (rows): " + str(len(self.tile_map)) + " (cols): " + str(len([row for row in self.tile_map])))
        for row in self.tile_map:
            for tile in row:
                out_str = out_str + str(tile.seed_val) + "  "
            out_str = out_str + "\n" + ("--" * len(self.tile_map) * 2) + "\n"
        output_str.write(out_str)



class Map:
    def __init__(self, screens=[], map_width=3, map_height=3, state=0):
        self.map_width = map_width
        self.map_height = map_height
        self.scr_x = 0
        self.scr_y = 0
        self.state = state
        if len(screens) == 0:
            self.screens = self.init_map()
            self.curr_screen = self.screens[self.scr_y][self.scr_x]

        else:
            self.screens = screens
            self.curr_screen = self.screens[self.scr_y][self.scr_x]

    #
    # def __init__(self):
    #     self.map_width = 3
    #     self.map_height = 3
    #     self.scr_x = 0
    #     self.scr_y = 0
    #     self.screens = self.init_map()
    #     self.state = 0
    #     self.curr_screen = self.screens[self.scr_y][self.scr_x]

    def display_screen(self, player, elist):
        self.curr_screen.display_screen(player)

    def change_screen(self, player, new_sx, new_sy):
        self.curr_screen.wipe_screen()
        self.scr_x = new_sx
        self.scr_y = new_sy
        new_screen = self.screens[new_sy][new_sx]
        new_screen.wipe_screen()
        new_screen.init_enemies()
        new_screen.display_screen(player)
        # pygame.display.update()
        self.curr_screen = new_screen
        return new_screen

    def height(self): return self.map_height
    def width(self): return self.map_width


    def init_map(self):
        global GAME_SIZE
        map_screens = []

        rand_map_row = random.randint(0, 3)
        rand_map_col = random.randint(0, 3)

        for h in range(self.map_height):
            screen_row = []
            for w in range(self.map_width):
                scr_tiles = []
                rand_scr_row = random.randint(0, 100) % GAME_SIZE
                rand_scr_col = random.randint(0, 100) % GAME_SIZE
                #### THIS IS WHERE THE TERRAIN GETS SET ####

                for y in range(GAME_SIZE):
                    new_row = []
                    for x in range(GAME_SIZE):
                        new_row.append(Tile(False, weighted_tile_types[0], pygame.Rect(x * 50, y * 50, 50, 50), x, y))
                    scr_tiles.append(new_row)

                new_screen = MapScreen(scr_tiles, ((h * self.map_width) + w), [])
                new_screen.tile_map = plant_seed(rand_scr_col, rand_scr_row, random.randint(1, 5), new_screen)
                new_screen.tile_map = fix_null_tiles(new_screen.tile_map)
                new_screen.init_scr_enemies()
                new_screen.wipe_screen()
                screen_row.append(new_screen)
            map_screens.append(screen_row)

        return map_screens

    def output_map_to_file(self, filename="output.txt"):
        output = open("output.txt", "w")
        for row in self.screens:
            for scr in row:
                scr.output_tiles(output)
                output.write("\n\n")
        output.close()


def plant_seed(tile_x, tile_y, seed_val, screen):
    screen_map = screen.tile_map
    tile = screen_map[tile_x][tile_y]
    tile.seed_val = seed_val
    grown_map = grow_seed(tile_x + 1, tile_y, tile, 0, screen_map)
    grown_map = fix_null_tiles(grown_map)
    return grown_map

def grow_seed(curr_x, curr_y, seed_tile, level, tile_map):
    # This is the function for calculating the current tile type and progressing forward.
    if level == 0:
        grow_seed(curr_x + 1, curr_y, seed_tile, level + 1, tile_map)
        grow_seed(curr_x - 1, curr_y, seed_tile, level + 1, tile_map)
        grow_seed(curr_x, curr_y + 1, seed_tile, level + 1, tile_map)
        grow_seed(curr_x, curr_y - 1, seed_tile, level + 1, tile_map)
        return tile_map
    else:
        if 0 < curr_x < GAME_SIZE and 0 < curr_y < GAME_SIZE:
            current_tile = tile_map[curr_y][curr_x]
        else:
            return tile_map
        if current_tile.seed_val % len(weighted_tile_types) == 0:
            floor_dist = math.ceil(seed_tile.dist_to(current_tile))
            avg = get_surrounding_avgs(current_tile, tile_map)
            seed_value = math.ceil(((floor_dist**2) + avg) / level)
            # print("Here is the calculated seed value for tile at: " + str(current_tile.tx) + ", " + str(current_tile.ty) + ": " + str(seed_value))
            current_tile.seed_val = seed_value
            # print("Level: " + str(level) + "\tSeedValue: " + str(current_tile.seed_val))
        if level < GAME_SIZE + 3:
            if curr_x > 0:
                grow_seed(curr_x - 1, curr_y, seed_tile, level + 1, tile_map)
            if curr_x < GAME_SIZE - 1:
                grow_seed(curr_x + 1, curr_y, seed_tile, level + 1, tile_map)
            if curr_y < GAME_SIZE - 1:
                grow_seed(curr_x, curr_y + 1, seed_tile, level + 1, tile_map)
            if curr_y > 0:
                grow_seed(curr_x, curr_y - 1, seed_tile, level + 1, tile_map)
        return tile_map

def fix_null_tiles(tile_map):
    fixed_map = tile_map
    for row in fixed_map:
        for tile in row:
            if tile.seed_val % len(weighted_tile_types) == 0:
                # print("This is the seed value of this type! Seed_val: " + str(tile.seed_val))
                avg = get_surrounding_avgs(tile, tile_map)
                if 1 < avg < len(weighted_tile_types):
                    tile.seed_val = int(avg + random.randint(-1, 1))
                elif avg < len(weighted_tile_types):
                    tile.seed_val = int(avg + random.randint(0, 1))
                elif avg > 1:
                    tile.seed_val = int(avg + random.randint(-1, 0))
    return fixed_map

def get_surrounding_avgs(current_tile, tile_map):
    # This will get the average index score for terrain distribution
    total = 0
    count = 0
    tx = current_tile.tx
    ty = current_tile.ty

    if tx < GAME_SIZE - 1:
        sv = tile_map[ty][tx + 1].seed_val
        if sv != 0:
            total = total + sv
            count = count + 1
    if tx > 0:
        sv = tile_map[ty][tx - 1].seed_val
        if sv != 0:
            total = total + sv
            count = count + 1
    if ty < GAME_SIZE - 1:
        sv = tile_map[ty + 1][tx].seed_val
        if sv != 0:
            total = total + sv
            count = count + 1
    if ty > 0:
        sv = tile_map[ty - 1][tx].seed_val
        if sv != 0:
            total = total + sv
            count = count + 1
    if count == 0:
        return 0
    else:
        return total / count


def check_tile_okay(tiles_list, row, col):
    global GAME_SIZE
    if not (0 <= row < GAME_SIZE) or not (0 <= col < GAME_SIZE):
        return False
    else:
        ind = (GAME_SIZE * row) + col
        # print("calculated index: " + str(ind))
        t = tiles_list[row][col]
        if t.terrain == ocean_tile or t.terrain == mountain_tile:
            # print("the tile being checked is impassable")
            return False
        elif t.occupied:
            # print("the tiles is currently occupied")
            return False
        else:
            # print("the tile being checked is free!")
            return True





# def __init__(self, screens, map_width, map_height, state):

LEVEL_MAP = Map([], 3, 3, 0)


def add_health(pts):
    def heal_target(target):
        target.hitpoints = target.hitpoints + pts
    return heal_target


def sub_health(pts):
    def hurt_target(target):
        target.hitpoints = target.hitpoints - pts
    return hurt_target


def explode(pts):
    def hurt_targets(target):
        for t in targeted:
            sub_health(pts)(t)
    return hurt_targets


def clear_aim():
    global MSG_DISP
    terrain = LEVEL_MAP.curr_screen.tile_map
    for row in terrain:
        for tile in row:
            tile.aimed_at = False
    for t in targeted:
        t.msg = ""
        targeted.remove(t)
    MSG_DISP = False


def draw_menu(player):
    menu_box = pygame.Rect((MENU_COORD_X, MENU_COORD_Y, 50, 100))
    screen.blit(menu_surface, menu_box)
    if player.state == 0:
        main_display(player)
    elif player.state == 1:
        menu_display()
    elif player.state == 2:
        attacks_screen(player)
    elif player.state == 3:
        move_screen(player)
    elif player.state == 4:
        stats_screen(player)
    elif player.state == 5:
        player.inv_disp_start = 0
        inventory_screen(player)
    elif player.state == 6:
        item_desc_screen(player)
        use_or_toss_poll(player)
    elif player.state == 7:
        item_desc_screen(player)
    elif player.state == 8:
        level_up_screen(player)


def draw_interim(map_state, player):
    global game_finished_surface
    interim_rect = game_finished_surface.get_rect()
    screen.blit(game_finished_surface, interim_rect)
    # print("map state rn = " + str(map_state))
    if map_state == 0:
        # lost the fight
        print("displaying, but lost the fight")
        map_finished_screen(player)
    elif map_state == 1:
        # won the level
        map_finished_screen(player)
    elif map_state < 0:
        print("The player quit! what are we still doing???")


def draw_main_menu(menu_selection):
    global main_menu_surface
    main_rect = main_menu_surface.get_rect()
    screen.blit(main_menu_surface, main_rect)
    main_menu_screen(menu_selection)

def get_index(row, col):
    global GAME_SIZE
    return (GAME_SIZE * row) + col


# States reference
# state = 0: default state, free movement
# state = 1: pause screen, menu selection, locked movement
# state = 2: FIGHT screen: player move selection screen, locked movement
# state = 3: aiming state, no menu selection, aiming movement
# state = 4: STATS screen: viewing stats screen
# state = 5: PACK screen: inventory menu and selection. Using Selection 1 - 4
# state = 6: use or throw poll
# state = 7: throwing aim state, no menu selection, free aiming movement
# state = 8: leveling up screen


# this draws an image at some frame/time on the screen following two parametric functions for x and y
# it returns an integer: if -1, done animating; if >= 0, then used to continue animation
def animate(img_code, param_func_x, param_func_y, current_frame, t1, t2):
    global throwable_imgs
    terrain = LEVEL_MAP.screens[LEVEL_MAP.curr_screen]
    afterfx = True
    img = throwable_imgs[img_code]
    t = t1 + (float(current_frame) / 100)
    if t <= t2:
        img_x = param_func_x(t, ANIM_COORD_1[0], ANIM_COORD_2[0])
        img_y = param_func_y(t, ANIM_COORD_1[1], ANIM_COORD_2[1])
        img_rect = pygame.Rect(img_x * 55, img_y * 55, img.get_width(), img.get_height())
        screen.blit(img, img_rect)
        current_frame = current_frame + 1
        return current_frame
    elif afterfx:
        if t <= (t2 + 2.0):
            tile = terrain[math.floor(param_func_x(t2, ANIM_COORD_1[0], ANIM_COORD_2[0]))][math.floor(param_func_y(t2, ANIM_COORD_1[1], ANIM_COORD_2[1]))]
            splash_boom(tile, 0)
            current_frame = current_frame + 1
            return current_frame
        else:
            current_frame = -1
            return current_frame
    else:
        current_frame = -1
        return current_frame



def health_bar(player, x_coord, y_coord):
    hb_surface = pygame.Surface((200, 25))
    hb_maxhealth = pygame.Rect((x_coord, y_coord, 200, 25))
    hb_health = hb_surface
    player_hp_percent = (player.hitpoints / player.max_hp) * 100
    if player.hitpoints <= 0:
        player.alive = False
        hb_health = pygame.Rect((x_coord, y_coord, 200, 25))
        hb_bloodcolor = pygame.Surface((200 , 25))
    else:
        hb_bloodcolor = pygame.Surface((player_hp_percent * 2, 25))
        hb_health = pygame.Rect((x_coord, y_coord, player_hp_percent * 2, 25))

    hb_surface.fill((0, 0, 0), hb_health)
    if player.alive:
        if player_hp_percent >= 60:
            hb_bloodcolor.fill((100, 240, 100))
        elif player_hp_percent >=30:
            hb_bloodcolor.fill((240, 150, 100))
        else:
            hb_bloodcolor.fill((255, 50, 0))

    else:
        hb_bloodcolor.fill((0, 0, 0))
    screen.blit(hb_surface, hb_maxhealth)
    screen.blit(hb_bloodcolor, hb_health)


def xp_bar(player, x_coord, y_coord):
    xpb_surface = pygame.Surface((200, 25))
    xpb_maxxp = pygame.Rect((x_coord, y_coord, 200, 25))
    player_xp_ratio = (player.curr_xp / player.next_lvl_xp) * 100
    if player.curr_xp <= 0:
        xpb_xp_bar = pygame.Rect((x_coord, y_coord, 200, 25))
        xpb_curr_xp = pygame.Surface((200, 25))
        xpb_curr_xp.fill((0, 0, 0))
    else:
        xpb_curr_xp = pygame.Surface((player_xp_ratio * 2, 25))
        xpb_xp_bar = pygame.Rect((x_coord, y_coord, player_xp_ratio * 2, 25))
        xpb_curr_xp.fill((255, 255, 0))

    xpb_surface.fill((0, 0, 0), xpb_xp_bar)
    screen.blit(xpb_surface, xpb_maxxp)
    screen.blit(xpb_curr_xp, xpb_xp_bar)


def text_objects(text, font, code):
    if code == 0:
        textSurface = font.render(text, True, (255, 255, 255))
    elif code == 1:
        textSurface = font.render(text, True, (255, 0, 0))
    elif code == 2:
        textSurface = font.render(text, True, (0, 255, 0)) # selection color
    return textSurface, textSurface.get_rect()


def dist_to_player(player, nx, ny):
    dist = math.sqrt((nx - player.x_pos)**2 + (ny - player.y_pos)**2)
    return dist


def char_display(actor):
    ax = actor.x_pos
    ay = actor.y_pos


def get_tgt_strs():
    tgts = []
    if not targeted:
        tgts.append("None")
        return tgts
    for t in targeted:
        tgts.append(t.name)
    return tgts

# ################################## SCREENS HERE #####################################

def main_display(player):
    TextSurf1, TextRect1 = text_objects("H.P.:", menufont3, 0)
    TextSurf2, TextRect2 = text_objects("Player:", menufont2, 0)
    TextSurf3, TextRect3 = text_objects("Exp:", menufont3, 0)
    TextSurf4, TextRect4 = text_objects("Act : SPC_BAR", menufont3, 2)

    TextRect1.center = (MENU_COORD_X + 50, MENU_COORD_Y + 75)
    TextRect2.center = (MENU_COORD_X + 100, MENU_COORD_Y + 25)
    TextRect3.center = (MENU_COORD_X + 50, MENU_COORD_Y + 125)
    health_bar(player, MENU_COORD_X + 100, MENU_COORD_Y + 60)
    xp_bar(player, MENU_COORD_X + 100, MENU_COORD_Y + 110)
    TextRect4.center = (MENU_COORD_X + 100, MENU_COORD_Y + 175)
    screen.blit(TextSurf1, TextRect1)
    screen.blit(TextSurf2, TextRect2)
    screen.blit(TextSurf3, TextRect3)
    screen.blit(TextSurf4, TextRect4)


def menu_display():
    global highlight_pos
    if highlight_pos == 1:
        TextSurf1, TextRect1 = text_objects("Fight", menufont2, 2)
        TextSurf2, TextRect2 = text_objects("Pack", menufont2, 0)
        TextSurf3, TextRect3 = text_objects("Stats", menufont2, 0)
        TextSurf4, TextRect4 = text_objects("Menu", menufont2, 0)
    elif highlight_pos == 2:
        TextSurf1, TextRect1 = text_objects("Fight", menufont2, 0)
        TextSurf2, TextRect2 = text_objects("Pack", menufont2, 2)
        TextSurf3, TextRect3 = text_objects("Stats", menufont2, 0)
        TextSurf4, TextRect4 = text_objects("Menu", menufont2, 0)
    elif highlight_pos == 3:
        TextSurf1, TextRect1 = text_objects("Fight", menufont2, 0)
        TextSurf2, TextRect2 = text_objects("Pack", menufont2, 0)
        TextSurf3, TextRect3 = text_objects("Stats", menufont2, 2)
        TextSurf4, TextRect4 = text_objects("Menu", menufont2, 0)
    elif highlight_pos == 4:
        TextSurf1, TextRect1 = text_objects("Fight", menufont2, 0)
        TextSurf2, TextRect2 = text_objects("Pack", menufont2, 0)
        TextSurf3, TextRect3 = text_objects("Stats", menufont2, 0)
        TextSurf4, TextRect4 = text_objects("Menu", menufont2, 2)

    TextSurf5, TextRect5 = text_objects("Select: ENTER    Exit: SPC_BAR", menufont3, 0)

    TextRect1.center = (MENU_COORD_X + 100, MENU_COORD_Y + 45)
    TextRect2.center = (MENU_COORD_X + 280, MENU_COORD_Y + 45)
    TextRect3.center = (MENU_COORD_X + 100, MENU_COORD_Y + 115)
    TextRect4.center = (MENU_COORD_X + 280, MENU_COORD_Y + 115)
    TextRect5.center = (MENU_COORD_X + 190, MENU_COORD_Y + 180)
    screen.blit(TextSurf1, TextRect1)
    screen.blit(TextSurf2, TextRect2)
    screen.blit(TextSurf3, TextRect3)
    screen.blit(TextSurf4, TextRect4)
    screen.blit(TextSurf5, TextRect5)

def attacks_screen(player):
    global highlight_pos
    move_0 = player.move_list[0]
    move_1 = player.move_list[1]
    if highlight_pos == 5:
        TextSurf1, TextRect1 = text_objects(move_0.name, menufont2, 2)
        TextSurf2, TextRect2 = text_objects(move_1.name, menufont2, 0)
    elif highlight_pos == 6:
        TextSurf1, TextRect1 = text_objects(move_0.name, menufont2, 0)
        TextSurf2, TextRect2 = text_objects(move_1.name, menufont2, 2)
    else:
        TextSurf1, TextRect1 = text_objects(move_0.name, menufont2, 0)
        TextSurf2, TextRect2 = text_objects(move_1.name, menufont2, 0)

    TextSurf3, TextRect3 = text_objects("Attacks:", menufont2, 0)
    TextSurf4, TextRect4 = text_objects("Select: ENTER    Return: BKSPC", menufont3, 0)
    TextRect1.center = (MENU_COORD_X + 200, MENU_COORD_Y + 75)
    TextRect2.center = (MENU_COORD_X + 200, MENU_COORD_Y + 125)
    TextRect3.center = (MENU_COORD_X + 100, MENU_COORD_Y + 30)
    TextRect4.center = (MENU_COORD_X + 190, MENU_COORD_Y + 180)
    screen.blit(TextSurf1, TextRect1)
    screen.blit(TextSurf2, TextRect2)
    screen.blit(TextSurf3, TextRect3)
    screen.blit(TextSurf4, TextRect4)


def move_screen(player):
    move = player.move_list[player.move_choice]
    tgts = get_tgt_strs()
    strs = ""
    for i in range(len(tgts)):
        strs = strs + tgts[i]
        tgtSurf, tgtRect = text_objects(tgts[i], menufont4, 1)
        tgtRect.center = (MENU_COORD_X + 80, MENU_COORD_Y + 90 + (30 * i))
        screen.blit(tgtSurf, tgtRect)
        if (targeted == []):
            health_bar(NULL_TGT, MENU_COORD_X + 180, MENU_COORD_Y + 80 + (30 * i))
        elif (len(targeted) > 0):
            health_bar(targeted[i], MENU_COORD_X + 180, MENU_COORD_Y + 80 + (30 * i))
    TextSurf1, TextRect1 = text_objects(move.name, menufont2, 0)
    TextSurf2, TextRect2 = text_objects(str(move.desc) + " HP", menufont3, 0)
    TextSurf3, TextRect3 = text_objects("Aim: num pad", menufont3, 0)
    TextSurf4, TextRect4 = text_objects("Target(s):", menufont4, 1)
    TextSurf5, TextRect5 = text_objects("Attack: enter", menufont3, 0)

    TextRect1.center = (MENU_COORD_X + 190, MENU_COORD_Y + 30)
    TextRect2.center = (MENU_COORD_X + 250, MENU_COORD_Y + 60)
    TextRect3.center = (MENU_COORD_X + 75, MENU_COORD_Y + 180)
    TextRect4.center = (MENU_COORD_X + 115, MENU_COORD_Y + 60)
    TextRect5.center = (MENU_COORD_X + 300, MENU_COORD_Y + 180)
    screen.blit(TextSurf1, TextRect1)
    screen.blit(TextSurf2, TextRect2)
    screen.blit(TextSurf3, TextRect3)
    screen.blit(TextSurf4, TextRect4)
    screen.blit(TextSurf5, TextRect5)


def stats_screen(player):
    TextSurf1, TextRect1 = text_objects("Player Level: " + str(player.level), menufont4, 0) # str(player.level), menufont4, 0)
    TextSurf2, TextRect2 = text_objects("H.P.: " + str(player.hitpoints) + " / " + str(player.max_hp), menufont3, 0)
    TextSurf3, TextRect3 = text_objects("EXP: " + str(player.curr_xp) + " / " + str(player.next_lvl_xp), menufont3, 0)
    TextSurf4, TextRect4 = text_objects("STR: " + str(player.Strength), menufont3, 0)
    TextSurf8, TextRect8 = text_objects("DEF: " + str(player.Defense), menufont3, 0)
    TextSurf5, TextRect5 = text_objects("AGL: " + str(player.Agility), menufont3, 0)
    TextSurf6, TextRect6 = text_objects("DEX: " + str(player.Dexterity), menufont3, 0)
    TextSurf7, TextRect7 = text_objects("LCK: " + str(player.Luck), menufont3, 0)
    TextSurf9, TextRect9 = text_objects("BKSPC: Return", menufont3, 0)
    TextSurf10, TextRect10 = text_objects("SPC: Exit", menufont3, 0)
    TextRect1.center = (MENU_COORD_X + 185, MENU_COORD_Y + 30)
    TextRect2.center = (MENU_COORD_X + 125, MENU_COORD_Y + 75)
    TextRect3.center = (MENU_COORD_X + 125, MENU_COORD_Y + 115)
    TextRect4.center = (MENU_COORD_X + 285, MENU_COORD_Y + 65)
    TextRect8.center = (MENU_COORD_X + 285, MENU_COORD_Y + 90)
    TextRect5.center = (MENU_COORD_X + 285, MENU_COORD_Y + 115)
    TextRect6.center = (MENU_COORD_X + 285, MENU_COORD_Y + 140)
    TextRect7.center = (MENU_COORD_X + 285, MENU_COORD_Y + 165)
    TextRect9.center = (MENU_COORD_X + 100, MENU_COORD_Y + 190)
    TextRect10.center = (MENU_COORD_X + 290, MENU_COORD_Y + 190)
    screen.blit(TextSurf1, TextRect1)
    screen.blit(TextSurf2, TextRect2)
    screen.blit(TextSurf3, TextRect3)
    screen.blit(TextSurf4, TextRect4)
    screen.blit(TextSurf5, TextRect5)
    screen.blit(TextSurf6, TextRect6)
    screen.blit(TextSurf7, TextRect7)
    screen.blit(TextSurf8, TextRect8)
    screen.blit(TextSurf9, TextRect9)
    screen.blit(TextSurf10, TextRect10)


def level_up_screen(player):
    strg = player.Strength
    dfn = player.Defense
    agi = player.Agility
    dex = player.Dexterity
    luk = player.Luck
    stats = [strg, dfn, agi, dex, luk]
    stat_str = "   "
    for s in stats:
        stat_str = stat_str + "  " + str(s) + "   "
    screen.blit(level_up_overlay, (0, 0))
    TextSurf1, TextRect1 = text_objects("Choose a skill to raise:", menufont3, 0)
    # TextSurf2, TextRect2 = text_objects("  STR   DEF   AGI   DEX   LUK", menufont3, 0)
    if highlight_pos == 15:
        StrSurf, StrRect = text_objects(" STR ", menufont3, 2)
    else:
        StrSurf, StrRect = text_objects(" STR ", menufont3, 0)
    if highlight_pos == 16:
        DefSurf, DefRect = text_objects(" DEF ", menufont3, 2)
    else:
        DefSurf, DefRect = text_objects(" DEF ", menufont3, 0)
    if highlight_pos == 17:
        AgiSurf, AgiRect = text_objects(" AGI ", menufont3, 2)
    else:
        AgiSurf, AgiRect = text_objects(" AGI ", menufont3, 0)
    if highlight_pos == 18:
        DexSurf, DexRect = text_objects(" DEX ", menufont3, 2)
    else:
        DexSurf, DexRect = text_objects(" DEX ", menufont3, 0)
    if highlight_pos == 19:
        LukSurf, LukRect = text_objects(" LUK ", menufont3, 2)
    else:
        LukSurf, LukRect = text_objects(" LUK ", menufont3, 0)
    TextSurf3, TextRect3 = text_objects(stat_str, menufont3, 0)
    TextSurf4, TextRect4 = text_objects("Level: " + str(player.level - 1) + " -> " + str(player.level), menufont2, 0)
    TextRect1.center = (MENU_COORD_X + 150, MENU_COORD_Y + 80)
    # TextRect2.center = (MENU_COORD_X + 175, MENU_COORD_Y + 110)
    StrRect.center = (MENU_COORD_X + 40, MENU_COORD_Y + 110)
    DefRect.center = (MENU_COORD_X + 115, MENU_COORD_Y + 110)
    AgiRect.center = (MENU_COORD_X + 190, MENU_COORD_Y + 110)
    DexRect.center = (MENU_COORD_X + 260, MENU_COORD_Y + 110)
    LukRect.center = (MENU_COORD_X + 330, MENU_COORD_Y + 110)
    TextRect3.center = (MENU_COORD_X + 175, MENU_COORD_Y + 130)
    TextRect4.center = (MENU_COORD_X + 175, MENU_COORD_Y + 25)
    screen.blit(TextSurf1, TextRect1)
    # screen.blit(TextSurf2, TextRect2)
    screen.blit(StrSurf, StrRect)
    screen.blit(DefSurf, DefRect)
    screen.blit(AgiSurf, AgiRect)
    screen.blit(DexSurf, DexRect)
    screen.blit(LukSurf, LukRect)
    screen.blit(TextSurf3, TextRect3)
    screen.blit(TextSurf4, TextRect4)


def map_finished_screen(player):
    TextSurf1, TextRect1 = text_objects("Victory!", menufont2, 1)
    TextSurf2, TextRect2 = text_objects("Continue", menufont2, 0)
    TextSurf3, TextRect3 = text_objects("Edit Player", menufont2, 0)
    TextSurf4, TextRect4 = text_objects("Save & Quit", menufont2, 0)
    TextRect1.center = ((GAME_SIZE / 2 * 55, 50))
    TextRect2.center = ((GAME_SIZE / 2 * 55, 150))
    TextRect3.center = ((GAME_SIZE / 2 * 55, 200))
    TextRect4.center = ((GAME_SIZE / 2 * 55, 250))
    screen.blit(TextSurf1, TextRect1)
    screen.blit(TextSurf2, TextRect2)
    screen.blit(TextSurf3, TextRect3)
    screen.blit(TextSurf4, TextRect4)


def main_menu_screen(selection):
    TextSurf1, TextRect1 = text_objects("Senior Project", menufont2, 0)
    if selection == 1:
        TextSurf2, TextRect2 = text_objects("START", menufont3, 2)
        TextSurf3, TextRect3 = text_objects("OPTIONS", menufont3, 0)
        TextSurf4, TextRect4 = text_objects("QUIT", menufont3, 0)
    elif selection == 2:
        TextSurf2, TextRect2 = text_objects("START", menufont3, 0)
        TextSurf3, TextRect3 = text_objects("OPTIONS", menufont3, 2)
        TextSurf4, TextRect4 = text_objects("QUIT", menufont3, 0)
    elif selection == 3:
        TextSurf2, TextRect2 = text_objects("START", menufont3, 0)
        TextSurf3, TextRect3 = text_objects("OPTIONS", menufont3, 0)
        TextSurf4, TextRect4 = text_objects("QUIT", menufont3, 2)
    else:
        TextSurf2, TextRect2 = text_objects("START", menufont3, 0)
        TextSurf3, TextRect3 = text_objects("OPTIONS", menufont3, 0)
        TextSurf4, TextRect4 = text_objects("QUIT", menufont3, 0)
    TextRect1.center = (GAME_SIZE / 2 * 55, 50)
    TextRect2.center = (GAME_SIZE / 2 * 55, 150)
    TextRect3.center = (GAME_SIZE / 2 * 55, 200)
    TextRect4.center = (GAME_SIZE / 2 * 55, 250)
    screen.blit(TextSurf1, TextRect1)
    screen.blit(TextSurf2, TextRect2)
    screen.blit(TextSurf3, TextRect3)
    screen.blit(TextSurf4, TextRect4)


def inventory_screen(player):
    global highlight_pos
    inv = player.item_list
    inv_size = 12
    item_surfs = []
    item_rects = []
    pack_size = len(inv)
    starting_display = player.inv_disp_start
    TitleTextSurf, TitleTextRect = text_objects("Inventory: ", menufont3, 0)
    TitleTextRect.center = (MENU_COORD_X + 75, MENU_COORD_Y + 15)
    screen.blit(TitleTextSurf, TitleTextRect)
    for j in range(pack_size):
        if highlight_pos == j + 7:
            ItemTextSurf, ItemTextRect = text_objects(inv[j].id, menufont2, 2)
        else:
            ItemTextSurf, ItemTextRect = text_objects(inv[j].id, menufont2, 0)
        item_surfs.append(ItemTextSurf)
        item_rects.append(ItemTextRect)
        curr_item_rect = item_rects[starting_display + j]
        if (j + 1) % 2 != 0:
            curr_item_rect.center = (MENU_COORD_X + 115, MENU_COORD_Y + (50 * (math.floor(j / 2) + 1)) )
        else:
            curr_item_rect.center = (MENU_COORD_X + 300, MENU_COORD_Y + (50 * (math.floor(j / 2) + 1)) )
        screen.blit(item_surfs[j], curr_item_rect)


def use_or_toss_poll(player):
    global highlight_pos
    if highlight_pos == 13:
        Poll_UseSurf, Poll_UseRect = text_objects("USE  ", menufont2, 2)
    else:
        Poll_UseSurf, Poll_UseRect = text_objects("USE  ", menufont2, 0)
    if highlight_pos == 14:
        Poll_ThrowSurf, Poll_ThrowRect = text_objects("  THROW", menufont2, 2)
    else:
        Poll_ThrowSurf, Poll_ThrowRect = text_objects("  THROW", menufont2, 0)

    PollMenuSurf, PollMenuRect = text_objects("  USE  THROW ", menufont2, 0)
    PollBackground = pygame.Surface(PollMenuSurf.get_size())
    PollBackground.fill((180, 120, 180))
    PollMenuRect.center = ((MENU_COORD_X + 225, MENU_COORD_Y - 25))
    Poll_UseRect.center = ((MENU_COORD_X + 175, MENU_COORD_Y - 25))
    Poll_ThrowRect.center = ((MENU_COORD_X + 275, MENU_COORD_Y - 25))
    screen.blit(PollBackground, PollMenuRect)
    screen.blit(Poll_UseSurf, Poll_UseRect)
    screen.blit(Poll_ThrowSurf, Poll_ThrowRect)


def item_desc_screen(player):
    reference = {"Potion": potion_img,
                 "Bomb": bomb_img}
    itm = player.item_sel
    id = itm.id
    desc = itm.desc
    img = reference.get(id, "New Item????")
    if player.aiming:
        if not targeted:
            TgtNameSurf, TgtNameRect = text_objects("TGT: [NONE]", menufont3, 0)
            TgtNameRect.center = (MENU_COORD_X + 90, MENU_COORD_Y + 60)
            screen.blit(TgtNameSurf, TgtNameRect)
        else:
            for t in range(len(targeted)):
                TgtNameSurf, TgtNameRect = text_objects("TGT: " + targeted[t].name, menufont3, 0)
                TgtNameRect.center = (MENU_COORD_X + 90, MENU_COORD_Y + (30 * (t + 2)))
                screen.blit(TgtNameSurf, TgtNameRect)
    else:
        TgtNameSurf, TgtNameRect = text_objects("TGT: SELF", menufont3, 0)
        TgtNameRect.center = (MENU_COORD_X + 90, MENU_COORD_Y + 60)
        screen.blit(TgtNameSurf, TgtNameRect)
    img_rect = pygame.Rect(MENU_COORD_X + 250, MENU_COORD_Y + 5, 100, 100)
    ItemNameSurf, ItemNameRect = text_objects(id, menufont2, 0)
    ItemNameRect.center = (MENU_COORD_X + 90, MENU_COORD_Y + 30)
    # ItemDescSurf, ItemDescRect = text_objects(desc, menufont3, 0)
    # ItemDescRect.center = (MENU_COORD_X + 150, MENU_COORD_Y + 150)
    wrap_text(desc, (MENU_COORD_X + 15, MENU_COORD_Y + 100), (MENU_COORD_X + 250, MENU_COORD_Y + 350), menufont3)
    screen.blit(img, img_rect)
    screen.blit(ItemNameSurf, ItemNameRect)
    # screen.blit(ItemDescSurf, ItemDescRect)


def wrap_text(text, pos, max, font, color=pygame.Color('white')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = max
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            screen.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def draw_grid(terr, size, player, enemylist):
    rows = size
    cols = size
    for r in range(rows):
        for c in range(cols):
            if math.floor(GAME_SIZE / 2) + 1 == r and math.floor(GAME_SIZE / 2) + 1 == c:
                tile = pygame.Rect(((55 * r) + OFFSET, (55 * c), 50, 50))
            tile = pygame.Rect(((55 * r) + OFFSET, (55 * c), 50, 50))
            tiles.append(tile)
            # print("Rows: " + str(len(terr)) + "\tCols: " + str(len(terr[0])))
            tertype = terr[r][c]
            screen.blit(weighted_tile_types[tertype.seed_val % (len(weighted_tile_types[1:]) + 1)], tile)
            if player.x_pos == r and player.y_pos == c:
                screen.blit(player.image, tile)
            for e in enemylist:
                if e.which_screen == LEVEL_MAP.curr_screen:
                    if e.x_pos == r and e.y_pos == c:
                        if e.hitpoints > 0:
                            screen.blit(e.image, tile)
                            if tertype.aimed_at:
                                e.target()
                        else:
                            print("Draw grid notices dead enemy")
                            # player.add_xp(e.xp_on_death)
                            tertype.change_occ()
                            enemylist.remove(e)
                        if e in targeted:
                            screen.blit(tgt_icon, pygame.Rect(((55 * r), (55 * c), 25, 25)))
            if tertype.aimed_at:
                screen.blit(aim_highlight, tile)




# build a recursive list to get a path to player
def move_near_player(player, enemy, moved):
    enemy.visited_tiles_check = []
    dx = math.fabs(enemy.x_pos - player.x_pos)
    dy = math.fabs(enemy.y_pos - player.y_pos)
    path_to_player = enemy.path
    at = enemy.last_seen_player
    # print("Where was I looking? (" + str(at.tx) + ", " + str(at.ty) + ")")
    # print("Where is the player? (" + str(player.x_pos) + ", " + str(player.y_pos) + ")")
    if not path_to_player or moved:
        # print(enemy.name + " had " + (lambda p: "no path" if not p else "a path")(path_to_player) + " and player " + (lambda m: "did" if m else "didn't")(moved) + " move.")
        path_to_player = build_paths_rec(enemy, player, [])
    # will put more code here to store and continue paths if the player does/doesn't move
    first_move = path_to_player[0]
    path_to_player.remove(path_to_player[0])
    enemy.path = path_to_player
    enemy.move_to(first_move)


def build_paths_rec(actor, target, paths_list):
    # print(actor.name + " is still trying to build a path.")
    terrain = LEVEL_MAP.curr_screen.tile_map
    ax = actor.x_pos
    ay = actor.y_pos
    tx = target.x_pos
    ty = target.y_pos
    if not paths_list:
        poss_paths = add_possibles(actor, [])
        if poss_paths:
            for i in poss_paths:
                paths_list.append(i)
            # print("paths_list first addition: " + str(len(paths_list)))
            return build_paths_rec(actor, target, paths_list)
        else:
            # print("no possible paths found. staying still")
            return [terrain[ay][ax]]
    else:
        for path in paths_list:
            # print("we have a paths_list already! let's find new possibilities")
            new_paths = add_possibles(actor, path)
            paths_list.remove(path)
            if new_paths:
                for np in new_paths:
                    if np[len(np) - 1].dist_to(terrain[ty][tx]) <= 1:
                        # print("FOUND A PATH")
                        return np
                    else:
                        if not (np in paths_list):
                            paths_list.append(np)
                            # print("appending a path to list")
        return build_paths_rec(actor, target, paths_list)


def add_possibles(actor, path):
    terrain = LEVEL_MAP.curr_screen.tile_map
    if not path:
        act_tile = terrain[actor.y_pos][actor.x_pos]
        actor.visited_tiles_check.append(act_tile)
    else:
        act_tile = path[(len(path) - 1)]
        for t in path:
            if not (t in actor.visited_tiles_check):
                actor.visited_tiles_check.append(t)
    tx = act_tile.tx
    ty = act_tile.ty
    new_paths = []
    new_path_count = 0
    # add RIGHT move poss.
    if check_tile_okay(terrain, tx + 1, ty):
        new_tile = terrain[ty][tx + 1]
        if new_tile in actor.visited_tiles_check:
            print(".")
        else:
            path.append(new_tile)
            new_paths.append(path)
            actor.visited_tiles_check.append(new_tile)
            new_path_count = new_path_count + 1
    # add UP move poss.
    if check_tile_okay(terrain, tx, ty - 1):
        new_tile = terrain[ty-1][tx]
        if new_tile in actor.visited_tiles_check:
            print("..")
        else:
            path.append(new_tile)
            new_paths.append(path)
            actor.visited_tiles_check.append(new_tile)
            new_path_count = new_path_count + 1
    # add LEFT move poss.
    if check_tile_okay(terrain, tx - 1, ty):
        new_tile = terrain[ty][tx - 1]
        if new_tile in actor.visited_tiles_check:
            print("...")
        else:
            path.append(new_tile)
            new_paths.append(path)
            actor.visited_tiles_check.append(new_tile)
            new_path_count = new_path_count + 1
    # add DOWN move poss.
    if check_tile_okay(terrain, tx, ty + 1):
        new_tile = terrain[ty + 1][tx]
        if new_tile in actor.visited_tiles_check:
            print("....")
        else:
            path.append(new_tile)
            new_paths.append(path)
            actor.visited_tiles_check.append(new_tile)
            new_path_count = new_path_count + 1
    # print(actor.name + " found " + str(new_path_count) + " new paths to try")
    return new_paths


def enemy_attack(player, enemy):
    move = enemy.move_list[0]
    move.target = player
    move.execute()


def enemy_turn(state, player, enemylist):
    directions = [1, 2, 3, 4, 6, 7, 8, 9]
    terrain = LEVEL_MAP.curr_screen.tile_map
    for e in enemylist:
        if e.which_screen == LEVEL_MAP.curr_screen:
            dist = math.sqrt(((e.x_pos - player.x_pos)**2) + ((e.y_pos - player.y_pos)**2))
            if 1 < math.floor(dist) <= 4:
                # print(e.name + ": I'm close to the Player!")
                p_tile = terrain[player.y_pos][player.x_pos]
                moved = not (p_tile == e.last_seen_player)
                e.last_seen_player = p_tile
                move_near_player(player, e, moved)
            elif math.floor(dist) <=1:
                enemy_attack(player, e)
            else:
                if e.path:
                    e.move_to(e.path[0])
                    e.path.remove(e.path[0])
                else:
                    e.move_actor(random.choice(directions))


def start_turn(key, player, enemylist):
    global state
    global highlight_pos
    if key == pygame.K_LEFT:
        player.move_player(4)
    elif key == pygame.K_RIGHT:
        player.move_player(6)
    elif key == pygame.K_UP:
        player.move_player(8)
    elif key == pygame.K_DOWN:
        player.move_player(2)
    elif key == pygame.K_SPACE:
        state = 1
        player.locked = True
        player.state = 1
        highlight_pos = 1
    elif 256 < key < 266:
        player.move_player(key - 256)
    else:
        print(key)

    if not player.locked:
        enemy_turn(state, player, enemylist)

def start_nav(key, menu_sel):
    global READY_TO_START
    # The start menu will have a Title Display, along with START, OPTIONS, and QUIT (for now)
    if key == pygame.K_RETURN:
        if menu_sel == 1:
            # Start menu selection
            READY_TO_START = True
            return 0
        elif menu_sel == 2:
            # Options Menu selection
            print("You selected options! It won't do anything...")
            return menu_sel
        elif menu_sel == 3:
            print("You're trying to quit!")
            return -1
        else:
            print("Bad Selection")
            return -1
    elif key == pygame.K_DOWN:
        if 0 < menu_sel < 3:
            return menu_sel + 1
        else:
            return menu_sel
    elif key == pygame.K_UP:
        if 1 < menu_sel <= 3:
            return menu_sel - 1
        else:
            return menu_sel
    elif key == pygame.K_ESCAPE:
        return -1


def menu_nav(key, player, enemy_list):
    global state
    global highlight_pos
    global SET_FOR_RESTATE
    global READY_TO_START
    global CONTINUING_PLAYER
    if key == pygame.K_SPACE:
        state = 0
        player.locked = False
        player.state = 0
        highlight_pos = 0
    elif key == pygame.K_DOWN:
        if highlight_pos == 1 or highlight_pos == 2:
            highlight_pos = highlight_pos + 2
        elif highlight_pos == 5:
            highlight_pos = highlight_pos + 1
        elif 7 <= highlight_pos <= 10:
            highlight_pos = highlight_pos + 2
        elif highlight_pos == 11 or highlight_pos == 12:
            if player.inv_disp_start < 6:
                print("changing inventory display")
                player.inv_disp_start = player.inv_disp_start + 2
        elif highlight_pos == 20 or highlight_pos == 21:  # after map menu nav
            highlight_pos = highlight_pos + 1
    elif key == pygame.K_UP:
        if highlight_pos == 3 or highlight_pos == 4:
            highlight_pos = highlight_pos - 2
        elif highlight_pos == 6:
            highlight_pos = highlight_pos - 1
        elif 9 <= highlight_pos <= 12:
            highlight_pos = highlight_pos - 2
        elif highlight_pos == 7 or highlight_pos == 8:
            if player.inv_disp_start > 0:
                print("changing inventory display")
                player.inv_disp_start = player.inv_disp_start - 2
        elif highlight_pos == 21 or highlight_pos == 22:  # after map menu nav
            highlight_pos = highlight_pos - 1
    elif key == pygame.K_RIGHT:
        if highlight_pos == 1 or highlight_pos == 3:
            highlight_pos = highlight_pos + 1
        elif highlight_pos in [7, 9, 11]:
            highlight_pos = highlight_pos + 1
        elif highlight_pos == 13:
            highlight_pos = highlight_pos + 1
        elif 14 < highlight_pos < 19:
            highlight_pos = highlight_pos + 1
    elif key == pygame.K_LEFT:
        if highlight_pos == 2 or highlight_pos == 4:
            highlight_pos = highlight_pos - 1
        elif highlight_pos in [8, 10, 12]:
            highlight_pos = highlight_pos - 1
        elif highlight_pos == 14:
            highlight_pos = highlight_pos - 1
        elif 15 < highlight_pos < 20:
            highlight_pos = highlight_pos - 1
    elif key == pygame.K_RETURN:
        if highlight_pos == 1: # FIGHT selection
            state = 2
            player.state = 2
            attacks_screen(player)
            highlight_pos = 5
        elif highlight_pos == 2: # PACK selection
            state = 5
            player.state = 5
            highlight_pos = 7
            inventory_screen(player)
        elif highlight_pos == 3: # STATS selection
            state = 4
            player.state = 4
            stats_screen(player)
            highlight_pos = 0 # this might be a problem.
        # if highlight_pos == 4: ...
        elif highlight_pos == 5: # RIFLE selection
            state = 3
            player.state = 3
            player.aiming = True
            player.move_choice = 0
            highlight_pos = 13
            move_screen(player)
        elif highlight_pos == 6: # KNIFE selection
            state = 3
            player.state = 3
            player.aiming = True
            player.move_choice = 1
            highlight_pos = 13
            move_screen(player)
        elif 7 <= highlight_pos <= 12:
            if len(player.item_list) >= (highlight_pos - 6):
                item = player.item_list[highlight_pos - 7]
                player.item_sel = item
                player.state = 6
                state = 6
                highlight_pos = 13
                use_or_toss_poll(player)
            else:
                print("No item there!")
        elif highlight_pos == 13:
            print("USE item: " + player.item_sel.id)
            player.item_sel.use_item()
            player.item_list.remove(player.item_sel)
            SET_FOR_RESTATE = 1
            start_turn(key, player, enemy_list)
        elif highlight_pos == 14:
            print("THROW item: " + player.item_sel.id)
            player.state = 7
            state = 7
            highlight_pos = 0
            player.aiming = True
            player_throw_aim(key, player, enemy_list)
        elif 15 <= highlight_pos < 20:
            player.attr_up(highlight_pos - 15)
            player.leveling = False
            SET_FOR_RESTATE = 1
        elif highlight_pos == 20:  # CONTINUE option after finishing a map
            READY_TO_START = True
            CONTINUING_PLAYER = player
            print("Hey.... we're here...")
        elif highlight_pos == 21 or highlight_pos == 22: #OTHER OPTIONS STILL TO BE IMPLEMENTED
            READY_TO_START = False
            CONTINUING_PLAYER = NULL_PLAYER
    elif key == pygame.K_BACKSPACE:
        if player.state == 4:
            state = 1
            player.state = 1
            highlight_pos = 1
        elif player.state == 2:
            state = 1
            player.state = 1
            highlight_pos = 1
        elif player.state == 5:
            state = 1
            player.state = 1
            highlight_pos = 1
        elif player.state == 6 or player.state == 7:
            state = 5
            player.state = 5
            highlight_pos = 7




def player_aim(key, player, enemy_list):
    global state
    global highlight_pos
    global SET_FOR_RESTATE
    terrain = LEVEL_MAP.screens[LEVEL_MAP.curr_screen]
    move_screen(player)

    if key == pygame.K_SPACE:
        clear_aim()
        state = 0
        player.locked = False
        player.aiming = False
        player.state = 0
        highlight_pos = 0
    elif key == pygame.K_BACKSPACE:
        clear_aim()
        state = 2
        player.state = 2
        player.aiming = False
        highlight_pos = 5
    elif key == pygame.K_LEFT:
        draw_aim(4, player, 0)
        check_target(player, 4, enemy_list)
    elif key == pygame.K_RIGHT:
        draw_aim(6, player, 0)
        check_target(player, 6, enemy_list)
    elif key == pygame.K_UP:
        draw_aim(8, player, 0)
        check_target(player, 8, enemy_list)
    elif key == pygame.K_DOWN:
        draw_aim(2, player, 0)
        check_target(player, 2, enemy_list)
    elif 256 < key < 266:
        dir = key - 256
        draw_aim(dir, player, 0)
        check_target(player, dir, enemy_list)
    elif key == pygame.K_RETURN:
        if not targeted:
            print("No target in sight")
        else:
            for t in targeted:
                move = player.move_list[player.move_choice]
                move.target = t
                move.execute()
                clear_aim()
                if not player.leveling:
                    SET_FOR_RESTATE = 1
                if not enemy_list:
                    highlight_pos = 20
                else:
                    start_turn(key, player, enemy_list)


def player_throw_aim(key, player, enemy_list):
    global state
    global highlight_pos
    global SET_FOR_RESTATE
    global ANIMATING
    global ANIM_COORD_1, ANIM_COORD_2
    global LINEAR_PARAM_X, LINEAR_PARAM_Y
    terrain = LEVEL_MAP.screens[LEVEL_MAP.curr_screen]
    range = math.floor((player.Strength + 1) / 2)
    tgt = player.throw_aim

    if key == pygame.K_SPACE:
        clear_aim()
        state = 0
        player.locked = False
        player.aiming = False
        player.state = 0
        highlight_pos = 0
    elif key == pygame.K_BACKSPACE:
        clear_aim()
        state = 6
        player.state = 6
        player.aiming = False
        highlight_pos = 13
    elif key == pygame.K_LEFT:
            if dist_to_player(player, tgt.tx - 1, tgt.ty) <= range \
                    and 0 <= tgt.tx - 1 < GAME_SIZE \
                    and 0 <= tgt.ty < GAME_SIZE:
                    player.throw_aim = terrain[tgt.tx - 1][tgt.ty]
                    draw_aim(4, player, 1)
                    check_target(player, 4, enemy_list)
    elif key == pygame.K_RIGHT:
            if dist_to_player(player, tgt.tx + 1, tgt.ty) <= range \
                    and 0 <= tgt.tx + 1 < GAME_SIZE \
                    and 0 <= tgt.ty < GAME_SIZE:
                    player.throw_aim = terrain[tgt.tx + 1][tgt.ty]
                    draw_aim(6, player, 1)
                    check_target(player, 6, enemy_list)
    elif key == pygame.K_UP:
            if dist_to_player(player, tgt.tx, tgt.ty - 1) <= range \
                    and 0 <= tgt.tx < GAME_SIZE \
                    and 0 <= tgt.ty - 1 < GAME_SIZE:
                    player.throw_aim = terrain[tgt.tx][tgt.ty - 1]
                    draw_aim(8, player, 1)
                    check_target(player, 8, enemy_list)
    elif key == pygame.K_DOWN:
            if dist_to_player(player, tgt.tx, tgt.ty + 1) <= range \
                    and 0 <= tgt.tx < GAME_SIZE \
                    and 0 <= tgt.ty + 1 < GAME_SIZE:
                    player.throw_aim = terrain[tgt.tx][tgt.ty + 1]
                    draw_aim(2, player, 1)
                    check_target(player, 2, enemy_list)
    elif 256 < key < 266:
        dir = key - 256
        draw_aim(dir, player, 1)
        check_target(player, dir, enemy_list)
    elif key == pygame.K_RETURN:
        if not targeted:
            print("No target in sight")
        else:
            ANIMATING = 0
            ANIM_COORD_1 = (player.x_pos, player.y_pos)
            ANIM_COORD_2 = (player.throw_aim.tx, player.throw_aim.ty)
            player.throw_item(player.item_sel, targeted[0])
            player.item_list.remove(player.item_sel)
            clear_aim()
            ANIMATING = animate(0, LINEAR_PARAM_X, LINEAR_PARAM_Y, ANIMATING, 0.0, 1.0)
            if not player.leveling:
                SET_FOR_RESTATE = 1
            if not enemy_list:
                highlight_pos = 20
                SET_FOR_RESTATE = 2
            else:
                start_turn(key, player, enemy_list)


def draw_aim(direction, player, aim_type):
    move = player.move_list[player.move_choice]
    clear_aim()
    terrain = LEVEL_MAP.screens[LEVEL_MAP.curr_screen]
    if aim_type == 0:
        for i in range(move.range):
            if direction == 4:
                if (player.x_pos - (i + 1)) < 0:
                    print("aim out of range")
                else:
                    tile = terrain[player.x_pos - (i + 1)][player.y_pos]
                    tile.aim_at()
            elif direction == 8:
                if player.y_pos - (i + 1) < 0:
                    print("aim out of range")
                else:
                    tile = terrain[player.x_pos][player.y_pos - (i + 1)]
                    tile.aim_at()
            elif direction == 6:
                if ((i + 1) + player.x_pos) >= GAME_SIZE:
                    print("aim out of range")
                else:
                    tile = terrain[player.x_pos + (i + 1)][player.y_pos]
                    tile.aim_at()
            elif direction == 2:
                if ((i + 1) + player.y_pos) >= GAME_SIZE:
                    print("aim out of range")
                else:
                    tile = terrain[player.x_pos][player.y_pos + (i + 1)]
                    tile.aim_at()
            elif direction == 7:
                if (player.x_pos - (i + 1)) < 0 or (player.y_pos - (i + 1)) < 0:
                    print("aim out of range")
                else:
                    tile = terrain[player.x_pos - (i + 1)][player.y_pos - (i + 1)]
                    tile.aim_at()
            elif direction == 9:
                if player.y_pos - (i + 1) < 0 or player.x_pos + (i + 1) >= GAME_SIZE:
                    print("aim out of range")
                else:
                    tile = terrain[player.x_pos + (i + 1)][player.y_pos - (i + 1)]
                    tile.aim_at()
            elif direction == 1:
                if (player.x_pos - (i + 1)) < 0 or player.y_pos + (i + 1) >= GAME_SIZE:
                    print("aim out of range")
                else:
                    tile = terrain[player.x_pos - (i + 1)][player.y_pos + (i + 1)]
                    tile.aim_at()
            elif direction == 3:
                if ((i + 1) + player.y_pos) >= GAME_SIZE or player.x_pos + (i + 1) >= GAME_SIZE:
                    print("aim out of range")
                else:
                    tile = terrain[player.x_pos + (i + 1)][player.y_pos + (i + 1)]
                    tile.aim_at()
    elif aim_type == 1:
        aim_tile = player.throw_aim
        if direction == 4:
            if aim_tile.tx < 0:
                print("aim out of range")
            else:
                tile = terrain[aim_tile.tx][aim_tile.ty]
                tile.aim_at()
                splash_aim(tile, 0)
                player.throw_aim = tile
        elif direction == 8:
            if aim_tile.ty < 0:
                print("aim out of range")
            else:
                tile = terrain[aim_tile.tx][aim_tile.ty]
                tile.aim_at()
                splash_aim(tile, 0)
                player.throw_aim = tile
        elif direction == 6:
            if aim_tile.tx >= GAME_SIZE:
                print("aim out of range")
            else:
                tile = terrain[aim_tile.tx][aim_tile.ty]
                tile.aim_at()
                splash_aim(tile, 0)
                player.throw_aim = tile
        elif direction == 2:
            if aim_tile.ty >= GAME_SIZE:
                print("aim out of range")
            else:
                tile = terrain[aim_tile.tx][aim_tile.ty]
                tile.aim_at()
                splash_aim(tile, 0)
                player.throw_aim = tile
        elif direction == 7:
            if aim_tile.tx < 0 or aim_tile.ty < 0:
                print("aim out of range")
            else:
                tile = terrain[aim_tile.tx][aim_tile.ty]
                tile.aim_at()
                splash_aim(tile, 0)
                player.throw_aim = tile
        elif direction == 9:
            if aim_tile.ty < 0 or aim_tile.tx >= GAME_SIZE:
                print("aim out of range")
            else:
                tile = terrain[aim_tile.tx][aim_tile.ty]
                tile.aim_at()
                splash_aim(tile, 0)
                player.throw_aim = tile
        elif direction == 1:
            if aim_tile.tx < 0 or aim_tile.ty >= GAME_SIZE:
                print("aim out of range")
            else:
                tile = terrain[aim_tile.tx][aim_tile.ty]
                tile.aim_at()
                splash_aim(tile, 0)
                player.throw_aim = tile
        elif direction == 3:
            if aim_tile.ty >= GAME_SIZE or aim_tile.tx >= GAME_SIZE:
                print("aim out of range")
            else:
                tile = terrain[aim_tile.tx][aim_tile.ty]
                tile.aim_at()
                splash_aim(tile, 0)
                player.throw_aim = tile


def splash_aim(tile, type):
    tx = tile.tx
    ty = tile.ty
    terrain = LEVEL_MAP.screens[LEVEL_MAP.curr_screen]
    if type == 0:
        if 0 < tx < GAME_SIZE - 1 and 0 < ty < GAME_SIZE - 1:
            splash = [tile, terrain[tile.tx - 1][tile.ty],
                      terrain[tile.tx][tile.ty - 1],
                      terrain[tile.tx + 1][tile.ty],
                      terrain[tile.tx][tile.ty + 1]]
        elif 0 < tx < GAME_SIZE - 1 and ty == 0:
            splash = [tile, terrain[tx - 1][ty],
                      terrain[tx + 1][ty],
                      terrain[tx][ty + 1]]
        elif 0 < tx < GAME_SIZE - 1 and ty == GAME_SIZE - 1:
            splash = [tile, terrain[tx - 1][ty],
                      terrain[tx + 1][ty],
                      terrain[tx][ty - 1]]
        elif tx == 0 and 0 < ty < GAME_SIZE - 1:
            splash = [tile, terrain[tx][ty - 1],
                      terrain[tx + 1][ty],
                      terrain[tx][ty + 1]]
        elif tx == GAME_SIZE - 1 and 0 < ty < GAME_SIZE - 1:
            splash = [tile, terrain[tx - 1][ty],
                      terrain[tx][ty - 1],
                      terrain[tx][ty + 1]]
        elif tx == 0 and ty == 0:
            splash = [tile,
                      terrain[tx + 1][ty],
                      terrain[tx][ty + 1]]
        elif tx == 0 and ty == GAME_SIZE - 1:
            splash = [tile,
                      terrain[tx + 1][ty],
                      terrain[tx][ty - 1]]
        elif tx == GAME_SIZE - 1and ty == 0:
            splash = [tile, terrain[tx - 1][ty],
                      terrain[tx][ty + 1]]
        elif tx == GAME_SIZE - 1 and ty == GAME_SIZE - 1:
            splash = [tile, terrain[tx - 1][ty],
                      terrain[tx][ty - 1]]
        for t in splash:
            t.aimed_at = True


def splash_boom(tile, type):
    global blaze_overlay
    tx = tile.tx
    ty = tile.ty
    terrain = LEVEL_MAP.screens[LEVEL_MAP.curr_screen]

    if type == 0:
        if 0 < tx < GAME_SIZE - 1 and 0 < ty < GAME_SIZE - 1:
            splash = [tile, terrain[tile.tx - 1][tile.ty],
                      terrain[tile.tx][tile.ty - 1],
                      terrain[tile.tx + 1][tile.ty],
                      terrain[tile.tx][tile.ty + 1]]
        elif 0 < tx < GAME_SIZE - 1 and ty == 0:
            splash = [tile, terrain[tx - 1][ty],
                      terrain[tx + 1][ty],
                      terrain[tx][ty + 1]]
        elif 0 < tx < GAME_SIZE - 1 and ty == GAME_SIZE - 1:
            splash = [tile, terrain[tx - 1][ty],
                      terrain[tx + 1][ty],
                      terrain[tx][ty - 1]]
        elif tx == 0 and 0 < ty < GAME_SIZE - 1:
            splash = [tile, terrain[tx][ty - 1],
                      terrain[tx + 1][ty],
                      terrain[tx][ty + 1]]
        elif tx == GAME_SIZE - 1 and 0 < ty < GAME_SIZE - 1:
            splash = [tile, terrain[tx - 1][ty],
                      terrain[tx][ty - 1],
                      terrain[tx][ty + 1]]
        elif tx == 0 and ty == 0:
            splash = [tile,
                      terrain[tx + 1][ty],
                      terrain[tx][ty + 1]]
        elif tx == 0 and ty == GAME_SIZE - 1:
            splash = [tile,
                      terrain[tx + 1][ty],
                      terrain[tx][ty - 1]]
        elif tx == GAME_SIZE - 1and ty == 0:
            splash = [tile, terrain[tx - 1][ty],
                      terrain[tx][ty + 1]]
        elif tx == GAME_SIZE - 1 and ty == GAME_SIZE - 1:
            splash = [tile, terrain[tx - 1][ty],
                      terrain[tx][ty - 1]]
        for t in splash:
            blaze_rect = (t.tx * 55 + 5, t.ty * 55, blaze_overlay.get_width(), blaze_overlay.get_height())
            screen.blit(blaze_overlay, blaze_rect)


def check_target(player, direction, enemies):
    move = player.move_list[player.move_choice]
    terrain = LEVEL_MAP.screens[LEVEL_MAP.curr_screen]
    d = 1000
    tiles_list = get_tiles(player, direction, move)
    for e in enemies:
        if terrain[e.x_pos][e.y_pos] in tiles_list:
            e.target()


# this function gets the tiles that are in range of a particular move/attack
def get_tiles(player, direction, move):
    px = player.x_pos
    py = player.y_pos
    terrain = LEVEL_MAP.screens[LEVEL_MAP.curr_screen]
    tiles = []
    for i in range(move.range):
        if direction == 1:
            if px - (i + 1) >= 0 and py + (i + 1) < GAME_SIZE:
                tiles.append(terrain[px - (i + 1)][py + (i + 1)])
        elif direction == 2:
            if py + (i + 1) < GAME_SIZE:
                tiles.append(terrain[px][py + (i + 1)])
        elif direction == 3:
            if px + (i + 1) < GAME_SIZE and py + (i + 1) < GAME_SIZE:
                tiles.append(terrain[px + (i + 1)][py + (i + 1)])
        elif direction == 4:
            if px - (i + 1) >= 0:
                tiles.append(terrain[px - (i + 1)][py])
        elif direction == 6:
            if px + (i + 1) < GAME_SIZE:
                tiles.append(terrain[px + (i + 1)][py])
        elif direction == 7:
            if px - (i + 1) >= 0 and py - (i + 1) >= 0:
                tiles.append(terrain[px - (i + 1)][py - (i + 1)])
        elif direction == 8:
            if py - (i + 1) >= 0:
                tiles.append(terrain[px][py - (i + 1)])
        elif direction == 9:
            if px + (i + 1) < GAME_SIZE and py - (i + 1) >= 0:
                tiles.append(terrain[px + (i + 1)][py - (i + 1)])
    return tiles


def main():
    global state
    global enemies
    global map_highlight_rects
    global highlight_pos
    global MSG_DISP
    global MSG_TIME
    global MSG
    global MSG_RECT
    global SET_FOR_RESTATE
    global READY_TO_START
    global CONTINUING_PLAYER
    global NULL_PLAYER
    global game_finished_surface
    app_loop = True
    if CONTINUING_PLAYER == NULL_PLAYER:
        player_main = Player(3, 3, 0)
    else:
        player_main = CONTINUING_PLAYER
    menu_selection = 1
    map_state = 0
    while app_loop:
        if READY_TO_START:
            player_main.state = 0
            state = 0
            highlight_pos = 0
            player_main.locked = False
            player_main.aiming = False
            player_main.leveling = False
            SET_FOR_RESTATE = 0
            print("HEY WE'RE STARTING A GAME")
            map_state = map_start(player_main)
            READY_TO_START = False
        elif map_state < 0:
            app_loop = False
            READY_TO_START = False
            continue
        elif map_state == 0:
            #This should be the main menu/start screen
            draw_main_menu(menu_selection)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    app_loop = False
                elif event.type == pygame.KEYDOWN:
                    menu_selection = start_nav(event.key, menu_selection)
                    print(str(menu_selection))
                    if menu_selection < 0:
                        app_loop = False
                    elif menu_selection == 0:
                        print(READY_TO_START)

                    continue
        else:
            draw_interim(map_state, player_main)
            if 19 < highlight_pos < len(map_highlight_rects) + 1:
                screen.blit(highlight_arrow, map_highlight_rects[highlight_pos - 1])
            for event in pygame.event.get():
                # print("got an event, event key is: " + str(event.key))
                if event.type == pygame.QUIT:
                    app_loop = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        app_loop = False
                    else:
                        menu_nav(event.key, player_main, enemies)
                        # print("The value of READY TO PLAY: " + str(READY_TO_START))
                        continue


        pygame.display.update()




def map_start(player_main):
    global state
    global enemies
    global map_highlight_rects
    global highlight_pos
    global MSG_DISP
    global MSG_TIME
    global MSG
    global MSG_RECT
    global SET_FOR_RESTATE
    global ANIMATING
    global ANIM_COORD_1, ANIM_COORD_2
    global LINEAR_PARAM_X, LINEAR_PARAM_Y
    global LEVEL_MAP
    enemies = []
    mainloop = True
    state = 0
    px = player_main.x_pos
    py = player_main.y_pos
    player_buffer = range(0, GAME_SIZE - 3)
    map_state = -1
    NUM_ENEMIES = 3
    i = 0

    LEVEL_MAP = Map()
    LEVEL_MAP.output_map_to_file()
    lvl_scr = LEVEL_MAP.curr_screen

    while mainloop:
        screen.blit(background, (0, 0))
        # print("Seed value at Player's location: " + str(lvl_scr.tile_map[player_main.y_pos][player_main.x_pos].seed_val))
        if lvl_scr != LEVEL_MAP.curr_screen:
            print("\n-------------------------------------\nChanged screens somewhere...\n------------------------\n")
            lvl_scr = LEVEL_MAP.curr_screen
        lvl_scr.display_screen(player_main)
        draw_menu(player_main)
        if 0 < highlight_pos < len(map_highlight_rects) + 1:
            screen.blit(highlight_arrow, map_highlight_rects[highlight_pos - 1])
        if player_main.hitpoints <= 0:
            print("Game Over!")
            player_main.alive = False
            mainloop = False
            highlight_pos = 20
            map_state = 0
        # elif not enemies:

        #     # mainloop = False
        #     highlight_pos = 20
        #     map_state = 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
                map_state = -1
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False
                    map_state = -1
                    break
                elif player_main.locked:
                    if player_main.aiming and player_main.state == 3:
                        player_aim(event.key, player_main, enemies)
                    elif player_main.aiming and player_main.state == 7:
                        player_throw_aim(event.key, player_main, enemies)
                    else:
                        menu_nav(event.key, player_main, enemies)
                else:
                    start_turn(event.key, player_main, enemies)
        for t in targeted:
            tile = LEVEL_MAP.curr_screen.tile_map[t.x_pos][t.y_pos]
            if tile.aimed_at:
                screen.blit(tgt_icon, tile.rect)
            else:
                 targeted.remove(t)

        if MSG_DISP:
            if MSG_TIME > 0:
                screen.blit(MSG, MSG_RECT)

        MSG_TIME = MSG_TIME - 1

        if ANIMATING >= 0:
            ANIMATING = animate(0, LINEAR_PARAM_X, LINEAR_PARAM_Y, ANIMATING, 0.0, 1.0)

        pygame.display.update()
        if SET_FOR_RESTATE == 1:
            player_main.state = 0
            state = 0
            highlight_pos = 0
            player_main.locked = False
            player_main.aiming = False
            player_main.leveling = False
            SET_FOR_RESTATE = 0
        elif SET_FOR_RESTATE == 2:
            player_main.state = 0
            state = 0
            highlight_pos = 20
            player_main.locked = False
            player_main.aiming = False
            player_main.leveling = False
            SET_FOR_RESTATE = 0
    return map_state


main()

pygame.quit()
