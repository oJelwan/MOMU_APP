# 2344
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from datetime import datetime
import time
import os
import csv

from modulo_registro import F_Ventas, F_Cotizaciones
from modulo_venta import F_Venta

class F_Compras(F_Ventas):   
    def __init__(self, root,  AutocompleteEntry, hoy, lista_productos, lista_claves, lista_total, productos_db, compra_db, tmpI1_db, clien_db, reg_db, *args, **kwargs):
        super().__init__(root,  AutocompleteEntry, hoy, lista_productos, lista_claves, lista_total, productos_db, compra_db, tmpI1_db, clien_db, *args, **kwargs)


        # Pequeños ajustes a parent class
        self.venta_db = compra_db
        self.tmpI1_db = tmpI1_db
        self.reg_db = reg_db

        self.labels = ("No. Compra", "Fecha", "(AAAA/MM/DD)", "Clave", "Producto", "Proveedor", "                     ")
        
        x = 1
        for l in self.labels:
            l = tk.Label(self.vf_filtros, text = l, font = "AppleGothic")
            l.grid(row = x, column = 0, pady = 3, padx = 5, sticky = tk.W)
            x += 1
        self.vf_fpago.grid_remove()
        self.lol.grid_remove()

        
        self.if_botones = tk.Frame(self.vf_filtros)
        self.if_botones.grid(row = 7, column = 1)

        self.vb_filtrar = tk.Button(self.if_botones, text = "Filtrar", width = 8, height = 1, fg = "green", font = "AppleGothic 15", command = self.filtrar)
        self.vb_filtrar.grid(row = 0, column = 0, pady = 8, sticky = tk.W)
        self.vb_limpiar = tk.Button(self.if_botones, text = "Limpiar", width = 8, height = 1, fg = "red", font = "AppleGothic 15", command = self.limpiar)
        self.vb_limpiar.grid(row = 0, column = 1, pady = 8, sticky = tk.E)
        self.ib_historial = tk.Button(self.vf_filtros, text = "Historial", width = 8, height = 1, fg = "black", font = "AppleGothic 15", command = self.historial)
        self.ib_historial.grid(row = 7, column = 0, pady = 8, sticky = tk.W, padx = 8)
        self.vb_historial.grid_remove()

        self.vf_trees.grid_remove()
        self.vb_expd.grid_remove()
        self.vb_red.grid_remove()

        self.ve_cliente.grid_remove()
        self.ie_prov = tk.Entry(self.vf_filtros)
        self.ie_prov.grid(row = 6, column = 1)



        self.vt_registro = ttk.Treeview(self.prueba, height = 8, columns=("#1","#2","#3","#4", "#5", "#6", "#7", "#8"), style = "mystyle.Treeview")
        self.vt_registro.grid(row = 4, column = 0,  columnspan = 8, pady = 20, padx = 20, sticky = tk.W + tk.S)
        self.vt_registro.heading("#0", text = "Fecha")
        self.vt_registro.column("#0", width = 120, minwidth = 120)
        self.vt_registro.heading("#1", text = "No. Compra")
        self.vt_registro.column("#1", width = 100, minwidth = 100)
        self.vt_registro.heading("#2", text = "Clave")
        self.vt_registro.column("#2", width = 70, minwidth = 70)
        self.vt_registro.heading("#3", text = "Producto")
        self.vt_registro.column("#3", width = 200, minwidth = 200)
        self.vt_registro.heading("#4", text = "Precio/u")
        self.vt_registro.column("#4", width = 100, minwidth = 100)
        self.vt_registro.heading("#5", text = "Cantidad")
        self.vt_registro.column("#5", width = 80, minwidth = 80)
        self.vt_registro.heading("#6", text = "Total")
        self.vt_registro.column("#6", width = 70, minwidth = 70)
        self.vt_registro.heading("#7", text = "Proveedor")
        self.vt_registro.column("#7", width = 100, minwidth = 100)
        self.vt_registro.heading("#8", text = "Notas")
        self.vt_registro.column("#8", width = 300, minwidth = 300)
        self.vt_registro.bind("<Double-1>", self.ac)

        # Label historial
        self.is_info = tk.StringVar()
        self.il_info = tk.Label(self.prueba, textvariable = self.is_info, font = "AppleBraille 15" )
        self.il_info.grid(row = 5, column = 6 , columnspan = 2,   sticky = tk.N)


        # Nueva compra
        self.if_compra = tk.LabelFrame(self.prueba, text = "Compra", font = "AppleGothic 18")
        self.if_compra.grid(row = 0, column = 4, rowspan = 4, columnspan = 4, sticky = tk.N )

        self.label_i = ("Fecha (AAAA/MM/DD)", "Clave", "Producto", "Precio Unitario", "Cantidad de Compra", "Total de Compra")

        x = 1
        for l in self.label_i:
            tk.Label(self.if_compra, text = l, font = "AppleGothic").grid(row = x, column = 0, pady = 2, padx = 10, sticky = tk.W)
            x += 1

        self.il_prov = tk.Label(self.if_compra, text = "Proveedor", font = "AppleGothic")
        self.il_prov.grid(row = 7, column = 0)

        # Fecha
        self.ie_fecha = tk.Entry(self.if_compra, textvariable = hoy)
        self.ie_fecha.insert(0, hoy)
        self.ie_fecha.grid(row = 1, column = 1,sticky = tk.W  )

        # Clave y producto
        self.ie_clave = AutocompleteEntry(self.lista_claves, self.if_compra, function =  self.clave_producto_validate1)
        self.ie_clave.grid(row = 2, column = 1, sticky = tk.W  )
        self.ie_clave.bind("<Return>", self.clave_prod_tmp, add="+") 
        self.ie_prod = AutocompleteEntry(self.lista_productos, self.if_compra, function = self.producto_clave_validate1)
        self.ie_prod.grid(row = 3, column = 1, sticky = tk.W  )
        self.ie_prod.bind("<Return>", self.prod_clave_tmp, add="+")

        # Precio unitario y cantidad y total
        self.i_compra = tk.StringVar()
        self.ie_punitario = tk.Entry(self.if_compra, validate="focusout", validatecommand = self.total_validate)
        self.ie_punitario.grid(row = 4, column = 1, sticky = tk.W  )

        self.ie_cant = tk.Entry(self.if_compra, validate="focusout", validatecommand = self.total_validate)
        self.ie_cant.grid(row = 5, column = 1, sticky = tk.W  )

        self.ie_total = tk.Label(self.if_compra, textvariable = self.i_compra, font = "AppleBraille 15")
        self.ie_total.grid(row = 6, column = 1, sticky = tk.W  )

        # Proveedor y notas
        self.ie_prov2 = tk.Entry(self.if_compra)
        self.ie_prov2.grid(row = 7, column = 1, sticky = tk.W  )

        self.il_notas = tk.Label(self.if_compra, text = "Notas", font = "AppleGothic")
        self.il_notas.grid(row = 4, column = 2, sticky = tk.E)

        self.it_notas = tk.Text(self.if_compra, width = 20, height = 4, wrap = tk.WORD, highlightthickness = 1, borderwidth = 1, fg = "black", font = "AppleGothic")
        self.it_notas.grid(row = 4, column = 3, padx = 6, rowspan = 2,  sticky = tk.W )

        # Botón compra y label compra
        self.ib_compra = tk.Button(self.if_compra, text = "Compra", font= "AppleGothic", width = 9, height = 1, command = self.compra) 
        self.ib_compra.grid(row = 6, column = 3, pady = 20, sticky = tk.W)

        self.s_ncompra = tk.StringVar()
        self.s_ncompra.set("No. de Compra: " + reg_db.numero("Compra"))
        self.il_ncompra = tk.Label(self.if_compra, textvariable = self.s_ncompra, font = "AppleBraille 14")
        self.il_ncompra .grid(row = 1, column = 2, sticky = tk.E)

        # Ajustar compra
        self.ib_ajustar = tk.Button(self.prueba, text = "Ajustar Compra", width = 15, height = 2, font = "AppleBraille", command =  self.ajustar_compra)
        self.ib_ajustar.grid(row = 5, column = 1, sticky = tk.W)

    def historial(self):
        self.limpiar()
        self.vre_Total = 0
        self.vre_Cant = 0
        for row in self.venta_db.inverse_fetch():
            self.vt_registro.insert("", "end", text = row[0], values =("No. " + str(row[1]), row[2], row[3], "$" + str(row[4]), row[5], "$" + str(row[6]), row[7], row[8]))
            self.vre_Total += row[6]
            self.vre_Cant += row[5]
        self.is_info.set("Productos totales: %s     Total en Dinero: $%s" % (round(self.vre_Cant, 3), round(self.vre_Total, 3)))
    ##### observar ####   
    def filtrar(self):
     # Variables
        self.is_info.set("--")
        self.vre_Cant = 0
        self.vre_Total = 0
     # 0. Borrar nuestra db provisional
        self.limpiar()
     # 1. No. Venta
        try:
            self.ve_numventa.get()[0]
            for row in self.venta_db.fetch():
                if str(row[1]) == self.ve_numventa.get():
                    self.tmpI1_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
            self.paint()
            return
        except:
            pass
     # 2. Fecha
        if self.intervalo.get() != 0:
            try:  # we'll just simply try to convert the string to a Python datetime and see if it fails
                datetime.strptime(self.ve_fecha.get(), '%Y/%m/%d')
            except ValueError:
                tkinter.messagebox.showerror("Error", "Error, la fecha tiene que estar en el formato correcto (AAAA/MM/DD), por favor.")
                self.focus_set()
                self.ve_fecha.focus_set()
                return  
        # 2.1 x Día
        if self.intervalo.get() == 1:
            dia_db = ""
            for row in self.venta_db.fetch():
                dia_db = dia_db + str(row[0][0])    # Tiene que ser el día del mismo mes y año
                dia_db = dia_db + str(row[0][1])
                dia_db = dia_db + str(row[0][2])
                dia_db = dia_db + str(row[0][3])
                dia_db = dia_db + str(row[0][4])
                dia_db = dia_db + str(row[0][5])
                dia_db = dia_db + str(row[0][6])
                dia_db = dia_db + str(row[0][7])
                dia_db = dia_db + str(row[0][8])
                dia_db = dia_db + str(row[0][9])
                if dia_db == self.ve_fecha.get():
                    self.tmpI1_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                dia_db = ""
        # 2.2 x Semana ******* VER DESPUÉS
        # 2.3 x Mes
        elif self.intervalo.get() == 3:
            mes_db = []
            mes_e = []
            mes_e.append(self.ve_fecha.get()[0])
            mes_e.append(self.ve_fecha.get()[1])
            mes_e.append(self.ve_fecha.get()[2])
            mes_e.append(self.ve_fecha.get()[3])
            mes_e.append(self.ve_fecha.get()[4])
            mes_e.append(self.ve_fecha.get()[5])
            mes_e.append(self.ve_fecha.get()[6])
            for row in self.venta_db.fetch():
                mes_db.append(row[0][0])    # Coincidir mes y año
                mes_db.append(row[0][1])
                mes_db.append(row[0][2])
                mes_db.append(row[0][3])
                mes_db.append(row[0][4])
                mes_db.append(row[0][5])
                mes_db.append(row[0][6])
                if mes_db == mes_e:
                    self.tmpI1_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                mes_db = []
        # 2.4 x Año
        elif self.intervalo.get() == 4:
            año_db = []
            año_e = []
            año_e.append(self.ve_fecha.get()[0])
            año_e.append(self.ve_fecha.get()[1])
            año_e.append(self.ve_fecha.get()[2])
            año_e.append(self.ve_fecha.get()[3])
            for row in self.venta_db.fetch():
                año_db.append(row[0][0])
                año_db.append(row[0][1])
                año_db.append(row[0][2])
                año_db.append(row[0][3])
                if año_db == año_e:
                    self.tmpI1_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                año_db = []
     # 3. Clave
        try:
            # Revisar que nada esté vacío
            self.ve_clave.get()[0]  
            try:
                self.tmpI1_db.fetch()[0]    # Ver si ya hay algo
                for row in self.tmpI1_db.fetch():
                    if row[2].lower() != self.ve_clave.get().lower():
                        self.tmpI1_db.remove_product(row[2])

            except: # Si no, usar la de ventas
                for row in self.venta_db.fetch():
                    if row[2].lower() == self.ve_clave.get().lower():
                        self.tmpI1_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])

        except:
            pass
     # 4. Producto
        try:
            # Revisar que nada esté vacío
            self.ve_producto.get()[0]  
            try:
                self.tmpI1_db.fetch()[0]    # Ver si ya hay algo
                for row in self.tmpI1_db.fetch():
                    if row[3].lower() != self.ve_producto.get().lower():
                        self.tmpI1_db.remove_product(row[2])
                        
            except: # Si no, usar la de ventas
                for row in self.venta_db.fetch():
                    if row[3].lower() == self.ve_producto.get().lower():
                        self.tmpI1_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])

        except:
            pass
     # 5. Proveedor
        try:
            # Revisar que nada esté vacío
            self.ie_prov.get()[0]  
            try:
                self.tmpI1_db.fetch()[0]    # Ver si ya hay algo
                for row in self.tmpI1_db.fetch():
                    if row[7].lower() != self.ie_prov.get().lower():
                        self.tmpI1_db.remove(row[1])
                        
            except: # Si no, usar la de ventas
                for row in self.venta_db.fetch():
                    if str(row[7]).lower() == self.ie_prov.get().lower():
                        self.tmpI1_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])

        except:
            pass
     # Paint
        self.paint()
        self.is_info.set("Total de artículos: %s. Total de dinero: $%s" % (round(self.vre_Cant, 3), round(self.vre_Total, 3)))
    ##### observar ####   
    def paint(self):
        try:
            for row in self.tmpI1_db.inverse_fetch():
                self.vt_registro.insert("", "end", text = row[0], values =("No. " + str(row[1]), row[2], row[3], "$" + str(row[4]), row[5], "$" + str(row[6]), row[7], row[8]))
                self.vre_Total += row[6]
                self.vre_Cant += row[5]
            self.is_info.set("Productos totales: %s       Total en Dinero: $%s" % (round(self.vre_Cant, 3), round(self.vre_Total, 3)))
        except:
            pass
    def limpiar(self):
        self.tmpR1_db.deleteall()
        for p in self.vt_registro.get_children():
            self.vt_registro.delete(p)
        for p in self.vt_selec.get_children():
            self.vt_selec.delete(p)
        self.vs_selec.set("")
        self.is_info.set("                                                      ")
    def total_validate(self):
        try:
            self.i_compra.set("$" + str(round(float(float(self.ie_punitario.get()) * float(self.ie_cant.get())), 3)))
            return True
        except:
            return True
    def clave_producto_validate1(self):
        for row in self.productos_db.fetch():
            if row[0] == self.ie_clave.get():    
                self.ie_prod.delete(0, tk.END)
                self.ie_prod.insert(0, row[1])
                self.ie_prod.focusOut()
    def producto_clave_validate1(self):
        for row in self.productos_db.fetch():
            if row[1] == self.ie_prod.get():    
                self.ie_clave.delete(0, tk.END)
                self.ie_clave.insert(0, row[0])
                self.ie_clave.focusOut()
    def borrar(self):
        entrys = (self.ie_clave, self.ie_prod, self.ie_fecha, self.ie_cant, self.ie_punitario, self.ie_prov2)
        for e in entrys:
            e.delete(0, tk.END)
        self.it_notas.delete("1.0", tk.END)
        self.i_compra.set("")
    def listas(self):   
        # Ajustar para el autocomplete
        for row in self.productos_db.fetch():
            self.lista_productos.append(row[1])
            self.lista_total.append(row[1])
    
        for row in self.productos_db.fetch():
            self.lista_claves.append(row[0])
            self.lista_total.append(row[0])
    def compra(self):

        entrys = (self.ie_clave, self.ie_prod, self.ie_fecha, self.ie_cant, self.ie_punitario, self.ie_prov2) # Todos son requeridos exepto las notas.
        for e in entrys:
            if len(e.get()) == 0:
                tkinter.messagebox.showerror("Error", "Error, no puedes dejar ningún campo vacío.")
                self.ie_clave.focus_set()
                return
        try:  # we'll just simply try to convert the string to a Python datetime and see if it fails
            datetime.strptime(self.ie_fecha.get(), '%Y/%m/%d')
        except ValueError:
            tkinter.messagebox.showerror("Error", "Error, la fecha tiene que estar en el formato correcto, por favor.")
            self.ie_fecha.focus_set()
            return

        
        try:
            float(self.ie_cant.get())
            float(self.ie_punitario.get())
        except:
            tkinter.messagebox.showerror("Error", "Los campos de cantidad y precio tienen que ser números")
            self.ie_punitario.focus_set()
            return

        p_nuevo = True     # Ver si es producto nuevo y hay que agregar a self.productos_db, con los campos de especial etc en 0. 
        for row in self.productos_db.fetch():
            if row[0] == self.ie_clave.get() and row[1].lower() == self.ie_prod.get().lower(): # Si ya existe, ajustar stock
                self.productos_db.update(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], round(row[8]+ float(self.ie_cant.get()), 3), row[9])
                p_nuevo = False
                s_t = round(row[8]+ float(self.ie_cant.get()), 3)
            elif row[0] == self.ie_clave.get() or row[1].lower() == self.ie_prod.get().lower(): #   NO SE PUEDE TENER MISMO NOMBRE PERO DIFERENTE CLAVE E INVERSA   
                tkinter.messagebox.showerror("Error", "No puedes agregar un producto existente con clave nueva o la inversa.")
                self.ie_clave.focus_set()
                return

        if p_nuevo: # Si es nuevo lo agregamos a la base de datos de productos, con los precios a cotizar!!!
            self.productos_db.insert(self.ie_clave.get(), self.ie_prod.get(), 0, 0, 0, 0, 0, 0, round(float(self.ie_cant.get()), 3), "")
            s_t = round(float(self.ie_cant.get()), 3)

        n_c = self.reg_db.accion("Compra")
        # Agregamos la compra a la compras db
        self.i_compra.set(round(float(float(self.ie_punitario.get()) * float(self.ie_cant.get())), 3))
        self.venta_db.insert(self.ie_fecha.get(),n_c ,self.ie_clave.get(), self.ie_prod.get(), self.ie_punitario.get(), self.ie_cant.get(),float(self.i_compra.get()) , self.ie_prov2.get(), self.it_notas.get("1.0", tk.END))

        self.i_compra.set("")
        self.it_notas.delete("1.0", tk.END)
        self.borrar()
        self.listas()
        self.historial()
        self.ie_fecha.insert(0, self.hoy)
        self.s_ncompra.set("No. de Compra: " + self.reg_db.numero("Compra"))
        #F_Productos.historial()
    def ajustar_compra(self):
        
        def t_v():
            try:
                iw_t.set("$" + str(round(float(float(iw_precio.get()) * float(iw_cantidad.get())), 3)))
                return True
            except:
                return True
        
        # Nueva ventana
        iw = tk.Toplevel(self)
        iw.title("Ajustar Compra")
        iw.transient(self) #set to be on top of the main window
        iw.grab_set() #hijack all commands from the master (clicks on the main window are ignored)
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        x = w/4
        y = h/5
        iw.geometry("+%d+%d" % (x, y))

        # Labels
        tk.Label(iw, text = "Ajustar Compra", font = "AppleBraille 20").grid(row = 0, column = 0, padx = 5, sticky = tk.W)
        tk.Label(iw, text = "Actual", font = "AppleGothic 16").grid(row = 1, column = 1, padx = 8, sticky = tk.W)
        tk.Label(iw, text = "Ajustar", font = "AppleGothic 16").grid(row = 1, column = 2, padx = 8, sticky = tk.W)

        label = ("Fecha:", "No. Compra:", "Clave:", "Producto:", "Precio Unitario:", "Cantidad:", "Total:", "Proveedor:", "Notas:")
        a = 2
        for l in label:
            tk.Label(iw, text = l, font = "AppleGothic").grid(row = a, column = 0, padx = 10, sticky = tk.W)
            a += 1

        # Get selected compra
        self.registro = self.vt_registro.item(self.vt_registro.selection())["values"][1]
        for c in self.venta_db.fetch():
            if c[2] == self.registro:
                compra = c

        b = 2
        for c in compra:
            if b == 8 or b == 6:
                tk.Label(iw, text = "$"+str(c), font = "AppleGothic").grid(row = b, column = 1, sticky = tk.W)      
            else:
                tk.Label(iw, text = c, font = "AppleGothic").grid(row = b, column = 1, sticky = tk.W)      
            b += 1
            if b == 10:
                break
        tk.Label(iw, text = compra[1], font = "AppleGothic").grid(row = 3, column = 2, sticky = tk.W)
        nota = tk.Text(iw, width = 20, height = 4, wrap = tk.WORD, highlightthickness = 1, borderwidth = 1, fg = "black", font = "AppleGothic")
        nota.grid(row = 10, column = 1, sticky = tk.W, rowspan = 2, pady = 5)
        nota.insert("1.0", compra[8])
        nota.config(state="disabled")

        # Ajustar fecha
        iw_fecha = tk.Entry(iw)
        iw_fecha.grid(row = 2, column = 2)
        iw_fecha.insert(0, compra[0])
        # Ajustar clave
        iw_clave = tk.Entry(iw)
        tk.Label(iw, text = compra[2], font = "AppleGothic").grid(row = 4, column = 2, sticky = tk.W)      
        #iw_clave.grid(row = 4, column = 2)
        iw_clave.insert(0, compra[2])
        # Ajustar producto
        iw_producto = tk.Entry(iw)
        tk.Label(iw, text = compra[3], font = "AppleGothic").grid(row = 5, column = 2, sticky = tk.W)      
        #iw_producto.grid(row = 5, column = 2)
        iw_producto.insert(0, compra[3])
        # Ajustar precio
        iw_precio = tk.Entry(iw, validate = "focusout", validatecommand= t_v)
        iw_precio.grid(row = 6, column = 2)
        iw_precio.insert(0, compra[4])
        # Ajustar cantidad
        iw_cantidad = tk.Entry(iw, validate = "focusout", validatecommand= t_v)
        tk.Label(iw, text = compra[5], font = "AppleGothic").grid(row = 7, column = 2, sticky = tk.W)      
        #iw_cantidad.grid(row = 7, column = 2)
        iw_cantidad.insert(0, compra[5])
        # Total string
        iw_t = tk.StringVar()
        iw_total = tk.Label(iw, textvariable = iw_t, font = "Applegothic")
        iw_total.grid(row = 8, column = 2)
        iw_t.set("$" + str(compra[6]))
        # Ajustar proveedor
        iw_proveedor = tk.Entry(iw)
        iw_proveedor.grid(row = 9, column = 2)
        iw_proveedor.insert(0, compra[7])
        # Ajustar nota
        iw_nota = tk.Text(iw, width = 20, height = 4, wrap = tk.WORD, highlightthickness = 1, borderwidth = 1, fg = "black", font = "AppleGothic")
        iw_nota.grid(row = 10, column = 2, rowspan = 2, pady = 5)
        iw_nota.insert("1.0", compra[8])
        # Botones: cerrar, eliminar, ajustar
        iw_cerrar = tk.Button(iw, text = "Cerrar", font = "AppleGothic", width = 10, height = 1, command = lambda: cerrar())
        iw_cerrar.grid(row = 12, column = 0)
        iw_eliminar = tk.Button(iw, text = "Eliminar", font = "AppleGothic", width = 10, height = 1, command = lambda: eliminar_compra())
        iw_eliminar.grid(row = 12, column = 1)
        iw_ajustar = tk.Button(iw, text = "Ajustar", font = "AppleGothic", width = 10, height = 1, command = lambda: ajustar())
        iw_ajustar.grid(row = 12, column = 2)

        iw.protocol("WM_DELETE_WINDOW", lambda: cerrar())

        def ajustar():
            try:  # we'll just simply try to convert the string to a Python datetime and see if it fails
                datetime.strptime(iw_fecha.get(), '%Y/%m/%d')
            except ValueError:
                tkinter.messagebox.showerror("Error", "Error, la fecha tiene que estar en el formato correcto (AAAA/MM/DD), por favor.")
                iw.focus_set()
                iw_fecha.focus_set()
                return  

            try:
                #float(iw_cantidad.get())
                float(iw_precio.get())
            except:
                tkinter.messagebox.showerror("Error", "Los campos de cantidad y precio tienen que ser números")
                iw_precio.focus_set()
                return

            entrys = (iw_fecha,  iw_precio, iw_proveedor)
            for e in entrys:
                if len(e.get()) == 0:
                    tkinter.messagebox.showerror("Error", "Error, no puedes dejar ningún campo vacío.")
                    self.ie_clave.focus_set()
                    return
            # Update, PELIGROSO STOOOOCK
            self.venta_db.updateu(iw_fecha.get(), compra[1], compra[2], compra[3], iw_precio.get(), compra[5], round(float(float(iw_precio.get()) * float(compra[5])), 3), iw_proveedor.get(), iw_nota.get("1.0", tk.END))
            cerrar()
        #  PELIGROSOOOOO, NEGATIVOS EN STOCK POR VENDER ALGUNOS Y QUE SE DESCUENTEN DEMÁS   
        def eliminar_compra():
            #if tkinter.messagebox.showerror("Eliminar Compra", "¿Segura que deseas eliminar esta compra? Se descontará todo el stock agregado por la compra y será irreversible."):
            pass
        def cerrar():
            iw.grab_release()
            iw.destroy()
            self.focus_set()
            self.historial()
    def ac(self, event):
        self.ajustar_compra()
    def clave_prod_tmp(self, event):
        self.clave_producto_validate1()
    def prod_clave_tmp(self, event):
        self.producto_clave_validate1()

