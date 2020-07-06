#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import time

from tkinter import *
from tkinter import filedialog, colorchooser
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

        self.img = None

        self.img_tk = None
        self.img_id = None

        self.frame = Frame(self.root)
        self.v_scroll = Scrollbar(self.frame, orient='vertical')
        self.h_scroll = Scrollbar(self.frame, orient='horizontal')

        self.canvas = Canvas(self.frame, bg="gray", highlightthickness=0)
        self.canvas.config(xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.v_scroll.config(command=self.canvas.yview)
        self.h_scroll.config(command=self.canvas.xview)
        self.v_scroll.pack(side=RIGHT, fill=Y)
        self.h_scroll.pack(side=BOTTOM, fill=X)
        self.canvas.pack(fill=BOTH, expand=True)
        self.frame.pack(fill=BOTH, expand=True)

        self.current_image = None
        self.refresh_menus()

        self.current_color = "#000000"
        self.color_window = None
        self.color_canvas = None
        self.color_label = None

        self.crop_window = None
        self.crop_rectangle = None

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
        self.imagemenu.add_command(label="Find a color", command=self.find_color)
        self.imagemenu.add_command(label="Crop area", command=self.crop_area_dialog)
        self.menubar.add_cascade(label="Image", menu=self.imagemenu)

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
            try:
                self.img = Image.open(filename).convert("RGBA")
            except:
                print(f"Unable to open file: {filename}! Invalid image format?")
                window = Toplevel()
                window.title("ERROR")
                window.attributes('-topmost', 'true')
                label = Label(window, text=f"Unable to open {filename}! Invalid image format?")
                label.pack(fill='x', padx=50, pady=5)
                button_close = Button(window, text="OK", command=window.destroy)
                button_close.pack(fill='x')
                return
            self.current_image = filename
            self.render_image()
            self.refresh_menus()
            print(f"File opened: {filename}")
        else:
            print(f"No file specified: {filename}")
    
    def render_image(self):
        self.canvas_generate_bg(*self.img.size)
        self.img_tk = ImageTk.PhotoImage(self.img)
        self.img_id = self.canvas.create_image(0, 0, image=self.img_tk, anchor=NW)
        self.canvas.config(scrollregion=self.canvas.bbox(self.img_id))

    def close_image(self):
        if self.current_image:
            self.canvas.delete("all")
            self.bg_tiles.clear()
            self.canvas.xview_moveto(0)
            self.canvas.yview_moveto(0)
            self.canvas.config(scrollregion=(0,0,0,0))
            self.current_image = None
            self.img = None
            self.img_tk = None
            self.img_id = None
            self.refresh_menus()
            print("File closed.")

    def save_image(self):
        pass

    def save_image_as(self):
        pass

    def image_info(self):
        window = Toplevel()
        window.title("Image details")
        window.attributes('-topmost', 'true')

        name_parts = os.path.basename(self.current_image).rsplit('.', 1)

        name = Label(window, text="Image Name:")
        name.grid(row=0, column=0, sticky=W)
        name_data = Label(window, text=f"{name_parts[0]}")
        name_data.grid(row=0, column=1, sticky=W)

        extension = Label(window, text="Image Extension:")
        extension.grid(row=1, column=0, sticky=W)
        if len(name_parts) > 1:
            extension_data = Label(window, text=f".{name_parts[1]}")
            extension_data.grid(row=1, column=1, sticky=W)
        else:
            extension_data = Label(window, text="-")
            extension_data.grid(row=1, column=1, sticky=W)

        location = Label(window, text="Image Location:")
        location.grid(row=2, column=0, sticky=W)
        location_data = Label(window, text=f"{os.path.dirname(self.current_image)}")
        location_data.grid(row=2, column=1, sticky=W)

        dimension = Label(window, text="Image Dimension:")
        dimension.grid(row=3, column=0, sticky=W)
        dimension_data = Label(window, text=f"{self.img.size[0]}x{self.img.size[1]}")
        dimension_data.grid(row=3, column=1, sticky=W)

        size = Label(window, text="Image Size:")
        size.grid(row=4, column=0, sticky=W)
        size_data = Label(window, text=f"{round(os.stat(self.current_image).st_size/1000, 2)} KB")
        size_data.grid(row=4, column=1, sticky=W)

        created = Label(window, text="Image Created On:")
        created.grid(row=5, column=0, sticky=W)
        created_data = Label(window, text=f"{time.ctime(os.path.getctime(self.current_image))}")
        created_data.grid(row=5, column=1, sticky=W)

        button_close = Button(window, text="OK", command=window.destroy)
        button_close.grid(row=6, column=0, columnspan=2)
    
    def count_pixels(self):
        window = Toplevel()
        window.title("Pixels in image")
        window.attributes('-topmost', 'true')
        cnt = 0
        rgb = tuple(int(self.current_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        for pixel in self.img.getdata():
            if pixel[0] == rgb[0] and pixel[1] == rgb[1] and pixel[2] == rgb[2]:
                cnt += 1
        label = Label(window, text=f"Pixels of this color in image: {cnt}")
        label.pack(fill='x', padx=50, pady=5)
        button_close = Button(window, text="OK", command=window.destroy)
        button_close.pack(fill='x')
    
    def set_color(self, new_color):
        self.current_color = new_color
        self.color_canvas.configure(bg=self.current_color)
        self.color_label.configure(text=f"{self.current_color}")

    def pick_color_palette(self):
        my_color = colorchooser.askcolor(color=self.current_color)
        if my_color[1]:
            self.set_color(my_color[1])
    
    def canvas_click(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        if self.img and x <= self.img.size[0] and y <= self.img.size[1]:
            rgba = self.img.getpixel((x, y))
            print(f"clicked at x={x}, y={y}, rgba={rgba}")
            rgb_hex = "#%02x%02x%02x" % (rgba[0], rgba[1], rgba[2])
            if self.color_canvas and self.color_label:
                self.set_color(rgb_hex)

    def find_color(self):
        self.color_window = Toplevel()
        self.color_window.title("Find a color")
        self.color_window.attributes('-topmost', 'true')

        self.color_canvas = Canvas(self.color_window, bg=self.current_color, width=64, height=64)
        self.color_canvas.grid(row=0, column=0, rowspan=2, columnspan=2)
        self.color_label = Label(self.color_window, text=f"{self.current_color}")
        self.color_label.grid(row=2, column=0)

        pick_color = Button(self.color_window, text="Pick a color from palette", command=self.pick_color_palette)
        pick_color.grid(row=0, column=2, columnspan=1)

        pick_color = Button(self.color_window, text="Pixels of this color in image", command=self.count_pixels)
        pick_color.grid(row=1, column=2, columnspan=1)

        button_close = Button(self.color_window, text="Close", command=self.close_color_window)
        button_close.grid(row=2, column=2, columnspan=1)
    
    def draw_crop_rectangle(self):
        if not self.crop_rectangle:
            self.crop_rectangle = self.canvas.create_rectangle(int(self.start_x_str.get()), int(self.start_y_str.get()), int(self.end_x_str.get()), int(self.end_y_str.get()))
        else:
            self.canvas.coords(self.crop_rectangle, int(self.start_x_str.get()), int(self.start_y_str.get()), int(self.end_x_str.get()), int(self.end_y_str.get()))

    def crop_area(self):
        self.img = self.img.crop((int(self.start_x_str.get()), int(self.start_y_str.get()), int(self.end_x_str.get()), int(self.end_y_str.get())))
        self.canvas.delete("all")
        self.bg_tiles.clear()
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        self.canvas.config(scrollregion=(0,0,0,0))
        self.img_tk = None
        self.img_id = None
        self.render_image()

    def crop_area_dialog(self):
        self.crop_window = Toplevel()
        self.crop_window.title("Crop area")
        self.crop_window.attributes('-topmost', 'true')

        start_x = Label(self.crop_window, text="Start X:")
        start_x.grid(row=0, column=0, sticky=W)
        self.start_x_str = StringVar()
        self.start_x_str.set("0")
        self.start_x_entry = Entry(self.crop_window, textvariable=self.start_x_str)
        self.start_x_entry.grid(row=0, column=1)

        start_y = Label(self.crop_window, text="Start Y:")
        start_y.grid(row=1, column=0, sticky=W)
        self.start_y_str = StringVar()
        self.start_y_str.set("0")
        self.start_y_entry = Entry(self.crop_window, textvariable=self.start_y_str)
        self.start_y_entry.grid(row=1, column=1)

        end_x = Label(self.crop_window, text="End X:")
        end_x.grid(row=2, column=0, sticky=W)
        self.end_x_str = StringVar()
        self.end_x_str.set("0")
        self.end_x_entry = Entry(self.crop_window, textvariable=self.end_x_str)
        self.end_x_entry.grid(row=2, column=1)

        end_y = Label(self.crop_window, text="End Y:")
        end_y.grid(row=3, column=0, sticky=W)
        self.end_y_str = StringVar()
        self.end_y_str.set("0")
        self.end_y_entry = Entry(self.crop_window, textvariable=self.end_y_str)
        self.end_y_entry.grid(row=3, column=1)

        preview = Button(self.crop_window, text="Preview", command=self.draw_crop_rectangle)
        preview.grid(row=4, column=0, columnspan=2)

        crop = Button(self.crop_window, text="Create new image from crop area", command=self.crop_area)
        crop.grid(row=5, column=0, columnspan=2)

        button_close = Button(self.crop_window, text="Close", command=self.close_crop_window)
        button_close.grid(row=6, column=0, columnspan=2)

    def close_color_window(self):
        self.color_window.destroy()
        self.color_canvas = None
        self.color_label = None
        self.color_window = None
    
    def close_crop_window(self):
        self.crop_window.destroy()
        self.crop_window = None
        if self.crop_rectangle:
            self.canvas.delete(self.crop_rectangle)
        self.crop_rectangle = None

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
