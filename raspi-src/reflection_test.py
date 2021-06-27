import tkinter as tk
import random
import time

class MainButton(tk.Frame):
  def __init__(self, master, **kw):
    super().__init__(master, **kw)
    self.master = master
    self.defaultBackground = self["background"]
    self.startedBackground = "green"
    self.flashedBackground = "yellow"
    self.missedBackground = "red"
    self.command = self.start
    self["width"] = 400
    self["height"] = 270
    self["borderwidth"] = 5
    self["relief"] = "ridge"
    self.bind("<ButtonPress>", self.on_enter)

  def on_enter(self, e):
    self.command(e)

  def start(self, e):
    self.command = self.miss
    self["background"] = self.startedBackground
    interval_time = random.randint(2000, 5000)
    self.after(interval_time, self.flash)

  def miss(self, e):
    self.command = self.reset
    self["background"] = self.missedBackground

  def flash(self):
    self.command = self.result
    self["background"] = self.flashedBackground
    self.start_time = time.time()

  def result(self, e):
    stop_time = time.time()
    passed_time = stop_time - self.start_time
    print(passed_time)
    self.reset(e)

  def reset(self, e):
    self["background"] = self.defaultBackground
    self.command = self.start

class Application(tk.Frame):
  def __init__(self, master):
    super().__init__(master)
    self.master = master
    self.pack()
    self.create_widgets()

  def create_widgets(self):
    self.main_button = MainButton(self)
    self.main_button.pack(side="top")

    self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
    self.quit.pack(side="bottom")

root = tk.Tk()
root.title("反応速度")
root.geometry("400x300")
app = Application(master=root)
app.mainloop()