class L_Compras(F_Venta):
    def __init__(self, root, Clock, AutocompleteEntry, hoy, lista_productos, lista_claves, lista_total, productos_db, tmpVent_db, tmpCot_db, clien_db, compra_db, venta_db, reg_db, cot_db, tmpI3_db, orden_db, *args, **kwargs):
        super().__init__( root, Clock, AutocompleteEntry, hoy, lista_productos, lista_claves, lista_total, productos_db, tmpVent_db, tmpCot_db, clien_db, compra_db, venta_db, reg_db, cot_db, *args, **kwargs)

        self.tmpI3_db = tmpI3_db
        # self.tmpI5_db = tmpI5_db
        self.orden_db = orden_db

        # Algunos ajustes estilisticos
        self.n_venta.set("No. Compra: " + self.reg_db.numero("Compra"))

        self.vt_tabla = ttk.Treeview(self, height = 15, columns=("#1","#2","#3","#4", "#5", "#6"), style = "mystyle.Treeview")
        self.vt_tabla.grid(row = 1, column = 0, padx = 7, pady = 10, columnspan = 4, sticky = tk.W + tk.E)
        self.vt_tabla.heading("#0", text = "Clave")
        self.vt_tabla.column("#0", width = 50, minwidth = 60)
        self.vt_tabla.heading("#1", text = "Producto")
        self.vt_tabla.column("#1", width = 290, minwidth = 200)
        self.vt_tabla.heading("#2", text = "Precio Compra")
        self.vt_tabla.column("#2", width = 80, minwidth = 70)
        self.vt_tabla.heading("#3", text = "Cantidad")
        self.vt_tabla.column("#3", width = 53, minwidth = 50)
        self.vt_tabla.heading("#4", text = "Subtotal")
        self.vt_tabla.column("#4", width = 60, minwidth = 60)
        self.vt_tabla.heading("#5", text = "Proveedor")
        self.vt_tabla.column("#5", width = 100, minwidth = 100)
        self.vt_tabla.heading("#6", text = "Notas")
        self.vt_tabla.column("#6", width = 200, minwidth = 200)
        self.vt_tabla.bind("<BackSpace>", self.quitar_producto)
        self.vt_tabla.bind("<Double-1>", self.info)

        self.l = []
        self.ve_clien = AutocompleteEntry(self.l, self.fvf)
        self.ve_clien.bind("<Return>", self.cambiar_proveedor, add="+")
        self.ve_clien.grid( row = 0, column = 5, sticky = tk.W)

        self.vl_notas = tk.Label(self.fvf, text = "Notas", font = "AppleGothic")
        self.vl_notas.grid(row = 1, column = 0, sticky = tk.E)
        self.vt_notas = tk.Text(self.fvf, width = 20, height = 4, wrap = tk.WORD, highlightthickness = 1, borderwidth = 1, fg = "black", font = "AppleGothic")
        self.vt_notas.bind("<Return>", self.notas)
        self.vt_notas.grid(row = 1, column = 1, padx = 6, rowspan = 2,  sticky = tk.W )
        
        self.vcb_se.grid_remove()
        self.vl_clien['text'] = 'Cambiar Proveedor'
        self.vb_venta.grid_remove()
        self.vb_compra = tk.Button(self.fvf, text = "COMPRA", width = 9, height = 1, fg = "green",font= ("AppleGothic 17 "), command =  self.compra)     
        self.vb_compra.grid(row = 1, column  = 5, pady = 20, sticky = tk.E)
        self.vb_guardar = tk.Button(self.fvf, text = "ORDEN de COMPRA", width = 18, height = 1, fg = "violet",font= ("AppleGothic"), command = self.orden_compra)     # Orden de compra
        self.vb_guardar.grid(row = 1, column  = 3, pady = 20, sticky = tk.E)
        self.vl_pago.grid_remove()
        self.fvp.grid_remove()
        self.fvr.grid_remove()


    # con el precio ultimamente usado, fetch db
    def agregar_producto(self):   
        cotexi = True
        for row in self.productos_db.fetch():
            if row[1] == self.ve_prod.get() or row[0] == self.ve_prod.get(): # Se busca por nombre o clave entonces tiene que coincidir en la self.productos_db de productos.       
                for rowcot in self.tmpI3_db.fetch():
                    if rowcot[2] == row[0]:  #Ya existe en la cotización
                        self.tmpI3_db.updateu(rowcot[0], rowcot[1], rowcot[2], rowcot[3], rowcot[4], rowcot[5]+1, round( rowcot[4]*(rowcot[5]+1), 3), rowcot[7], rowcot[8] )  # Actualizar cantidad y subtotal y precio
                        cotexi = False

                if cotexi:    # No existía en cotización antes
                    lock = False    
                    for p in self.compra_db.inverse_fetch():
                            if row[0] == p[2]:
                    # COMO MANEJAR EL NUMERO DE COMPRA CUANDO ES UNA LISTA?? , quiza sumarle uno pero se cambiaria y bla bla, o solo dejarlo como una compra como en venta quiza, y el 
                    #update que sea diferente, unitario, usando la clave en vez de ncompra
                                self.tmpI3_db.insert(self.hoy, self.reg_db.numero("Compra"), row[0], row[1], p[4], 1, round( p[4], 3), '', '' )  
                                lock = True
                            if lock:
                                print("exit for")
                                break
                    if not lock:
                        print("liblock")
                        self.tmpI3_db.insert(self.hoy, self.reg_db.numero("Compra"), row[0], row[1], 0, 1, 0, '', '' )  

        # Refresh
        self.paint()
    def paint(self):
        total = 0
        # Insertar en el arbol los datos de self.tmpVent_db, "refresh"
            # Eliminar primero todo el árbol
        leaves = self.vt_tabla.get_children()   
        for row in leaves:
            self.vt_tabla.delete(row)
            # Poblar el árbol
        for row in self.tmpI3_db.fetch():
            self.vt_tabla.insert("", "end",text = row[2],  values = (row[3],"$" + str(row[4]), row[5], "$"+ str(row[6]), row[7], row[8]) )
            total += float(row[6])

        self.vst_total.set("TOTAL ---- $ " + str(round(total, 3)))
    def quitar_producto(self, e):
        # Quitar de la self.tmpVent_db el elemento seleccionado text es clave.
        for p in self.vt_tabla.selection():
            pselec = self.vt_tabla.item(p)["text"]
            self.tmpI3_db.remove(pselec)

        self.paint()
    def cambiar_cantidad(self, e):
        try:
            pselec = self.vt_tabla.item(self.vt_tabla.selection())

            for rowcot in self.tmpI3_db.fetch():   
                if pselec["text"] == rowcot[2]: 
                    self.tmpI3_db.updateu(rowcot[0], rowcot[1], rowcot[2], rowcot[3], rowcot[4], round((round(float(self.ve_cant.get()), 3)), 3), round((round(float(self.ve_cant.get()), 3)) * rowcot[4], 3), rowcot[7], rowcot[8])  
        except:
            pass

        # Refresh
        self.paint()
    def cambiar_proveedor(self, e):
        try:    # No queremos que haga nada si nada está seleccionado
            for row in self.tmpI3_db.fetch():
                self.tmpI3_db.updateu(row[0], row[1], row[2], row[3], row[4], row[5], row[6], self.ve_clien.get(), row[8])
            self.paint()
        except:
            pass
    def notas (self, e):
        try:    # No queremos que haga nada si nada está seleccionado
            for p in self.vt_tabla.selection():
                pselec = self.vt_tabla.item(p)
                for row in self.tmpI3_db.fetch():
                    if pselec["text"] == row[2]:
                        self.tmpI3_db.updateu(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], self.vt_notas.get("1.0", tk.END))
        except:
            pass

        # Refresh
        self.paint()
    def cambiar_precio(self, e):
        try:    # No queremos que haga nada si nada está seleccionado
            pselec = self.vt_tabla.item(self.vt_tabla.selection())

            for row in self.tmpI3_db.fetch():   
                if pselec["text"] == row[2]: 
                    self.tmpI3_db.updateu(row[0], row[1], row[2], row[3], self.ve_precio.get(), row[5], round((float(self.ve_precio.get()) * float(row[5] )), 3), row[7], row[8])
            self.paint()
        except:
            pass

    ### def cambiar_fecha(self) ????? §§§§

    # §§§ autoagregar nhevo producto, no se podra' porque no va a dejar que se agregue al tree
    def compra(self):
        datestring = datetime.today().strftime("%Y/%m/%d")
        total = 0
        # No hacer nada si no hay nada
        x = 0
        for leaves in self.vt_tabla.get_children():
            x += 1
        if x == 0:
            return

            # Escribir
        for row in self.tmpI3_db.fetch():
            # guardar en compras db
            self.compra_db.insert(datestring, row[1], row [2], row[3], row[4], row[5], row[6], row[7], row[8])
            for roww in self.productos_db.fetch():
                if row[2] == roww[0]:
                # Ajustar el stock
                    self.productos_db.update(roww[0], roww[1], roww[2], roww[3], roww[4], roww[5], roww[6], roww[7], round(roww[8]+ float(row[5]), 3), roww[9])

        registro = self.reg_db.accion("Compra")  # Se incrementa dependiendo del tipo
        tkinter.messagebox.showinfo("Compra", "Compra guardada con éxito." )

        self.focus() 
        self.ve_prod.focus() 

        # Borrar tmpI3_db
        self.vt_info.delete("1.0", tk.END)
        for row in self.tmpI3_db.fetch():
            self.tmpI3_db.remove(row[2])

        # Borrar árbol 
        leaves = self.vt_tabla.get_children()    
        for row in leaves:
            self.vt_tabla.delete(row)
        # Borrar labels 
        self.vst_total.set("TOTAL ---- $ 0")
        self.vt_info.config(state = "normal")
        self.vt_info.delete("1.0", tk.END)
        self.vt_info.config(state = "disabled")
        self.n_venta.set("No. Compra: " + self.reg_db.numero("Compra"))
    def cancelar(self):
        try:        # Only do if list is not empty
            self.tmpI3_db.fetch()[0]
            result = tkinter.messagebox.askyesno("Cancelar", "¿Segura que quieres cancelar? Se borrarán todos los productos.")

            if result:
                self.vt_info.delete("1.0", tk.END)
                # Borrar cot self.productos_db
                for row in self.tmpI3_db.fetch():
                    self.tmpI3_db.remove(row[2])
                # Borrar árbol
                leaves = self.vt_tabla.get_children()    
                for row in leaves:
                    self.vt_tabla.delete(row)
                self.focus() 
                self.ve_prod.focus() 
                self.vst_total.set("TOTAL ---- $ 0")
            self.vt_info.config(state = "normal")
            self.vt_info.delete("1.0", tk.END)
            self.vt_info.config(state = "disable")
        except:
            pass
    def orden_compra(self):
        datestring = datetime.today().strftime("%Y/%m/%d")
        total = 0
        # No hacer nada si no hay nada
        x = 0
        for leaves in self.vt_tabla.get_children():
            x += 1
        if x == 0:
            return
            # Escribir
        num = self.reg_db.numero("Orden")  # Se incrementa dependiendo del tipo
        for row in self.tmpI3_db.fetch():
            # a la db ordem
            self.orden_db.insert(datestring, num, row [2], row[3], row[4], row[5], row[6], row[7], row[8])

        self.reg_db.accion("Orden")
        tkinter.messagebox.showinfo("Orden de Compra", "Orden de compra guardada con éxito." )

        self.focus() 
        self.ve_prod.focus() 

        # Borrar tmpI3_db
        self.vt_info.delete("1.0", tk.END)
        for row in self.tmpI3_db.fetch():
            self.tmpI3_db.remove(row[2])

        # Borrar árbol 
        leaves = self.vt_tabla.get_children()    
        for row in leaves:
            self.vt_tabla.delete(row)
        # Borrar labels 
        self.vst_total.set("TOTAL ---- $ 0")
        self.vt_info.config(state = "normal")
        self.vt_info.delete("1.0", tk.END)
        self.vt_info.config(state = "disabled")
        # self.n_venta.set("No. Compra: " + self.reg_db.numero("Compra"))

