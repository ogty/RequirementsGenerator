import tkinter
from tkinter import ttk
import os


#ファイル・フォルダ名を取得してinsertする関数
def process_directory(parent, path):
    for p in os.listdir(path):
        abspath = os.path.join(path, p)
        child = tree.insert(parent, "end", text=p)
        if os.path.isdir(abspath):  #子要素がある場合は再帰呼び出し
            process_directory(child, abspath)


root = tkinter.Tk()
root.geometry("500x500")
#Treeview
tree = ttk.Treeview(root, height=500))
process_directory("", "C:\\Users\\dadad\\Desktop\\ovaas")
tree.pack()

root.mainloop()