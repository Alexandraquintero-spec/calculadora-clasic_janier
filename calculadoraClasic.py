import sys
import os
import sqlite3
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import math
from tkvideo import tkvideo

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def init_db():
    conexion = sqlite3.connect("usuarios_Clasic.db")
    cursor = conexion.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       usuario TEXT UNIQUE, 
                       password TEXT)''')
    conexion.commit()
    conexion.close()

class AppCalculadoraEscolar:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Clásica")
        
        self.root.minsize(400, 650) 
        self.centrar_ventana()
        
        self.color_fondo = "#FFFFFF"     
        self.color_pantalla = "#7A92A3"  
        self.color_texto_p = "#FFFFFF"   
        self.color_login = "#2C3E50"     
        
        try:
            self.root.iconbitmap(resource_path("icotkin.ico"))
        except:
            pass
            
        self.root.configure(bg=self.color_fondo)
        self.contenedor = tk.Frame(self.root, bg=self.color_fondo)
        self.contenedor.pack(expand=True, fill="both")

        self.mostrar_video_intro()

    def centrar_ventana(self):
        self.root.withdraw() 
        self.root.update_idletasks()
        
        ancho = 400
        alto = 650
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        
        x = (ancho_pantalla // 2) - (ancho // 2)
        y = (alto_pantalla // 2) - (alto // 2) - 30 
        
        self.root.geometry(f'{ancho}x{alto}+{x}+{y}')
        self.root.deiconify()

    def limpiar_pantalla(self):
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def guardar_en_excel(self, usuario, password, accion):
        archivo = "log_Clasic.xlsx"
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        datos = pd.DataFrame({"Usuario": [usuario], "Password": [password], "Accion": [accion], "Fecha": [ahora]})
        try:
            if not os.path.exists(archivo):
                datos.to_excel(archivo, index=False)
            else:
                df = pd.read_excel(archivo)
                pd.concat([df, datos], ignore_index=True).to_excel(archivo, index=False)
        except: pass


    def mostrar_video_intro(self):
        self.limpiar_pantalla()
        self.contenedor.configure(bg="black")
        lbl_v = tk.Label(self.contenedor, bg="black")
        lbl_v.pack(expand=True, fill="both")
        
        try:
            video_p = resource_path("introtkinn.wmv")
            tkvideo(video_p, lbl_v, loop=0, size=(400, 650)).play()
        except:
            tk.Label(lbl_v, text="[ Reproduciendo Intro... ]", fg="white", bg="black").pack(pady=100)

      
        self.root.after(4000, self.mostrar_login)


    def mostrar_login(self):
        self.limpiar_pantalla()
        self.contenedor.configure(bg=self.color_fondo)
        f = tk.Frame(self.contenedor, bg=self.color_login, bd=10, relief="ridge")
        f.place(relx=0.5, rely=0.5, anchor="center", width=350, height=350)

        tk.Label(f, text="ACCESO", font=("Verdana", 22, "bold"), bg=self.color_login, fg="white").pack(pady=20)

      
        self.e_u = tk.Entry(f, font=("Arial", 14), justify="center", bd=3, relief="sunken", fg="grey", width=22)
        self.e_u.pack(pady=10)
        self.e_u.insert(0, "Usuario") 
        self.e_u.bind("<FocusIn>", lambda args: self.clear_placeholder(self.e_u, "Usuario"))
        self.e_u.bind("<FocusOut>", lambda args: self.add_placeholder(self.e_u, "Usuario"))


        caja_pass = tk.Frame(f, bg=self.color_login)
        caja_pass.pack(pady=10)

        self.e_p = tk.Entry(caja_pass, font=("Arial", 14), justify="center", bd=3, relief="sunken", fg="grey", width=17)
        self.e_p.pack(side="left")
        self.e_p.insert(0, "Contraseña")
        self.e_p.bind("<FocusIn>", lambda args: self.clear_placeholder_pass(self.e_p))
        self.e_p.bind("<FocusOut>", lambda args: self.add_placeholder_pass(self.e_p))

        self.btn_ojito = tk.Button(caja_pass, text="🔒", font=("Arial", 12), cursor="hand2", 
                                   bg=self.color_login, fg="white", relief="flat", 
                                   command=self.alternar_visibilidad_pass)
        self.btn_ojito.pack(side="left", padx=(5,0))

      
        self.tooltip_text = "Ver"
        self.btn_ojito.bind("<Enter>", self.mostrar_tooltip)
        self.btn_ojito.bind("<Leave>", self.ocultar_tooltip)
   
        btn_f = tk.Frame(f, bg=self.color_login)
        btn_f.pack(pady=20)

        self.crear_boton_3d(btn_f, "ENTRAR", "#115293", "#115293", self.login, "left")
        self.crear_boton_3d(btn_f, "REGISTRAR", "#8D8989", "#615E5E", self.registrar, "right")

   
    def mostrar_tooltip(self, event):
        x = event.widget.winfo_rootx() + 25
        y = event.widget.winfo_rooty() + 30
        self.tw = tk.Toplevel(event.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tw, text=self.tooltip_text, bg="#333333", fg="#FFD700", relief="solid", bd=1, font=("Arial", 10))
        label.pack(ipadx=4, ipady=2)

    def ocultar_tooltip(self, event):
        if hasattr(self, 'tw') and self.tw:
            self.tw.destroy()
            self.tw = None

   
    def alternar_visibilidad_pass(self):
        if self.e_p.get() == "Contraseña":
            return 
            
        if self.e_p.cget("show") == "*":
            self.e_p.config(show="")
            self.btn_ojito.config(text="👁️")
            self.tooltip_text = "Ocultar"
        else:
            self.e_p.config(show="*")
            self.btn_ojito.config(text="🔒")
            self.tooltip_text = "Ver"
            
 
        if hasattr(self, 'tw') and self.tw:
            for widget in self.tw.winfo_children():
                widget.config(text=self.tooltip_text)

    # --- PLACEHOLDERS ---
    def clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def add_placeholder(self, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="grey")

    def clear_placeholder_pass(self, entry):
        if entry.get() == "Contraseña":
            entry.delete(0, tk.END)
   
            es_candado = self.btn_ojito.cget("text") == "🔒"
            entry.config(fg="black", show="*" if es_candado else "") 

    def add_placeholder_pass(self, entry):
        if entry.get() == "":
            entry.config(show="", fg="grey")
            entry.insert(0, "Contraseña")

    def registrar(self):
        u, p = self.e_u.get(), self.e_p.get()
        if not u or not p or u == "Usuario" or p == "Contraseña":
            messagebox.showwarning("Atención", "Escribe un usuario y contraseña")
            return
        try:
            c = sqlite3.connect("usuarios_Clasic.db")
            c.cursor().execute("INSERT INTO usuarios (usuario, password) VALUES (?, ?)", (u, p))
            c.commit()
            c.close()
            self.guardar_en_excel(u, p, "NUEVO REGISTRO")
            messagebox.showinfo("Listo", "Usuario creado con éxito")
            
            self.e_u.delete(0, tk.END); self.add_placeholder(self.e_u, "Usuario")
            self.e_p.delete(0, tk.END); self.add_placeholder_pass(self.e_p)
            
            
            self.btn_ojito.config(text="🔒")
            self.tooltip_text = "Ver"
        except: messagebox.showerror("Error", "El usuario ya existe")

    def login(self):
        u, p = self.e_u.get(), self.e_p.get()
        if u == "Usuario" or p == "Contraseña":
            messagebox.showwarning("Error", "Ingresa credenciales válidas")
            return
        c = sqlite3.connect("usuarios_Clasic.db")
        r = c.cursor().execute("SELECT * FROM usuarios WHERE usuario=? AND password=?", (u, p)).fetchone()
        c.close()
        if r:
            self.guardar_en_excel(u, p, "INICIO SESION")
            self.mostrar_calculadora() 
        else: messagebox.showerror("Error", "Usuario o clave incorrecta")


    def mostrar_calculadora(self):
        self.limpiar_pantalla()
        self.contenedor.configure(bg=self.color_fondo)
        self.exp = ""
        
        marco_pantalla = tk.Frame(self.contenedor, bg="black", bd=5, relief="sunken")
        marco_pantalla.pack(padx=15, pady=20, fill="x")
        
        self.pantalla = tk.Entry(marco_pantalla, font=("Consolas", 40, "bold"), bg=self.color_pantalla, fg=self.color_texto_p, bd=10, justify="right", relief="flat")
        self.pantalla.pack(fill="x")

        grid = tk.Frame(self.contenedor, bg=self.color_fondo)
        grid.pack(expand=True, fill="both", padx=15, pady=10)

        c_num = ("#E0E0E0", "#BDBDBD")  
        c_ope = ("#2196F3", "#1565C0")  
        c_red = ("#E53935", "#B71C1C")  
        c_grn = ("#4CAF50", "#2E7D32")  
        c_org = ("#FF9800", "#E65100")  
        c_yel = ("#FBC02D", "#F57F17")  

        
        btns = [
            ('7',0,0, c_num), ('8',0,1, c_num), ('9',0,2, c_num), ('/',0,3, c_ope),
            ('4',1,0, c_num), ('5',1,1, c_num), ('6',1,2, c_num), ('*',1,3, c_ope),
            ('1',2,0, c_num), ('2',2,1, c_num), ('3',2,2, c_num), ('-',2,3, c_ope),
            ('0',3,0, c_num), ('.',3,1, c_num), ('^',3,2, c_org), ('+',3,3, c_ope),
            ('C',4,0, c_red), ('Factor',4,1, c_grn), ('=',4,2, c_yel)
        ]

        for (t, f, c, (col_normal, col_hover)) in btns:
            span = 2 if t == '=' else 1 
            fg_color = "black" if col_normal in ["#E0E0E0", "#FBC02D"] else "white"
            
            btn = tk.Button(grid, text=t, font=("Arial", 18, "bold"), bg=col_normal, fg=fg_color,
                            activebackground=col_hover, activeforeground=fg_color,
                            relief="raised", bd=5, command=lambda x=t: self.clic(x))
            btn.grid(row=f, column=c, columnspan=span, sticky="nsew", padx=4, pady=4)
            
            btn.bind("<Enter>", lambda e, h=col_hover: e.widget.config(bg=h))
            btn.bind("<Leave>", lambda e, n=col_normal: e.widget.config(bg=n))
            btn.bind("<Button-1>", lambda e: e.widget.config(relief="sunken"))
            btn.bind("<ButtonRelease-1>", lambda e: e.widget.config(relief="raised"))

        
        for i in range(5): grid.grid_rowconfigure(i, weight=1, uniform="row")
        for i in range(4): grid.grid_columnconfigure(i, weight=1, uniform="col")

    def crear_boton_3d(self, padre, texto, col_normal, col_hover, comando, lado):
        btn = tk.Button(padre, text=texto, font=("Arial", 11, "bold"), bg=col_normal, fg="white",
                        activebackground=col_hover, activeforeground="white",
                        relief="raised", bd=4, command=comando, width=12)
        btn.pack(side=lado, padx=10)
        btn.bind("<Enter>", lambda e: e.widget.config(bg=col_hover))
        btn.bind("<Leave>", lambda e: e.widget.config(bg=col_normal))
        btn.bind("<Button-1>", lambda e: e.widget.config(relief="sunken"))
        btn.bind("<ButtonRelease-1>", lambda e: e.widget.config(relief="raised"))

    def clic(self, t):
        if t == "=":
            try:
                res = eval(self.exp.replace('^', '**'))
                
            
                if isinstance(res, float):
                    res = round(res, 6)         
                    if res.is_integer():        
                        res = int(res)          
              
                
                self.pantalla.delete(0, tk.END)
                self.pantalla.insert(0, str(res))
                self.exp = str(res)
            except:
                self.pantalla.delete(0, tk.END)
                self.pantalla.insert(0, "Error")
                self.exp = ""
        elif t == "C":
            self.exp = ""
            self.pantalla.delete(0, tk.END)
        elif t == "Factor":
            try:
                val = self.pantalla.get()
                n = int(float(val))
                if n < 0:
                    self.pantalla.delete(0, tk.END); self.pantalla.insert(0, "Error")
                    self.exp = ""
                else:
                    res = math.factorial(n)
                    self.pantalla.delete(0, tk.END)
                    self.pantalla.insert(0, str(res))
                    self.exp = str(res)
            except:
                messagebox.showerror("Error", "Ingresa un número entero positivo")
        else:
            self.exp += str(t)
            self.pantalla.delete(0, tk.END)
            self.pantalla.insert(0, self.exp)

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = AppCalculadoraEscolar(root)
    root.mainloop()