class F_Orden(tk.Frame):
    def __init__(self, root,  AutocompleteEntry, hoy, lista_productos, lista_claves, lista_total, productos_db, reg_db, tmpI4_db, tmpI5_db, orden_db, compra_db, l_compras, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.AutocompleteEntry = AutocompleteEntry
        self.hoy = hoy
        self.lista_productos = lista_productos
        self.lista_claves = lista_claves
        self.lista_total = lista_total
        self.productos_db = productos_db
        self.reg_db = reg_db
        self.tmpI4_db = tmpI4_db
        self.tmpI5_db = tmpI5_db
        self.orden_db = orden_db
        self.compra_db = compra_db
        self.l_compras = l_compras

        self.fecha = ""
        self.registro = ""

        self.prueba = tk.Frame(self)
        self.prueba.grid(row = 0, column = 0, sticky = tk.N)


        # LabelFrame filtros etc
        self.vf_filtros = tk.LabelFrame(self.prueba, text = "Filtros", font = "AppleGothic 18")
        self.vf_filtros.grid(row = 0, column = 0, columnspan = 3, rowspan = 4,  padx = 16, sticky = tk.N)

        labels = ("No. Orden", "Fecha", "(AAAA/MM/DD)", "Clave", "Producto", "Proveedor")
        x = 1
        for l in labels:
            tk.Label(self.vf_filtros, text = l, font = "AppleGothic").grid(row = x, column = 0, pady = 3, padx = 5, sticky = tk.W)
            x += 1

        # Numero de venta       
        self.ve_numventa = tk.Entry(self.vf_filtros)
        self.ve_numventa.grid(row = 1, column = 1)

        # Intervalo  
        self.vf_intervalo = tk.Frame(self.vf_filtros)
        self.vf_intervalo.grid(row = 2, column = 1, columnspan = 3)

        # Fecha
        self.ve_fecha = tk.Entry(self.vf_filtros)

        self.intervalo = tk.IntVar()
        self.intervalo.set("0")
        self.vr_no = tk.Radiobutton(self.vf_intervalo, text = "Todo", font = "AppleGothic", variable = self.intervalo, value = 0, command = self.check_fecha)
        self.vr_no.grid(row = 0, column = 0, sticky = tk.W)
        self.vr_dia = tk.Radiobutton(self.vf_intervalo, text = "Día", font = "AppleGothic", variable = self.intervalo, value = 1, command = self.check_fecha)
        self.vr_dia.grid(row = 0, column = 1, sticky = tk.W)
        self.vr_mes = tk.Radiobutton(self.vf_intervalo, text = "Mes", font = "AppleGothic", variable = self.intervalo, value = 3, command = self.check_fecha)
        self.vr_mes.grid(row = 1, column = 0, sticky = tk.W)
        self.vr_año = tk.Radiobutton(self.vf_intervalo, text = "Año", font = "AppleGothic", variable = self.intervalo, value = 4, command = self.check_fecha)
        self.vr_año.grid(row = 1, column = 1, sticky = tk.W)


        # Clave
        self.ve_clave = AutocompleteEntry(self.lista_claves, self.vf_filtros)
        self.ve_clave.grid(row = 4, column = 1)

        # Producto
        self.ve_producto = AutocompleteEntry(self.lista_productos, self.vf_filtros)
        self.ve_producto.grid(row = 5, column = 1)

        # Cliente
        self.ve_cliente = tk.Entry(self.vf_filtros)
        self.ve_cliente.grid(row = 6, column = 1)

        self.vf_fpago = tk.Frame(self.vf_filtros)
        self.vf_fpago.grid(row = 7, column = 1, columnspan = 2, rowspan = 5)

        # Añadir filtros
        self.vb_filtrar = tk.Button(self.vf_fpago, text = "Filtrar", width = 8, height = 1, fg = "green", font = "AppleGothic 15", command = self.filtrar)
        self.vb_filtrar.grid(row = 4, column = 0, pady = 8, padx = 3, sticky = tk.W)
        # Limpiar
        self.vb_limpiar = tk.Button(self.vf_fpago, text = "Limpiar", width = 8, height = 1, fg = "red", font = "AppleGothic 15", command = self.limpiar)
        self.vb_limpiar.grid(row = 4, column = 1, pady = 8, sticky = tk.E)
        # Historial
        self.vb_historial = tk.Button(self.vf_filtros, text = "Historial", width = 8, height = 1, fg = "black", font = "AppleGothic 15", command = self.historial)
        self.vb_historial.grid(row = 11, column = 0, pady = 8, sticky = tk.W, padx = 8)




        # Frame trees etc.
        self.vf_trees = tk.Frame(self)
        self.vf_trees.grid(row = 0, column = 3)

        # Treeview Registro
        self.style = ttk.Style()
        self.style.configure("mystyle.Treeview", highlightthickness=0, bd=0, rowheight = 20, font=('AppleGothic', 13)) # Modify the font of the body
        self.style.configure("mystyle.Treeview.Heading", font=('AppleBraille', 15,'bold')) # Modify the font of the headings

        self.vt_registro = ttk.Treeview(self.vf_trees, height = 12, columns=("#1","#2","#3","#4"), style = "mystyle.Treeview")
        self.vt_registro.grid(row = 0, column = 0,  columnspan = 4, pady = 27, padx = 15, sticky = tk.W + tk.N)
        self.vt_registro.heading("#0", text = "Fecha")
        self.vt_registro.column("#0", width = 170, minwidth = 150)
        self.vt_registro.heading("#1", text = "No. Orden")
        self.vt_registro.column("#1", width = 90, minwidth = 90)
        self.vt_registro.heading("#2", text = "Cantidad")
        self.vt_registro.column("#2", width = 90, minwidth = 90)
        self.vt_registro.heading("#3", text = "Total")
        self.vt_registro.column("#3", width = 120, minwidth = 120)
        self.vt_registro.heading("#4", text = "Proveedor")
        self.vt_registro.column("#4", width = 136, minwidth = 136)
        self.vt_registro.bind("<Double-1>", self.seleccionado)

            
        # Label info registro tree
        self.vs_info = tk.StringVar()
        self.vl_info = tk.Label(self.vf_trees, textvariable = self.vs_info, font = "AppleBraille 15" )
        self.vl_info.grid(row = 1, column = 3, sticky = tk.E + tk.N)



        # Treeview Detalle
        self.vt_selec = ttk.Treeview(self.vf_trees, height = 10, columns=("#1","#2","#3","#4", "#5"), style = "mystyle.Treeview")
        self.vt_selec.grid(row = 3, column = 0, padx = 15, columnspan = 4, sticky = tk.W + tk.E)
        self.vt_selec.heading("#0", text = "Clave")
        self.vt_selec.column("#0", width = 80, minwidth = 60)
        self.vt_selec.heading("#1", text = "Producto")
        self.vt_selec.column("#1", width = 250, minwidth = 100)
        self.vt_selec.heading("#2", text = "Precio")
        self.vt_selec.column("#2", width = 70, minwidth = 70)
        self.vt_selec.heading("#3", text = "Cantidad")
        self.vt_selec.column("#3", width = 80, minwidth = 70)
        self.vt_selec.heading("#4", text = "Total")
        self.vt_selec.column("#4", width = 70, minwidth = 70)
        self.vt_selec.heading("#5", text = "Notas")
        self.vt_selec.column("#5", width = 250, minwidth = 100)

        # Label detalle
        self.vs_selec = tk.StringVar()
        self.vs_selec.set("")
        self.vl_selec = tk.Label(self.vf_trees, textvariable = self.vs_selec, font = ("AppleGothic",16, "bold"))
        self.vl_selec.grid(row = 2, column = 0, sticky = tk.W, padx = 10)

        # Exportar orden
        # self.vb_expd = tk.Button(self.prueba, text = "Exportar Orden", font = "AppleBraille", width = 20, height = 2, command = lambda: self.exportar_nota(self.orden, self.fecha, self.registro, self.vt_selec, "Orden", "ordenes") )
        # self.vb_expd.grid(row = 4, column = 1, pady = 25)

        # Vender Orden
        self.vb_vencot = tk.Button(self.prueba, text = "Comprar Orden", font = "AppleBraille", fg = "green", width = 20, height = 2, command = self.comprar_orden)
        self.vb_vencot.grid(row = 4, column = 2)

        # Eliminar Orden
        self.vb_red = tk.Button(self.prueba, text = "Eliminar Orden", font = "AppleBraille", fg = "red", width = 20, height = 2, command = self.eliminar_orden)
        self.vb_red.grid(row = 5, column = 2)        
        
        # Ajustar cotizacion
        self.vb_ajcot = tk.Button(self.prueba, text = "Ajustar Orden", font = "AppleBraille", fg = "violet", width = 20, height = 2, command = self.ajustar_orden)
        self.vb_ajcot.grid(row = 5, column = 1)
    def historial(self):
        self.limpiar()
        for row in self.orden_db.fetch():
            self.tmpI4_db.insert(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
        self.paint()
        # self.limpiar()
    def check_fecha(self):
        if self.intervalo.get() == 0:
            self.ve_fecha.grid_remove()
        else:
            self.ve_fecha.grid(row = 3, column = 1)
    ##### observar - semana no implementado ####   
    def filtrar(self):
     # Variables
        self.vs_info.set("")
     # 0. Borrar nuestra db provisional
        self.limpiar()
     # 1. No. Venta
        try:
            self.ve_numventa.get()[0]
            for row in self.orden_db.fetch():
                if str(row[1]) == str(self.ve_numventa.get()):
                    self.tmpI4_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
            self.paint()
            return
        except:
            pass
     # 2. Fecha
        if self.intervalo.get() != 0:
            try:  # we'll just simply try to convert the string to a Python datetime and see if it fails
                datetime.strptime(self.ve_fecha.get(), '%Y/%m/%d')
            except ValueError:
                tkinter.messagebox.showerror("Error", "Error, la fecha tiene que estar en el formato correcto, por favor.")
                self.focus_set()
                self.ve_fecha.focus_set()
                return  
        # 2.1 x Día
        if self.intervalo.get() == 1:
            dia_db = ""
            for row in self.orden_db.fetch():
                dia_db = dia_db + str(row[0][0])    # Tiene que ser el día del mismo mes y año
                dia_db = dia_db + str(row[0][1])
                dia_db = dia_db + str(row[0][2])
                dia_db = dia_db + str(row[0][3])
                dia_db = dia_db + str(row[0][4])
                dia_db = dia_db + str(row[0][5])
                dia_db = dia_db + str(row[0][6])
                dia_db = dia_db + str(row[0][7])
                dia_db = dia_db + str(row[0][8])
                dia_db = dia_db + str(row[0][9])
                if dia_db == self.ve_fecha.get():
                    self.tmpI4_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                dia_db = ""
        # 2.2 x Semana ******* VER DESPUÉS
        # 2.3 x Mes
        elif self.intervalo.get() == 3:
            mes_db = []
            mes_e = []
            mes_e.append(self.ve_fecha.get()[0])
            mes_e.append(self.ve_fecha.get()[1])
            mes_e.append(self.ve_fecha.get()[2])
            mes_e.append(self.ve_fecha.get()[3])
            mes_e.append(self.ve_fecha.get()[4])
            mes_e.append(self.ve_fecha.get()[5])
            mes_e.append(self.ve_fecha.get()[6])
            for row in self.orden_db.fetch():
                mes_db.append(row[0][0])    # Coincidir mes y año
                mes_db.append(row[0][1])
                mes_db.append(row[0][2])
                mes_db.append(row[0][3])
                mes_db.append(row[0][4])
                mes_db.append(row[0][5])
                mes_db.append(row[0][6])
                if mes_db == mes_e:
                    self.tmpI4_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                mes_db = []
        # 2.4 x Año
        elif self.intervalo.get() == 4:
            año_db = []
            año_e = []
            año_e.append(self.ve_fecha.get()[0])
            año_e.append(self.ve_fecha.get()[1])
            año_e.append(self.ve_fecha.get()[2])
            año_e.append(self.ve_fecha.get()[3])
            for row in self.orden_db.fetch():
                año_db.append(row[0][0])
                año_db.append(row[0][1])
                año_db.append(row[0][2])
                año_db.append(row[0][3])
                if año_db == año_e:
                    self.tmpI4_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                año_db = []
     # 3. Clave
        try:
            # Revisar que nada esté vacío
            self.ve_clave.get()[0]  
            try:
                self.tmpI4_db.fetch()[0]    # Ver si ya hay algo
                for row in self.tmpI4_db.fetch():
                    if row[2].lower() != self.ve_clave.get().lower():
                        self.tmpI4_db.remove(row[2])

            except: # Si no, usar la de ventas
                for row in self.orden_db.fetch():
                    if row[2].lower() == self.ve_clave.get().lower():
                        self.tmpI4_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])

        except:
            pass
     # 4. Producto
        try:
            # Revisar que nada esté vacío
            self.ve_producto.get()[0]  
            try:
                self.tmpI4_db.fetch()[0]    # Ver si ya hay algo
                for row in self.tmpI4_db.fetch():
                    if row[3].lower() != self.ve_producto.get().lower():
                        self.tmpI4_db.remove(row[2])
                        
            except: # Si no, usar la de ventas
                for row in self.orden_db.fetch():
                    if row[3].lower() == self.ve_producto.get().lower():
                        self.tmpI4_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])

        except:
            pass
     # 5. proveedor
        try:
            # Revisar que nada esté vacío
            self.ve_cliente.get()[0]  
            try:
                self.tmpI4_db.fetch()[0]    # Ver si ya hay algo
                for row in self.tmpI4_db.fetch():
                    if row[7].lower() != self.ve_cliente.get().lower():
                        self.tmpI4_db.remove(row[2])
                        
            except: # Si no, usar la de ventas
                for row in self.orden_db.fetch():
                    if row[7].lower() == self.ve_cliente.get().lower():
                        self.tmpI4_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])

        except:
            pass


     # Paint
        self.paint()

    ##### observar ####   
    def limpiar(self):
        self.tmpI4_db.deleteall()
        for p in self.vt_registro.get_children():
            self.vt_registro.delete(p)
        for p in self.vt_selec.get_children():
            self.vt_selec.delete(p)
        self.vs_selec.set("")
        self.vs_info.set("")
    def paint(self):
        try:
            tmp = self.tmpI4_db.inverse_fetch()[0][1]           
            tmptot = 0
            tmpcant = 0
            f = ""
            seven = ""
            eight = ""

            for row in self.tmpI4_db.inverse_fetch():

                if row[1] == tmp:
                    tmptot += row[6]
                    tmpcant += row[5]
                    f = row[0]
                    seven = row[7]
                else:
                    self.vt_registro.insert("", "end", text = f, values =("No. " + str(tmp), round(tmpcant, 3), "$" + str(round(tmptot, 3)), seven))
                    tmp = row[1]
                    tmptot = row[6]
                    tmpcant = row[5]
                    f = row[0]
                    seven = row[7]
   

            self.vt_registro.insert("", "end", text = f, values =("No. " + str(tmp), round(float(tmpcant), 3), "$" + str(round(float(tmptot),3)), seven))
        except:
            pass
    def seleccionado(self, event):
        try:
            self.fecha = self.vt_registro.item(self.vt_registro.selection())["text"]
            self.registro = self.vt_registro.item(self.vt_registro.selection())["values"][0]
            # print(self.registro)
            total = 0

            for row in self.vt_selec.get_children():
                self.vt_selec.delete(row)

            for row in self.tmpI4_db.fetch():
                if ("No. " + str(row[1])) == self.registro:
                    self.vt_selec.insert("", "end",text = row[2],  values = (row[3],"$" + str(row[4]), row[5], "$"+ str(row[6]), row[8]) )
                    total += row[6]

            self.vs_selec.set("Detalle de venta "+ self.registro + ". Total de nota: $" + str(round(total, 3)))
        except:
            pass
    # def exportar_nota(self, db, fecha, registro, tree, tipo, folder):

    #     tmp = tipo + "_" + registro + ".csv"
    #     # filename = os.path.abspath(
    #     # os.path.join(sys.executable + "/archivos_momu/", '..', '..', '..', '..','..', "archivos_momu"))
    #     # filename = os.path.join(filename +  "/" + folder + '/',tmp)
    #     filename = os.path.join(os.path.expanduser('~'),'Documents/momu_la_bola/archivos_momu/' + folder + '/',tmp)
    #     print(filename)
    #     total_nota = 0
    #     newfile = not os.path.exists(filename)    
    #     data = {}
    #     status = ""

    #     # No hacer nada si no hay nada
    #     x = 0
    #     for leaves in tree.get_children():
    #         x += 1
    #     if x == 0:
    #         return


    #     with open(filename, 'a', encoding='utf_8_sig', newline='') as fh:	
    #         csvwriter= csv.DictWriter(fh, fieldnames=("Fecha", "Registro", "Clave", "Producto", "Precio", "Cantidad", "Total", "Cliente", "S/E", "Lista", "Pago", "Status"))
    #         if newfile:
    #             csvwriter.writeheader()

    #         # Escribir
    #         for row in db.fetch():

    #             if "No. " + str(row[1]) == self.registro:
    #                 # Agregar a .csv
    #                 data["Fecha"] = self.fecha
    #                 data["Registro"] = self.registro
    #                 data["Clave"] = row[2]
    #                 data["Producto"] = row[3]
    #                 data["Precio"] = row[4]
    #                 data["Cantidad"] = row[5]
    #                 data["Total"] = row[6]
    #                 data["Cliente"] = row[7]
    #                 data["S/E"] = row[8]
    #                 data["Lista"] = row[9]
    #                 data["Pago"] = row[10]
    #                 status = row[11]

    #                 total_nota += row[6]

    #                 csvwriter.writerow(data)

    #         # Solo generar un registro si sí hay algo que vender y si hay suficiente!!
    #                 # Añadir fila del *total* de cada registro
    #         data = {}
    #         data["Fecha"] = self.fecha
    #         data["Registro"] = self.registro
    #         data["Clave"] = "Total "
    #         data["Producto"] = "de nota número " + self.registro
    #         data["Total"] = round(total_nota, 3)
    #         data["Status"] = status
            
    #         csvwriter.writerow(data)

    #     os.chmod(filename, 0o444)
    #     tkinter.messagebox.showinfo("Exportado", "Exportación exitosa. Se encontrará en un archivo con nombre: " + tipo + "_" + self.registro + ".csv")
    #     self.focus()
    #     for c in self.vt_selec.get_children():
    #         self.vt_selec.delete(c)
    #     self.vs_selec.set("")

        
    #     if tkinter.messagebox.askyesno("Cancelar", "¿Segura que quieres cancelar la nota? Se marcará como cancelada y el stock de los productos se ajustará."):
    #         for row in db.fetch():
    #             if "No. " + str(row[1]) == registro:  # Cambiar el status de los productos de la nota con dicho número
    #                 db.cancelado(row[0], row[1], row[2] )
    #                 # Y luego incrementar el stock de dichos productos
    #                 for pro in self.productos_db.fetch():
    #                     if row[2] == pro[0]:
    #                         self.productos_db.update(pro[0], pro[1], pro[2], pro[3], pro[4], pro[5], pro[6], pro[7], pro[8] + row[5], pro[9])
            
    #         for c in self.vt_selec.get_children():
    #             self.vt_selec.delete(c)
    #         self.vs_selec.set("")
    #         self.filtrar()
    def eliminar_orden(self): 
        # Ver si hay algo seleccionado
        x = 0
        for l in self.vt_selec.get_children():
            x += 1
        if x == 0:
            tkinter.messagebox.showinfo("Eliminar", "Selecciona una orden a eliminar." )
            self.focus() 
            return

        if tkinter.messagebox.askyesno("Eliminar", "¿Segura que quieres eliminar la orden?"):
            for row in self.orden_db.fetch():
                if "No. " + str(row[1]) == self.registro:  
                    self.orden_db.removeNum(row[1])
            
            for c in self.vt_selec.get_children():
                self.vt_selec.delete(c)
            self.vs_selec.set("")
            self.historial()
            self.focus()
    def comprar_orden(self):
        x = 0
        for l in self.vt_selec.get_children():
            x += 1
        if x == 0:
            tkinter.messagebox.showinfo("Comprar", "Selecciona una orden a comprar." )
            self.focus() 
            return
        datestring = datetime.today().strftime("%Y/%m/%d")
       
        # No hacer nada si no hay nada
        x = 0
        for leaves in self.vt_selec.get_children():
            x += 1
        if x == 0:
            return

        # podemos proseguir a hacer la compra. 
        reg = self.reg_db.accion("Compra")  
        for row in self.orden_db.fetch():   
            if "No. " + str(row[1]) == self.registro:
                self.compra_db.insert(datestring, reg, row[2], row[3], row[4], row[5], row[6], row[7], row[8])

                for stock in self.productos_db.fetch():
                    if row[2] == stock[0]:
                        # Ajustar stock
                        self.productos_db.update(stock[0], stock[1], stock[2], stock[3], stock[4], stock[5], stock[6], stock[7], stock[8] + row[5], stock[9] )  

                self.orden_db.removeNC(row[1], row[2])

        tkinter.messagebox.showinfo("Compra", "Compra guardada con éxito." )
        self.filtrar()
        self.focus() 
        self.ve_numventa.focus() 


        for c in self.vt_selec.get_children():
            self.vt_selec.delete(c)
        self.vs_selec.set("")
    def ajustar_orden(self):

        # Ver si hay algo seleccionado
        x = 0
        for leaves in self.vt_selec.get_children():
            x += 1
        if x == 0:
            tkinter.messagebox.showinfo("Seleccionar", "Selecciona una orden a ajustar." )
            self.focus() 
            return


        # Nueva ventana
        ajustar_window = tk.Toplevel(self)
        ajustar_window.title("Ajustar Orden")
        ajustar_window.transient(self) #set to be on top of the main window
        ajustar_window.grab_set() #hijack all commands from the master (clicks on the main window are ignored)
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        ajustar_window.geometry("+%d+%d" % (w/12 , h/8))

        # Heredar
        f_ajOrden = F_ajOrden(ajustar_window, self.l_compras.Clock, self.l_compras.AutocompleteEntry, self.l_compras.hoy, self.l_compras.lista_productos, self.l_compras.lista_claves, self.l_compras.lista_total, self.l_compras.productos_db, self.l_compras.tmpVent_db, self.l_compras.tmpCot_db, self.l_compras.clien_db, self.l_compras.compra_db ,self.l_compras.venta_db, self.l_compras.reg_db, self.l_compras.cot_db, self.tmpI5_db, self.l_compras.orden_db)
        f_ajOrden.grid(row = 0 , column = 0 )

        # Agregar productos en cotizacion pasada
        f_ajOrden.vt_info.delete("1.0", tk.END)
        # Borrar tmpI5 llamada tmpI3
        for row in f_ajOrden.tmpI3_db.fetch():
            f_ajOrden.tmpI3_db.removeNum(row[1])
        # Borrar árbol
        leaves = f_ajOrden.vt_tabla.get_children()    
        for row in leaves:
            f_ajOrden.vt_tabla.delete(row)
        for row in self.tmpI4_db.fetch():
            if ("No. " + str(row[1])) == self.registro:
                f_ajOrden.tmpI3_db.insert(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8] )
        f_ajOrden.paint()

        def cerrar():
            ajustar_window.grab_release()
            ajustar_window.destroy()
            self.focus_set()
            self.historial()
        def ajustarCot():
            f_ajOrden.orden_compra()
            cerrar()
        def cancelarAjustar():
            try:        # Only do if list is not empty
                f_ajOrden.tmpI3_db.fetch()[0]
                result = tkinter.messagebox.askyesno("Cancelar", "¿Segura que quieres cancelar? No se guardarán los cambios a la orden.")
                if result:
                    f_ajOrden.vt_info.delete("1.0", tk.END)
                    # Borrar tmpI3_db
                    for row in f_ajOrden.tmpI3_db.fetch():
                        f_ajOrden.tmpI3_db.remove(row[0])
                    # Borrar árbol
                    leaves = f_ajOrden.vt_tabla.get_children()    
                    for row in leaves:
                        f_ajOrden.vt_tabla.delete(row)
                    f_ajOrden.focus() 
                    f_ajOrden.ve_prod.focus() 
                    f_ajOrden.vst_total.set("TOTAL ---- $ 0")
                f_ajOrden.vt_info.config(state = "normal")
                f_ajOrden.vt_info.delete("1.0", tk.END)
                f_ajOrden.vt_info.config(state = "disable")
                cerrar()
            except:
                pass

        ajustar_window.protocol("WM_DELETE_WINDOW", lambda: cerrar())
        f_ajOrden.vb_guardar["command"] = ajustarCot
        f_ajOrden.vb_cancelar["command"] = cancelarAjustar
        

