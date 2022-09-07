from cgi import print_arguments
from stat import FILE_ATTRIBUTE_SYSTEM
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from datetime import datetime
import time
import os
import csv
from warnings import filters

from modulo_registro import F_Ventas
## §§§§§§
class F_reportes(tk.Frame):   
    def __init__(self, root,  AutocompleteEntry, hoy, lista_productos, lista_claves, lista_total, venta_db, cot_db, productos_db, compra_db, clien_db, reg_db, reporte_db, sucursal, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.sucursal = sucursal
        self.AutocompleteEntry = AutocompleteEntry
        self.hoy = hoy
        self.lista_productos = lista_productos
        self.lista_claves = lista_claves
        self.lista_total = lista_total
        self.venta_db = venta_db
        self.cot_db = cot_db
        self.productos_db = productos_db
        self.compra_db = compra_db
        self.clien_db = clien_db
        self.reg_db = reg_db
        self.reporte_db = reporte_db

        self.lista_clientes = []
        for row in self.clien_db.fetch():
            self.lista_clientes.append(row[1])

        self.fecha = ""
        self.registro = ""


        self.prueba = tk.Frame(self)
        self.prueba.grid(row = 0, column = 0, sticky = tk.N)


        # LabelFrame filtros etc
        self.vf_filtros = tk.LabelFrame(self.prueba, text = "Filtros", font = "AppleGothic 18")
        self.vf_filtros.grid(row = 0, column = 0, columnspan = 3, rowspan = 4,  padx = 16, sticky = tk.N)

        labels = ("Número: ", "Fecha: ", "(AAAA/MM/DD)", "Clave:", "Producto:")
        x = 1
        for l in labels:
            tk.Label(self.vf_filtros, text = l, font = "AppleGothic").grid(row = x, column = 0, pady = 3, padx = 5, sticky = tk.W)
            x += 1

        # Numero de venta       
        self.ve_numventa = tk.Entry(self.vf_filtros)
        self.ve_numventa.grid(row = 1, column = 1)

        # Tipo: Venta, Cotizacion o Compra
        self.vf_status = tk.Frame(self.vf_filtros)
        self.vf_status.grid(row = 1, column = 3, columnspan = 3)

        self.vl_status = tk.Label(self.vf_filtros, text ="Tipo", font="AppleGothic")
        self.vl_status.grid(row = 1, column = 2, padx=10, sticky=tk.W)

        self.status = tk.IntVar()
        self.status.set("0")
        self.vr_venta = tk.Radiobutton(self.vf_status, text = "Venta", font = "AppleGothic", variable = self.status, value = 0, command = self.check_tipo)
        self.vr_venta.grid(row = 0, column = 2, sticky = tk.W)
        self.vr_cot = tk.Radiobutton(self.vf_status, text = "Cotización", font = "AppleGothic", variable = self.status, value = 1, command = self.check_tipo)
        self.vr_cot.grid(row = 0, column = 3, sticky = tk.W)
        self.vr_compra = tk.Radiobutton(self.vf_status, text = "Compra", font = "AppleGothic", variable = self.status, value = 2, command = self.check_tipo)
        self.vr_compra.grid(row = 1, column = 2, sticky = tk.W)

        # Intervalo  
        self.vf_intervalo = tk.Frame(self.vf_filtros)
        self.vf_intervalo.grid(row = 2, column = 1, columnspan = 3, sticky = tk.W)

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
        self.vl_cliente = tk.Label(self.vf_filtros, text = "Cliente", font = "AppleGothic")
        self.vl_cliente.grid(row = 6, column = 0, pady = 3, padx = 5, sticky = tk.W)
        self.ve_cliente = AutocompleteEntry(self.lista_clientes, self.vf_filtros)
        self.ve_cliente.grid(row = 6, column = 1)

            # Nuevo filtro - tipo pago y envio sucursal

        # Tipo de pago
        self.vf_fpago = tk.Frame(self.vf_filtros)
        self.vf_fpago.grid(row = 7, column = 0, columnspan = 2, rowspan = 5, sticky = tk.W)

        self.vl_tpago = tk.Label(self.vf_fpago, text = "Tipo Pago: ", font = "AppleGothic")
        self.vl_tpago.grid(row = 0, column = 0, pady = 3, padx = 5, sticky = tk.W)
        self.t_pago = tk.IntVar()
        self.t_pago.set("0")
        self.vr_todos = tk.Radiobutton(self.vf_fpago, text = "Todos", font = "AppleGothic", variable = self.t_pago, value = 0)
        self.vr_todos.grid(row = 0, column = 1, sticky = tk.W)
        self.vr_efectivo = tk.Radiobutton(self.vf_fpago, text = "Efectivo", font = "AppleGothic", variable = self.t_pago, value = 1)
        self.vr_efectivo.grid(row = 0, column = 2, sticky = tk.W)
        self.vr_tarjeta = tk.Radiobutton(self.vf_fpago, text = "Tarjeta", font = "AppleGothic", variable = self.t_pago, value = 2)
        self.vr_tarjeta.grid(row = 1, column = 1, sticky = tk.W)
        self.vr_credito = tk.Radiobutton(self.vf_fpago, text = "Crédito", font = "AppleGothic", variable = self.t_pago, value = 3)
        self.vr_credito.grid(row = 1, column = 2, sticky = tk.W)

        # Envío o sucursal
        self.vl_se = tk.Label(self.vf_fpago, text = "Sucursal/Envío: ", font = "AppleGothic")
        self.vl_se.grid(row = 2, column = 0, pady = 3, padx = 5, sticky = tk.W)
        self.int_se = tk.IntVar()
        self.int_se.set("0")
        self.vr_ambos = tk.Radiobutton(self.vf_fpago, text = "Todos", font = "AppleGothic", variable = self.int_se, value = 0)
        self.vr_ambos.grid(row = 2, column = 1, pady = 7, sticky = tk.W)
        self.vr_suc = tk.Radiobutton(self.vf_fpago, text = "Sucursal", font = "AppleGothic", variable = self.int_se, value = 1)
        self.vr_suc.grid(row = 2, column = 2, sticky = tk.W)
        self.vr_env = tk.Radiobutton(self.vf_fpago, text = "Envío", font = "AppleGothic", variable = self.int_se, value = 2)
        self.vr_env.grid(row = 3, column = 2, sticky = tk.W)

        # Añadir filtros
        self.vb_filtrar = tk.Button(self.vf_filtros, text = "Filtrar", width = 8, height = 1, fg = "green", font = "AppleGothic 15", command = self.filtrarPrevio)
        self.vb_filtrar.grid(row = 6, column = 3, pady = 8, padx = 3, sticky = tk.E)

        # Frame trees etc.
        self.vf_trees = tk.Frame(self)
        # self.vf_trees.grid(row = 0, column = 3)

        # Treeview Registro
        self.style = ttk.Style()
        self.style.configure("mystyle.Treeview", highlightthickness=0, bd=0, rowheight = 20, font=('AppleGothic', 13)) # Modify the font of the body
        self.style.configure("mystyle.Treeview.Heading", font=('AppleBraille', 15,'bold')) # Modify the font of the headings

        self.vt_registro = ttk.Treeview(self.vf_trees, height = 12, columns=("#1","#2","#3","#4", "#5", "#6", "#7", "#8", "#9", "#10", "#11","#12", "#13"), style = "mystyle.Treeview")
        self.vt_registro.grid(row = 0, column = 0,  columnspan = 4, pady = 27, padx = 15, sticky = tk.E + tk.N)
        self.vt_registro.heading("#0", text = "Fecha")
        self.vt_registro.column("#0", width = 170, minwidth = 150)
        self.vt_registro.heading("#1", text = "Número")
        self.vt_registro.column("#1", width = 70, minwidth = 70)
        self.vt_registro.heading("#2", text = "Clave")
        self.vt_registro.column("#2", width = 70, minwidth = 70)
        self.vt_registro.heading("#3", text = "Producto")
        self.vt_registro.column("#3", width = 180, minwidth = 100)
        self.vt_registro.heading("#4", text = "Precio")
        self.vt_registro.column("#4", width = 80, minwidth = 80)
        self.vt_registro.heading("#5", text = "Cantidad")
        self.vt_registro.column("#5", width = 80, minwidth = 80)
        self.vt_registro.heading("#6", text = "Subtotal")
        self.vt_registro.column("#6", width = 100, minwidth = 100)
        self.vt_registro.heading("#7", text = "Proveedor")
        self.vt_registro.column("#7", width = 140, minwidth = 100)
        self.vt_registro.heading("#8", text = "Notas")
        self.vt_registro.column("#8", width = 100, minwidth = 100)
        self.vt_registro.heading("#9", text = "Cliente")
        self.vt_registro.column("#9", width = 120, minwidth = 100)
        self.vt_registro.heading("#10", text = "Suc/En")
        self.vt_registro.column("#10", width = 70, minwidth = 70)
        self.vt_registro.heading("#11", text = "Lista")
        self.vt_registro.column("#11", width = 70, minwidth = 70)
        self.vt_registro.heading("#12", text = "Pago")
        self.vt_registro.column("#12", width = 70, minwidth = 70)        
        self.vt_registro.heading("#13", text = "Estado")
        self.vt_registro.column("#13", width = 70, minwidth = 70)
        # self.vt_registro.bind("<Double-1>", self.seleccionado)

            
        self.vre_Total = 0
        self.vre_Cant = 0

        # Label info registro tree
        self.vs_info = tk.StringVar()
        self.vl_info = tk.Label(self.vf_trees, textvariable = self.vs_info, font = "AppleBraille 15" )
        self.vl_info.grid(row = 1, column = 3, sticky = tk.E + tk.N)

            # Botones
        # Exportar
        self.vb_exportar = tk.Button(self.vf_trees, text = "Exportar", width = 8, height = 1, fg = "red", font = "AppleGothic 15", command = self.exportar)
        self.vb_exportar.grid(row = 2, column = 1, pady = 8, sticky = tk.E) 
        # Limpiar
        self.vb_regresar = tk.Button(self.vf_trees, text = "Regresar", width = 8, height = 1, font = "AppleGothic 15", command = self.regresar)
        self.vb_regresar.grid(row = 2, column = 2, pady = 8, sticky = tk.E) 
    def exportar(self):
        if self.status.get() == 0:
            tipo = "ReporteVentas"
            folder = "reportes"
        elif self.status.get() == 1:
            tipo = "ReporteCotización"
            folder = "reportes"
        else:
            tipo = "ReporteCompra"
            folder = "reportes"

        registro = self.reg_db.accion("Reporte")

        tmp = tipo + "_" + registro + ".csv"
        filename = os.path.join(os.path.expanduser('~'),'Documents/' + self.sucursal + '/archivos_momu/' + folder + '/',tmp)
        total_neto = 0
        newfile = not os.path.exists(filename)    
        data = {}

        # Pintar si es COMPRA
        if self.status.get() == 2:
            with open(filename, 'a', encoding='utf_8_sig', newline='') as fh:	
                csvwriter= csv.DictWriter(fh, fieldnames=("Fecha", "No.", "Clave", "Producto", "Precio/u", "Cantidad", "Total", "Proveedor", "Notas"))
                if newfile:
                    csvwriter.writeheader()
                # Escribir
                for row in self.reporte_db.fetch():
                    # Agregar a .csv
                    data["Fecha"] = row[0]
                    data["No."] = row[1]
                    data["Clave"] = row[2]
                    data["Producto"] = row[3]
                    data["Precio/u"] = row[4]
                    data["Cantidad"] = row[5]
                    data["Total"] = row[6]
                    data["Proveedor"] = row[7]
                    data["Notas"] = row[8]

                    total_neto += row[6]

                    csvwriter.writerow(data)

                # Añadir fila del *total* de cada registro
                data = {}
                data["Fecha"] = self.hoy
                data["Clave"] = "Total "
                data["Producto"] = "de reporte número " + str(registro)
                data["Total"] = round(total_neto, 3)
                csvwriter.writerow(data)

                tkinter.messagebox.showinfo("Exportado", "Exportación exitosa. Se encontrará en un archivo con nombre: " + tipo + "_" + registro + ".csv")
                self.focus()


        # O si es VENTA o COTIZACION 
        else:
            with open(filename, 'a', encoding='utf_8_sig', newline='') as fh:	
                csvwriter= csv.DictWriter(fh, fieldnames=("Fecha", "No.", "Clave", "Producto", "Precio", "Cantidad", "Total", "Cliente", "S/E", "Lista", "Pago", "Status"))
                if newfile:
                    csvwriter.writeheader()

                # Escribir
                for row in self.reporte_db.fetch():
                    # Agregar a .csv
                    data["Fecha"] = row[0]
                    data["No."] = row[1]
                    data["Clave"] = row[2]
                    data["Producto"] = row[3]
                    data["Precio"] = row[4]
                    data["Cantidad"] = row[5]
                    data["Total"] = row[6]
                    data["Cliente"] = row[13]
                    data["S/E"] = row[9]
                    data["Lista"] = row[10]
                    data["Pago"] = row[11]
                    data["Status"] = row[12]

                    if row[12] == "VEN":
                        total_neto += row[6]

                    csvwriter.writerow(data)

                # Añadir fila del *total* de cada registro
                data = {}
                data["Fecha"] = self.hoy
                data["Clave"] = "Total "
                data["Producto"] = "de reporte número " + str(registro)
                data["Total"] = total_neto
                csvwriter.writerow(data)

                tkinter.messagebox.showinfo("Exportado", "Exportación exitosa. Se encontrará en un archivo con nombre: " + tipo + "_" + registro + ".csv")
                self.focus()
    def regresar(self):
        self.limpiar()
        self.vf_trees.grid_remove()
        self.prueba.grid(row = 0, column = 0, sticky = tk.N)
    def check_fecha(self):
        if self.intervalo.get() == 0:
            self.ve_fecha.grid_remove()
        else:
            self.ve_fecha.grid(row = 3, column = 1)
    def check_tipo(self):
        if self.status.get() == 2:
            self.vf_fpago.grid_remove()
        else:
            self.vf_fpago.grid(row = 7, column = 0, columnspan = 2, rowspan = 5, sticky = tk.W)
    def filtrarPrevio(self):
        # self.prueba.grid_remove()
        # self.vf_trees.grid(row = 0, column = 3)

        # Si es venta
        if self.status.get() == 0:
            self.filtrarVenCot(self.venta_db)
        # Si es cotizacion
        elif self.status.get() == 1:
            self.filtrarVenCot(self.cot_db)
        # O si es compra
        else:
            self.filtrarCompras()
    # Tipo de paint sera 0 o 1
    def paint(self, tipo):
        try:
            self.reporte_db.fetch()[0]
            # If VENTA o COT 
            if tipo ==  0:
                for row in self.reporte_db.inverse_fetch():
                    self.vt_registro.insert("", "end", text = row[0], values =("No. " + str(row[1]), row[2], row[3], "$" + str(round(row[4], 3)), row[5], "$" + str(round(row[6], 3)),"", "", row[13], row[9], row[10], row[11], row[12]))
                    # Solo se suma al total si no está cacelada
                    if row[12] == "VEN":
                        self.vre_Total += row[6]
                        self.vre_Cant += row[5]
                    if row[12] == "COT":
                        self.vl_info.grid_remove()

                self.prueba.grid_remove()       

                self.vt_registro.column("#9", width = 120, minwidth = 100)
                self.vt_registro.column("#10", width = 70, minwidth = 70)
                self.vt_registro.column("#11", width = 70, minwidth = 70)
                self.vt_registro.column("#12", width = 70, minwidth = 70)
                self.vt_registro.column("#13", width = 70, minwidth = 70)
                self.vt_registro.column("#7", width = 0, minwidth = 0)
                self.vt_registro.column("#8", width = 0, minwidth = 0)

                self.vf_trees.grid(row = 0, column = 3)
                self.vs_info.set("Total de artículos: %s. Total de dinero: $%s" % (round(self.vre_Cant, 3), round(self.vre_Total, 3)))
            # IF COMPRA
            else:
                for row in self.reporte_db.inverse_fetch():
                    self.vt_registro.insert("", "end", text = row[0], values =("No. " + str(row[1]), row[2], row[3], "$" + str(round(row[4], 3)), row[5], "$" + str(round(row[6], 3)), row[7], row[8], "", "", "","",""))
                    self.vre_Total += row[6]
                    self.vre_Cant += row[5]

                self.prueba.grid_remove()       

                self.vt_registro.column("#9", width = 0, minwidth = 0)
                self.vt_registro.column("#10", width = 0, minwidth = 0)
                self.vt_registro.column("#11", width = 0, minwidth = 0)
                self.vt_registro.column("#12", width = 0, minwidth = 0)
                self.vt_registro.column("#13", width = 0, minwidth = 0)
                self.vt_registro.column("#7", width = 140, minwidth = 100)
                self.vt_registro.column("#8", width = 250, minwidth = 100)

                self.vf_trees.grid(row = 0, column = 3)
                self.vs_info.set("Total de artículos: %s. Total de dinero: $%s" % (round(self.vre_Cant, 3), round(self.vre_Total, 3)))
        except:
            print("exception paint reportes")
            print(Exception)
            pass
    def limpiar(self):
        # Limpiar db
        self.reporte_db.deleteall()
        for row in self.reporte_db.fetch():
            self.reporte_db.removeu(row[1], row[2])
        for p in self.vt_registro.get_children():
            self.vt_registro.delete(p)
        # Limpiar Labels
        self.vs_info.set("")
        self.vre_Total = 0
        self.vre_Cant = 0
    def filtrarVenCot(self, db):
     # Variables
        self.vs_info.set("")
        self.vre_Cant = 0
        self.vre_Total = 0
        filter = " "
        filtersmt = False
        both = False
     # 0. Borrar nuestra db provisional
        self.limpiar()
     # 1. No. Venta
        try:
            self.ve_numventa.get()[0]
            for row in db.fetch():
                if str(row[1]) == self.ve_numventa.get():
                    self.reporte_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6], "", "", row[8], row[9], row[10], row[11], row[7])
            self.paint(0)
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
            if filtersmt:
                filter += " AND fecha LIKE " + '"%{}%"'.format(self.ve_fecha.get())
            else: 
                filter += " fecha LIKE " + '"%{}%"'.format(self.ve_fecha.get())
                filtersmt = True
        # 2.2 x Semana ******* VER DESPUÉS
        # 2.3 x Mes
        elif self.intervalo.get() == 3:
            mes_e = self.ve_fecha.get()[0] + self.ve_fecha.get()[1] + self.ve_fecha.get()[2] + self.ve_fecha.get()[3] + self.ve_fecha.get()[4] + self.ve_fecha.get()[5] + self.ve_fecha.get()[6]
            print(mes_e)
            if filtersmt:
                filter += " AND fecha LIKE " + '"%{}%"'.format(mes_e)
            else: 
                filter += " fecha LIKE " + '"%{}%"'.format(mes_e)
                filtersmt = True
        # 2.4 x Año
        elif self.intervalo.get() == 4:
            a_e = self.ve_fecha.get()[0] + self.ve_fecha.get()[1] + self.ve_fecha.get()[2] + self.ve_fecha.get()[3]
            if filtersmt:
                filter += " AND fecha LIKE " + '"%{}%"'.format(a_e)
            else: 
                filter += " fecha LIKE " + '"%{}%"'.format(a_e)
                filtersmt = True
        tmp = ""
     # 3. Clave
        try:
            # Revisar que nada esté vacío
            self.ve_clave.get()[0]
            if filtersmt:
                tmp = "( AND clave = " + '"{}"'.format(self.ve_clave.get())
                filter += " AND clave = " + '"{}"'.format(self.ve_clave.get())
            else:
                filter += "( clave = " + '"{}"'.format(self.ve_clave.get())
                filtersmt = True
            both = True
        except:
            pass
     # 4. Producto
        try:
            # Revisar que nada esté vacío
            self.ve_producto.get()[0]  
            if filtersmt:
                if both:
                    filter += " OR producto = " + '"{}"'.format(self.ve_producto.get()) + ")"
                else:
                    filter += " AND producto = " + '"{}"'.format(self.ve_producto.get())
            else:
                filter += "producto = " + '"{}"'.format(self.ve_producto.get())
                filtersmt = True
        except:
            if both:
                filter += ")"
            else:
                pass
     # 5. Cliente
        try:
            # Revisar que nada esté vacío
            self.ve_cliente.get()[0]  
            if filtersmt:
                filter += " AND cliente = " + '"{}"'.format(self.ve_cliente.get())
            else:
                filter += "cliente = " + '"{}"'.format(self.ve_cliente.get())
                filtersmt = True

        except:
            pass
     # 6. Tipo de pago
        # 6.0 Todos
        # 6.1 Efectivo
        if self.t_pago.get() == 1:
            if filtersmt:
                filter += " AND pago = " + '"{}"'.format('efectivo')
            else:
                filter += "pago = " + '"{}"'.format('efectivo')
                filtersmt = True

        # 6.1 Tarjeta
        elif self.t_pago.get() == 2:
            if filtersmt:
                filter += " AND pago = " + '"{}"'.format('tarjeta')
            else:
                filter += "pago = " + '"{}"'.format('tarjeta')
                filtersmt = True
        # 6.1 Crédito
        elif self.t_pago.get() == 3:
            if filtersmt:
                filter += " AND pago = " + '"{}"'.format('credito')
            else:
                filter += "pago = " + '"{}"'.format('credito')
                filtersmt = True
     # 7. Sucursal o Envío
        # 7.0 Ambas
        # 7.1 Sucursal
        if self.int_se.get() == 1:
            if filtersmt:
                filter += " AND se = " + '"{}"'.format('Sucursal')
            else:
                filter += "se = " + '"{}"'.format('Sucursal')
                filtersmt = True
        # 7.1 Envío
        elif self.int_se.get() == 2:
            if filtersmt:
                filter += " AND se = " + '"{}"'.format('Envio')
            else:
                filter += "se = " + '"{}"'.format('Envio')
                filtersmt = True
     # Filter

        if filtersmt:
            for row in db.filter(filter):
                self.reporte_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6], "", "", row[8], row[9], row[10], row[11], row[7])
        else:
            for row in db.fetch():
                self.reporte_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6], "", "", row[8], row[9], row[10], row[11], row[7])
      # Paint
        self.paint(0)
        self.vs_info.set("Total de artículos: %d. Total de dinero: $%d" % (self.vre_Cant, self.vre_Total))
    

    
    
    
    def filtrarCompras(self):
     # Variables
        self.vs_info.set("--")
        self.vre_Cant = 0
        self.vre_Total = 0
        db = self.compra_db

        filter = " "
        filtersmt = False
        both = False
     # 0. Borrar nuestra db provisional
        self.limpiar()
      # 1. No. Venta
        try:
            self.ve_numventa.get()[0]
            for row in db.fetch():
                if str(row[1]) == self.ve_numventa.get():
                    self.reporte_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6], row[7], row[8] , "", "", "", "", "")
            self.paint(1)
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
            if filtersmt:
                filter += " AND fecha LIKE " + '"%{}%"'.format(self.ve_fecha.get())
            else: 
                filter += " fecha LIKE " + '"%{}%"'.format(self.ve_fecha.get())
                filtersmt = True
        # 2.2 x Semana ******* VER DESPUÉS
        # 2.3 x Mes
        elif self.intervalo.get() == 3:
            mes_e = self.ve_fecha.get()[0] + self.ve_fecha.get()[1] + self.ve_fecha.get()[2] + self.ve_fecha.get()[3] + self.ve_fecha.get()[4] + self.ve_fecha.get()[5] + self.ve_fecha.get()[6]
            if filtersmt:
                filter += " AND fecha LIKE " + '"%{}%"'.format(mes_e)
            else: 
                filter += " fecha LIKE " + '"%{}%"'.format(mes_e)
                filtersmt = True
        # 2.4 x Año
        elif self.intervalo.get() == 4:
            a_e = self.ve_fecha.get()[0] + self.ve_fecha.get()[1] + self.ve_fecha.get()[2] + self.ve_fecha.get()[3]
            if filtersmt:
                filter += " AND fecha LIKE " + '"%{}%"'.format(a_e)
            else: 
                filter += " fecha LIKE " + '"%{}%"'.format(a_e)
                filtersmt = True
     # 3. Clave
        try:
            # Revisar que nada esté vacío
            self.ve_clave.get()[0]
            if filtersmt:
                filter += "( AND clave = " + '"{}"'.format(self.ve_clave.get())
            else:
                filter += "( clave = " + '"{}"'.format(self.ve_clave.get())
                filtersmt = True
            both = True
        except:
            pass
     # 4. Producto
        try:
            # Revisar que nada esté vacío
            self.ve_producto.get()[0]  
            if filtersmt:
                if both:
                    filter += " OR producto = " + '"{}"'.format(self.ve_producto.get()) + ")"
                else:
                    filter += " AND producto = " + '"{}"'.format(self.ve_producto.get())
            else:
                filter += "producto = " + '"{}"'.format(self.ve_producto.get())
                filtersmt = True
        except:
            if both:
                filter += ")"
            else:
                pass
     # 5. Proveedor
        try:
            # Revisar que nada esté vacío
            self.ve_cliente.get()[0]  
            if filtersmt:
                filter += " AND proveedor = " + '"{}"'.format(self.ve_cliente.get())
            else:
                filter += "proveedor = " + '"{}"'.format(self.ve_cliente.get())
                filtersmt = True
        except:
            pass

         # Filter

        if filtersmt:
            for row in db.filter(filter):
                self.reporte_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6], row[7], row[8] , "", "", "", "", "")
        else:
            for row in db.fetch():
                self.reporte_db.insert(row[0], row[1],row[2],row[3],row[4],row[5],row[6], row[7], row[8] , "", "", "", "", "")

     # Paint
        self.paint(1)
        self.vs_info.set("Total de artículos: %s. Total de dinero: $%s" % (round(self.vre_Cant, 3), round(self.vre_Total, 3)))


    # Quiza dejar para mostrar las notas si se da doble click
    def seleccionado(self):
        pass

