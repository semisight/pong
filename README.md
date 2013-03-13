#Pong
##Experimenting with Pyglet

I wrote this quickly in about 2 hours out of curiosity. It has been a long time since I've done any game programming--I taught myself on it (DarkBASIC), but I've not gotten back to it since I picked up my first real language, C++.

As it turned out, this was a lot of fun! I really liked working with Pyglet. It is a very Pythonic 2D game library, and reminds me a lot of my experiences with Flask, the web micro-framework. Pyglet is opinionated, but not overly so. You can create your own timer/callback pairings for events as I did for physics and AI, and nothing is forced on you.

```python
@window.event
def on_draw():
	... 
```

Pyglet

```python
@app.route
def index():
	...
```

Flask

I may come back to this in the future. For now, it's definitely a good example of how easy and relaxed Python gamedev can be.
