#!/usr/bin/python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
import cairo
import numpy as np
import os
import sys
    
class Clasificador(Gtk.Window):

    def __init__(self):
        super(Clasificador, self).__init__()
        self.init_ui()
        
    def init_ui(self):
        self.set_border_width(10)
        #self.set_title("Clasificador")
        #self.maximize()
        self.set_focus_visible(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        toolbar = Gtk.Toolbar()
        
        self.darea = Gtk.DrawingArea()
        self.darea.set_size_request(640, 480)
        self.darea.connect("draw", self.on_draw)
        self.darea.set_events(Gdk.EventMask.KEY_PRESS_MASK | Gdk.EventMask.BUTTON_PRESS_MASK)    
        self.vbox.pack_end(self.darea, True, True, 0)
        
        self.add(self.vbox)
        self.show_all()
        
        self.connect("delete-event", Gtk.main_quit)
        self.connect("key-press-event", self.on_key_press)
        self.darea.connect("button-press-event", self.on_button_press)
        
        if len(sys.argv) > 1:
            path = sys.argv[1]
        else:
            path = "./"
        self.num = 0
        self.files = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path):
            for file in f:
                if '.png' in file:
                    self.files.append(os.path.join(r, file))
        self.files.sort()
        self.set_title(self.files[self.num])
        self.surf = cairo.ImageSurface.create_from_png(self.files[self.num])
        
        self.d_pulse = False
        self.i_pulse = False
        self.e_pulse = False
        
        self.pressed = 0
        self.left = 0
        self.right = 0
        self.top = 0
        self.bot = 0
        self.fall = 0
        self.elim = 0
   
    def on_draw(self, wid, cr):
        cr.set_source_surface(self.surf, 0, 0)
        cr.paint()
        
        name_txt = self.files[self.num][:-3]+"txt"
        file_txt = open(name_txt, "r")
        
        cr.set_line_width(1)
        for line in file_txt:
            fall, left, right, top, bot = line.split()
            fall = int(fall)
            left = int(left)
            right = int(right)
            top = int(top)
            bot = int(bot)
            if fall == 1:
                cr.set_source_rgb(1.0, 0.0, 0.0) #red
            elif fall == -1:
                cr.set_source_rgb(0.0, 1.0, 0.0) #green
            else:
                cr.set_source_rgb(0.0, 0.0, 1.0) #blue
            cr.move_to(left, top)
            cr.line_to(right, top)
            cr.stroke()
            cr.move_to(right, top)
            cr.line_to(right, bot)
            cr.stroke()
            cr.move_to(right, bot)
            cr.line_to(left, bot)
            cr.stroke()
            cr.move_to(left, bot)
            cr.line_to(left, top)
            cr.stroke()
        file_txt.close()

    def on_key_press(self, w, e):
        mod = Gtk.accelerator_get_label(e.keyval, e.state);
        if e.keyval == 65363: #right
            self.num +=1
            if self.num == len(self.files):
                self.num = 0
            self.surf = cairo.ImageSurface.create_from_png(self.files[self.num])
            self.set_title(self.files[self.num])
            self.elim = 0
            self.darea.queue_draw()
        elif e.keyval == 65361: #left
            self.num -=1
            if self.num < 0:
                self.num = len(self.files)-1
            self.surf = cairo.ImageSurface.create_from_png(self.files[self.num])
            self.set_title(self.files[self.num])
            self.elim = 0
            self.darea.queue_draw()
        elif e.keyval == Gdk.KEY_d:
            self.d_pulse = True
            self.i_pulse = False
            self.e_pulse = False
        elif e.keyval == Gdk.KEY_i:
            self.d_pulse = False
            self.i_pulse = True
            self.e_pulse = False
        elif e.keyval == Gdk.KEY_e:
            self.d_pulse = False
            self.i_pulse = False
            self.e_pulse = True
        elif e.keyval == Gdk.KEY_r:
            self.d_pulse = False
            self.i_pulse = False
            self.e_pulse = False
            if self.elim == 1:
                name_txt = self.files[self.num][:-3]+"txt"
                file_txt = open(name_txt, "a")
                file_txt.write("%d %d %d %d %d\n" % (self.fall, self.left, self.right, self.top, self.bot))
                self.darea.queue_draw()  
        elif e.keyval == Gdk.KEY_1:
            if self.d_pulse == True or self.i_pulse == True or self.e_pulse == True:
                self.key_num(0)
            self.d_pulse = False
            self.i_pulse = False
            self.e_pulse = False
        elif e.keyval == Gdk.KEY_2:
            if self.d_pulse == True or self.i_pulse == True or self.e_pulse == True:
                self.key_num(1)
            self.d_pulse = False
            self.i_pulse = False
            self.e_pulse = False
        elif e.keyval == Gdk.KEY_3:
            if self.d_pulse == True or self.i_pulse == True or self.e_pulse == True:
                self.key_num(2)
            self.d_pulse = False
            self.i_pulse = False
            self.e_pulse = False
        elif e.keyval == Gdk.KEY_4:
            if self.d_pulse == True or self.i_pulse == True or self.e_pulse == True:
                self.key_num(3)
            self.d_pulse = False
            self.i_pulse = False
            self.e_pulse = False
        elif e.keyval == Gdk.KEY_5:
            if self.d_pulse == True or self.i_pulse == True or self.e_pulse == True:
                self.key_num(4)
            self.d_pulse = False
            self.i_pulse = False
            self.e_pulse = False
        else:
            self.d_pulse = False
            self.i_pulse = False
            self.e_pulse = False
        self.pressed = 0
        return True #Para que no cambie el foco de los widget al pulsar teclas
        
    def key_num(self, num_line):
        name_txt = self.files[self.num][:-3]+"txt"
        file_txt = open(name_txt, "r")
        for i, line in enumerate(file_txt):
            if i == num_line:
                fall, left, right, top, bot = line.split()
                fall = int(fall)
                left = int(left)
                right = int(right)
                top = int(top)
                bot = int(bot)
                if self.d_pulse == True:
                    fall = 0
                elif self.i_pulse == True:
                    if fall == -1:
                        fall = 1
                    else:
                        fall = -1
                break
        file_txt.close()
        file_txt = open(name_txt, "r")
        lines = file_txt.readlines()
        if self.e_pulse == True:
            lines.pop(num_line)
            self.left = left
            self.right = right
            self.top = top
            self.bot = bot
            self.fall = fall
            self.elim = 1
        else:
            lines[num_line] = "%d %d %d %d %d\n" % (fall, left, right, top, bot)
        file_txt.close()
        file_txt = open(name_txt, "w")
        file_txt.writelines(lines)
        file_txt.close()
        self.darea.queue_draw()
        
    def on_button_press(self, w, e):
        if e.type == Gdk.EventType.BUTTON_PRESS and (e.button == 1 or e.button == 3):
            if self.pressed == 0:
                self.left = e.x
                self.pressed = 1
            elif self.pressed == 1:
                self.top = e.y
                self.pressed = 2
            elif self.pressed == 2:
                self.right = e.x
                self.pressed = 3
            else:
                self.bot = e.y
                self.pressed = 0                
                name_txt = self.files[self.num][:-3]+"txt"
                file_txt = open(name_txt, "a")
                if e.button == 1:
                    file_txt.write("1 %d %d %d %d\n" % (self.left, self.right, self.top, self.bot))
                else:
                    file_txt.write("-1 %d %d %d %d\n" % (self.left, self.right, self.top, self.bot))
                self.darea.queue_draw()  
    
def main():
    app = Clasificador()
    Gtk.main()
        
if __name__ == "__main__":    
    main()
