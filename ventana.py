from tkinter import *
from tkinter import ttk
from countries import *
from tkinter import messagebox

class Ventana(Frame):

    paises = Countries()

    def __init__(self,master=None):
        super().__init__(master, width=680, height=260)
        self.master = master
        self.pack()
        self.create_widgets()
        self.llenaDatos()
        self.habilitarBtnGuar('disabled')
        self.habilitarCajas('disabled')
        self.id=-1

    def habilitarCajas(self, estado):
        # self.txtISO3.configure(state='disabled') # Desactivar casilla de texto o Entrada
        # self.txtISO3.configure(state='normal') # Habilitar cajas de entrada
        self.txtISO3.configure(state=estado)
        self.txtCapital.configure(state=estado)
        self.txtCurrency.configure(state=estado)
        self.txtCountry.configure(state=estado)

    def habilitarBtnOper(self, estado):
        self.btnNuevo.configure(state=estado)
        self.btnModificar.configure(state=estado)
        self.btnEliminar.configure(state=estado)

    def habilitarBtnGuar(self, estado):
        self.btn_save.configure(state=estado)
        self.btn_cancel.configure(state=estado)

    def limpiarCajas(self):
        self.txtCapital.delete(0, END)
        self.txtCurrency.delete(0, END)
        self.txtISO3.delete(0, END)
        self.txtCountry.delete(0, END)

    def limpiarGrid(self):
        for item in self.grid.get_children():
            self.grid.delete(item)

    def llenaDatos(self):
        datos = self.paises.consulta_paises()
        for row in datos:
            self.grid.insert('',END,text=row[0],values=(row[1],row[2], row[3],row[4]))

        if len(self.grid.get_children()) > 0:
            self.grid.selection_set(self.grid.get_children()[0])
    def Nuevo(self):
        self.habilitarCajas('normal')
        self.habilitarBtnOper('disabled')
        self.habilitarBtnGuar('normal')
        self.limpiarCajas()
        self.txtISO3.focus()

    def Guardar(self):
        if self.id == 1:
            self.paises.insertar_pais(self.txtISO3.get(),self.txtCountry.get(),self.txtCapital.get(),self.txtCurrency.get())
            messagebox.showinfo('Insertar', 'Elemento insertado correctamente.')
        else:
            self.paises.modificar_pais(self.id,self.txtISO3.get(),self.txtCountry.get(),self.txtCapital.get(),self.txtCurrency.get())
            messagebox.showinfo('Modificar', 'Elemento modificado correctamente.')
            self.id=-1
        self.limpiarGrid()
        self.llenaDatos()
        self.limpiarCajas()
        self.habilitarBtnGuar('disabled')
        self.habilitarBtnOper('normal')
        self.habilitarCajas('disabled')

    def Modificar(self):
        selected = self.grid.focus()
        clave = self.grid.item(selected, 'text')

        if clave == '':
            messagebox.showwarning('Modificar', 'Debes seleccionar un elemento.')
        else:
            self.id=clave
            self.habilitarCajas('normal')
            valores = self.grid.item(selected, 'values')
            self.limpiarCajas()

            self.txtISO3.insert(0,valores[0])
            self.txtCountry.insert(0,valores[1])
            self.txtCapital.insert(0,valores[2])
            self.txtCurrency.insert(0,valores[3])

            self.habilitarBtnOper('disabled')
            self.habilitarBtnGuar('normal')
            self.txtISO3.focus()

    def Eliminar(self):
        selected = self.grid.focus()
        clave = self.grid.item(selected, 'text')

        if clave == '':
            messagebox.showwarning('Eliminar', 'Debes seleccionar un elemento.')
        else:
            valores = self.grid.item(selected, 'values')
            data = str(clave) + ', ' + valores[0] + ', ' + valores[1]
            r = messagebox.askquestion('Eliminar', 'Deseas eliminar el registro seleccionado?\n' + data.center(49, ' '))#Respuesta

            if r == messagebox.YES:
                n = self.paises.eliminar_pais(clave)
                if n == 1:
                    messagebox.showinfo('Eliminar', 'Elemento eliminado correctamente.')
                    self.limpiarGrid()
                    self.llenaDatos()
                else:
                    messagebox.showwarning('Eliminar', 'No fue posible eliminar el elemento')

    def Cancelar(self):
        r = messagebox.askquestion('Cancelar','Esta seguro que dease cancelar la operación actual')
        if r == messagebox.YES:
            self.limpiarCajas()
            self.habilitarBtnGuar('disabled')
            self.habilitarBtnOper('normal')
            self.habilitarCajas('disabled')
            
    def create_widgets(self):

        frame1 = Frame(self, background="#bfdaff")
        frame1.place(x=0, y=0,width=93,height=259)

        self.btnNuevo = Button(frame1, text='Nuevo', command=self.Nuevo, background='blue', fg='white')
        self.btnNuevo.place(x=5,y=50,width=80,height=30)

        self.btnModificar = Button(frame1, text='Modificar', command=self.Modificar, background='blue', fg='white')
        self.btnModificar.place(x=5,y=90,width=80,height=30)

        self.btnEliminar = Button(frame1, text='Eliminar', command=self.Eliminar, background='blue', fg='white')
        self.btnEliminar.place(x=5,y=130,width=80,height=30)

        frame2 = Frame(self, background='#d3dde3')
        frame2.place(x=95,y=0,width=150,height=259)

        lbl1 = Label(frame2,text='ISO3: ')
        lbl1.place(x=3,y=5)

        self.txtISO3=Entry(frame2)
        self.txtISO3.place(x=3,y=25,width=50,height=20)

        lbl2= Label(frame2,text='Country name: ')
        lbl2.place(x=3,y=55)

        self.txtCountry=Entry(frame2)
        self.txtCountry.place(x=3,y=75,width=100, height=20)  

        lbl3 = Label(frame2, text='Capital: ')
        lbl3.place(x=3,y=105)

        self.txtCapital=Entry(frame2)
        self.txtCapital.place(x=3, y=125,width=100,height=20) 

        lbl4=Label(frame2, text='Currency code :')  
        lbl4.place(x=3,y=155)

        self.txtCurrency=Entry(frame2)
        self.txtCurrency.place(x=3,y=175,width=50,height=20)   

        self.btn_save=Button(frame2, text='Guardar', command=self.Guardar, background='green', fg='white')
        self.btn_save.place(x=10, y=210, width=60, height=30)

        self.btn_cancel=Button(frame2, text='Cancelar', command=self.Cancelar, background='green', fg='white')
        self.btn_cancel.place(x=80,y=210,width=60, height=30)

        frame3 = Frame(self, background='yellow')
        frame3.place(x=247,y=0,width=420,height=259)

        self.grid=ttk.Treeview(frame3,columns=('col1','col2','col3','col4'))

        self.grid.column('#0',width=60)
        self.grid.column('col1',width=70, anchor=CENTER)
        self.grid.column('col2',width=90, anchor=CENTER)
        self.grid.column('col3',width=90, anchor=CENTER)
        self.grid.column('col4',width=90, anchor=CENTER)

        self.grid.heading('#0', text='Id', anchor=CENTER)
        self.grid.heading('col1', text='ISO3', anchor=CENTER)
        self.grid.heading('col2', text='Country', anchor=CENTER)
        self.grid.heading('col3', text='Capital', anchor=CENTER)
        self.grid.heading('col4', text='Currency Code', anchor=CENTER)

        self.grid.pack(side=LEFT,fill = Y)

        sb = Scrollbar(frame3,orient=VERTICAL)
        sb.pack(side=RIGHT, fill = Y)
        self.grid.config(yscrollcommand=sb.set)
        sb.config(command=self.grid.yview)

        self.grid['selectmode']='browse'