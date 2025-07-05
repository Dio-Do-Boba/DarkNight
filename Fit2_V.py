import pyxel
import random

class App:
    def __init__(self):
        pyxel.init(200, 170, title='darknight')
        pyxel.load("assets/darknight.pyxres")
        pyxel.mouse(True)
        self.scene = Scene(self)
        
        pyxel.run(self.update, self.draw)

    def update(self):
        self.scene.update()

    def draw(self):
        pyxel.cls(0)
        self.scene.draw()
    

class Scene:
    def __init__(self, app):
        self.app= app
        self.state = "start" #  "start" -> "instructions" ->"story" ->"play"
        self.end_state = "scene1" # scene1-5
        self.player = Player(100, 85, 32, 48, 2) 

        self.PCLock = None
        self.pc_show = False
        self.PasswordLock = None
        self.password = str(random.randint(1000, 9999))

        self.inventory = []  # 存储已获得的道具
        self.last_item_text = ""  # 左下角的提示文字
        self.last_item_timer = 0  # 提示文字的消失计时器

        self.Current_Map_option = 0
        self.Map_options = ['Guide','F3','F2','F1','Elevator','Gate','Office1','Office2','Toilet_Female','Toilet_Male','End']
                            # 0     1      2    3       4       5       6           7       8               9           10
        self.Objects = {
            "F1":[
                {"x": -50, "y": 0, "width": 50, "height": 170, "type": "block", "name": "Wall"},
                {"x": -50, "y": 170, "width": 300, "height": 20, "type": "block", "name": "Wall"},
                {"x": 0, "y": 0, "width": 200, "height": 70, "type": "block", "name": "Wall"},
                {"x": 120, "y": 60, "width": 20, "height": 10, "type": "item", "name": "worm", "icon": (232, 0), "text": "ewww, a worm"}
                ],
            "F2":[
                {"x": -50, "y": 0, "width": 50, "height": 170, "type": "block", "name": "Wall"},
                {"x": 200, "y": 0, "width": 50, "height": 170, "type": "block", "name": "Wall"},
                {"x": -50, "y": 170, "width": 300, "height": 20, "type": "block", "name": "Wall"},
                {"x": 0, "y": 0, "width": 200, "height": 70, "type": "block", "name": "Wall"}
                ],
            "F3":[
                {"x": -50, "y": 0, "width": 50, "height": 170, "type": "block", "name": "Wall"},
                {"x": 200, "y": 0, "width": 50, "height": 170, "type": "block", "name": "Wall"},
                {"x": -50, "y": 170, "width": 300, "height": 20, "type": "block", "name": "Wall"},
                {"x": 0, "y": 0, "width": 200, "height": 70, "type": "block", "name": "Wall"}
                ],
            "Gate":[
                {"x": 200, "y": 0, "width": 50, "height": 170, "type": "block", "name": "Wall"},
                {"x": -50, "y": 170, "width": 300, "height": 20, "type": "block", "name": "Wall"},
                {"x": 0, "y": 0, "width": 200, "height": 70, "type": "block", "name": "Wall"},
                {"x": 30, "y": 60, "width": 20, "height": 10, "type": "item", "name": "worm", "icon": (232, 0), "text": "ewww, a worm"}
                ],
            'Office1':[
                {"x": 153, "y": 24, "width": 31, "height": 35, "type": "item", "name": "note", "icon": (208, 0), "text": "a note with weird symbol, what its for?"},
                {"x": 135, "y": 87, "width": 46, "height": 20, "type": "item", "name": "key", "icon": (168, 48), "text": "i got a key, use it to open something"},
                {"x": 135, "y": 110, "width": 46, "height": 20, "type": "item", "name": "scissor", "icon": (208, 24), "text": "scissor...hmmmm"}
                ],
            'Office2':[
                {"x": 135, "y": 87, "width": 46, "height": 20, "type": "item", "name": "phone", "icon": (208, 72), "text": "i find my phone...why is it here"},
                {"x": 135, "y": 110, "width": 46, "height": 20, "type": "item", "name": "card", "icon": (208, 48), "text": "id card, i can use elevator now"}
                ],
            'Toilet_Female':[
                {"x": -50, "y": 0, "width": 50, "height": 170, "type": "block", "name": "Wall"},
                {"x": 200, "y": 0, "width": 50, "height": 170, "type": "block", "name": "Wall"},
                {"x": -50, "y": 170, "width": 300, "height": 20, "type": "block", "name": "Wall"},
                {"x": 0, "y": 0, "width": 200, "height": 70, "type": "block", "name": "Wall"},
                {"x": 160, "y": 140, "width": 25, "height": 20, "type": "item", "name": "none", "text": "nothing special"},
                {"x": 30, "y": 60, "width": 35, "height": 10, "type": "item", "name": "hair", "icon": (184, 72), "text": "lots of hair...ewww"}
                ],
            'Toilet_Male':[
                {"x": -50, "y": 0, "width": 50, "height": 170, "type": "block", "name": "Wall"},
                {"x": 200, "y": 0, "width": 50, "height": 170, "type": "block", "name": "Wall"},
                {"x": -50, "y": 170, "width": 300, "height": 20, "type": "block", "name": "Wall"},
                {"x": 0, "y": 0, "width": 200, "height": 70, "type": "block", "name": "Wall"},
                {"x": 160, "y": 140, "width": 25, "height": 20, "type": "item", "name": "shit", "icon": (184, 48), "text": "!!! who didn't flush the toilet"},
                {"x": 30, "y": 60, "width": 35, "height": 10, "type": "item", "name": "none", "text": "nothing special, i washed my hands"}
                ],
            }


    def get_current_objects(self):
        return self.Objects.get(self.Map_options[self.Current_Map_option], [])

    def check_item_pickup(self):
        current_map = self.Map_options[self.Current_Map_option]  # 当前地图选项
        picked_up_item = None

        if current_map in ['F3', 'F2', 'F1', 'Gate', 'Toilet_Female', 'Toilet_Male']:
            if pyxel.btnp(pyxel.KEY_R):
                for obj in self.get_current_objects():
                    if obj["type"] == "item":
                        if (abs(self.player.x - obj["x"]) <= 60 and
                                abs(self.player.y - obj["y"]) <= 60):
                            picked_up_item = obj
                            break

        elif current_map in ['Office1', 'Office2']:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y
                for obj in self.get_current_objects():
                    if obj["type"] == "item":
                        if (obj["x"] <= mouse_x <= obj["x"] + obj["width"] and
                                obj["y"] <= mouse_y <= obj["y"] + obj["height"]):
                            picked_up_item = obj
                            break

        if picked_up_item:
            self.pickup_item(picked_up_item)

    def pickup_item(self, obj):
        if obj["name"] == "card" and "key" not in [i["name"] for i in self.inventory]:
            self.last_item_text = "it's locked... where is the key..."
            self.last_item_timer = pyxel.frame_count
            return  

        if obj["name"] not in [i["name"] for i in self.inventory]:
            if obj["name"] != "none":
                self.inventory.append(obj)  
            self.last_item_text = f"{obj['text']}"  
            self.last_item_timer = pyxel.frame_count  

    def draw_inventory(self): 
        x, y = 5, 5 
        for item in self.inventory:
            pyxel.blt(x, y, 0, item["icon"][0], item["icon"][1], 16, 16)  # item sign
            x += 18  # new item move right
        if self.last_item_text and pyxel.frame_count - self.last_item_timer < 300: # show text for 3 sec
            pyxel.text(5, 150, self.last_item_text, 7)


    def update(self):

        if self.Map_options[self.Current_Map_option] == 'Guide':
            self.update_Guide()
        elif self.Map_options[self.Current_Map_option] == 'F3':
            self.update_F3()
        elif self.Map_options[self.Current_Map_option] == 'F2':
            self.update_F2()
        elif self.Map_options[self.Current_Map_option] == 'F1':
            self.update_F1()
        elif self.Map_options[self.Current_Map_option] == 'Elevator':
            self.update_Elevator()
        elif self.Map_options[self.Current_Map_option] == 'Gate':
            self.update_Gate()
        elif self.Map_options[self.Current_Map_option] == 'Office1':
            self.update_Office1()
        elif self.Map_options[self.Current_Map_option] == 'Office2':
            self.update_Office2()
        elif self.Map_options[self.Current_Map_option] == 'Toilet_Female':
            self.update_Toilet_Female()
        elif self.Map_options[self.Current_Map_option] == 'Toilet_Male':
            self.update_Toilet_Male()
        elif self.Map_options[self.Current_Map_option] == 'End':
            self.update_End()
        
    def draw(self):
        self.draw_inventory()
        if self.Map_options[self.Current_Map_option] == 'Guide':
            self.draw_Guide()
        elif self.Map_options[self.Current_Map_option] == 'F3':
            self.draw_F3()
        elif self.Map_options[self.Current_Map_option] == 'F2':
            self.draw_F2()
        elif self.Map_options[self.Current_Map_option] == 'F1':
            self.draw_F1()
        elif self.Map_options[self.Current_Map_option] == 'Elevator':
            self.draw_Elevator()
        elif self.Map_options[self.Current_Map_option] == 'Gate':
            self.draw_Gate()
        elif self.Map_options[self.Current_Map_option] == 'Office1':
            self.draw_Office1()
        elif self.Map_options[self.Current_Map_option] == 'Office2':
            self.draw_Office2()
        elif self.Map_options[self.Current_Map_option] == 'Toilet_Female':
            self.draw_Toilet_Female()
        elif self.Map_options[self.Current_Map_option] == 'Toilet_Male':
            self.draw_Toilet_Male()
        elif self.Map_options[self.Current_Map_option] == 'End':
            self.draw_End()


    def update_Guide(self):
        if self.state == "start":
            if pyxel.btnp(pyxel.KEY_SPACE):  
                self.state = "instructions"
        elif self.state == "instructions":
            if pyxel.btnp(pyxel.KEY_SPACE): 
                self.state = "story"
        elif self.state == "story":
            if pyxel.btnp(pyxel.KEY_SPACE):  
                self.state = "play"
        elif self.state == "play":
            self.Current_Map_option = 1
    
    def draw_Guide(self):
        if self.state == "start":
            pyxel.blt(35, 40, 0, 64, 152, 128, 70)
            pyxel.rect(58, 113, 88, 17,7)
            pyxel.text(63, 120, "Press SPACE to START", 0)
        elif self.state == "instructions":
            pyxel.text(10, 45, "Use WASD keys to move", 7)
            pyxel.text(40, 90, "Use R / MOUSE LEFT CLICK  to interact", 7)
            pyxel.text(30, 120, "Press SPACE to start the game", 7)
        elif self.state == "story":
            pyxel.text(20, 40, "yOU FaLL aSlEeP in cOMpaNy", 7)
            pyxel.text(20, 60, "wHEn YOU wAkE uP", 7)
            pyxel.text(20, 80, "oNLy you StILL iN tHE buILdiNG", 7)
            pyxel.text(100, 150, "yOu nEEd tO Go HOME......", 7)
        elif self.state == "play":
            pass


    def update_F3(self):
        current_objects = self.get_current_objects()
        self.player.move(current_objects)

        if 60 < self.player.x < 110 and 48 < self.player.y < 48+30: # Elevator
            if pyxel.btnp(pyxel.KEY_R):
                if "card" not in [i["name"] for i in self.inventory]:
                    self.last_item_text = "can't use it with out an ID card..."
                else:
                    self.Current_Map_option = 4
        if 0 < self.player.x < 33 and 48 < self.player.y < 48+30: # office1
            if pyxel.btnp(pyxel.KEY_R):
                self.Current_Map_option = 6
        if 130 < self.player.x < 165 and 48 < self.player.y < 48+30: # office2
            if pyxel.btnp(pyxel.KEY_R):
                self.Current_Map_option = 7

    def draw_F3(self):
        pyxel.line(0, 100, 200, 100, 7)
        pyxel.text(98, 40, "F3", 7)
        pyxel.blt(20, 53, 0, 72, 48, 32, 47) #office1
        pyxel.blt(148, 53, 0, 72, 48, 32, 47) #office2
        pyxel.blt(80, 48, 0, 112, 0, 58, 50) #elevator
        self.player.draw()
        self.draw_inventory()

    def update_F2(self):
        current_objects = self.get_current_objects()
        self.player.move(current_objects)

        if 60 < self.player.x < 110 and 48 < self.player.y < 48+30: # Elevator
            if pyxel.btnp(pyxel.KEY_R):
                self.Current_Map_option = 4
        if 0 < self.player.x < 33 and 48 < self.player.y < 48+30: # toiletfemale
            if pyxel.btnp(pyxel.KEY_R):
                self.player.x = 85
                self.Current_Map_option = 8
        if 130 < self.player.x < 165 and 48 < self.player.y < 48+30: # toiletmale
            if pyxel.btnp(pyxel.KEY_R):
                self.player.x = 85
                self.Current_Map_option = 9

    def draw_F2(self):
        pyxel.line(0, 100, 200, 100, 7)
        pyxel.text(98, 40, "F2", 7)
        pyxel.blt(80, 48, 0, 112, 0, 58, 50) #elevator
        pyxel.blt(20, 61, 0, 72, 96, 27, 39) #toilet
        pyxel.text(20, 55, "FEMALE", 7)
        pyxel.blt(148, 61, 0, 72, 96, 27, 39) #toilet
        pyxel.text(148, 55, "MALE", 7)
        self.player.draw()
        self.draw_inventory()

    def update_F1(self):
        current_objects = self.get_current_objects()
        self.player.move(current_objects)
        self.check_item_pickup()

        if 30 < self.player.x < 80 and 48 < self.player.y < 48+30: # Elevator
            if pyxel.btnp(pyxel.KEY_R):
                self.Current_Map_option = 4
        if self.player.x > 200: # gateway
            self.Current_Map_option = 5
            self.player.x = 20

    def draw_F1(self):
        pyxel.line(0, 100, 200, 100, 7)
        pyxel.text(67, 40, "F1", 7)
        pyxel.blt(50, 48, 0, 112, 0, 58, 50) #elevator
        pyxel.blt(118, 68, 0, 115, 112, 30, 32) #plants
        pyxel.blt(145, 25, 0, 1, 218, 25, 10) #exitsigh
        self.player.draw()
        self.draw_inventory()


    def update_Elevator(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):  
            x, y = pyxel.mouse_x, pyxel.mouse_y
            if 90 <= x <= 110 and 40 <= y <= 60:  #F3
                self.Current_Map_option = 1
            elif 90 <= x <= 110 and 80 <= y <= 100:  #F2
                self.Current_Map_option = 2
            elif 90 <= x <= 110 and 120 <= y <= 140:  #F1
                self.Current_Map_option = 3
            
    def draw_Elevator(self):
        pyxel.cls(0)
        pyxel.blt(90, 120 ,0 , 200, 96, 16, 16) #F1
        pyxel.blt(90, 80 ,0 , 200, 112, 16, 16) #F2
        pyxel.blt(90, 40 ,0 , 200, 128, 16, 16) #F3


    def update_Gate(self):
        current_objects = self.get_current_objects()
        self.player.move(current_objects)
        self.check_item_pickup()
        if self.player.x < 0: # F1
            self.Current_Map_option = 3
            self.player.x = 180
        if 130 < self.player.x < 155 and 48 < self.player.y < 48+30: # passwordlock
            if pyxel.btnp(pyxel.KEY_R):
                if not self.PasswordLock:  
                    self.PasswordLock = PasswordLock(self)
            if self.PasswordLock:  
                self.PasswordLock.update()
            if self.PasswordLock and self.PasswordLock.door_open:
                self.PasswordLock = None  # 清空密码锁
                return  # 防止后续逻辑干扰
        
    def draw_Gate(self):
        pyxel.line(0, 100, 200, 100, 7)
        pyxel.blt(90, 48, 0, 112, 56, 55, 50) #gate
        pyxel.blt(150, 65, 0, 168, 77, 11, 15) #lock
        pyxel.blt(28, 68, 0, 115, 112, 30, 32) #plants
        pyxel.blt(55, 25, 0, 1, 218, 25, 10) #exitsigh
        self.player.draw()
        self.draw_inventory()
        if self.PasswordLock:  
            self.PasswordLock.draw()


    def update_Office1(self):
        self.check_item_pickup()
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):  
            x, y = pyxel.mouse_x, pyxel.mouse_y
            if 15 <= x <= 50 and 25 <= y <= 41:  #F3
                self.Current_Map_option = 1
        
    def draw_Office1(self):
        pyxel.blt(0, 0, 1, 0, 0, 200, 170)
        pyxel.blt(15, 25, 0, 32, 216, 35, 16)
        self.draw_inventory()

    def update_Office2(self):
        self.check_item_pickup()
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):  
            x, y = pyxel.mouse_x, pyxel.mouse_y
            if 15 <= x <= 50 and 25 <= y <= 41:  #F3
                self.Current_Map_option = 1
            if 9 <= x <= 34 and 134 <= y <= 157:
                if not self.PCLock:
                    self.PCLock = PCLock(self)
            if self.PCLock:
                self.PCLock.update()
            if self.PCLock and self.PCLock.pc_unlock:
                self.pc_show = True
                self.PCLock = None
                return

    def draw_Office2(self):
        pyxel.blt(0, 0, 2, 0, 0, 200, 170)
        pyxel.blt(15, 25, 0, 32, 216, 35, 16)
        self.draw_inventory()
        if self.PCLock:  
            self.PCLock.draw()
        if self.pc_show:
            pyxel.text(68, 77, "PC Unlocked!", 8)
            pyxel.text(68, 85, f"PW: {self.password}", 8)


    def update_Toilet_Female(self):
        current_objects = self.get_current_objects()
        self.player.move(current_objects)
        self.check_item_pickup()

        if 90 < self.player.x < 120 and 50 < self.player.y < 50+30: # F2
            if pyxel.btnp(pyxel.KEY_R):
                self.player.x = 20
                self.player.y = 100
                self.Current_Map_option = 2

    def draw_Toilet_Female(self):
        pyxel.line(0, 100, 200, 100, 7)
        pyxel.blt(115, 61, 0, 72, 96, 27, 39) #toilet door
        pyxel.text(117, 50, "FEMALE", 7)
        pyxel.blt(150, 110, 0, 144, 112, 31, 39) #toilet
        pyxel.blt(30, 50, 0, 168, 0, 39, 45) #sink
        self.player.draw()
        self.draw_inventory()

    def update_Toilet_Male(self):
        current_objects = self.get_current_objects()
        self.player.move(current_objects)
        self.check_item_pickup()

        if 90 < self.player.x < 120 and 50 < self.player.y < 50+30: # F2
            if pyxel.btnp(pyxel.KEY_R):
                self.player.x = 150
                self.player.y = 100
                self.Current_Map_option = 2

    def draw_Toilet_Male(self):
        pyxel.line(0, 100, 200, 100, 7)
        pyxel.blt(115, 61, 0, 72, 96, 27, 39) #toilet door
        pyxel.text(117, 50, "MALE", 7)
        pyxel.blt(150, 110, 0, 144, 112, 31, 39) #toilet
        pyxel.blt(30, 50, 0, 168, 0, 39, 45) #sink
        self.player.draw()
        self.draw_inventory()


    def update_End(self):
        if self.end_state == "scene1":
            if pyxel.btnp(pyxel.KEY_SPACE):  
                self.end_state = "s2"
        elif self.end_state == "s2":
            if pyxel.btnp(pyxel.KEY_SPACE): 
                self.end_state = "s3"
        elif self.end_state == "s3":
            if pyxel.btnp(pyxel.KEY_SPACE):  
                self.end_state = "s4"
        elif self.end_state == "s4":
            if pyxel.btnp(pyxel.KEY_SPACE):  
                self.end_state = "s5"

    def draw_End(self):
        if self.end_state == "scene1":
            pyxel.rect(75, 70, 50, 40,7)
            pyxel.text(63, 153, "Press SPACE to walk", 7)
        elif self.end_state == "s2":
            pyxel.rect(50, 50, 100, 80,7)
            pyxel.text(63, 153, "Press SPACE to walk", 7)
        elif self.end_state == "s3":
            pyxel.rect(25, 30, 150, 120,7)
            pyxel.text(63, 153, "Press SPACE to RUN", 8)
        elif self.end_state == "s4":
            pyxel.rect(0, 0, 200, 170,7)
            pyxel.text(70, 80, "I can go home now", 0)
            pyxel.text(97, 90, "...", 0)
        elif self.end_state == "s5":
            pyxel.rect(0, 0, 200, 170,7)
            pyxel.text(77, 80, "GAMEOVER", 0)



