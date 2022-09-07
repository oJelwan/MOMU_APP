import sqlite3

#INVENTARIO DATABASE
class Database_Productos: 
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        # Create our data base's table
        self.cur.execute("""
         CREATE TABLE IF NOT EXISTS productos_momu ( clave TEXT PRIMARY KEY, producto text, en_especial real, su_especial real, en_mayoreo real, su_mayoreo real, en_menudeo real, su_menudeo real, stock real, notas string)""")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("""SELECT * FROM productos_momu""")
        rows = self.cur.fetchall()
        return rows

    def fetch_alph(self):
        self.cur.execute("""SELECT * FROM productos_momu ORDER BY producto""")
        rows = self.cur.fetchall()
        return rows
    
    def insert(self, clave, producto, en_especial, su_especial, en_mayoreo, su_mayoreo, en_menudeo, su_menudeo, stock, notas):
        self.cur.execute(""" INSERT INTO productos_momu VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (clave, producto, en_especial, su_especial, en_mayoreo, su_mayoreo, en_menudeo, su_menudeo, stock, notas))
        self.conn.commit()

    def remove(self, clave):
        self.cur.execute("""DELETE FROM productos_momu WHERE clave = ?""", (clave, ))
        self.conn.commit()

    def update(self, clave, producto, en_especial, su_especial, en_mayoreo, su_mayoreo, en_menudeo, su_menudeo, stock, notas):
        self.cur.execute("""UPDATE productos_momu SET producto = ?, en_especial = ?, su_especial = ?, en_mayoreo = ?, su_mayoreo = ?, en_menudeo = ?, su_menudeo = ?, stock = ?, notas = ? WHERE clave = ? """, (producto, en_especial, su_especial, en_mayoreo, su_mayoreo, en_menudeo, su_menudeo, stock, notas, clave))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

# VENTAS DATABASE
class Venta_Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        # Create our data base's table
        self.cur.execute("""
         CREATE TABLE IF NOT EXISTS ventas ( fecha text, registro string, clave text, producto text, precio real, cantidad real, total real, 
         cliente text, se text, lista text, pago string, status string)""")
        self.conn.commit()

    def fetch(self):
        self.cur.execute(""" SELECT * FROM ventas""")
        rows = self.cur.fetchall()
        return rows

    def inverse_fetch(self):
        self.cur.execute(""" SELECT * FROM ventas ORDER BY registro DESC """)
        rows = self.cur.fetchall()
        line  = []
        for r in rows:
            line.append(r)
        return line
    

    def insert(self,fecha, registro, clave, producto, precio, cantidad, total, cliente, se, lista, pago, status):
        self.cur.execute("""INSERT INTO ventas VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (fecha, registro, clave, producto, precio, cantidad, total, cliente, se, lista, pago, status))
        self.conn.commit()

    def remove(self, registro ):
        self.cur.execute("""  DELETE FROM ventas WHERE registro    = ?""", (registro, ))
        self.conn.commit()

    def remove_product(self, clave ):
        self.cur.execute("""  DELETE FROM ventas WHERE clave    = ?""", (clave, ))
        self.conn.commit()

    def deleteall(self):
        self.cur.execute("""DELETE FROM ventas """)
        self.conn.commit()

    def update(self, fecha, registro, clave, producto, precio, cantidad, total, cliente, se, lista, pago, status):
        self.cur.execute("""UPDATE ventas SET fecha = ?, clave = ?, producto = ?, precio = ?, cantidad = ?, total = ?, cliente = ?, se = ?, lista = ?, pago = ?, status = ? WHERE registro = ?""", (fecha, clave, producto, precio, cantidad, total, cliente, se, lista, pago, status, registro))
        self.conn.commit()

    def cancelado(self, fecha, registro, clave):
        self.cur.execute("""UPDATE ventas SET status = "CAN" WHERE fecha = ? and registro = ? and clave = ?""", (fecha, registro, clave))
        self.conn.commit()

    def __del__(self):
        self.conn.close()


