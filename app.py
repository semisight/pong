from __future__ import division

from math import sin, cos, pi
import random

import pyglet
from pyglet.window import key
from pyglet import clock

# general setup code

random.seed()

keys = {'up': False,
        'dn': False}

window = pyglet.window.Window(600, 400, "Pong!")

fps = clock.ClockDisplay()

ready_label = pyglet.text.Label("Ready?",
                                x=window.width / 2,
                                y=window.height / 2,
                                anchor_x='center',
                                anchor_y='center')
ready_visible = False

point_label = pyglet.text.Label("",
                                font_size=16,
                                x=window.width / 2,
                                y=window.height - 16,
                                anchor_x='center')

ppoints = 0
cpoints = 0

pimg = pyglet.image.load("paddle.png")
bimg = pyglet.image.load("ball.png")

player = pyglet.sprite.Sprite(pimg, y=window.height / 2)
computer = pyglet.sprite.Sprite(pimg)

ball = pyglet.sprite.Sprite(bimg, x=window.width / 2, y=0)
bvx, bvy = 0, 0

# small helper functions


def bounds_check(spr, outer):
    rv = [False, False]

    if spr.x > (outer.width - spr.width):
        spr.x = outer.width - spr.width
        rv[0] = True

    if spr.x < 0:
        spr.x = 0
        rv[0] = True

    if spr.y > (outer.height - spr.height):
        spr.y = outer.height - spr.height
        rv[1] = True

    if spr.y < 0:
        spr.y = 0
        rv[1] = True

    return rv


def push_ball(dt):
    global bvx, bvy, ready_visible

    # First, get rid of the ready label.
    ready_visible = False

    # Set bvx, bvy to a random direction but a magnitude of about 5. We want it
    # to go to the player's side (always), and not be too vertical or
    # horizontal. The minimum y component should be at least 4.
    theta = random.uniform(pi - .7297, pi - pi / 3)
    magn = 5.0

    bvx = magn * cos(theta)
    bvy = magn * sin(theta)


def reset_game():
    global bvx, bvy

    point_label.text = 'Player: {0} Computer: {1}'.format(ppoints, cpoints)

    computer.x = window.width - 8
    computer.y = window.height / 2

    ball.x = window.width / 2
    ball.y = 0
    bvx = 0
    bvy = 0

    global ready_visible
    ready_visible = True
    clock.schedule_once(push_ball, 2)


# pyglet event handlers

@window.event
def on_draw():
    window.clear()

    fps.draw()
    point_label.draw()

    if ready_visible:
        ready_label.draw()

    player.draw()
    computer.draw()
    ball.draw()


@window.event
def on_key_press(keycode, modifiers):
    if keycode == key.UP:
        keys['up'] = True
    elif keycode == key.DOWN:
        keys['dn'] = True


@window.event
def on_key_release(keycode, modifiers):
    if keycode == key.UP:
        keys['up'] = False
    elif keycode == key.DOWN:
        keys['dn'] = False


def phys_input_and_ai(dt):
    # physics (ball)
    global bvx, bvy, cpoints, ppoints

    ball.x += bvx
    ball.y += bvy

    change_x, change_y = bounds_check(ball, window)

    # we have a winner!
    if change_x:
        # player lost
        if bvx < 0:
            cpoints += 1
        else:
            ppoints += 1

        reset_game()
        return

    if change_y:
        bvy = -bvy

    # input
    if keys['up']:
        player.y += 3

    if keys['dn']:
        player.y -= 3

    bounds_check(player, window)

    # ai
    if ball.y < computer.y + computer.height / 2:
        computer.y -= 3

    if ball.y > computer.y + computer.height / 2:
        computer.y += 3

    bounds_check(computer, window)

    # collision detection

    # is computer touching?
    if ball.x > window.width - ball.width - 8:
        if (ball.y > computer.y) and (ball.y < computer.y + computer.height):
            bvx = -bvx

    # is player touching?
    if ball.x < 8:
        if (ball.y > player.y) and (ball.y < player.y + player.height):
            bvx = -bvx

clock.schedule(phys_input_and_ai)

if __name__ == '__main__':
    reset_game()
    pyglet.app.run()