class Player:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

        self.direction = 'idle' 
        self.animation_frame = 0
        self.animation_speed = 4
        self.frame_count = 0

    def move(self, collision_objects):
        move_x, move_y = 0, 0

        if pyxel.btn(pyxel.KEY_A):
            move_x = -1
            self.direction = 'left'
        elif pyxel.btn(pyxel.KEY_D):
            move_x = 1
            self.direction = 'right'
        elif pyxel.btn(pyxel.KEY_S):
            move_y = 1
            self.direction = 'down'
        elif pyxel.btn(pyxel.KEY_W):
            move_y = -1
            self.direction = 'up'
        else:
            self.direction = 'idle'

        move_x *= self.speed
        move_y *= self.speed

        if move_x != 0:
            move_y = 0

        if not self.is_colliding(move_x, 0, collision_objects):
            self.x += move_x
        if not self.is_colliding(0, move_y, collision_objects):
            self.y += move_y

        if move_x != 0 or move_y != 0:
            self.frame_count += 1
            if self.frame_count >= self.animation_speed:
                self.frame_count = 0
                self.animation_frame = (self.animation_frame + 1) % 2

    def is_colliding(self, dx, dy, collision_objects):
    
        player_box = {
            "x1": self.x + dx,
            "y1": self.y + dy,
            "x2": self.x + dx + self.width,
            "y2": self.y + dy + self.height
        }

        for obj in collision_objects:
            object_box = {
                "x1": obj["x"],
                "y1": obj["y"],
                "x2": obj["x"] + obj["width"],
                "y2": obj["y"] + obj["height"]
            }
            if not (
                player_box["x2"] < object_box["x1"] or  # 左侧
                player_box["x1"] > object_box["x2"] or  # 右侧
                player_box["y2"] < object_box["y1"] or  # 上方
                player_box["y1"] > object_box["y2"]     # 下方
            ):
                return True  
        return False  

    def draw(self):
        if self.direction == 'down':
            v = 0
            u = self.animation_frame * 32
        elif self.direction == 'up':
            v = 144
            u = self.animation_frame * 32
        elif self.direction == 'left':
            v = 48
            u = self.animation_frame * 32
        elif self.direction == 'right':
            v = 96
            u = self.animation_frame * 32
        else:
            u, v = 0, 0
        pyxel.blt(self.x, self.y, 0, u, v, self.width, self.height, 0)