# COTIZACION DATABASE
class Cotizacion_Database():
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        # Create our data base's table
        self.cur.execute("""
         CREATE TABLE IF NOT EXISTS cotizacion ( fecha text, registro string, clave text, producto text, precio real, cantidad real, total real, cliente text, se text, lista text, pago string, status string)""")
        self.conn.commit()

    def fetch(self):
        self.cur.execute(""" SELECT * FROM cotizacion""")
        rows = self.cur.fetchall()
        return rows

    def inverse_fetch(self):
        self.cur.execute(""" SELECT * FROM cotizacion ORDER BY registro DESC """)
        rows = self.cur.fetchall()
        line  = []
        for r in rows:
            line.append(r)
        return line
    

    def insert(self,fecha, registro, clave, producto, precio, cantidad, total, cliente, se, lista, pago, status):
        self.cur.execute("""INSERT INTO cotizacion VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (fecha, registro, clave, producto, precio, cantidad, total, cliente, se, lista, pago, status))
        self.conn.commit()

    # No necesarias realmente pero igual y después más, es la idea. 
    def remove(self, registro ):
        self.cur.execute("""  DELETE FROM cotizacion WHERE registro    = ?""", (registro, ))
        self.conn.commit()

    def update(self, fecha, registro, producto, clave, precio, cantidad, total, cliente, se, lista, pago, status):
        self.cur.execute("""UPDATE cotizacion SET fecha = ?, clave = ?, producto = ?, precio = ?, cantidad = ?, total = ?, cliente = ?, se = ?, lista = ?, pago = ?, status = ? WHERE registro = ?""", (fecha, producto, clave, precio, cantidad, total, cliente, se, lista, pago, status, registro))
        self.conn.commit()

    def __del__(self):
        self.conn.close()


#CLIENTES DATABASE
class Clientes_Database: 
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        # Create our data base's table
        self.cur.execute("""
         CREATE TABLE IF NOT EXISTS clientes (numero TEXT PRIMARY KEY UNIQUE, cliente text)""")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("""SELECT * FROM clientes""")
        rows = self.cur.fetchall()
        return rows

    def registro(self):
        return self.fetch()[0][0]
    
    def insert(self, numero, cliente):
        self.cur.execute(""" INSERT INTO clientes VALUES (?, ?)""", (numero, cliente))
        self.conn.commit()

    def remove(self, numero):
        self.cur.execute("""DELETE FROM clientes WHERE numero = ?""", (numero, ))
        self.conn.commit()

    def update(self, numero, cliente):
        self.cur.execute("""UPDATE clientes SET cliente = ? WHERE numero = ? """, (cliente, numero))
        self.conn.commit()
    
    def __del__(self):
        self.conn.close()

#REGISTRO DATABASE
class Registros_Database: 
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        # Create our data base's table
        self.cur.execute("""
         CREATE TABLE IF NOT EXISTS registros (numero text, tipo text)""")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("""SELECT * FROM registros""")
        rows = self.cur.fetchall()
        return rows

    def registro(self):
        return self.fetch()[0][0]
    
    def insert(self, numero, tipo):
        self.cur.execute(""" INSERT INTO registros VALUES (?, ?)""", (numero, tipo))
        self.conn.commit()

    def remove(self, numero):
        self.cur.execute("""DELETE FROM registros WHERE numero = ?""", (numero, ))
        self.conn.commit()

    def update(self, numero, tipo):
        self.cur.execute("""UPDATE registros SET tipo = ? WHERE numero = ? """, (tipo, numero))
        self.conn.commit()
    
    def accion(self, tipo):
        for row in self.fetch():
            if row[1] == tipo:
                registro = row[0]
        self.cur.execute("""UPDATE registros SET numero = ? WHERE tipo = ? """, (int(registro) +1, tipo))
        self.conn.commit()
        return registro

    def numero(self, tipo):
        for row in self.fetch():
            if row[1] == tipo:
                num = row[0]
        return num

    def __del__(self):
        self.conn.close()

# TMPVENTA DATABASE
class TmpVent_Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        # Create our data base's table
        self.cur.execute("""
         CREATE TABLE IF NOT EXISTS temporario_venta ( clave TEXT PRIMARY KEY, producto text, precio real, cantidad real, subtotal real, cliente text)""")
        self.conn.commit()

    def fetch(self):
        self.cur.execute(""" SELECT * FROM temporario_venta""")
        rows = self.cur.fetchall()
        return rows


    def inverse_fetch(self):
        self.cur.execute(""" SELECT *,  ROW_NUMBER() over (PARTITION BY clave) as number
FROM temporario_venta 
ORDER BY number DESC """)
        rows = self.cur.fetchall()
        line  = []
        for r in rows:
            line.append(r)
        return line

    def deleteall(self):
        self.cur.execute("""DELETE FROM temporario_venta """)
        self.conn.commit()
    
    def insert(self,clave, producto, precio, cantidad, subtotal, cliente):
        self.cur.execute("""INSERT INTO temporario_venta VALUES (?, ?, ?, ?, ?, ?)""", (clave, producto, precio, cantidad, subtotal, cliente))
        self.conn.commit()

    def remove(self, clave):
        self.cur.execute("""  DELETE FROM temporario_venta WHERE clave = ?""", (clave, ))
        self.conn.commit()

    def update(self, clave, producto, precio, cantidad, subtotal, cliente):
        self.cur.execute("""UPDATE temporario_venta SET producto = ?, precio = ?, cantidad = ?, subtotal = ?, cliente = ? WHERE clave = ?""", (producto, precio, cantidad, subtotal, cliente, clave))
        self.conn.commit()


    def __del__(self):
        self.conn.close()

# TMPCOT DATABASE
class TmpCot_Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        # Create our data base's table
        self.cur.execute("""
         CREATE TABLE IF NOT EXISTS temporario_cot ( clave TEXT PRIMARY KEY, producto text, precio real, cantidad real, subtotal real, cliente text)""")
        self.conn.commit()

    def fetch(self):
        self.cur.execute(""" SELECT * FROM temporario_cot""")
        rows = self.cur.fetchall()
        return rows

    def deleteall(self):
        self.cur.execute("""DELETE FROM temporario_cot """)
        self.conn.commit()
    
    def insert(self,clave, producto, precio, cantidad, subtotal, cliente):
        self.cur.execute("""INSERT INTO temporario_cot VALUES (?, ?, ?, ?, ?, ?)""", (clave, producto, precio, cantidad, subtotal, cliente))
        self.conn.commit()

    def remove(self, clave):
        self.cur.execute("""  DELETE FROM temporario_cot WHERE clave = ?""", (clave, ))
        self.conn.commit()

    def update(self, clave, producto, precio, cantidad, subtotal, cliente):
        self.cur.execute("""UPDATE temporario_cot SET producto = ?, precio = ?, cantidad = ?, subtotal = ?, cliente = ? WHERE clave = ?""", (producto, precio, cantidad, subtotal, cliente, clave))
        self.conn.commit()


    def __del__(self):
        self.conn.close()

# COMPRAS DATABASE
class Compras_Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        # Create our data base's table
        self.cur.execute(""" CREATE TABLE IF NOT EXISTS compras (fecha string, n_compra string, clave string, producto string, p_unitario real, cantidad real, t_compra real, proveedor string, notas string )""")
        self.conn.commit()

    def fetch(self):
        self.cur.execute(""" SELECT * FROM compras""")
        rows = self.cur.fetchall()
        return rows
    def inverse_fetch(self):
        self.cur.execute(""" SELECT * FROM compras ORDER BY n_compra DESC """)
        rows = self.cur.fetchall()
        line  = []
        for r in rows:
            if r[2] != "Registro":
                line.append(r)
        return line
    def insert(self,fecha, n_compra, clave, producto, p_unitario, cantidad, t_compra, proveedor, notas):
        self.cur.execute("""INSERT INTO compras VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (fecha,n_compra, clave, producto, p_unitario, cantidad, t_compra, proveedor, notas))
        self.conn.commit()

    def remove(self, clave):
        self.cur.execute("""  DELETE FROM compras WHERE clave = ?""", (clave, ))
        self.conn.commit()

    def removeNum(self, n_compra):
        self.cur.execute("""  DELETE FROM compras WHERE n_compra = ?""", (n_compra, ))
        self.conn.commit()
        
    def removeNC(self, n_compra, clave):
        self.cur.execute("""  DELETE FROM compras WHERE n_compra = ? AND clave = ?""", (n_compra, clave))
        self.conn.commit()
    def update(self, fecha, n_compra, clave, producto, p_unitario, cantidad, t_compra, proveedor, notas):
        self.cur.execute("""UPDATE compras SET fecha = ?,clave = ?, producto = ?, p_unitario = ?, cantidad = ?, t_compra = ?, proveedor = ?, notas = ? WHERE n_compra = ?""", (fecha, clave, producto, p_unitario, cantidad, t_compra, proveedor, notas, n_compra))
        self.conn.commit()

    def updateu(self, fecha, n_compra, clave, producto, p_unitario, cantidad, t_compra, proveedor, notas):
        self.cur.execute("""UPDATE compras SET fecha = ?, p_unitario = ?, cantidad = ?, t_compra = ?, proveedor = ?, notas = ? WHERE n_compra = ? and clave = ? and producto = ?""", (fecha, p_unitario, cantidad, t_compra, proveedor, notas, n_compra, clave, producto))
        self.conn.commit()

    def deleteall(self):
        self.cur.execute("""DELETE FROM compras """)
        self.conn.commit()

    def __del__(self):
        self.conn.close()


