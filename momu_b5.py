import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from datetime import datetime
import time
import os
import csv

sucursal = "momu_la_bola"

# IMPORTS
from momu_db_b5 import Database_Productos, TmpVent_Database, Clientes_Database, Venta_Database, Compras_Database, TmpCot_Database, Registros_Database, Cotizacion_Database, Reporte_Database
from modulo_venta import F_Venta, F_Cotizacion
from modulo_registro import F_Cotizaciones, F_Ventas
from modulo_inventario import F_Compras, F_Productos, L_Compras, F_Orden
from modulo_reporte import F_reportes
import re

# Inicializar bases de datos
productos_db = Database_Productos('productos_momu.db')
tmpVent_db = TmpVent_Database('tmpVent_momu.db')
tmpCot_db = TmpCot_Database("tmpCot_momu.db")
clien_db = Clientes_Database("clientes_momu.db")
venta_db = Venta_Database("ventas_momu.db")
cot_db = Cotizacion_Database("cotizaciones_momu.db")
compra_db = Compras_Database("compras_momu.db")
orden_db = Compras_Database("orden_momu.db")
reg_db = Registros_Database("registros_momu.db")
tmpR1_db = Venta_Database("tmpR1_momu.db")
tmpR2_db = Venta_Database("tmpR2_momu.db")
tmpI1_db = Compras_Database("tmpI1_momu.db")
tmpI2_db = Compras_Database("tmpI2_momu.db")
tmpI3_db = Compras_Database("tmpI3_momu.db")
tmpI4_db = Compras_Database("tmpI4_momu.db")
tmpI5_db = Compras_Database("tmpI5_momu.db")
reporte_db = Reporte_Database("reportes_momu.db")

#reg_db.insert(0, "Venta") 
#reg_db.insert(0, "Compra")
#reg_db.insert(0, "Cotizacion")


# reg_db.insert(0, "Orden")



# Autosave a backups 
hoy = datetime.today().strftime("%Y/%m/%d") 
today = datetime.today().strftime("%Y.%m.%d") 
dia = datetime.today().strftime("%d")

if dia == "14" or dia == "15" or dia == "16":
    c = 'mkdir -p ~/Documents/'+sucursal+'/backups/' + today
    os.system(c)
    d = 'cp *.db ~/Documents/'+sucursal+'/backups/' + today
    os.system(d) 

if dia == "1" or dia == "2" or dia == "3":
    c = 'mkdir -p ~/Documents/'+sucursal+'/backups/' + today
    os.system(c)
    d = 'cp *.db ~/Documents/'+sucursal+'/backups/' + today
    os.system(d) 

# Daily backup but yesterday's 
c = 'mkdir -p ~/Documents/'+sucursal+'/backups/hier'
os.system(c)
d = 'cp *.db ~/Documents/'+sucursal+'/backups/hier'
os.system(d) 



lista_productos = []
lista_claves = []
lista_total = []
for row in productos_db.fetch():
    lista_productos.append(row[1])
    lista_total.append(row[1])
for row in productos_db.fetch():
    lista_claves.append(row[0])
    lista_total.append(row[0])


class Clock(tkinter.Label):
    """ Class that contains the clock widget and clock refresh """
    def __init__(self, parent=None, seconds=True):

        tkinter.Label.__init__(self, parent)

        self.display_seconds = seconds
        if self.display_seconds:
            self.time     = time.strftime('%H:%M:%S')
        else:
            self.time     = time.strftime('%I:%M %p').lstrip('0')
        self.display_time = self.time
        self.configure(text=self.display_time, font = "AppleBraille 17")

        self.after(200, self.tick)


    def tick(self):
        """ Updates the display clock every 200 milliseconds """
        if self.display_seconds:
            new_time = time.strftime('%H:%M:%S')
        else:
            new_time = time.strftime('%I:%M %p').lstrip('0')
        if new_time != self.time:
            self.time = new_time
            self.display_time = self.time
            self.config(text=self.display_time, font = "AppleBraille 17")
        self.after(200, self.tick)