class PasswordLock:
    def __init__(self, Scene):
        self.scene = Scene 
        self.input_password = ""  
        self.feedback = ""  
        self.door_open = False

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):  
            x, y = pyxel.mouse_x, pyxel.mouse_y
            self.handle_click(x, y)

    def handle_click(self, x, y):
        lock_x1, lock_x2 = 70, 130
        lock_y1, lock_y2 = 40, 130

        if lock_x1 <= x <= lock_x2 and lock_y1 <= y <= lock_y2:
            if 40+70 <= x <= 54+70 and 72+40 <= y <= 84+40:  
                self.check_password()
            elif 5+70 <= x <= 20+70 and 29+40 <= y <= 41+40:  
                self.add_digit("1")
            elif 23+70 <= x <= 37+70 and 29+40 <= y <= 41+40:  
                self.add_digit("2")
            elif 40+70 <= x <= 54+70 and 29+40 <= y <= 41+40:  
                self.add_digit("3")
            elif 5+70 <= x <= 20+70 and 44+40 <= y <= 55+40:  
                self.add_digit("4")
            elif 23+70 <= x <= 37+70 and 44+40 <= y <= 55+40:  
                self.add_digit("5")
            elif 40+70 <= x <= 54+70 and 44+40 <= y <= 55+40:  
                self.add_digit("6")
            elif 5+70 <= x <= 20+70 and 58+40 <= y <= 69+40:  
                self.add_digit("7")
            elif 23+70 <= x <= 37+70 and 58+40 <= y <= 69+40:  
                self.add_digit("8")
            elif 40+70 <= x <= 54+70 and 58+40 <= y <= 69+40:  
                self.add_digit("9")
            elif 5+70 <= x <= 37+70 and 72+40 <= y <= 84+40:  
                self.add_digit("0")
        else:
            self.scene.PasswordLock = None
        
    def add_digit(self, digit):
        if len(self.input_password) < 4: 
            self.input_password += digit

    def check_password(self):
        if self.input_password == self.scene.password:
            self.feedback = "Access Granted!"
            self.door_open = True

            if "End" in self.scene.Map_options:
                self.scene.Current_Map_option = self.scene.Map_options.index("End")
        else:
            self.feedback = "Access Denied!"
            self.input_password = ""  

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(70, 40 ,0 , 192, 160, 60, 90)
        pyxel.text(80, 50, f"{self.input_password}", 8)
        pyxel.text(20, 160, self.feedback, 7)
       


