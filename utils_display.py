tkinter = True

if tkinter:
    from tkinter.filedialog import askopenfilename, asksaveasfilename
    from tkinter.simpledialog import askstring
    from tkinter.messagebox import showinfo, showerror
    import tkinter as tk

    root = tk.Tk()
    root.withdraw()


def askstring_or_tk(message):
    if tkinter:
        return askstring("INPUT", message)
    else:
        return input(message)


def print_or_tk(message, type):
    if tkinter:
        if type == 'ERROR':
            showerror(type, message)
        elif type == "INFO":
            showinfo(type, message)
    else:
        print(f'{type} : {message}')
