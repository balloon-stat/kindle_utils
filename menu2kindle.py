#!/usr/bin/python
# -*- coding: utf-8 -*-

booklist = []
lib_directory = "/home/user/documents/library/"
mail2kindel = "./mail2kindle.py"

import os
import subprocess
import pygtk
import gtk

class TreeView(gtk.TreeView):
  def __init__(self, *args, **kwargs):
    gtk.TreeView.__init__(self, *args, **kwargs)
    self.col = gtk.TreeViewColumn('BookList', gtk.CellRendererText(), text=0)
    self.append_column(self.col)
    self.connect('button_press_event', self.on_button_press_event)

  def on_button_press_event(self, widget, event):
    path_at_pos = None
    if event.button == 1:
      path_at_pos = self.get_path_at_pos(int(event.x), int(event.y))
    if path_at_pos:
      path, col, rx, ry = path_at_pos
      book = booklist[path[0]]
      #os.remove(lib_directory + book + ".epub")
      #subprocess.Popen([mail2kindel, lib_directory + book + ".mobi"])
      liter = self.get_model().get_iter(path[0])
      print liter
      self.get_model().remove(liter)

class MainWindow(gtk.Window):
  def __init__(self, *args, **kwargs):
    gtk.Window.__init__(self, *args, **kwargs)
    # ショートカットキー(アクセラレータ)
    self.accelgroup = gtk.AccelGroup()
    self.add_accel_group(self.accelgroup)
    # メニュー項目
    self.item_quit = gtk.ImageMenuItem(gtk.STOCK_QUIT, self.accelgroup)
    self.menu_file = gtk.Menu()
    self.menu_file.add(self.item_quit)
    self.item_file = gtk.MenuItem('_File')
    self.item_file.set_submenu(self.menu_file)
    self.menubar = gtk.MenuBar()
    self.menubar.append(self.item_file)
    # ツリービュー
    self.treeview = TreeView(model=gtk.ListStore(str))
    self.treeview.set_rules_hint(True)  # 背景色のシマシマを付ける
    # ツリービュー向けスクロールウィンドウ
    self.sw = gtk.ScrolledWindow()
    self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    self.sw.add(self.treeview)  # 子にツリービューを指定してスクロール可能にする
    # レイアウト用コンテナ
    self.vbox = gtk.VBox()
    self.vbox.pack_start(self.menubar, expand=False, fill=False)
    self.vbox.pack_start(self.sw)
    # シグナル
    self.connect('delete_event', gtk.main_quit)
    self.item_quit.connect('activate', gtk.main_quit)
    # データ追加
    for book in booklist:
      self.treeview.get_model().append((book,))

    # ウィンドウ
    self.add(self.vbox)
    self.set_size_request(300, 300)

def createBooklist():
    for book in os.listdir(lib_directory):
        root, ext = os.path.splitext(book)
        if ext == ".epub":
            booklist.append(root)

def main():
    createBooklist()
    win = MainWindow()
    win.show_all()
    gtk.main()

if __name__ == '__main__':
    main()
