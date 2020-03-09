#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROGRAMA PER ENVIAR IMATGES A UNA PANTALLA LCD CONNECTADA

    Utilitzant tcl, una finestra en pantalla completa s'envia
a la pantalla seleccionada. Una finestra s'obre en la pantalla
principal per controlar les imatges enviades.
"""

__author__ = "Marcos Pérez Aviñoa"
__email__ = "mperezav7@alumnes.ub.edu"

import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import os
import sys
import camwire
import imageio as io
from tplot import PlotWidget

class CommandWindow(tk.Frame):
    def __init__(self, master, resolution):
        tk.Frame.__init__(self, master)
        self.master = master
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("BW.TCheckbutton", foreground="black",
                background=self.master["bg"])
        self.master.title("HoloAi")
        self.cwd = os.getcwd()  # Directori actual
        self.loop = False       # Fes un bucle amb les imatges
        self.dt = 10            # ms d'espera entre imatge i imatge
        self.timeseries = "rec"
        self.nim = 0
        self.pausa = True
        self.current_im = 0
        self.cam = camwire.CamBus()     # Inicialitzo càmera
        self.frame = self.cam.capture_frame()
        self.frameTk = None
        self.rec = False
        self.nsingle = 0        # Nombre de captures simples

        # Text de selecció de carpeta
        self.text = tk.Label(self.master, text="Carpeta d'hologrames")
        self.text.grid(row=0, column=0, sticky=tk.W+tk.S)

        # Obro la finestra on mostrar la imatge
        self.lcd = ImageWindow(self.master, resolution)

        # Selecció de la carpeta on es troben les imatges
        self.carpeta = ttk.Button(self.master, text="Navega...",
                command=self.select_dir)
        self.carpeta.grid(row=1, column=0, sticky=tk.N)

        # Nom de les dades
        self.dades_label = tk.Label(self.master,
                                    text="Nom de la sèrie de dades")
        self.dades_label.grid(row=2, column=0, sticky=tk.E)
        self.dades_entry = ttk.Entry(self.master, width=8)
        self.dades_entry.insert(10, self.timeseries)
        self.dades_entry.grid(row=3, column=0, sticky=tk.N)

        # Checkbox per fer loops
        self.check_loop = ttk.Checkbutton(self.master, text="Loop",
                variable=self.loop, style="BW.TCheckbutton")
        self.check_loop.grid(row=4, column=0)

        # Visualització dels continguts de la carpeta, només imatges
        # compatibles.
        self.scrollbar = ttk.Scrollbar(self.master)
        self.scrollbar.grid(row=0, column=5, rowspan=4, sticky=tk.N+tk.S)
        self.listbox = tk.Listbox(self.master, width=40,
                                    yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        # Dibuix de la imatge en seleccionar-la
        self.listbox.bind("<<ListboxSelect>>", self.draw_image)
        self.listbox.grid(row=0, column=1, columnspan=4, rowspan=4,
                sticky=tk.E)

        # Caixa d'entrada del nombre de ms entre imatge i imatge
        self.entry_dt = ttk.Entry(self.master, width=8)
        self.entry_dt.insert(10, str(self.dt))
        self.entry_dt.grid(row=4, column=1)

        # Text de la caixa
        self.speed_txt = tk.Label(self.master, text="ms")
        self.speed_txt.grid(row=4, column=2, sticky=tk.W)

        # Botó de play, per passar les imatges, com a màxim, a la
        # velocitat determinada.
        self.play_bt = ttk.Button(text="Reprodueix", command=self.play_list)
        self.play_bt.grid(row=4, column=3)
        self.play_bt.bind("<Button-1>", self.ch_pause)

        # Captura simple. Captura una sola imatge independentment de
        # la sèrie que es pugui capturar. Poso un nom per defecte, amb
        # quatre xifres significatives (no crec que amb aquest mètode ningú
        # faci més de cent imatges una a una...
        self.single_bt = ttk.Button(text="Captura simple",
                            command=self.single_shot)
        self.single_bt.grid(row=4, column=4)

        ## VISTA DE LA CÀMERA
        # TODO
        self.cam_window = CamView(self.master, self.cam)

        # On Close
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def select_dir(self):
        # Seleccionem directori de treball, on es trobin les imatges
        self.cwd = tk.filedialog.askdirectory(initialdir=self.cwd)
        os.chdir(self.cwd)


        # Llistat d'imatges
        fnames = os.listdir()
        images = []
        for fname in fnames:
            if fname.endswith("png"):
                images.append(fname)
        images.sort()
        self.nim = len(images)

        # Afegim imatges a listbox
        self.listbox.delete(0, tk.END)  # Esborro el contingut actual
        for image in images:
            self.listbox.insert(tk.END, image)

    def draw_image(self, event):
        """Dibuixat de la imatge en la segona pantalla"""
        self.current_im = self.listbox.curselection()[0]
        imname = self.listbox.get(self.current_im)
        self.lcd.load_img(imname)

    def play_list(self):
        """Reprodueix les imatges del directori amb un temps d'espera,
        com a mínim, de self.dt"""
        # TODO implementar la funció de bucle en la carpeta

        # TODO netejar el codi de captura d'imatge
        if not self.pausa:
            if self.cam_window.rec:
                # Doble captura degut als dos frame buffers!
                self.cam_window.update()
                self.cam_window.update()
                frame = self.cam_window.im
                io.imwrite("{:s}/capture-{:06d}.png".format(self.timeseries,
                                                       self.current_im),frame)

            if self.current_im >= self.nim-1:
                if self.loop:
                    self.current_im = 0
                else:
                    self.ch_pause()
                    self.current_im -= 1
                    messagebox.showinfo(message="Captura finalitzada!",
                                    title="Captura finalitzada")

            self.current_im += 1
            nextim = self.listbox.get(self.current_im)

            self.lcd.load_img(nextim)
            self.after(self.entry_dt.get(), self.play_list)

    def single_shot(self):
        # Dispara i captura una única imatge.
        # FIXME: Comprova si continua funcionant be aixo...
        #self.ch_pause()
        #self.cam_window.update()
        #self.cam_window.update()
        frame = self.cam_window.im
        self.timeseries = self.dades_entry.get()
        io.imwrite("{:s}/single-{:06d}.png".format(self.timeseries,
                    self.nsingle), frame)
        self.nsingle += 1
        #self.ch_pause()

    def ch_pause(self, event=None):
        self.pausa = not self.pausa
        self.cam_window.rec = not self.cam_window.rec
        self.timeseries = self.dades_entry.get()

        # Creació de la carpeta de gravació
        try:
            os.mkdir(self.timeseries)
        except:
            pass

        if not self.pausa:
            self.play_bt["text"] = "Pausa"
            self.cam_window.sync(self.dt)
        else:
            self.play_bt["text"] = "Reprodueix"
            self.cam_window.unsync()
            self.cam_window.update()

    def on_close(self):
        self.cam.close()
        self.master.destroy()
        sys.exit(0)

class ImageWindow(tk.Toplevel):
    """Finestra per mostrar l'holograma. S'intenta obrir a la segona pantalla,
    suposant que es trobi a la dreta de la principal (en pixels), i en pantalla
    completa. Qualsevol imatge es reescalada a la mida de la pantalla LCD,
    tot ignorant-ne les proporcions.
    """
    def __init__(self, master, res):
        tk.Toplevel.__init__(self, master)
        self.title("Hologram")
        self.position = 0, 0
        self.r0 = 0, 0
        # Moc la finestra cap a la segona pantalla
        try:
            self.geometry("{:d}x{:d}+{:d}+{:d}".format(
                res[0], res[1], res[0] + res[0] // 2, 0))
        except:
            messagebox.showerror("Error", "Pantalla LCD no detectada.")
            master.destroy()
            raise
        self.attributes("-fullscreen", True)
        # Resolució de la pantalla LCD
        self.update_idletasks()
        self.w, self.h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.w = self.w - res[0]
        self.h = 768
        self.position = self.w//2, self.h//2
        self.image_tk = None

        # Etiqueta per on mostrar la imatge
        self.image_canvas = tk.Canvas(self, width=self.w, height=self.h)
        self.image_canvas.pack()

        # Desplacament de la imatge en el canvas.
        self.image_canvas.bind("<Button-1>", self.set_anchor)
        self.image_canvas.bind("<B1-Motion>", self.displace)

    def load_img(self, imname):
        """Carrega una imatge i mostra-la en l'etiqueta"""
        # Càrrega de la imatge amb la llibreria pillow
        image_pil = Image.open(imname)
        # Detecció de la resolució: si diferent de la de la pantalla,
        # se'n canvia la mida.
        iw, ih = image_pil.size
        if (iw != self.w) or (ih != self.h):
            image_pil = image_pil.resize((self.w, self.h))

        # Creació de la imatge Tk, tot desant una referència perquè no
        # desaparegui.
        self.image_tk = ImageTk.PhotoImage(image_pil)
        self.image_item = self.image_canvas.create_image(*self.position,
                image=self.image_tk)

    def set_anchor(self, event):
        """Coloco l'ancora del desplacament, el punt que ens servira com a
        referencia dels desplacaments, al punt directament a sota del ratoli
        """
        self.image_canvas.scan_mark(event.x, event.y)
        self.r0 = event.x, event.y  # Nou origen al punt on es fa clic.

    def displace(self, event):
        """Desplaco la imatge del canvas una quantitat diferencial respecte
        el punt d'anclatge. Un cop moguda, el punt d'anclatge s'actualitza a
        la darrera posicio del ratoli."""
        dx, dy = event.x-self.r0[0], event.y-self.r0[1]
        self.image_canvas.move(self.image_item, dx, dy)
        # Deso les noves coordenades de la imatge
        self.position = self.image_canvas.coords(self.image_item)
        # Colloco el nou punt de referencia
        self.set_anchor(event)

