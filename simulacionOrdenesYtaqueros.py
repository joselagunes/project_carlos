# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 18:21:40 2021

@author: Jose Miguel Lagunes
"""
import pandas as pd
import numpy as np
import math 
import random as rand
from pynput.keyboard import Key, Listener
from collections import deque
import matplotlib.pyplot as plt
import datetime as dt
import time
from tabulate import tabulate
import tkinter as tk
from tkinter import ttk
from pandastable import Table, TableModel
import threading as tr

    
#%%

class MyTimer():
    def __init__(self):
        self.flag = True
        self.counter = 1
        self.msj = ""
        # self.seconds = seconds
    
    def finish(self):
        self.flag = True
        print("finish")            
        
    def start(self, seconds, msj=""):
        self.msj = msj
        # print('Start')
        self.flag = False
        timer = tr.Timer(seconds, self.finish)
        timer.start()


#%%
"""CLASES DE LOS TAQUEROS"""
class Taqueros():
    def __init__(self):   
        self.before_refill = {
            "Asada": {
                "Cebolla": 200,
                "Cilantro": 200,
                "Guacamole": 100,
                "Salsa": 150,
                "Tortillas": 50,
                "Global_time": 0,
                "Time_list": []
            },
            "Suadero": {
                "Cebolla": 200,
                "Cilantro": 200,
                "Guacamole": 100,
                "Salsa": 150,
                "Tortillas": 50,
                "Global_time": 0,
                "Time_list": []
            },
            "Tripa": {
                "Cebolla": 200,
                "Cilantro": 200,
                "Guacamole": 100,
                "Salsa": 150,
                "Tortillas": 50,
                "Global_time": 0,
                "Time_list": []
            },
            "Adobada": {
                "Cebolla": 200,
                "Cilantro": 200,
                "Guacamole": 100,
                "Salsa": 150,
                "Tortillas": 50,
                "Global_time": 0,
                "Time_list": []
            },
            "Quesadillas": {
                "Global_time": 0,
                "Time_list": []
            }
        }
        
    def refill(self, food, ing):
        time_wait = 0
        if ing == 'Cebolla':
            self.ingrdientes[food]['Cebolla'] = 200 
            time_wait = 10
        elif ing == 'Cilantro':
            self.ingrdientes[food]['Cilantro'] = 200
            time_wait = 10
        elif ing == 'Guacamole':
            self.ingrdientes[food]['Guacamole'] = 100
            time_wait = 20
        elif ing == 'Salsa':
            self.ingrdientes[food]['Salsa'] = 150
            time_wait = 15
        elif ing == 'Tortillas':
            self.ingrdientes[food]['Tortillas'] = 50
            time_wait = 5
        return time_wait
        
#%%


class Orders():
    def __init__(self, orders_simu, taqueros):
        self.ingredientes = ["Cebolla", "Cilantro", "Guacamole", "Salsa"] 
        self.rellenos = [0, 0, 0, 0, 0]
        self.close_run = False
        self.tortillas = 50
        self.df_tiempos = pd.DataFrame()
        self.tiempos = []
        self.ordenes = deque()
        self.orders_in = orders_simu
        self.c = []
        self.tiempo_global = [0,0,0,0]
        self.orders_id = 1
        self.orders_counter = 1
        self.num_orders_simu = len(orders_simu)
        self.taqueros = taqueros
        self.dataframe_deque = pd.DataFrame()
        self.list_values_gui = []

        

    def new_order(self):
        order_num = rand.randrange(0,self.num_orders_simu,1)
        orden = self.orders_in[order_num]
        orden['ID'] = str(self.orders_id)
        orden['Hora'] = dt.datetime.strftime(dt.datetime.today(), 
                                                      format="%I:%M:%S %p")
        for i, order in enumerate(orden['Orden']):
             order['ID orden'] = f'{self.orders_id}-{i+1}'
        self.orders_id += 1 
        # time_order = self.order(orden['Orden'])
        orden['Orden'] = self.order(orden['Orden'])
        self.orders_counter += 1
        orden['Wait time'] = self.tiempo_global
        print()
        self.ordenes.append(orden)
        
        num_tacos_c_t = 0
        flag = False
        num = [[] for i in range(4)]
        for o_list in orden['Orden']:
                # print(o_list)
                type_food = o_list['Comida']
                if o_list['Guiso'] == "Asada":
                    num[0].append(o_list["Cantidad"])
                elif o_list['Guiso'] == "Suadero":
                    num[1].append(o_list["Cantidad"])          
                elif o_list['Guiso'] == "Tripa":
                    if flag == False:
                        num_tacos_c_t += o_list['Cantidad']
   
                elif o_list['Guiso'] == "Cabeza":
                    if flag == False:
                        num_tacos_c_t += o_list['Cantidad']
                      
                elif o_list['Guiso'] == "Adobada":
                    num[3].append(o_list["Cantidad"])   
        num[2].append(num_tacos_c_t)  
        list1 = (orden['Hora'], orden['ID'], orden['Estado'], '', "", str(num[0][0]), str(num[1][0]), str(num[2][0]), str(num[3][0]))     
        list2 = []
        
        for order in orden['Orden']:
            ings = order['Ingredientes']
            for i, ing in enumerate(ings):
                ings[i] = ing[0:3]
            # print(order)
            if order['Comida'] == 'Tacos':
                if order['Guiso'] == 'Asada':
                    list2.append(('', order["ID orden"], '', order['time'], order["Comida"], ings, '-', '-', '-'))
                elif order['Guiso'] == 'Suadero':
                    list2.append(('', order["ID orden"], '', order['time'], order['Comida'], '-', ings, '-', '-')) 
                elif order['Guiso'] == 'Tripa':
                    list2.append(('', order["ID orden"], '', order['time'], order['Comida'], '-', '-', ings, '')) 
                elif order['Guiso'] == 'Cabeza':
                    list2.append(('', order["ID orden"], '', order['time'], order['Comida'], '-', '-', ings, '')) 
                elif order['Guiso'] == 'Adobada':
                    list2.append(('', order["ID orden"], '', order['time'], order['Comida'], '-', '-', '-', ings))         
            else:
                if order['Guiso'] == 'Asada':
                    list2.append(('', order["ID orden"], '', order['time'], order['Comida'], '\u2705', '-', '-', '-'))
                elif order['Guiso'] == 'Suadero':
                    list2.append(('', order["ID orden"], '', order['time'], order['Comida'], '-', '\u2705', '-', '-')) 
                elif order['Guiso'] == 'Tripa':
                    list2.append(('', order["ID orden"], '', order['time'], order['Comida'], '-', '-', '\u2705', '-')) 
                elif order['Guiso'] == 'Cabeza':
                    list2.append(('', order["ID orden"], '', order['time'], order['Comida'], '-', '-', '\u2705', '-')) 
                elif order['Guiso'] == 'Adobada':
                    list2.append(('', order["ID orden"], '', order['time'], order['Comida'], '-', '-', '-', '\u2705')) 
        
        list_tot = [list1, list2]
        self.list_values_gui = list_tot

    
    def order(self, order_dict):
        tiempo_orden_completa = []
        for i, order in enumerate(order_dict):
            cantidad = order['Cantidad']
            ings_temp = order['Ingredientes']
            self.tortillas -= cantidad
            
            time_to_wait = 0
            
            food = order['Guiso']
            if food == 'Cabeza':
                food = 'Tripa' 
            
            for ing in ings_temp:
                # print(self.taqueros.before_refill[food][ing])
                if self.taqueros.before_refill[food][ing] < cantidad:
                    time_to_wait = self.taqueros.refill(food, ing)
                    self.tiempo_global += time_to_wait
 
            if order['Comida'] == 'Tacos':
                tiempo_orden = cantidad * (1 + len(ings_temp)*.5) + time_to_wait
                if order['Guiso'] == 'Asada':
                    self.taqueros.before_refill[food]['Global_time'] += tiempo_orden
                    self.taqueros.before_refill[food]['Time_list'].append(tiempo_orden)
                elif order['Guiso'] == 'Suadero':
                    self.taqueros.before_refill[food]['Global_time'] += tiempo_orden
                    self.taqueros.before_refill[food]['Time_list'].append(tiempo_orden)
                elif order['Guiso'] == 'Tripa':
                    self.taqueros.before_refill[food]['Global_time'] += tiempo_orden
                    self.taqueros.before_refill[food]['Time_list'].append(tiempo_orden)
                elif order['Guiso'] == 'Cabeza':
                    self.taqueros.before_refill[food]['Global_time'] += tiempo_orden
                    self.taqueros.before_refill[food]['Time_list'].append(tiempo_orden)
                elif order['Guiso'] == 'Adobada':
                    self.taqueros.before_refill[food]['Global_time'] += tiempo_orden
                    self.taqueros.before_refill[food]['Time_list'].append(tiempo_orden)
                # print(self.taqueros.before_refill[food])
                
                # self.taqueros.before_refill['Quesadillas']['Time_list'].append(0)
                order_dict[i]['time'] = self.taqueros.before_refill[food]['Global_time']
                order_dict[i]['time_o'] = tiempo_orden
            else:
                tiempo_orden = cantidad * 20
                self.taqueros.before_refill['Quesadillas']['Global_time'] += tiempo_orden 
                self.taqueros.before_refill['Quesadillas']['Time_list'].append(tiempo_orden)
                # self.taqueros.before_refill[food]['Time_list'].append(0)
                
                # print(self.taqueros.before_refill['Quesadillas'])
                order_dict[i]['time'] = self.taqueros.before_refill['Quesadillas']['Global_time']
                order_dict[i]['time_o'] = tiempo_orden
                '''
                if order['Guiso'] == 'Asada':
                    self.taqueros.before_refill['Quesadillas']['Global_time'] += tiempo_orden  
                elif order['Guiso'] == 'Suadero':
                    self.taqueros.before_refill['Quesadillas']['Global_time'] += tiempo_orden
                elif order['Guiso'] == 'Tripa':
                    self.taqueros.before_refill['Quesadillas']['Global_time'] += tiempo_orden
                elif order['Guiso'] == 'Cabeza':
                    self.taqueros.before_refill['Quesadillas']['Global_time'] += tiempo_orden
                elif order['Guiso'] == 'Adobada':
                    self.taqueros.before_refill['Quesadillas']['Global_time'] += tiempo_orden
                '''
                
            
        
        return order_dict
        
    def less_time(self):
        time_last_order = self.ordenes[0]['wait_time']
        self.tiempo_global -= time_last_order
        self.ordenes.popleft()
        for i in range(len(self.ordenes)):
            self.ordenes[i]['wait_time'] -= time_last_order
            
    def while_function(self):
        # def while_infinito(segundos):
        pass
                
                
        # t = tr.Thread(target = contador, args=(5,t_init,))
        # hilos.append(t)
        # t.start()
    
class Orders_simu():
    def __init__(self):
        self.num_orders_simu = 200
        self.big_order = 1
        self.ingredientes = ["Cebolla", "Cilantro", "Guacamole", "Salsa"]
        self.meat = ["Asada", "Suadero", "Tripa", "Cabeza", "Adobada"]
        self.food = ["Tacos", "Quesadillas"]
        self.add_in = ["Con todo", 
                       ""]
        self.proba_food = [7, 3]
        self.probas_ings = [8, 8, 8, 8]
        self.probas_meat = [40, 60, 75, 85, 100]
        self.orders_in = []
        self.order_id = 1
        
        
    def create_orders_simu(self):
        dict_temp_list = []
        for i in range(self.num_orders_simu):
            ran_small = 10
            ran_medium = 20
            ran_big = 35
            size_order = rand.randrange(1, 101, 1)
            if(size_order <= 50):
                ran = ran_small
            elif(size_order <= 35):
                ran = ran_medium
            elif(size_order <= 100):
                ran = ran_big
            
            cantidad = rand.randrange(1,ran+1,1)
            dict_temp = {"ID": "",
                         "Hora": "",
                         "Estado": "Pendiente",
                         "Orden": {}}
            
            counter_down = cantidad+1
            meats = [0,1,2,3,4]
            num_meats = []
            num_tacos = 0
            while(len(meats) > 0):
                if len(meats) == 1:
                    num_tacos = counter_down
                    num = meats.pop()
                    num_meats.append([self.meat[num], num_tacos])
                else:
                    if counter_down == 1:
                        num_tacos = counter_down
                        num = meats.pop()
                        num_meats.append([self.meat[num], num_tacos])
                    else:
                        num_tacos = rand.randrange(1, counter_down, 1)    
                        m = rand.randrange(0, len(meats), 1)
                        num = meats.pop(m)
                        num_meats.append([self.meat[num], num_tacos])
                        counter_down -= num_tacos
            
            for i in range(len(num_meats)):
                type_food = rand.randrange(1,11,1)
                if type_food < self.proba_food[0]:
                    food = 'Tacos'
                else:
                    food = 'Quesadillas'
                num_meats[i].append(food)
                
                ings_temp = []
                for ing, prob in zip(self.ingredientes, self.probas_ings):
                    random_num = rand.randrange(0,11,1)
                    if random_num < prob:
                        ings_temp.append(ing)
                num_meats[i].append(ings_temp)
                
            dict_list = []
            id_o = 1
            for order_food in num_meats:
                if order_food[2] == 'Quesadillas':
                    ings = []
                else :
                    ings = order_food[3]
                    
                order = {"ID orden": "",
                         "Comida": order_food[2],
                         "Guiso": order_food[0],
                         "Estado": "Pendiente",
                         "Cantidad": order_food[1],
                         "Ingredientes": ings,
                        }
                id_o += 1
                        
                dict_list.append(order)
            dict_temp.update({"Orden": dict_list})
            self.order_id+=1
            dict_temp_list.append(dict_temp)    
        return dict_temp_list
    
class Interfaz():
    def __init__(self, new_orders):
        self.root = tk.Tk()
        self.root.title('PythonGuides')
        self.root.geometry('900x500')
        self.root['bg']='#fb0'

        self.new_orders = new_orders
        self.index_prueba = 0
        
        self.trees = []

        self.button_new = tk.Button(self.root, text="Nueva Orden", command=self.nueva_orden)
        self.button_new.pack(side = tk.BOTTOM)
        self.button_update = tk.Button(self.root, text="Actualizar", command="edit")
        self.button_update.pack(side = tk.BOTTOM)

        self.t = tr.Thread(target = self.update)
        self.t.start()



        

        columnas = ("Hora", "ID", "Estado", "T. Espera", "Comida", "Asada", "Suadero", "Tripa/Cabeza", "Adobada")

        self.tree = ttk.Treeview(self.root, columns = columnas, height=30)
        self.tree.column('#0', width=20, stretch=tk.NO)
        for i,c in enumerate(columnas):
            if i == 0:
                self.tree.column(c, anchor=tk.CENTER, width=70)
            elif i == 1:
                self.tree.column(c, anchor=tk.CENTER, width=40)
            else:
                self.tree.column(c, anchor=tk.CENTER, width=100)
        self.tree.heading('#0', text='', anchor=tk.CENTER)
        for c in columnas:
            self.tree.heading(c, text=c, anchor=tk.CENTER)

        
        # self.tree.insert(parent='', index=0, iid=0, text='', values=('','',''))
        self.tree.pack()
        self.root.mainloop()
        
    def insert(self, parent, values_list):
        # print(values)
        # print(self.new_orders.taqueros.before_refill)

        vals_head = values_list[0]
        vals_body = values_list[1]
        rama = self.tree.insert('', vals_head[1], values=vals_head)
        self.trees.append(rama)
        for tup in vals_body:
            self.tree.insert(self.trees[len(self.trees)-1], index = self.index_prueba, values=tup)
        self.index_prueba += 1
        
    def nueva_orden(self):
        self.new_orders.new_order()
        list0 = self.new_orders.list_values_gui
        self.insert("", list0)
    
    def update(self):
        print('dentro de update')
        
        t_asada = MyTimer()
        t_suadero = MyTimer()
        t_tripa = MyTimer()
        t_adobada = MyTimer()
        t_quesadillas = MyTimer()
        
        while(True):
            if len(self.trees) > 0:
                print('dentro de while')
                general_flag = True
                # print(self.new_orders.taqueros.before_refill['Tripa'])
                flag_asada = False
                flag_suadero = False
                flag_tripa = False
                flag_adobada = False
                flag_quesa = False
                
                
                if len(self.new_orders.taqueros.before_refill['Asada']['Time_list']) > 0:
                    asada =  self.new_orders.taqueros.before_refill['Asada']['Time_list'][0]
                    flag_asada = True
                else:
                    asada = 0
                if len(self.new_orders.taqueros.before_refill['Suadero']['Time_list']) > 0:
                    suadero =  self.new_orders.taqueros.before_refill['Suadero']['Time_list'][0]
                    flag_suadero = True
                else:
                    suadero = 0
                if len(self.new_orders.taqueros.before_refill['Tripa']['Time_list']) > 0:
                    tripa =  self.new_orders.taqueros.before_refill['Tripa']['Time_list'][0]
                    flag_tripa = True
                else:
                    tripa = 0
                if len(self.new_orders.taqueros.before_refill['Adobada']['Time_list']) > 0:
                    adobada =  self.new_orders.taqueros.before_refill['Adobada']['Time_list'][0]
                    flag_adobada = True
                else:
                    adobada = 0
                if len(self.new_orders.taqueros.before_refill['Quesadillas']['Time_list']) > 0:
                    quesadillas =  self.new_orders.taqueros.before_refill['Quesadillas']['Time_list'][0]
                    flag_quesa = True
                else:
                    quesadillas = 0                   
                '''
                asada =  self.new_orders.taqueros.before_refill['Asada']['Time_list'][0]
                suadero = self.new_orders.taqueros.before_refill['Suadero']['Time_list'][0]
                tripa = self.new_orders.taqueros.before_refill['Tripa']['Time_list'][0]
                adobada = self.new_orders.taqueros.before_refill['Adobada']['Time_list'][0]
                quesadillas = self.new_orders.taqueros.before_refill['Quesadillas']['Time_list'][0]
                '''
                # self.tree.item(self.trees[0]
                t_asada.start(asada, "")
                t_suadero.start(suadero, "")
                t_tripa.start(tripa, "")
                t_adobada.start(adobada, "")
                t_quesadillas.start(quesadillas, "")
                print(t_asada.flag)
                counter = 0
                
                flags = [0,0,0,0,0]
                
                
                while(general_flag):
                    print(flags)
                    if t_asada.flag:
                        flags[0] = 1
                    if t_suadero.flag:
                        flags[1] = 1
                    if t_tripa.flag:
                        flags[2] = 1
                    if t_adobada.flag:
                        flags[3] = 1
                    if t_quesadillas.flag:
                        flags[4] = 1
                    if sum(flags) == 5:
                        general_flag = False
                    time.sleep(.1)
                print('Finished order')
                self.new_orders.taqueros.before_refill['Asada']['Global_time'] - asada
                self.new_orders.taqueros.before_refill['Suadero']['Global_time'] - adobada
                self.new_orders.taqueros.before_refill['Tripa']['Global_time'] - tripa
                self.new_orders.taqueros.before_refill['Adobada']['Global_time'] - adobada
                self.new_orders.taqueros.before_refill['Quesadillas']['Global_time'] - quesadillas
        
                if flag_asada:
                    self.new_orders.taqueros.before_refill['Asada']['Time_list'].pop(0)
                if flag_suadero:
                    self.new_orders.taqueros.before_refill['Suadero']['Time_list'].pop(0)
                if flag_tripa:
                    self.new_orders.taqueros.before_refill['Tripa']['Time_list'].pop(0)
                if flag_adobada:
                    self.new_orders.taqueros.before_refill['Adobada']['Time_list'].pop(0)
                if flag_quesa:
                    self.new_orders.taqueros.before_refill['Quesadillas']['Time_list'].pop(0)
                self.tree.delete(self.trees[0])
                self.trees.pop(0)
                print(len(self.trees))
    
taqueros = Taqueros()

simulation_orders = Orders_simu()
orders = simulation_orders.create_orders_simu()

# timers_list = [MyTimer(), MyTimer(), MyTimer(), MyTimer(), MyTimer()]
    
new_orders = Orders(orders, taqueros)     


interfaz = Interfaz(new_orders)
interfaz.t.join()




