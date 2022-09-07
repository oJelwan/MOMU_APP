import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from datetime import datetime
import time
import os
import sys
import csv

from modulo_venta import F_Cotizacion

class F_AjustarCot(F_Cotizacion):
    def __init__(self, root, Clock, AutocompleteEntry, hoy, lista_productos, lista_claves, lista_total, productos_db, tmpVent_db, tmpCot_db, clien_db, compra_db, venta_db, reg_db, cot_db, *args, **kwargs):
        super().__init__(root, Clock, AutocompleteEntry, hoy, lista_productos, lista_claves, lista_total, productos_db, tmpVent_db, tmpCot_db, clien_db, compra_db, venta_db, reg_db, cot_db, *args, **kwargs)

        self.vb_guardar["text"] = "AJUSTAR COTIZACIÓN"
        self.fvr.grid_remove()
        self.n_venta.set("No. Cot: " + self.reg_db.numero("Cotizacion"))

class F_Ventas(tk.Frame):   # Frame con registro de ventas
    def __init__(self, root,  AutocompleteEntry, hoy, lista_productos, lista_claves, lista_total, productos_db, venta_db, tmpR1_db, clien_db, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.AutocompleteEntry = AutocompleteEntry
        self.hoy = hoy
        self.lista_productos = lista_productos
        self.lista_claves = lista_claves
        self.lista_total = lista_total
        self.productos_db = productos_db
        self.venta_db = venta_db
        self.tmpR1_db = tmpR1_db
        self.clien_db = clien_db

        self.fecha = ""
        self.registro = ""

        self.lista_clientes = []
        for row in self.clien_db.fetch():
            self.lista_clientes.append(row[1])
            
        self.prueba = tk.Frame(self)
        self.prueba.grid(row = 0, column = 0, sticky = tk.N)


        # LabelFrame filtros etc
        self.vf_filtros = tk.LabelFrame(self.prueba, text = "Filtros", font = "AppleGothic 18")
        self.vf_filtros.grid(row = 0, column = 0, columnspan = 3, rowspan = 4,  padx = 16, sticky = tk.N)

        labels = ("No. Venta", "Fecha", "(AAAA/MM/DD)", "Clave", "Producto", "Cliente", "Forma de Pago")
        x = 1
        for l in labels:
            tk.Label(self.vf_filtros, text = l, font = "AppleGothic").grid(row = x, column = 0, pady = 3, padx = 5, sticky = tk.W)
            x += 1
        self.lol = tk.Label(self.vf_filtros, text = "Sucursal/Envío", font = "AppleGothic")
        self.lol.grid(row = x, column = 0, pady = 3, padx = 5, sticky = tk.W)

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
        self.ve_cliente = AutocompleteEntry(self.lista_clientes, self.vf_filtros)
        self.ve_cliente.grid(row = 6, column = 1)

        # Tipo de pago
        self.vf_fpago = tk.Frame(self.vf_filtros)
        self.vf_fpago.grid(row = 7, column = 1, columnspan = 2, rowspan = 5)
        self.t_pago = tk.IntVar()
        self.t_pago.set("0")
        self.vr_todos = tk.Radiobutton(self.vf_fpago, text = "Todos", font = "AppleGothic", variable = self.t_pago, value = 0)
        self.vr_todos.grid(row = 0, column = 0, sticky = tk.W)
        self.vr_efectivo = tk.Radiobutton(self.vf_fpago, text = "Efectivo", font = "AppleGothic", variable = self.t_pago, value = 1)
        self.vr_efectivo.grid(row = 0, column = 1, sticky = tk.W)
        self.vr_tarjeta = tk.Radiobutton(self.vf_fpago, text = "Tarjeta", font = "AppleGothic", variable = self.t_pago, value = 2)
        self.vr_tarjeta.grid(row = 1, column = 0, sticky = tk.W)
        self.vr_credito = tk.Radiobutton(self.vf_fpago, text = "Crédito", font = "AppleGothic", variable = self.t_pago, value = 3)
        self.vr_credito.grid(row = 1, column = 1, sticky = tk.W)

        # Envío o sucursal
        self.int_se = tk.IntVar()
        self.int_se.set("0")
        self.vr_ambos = tk.Radiobutton(self.vf_fpago, text = "Todos", font = "AppleGothic", variable = self.int_se, value = 0)
        self.vr_ambos.grid(row = 2, column = 0, pady = 7, sticky = tk.W)
        self.vr_suc = tk.Radiobutton(self.vf_fpago, text = "Sucursal", font = "AppleGothic", variable = self.int_se, value = 1)
        self.vr_suc.grid(row = 2, column = 1, sticky = tk.W)
        self.vr_env = tk.Radiobutton(self.vf_fpago, text = "Envío", font = "AppleGothic", variable = self.int_se, value = 2)
        self.vr_env.grid(row = 3, column = 1, sticky = tk.W)

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

        self.vt_registro = ttk.Treeview(self.vf_trees, height = 12, columns=("#1","#2","#3","#4", "#5", "#6", "#7"), style = "mystyle.Treeview")
        self.vt_registro.grid(row = 0, column = 0,  columnspan = 4, pady = 27, padx = 15, sticky = tk.E + tk.N)
        self.vt_registro.heading("#0", text = "Fecha")
        self.vt_registro.column("#0", width = 170, minwidth = 150)
        self.vt_registro.heading("#1", text = "No. Venta")
        self.vt_registro.column("#1", width = 90, minwidth = 90)
        self.vt_registro.heading("#2", text = "Cantidad")
        self.vt_registro.column("#2", width = 90, minwidth = 90)
        self.vt_registro.heading("#3", text = "Total")
        self.vt_registro.column("#3", width = 120, minwidth = 120)
        self.vt_registro.heading("#4", text = "Cliente")
        self.vt_registro.column("#4", width = 136, minwidth = 136)
        self.vt_registro.heading("#5", text = "Suc/En")
        self.vt_registro.column("#5", width = 70, minwidth = 70)
        self.vt_registro.heading("#6", text = "Pago")
        self.vt_registro.column("#6", width = 70, minwidth = 70)
        self.vt_registro.heading("#7", text = "Estado")
        self.vt_registro.column("#7", width = 70, minwidth = 70)
        self.vt_registro.bind("<Double-1>", self.seleccionado)

            
        self.vre_Total = 0
        self.vre_Cant = 0

        # Label info registro tree
        self.vs_info = tk.StringVar()
        self.vl_info = tk.Label(self.vf_trees, textvariable = self.vs_info, font = "AppleBraille 15" )
        self.vl_info.grid(row = 1, column = 3, sticky = tk.E + tk.N)



        # Treeview Detalle
        self.vt_selec = ttk.Treeview(self.vf_trees, height = 10, columns=("#1","#2","#3","#4", "#5"), style = "mystyle.Treeview")
        self.vt_selec.grid(row = 3, column = 0, padx = 15, columnspan = 4, sticky = tk.W + tk.E)
        self.vt_selec.heading("#0", text = "Clave")
        self.vt_selec.column("#0", width = 70, minwidth = 60)
        self.vt_selec.heading("#1", text = "Producto")
        self.vt_selec.column("#1", width = 300, minwidth = 200)
        self.vt_selec.heading("#2", text = "Precio")
        self.vt_selec.column("#2", width = 70, minwidth = 70)
        self.vt_selec.heading("#3", text = "Cantidad")
        self.vt_selec.column("#3", width = 70, minwidth = 70)
        self.vt_selec.heading("#4", text = "Total")
        self.vt_selec.column("#4", width = 70, minwidth = 70)
        self.vt_selec.heading("#5", text = "Lista")
        self.vt_selec.column("#5", width = 100, minwidth = 100)

        # Label detalle
        self.vs_selec = tk.StringVar()
        self.vs_selec.set("")
        self.vl_selec = tk.Label(self.vf_trees, textvariable = self.vs_selec, font = ("AppleGothic",16, "bold"))
        self.vl_selec.grid(row = 2, column = 0, sticky = tk.W, padx = 10)

        # Exportar venta
        self.vb_expd = tk.Button(self.prueba, text = "Exportar Nota", font = "AppleBraille",width = 15, height = 2, command = lambda: self.exportar_nota(self.venta_db, self.fecha, self.registro, self.vt_selec, "Venta", "ventas" ) )
        self.vb_expd.grid(row = 4, column = 2, pady = 25)

        # Cancelar venta 
        self.vb_red = tk.Button(self.prueba, text = "Cancelar Nota", font = "AppleBraille", fg = "red", width = 15, height = 2, command = lambda: self.cancelar_nota(self.venta_db, self.fecha, self.registro, self.vt_selec))
        self.vb_red.grid(row = 5, column = 2)

    def historial(self):
        self.limpiar()
        for row in self.venta_db.fetch():
            self.tmpR1_db.insert(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
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
        self.vre_Cant = 0
        self.vre_Total = 0
     # 0. Borrar nuestra db provisional
        self.limpiar()
     # 1. No. Venta
        try:
            self.ve_numventa.get()[0]
            for row in self.venta_db.fetch():
                if str(row[1]) == str(self.ve_numventa.get()):
                    self.tmpR1_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8], row[9], row[10], row[11])
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
                    self.tmpR1_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8], row[9], row[10], row[11])
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
                    self.tmpR1_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8], row[9], row[10], row[11])
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
                    self.tmpR1_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8], row[9], row[10], row[11])
                año_db = []
     # 3. Clave
        try:
            # Revisar que nada esté vacío
            self.ve_clave.get()[0]  
            try:
                self.tmpR1_db.fetch()[0]    # Ver si ya hay algo
                for row in self.tmpR1_db.fetch():
                    if row[2].lower() != self.ve_clave.get().lower():
                        self.tmpR1_db.remove_product(row[2])

            except: # Si no, usar la de ventas
                for row in self.venta_db.fetch():
                    if row[2].lower() == self.ve_clave.get().lower():
                        self.tmpR1_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8], row[9], row[10], row[11])

        except:
            pass
     # 4. Producto
        try:
            # Revisar que nada esté vacío
            self.ve_producto.get()[0]  
            try:
                self.tmpR1_db.fetch()[0]    # Ver si ya hay algo
                for row in self.tmpR1_db.fetch():
                    if row[3].lower() != self.ve_producto.get().lower():
                        self.tmpR1_db.remove_product(row[2])
                        
            except: # Si no, usar la de ventas
                for row in self.venta_db.fetch():
                    if row[3].lower() == self.ve_producto.get().lower():
                        self.tmpR1_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8], row[9], row[10], row[11])

        except:
            pass
     # 5. Cliente
        try:
            # Revisar que nada esté vacío
            self.ve_cliente.get()[0]  
            try:
                self.tmpR1_db.fetch()[0]    # Ver si ya hay algo
                for row in self.tmpR1_db.fetch():
                    if row[7].lower() != self.ve_cliente.get().lower():
                        self.tmpR1_db.remove(row[1])
                        
            except: # Si no, usar la de ventas
                for row in self.venta_db.fetch():
                    if row[7].lower() == self.ve_cliente.get().lower():
                        self.tmpR1_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8], row[9], row[10], row[11])

        except:
            pass
     # 6. Tipo de pago
        # 6.0 Todos
        if self.t_pago.get() == 0:
            try:
                self.tmpR1_db.fetch()[0]
                pass
            except:
                for row in self.venta_db.fetch():
                    self.tmpR1_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8], row[9], row[10], row[11])

        # 6.1 Efectivo
        if self.t_pago.get() == 1:
            try:
                self.tmpR1_db.fetch()[0]
                for row in self.tmpR1_db.fetch():
                    if row[10] != "Efectivo":
                        self.tmpR1_db.remove(row[1])
            except:
                for row in self.venta_db.fetch():
                    if row[10] == "Efectivo":
                        self.tmpR1_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8], row[9], row[10], row[11])
        # 6.1 Tarjeta
        elif self.t_pago.get() == 2:
            try:
                self.tmpR1_db.fetch()[0]
                for row in self.tmpR1_db.fetch():
                    if row[10] != "Tarjeta":
                        self.tmpR1_db.remove(row[1])
            except:
                for row in self.venta_db.fetch():
                    if row[10] == "Tarjeta":
                        self.tmpR1_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8], row[9], row[10], row[11])
        # 6.1 Crédito
        elif self.t_pago.get() == 3:
            try:
                self.tmpR1_db.fetch()[0]
                for row in self.tmpR1_db.fetch():
                    if row[10] != "Crédito":
                        self.tmpR1_db.remove(row[1])
            except:
                for row in self.venta_db.fetch():
                    if row[10] == "Crédito":
                        self.tmpR1_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8], row[9], row[10], row[11])
     # 7. Sucursal o Envío
        # 7.0 Ambas
        if self.int_se.get() == 1:
            try:
                self.tmpR1_db.fetch()[0]
                pass
            except:
                for row in self.venta_db.fetch():
                    self.tmpR1_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8], row[9], row[10], row[11])
        # 7.1 Sucursal
        if self.int_se.get() == 1:
            try:
                self.tmpR1_db.fetch()[0]
                for row in self.tmpR1_db.fetch():
                    if row[8] != "Sucursal":
                        self.tmpR1_db.remove(row[1])
            except:
                for row in self.venta_db.fetch():
                    if row[8] == "Sucursal":
                        self.tmpR1_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8], row[9], row[10], row[11])
        # 7.1 Envío
        elif self.int_se.get() == 2:
            try:
                self.tmpR1_db.fetch()[0]
                for row in self.tmpR1_db.fetch():
                    if row[8] != "Envío":
                        self.tmpR1_db.remove(row[1])
            except:
                for row in self.venta_db.fetch():
                    if row[8] == "Envío":
                        self.tmpR1_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8], row[9], row[10], row[11])
     # Paint
        self.paint()
        self.vs_info.set("Total de artículos: %d. Total de dinero: $%d" % (self.vre_Cant, self.vre_Total))
    ##### observar ####   
    def limpiar(self):
        self.tmpR1_db.deleteall()
        for p in self.vt_registro.get_children():
            self.vt_registro.delete(p)
        for p in self.vt_selec.get_children():
            self.vt_selec.delete(p)
        self.vs_selec.set("")
        self.vs_info.set("")
        self.vre_Total = 0
        self.vre_Cant = 0
    def paint(self):
        try:
            tmp = self.tmpR1_db.inverse_fetch()[0][1]           
            tmptot = 0
            tmpcant = 0
            f = ""
            seven = ""
            eight = ""
            ten = ""
            ele = ""
            for row in self.tmpR1_db.inverse_fetch():

                if row[1] == tmp:
                    tmptot += row[6]
                    tmpcant += row[5]
                    f = row[0]
                    seven = row[7]
                    eight = row[8]
                    ten = row[10]
                    ele = row[11]

                    # Solo se suma al total si no está cacelada
                    if row[11] == "VEN":
                        self.vre_Total += row[6]
                        self.vre_Cant += row[5]
                else:
                    self.vt_registro.insert("", "end", text = f, values =("No. " + str(tmp), round(tmpcant, 3), "$" + str(round(tmptot, 3)), seven, eight, ten, ele))
                    tmp = row[1]
                    tmptot = row[6]
                    tmpcant = row[5]
                    f = row[0]
                    seven = row[7]
                    eight = row[8]
                    ten = row[10]
                    ele = row[11]

                   # Solo se suma al total si no está cacelada
                    if row[11] == "VEN":
                        self.vre_Total += row[6]
                        self.vre_Cant += row[5]

            self.vt_registro.insert("", "end", text = f, values =("No. " + str(tmp), round(float(tmpcant), 3), "$" + str(round(float(tmptot),3)), seven, eight, ten, ele))
            self.vs_info.set("Total de artículos: %s. Total de dinero: $%s" % (round(self.vre_Cant, 3), round(self.vre_Total, 3)))
        except:
            pass
    def seleccionado(self, event):
        self.fecha = self.vt_registro.item(self.vt_registro.selection())["text"]
        self.registro = self.vt_registro.item(self.vt_registro.selection())["values"][0]
        total = 0

        for row in self.vt_selec.get_children():
            self.vt_selec.delete(row)

        for row in self.venta_db.fetch():
            if ("No. " + str(row[1])) == self.registro:
                self.vt_selec.insert("", "end",text = row[2],  values = (row[3],"$" + str(row[4]), row[5], "$"+ str(row[6]), row[9]) )
                total += row[6]

        self.vs_selec.set("Detalle de venta "+ self.registro + ". Total de nota: $" + str(round(total, 3)))
    def exportar_nota(self, db, fecha, registro, tree, tipo, folder):

        tmp = tipo + "_" + registro + ".csv"
        # filename = os.path.abspath(
        # os.path.join(sys.executable + "/archivos_momu/", '..', '..', '..', '..','..', "archivos_momu"))
        # filename = os.path.join(filename +  "/" + folder + '/',tmp)
        filename = os.path.join(os.path.expanduser('~'),'Documents/momu_la_bola/archivos_momu/' + folder + '/',tmp)
        print(filename)
        total_nota = 0
        newfile = not os.path.exists(filename)    
        data = {}
        status = ""

        # No hacer nada si no hay nada
        x = 0
        for leaves in tree.get_children():
            x += 1
        if x == 0:
            return


        with open(filename, 'a', encoding='utf_8_sig', newline='') as fh:	
            csvwriter= csv.DictWriter(fh, fieldnames=("Fecha", "Registro", "Clave", "Producto", "Precio", "Cantidad", "Total", "Cliente", "S/E", "Lista", "Pago", "Status"))
            if newfile:
                csvwriter.writeheader()

            # Escribir
            for row in db.fetch():

                if "No. " + str(row[1]) == self.registro:
                    # Agregar a .csv
                    data["Fecha"] = self.fecha
                    data["Registro"] = self.registro
                    data["Clave"] = row[2]
                    data["Producto"] = row[3]
                    data["Precio"] = row[4]
                    data["Cantidad"] = row[5]
                    data["Total"] = row[6]
                    data["Cliente"] = row[7]
                    data["S/E"] = row[8]
                    data["Lista"] = row[9]
                    data["Pago"] = row[10]
                    status = row[11]

                    total_nota += row[6]

                    csvwriter.writerow(data)

            # Solo generar un registro si sí hay algo que vender y si hay suficiente!!
                    # Añadir fila del *total* de cada registro
            data = {}
            data["Fecha"] = self.fecha
            data["Registro"] = self.registro
            data["Clave"] = "Total "
            data["Producto"] = "de nota número " + self.registro
            data["Total"] = round(total_nota, 3)
            data["Status"] = status
            
            csvwriter.writerow(data)

        os.chmod(filename, 0o444)
        tkinter.messagebox.showinfo("Exportado", "Exportación exitosa. Se encontrará en un archivo con nombre: " + tipo + "_" + self.registro + ".csv")
        self.focus()
        for c in self.vt_selec.get_children():
            self.vt_selec.delete(c)
        self.vs_selec.set("")
    def cancelar_nota(self, db, fecha, registro, tree): 
        
        if tkinter.messagebox.askyesno("Cancelar", "¿Segura que quieres cancelar la nota? Se marcará como cancelada y el stock de los productos se ajustará."):
            for row in db.fetch():
                if "No. " + str(row[1]) == registro:  # Cambiar el status de los productos de la nota con dicho número
                    db.cancelado(row[0], row[1], row[2] )
                    # Y luego incrementar el stock de dichos productos
                    for pro in self.productos_db.fetch():
                        if row[2] == pro[0]:
                            self.productos_db.update(pro[0], pro[1], pro[2], pro[3], pro[4], pro[5], pro[6], pro[7], pro[8] + row[5], pro[9])
            
            for c in self.vt_selec.get_children():
                self.vt_selec.delete(c)
            self.vs_selec.set("")
            self.filtrar()