class CamView(tk.Toplevel):
    def __init__(self, master, cam):
        tk.Toplevel.__init__(self, master)
        self.title("CamView")
        self.geometry("800x600+300+300")
        self.w = 800
        self.h = 600
        self.ratio = 1
        self.cam = cam
        self.master = master
        self.frame = None
        self.im = None
        self.dt = 1 # ms
        self.rec = False
        self.iw, self.ih = 0, 0
        self.histogram = None
        self.hvisible = True
        self.bg = self.master["bg"]

        # Visor de la imatge
        self.camview = tk.Canvas(self, width=self.w, height=self.h)
        self.camview.pack(fill="both", expand=True)
        
        # Histograma
        self.pw, self.ph = self.w//5, self.h//5
        self.plwindow = PlotWidget(self.camview, w=self.pw, 
                h=self.ph, xmargin=3, ymargin=3)
        self.plwindow.configure(bg="gray")
        self.plid = self.camview.create_window((0, 0), 
                window=self.plwindow, anchor="nw",
                width=self.pw, height=self.ph, state="normal")
        self.current_plot = None
        self.update()

        # Redimensiona i adapta a la mida total de la finestra
        self.bind("<Configure>", self.on_resize)
        self.bind("<h>", self.toggle_hist)

    def update(self):
        self.im = self.cam.capture_frame()

        if not self.rec:
            image_pil = Image.fromarray(self.im >> 8)
            self.iw = image_pil.size[0]
            self.ih = image_pil.size[1]
            ratio = self.ih/self.iw

            #if (self.iw > self.w) or (self.ih > self.h):
            if (self.iw > self.w):
                self.iw = self.w
                self.ih = int(self.w*ratio)
                if self.ih > self.h:
                    self.ih = self.h
                    self.iw = int(self.w*ratio)
                image_pil = image_pil.resize((self.iw, self.ih))
            elif (self.ih > self.h):
                self.ih = self.h
                self.iw = int(self.w/ratio)
                if self.iw > self.w:
                    self.iw = self.w
                    self.ih = int(self.h/self.ratio)
                image_pil = image_pil.resize((self.iw, self.ih))
            self.frame = ImageTk.PhotoImage(image_pil)

            self.cam_image = self.camview.create_image(self.w//2, self.h//2,
                    image=self.frame)
            # Plotting the histogram
            self.histogram = np.histogram(self.im, bins=4096, range=(0, 65532))
            self.plwindow.delete_plot("all", preserve=False)
            self.current_plot = self.plwindow.add_plot(self.histogram[1][:-1],
                    self.histogram[0], fill="blue")
            if (self.im == 65532).any():
                self.plwindow.configure(bg="red")
            else:
                self.plwindow.configure(bg=self.bg)

            self.after(self.dt, self.update)

    def on_resize(self, event):
        # Canviant de mida la finestra
        self.w = self.winfo_width()
        self.h = self.winfo_height()
        # Canviant de mida el plot
        self.pw = self.w//5
        self.ph = self.h//5

        self.camview.config(width=self.w, height=self.h)
        self.plwindow.resize(self.pw, self.ph)
        self.camview.itemconfig(self.plid, width=self.pw, height=self.ph)

    def toggle_hist(self, event):
        if self.hvisible:
            self.camview.itemconfig(self.plid, state="hidden")
            self.hvisible = False
        else:
            self.camview.itemconfig(self.plid, state="normal")
            self.hvisible = True

    def sync(self, dt):
        self.dt = dt
        self.rec = True

    def unsync(self):
        self.dt = 1
        self.rec = False

def get_res():
    """Workaround"""
    root = tk.Tk()
    root.update_idletasks()
    root.attributes("-fullscreen", True)
    root.state("iconic")
    geometry = root.winfo_geometry()
    root.destroy()
    w, _= geometry.split("x")
    h, _, _ = _.split("+")
    return int(w), int(h)

if __name__ == "__main__":
    res = get_res()

    root = tk.Tk()
    app = CommandWindow(root, res)
    root.mainloop()
