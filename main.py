try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import FleetSim.MainMenu as MM


def main():
    print('main')
    root = tk.Tk()
    MM.main_menu_window(root)
    root.tk.mainloop()

if __name__=='__main__':
    main()
