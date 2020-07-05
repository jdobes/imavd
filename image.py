#!/usr/bin/python3
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import filedialog
import PIL
from PIL import ImageTk, Image


class ImageEditor:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("1280x720")
        self.root.resizable(width=True, height=True)
        self.setup_menus()

        self.bg_img = Image.open("./tile.png")
        self.bg_tiles = set()

        self.frame = Frame(self.root)
        self.v_scroll = Scrollbar(self.frame, orient='vertical')
        self.h_scroll = Scrollbar(self.frame, orient='horizontal')

        self.canvas = Canvas(self.frame, bg="gray")
        self.canvas.config(xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)
        self.v_scroll.config(command=self.canvas.yview)
        self.h_scroll.config(command=self.canvas.xview)
        self.v_scroll.pack(side=RIGHT, fill=Y)
        self.h_scroll.pack(side=BOTTOM, fill=X)
        self.canvas.pack(fill=BOTH, expand=True)
        self.frame.pack(fill=BOTH, expand=True)

        self.current_image = None
        self.refresh_menus()

    def setup_menus(self):
        self.menubar = Menu(self.root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open image", command=self.open_image)
        self.filemenu.add_command(label="Close image", command=self.close_image)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Save as", command=self.save_image_as)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.exit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.imagemenu = Menu(self.menubar, tearoff=0)
        self.imagemenu.add_command(label="Info about image", command=self.image_info)
        self.menubar.add_cascade(label="Image", menu=self.imagemenu)

        self.toolmenu = Menu(self.menubar, tearoff=0)
        self.toolmenu.add_command(label="Pick color", command=self.pick_color_tool)
        self.menubar.add_cascade(label="Tool", menu=self.toolmenu)

        self.root.config(menu=self.menubar)
    
    def refresh_menus(self):
        if self.current_image:
            state = "normal"
            title = f"PhotoEdit - {self.current_image}"
        else:
            state = "disabled"
            title = "PhotoEdit"
        
        self.root.title(title)

        self.filemenu.entryconfig(1, state=state)
        self.filemenu.entryconfig(3, state=state)

        self.menubar.entryconfig(2, state=state)
        self.menubar.entryconfig(3, state=state)

    def canvas_generate_bg(self, w, h):
        new_background_width = 0
        while new_background_width < w:
            new_background_width += 800
        new_background_height = 0
        while new_background_height < h:
            new_background_height += 800
        x = 0
        while x < new_background_width:
            y = 0
            while y < new_background_height:
                #print(f"Creating background tile: x={x}, y={y}")
                crop = [0, 0, 800, 800]
                if (x + 800) > w:
                    crop[2] = w % 800
                if (y + 800) > h:
                    crop[3] = h % 800
                #print(f"crop {crop}")
                img_tk = ImageTk.PhotoImage(self.bg_img.crop(crop))
                self.bg_tiles.add(img_tk)
                self.canvas.create_image(x, y, image=img_tk, anchor=NW)
                y += 800
            x += 800

    def open_image(self):
        filename = filedialog.askopenfilename(title='open')
        if filename:
            self.close_image()
            img = Image.open(filename)
            self.canvas_generate_bg(*img.size)
            self.img = ImageTk.PhotoImage(img)
            self.img_id = self.canvas.create_image(0, 0, image=self.img, anchor=NW)
            self.canvas.config(scrollregion=self.canvas.bbox(self.img_id))
            self.current_image = filename
            self.refresh_menus()
            print(f"File opened: {filename}")
        else:
            print(f"Invalid file: {filename}")

    def close_image(self):
        if self.current_image:
            self.canvas.delete("all")
            self.bg_tiles.clear()
            self.canvas.xview_moveto(0)
            self.canvas.yview_moveto(0)
            self.canvas.config(scrollregion=(0,0,0,0))
            self.current_image = None
            self.refresh_menus()
            print("File closed.")

    def save_image(self):
        pass

    def save_image_as(self):
        pass

    def image_info(self):
        pass

    def pick_color_tool(self):
        pass

    def exit(self):
        self.close_image()
        self.root.quit()

    def run(self):
        self.root.mainloop()


def main():
    ie = ImageEditor()
    ie.run()

if __name__ == "__main__":
    main()
