# Final Project Pygame: Reach Past The Stars
# Author: Joey Petrovic
# Professor: Professor Zanyar Zohourianshahzadi
# Mini Game with Pygame

#.______       _______     ___       ______  __    __     .______      ___           _______.___________.   .___________. __    __   _______         _______.___________.    ___      .______          _______.
#|   _  \     |   ____|   /   \     /      ||  |  |  |    |   _  \    /   \         /       |           |   |           ||  |  |  | |   ____|       /       |           |   /   \     |   _  \        /       |
#|  |_)  |    |  |__     /  ^  \   |  ,----'|  |__|  |    |  |_)  |  /  ^  \       |   (----`---|  |----`   `---|  |----`|  |__|  | |  |__         |   (----`---|  |----`  /  ^  \    |  |_)  |      |   (----`
#|      /     |   __|   /  /_\  \  |  |     |   __   |    |   ___/  /  /_\  \       \   \       |  |            |  |     |   __   | |   __|         \   \       |  |      /  /_\  \   |      /        \   \    
#|  |\  \----.|  |____ /  _____  \ |  `----.|  |  |  |    |  |     /  _____  \  .----)   |      |  |            |  |     |  |  |  | |  |____    .----)   |      |  |     /  _____  \  |  |\  \----.----)   |   
#| _| `._____||_______/__/     \__\ \______||__|  |__|    | _|    /__/     \__\ |_______/       |__|            |__|     |__|  |__| |_______|   |_______/       |__|    /__/     \__\ | _| `._____|_______/    
                                                                                                                                                                                                              
# In this game, you're a space ship that is trying to reach unfathomable speeds to travel the univers. Avoid passing stars to survive, and destroy stars to absorb 
#their energy to increase your speed. 

import turtle
import random
import math

# Setup
wn = turtle.Screen()
wn.title("Reach For The Stars")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)


# BACKDROP----------------------------------------------------------------------------

stars_far = []
stars_near = []

def create_star(color, size):
    s = turtle.Turtle()
    s.speed(0)
    s.shape("circle")
    s.color(color)
    s.penup()
    s.shapesize(stretch_len=size, stretch_wid=size)
    s.goto(random.randint(-300, 300), random.randint(-300, 300))
    return s

# far stars so lil + slower
for _ in range(45):
    stars_far.append(create_star("white", 0.1))

# near stars so big + zoom
for _ in range(25):
    stars_near.append(create_star("white", 0.15))


# PLAYER----------------------------------------------------------------------------PLAYER

player = turtle.Turtle()
player.speed(0)
player.shape("triangle")
player.color("lightgray")
player.penup()
player.setheading(90)
player.goto(0, -250)

player_velocity = 0
player_acceleration = 0.5
max_speed = 6


# BULLET----------------------------------------------------------------------------BULLET

bullet = turtle.Turtle()
bullet.speed(0)
bullet.shape("square")
bullet.color("magenta")
bullet.penup()
bullet.shapesize(stretch_wid=0.7, stretch_len=0.4)
bullet.hideturtle()

bullet_speed = 4
bullet_state = "ready"

# side bullets for multi-shot
side_bullets = []
side_bullet_speed = 2.95 # bec it looks cooler


# BAD GUYS---------------------------------AKA LITERAL STARS------------------------------------------- ENEMIES

enemy_colors = ["cyan", "lime", "yellow", "red", "orange", "magenta", "white"]

def create_enemies():
    enemies = []
    num_enemies = 5
    for _ in range(num_enemies):
        enemy = turtle.Turtle()
        enemy.speed(0)
        enemy.shape("circle")
        enemy.color(random.choice(enemy_colors))
        enemy.penup()
        enemy.goto(random.randint(-280, 280), random.randint(100, 250))
        enemies.append(enemy)
    return enemies

enemies = create_enemies()
enemy_speed = 2
next_speed_threshold = 100


# SCORE----------------------------------------------------------------------------