class F_ajOrden(L_Compras):
    def __init__(self, root, Clock, AutocompleteEntry, hoy, lista_productos, lista_claves, lista_total, productos_db, tmpVent_db, tmpCot_db, clien_db, compra_db, venta_db, reg_db, cot_db, tmpI3_db, orden_db, *args, **kwargs):
        super().__init__( root, Clock, AutocompleteEntry, hoy, lista_productos, lista_claves, lista_total, productos_db, tmpVent_db, tmpCot_db, clien_db, compra_db, venta_db, reg_db, cot_db, tmpI3_db, orden_db, *args, **kwargs)

        self.vb_guardar["text"] = "AJUSTAR ORDEN"
        self.vb_compra.grid_remove()
        self.n_venta.set("No. Orden: " + self.reg_db.numero("Orden"))        









class F_Productos(tk.Frame):   
    def __init__(self, root,  AutocompleteEntry, hoy, lista_productos, lista_claves, lista_total, productos_db,  venta_db, compra_db, tmpI2_db, clien_db, reg_db,  *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.productos_db = productos_db
        self.clien_db = clien_db
        self.compra_db = compra_db
        self.venta_db = venta_db
        self.tmpI2_db = tmpI2_db
        self.reg_db = reg_db
        self.hoy = hoy
        self.AutocompleteEntry = AutocompleteEntry
        self.lista_productos = lista_productos
        self.lista_claves = lista_claves
        self.lista_total = lista_total

        

        # Frame
        self.prueba = tk.Frame(self)
        self.prueba.grid(row = 0, column = 0, sticky = tk.N)

        # Frame buscar
        self.if_buscar = tk.LabelFrame(self.prueba, text = "Buscar Producto", font = "AppleGothic 18")
        self.if_buscar.grid(row = 0, column = 0, columnspan = 3, rowspan = 4,  padx = 20, pady = 10, sticky = tk.N + tk.W)

        labels = ("Clave", "Producto")
        x = 0
        for l in labels:
            tk.Label(self.if_buscar, text = l, font = "AppleGothic").grid(row = x, column = 0, pady = 3, padx = 5, sticky = tk.W)
            x += 1

        self.ie_clave = AutocompleteEntry(self.lista_claves, self.if_buscar, width = 20, function = self.clave_producto_validate1 )
        self.ie_clave.grid(row = 0, column = 1, sticky = tk.W)
        self.ie_clave.bind("<Return>", self.clave_prod_tmp, add="+") 
        self.ie_prod = AutocompleteEntry(self.lista_productos, self.if_buscar, width = 40, function = self.producto_clave_validate1)
        self.ie_prod.grid(row = 1, column = 1, sticky = tk.W)
        self.ie_prod.bind("<Return>", self.prod_clave_tmp, add="+")
        self.ib_ba = tk.Button(self.if_buscar, text = "Buscar", width = 10, height = 2, font = "AppleBraille 15", command = self.buscar)
        self.ib_ba.grid(row = 2, column = 1, sticky = tk.W, pady = 5)
        
        self.extra = tk.Label(self.if_buscar)
        self.extra.grid(row = 3, column =1)


        # Frame Ajustar
        self.if_ajustar = tk.LabelFrame(self.prueba, text = "", font = "AppleBraille 18")
        
        # Labels
        tk.Label(self.if_ajustar, text = "Producto:", font = "AppleBraille 15").grid(row = 0, column = 0, sticky = tk.W)
        tk.Label(self.if_ajustar, text = "Stock: ", font = "AppleBraille 15").grid(row = 2, column = 0, sticky = tk.E)
        tk.Label(self.if_ajustar, text = "EN-Esp: $", font = "AppleGothic").grid(row = 0, column = 2, sticky = tk.E)
        tk.Label(self.if_ajustar, text = "EN-May: $", font = "AppleGothic").grid(row = 1, column = 2, sticky = tk.E)
        tk.Label(self.if_ajustar, text = "EN-Men: $", font = "AppleGothic").grid(row = 2, column = 2, sticky = tk.E)
        tk.Label(self.if_ajustar, text = "SU-Esp: $", font = "AppleGothic").grid(row = 0, column = 5, sticky = tk.E)
        tk.Label(self.if_ajustar, text = "SU-May: $", font = "AppleGothic").grid(row = 1, column = 5, sticky = tk.E)
        tk.Label(self.if_ajustar, text = "SU-Men: $", font = "AppleGothic").grid(row = 2, column = 5, sticky = tk.E)
        tk.Label(self.if_ajustar, text = "Notas:", font = "AppleGothic").grid(row = 0, column = 8, sticky = tk.E)

        
        # Actual
        self.ps = tk.StringVar()
        self.aas = tk.StringVar()
        self.bs = tk.StringVar()
        self.cs = tk.StringVar()
        self.ds = tk.StringVar()
        self.es = tk.StringVar()
        self.fs = tk.StringVar()
        self.gs = tk.StringVar()

        self.p = tk.Label(self.if_ajustar, textvariable = self.ps, font = "AppleBraille 14")
        self.p.grid(row = 0, column = 1, sticky = tk.W)
        self.a = tk.Label(self.if_ajustar, textvariable = self.aas, font = "AppleGothic")
        self.a.grid(row = 0, column = 3, sticky = tk.W)
        self.b = tk.Label(self.if_ajustar, textvariable = self.bs, font = "AppleGothic")
        self.b.grid(row = 0, column = 6, sticky = tk.W)
        self.c = tk.Label(self.if_ajustar, textvariable = self.cs, font = "AppleGothic")
        self.c.grid(row = 1, column = 3, sticky = tk.W)
        self.d = tk.Label(self.if_ajustar, textvariable = self.ds, font = "AppleGothic")
        self.d.grid(row = 1, column = 6, sticky = tk.W)
        self.e = tk.Label(self.if_ajustar, textvariable = self.es, font = "AppleGothic")
        self.e.grid(row = 2, column = 3, sticky = tk.W)
        self.f = tk.Label(self.if_ajustar, textvariable = self.fs, font = "AppleGothic")
        self.f.grid(row = 2, column = 6, sticky = tk.W)
        self.g = tk.Label(self.if_ajustar, textvariable = self.gs, font = "AppleBraille 17")
        self.g.grid(row = 2, column = 1, sticky = tk.W)
        self.nota = tk.Text(self.if_ajustar, width = 30, height = 5, highlightthickness = 1, wrap = tk.WORD,   borderwidth = 1, fg = "black", font = "AppleGothic")
        self.nota.grid(row = 0, column = 9, rowspan = 2, sticky = tk.W)


        # Botones
        self.ib_cancelar = tk.Button(self.if_ajustar, text = "Cancelar", font = "AppleBraille", width = 10, height = 2, command = self.cancelar)
        self.ib_cancelar.grid(row = 3, column = 0, sticky = tk.W, pady = 10, padx = 10 ) 
        self.ib_eliminar = tk.Button(self.if_ajustar, text = "Eliminar", font = "AppleBraille", fg = "red", width = 10, height = 2, command = self.eliminar)
        self.ib_eliminar.grid(row = 3, column = 4, sticky = tk.W, pady = 10 ) 
        self.ib_ajustar = tk.Button(self.if_ajustar, text = "Ajustar", font = "AppleBraille", fg = "green", width = 10, height = 2, command = self.ajustar)
        self.ib_ajustar.grid(row = 3, column = 7, sticky = tk.W, pady = 10 ) 

        # Entries
        self.ie_producto = tk.Entry(self.if_ajustar, width = 40)
        self.ie_producto.grid(row = 1, column = 0, columnspan = 2, sticky = tk.W)
        self.ie_ee = tk.Entry(self.if_ajustar, width = 7)
        self.ie_ee.grid(row = 0, column = 4, sticky = tk.W)
        self.ie_ema = tk.Entry(self.if_ajustar, width = 7)
        self.ie_ema.grid(row = 1, column = 4, sticky = tk.W)
        self.ie_eme = tk.Entry(self.if_ajustar, width = 7)
        self.ie_eme.grid(row = 2, column = 4, sticky = tk.W)
        self.ie_se = tk.Entry(self.if_ajustar, width = 7)
        self.ie_se.grid(row = 0, column = 7, sticky = tk.W)
        self.ie_sma = tk.Entry(self.if_ajustar, width = 7)
        self.ie_sma.grid(row = 1, column = 7, sticky = tk.W)
        self.ie_sme = tk.Entry(self.if_ajustar, width = 7)
        self.ie_sme.grid(row = 2, column = 7, sticky = tk.W)

        # Notas
        self.it_notas = tk.Text(self.if_ajustar, width = 30, height = 5, highlightthickness = 1, wrap = tk.WORD, borderwidth = 1, fg = "black", font = "AppleGothic")
        self.it_notas.grid(row = 2, column = 9, rowspan = 2, sticky = tk.W)


        # Style for all trees
        self.style = ttk.Style()
        self.style.configure("mystyle.Treeview", highlightthickness=0, bd=0, rowheight = 25, font="AppleGothic 14") # Modify the font of the body
        self.style.configure("mystyle.Treeview.Heading", font=('AppleBraille', 17,'bold'), bg = "blue") # Modify the font of the headings


        # Árbol con productos 
        self.it_productos = ttk.Treeview(self.prueba, height = 15, columns=("#1","#2","#3","#4", "#5", "#6", "#7", "#8", "#9"), style = "mystyle.Treeview")
        self.it_productos.grid(row = 4, column = 0,  columnspan = 8, pady = 20, padx = 20, sticky = (tk.W + tk.N))
        self.it_productos.heading("#0", text = "Clave")
        self.it_productos.column("#0", width = 85, minwidth = 85)
        self.it_productos.heading("#1", text = "Producto")
        self.it_productos.column("#1", width = 330, minwidth = 330)
        self.it_productos.heading("#2", text = "EN-Esp")
        self.it_productos.column("#2", width = 80, minwidth = 80)
        self.it_productos.heading("#3", text = "EN-May")
        self.it_productos.column("#3", width = 80, minwidth = 80)
        self.it_productos.heading("#4", text = "EN-Men")
        self.it_productos.column("#4", width = 80, minwidth = 80)
        self.it_productos.heading("#5", text = "SU-Esp")
        self.it_productos.column("#5", width = 80, minwidth = 80)
        self.it_productos.heading("#6", text = "SU-May")
        self.it_productos.column("#6", width = 80, minwidth = 80)
        self.it_productos.heading("#7", text = "SU-Men")
        self.it_productos.column("#7", width = 80, minwidth = 80)
        self.it_productos.heading("#8", text = "Stock")
        self.it_productos.column("#8", width = 80, minwidth = 80)
        self.it_productos.heading("#9", text = "Notas")
        self.it_productos.column("#9", width = 250, minwidth = 250)
        self.it_productos.bind("<Double-1>", self.bu)

        self.it_productos.tag_configure('odd', background='#C2B4E2')
        self.it_productos.tag_configure('even', background='#D0C9EA')
        
        # Info 
        self.is_info = tk.StringVar()
        self.il_info = tk.Label(self.prueba, textvariable = self.is_info, font = "AppleBraille 18" )
        self.il_info.grid(row = 5, column = 5, sticky = tk.E + tk.N)

    def historial(self):

        for p in self.it_productos.get_children():
            self.it_productos.delete(p)
        self.vre_Total = 0
        self.vre_Cant = 0
        x = 1
        for row in self.productos_db.fetch_alph():
            if x % 2:
                self.it_productos.insert("", "end", tags = "odd", text = row[0], values =(row[1], "$" + str(row[2]), "$" + str(row[4]), "$" + str(row[6]), "$" + str(row[3]), "$" + str(row[5]), "$" + str(row[7]), row[8], row[9]))
                x += 1
            else:
                self.it_productos.insert("", "end", tags = "even", text = row[0], values =(row[1], "$" + str(row[2]), "$" + str(row[4]), "$" + str(row[6]), "$" + str(row[3]), "$" + str(row[5]), "$" + str(row[7]), row[8], row[9]))
                x += 1
            #self.vre_Total += row[]
            self.vre_Cant += row[8]
        self.is_info.set("Productos totales: %s     Total en Dinero: $%s" % (round(self.vre_Cant, 3), round(self.vre_Total, 3)))
    def buscar(self):
       
        for row in self.productos_db.fetch():
            if row[0] == self.ie_clave.get() and row[1] == self.ie_prod.get():
                producto = row

        
        try:
            self.clave = producto[0]
            self.stock = producto[8]
        except:
            tkinter.messagebox.showerror("Error", "El producto que quieres buscar no existe. Haz una compra o intenta de nuevo.")
            self.ie_clave.focus_set()
            return
        
        self.if_buscar.grid_remove()
        self.if_ajustar.grid(row = 0, column =  0, columnspan = 8, pady = 10, padx = 20, sticky = tk.W)
        self.if_ajustar["text"] = "Ajustar Producto,  Clave: " + producto[0]

        # Actual
        labels = (self.ps, self.aas, self.bs, self.cs, self.ds, self.es, self.fs)
        x = 1
        for l in labels:
            l.set(producto[x])
            x+=1
        self.gs.set(round(producto[x], 3))
        self.nota.config(state = "normal")
        self.nota.insert("1.0", producto[9])
        self.nota.config(state = "disable")

        
        # Agregar a entries
        self.ie_producto.insert(0, producto[1])
        self.ie_ee.insert(0, producto[2])
        self.ie_se.insert(0, producto[3])
        self.ie_ema.insert(0, producto[4])
        self.ie_sma.insert(0, producto[5])
        self.ie_eme.insert(0, producto[6])
        self.ie_sme.insert(0, producto[7])
        self.it_notas.insert("1.0", producto[9])

        self.it_productos["height"] = 10
    def bu (self, event):   
        self.cancelar()
        
        self.ie_clave.delete(0, tk.END)
        self.ie_prod.delete(0, tk.END)
        self.ie_clave.insert(0, self.it_productos.item(self.it_productos.selection())["text"])
        self.ie_prod.insert(0, self.it_productos.item(self.it_productos.selection())["values"][0])

        self.buscar()
    def eliminar(self):
        if tkinter.messagebox.askyesno("Eliminar", "¿Segura que deseas ELIMINAR %s?" % (self.ps.get())):
            if tkinter.messagebox.askyesno("Eliminar", "¿Segura?"):
                self.productos_db.remove(self.clave)
                self.historial()
                self.cancelar()
                self.focus_set()
    def ajustar(self):
        # Revisar que todo esté completado
        entries = (self.ie_producto, self.ie_ee, self.ie_ema, self.ie_eme, self.ie_se, self.ie_sma, self.ie_sme)
        for e in entries:
            if len(e.get()) == 0:
                tkinter.messagebox.showerror("Error", "Error, no puedes dejar ningún campo vacío.")
                self.ie_producto.focus_set()
                return
        try:
            f = (self.ie_ee, self.ie_ema, self.ie_eme, self.ie_se, self.ie_sma, self.ie_sme)
            for i in f:
                float(i.get())
        except:
            tkinter.messagebox.showerror("Error", "Los campos de precios tienen que ser números.")
            self.ie_ee.focus_set()
            return

        for row in self.productos_db.fetch():
            if row[1].lower() == self.ie_producto.get().lower() and row[0] != self.clave:
                tkinter.messagebox.showerror("Error", "El nombre que escogiste ya está asociado a otra clave. Por favor, cambia el nombre del producto.")
                self.ie_producto.focus_set()
                self.focus_set()
                return

       # Escribir 
        self.productos_db.update(self.clave, self.ie_producto.get(), self.ie_ee.get(), self.ie_se.get(), self.ie_ema.get(), self.ie_sma.get(), self.ie_eme.get(), self.ie_sme.get(), self.stock, self.it_notas.get("1.0", tk.END))

        self.cancelar()
        self.historial()
        F_Compras.listas(self)
        self.it_productos["height"] = 15
    def cancelar(self):
    
        # Borrar
        # Ajustable
        entries = (self.ie_producto, self.ie_ee, self.ie_ema, self.ie_eme, self.ie_se, self.ie_sma, self.ie_sme)
        for e in entries:
            e.delete(0, tk.END)
        self.it_notas.delete("1.0", tk.END)

        # Actual
        labels = (self.ps, self.aas, self.bs, self.cs, self.ds, self.es, self.fs, self.gs)
        for l in labels:
            l.set("")
        self.nota.config(state = "normal")
        self.nota.delete("1.0", tk.END)
        self.nota.config(state = "disable")

        
        # Mover frames
        self.if_ajustar.grid_remove()
        self.if_buscar.grid()

        self.it_productos["height"] = 15

        self.ie_clave.delete(0, tk.END)
        self.ie_prod.delete(0, tk.END)
    def clave_prod_tmp(self, event):
        self.clave_producto_validate1()
    def prod_clave_tmp(self, event):
        self.producto_clave_validate1()
    def clave_producto_validate1(self):
        for row in self.productos_db.fetch():
            if row[0] == self.ie_clave.get():    
                self.ie_prod.delete(0, tk.END)
                self.ie_prod.insert(0, row[1])
                self.ie_prod.focusOut()
    def producto_clave_validate1(self):
        for row in self.productos_db.fetch():
            if row[1] == self.ie_prod.get():    
                self.ie_clave.delete(0, tk.END)
                self.ie_clave.insert(0, row[0])
                self.ie_clave.focusOut()


