#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division

import sys
import time
from math import cos, sin, pi, sqrt

import tkinter
import speech_recognition as sr

LAST_COMMAND = '-'
OBJECTS = [[None, None, None, None, None, None, None, None],
           [None, None, None, None, None, None, None, None],
           [None, None, None, None, None, None, None, None],
           [None, None, None, None, None, None, None, None]]
OBJECTS_COUNTS = {"circle": 0, "square": 0, "triangle": 0}
COLORS = ["red", "green", "blue", "yellow", "orange", "black", "white", "grey"]
COLORS_CZECH = {"červená": "red", "zelená": "green", "modrá": "blue",
                "žlutá": "yellow", "oranžová": "orange", "černá": "black", "bílá": "white", "šedá": "grey"}
BACKGROUND_COLOR = "white"
CIRCLE_COLOR = "white"
SQUARE_COLOR = "white"
TRIANGLE_COLOR = "white"
CIRCLE_SCALE = 1.0
SQUARE_SCALE = 1.0
TRIANGLE_SCALE = 1.0
ANGLE = pi/32
SQUARE_ROTATE = 0
TRIANGLE_ROTATE = 0
VOICE_LANGUAGE = "en-US"
canvas = None
DEFAULT_SIZE = 100
HELP_EN = "Voice commands:\n background [color]\n [circle|square|triangle] [color]\n [circle|square|triangle] duplicate\n [circle|square|triangle] [grow|shrink]\n [circle|square|triangle] rotate [left|stop|right]"
HELP_CZ = "Hlasové příkazy:\n pozadí [barva]\n [kruh|čtverec|trojúhelník] [barva]\n [kruh|čtverec|trojúhelník] duplikovat\n [kruh|čtverec|trojúhelník] [zvětšit|zmenšit]\n [kruh|čtverec|trojúhelník] rotovat [doleva|zastavit|doprava]"
HELP = HELP_EN


def set_english():
    global VOICE_LANGUAGE, HELP
    HELP = HELP_EN
    VOICE_LANGUAGE = "en-US"


def set_czech():
    global VOICE_LANGUAGE, HELP
    HELP = HELP_CZ
    VOICE_LANGUAGE = "cs"


def parse_command(text):
    global LAST_COMMAND, CIRCLE_COLOR, SQUARE_COLOR, TRIANGLE_COLOR, CIRCLE_SCALE, \
        SQUARE_SCALE, TRIANGLE_SCALE, SQUARE_ROTATE, TRIANGLE_ROTATE, \
            BACKGROUND_COLOR
    LAST_COMMAND = text.lower()
    parts = text.lower().split()
    if len(parts) < 2:
        return
    if parts[0] == "background" or parts[0] == "pozadí":
        if parts[1] in COLORS:
            BACKGROUND_COLOR = parts[1]
        elif parts[1] in COLORS_CZECH:
            BACKGROUND_COLOR = COLORS_CZECH[parts[1]]
    if parts[0] == "circle" or parts[0] == "kruh":
        if parts[1] == "duplicate" or parts[1] == "duplikovat":
            for _ in range(OBJECTS_COUNTS["circle"]):
                create_object("circle")
        elif parts[1] == "grow" or parts[1] == "zvětšit":
            CIRCLE_SCALE += 0.25
        elif parts[1] == "shrink" or parts[1] == "zmenšit":
            CIRCLE_SCALE -= 0.25
        elif parts[1] in COLORS:
            CIRCLE_COLOR = parts[1]
        elif parts[1] in COLORS_CZECH:
            CIRCLE_COLOR = COLORS_CZECH[parts[1]]
    elif parts[0] == "square" or parts[0] == "čtverec":
        if parts[1] == "duplicate" or parts[1] == "duplikovat":
            for _ in range(OBJECTS_COUNTS["square"]):
                create_object("square")
        elif parts[1] == "grow" or parts[1] == "zvětšit":
            SQUARE_SCALE += 0.25
        elif parts[1] == "shrink" or parts[1] == "zmenšit":
            SQUARE_SCALE -= 0.25
        elif parts[1] == "rotate" or parts[1] == "rotovat":
            if len(parts) > 2:
                if parts[2] == "stop" or parts[2] == "zastavit":
                    SQUARE_ROTATE = 0
                elif parts[2] == "left" or parts[2] == "doleva":
                    SQUARE_ROTATE = -ANGLE
                elif parts[2] == "right" or parts[2] == "doprava":
                    SQUARE_ROTATE = ANGLE
        elif parts[1] in COLORS:
            SQUARE_COLOR = parts[1]
        elif parts[1] in COLORS_CZECH:
            SQUARE_COLOR = COLORS_CZECH[parts[1]]
    elif parts[0] == "triangle" or parts[0] == "trojúhelník":
        if parts[1] == "duplicate" or parts[1] == "duplikovat":
            for _ in range(OBJECTS_COUNTS["triangle"]):
                create_object("triangle")
        elif parts[1] == "grow" or parts[1] == "zvětšit":
            TRIANGLE_SCALE += 0.25
        elif parts[1] == "shrink" or parts[1] == "zmenšit":
            TRIANGLE_SCALE -= 0.25
        elif parts[1] == "rotate" or parts[1] == "rotovat":
            if len(parts) > 2:
                if parts[2] == "stop" or parts[2] == "zastavit":
                    TRIANGLE_ROTATE = 0
                elif parts[2] == "left" or parts[2] == "doleva":
                    TRIANGLE_ROTATE = -ANGLE
                elif parts[2] == "right" or parts[2] == "doprava":
                    TRIANGLE_ROTATE = ANGLE
        elif parts[1] in COLORS:
            TRIANGLE_COLOR = parts[1]
        elif parts[1] in COLORS_CZECH:
            TRIANGLE_COLOR = COLORS_CZECH[parts[1]]


