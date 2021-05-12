from flask import Flask,request,render_template,redirect,url_for
from netaddr import *

app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def hello_world():
    totalplay = []
    if request.method == 'POST':
        ipnetwork = request.form['ip_network']
        subred = request.form['subred']
        subred = int(subred)
        # obtner subredes carnal
        subredes = obtenerTabla(subred,ipnetwork,1)
        rango =  obtenerTabla(subred,ipnetwork,2)
        broadcast = obtenerTabla(subred,ipnetwork,3)
        
        for i in range(subred):
            totalplay.append(Redes(subredes[i],rango[i],broadcast[i]))
            

    return render_template('index.html',ipnetwork='ip',subred='red',totalplay=totalplay)




class Redes:
    def __init__(self,ip, ip_utilizables,broadcast):
        self.ip = ip
        self.ip_utilizables =ip_utilizables
        self.broadcast = broadcast

# redes
no_hay = -1
all_Subredes =[]
# almacenas los posibles subredes basados en la formula 2^n que son los bits
for i in range(24):
    all_Subredes.append(i**2)


#buscar el bit para sumar a la mascara 
def check_bit(num_de_subred):
    #Encontrar el bits
    for x in all_Subredes:
        if num_de_subred == x:
            return x
        if num_de_subred < x:
            return x
    return -1

#obtner todo alv
def obtenerTabla(num_de_subred,ip_network,opcion):
    las_IP = []
    ip_utilizables=[]
    broadcastss = []
    ip = IPNetwork(ip_network)
    bitss = check_bit(num_de_subred)
    if bitss > no_hay:
        #calculamos la nuevas mascara
        nueva_mascara = ip.prefixlen + all_Subredes.index(bitss)
        ip.prefixlen = nueva_mascara
        if opcion == 1:
            for i in range(num_de_subred):
                las_IP.append(ip.next(i))
            return las_IP
        if opcion == 2:
            
            for i in range(num_de_subred):
                antepenultima = len(ip.next(i)) -2
                rangos = ip.next(i)[1],ip.next(i)[antepenultima]
                ip_utilizables.append(rangos)
            return ip_utilizables    
        if opcion == 3:
            for i in range(num_de_subred):
                 broadcastss.append(ip.next(i).broadcast)
            return broadcastss

