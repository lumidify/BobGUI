import tkinter as tk
root = tk.Tk()
label = tk.Label(root, text="Hello")
label.grid(row=0, column=0, sticky="nswe")
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.mainloop()