class AutocompleteEntry(tk.Entry):
    def __init__(self, autocompleteList, *args, **kwargs):

        # Listbox length
        if 'listboxLength' in kwargs:
            self.listboxLength = kwargs['listboxLength']
            del kwargs['listboxLength']
        else:
            self.listboxLength = 8

        self.parent = args[0]
        

        # Custom matches function
        if 'matchesFunction' in kwargs:
            self.matchesFunction = kwargs['matchesFunction']
            del kwargs['matchesFunction']
        else:
            def matches(fieldValue, acListEntry):
                pattern = re.compile(re.escape(fieldValue) + '.*', re.IGNORECASE)
                return re.match(pattern, acListEntry)
                
            self.matchesFunction = matches

        
        if 'function' in kwargs:
            self.function = kwargs['function']
            del kwargs['function']
        else:
            def null():
                pass
            self.function = null

        tk.Entry.__init__(self, *args, **kwargs)

        self.autocompleteList = autocompleteList
        
        self.var = self["textvariable"]     # var is whatever is in the entrybox
        if self.var == '':
            self.var = self["textvariable"] = tk.StringVar()

        self.var.trace('w', self.changed)       # mode? so if we write something it triggers this function 
        self.bind("<Right>", self.selection)    # to select it
        self.bind("<Up>", self.moveUp)          # self explanatory
        self.bind("<Return>", self.selection, add="+")
        self.bind("<Down>", self.moveDown)      # '' 
        # self.bind("<FocusIn>", self.focusIn)      # ''
        self.bind("<FocusOut>", self.focusOut)      # '' 
        self.showListbox = False                # The listbox isn't displayed at the beggining 
        self.listbox = tk.Listbox(width=self["width"], height=self.listboxLength)

    def changed(self, name, index, mode):
        if self.var.get() == '':                # if Entrybox is empty
            if self.showListbox:
                self.listbox.destroy()          # This is correct, we remove the listbox if there is nothing written
                self.showListbox = False
        else:   # If Entrybox not empty
            words = self.comparison()
            if words:
                if not self.showListbox:
                    self.listbox = tk.Listbox(self.parent, width=self["width"], height=self.listboxLength)
                    self.listbox.place(in_=self , x=-2, y=2, rely=1, relwidth=1.0, anchor="nw"  )         # por labelframe!!!!
                    self.showListbox = True
                
                self.listbox.delete(0, tk.END)
                for w in words:
                    self.listbox.insert(tk.END,w)

            else:
                if self.showListbox:
                    self.listbox.destroy()
                    self.showListbox = False
        
    def selection(self, event):         # This will make the selection of the desired word in the listbox
        if self.showListbox:    # Provided it is not empty
            self.var.set(self.listbox.get(tk.ACTIVE))  # We set the var of the entrybox to the one selected in the listbox
            self.listbox.destroy()      # destroy the listbox
            self.showListbox = False    # mark it as false
            self.icursor(tk.END)           # put the cursor at end of word inserted
    def click(self, event):
        if self.showListbox:
            if self.listbox.curselection() != ():
                self.var.set(self.listbox.get( self.listbox.curselection()[0]  ))  # We set the var of the entrybox to the one selected in the listbox
                self.listbox.destroy()      # destroy the listbox
                self.showListbox = False    # mark it as false
                self.icursor(tk.END)           # put the cursor at end of word inserted
                self.function()
    def moveUp(self, event):
        if self.showListbox:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]  
                
            if index != '0':                
                self.listbox.selection_clear(first=index)
                index = str(int(index) - 1)
                
                self.listbox.see(str(int(index) - 2)) # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)
    def moveDown(self, event):
        if self.showListbox:
            if self.listbox.curselection() == ():
                index = '0'
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)
            else:
                index = self.listbox.curselection()[0]
                
            if index != tk.END:                        
                self.listbox.selection_clear(first=index)
                if index != '0':
                    index = str(int(index) + 1)
                
                self.listbox.see(str(int(index) + 3)) # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index) 

    def comparison(self):
        return [ w for w in self.autocompleteList if self.matchesFunction(self.var.get(), w) ]

    def focusOut(self, *args):
        x = self.focus_get()
        if 'listbox' not in str(x):
            self.listbox.destroy()
            self.showListbox = False    # mark it as false
        else:
            self.listbox.bind("<Double-1>", self.click)
            self.listbox.bind("<ButtonRelease-1>", self.click)

    
    def focusIn(self, event):
        self.changed(self.var, self.index, 'w')
        # SELECT_RANGE(0, TK.END) possibly

# *** Root y frame ***
root = tk.Tk()
root.title('Aplicación MOMU')
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d" % (w, h))

f_root = tk.Frame(root)
f_root.grid()
f_root.focus_set()

#########################################################################################################################################################################

# nb styles
nb_style = ttk.Style(root)
nb_style.configure("nb.TNotebook", tabposition = "nw")
nb_style.configure('TNotebook.Tab', font = "AppleBraille 15")

# TEST NB_ALL
nb_all = ttk.Notebook(root, width = w-50, height = h-100, style="nb.TNotebook")
# *** notebook venta ***
f_venta = F_Venta(nb_all, Clock, AutocompleteEntry,hoy, lista_productos, lista_claves, lista_total, productos_db, tmpVent_db, tmpCot_db, clien_db, compra_db, venta_db, reg_db, cot_db)
f_cot = F_Cotizacion(nb_all, Clock, AutocompleteEntry,hoy, lista_productos, lista_claves, lista_total, productos_db, tmpVent_db, tmpCot_db, clien_db, compra_db, venta_db, reg_db, cot_db)