score = 0
game_over = False

score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.hideturtle()
score_pen.goto(0, 260)
score_pen.write("Score: 0", align="center", font=("Courier", 18, "normal"))


# MOVEMENT----------------------------------------------------------------------------

left_pressed = False
right_pressed = False

def hold_left():
    global left_pressed
    left_pressed = True

def release_left():
    global left_pressed
    left_pressed = False

def hold_right():
    global right_pressed
    right_pressed = True

def release_right():
    global right_pressed
    right_pressed = False

# POWER UPS ----------------------------------------------------------------------------

powerup_active = False
powerup_type = None
powerup_timer = 0
multi_shot_enabled = False
rapid_fire_enabled = False
powerup_duration = 300  # 5 seconds at 60 FPS


#ALMOST FORGOT 
#CLASS (for power ups--------------------------------------------------------------------------------------- CLASS HERE
class PowerUp:
    def __init__(self):
        self.t = turtle.Turtle()
        self.t.speed(0)
        self.t.shape("triangle")
        self.t.color("gray")
        self.t.penup()
        self.t.shapesize(0.8, 0.8)
        self.active = False
        self.type = None

    def spawn(self):
        self.active = True
        self.type = random.choice(["rapidfire", "multishot"])
        self.t.color("gray" if self.type == "rapidfire" else "gold")
        self.t.goto(random.randint(-250, 250), random.randint(100, 250))
        self.t.showturtle()

    def hide(self):
        self.active = False
        self.t.hideturtle()

    def update(self):
        if not self.active:
            return
        self.t.sety(self.t.ycor() - 1)
        if self.t.ycor() < -300:
            self.hide()

    def check_collision(self, player):
        if not self.active:
            return False
        distance = math.hypot(self.t.xcor() - player.xcor(), self.t.ycor() - player.ycor())
        return distance < 25

powerup = PowerUp()


# ACTUALLY FIRING BULLET + MULTISHOT----------------------------------------------------------------------------

def create_side_bullet(offset):
    b = turtle.Turtle()
    b.speed(0)
    b.shape("square")
    b.color("yellow")
    b.penup()
    b.shapesize(0.2, 0.5)
    b.goto(player.xcor() + offset, player.ycor() + 10)
    side_bullets.append(b)

def fire_bullet():
    global bullet_state, multi_shot_enabled
    if bullet_state != "ready" or game_over:
        return
    bullet_state = "fire"
    bullet.goto(player.xcor(), player.ycor() + 10)
    bullet.showturtle()
    if multi_shot_enabled:
        create_side_bullet(-20)
        create_side_bullet(20)

# Restart----------------------------------------------------------------------------

def restart():
    global score, game_over, enemies, bullet_state
    global enemy_speed, bullet_speed, next_speed_threshold
    global powerup_active, powerup_type, powerup_timer
    global multi_shot_enabled, rapid_fire_enabled, side_bullets

    if not game_over:
        return

    score = 0
    game_over = False
    bullet_state = "ready"
    enemy_speed = 2
    bullet_speed = 4
    next_speed_threshold = 100

    score_pen.clear()
    score_pen.goto(0, 260)
    score_pen.write("Score: 0", align="center", font=("Courier", 18, "normal"))

    player.goto(0, -250)
    bullet.hideturtle()
    bullet.goto(0, -400)

    for e in enemies:
        e.hideturtle()
    enemies[:] = create_enemies()

    # Reset the power UPS
    powerup.hide()
    powerup_active = False
    multi_shot_enabled = False
    rapid_fire_enabled = False
    side_bullets.clear()

# COLISION----------------------------------------------------------------------------

def is_collision(t1, t2):
    distance = math.hypot(t1.xcor() - t2.xcor(), t1.ycor() - t2.ycor())
    return distance < 20

# INPUTS/KEYBINDS----------------------------------------------------------------------------