def callback(recognizer, audio):
    try:
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        text = recognizer.recognize_google(audio, language=VOICE_LANGUAGE)
        print("Detected: " + text)
        parse_command(text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def create_object(obj_type):
    global OBJECTS, OBJECTS_COUNTS
    x1 = 30
    y1 = 30
    for idx, row in enumerate(OBJECTS):
        x1 = 30
        for jdx, column in enumerate(row):
            if not column:
                if obj_type == "circle":
                    obj = canvas.create_oval(x1, y1, x1 + DEFAULT_SIZE * CIRCLE_SCALE, y1 + DEFAULT_SIZE * CIRCLE_SCALE, tags="circle")
                    OBJECTS_COUNTS["circle"] += 1
                elif obj_type == "square":
                    obj = canvas.create_polygon([x1, y1, x1 + DEFAULT_SIZE * SQUARE_SCALE, y1, x1 + DEFAULT_SIZE * SQUARE_SCALE, y1 + DEFAULT_SIZE * SQUARE_SCALE, x1, y1 + DEFAULT_SIZE * SQUARE_SCALE], tags="square")
                    OBJECTS_COUNTS["square"] += 1
                elif obj_type == "triangle":
                    obj = canvas.create_polygon([x1, y1 + DEFAULT_SIZE * TRIANGLE_SCALE, x1 + DEFAULT_SIZE * TRIANGLE_SCALE, y1 + DEFAULT_SIZE * TRIANGLE_SCALE, x1 + DEFAULT_SIZE * TRIANGLE_SCALE/2.0, y1], tags="triangle")
                    OBJECTS_COUNTS["triangle"] += 1
                else:
                    return
                OBJECTS[idx][jdx] = obj
                return
            x1 += 130
        y1 += 130


def main():
    root = tkinter.Tk()
    menubar = tkinter.Menu(root)
    langmenu = tkinter.Menu(menubar, tearoff=0)
    langmenu.add_command(label="English", command=set_english)
    langmenu.add_command(label="Czech", command=set_czech)
    menubar.add_cascade(label="Voice language", menu=langmenu)
    root.config(menu=menubar)

    global canvas
    canvas = tkinter.Canvas(root, bg="white", width=1080, height=720)
    canvas.pack()

    create_object("circle")
    create_object("square")
    create_object("triangle")

    help_text = canvas.create_text(200, 630)
    last_command = canvas.create_text(200, 700)

    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source)

    stop_listening = r.listen_in_background(m, callback, phrase_time_limit=5)

    def refresh():
        global CIRCLE_SCALE, SQUARE_SCALE, TRIANGLE_SCALE
        canvas.itemconfigure(help_text, text=HELP)
        canvas.itemconfigure(last_command, text="Last command (%s): %s" % (VOICE_LANGUAGE, LAST_COMMAND))
        canvas.configure(bg=BACKGROUND_COLOR)
        canvas.itemconfig("circle", fill=CIRCLE_COLOR, outline="black")
        canvas.itemconfig("square", fill=SQUARE_COLOR, outline="black")
        canvas.itemconfig("triangle", fill=TRIANGLE_COLOR, outline="black")
        for row in OBJECTS:
            for obj in row:
                if obj is None:
                    continue
                tag = canvas.itemcget(obj, "tags")
                if tag == "circle":
                    x1, y1, x2, y2 = canvas.coords(obj)
                    cx = (x1 + x2)/2
                    cy = (y1 + y2)/2
                    # scale size
                    x1 = cx + sqrt(CIRCLE_SCALE) * (x1 - cx)
                    y1 = cy + sqrt(CIRCLE_SCALE) * (y1 - cy)
                    x2 = cx + sqrt(CIRCLE_SCALE) * (x2 - cx)
                    y2 = cy + sqrt(CIRCLE_SCALE) * (y2 - cy)
                    canvas.coords(obj, x1, y1, x2, y2)
                elif tag == "square":
                    x1, y1, x2, y2, x3, y3, x4, y4 = canvas.coords(obj)
                    cx = (x1 + x2 + x3 + x4)/4
                    cy = (y1 + y2 + y3 + y4)/4
                    # scale size
                    x1 = cx + sqrt(SQUARE_SCALE) * (x1 - cx)
                    y1 = cy + sqrt(SQUARE_SCALE) * (y1 - cy)
                    x2 = cx + sqrt(SQUARE_SCALE) * (x2 - cx)
                    y2 = cy + sqrt(SQUARE_SCALE) * (y2 - cy)
                    x3 = cx + sqrt(SQUARE_SCALE) * (x3 - cx)
                    y3 = cy + sqrt(SQUARE_SCALE) * (y3 - cy)
                    x4 = cx + sqrt(SQUARE_SCALE) * (x4 - cx)
                    y4 = cy + sqrt(SQUARE_SCALE) * (y4 - cy)
                    # rotate
                    x1_org = x1
                    x1 = cos(SQUARE_ROTATE) * (x1_org - cx) - sin(SQUARE_ROTATE) * (y1 - cy) + cx
                    y1 = sin(SQUARE_ROTATE) * (x1_org - cx) + cos(SQUARE_ROTATE) * (y1 - cy) + cy
                    x2_org = x2
                    x2 = cos(SQUARE_ROTATE) * (x2_org - cx) - sin(SQUARE_ROTATE) * (y2 - cy) + cx
                    y2 = sin(SQUARE_ROTATE) * (x2_org - cx) + cos(SQUARE_ROTATE) * (y2 - cy) + cy
                    x3_org = x3
                    x3 = cos(SQUARE_ROTATE) * (x3_org - cx) - sin(SQUARE_ROTATE) * (y3 - cy) + cx
                    y3 = sin(SQUARE_ROTATE) * (x3_org - cx) + cos(SQUARE_ROTATE) * (y3 - cy) + cy
                    x4_org = x4
                    x4 = cos(SQUARE_ROTATE) * (x4_org - cx) - sin(SQUARE_ROTATE) * (y4 - cy) + cx
                    y4 = sin(SQUARE_ROTATE) * (x4_org - cx) + cos(SQUARE_ROTATE) * (y4 - cy) + cy
                    canvas.coords(obj, x1, y1, x2, y2, x3, y3, x4, y4)
                elif tag == "triangle":
                    x1, y1, x2, y2, x3, y3 = canvas.coords(obj)
                    cx = (x1 + x2 + x3)/3
                    cy = (y1 + y2 + y3)/3
                    # scale size
                    x1 = cx + sqrt(TRIANGLE_SCALE) * (x1 - cx)
                    y1 = cy + sqrt(TRIANGLE_SCALE) * (y1 - cy)
                    x2 = cx + sqrt(TRIANGLE_SCALE) * (x2 - cx)
                    y2 = cy + sqrt(TRIANGLE_SCALE) * (y2 - cy)
                    x3 = cx + sqrt(TRIANGLE_SCALE) * (x3 - cx)
                    y3 = cy + sqrt(TRIANGLE_SCALE) * (y3 - cy)
                    # rotate
                    x1_org = x1
                    x1 = cos(TRIANGLE_ROTATE) * (x1_org - cx) - sin(TRIANGLE_ROTATE) * (y1 - cy) + cx
                    y1 = sin(TRIANGLE_ROTATE) * (x1_org - cx) + cos(TRIANGLE_ROTATE) * (y1 - cy) + cy
                    x2_org = x2
                    x2 = cos(TRIANGLE_ROTATE) * (x2_org - cx) - sin(TRIANGLE_ROTATE) * (y2 - cy) + cx
                    y2 = sin(TRIANGLE_ROTATE) * (x2_org - cx) + cos(TRIANGLE_ROTATE) * (y2 - cy) + cy
                    x3_org = x3
                    x3 = cos(TRIANGLE_ROTATE) * (x3_org - cx) - sin(TRIANGLE_ROTATE) * (y3 - cy) + cx
                    y3 = sin(TRIANGLE_ROTATE) * (x3_org - cx) + cos(TRIANGLE_ROTATE) * (y3 - cy) + cy
                    canvas.coords(obj, x1, y1, x2, y2, x3, y3)

        # make current size new original scale
        CIRCLE_SCALE = TRIANGLE_SCALE = SQUARE_SCALE = 1.0
        root.after(40, refresh)

    root.after(40, refresh)
    root.mainloop()
    stop_listening(wait_for_stop=False)

if __name__ == "__main__":
    main()