#*** notebook registro ***
f_ventas = F_Ventas(nb_all, AutocompleteEntry, hoy, lista_productos, lista_claves, lista_total, productos_db, venta_db, tmpR1_db, clien_db, sucursal)
f_cotizaciones = F_Cotizaciones(nb_all, AutocompleteEntry, hoy, lista_productos, lista_claves, lista_total, productos_db, cot_db, tmpR2_db, clien_db, venta_db, reg_db, f_cot)

# *** notebook inventario ***
f_compras = F_Compras(nb_all, AutocompleteEntry, hoy, lista_productos, lista_claves, lista_total, productos_db, compra_db, tmpI1_db, clien_db, reg_db, sucursal)
l_compras = L_Compras(nb_all, Clock, AutocompleteEntry, hoy, lista_productos, lista_claves, lista_total, productos_db, tmpVent_db, tmpCot_db, clien_db, compra_db, venta_db, reg_db, cot_db, tmpI3_db, orden_db)
f_orden = F_Orden(nb_all, AutocompleteEntry, hoy, lista_productos, lista_claves, lista_total, productos_db, reg_db, tmpI4_db, tmpI5_db, orden_db, compra_db, l_compras)
f_productos = F_Productos(nb_all, AutocompleteEntry, hoy, lista_productos, lista_claves, lista_total, productos_db, venta_db, compra_db, tmpI2_db, clien_db, reg_db)

# *** notebook reportes ***
f_reportes = F_reportes(nb_all, AutocompleteEntry, hoy, lista_productos, lista_claves, lista_total, venta_db, cot_db, productos_db, compra_db, clien_db, reg_db, reporte_db, sucursal)


nb_all.add(f_venta, text = "Ventas")
nb_all.add(f_cotizaciones, text = "Cotizaciones")
nb_all.add(f_ventas, text = "Historial Ventas")
nb_all.add(l_compras, text= "Lista de Compras")
nb_all.add(f_compras, text = "Historial Compras")
nb_all.add(f_orden, text = "Órdenes de Compra")
nb_all.add(f_productos, text = "Inventario")
nb_all.add(f_reportes, text = "Generar Reportes")

f_ventas.historial()
f_cotizaciones.historial()
f_productos.historial()
f_compras.historial()
f_orden.historial()

root.title('Aplicación MOMU')
root.focus_set()
nb_all.grid()

##########  NOTEBOOK FUNCTIONS ###############################################################################################################################################################
def on_tab_changed(event):
    tab = event.widget.tab('current')['text']
    if tab == 'Ventas':
        f_root.grid_remove()
        f_venta.ve_prod.focus_set()
        root.title("Ventas")
    elif tab == 'Historial Ventas':
        f_root.grid_remove()
        f_ventas.ve_numventa.focus_set()
        root.title("Historial Ventas")
    elif tab == 'Cotizaciones':
        f_root.grid_remove()
        f_cotizaciones.ve_numventa.focus_set()
        root.title("Cotizaciones")
    elif tab == 'Historial Compras':
        f_root.grid_remove()
        f_compras.ve_numventa.focus_set()
        f_compras.s_ncompra.set("No. de Compra: " + reg_db.numero("Compra"))
        root.title("Historial Compras")
    elif tab == 'Lista de Compras':
        f_root.grid_remove()
        l_compras.ve_prod.focus_set()
        l_compras.n_venta.set("No. Compra: " + reg_db.numero("Compra"))
        root.title("Lista de Compras")
    elif tab == 'Inventario':
        f_productos.historial()
        f_root.grid_remove()
        root.title("Inventario")
    elif tab == "Órdenes de Compra":
        f_root.grid_remove()
        root.title("Órdenes de Compra")
    else:
        f_root.grid_remove()
        root.title("Reportes")

        

nb_all.bind("<<NotebookTabChanged>>", on_tab_changed)



def on_closing():
    if tkinter.messagebox.askokcancel("Salir", "¿Segura que deseas salir? Se borrarán todas las cotizaciones no vendidas."):
        tmpVent_db.deleteall()
        tmpI3_db.deleteall()
        root.destroy()
        c = 'mkdir -p ~/Documents/momu_la_bola/backups/hier'
        os.system(c)
        d = 'cp *.db ~/Documents/momu_la_bola/backups/hier'
        os.system(d) 
    else:
        root.focus_set()

root.protocol("WM_DELETE_WINDOW", on_closing)


root.mainloop()