wn.listen()
wn.onkeypress(hold_left, "Left")
wn.onkeyrelease(release_left, "Left")
wn.onkeypress(hold_right, "Right")
wn.onkeyrelease(release_right, "Right")
wn.onkeypress(fire_bullet, "space")
wn.onkeypress(restart, "r")


# MAIN GAME LOOP----------------------------------------------------------------------------MAIN GAME LOOP----------------------------------------------

while True:
    wn.update()

    if game_over:
        continue

    # For star backdrop
    for s in stars_far:
        s.sety(s.ycor() - 0.4)
        if s.ycor() < -320:
            s.goto(random.randint(-300, 300), 320)
    for s in stars_near:
        s.sety(s.ycor() - 1.2)
        if s.ycor() < -320:
            s.goto(random.randint(-300, 300), 320)

    # Movement
    if left_pressed:
        player_velocity -= player_acceleration
    if right_pressed:
        player_velocity += player_acceleration
    player_velocity *= 0.9
    if abs(player_velocity) < 0.01:
        player_velocity = 0
    if player_velocity > max_speed:
        player_velocity = max_speed
    if player_velocity < -max_speed:
        player_velocity = -max_speed
    new_x = player.xcor() + player_velocity
    if -280 < new_x < 280:
        player.setx(new_x)

    # Enemies moving
    for enemy in enemies:
        enemy.sety(enemy.ycor() - enemy_speed)
        if enemy.ycor() < -300:
            enemy.color(random.choice(enemy_colors))
            enemy.goto(random.randint(-280, 280), random.randint(200, 300))

        if is_collision(enemy, player):
            score_pen.clear()
            score_pen.goto(0, 0)
            score_pen.write("GAME OVER - Press R to Restart",
                            align="center", font=("Courier", 20, "bold"))
            game_over = True
            break

        if bullet_state == "fire" and is_collision(bullet, enemy):
            bullet.hideturtle()
            bullet_state = "ready"
            bullet.goto(0, -400)
            enemy.color(random.choice(enemy_colors))
            enemy.goto(random.randint(-280, 280), random.randint(200, 300))
            score += 10
            score_pen.clear()
            score_pen.goto(0, 260)
            score_pen.write(f"Score: {score}", align="center", font=("Courier", 18, "normal")) #--------------------------POWER UP SPEEDS------------------
            if score >= next_speed_threshold:
                enemy_speed += 1
                bullet_speed += 1
                next_speed_threshold += 100
                score_pen.goto(0, 230)
                score_pen.write("Speed Up!", align="center", font=("Courier", 14, "bold"))
                score_pen.goto(0, 260)

    # Bullet firing/moving
    if bullet_state == "fire":
        bullet.sety(bullet.ycor() + bullet_speed)
    if bullet.ycor() > 290:
        bullet.hideturtle()
        bullet_state = "ready"

    for b in side_bullets[:]:
        b.sety(b.ycor() + side_bullet_speed)
        if b.ycor() > 290:
            b.hideturtle()
            side_bullets.remove(b)

    # Spawning Powerups
    if not powerup.active and random.random() < 0.001:
        powerup.spawn()

    powerup.update()
    if powerup.check_collision(player):
        powerup.hide()
        powerup_active = True
        powerup_timer = powerup_duration
        powerup_type = powerup.type
        if powerup_type == "rapidfire":
            rapid_fire_enabled = True
        elif powerup_type == "multishot":
            multi_shot_enabled = True
            score_pen.clear()
            score_pen.write(f"Score: {score} (MULTI SHOT!)", align="center", font=("Courier", 18, "normal"))

    # Powerup effects-----------------------------------------------------------------------------------------------True Bullet Speed
    if rapid_fire_enabled:
        bullet_speed = 15
    else:
        bullet_speed = 6

    if powerup_active:
        powerup_timer -= 1
        if powerup_timer <= 0:
            rapid_fire_enabled = False
            multi_shot_enabled = False
            powerup_active = False