# REPORTE DATABASE
class Reporte_Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        # Create our data base's table
        self.cur.execute(""" CREATE TABLE IF NOT EXISTS reportes (fecha string, n_compra string, clave string, producto string,
        p_unitario real, cantidad real, t_compra real, proveedor string, notas string,
        se text, lista text, pago string, status string, cliente text )""")
        self.conn.commit()

    def fetch(self):
        self.cur.execute(""" SELECT * FROM reportes""")
        rows = self.cur.fetchall()
        return rows
    def inverse_fetch(self):
        self.cur.execute(""" SELECT * FROM reportes ORDER BY n_compra DESC """)
        rows = self.cur.fetchall()
        line= []
        for r in rows:
            line.append(r)
        return line

    def insert(self,fecha, n_compra, clave, producto, p_unitario, cantidad, t_compra, proveedor, notas, se , lista , pago , status, cliente):
        self.cur.execute("""INSERT INTO reportes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (fecha,n_compra, clave, producto, p_unitario, cantidad, t_compra, proveedor, notas, se , lista , pago , status, cliente  ))
        self.conn.commit()

    def remove(self, clave):
        self.cur.execute("""  DELETE FROM reportes WHERE clave = ?""", (clave, ))
        self.conn.commit()
        
    def update(self, fecha, n_compra, clave, producto, p_unitario, cantidad, t_compra, proveedor, notas, se , lista , pago , status, cliente  ):
        self.cur.execute("""UPDATE reportes SET fecha = ?,clave = ?, producto = ?, p_unitario = ?, cantidad = ?, t_compra = ?, proveedor = ?, notas = ?, se = ?, lista = ?, pago = ?, status = ?, cliente = ? WHERE n_compra = ?""", (fecha, clave, producto, p_unitario, cantidad, t_compra, proveedor, notas, se , lista , pago , status, cliente  , n_compra))
        self.conn.commit()

    def updateu(self, fecha, n_compra, clave, producto, p_unitario, cantidad, t_compra, proveedor, notas, se , lista , pago , status, cliente  ):
        self.cur.execute("""UPDATE reportes SET n_compra = ? WHERE fecha = ? and clave = ? and producto = ? and p_unitario = ? and cantidad = ? and t_compra = ? and proveedor = ? and notas = ? and se = ? and lista = ? and pago = ? and status = ? and cliente = ?""", (n_compra, fecha, clave, producto, p_unitario, cantidad, t_compra, proveedor, notas, se , lista , pago , status, cliente  ))
        self.conn.commit()

    def deleteall(self):
        self.cur.execute("""DELETE FROM reportes """)
        self.conn.commit()

    def __del__(self):
        self.conn.close()