class PCLock:
    def __init__(self, Scene):
        self.scene = Scene 
        self.order = "1234"
        self.input_order = ""  
        self.feedback = ""  
        self.pc_unlock = False

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):  
            x, y = pyxel.mouse_x, pyxel.mouse_y
            self.handle_click(x, y)

    def handle_click(self, x, y):
        if 100 <= x <= 140 and 120 <= y <= 135:  
            self.check_password()
        elif 60 <= x <= 100 and 40 <= y <= 80:  
            self.add_digit("2")
        elif 100 <= x <= 140 and 40 <= y <= 80:  
            self.add_digit("3")
        elif 60 <= x <= 100 and 80 <= y <= 120:  
            self.add_digit("4")
        elif 100 <= x <= 140 and 80 <= y <= 120:  
            self.add_digit("1")
        elif 60 <= x <= 140 and 120 <= y <= 135:
            self.scene.PCLock = None   

    def add_digit(self, digit):
        if len(self.input_order) < 4: 
            self.input_order += digit

    def check_password(self):
        if self.input_order == self.order:
            self.feedback = "Access Granted!"
            self.pc_unlock = True

        else:
            self.feedback = "Access Denied!"
            self.input_order = ""  

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(40,30,120,110,1)
        pyxel.blt(140, 35, 1, 208, 160, 16, 16)
        #2
        pyxel.blt(63, 41 ,1 , 208, 0, 32, 32)
        #3
        pyxel.blt(102, 41 ,1 , 208, 40, 32, 32)
        #4
        pyxel.blt(63, 81 ,1 , 208, 80, 32, 32)
        #1
        pyxel.blt(102, 81 ,1 , 208, 120, 32, 32)
        #check
        pyxel.text(111, 122, "CHECK", 7)
        pyxel.text(64, 122, "RETURN", 7)
        pyxel.text(70, 32, self.feedback, 7)


App()