class F_Cotizaciones(F_Ventas):   # Frame con registro de cotizaciones
    def __init__(self, root,  AutocompleteEntry, hoy, lista_productos, lista_claves, lista_total, productos_db, cot_db, tmpR2_db, clien_db ,venta_db, reg_db, f_venta, *args, **kwargs):
        super().__init__(root,  AutocompleteEntry, hoy, lista_productos, lista_claves, lista_total, productos_db, cot_db, tmpR2_db, clien_db, f_venta, *args, **kwargs)

        # Algunos ajustes...  
        self.venta_db = cot_db
        self.tmpR1_db = tmpR2_db
        self.v_db = venta_db
        self.reg_db = reg_db
        self.f_venta = f_venta

        self.vt_registro.heading("#1", text = "No. Cot.")
        self.vt_registro.column("#3", width = 100, minwidth = 100)

        self.labels = ("No. Cotización", "Fecha", "(AAAA/MM/DD)", "Clave", "Producto", "Cliente")
        x = 1
        for l in self.labels:
            tk.Label(self.vf_filtros, text = l, font = "AppleGothic").grid(row = x, column = 0, pady = 3, padx = 5, sticky = tk.W)
            x += 1

        self.a = tk.Label(self.vf_filtros, text = "Forma de Pago", font = "AppleGothic")
        self.a.grid(row = x, column = 0, pady = 3, padx = 5, sticky = tk.W)

        self.b = tk.Label(self.vf_filtros, text = "Sucursal/Envío", font = "AppleGothic")
        self.b.grid(row = x+1, column = 0, pady = 3, padx = 5, sticky = tk.W)

        self.vb_expd.grid(row = 4, column = 1, pady = 25, sticky = tk.S)

        # Exportar cotizacion
        self.vb_expd = tk.Button(self.prueba, text = "Exportar Cotización", font = "AppleBraille", width = 20, height = 2, command = lambda: self.exportar_nota(self.venta_db, self.fecha, self.registro, self.vt_selec, "Cotización", "cotizaciones") )
        self.vb_expd.grid(row = 4, column = 1, pady = 25)

        # Vender cotización
        self.vb_vencot = tk.Button(self.prueba, text = "Vender Cotización", font = "AppleBraille", fg = "green", width = 20, height = 2, command = lambda: self.vender_cotizacion(self.v_db))
        self.vb_vencot.grid(row = 4, column = 2)

        # Eliminar cotización
        self.vb_red = tk.Button(self.prueba, text = "Eliminar Cotización", font = "AppleBraille", fg = "red", width = 20, height = 2, command = self.eliminar_cotizacion)
        self.vb_red.grid(row = 5, column = 2)        
        
        # Ajustar cotizacion
        self.vb_ajcot = tk.Button(self.prueba, text = "Ajustar Cotización", font = "AppleBraille", fg = "violet", width = 20, height = 2, command = self.ajustar_cotizacion)
        self.vb_ajcot.grid(row = 5, column = 1)
    def eliminar_cotizacion(self): 
        # Ver si hay algo seleccionado
        x = 0
        for l in self.vt_selec.get_children():
            x += 1
        if x == 0:
            tkinter.messagebox.showinfo("Eliminar", "Selecciona una cotización a eliminar." )
            self.focus() 
            return

        if tkinter.messagebox.askyesno("Eliminar", "¿Segura que quieres eliminar la cotización?"):
            for row in self.venta_db.fetch():
                if "No. " + str(row[1]) == self.registro:  
                    self.venta_db.remove(row[1])
            
            for c in self.vt_selec.get_children():
                self.vt_selec.delete(c)
            self.vs_selec.set("")
            self.filtrar()
            self.focus()
    def vender_cotizacion(self, db_final):
        x = 0
        for l in self.vt_selec.get_children():
            x += 1
        if x == 0:
            tkinter.messagebox.showinfo("Vender", "Selecciona una cotización a vender." )
            self.focus() 
            return
        datestring = datetime.today().strftime("%Y/%m/%d -%H:%M")
        enough_lista = []
       
        # No hacer nada si no hay nada
        x = 0
        for leaves in self.vt_selec.get_children():
            x += 1
        if x == 0:
            return


        # Revisar primero si hay de todos los productos y agregarlos a una lista!!
        for stock in self.productos_db.fetch():
            for row in self.venta_db.fetch():   # cot_db
                if "No. " + str(row[1]) == self.registro:
                    if stock[0] == row[2]:
                        if row[5] > stock[8]:       # Si se quiere vernder más de lo que hay. 
                            enough_lista.append(row[3])     # Habrá suficiente de todo si la lista está vacía

        if len(enough_lista) != 0:      # No se hace nada hasta que estemos seguros de que hay algo que escribir. 
            tkinter.messagebox.showinfo("Error", "No hay suficiente de: %s  en inventario." % enough_lista) # ** decir qué productos **
            self.focus() 
            return

        # Significa que sí hay de todo y podemos proseguir a hacer la venta. 
            # Escribir
        reg = self.reg_db.accion("Venta")  
        for row in self.venta_db.fetch():   # cot_db
            if "No. " + str(row[1]) == self.registro:
                # venta_db , pero venta_db REAL
                db_final.insert(datestring, reg, row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], "VEN")
    
                # Solo se decrementa del stock si sí es venta
                for stock in self.productos_db.fetch(): 
                    if stock[0] == row[2]:
                        # Ajustar stock
                        self.productos_db.update(stock[0], stock[1], stock[2], stock[3], stock[4], stock[5], stock[6], stock[7], stock[8] - row[5], stock[9] )    # Decrementar del stock

                # Remover de cot_db, llamada venta_db
                self.venta_db.remove(row[1])

        tkinter.messagebox.showinfo("Venta", "Venta guardada con éxito." )
        self.filtrar()
        self.focus() 
        self.ve_numventa.focus() 


        for c in self.vt_selec.get_children():
            self.vt_selec.delete(c)
        self.vs_selec.set("")
    def ajustar_cotizacion(self):

        # Ver si hay algo seleccionado
        x = 0
        for leaves in self.vt_selec.get_children():
            x += 1
        if x == 0:
            tkinter.messagebox.showinfo("Seleccionar", "Selecciona una cotización a ajustar." )
            self.focus() 
            return


        # Nueva ventana
        ajustar_window = tk.Toplevel(self)
        ajustar_window.title("Ajustar Cotización")
        ajustar_window.transient(self) #set to be on top of the main window
        ajustar_window.grab_set() #hijack all commands from the master (clicks on the main window are ignored)
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        ajustar_window.geometry("+%d+%d" % (w/12 , h/8))

        # Heredar
        f_AjustarCot = F_AjustarCot(ajustar_window, self.f_venta.Clock, self.f_venta.AutocompleteEntry, self.f_venta.hoy, self.f_venta.lista_productos, self.f_venta.lista_claves, self.f_venta.lista_total, self.f_venta.productos_db, self.f_venta.tmpVent_db, self.f_venta.tmpCot_db, self.f_venta.clien_db, self.f_venta.compra_db ,self.f_venta.venta_db, self.f_venta.reg_db, self.f_venta.cot_db,)
        f_AjustarCot.grid(row = 0 , column = 0 )

        # Agregar productos en cotizacion pasada
        f_AjustarCot.vt_info.delete("1.0", tk.END)
        # Borrar tmpCot_db
        for row in f_AjustarCot.tmpCot_db.fetch():
            f_AjustarCot.tmpCot_db.remove(row[0])
        # Borrar árbol
        leaves = f_AjustarCot.vt_tabla.get_children()    
        for row in leaves:
            f_AjustarCot.vt_tabla.delete(row)
        # Pintar de nuevo con lo seleccionado
        for row in self.venta_db.fetch():
            if ("No. " + str(row[1])) == self.registro:
                f_AjustarCot.tmpCot_db.insert(row[2], row[3], row[4], row[5], row[6], row[7] )
        f_AjustarCot.paint()

        def cerrar():
            ajustar_window.grab_release()
            ajustar_window.destroy()
            self.focus_set()
            self.filtrar()
        def ajustarCot():
            f_AjustarCot.venta_cotizacion(f_AjustarCot.cot_db, "Cotizacion")
            self.filtrar()
            cerrar()
        def cancelarAjustar():
            try:        # Only do if list is not empty
                f_AjustarCot.tmpCot_db.fetch()[0]
                result = tkinter.messagebox.askyesno("Cancelar", "¿Segura que quieres cancelar? No se guardarán los cambios a la cotización.")
                if result:
                    f_AjustarCot.vt_info.delete("1.0", tk.END)
                    # Borrar tmpCot_db
                    for row in f_AjustarCot.tmpCot_db.fetch():
                        f_AjustarCot.tmpCot_db.remove(row[0])
                    # Borrar árbol
                    leaves = f_AjustarCot.vt_tabla.get_children()    
                    for row in leaves:
                        f_AjustarCot.vt_tabla.delete(row)
                    f_AjustarCot.focus() 
                    f_AjustarCot.ve_prod.focus() 
                    f_AjustarCot.vst_total.set("TOTAL ---- $ 0")
                f_AjustarCot.vt_info.config(state = "normal")
                f_AjustarCot.vt_info.delete("1.0", tk.END)
                f_AjustarCot.vt_info.config(state = "disable")
                cerrar()
            except:
                pass

        ajustar_window.protocol("WM_DELETE_WINDOW", lambda: cerrar())
        f_AjustarCot.vb_guardar["command"] = ajustarCot
        f_AjustarCot.vb_cancelar["command"] = cancelarAjustar
        



