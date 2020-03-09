import tkinter as tk

class PlotWidget(tk.Canvas):
    """Plot widget. Manages a single axes and data"""
    def __init__(self, master, w, h, xmargin=20, ymargin=20):
        tk.Canvas.__init__(self, master, width=w, height=h)
        self.master = master
        self.w = w
        self.h = h
        self.plots = []

        # Margins of the plot
        self.xmargin = xmargin
        self.ymargin = ymargin

        # Drawing the rectangle bounding box of the plot
        self.idr = self.create_rectangle(self.xmargin, self.ymargin,
                self.w - self.xmargin, self.h - self.ymargin)

    def add_plot(self, xdata, ydata, fill="#000000"):
        np = len(xdata)
        # Consistency check
        if np != len(ydata):
            raise ValueError("x and y must have the same dimensions")

        # Making all values positive and scaling to the dimensions of the box
        data = [0] * np
        #ypos = [0] * np
        xmin = min(xdata)
        ymin = min(ydata)
        scx = (self.w - 2 * self.xmargin) / (max(xdata) - xmin) 
        scy = (self.h - 2 * self.ymargin) / (max(ydata) - ymin) 
        for i in range(np):
            xp = int((xdata[i] - xmin) * scx + self.xmargin)
            yp = self.h - int((ydata[i] - ymin) * scy + self.ymargin)
            data[i] = [xp, yp]
        # Plotting the points as a continuous line
        ids = self.create_line(*data, fill=fill)
        # Saving a reference to the object
        p = IdObj(ids, data)
        self.plots.append(p)
        return len(self.plots)-1 # id del plot en questio...

    def delete_plot(self, id_obj, preserve=True):
        """Delete the plot pointed by id_obj"""
        if id_obj == "all":
            self.delete("all")
            if not preserve:
                self.plots = []
        else:
            obj = self.plots[id_obj]
            id0 = obj.ids
            nobj = obj.np
            self.delete(i)
            # Finally, deleting the reference to the object.
            if not preserve:
                self.plots.remove(obj)
    
    def resize(self, w, h):
        """Changes the size of the plotting region."""
        # First, changing the canvas' size
        self.w = w
        self.h = h
        self.config(width=self.w, height=self.h)
        # Now, changing the boundary box
        self.coords(self.idr, self.xmargin, self.ymargin, 
                self.w - self.xmargin, self.h - self.ymargin)
        # Replotting if necessary
        if self.plots:
            p_old = self.plots.copy()
            self.delete_plot("all", preserve=False)
            for obj in self.plots:
                self.add_plot(obj.xdata, obj.ydata)

class TPlot:
    """Plotter class. Manages window and plots"""
    def __init__(self, w, h):
        self.master = tk.Tk()
        self.w, self.h = w, h
        self.plt = PlotWidget(self.master, self.w, self.h)
        self.plt.pack()

    def plot(self, xdata, ydata):
        p = self.plt.add_plot(xdata, ydata)
        return p
    def show(self):
        self.master.mainloop()
    def delete(self, ids):
        self.plt.delete_plot(ids)

class IdObj:
    """Object to contain the id of the lines created, equivalent to
    knowing the ids of all the lines contained in a plot."""
    def __init__(self, ids, data):
        self.ids = ids
        self.data = data
