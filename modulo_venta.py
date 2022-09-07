import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from datetime import datetime
import time


class F_Venta(tk.Frame):   # Frame de venta
    def __init__(self, root, Clock, AutocompleteEntry, hoy, lista_productos, lista_claves, lista_total, productos_db, tmpVent_db, tmpCot_db, clien_db, compra_db, venta_db, reg_db, cot_db, *args, **kwargs):
    
        super().__init__(root, *args, **kwargs)

        # Databases
        self.productos_db = productos_db
        self.tmpVent_db = tmpVent_db
        self.tmpCot_db = tmpCot_db
        self.clien_db = clien_db
        self.compra_db = compra_db
        self.venta_db = venta_db
        self.reg_db = reg_db
        self.cot_db = cot_db
        self.Clock = Clock
        self.AutocompleteEntry = AutocompleteEntry

        # Total Label
        self.vst_total = tk.StringVar()
        self.vst_total.set("TOTAL ---- $ 0")

        self.hoy = hoy


        # Listas
        self.lista_productos = lista_productos
        self.lista_claves = lista_claves
        self.lista_total = lista_total

            # Tree2
        self.vt_tabla = ttk.Treeview(self, height = 15, columns=("#1","#2","#3","#4", "#5"), style = "mystyle.Treeview")
        self.vt_tabla.grid(row = 1, column = 0, padx = 7, pady = 10, columnspan = 4, sticky = tk.W + tk.E)
        self.vt_tabla.heading("#0", text = "Clave")
        self.vt_tabla.column("#0", width = 70, minwidth = 60)
        self.vt_tabla.heading("#1", text = "Producto")
        self.vt_tabla.column("#1", width = 300, minwidth = 200)
        self.vt_tabla.heading("#2", text = "Precio")
        self.vt_tabla.column("#2", width = 70, minwidth = 70)
        self.vt_tabla.heading("#3", text = "Cantidad")
        self.vt_tabla.column("#3", width = 70, minwidth = 70)
        self.vt_tabla.heading("#4", text = "Subtotal")
        self.vt_tabla.column("#4", width = 70, minwidth = 70)
        self.vt_tabla.heading("#5", text = "Cliente")
        self.vt_tabla.column("#5", width = 100, minwidth = 100)
        self.vt_tabla.bind("<BackSpace>", self.quitar_producto)
        self.vt_tabla.bind("<Double-1>", self.info)


        # Agregar

        self.vl_busc = tk.Label(self, text = "Buscar Producto", font= ("AppleGothic") )
        self.vl_busc.grid(row = 0, column = 0, padx = 7, pady = 5, sticky = tk.W)
        self.ve_prod = AutocompleteEntry(self.lista_total, self, width = 35, function=self.agregar_producto)
        self.ve_prod.bind("<Return>", self.agregar_producto_event, add="+")
        self.ve_prod.focus()         # Set cursor to entry after frame is loaded
        self.ve_prod.grid(row = 0, column = 1, sticky = tk.W)

        # Reloj
        self.v_clock = self.Clock(self)
        self.v_clock.grid(row = 0, column = 3, sticky = tk.W)

        # Info 
        self.vb_info = tk.Button(self, text = "Info", font = ("AppleGothic"), command = self.informacion)
        self.vb_info.grid(row = 0, column = 3, sticky = tk.E)
        self.vt_info = tk.Text(self, width = 20, height = 12, highlightthickness = 1, wrap = tk.WORD,  state="disabled", borderwidth = 1, fg = "black", font = "AppleGothic")
        self.vt_info.grid(row = 1, column = 4, pady = 10, sticky = tk.N)

        # Numero de venta
        self.n_venta = tk.StringVar()
        self.n_venta.set("No. Venta: " + self.reg_db.numero("Venta"))
        self.vl_nventa = tk.Label(self, textvariable= self.n_venta, font = "AppleBraille")
        self.vl_nventa.grid(row = 0, column = 4, sticky = tk.W)

        # Entrega
        self.se = tk.IntVar()
        self.vcb_se = tk.Checkbutton(self, text = "¿ENTREGA?", font = "AppleGothic", variable= self.se, command = self.checkbutton)      # Checkbutton envío
        self.vcb_se.grid(row = 0, column = 2, sticky = tk.W)

        # Nuevo frame - cantidad, precio, clientes
        self.fvf = tk.Frame(self)
        self.fvf.grid(row = 2,column = 0, columnspan = 4, pady = 20, padx = 7, sticky = tk.W)

        self.lista_clientes = []
        for row in self.clien_db.fetch():
            self.lista_clientes.append(row[1])
        
            # Cambiar cantidad
        self.vl_cant = tk.Label(self.fvf, text = "Cambiar Cantidad", font= ("AppleGothic"))           
        self.vl_cant.grid(row = 0, column = 0, sticky = tk.W)
        self.ve_cant = tk.Entry(self.fvf)
        self.ve_cant.bind("<Return>", self.cambiar_cantidad)
        self.ve_cant.grid( row = 0, column = 1, sticky = tk.W)

            # Cambiar precio
        self.vl_precio = tk.Label(self.fvf, text = "Cambiar Precio", font= ("AppleGothic"))           
        self.vl_precio.grid(row = 0, column = 2, sticky = tk.W)
        self.ve_precio = tk.Entry(self.fvf)
        self.ve_precio.bind("<Return>", self.cambiar_precio)
        self.ve_precio.grid( row = 0, column = 3, sticky = tk.W)

            # Cambiar cliente
        self.vl_clien = tk.Label(self.fvf, text = "Cambiar Cliente", font= ("AppleGothic"))           
        self.vl_clien.grid(row = 0, column = 4, sticky = tk.W)
        self.ve_clien = AutocompleteEntry(self.lista_clientes, self.fvf)
        self.ve_clien.bind("<Return>", self.cambiar_cliente, add="+")
        self.ve_clien.grid( row = 0, column = 5, sticky = tk.W)

            # Total label
        self.vl_total = tk.Label(self.fvf, textvariable = self.vst_total, fg = "red", font= ("AppleBraille", 17)) 
        self.vl_total.grid(row = 0, column  = 6, columnspan = 2, sticky = tk.W) 


            # Venta o cancelar o guardar cotización
        self.vb_venta = tk.Button(self.fvf, text = "VENTA", width = 9, height = 1, fg = "green",font= ("AppleGothic 17 "), command = lambda: self.venta_cotizacion(self.venta_db, "Venta"))     # Venta
        self.vb_venta.grid(row = 1, column  = 5, pady = 20, sticky = tk.E)
        self.vb_guardar = tk.Button(self.fvf, text = "GUARDAR COTIZACIÓN", width = 18, height = 1, fg = "violet",font= ("AppleGothic"), command = lambda: self.venta_cotizacion(self.cot_db, "Cotizacion"))     # Guardar la cotización
        self.vb_guardar.grid(row = 1, column  = 3, pady = 20, sticky = tk.E)
        self.vb_cancelar = tk.Button(self.fvf, text = "CANCELAR", font= ("AppleGothic"), width = 10, height = 1, command = self.cancelar)              # Cancelar
        self.vb_cancelar.grid(row = 1, column  = 4, pady = 20, sticky = tk.E +  tk.W)

            # Tipo de pago
        self.vl_pago = tk.Label(self.fvf, text = "Tipo de pago", font = "AppleGothic")
        self.vl_pago.grid(row = 1, column  = 0, sticky = tk.W)

        self.fvp = tk.Frame(self.fvf)
        self.fvp.grid(row = 1, column = 1, pady = 10)
        self.t_pago = tk.IntVar()
        self.t_pago.set("1")
        self.vr_efectivo = tk.Radiobutton(self.fvp, text = "Efectivo", font = "AppleGothic", variable = self.t_pago, value = 1)
        self.vr_efectivo.grid(row = 0, column = 0, sticky = tk.W)
        self.vr_tarjeta = tk.Radiobutton(self.fvp, text = "Tarjeta", font = "AppleGothic", variable = self.t_pago, value = 2)
        self.vr_tarjeta.grid(row = 0, column = 1, sticky = tk.W)
        self.vr_credito = tk.Radiobutton(self.fvp, text = "Crédito", font = "AppleGothic", variable = self.t_pago, value = 3)
        self.vr_credito.grid(row = 1, column = 0, sticky = tk.W)

            # Calculadora de cambio
        self.fvr = tk.Frame(self.fvf)
        self.fvr.grid(row = 1, column = 6)
        self.vl_recibo = tk.Label(self.fvr, text = "Recibo:", font = "AppleGothic")
        self.vl_recibo.grid(row = 0, column = 0, sticky = tk.S)
        self.ve_recibo = tk.Entry(self.fvr, width = 10)
        self.ve_recibo.bind("<KeyRelease>", self.get_cambio)
        self.ve_recibo.grid(row = 0, column = 1, sticky = tk.S)
        self.cambio = tk.StringVar()
        self.cambio.set("Cambio: ")
        self.vl_cambio = tk.Label(self.fvr, textvariable = self.cambio, font = "AppleBraille 13" )
        self.vl_cambio.grid(row = 2, column = 0, columnspan = 2, sticky = tk.W)

    def agregar_producto_event(self, event):
        self.agregar_producto()
    def informacion(self):
        try:
            self.vt_info.config(state = "normal")
            self.vt_info.delete("1.0", tk.END)
            #compra = False
            pselec = self.vt_tabla.item(self.vt_tabla.selection())
            for row in self.productos_db.fetch():
                if row[0] == pselec["text"]:    # Buscar producto en base de datos solo para el stock actual y notas de producto, sí
                    self.vt_info.insert("1.0", "Clave: %s \nProducto: %s \nStock: %s \nNotas: %s \n\nHistorial de Compras" % ( row[0], row[1], row[8], row[9]))
                    for comp in self.compra_db.inverse_fetch():# Para saber los precios de compra y proveedor
                        if comp[2] == pselec["text"]:
                            self.vt_info.insert(tk.END, "\nFecha: %s \nPrecio: %s \nProveedor: %s\nNotas: %s" % (comp[0], comp[4], comp[7], comp[8]))
            self.vt_info.config(state = "disabled")
        except:
            pass
        # Automatización de entry widget 
    def info(self, event):
        self.informacion()
    def agregar_producto(self):   
        cotexi = True

        if self.se.get() == 0:       # Dependiendo de si el checkbutton está seleccionado o no 
            # Buscar el elemento en self.productos_db a agregar en self.tmpVent_db
            for row in self.productos_db.fetch():
                if row[1] == self.ve_prod.get() or row[0] == self.ve_prod.get(): # Se busca por nombre o clave entonces tiene que coincidir en la self.productos_db de productos.       
                    for rowcot in self.tmpVent_db.fetch():
                        if rowcot[0] == row[0]:  #Ya existe en la cotización

                            if rowcot[3] > 18:  # Si es precio especial
                                self.tmpVent_db.update(rowcot[0], rowcot[1], row[3], rowcot[3]+1, round((rowcot[3]+1) * row[3], 3), rowcot[5])  # Actualizar cantidad y subtotal y precio
                                cotexi = False
                            elif rowcot[3] > 2:   # Si es precio de mayoreo
                                self.tmpVent_db.update(rowcot[0], rowcot[1], row[5], rowcot[3]+1, round((rowcot[3]+1) * row[5], 3), rowcot[5])  # Actualizar cantidad y subtotal y precio
                                cotexi = False
                            else:   # Menudeo 
                                
                                self.tmpVent_db.update(rowcot[0], rowcot[1], row[7], rowcot[3]+1, round((rowcot[3]+1) * row[7], 3), rowcot[5])  # Actualizar cantidad y subtotal y precio
                                cotexi = False

                    if cotexi:    # No existía en cotización antes
                            # Menudeo 
                        self.tmpVent_db.insert(row[0], row[1], row[7], 1, row[7], "Mostrador")  # Actualizar cantidad y subtotal y precio


        else:   # Si es de los productos de la lista de envío
            # Buscar elementos en self.productos_db y agregarlos a self.tmpVent_db
            for row in self.productos_db.fetch():
                if row[1] == self.ve_prod.get() or row[0] == self.ve_prod.get(): # Se busca por nombre entonces tiene que coincidir en la self.productos_db de productos.         
                    for rowcot in self.tmpVent_db.fetch():
                        if rowcot[0] == row[0]:  #Ya existe en la cotización

                            if rowcot[3] > 18:  # Si es precio especial
                                self.tmpVent_db.update(rowcot[0], rowcot[1], row[2], rowcot[3]+1, round((rowcot[3]+1) * row[2], 3), rowcot[5])  # Actualizar cantidad y subtotal y precio
                                cotexi = False
                            elif rowcot[3] > 2:   # Si es precio de mayoreo
                                self.tmpVent_db.update(rowcot[0], rowcot[1], row[4], rowcot[3]+1, round((rowcot[3]+1) * row[4], 3), rowcot[5])  # Actualizar cantidad y subtotal y precio
                                cotexi = False
                            else:   # Menudeo 
                                self.tmpVent_db.update(rowcot[0], rowcot[1], row[6], rowcot[3]+1, round((rowcot[3]+1) * row[6], 3), rowcot[5])  # Actualizar cantidad y subtotal y precio
                                cotexi = False

                    if cotexi:    # No existía en cotización antes
                        # Menudeo 
                        self.tmpVent_db.insert(row[0], row[1], row[6], 1, row[6], "Mostrador")  # Actualizar cantidad y subtotal y precio

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
        for row in self.tmpVent_db.fetch():
            self.vt_tabla.insert("", "end",text = row[0],  values = (row[1],"$" + str(row[2]), row[3], "$"+ str(row[4]), row[5]) )
            total += float(row[4])

        self.vst_total.set("TOTAL ---- $ " + str(round(total, 3)))
    def quitar_producto(self,event):
        # Quitar de la self.tmpVent_db el elemento seleccionado text es clave.
        for p in self.vt_tabla.selection():
            pselec = self.vt_tabla.item(p)["text"]
            self.tmpVent_db.remove(pselec)

        self.paint()
    def cambiar_cantidad(self,event):
        try:
            pselec = self.vt_tabla.item(self.vt_tabla.selection())
            
            for row in self.productos_db.fetch():        # Para tener los precios del producto, buscamos el producto seleccionado.
                if row[0] == pselec["text"]:
                    prod = row
            for rowcot in self.tmpVent_db.fetch():   
                if pselec["text"] == rowcot[0]:       # Lo buscamos en la base de datos de cotización ahora. 
                    if self.se.get() == 0:
                        if float(self.ve_cant.get()) >= 20:  # Si es precio especial
                            self.tmpVent_db.update(rowcot[0], rowcot[1], prod[3], round(float(self.ve_cant.get()), 3), round((round(float(self.ve_cant.get()), 3)) * prod[3], 3), rowcot[5])  
                        elif float(self.ve_cant.get()) >= 4:   # Si es precio de mayoreo
                            self.tmpVent_db.update(rowcot[0], rowcot[1], prod[5], round(float(self.ve_cant.get()), 3), round((round(float(self.ve_cant.get()), 3)) * prod[5], 3), rowcot[5])  
                        else:   # Menudeo 
                            
                            self.tmpVent_db.update(rowcot[0], rowcot[1], prod[7], round(float(self.ve_cant.get()), 3), round((round(float(self.ve_cant.get()), 3)) * prod[7], 3), rowcot[5])  
                    
                    else:
                        if float(self.ve_cant.get()) >= 20:  # Si es precio especial
                            self.tmpVent_db.update(rowcot[0], rowcot[1], prod[2], round(float(self.ve_cant.get()), 3), round((round(float(self.ve_cant.get()), 3)) * prod[2], 3), rowcot[5])  
                        elif float(self.ve_cant.get()) >= 4:   # Si es precio de mayoreo
                            self.tmpVent_db.update(rowcot[0], rowcot[1], prod[4], round(float(self.ve_cant.get()), 3), round((round(float(self.ve_cant.get()), 3)) * prod[4], 3), rowcot[5])  
                        else:   # Menudeo 
                            self.tmpVent_db.update(rowcot[0], rowcot[1], prod[6], round(float(self.ve_cant.get()), 3), round((round(float(self.ve_cant.get()), 3)) * prod[6], 3), rowcot[5])  
        except:
            pass

        # Refresh
        self.paint()
    def cambiar_cliente(self,event):
        try:    # No queremos que haga nada si nada está seleccionado
           # for p in self.vt_tabla.selection():
            for row in self.tmpVent_db.fetch():
                self.tmpVent_db.update(row[0], row[1], row[2], row[3], row[4] , self.ve_clien.get())
        except:
            pass

        # Ver si se agrega el nuevo cliente a la base de datos, si es que es nuevo
        numero_cliente = 0
        n_c = True
        for row in self.clien_db.fetch():
            numero_cliente = row[0]
            if self.ve_clien.get() == row[1]:
                n_c = False
        if n_c:       
            self.clien_db.insert(str(int(numero_cliente) + 1), self.ve_clien.get())  # Dar de alta el nuevo cliente sin preguntards


        # Insertar en el arbol los datos de self.tmpVent_db  "refresh"
            # Eliminar primero todo el árbol
        leaves = self.vt_tabla.get_children()    
        for row in leaves:
            self.vt_tabla.delete(row)
            # Poblar el árbol
        for row in self.tmpVent_db.fetch():
            self.vt_tabla.insert("", "end",text = row[0],  values = (row[1],"$" + str(row[2]), row[3], "$" + str(row[4]), row[5]) )
    def cambiar_precio(self,event):      # ***** AQUI EL UNICO DETALLE ES QUE SI SE CAMBIA EL PRODUCTO Y SE VUELVE A AGREGAR DESDE ARRIBA, EL PRECIO SE PERDERÁ ****

        try:    # No queremos que haga nada si nada está seleccionado
            for p in self.vt_tabla.selection():
                pselec = self.vt_tabla.item(p)
                for row in self.tmpVent_db.fetch():
                    if pselec["text"] == row[0]:
                        self.tmpVent_db.update(row[0], row[1], self.ve_precio.get(), row[3], round((float(self.ve_precio.get()) * float(row[3] )), 3) , row[5])
        except:
            pass

        # Refresh
        self.paint()
    def venta_cotizacion(self, db_final, tipo):

        datestring = datetime.today().strftime("%Y/%m/%d -%H:%M")
        total = 0
        enough_lista = []
        lista = ""
        tipo_pago = ""

        if tipo == "Venta":
            status = "VEN"
        else:
            status = "COT"

        # No hacer nada si no hay nada
        x = 0
        for leaves in self.vt_tabla.get_children():
            x += 1
        if x == 0:
            return

        enough = True

        # Revisar primero si hay de todos los productos y agregarlos a una lista!!
        for stock in self.productos_db.fetch():
            for row in self.tmpVent_db.fetch():
                    if stock[0] == row[0]:
                        if row[3] > stock[8]:       # Si se quiere vernder más de lo que hay. 
                            enough_lista.append(str(row[1]))     # Habrá suficiente de todo si la lista está vacía

        if len(enough_lista) != 0:      # No se hace nada hasta que estemos seguros de que hay algo que escribir. 
            if tipo == "Venta":
                tkinter.messagebox.showinfo("Error", "No hay suficiente de: %s  en inventario." % enough_lista) # ** decir qué productos **
                self.focus() 
                self.ve_prod.focus() 
                return
            else:
                enough = True

        # Significa que sí hay de todo y podemos proseguir a hacer la venta. 
        if enough:

            # Tipo de pago
            if self.t_pago.get() == 1:
                tipo_pago = "Efectivo"
            elif self.t_pago.get() == 2:
                tipo_pago = "Tarjeta"
            else:
                tipo_pago = "Crédito"
            
            # S/E
            se_venta = "Sucursal"
            if self.se.get() == 1:       # Si checkbutton seleccionado
                se_venta = "Envio"
            

                # Escribir
            registro = self.reg_db.accion(tipo)  # Se incrementa dependiendo del tipo
            for row in self.tmpVent_db.fetch():

                total += row[4]
                cliente = row[5]

                if row[3] < 4:
                    lista = "Menudeo"
                elif row[3] < 20:
                    lista = "Mayoreo"
                else:
                    lista = "Especial"

                # venta_db o cot_db
                db_final.insert(datestring, registro, row [0], row[1], row[2], row[3], row[4], row[5], se_venta, lista, tipo_pago, status)

                # Solo se decrementa del stock si sí es venta
                if tipo == "Venta":
                    for stock in self.productos_db.fetch():
                        if stock[0] == row[0]:
                            # Ajustar stock
                            self.productos_db.update(stock[0], stock[1], stock[2], stock[3], stock[4], stock[5], stock[6], stock[7], round(stock[8] - row[3], 3), stock[9] )    # Decrementar del stock

            if tipo == "Venta":
                tkinter.messagebox.showinfo("Venta", "Venta guardada con éxito." )
            else:
                tkinter.messagebox.showinfo("Cotización", "Cotización guardada con éxito." )

            self.focus() 
            self.ve_prod.focus() 

            # Borrar tmpVent_db
            self.vt_info.delete("1.0", tk.END)
            for row in self.tmpVent_db.fetch():
                self.tmpVent_db.remove(row[0])

            # Borrar árbol 
            leaves = self.vt_tabla.get_children()    
            for row in leaves:
                self.vt_tabla.delete(row)
            # Borrar labels 
            self.vst_total.set("TOTAL ---- $ 0")
            self.vt_info.config(state = "normal")
            self.vt_info.delete("1.0", tk.END)
            self.vt_info.config(state = "disabled")
            for row in self.clien_db.fetch():
                self.lista_clientes.append(row[1])
            self.n_venta.set("No. Venta:" + self.reg_db.numero("Venta"))
    def cancelar(self):
        try:        # Only do if list is not empty
            self.tmpVent_db.fetch()[0]
            result = tkinter.messagebox.askyesno("Cancelar", "¿Segura que quieres cancelar? Se borrarán todos los productos.")

            if result:
                self.vt_info.delete("1.0", tk.END)
                # Borrar cot self.productos_db
                for row in self.tmpVent_db.fetch():
                    self.tmpVent_db.remove(row[0])
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
    def checkbutton(self):

        if self.se.get() == 0:       # Dependiendo de si el checkbutton está seleccionado o no 
            # Buscar el elemento en self.productos_db a agregar en self.tmpVent_db
            for row in self.productos_db.fetch():
                for rowcot in self.tmpVent_db.fetch():
                    if rowcot[0] == row[0]:  #Ya existe en la cotización

                        if rowcot[3] > 18:  # Si es precio especial
                            self.tmpVent_db.update(rowcot[0], rowcot[1], row[3], rowcot[3], round((rowcot[3]) * row[3], 3), rowcot[5])  # Actualizar precio
                        elif rowcot[3] > 2:   # Si es precio de mayoreo
                            self.tmpVent_db.update(rowcot[0], rowcot[1], row[5], rowcot[3], round((rowcot[3]) * row[5], 3), rowcot[5])  # Actualizar precio
                        else:   # Menudeo 
                            
                            self.tmpVent_db.update(rowcot[0], rowcot[1], row[7], rowcot[3], round((rowcot[3]) * row[7], 3), rowcot[5])  # Actualizar precio

        else:   # Si es de los productos de la lista de productos
            # Buscar elementos en self.productos_db y agregarlos a self.tmpVent_db
            for row in self.productos_db.fetch():
                #if row[1] == vt_tabla.get_children()[1]: # Buscamos qué productos están en el árbol y esos son los que ajustamos de precio      
                for rowcot in self.tmpVent_db.fetch():
                    if rowcot[0] == row[0]:  #Ya existe en la cotización

                        if rowcot[3] > 18:  # Si es precio especial
                            self.tmpVent_db.update(rowcot[0], rowcot[1], row[2], rowcot[3], round((rowcot[3]) * row[2], 3), rowcot[5])  # Actualizar precio
                        elif rowcot[3] > 2:   # Si es precio de mayoreo
                            self.tmpVent_db.update(rowcot[0], rowcot[1], row[4], rowcot[3], round((rowcot[3]) * row[4], 3), rowcot[5])  # Actualizar precio
                        else:   # Menudeo 
                            self.tmpVent_db.update(rowcot[0], rowcot[1], row[6], rowcot[3], round((rowcot[3]) * row[6], 3), rowcot[5])  # Actualizar precio

        self.paint()
    def get_cambio(self,event):
        t = ""
        for c in self.vst_total.get():
            if c.isdigit() or c == ".":
                t = t + c

        try:
            self.cambio.set("Cambio: $" + str( round(float(self.ve_recibo.get()) - float(t), 3)))
        except:
            self.cambio.set("Cambio: ")


class F_Cotizacion(F_Venta):
    def __init__(self, root, Clock, AutocompleteEntry, hoy, lista_productos, lista_claves, lista_total, productos_db, tmpVent_db, tmpCot_db, clien_db, compra_db, venta_db, *args, **kwargs):
       
        super().__init__( root, Clock, AutocompleteEntry, hoy, lista_productos, lista_claves, lista_total, productos_db, tmpVent_db, tmpCot_db, clien_db, compra_db, venta_db, *args, **kwargs)
        self.tmpVent_db = tmpCot_db
        self.vb_venta.grid_remove() 

    