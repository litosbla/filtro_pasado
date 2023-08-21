import json
import random
def error(msg):
    print("!!!!! ERROR --->",msg.upper(), end=" ")
    input("Digite cualquier tecla para continuar")
def leer_numero(msg):
    while True:
        try:
            numero=int(input(msg))
            if numero < 0:
                error("Número invalido")
                continue
            return numero
        except ValueError:
            error("Número invalido")
            continue
def leer_string(msg):
    while True:
        try:
            caracter=input(msg)
            if caracter=="":
                error("Caracter invalido")
                continue
            return caracter
        except ValueError:
            error("Caracter invalid")
            continue
def leer_rango(msg,min,max):
    while True:
        try:
            valor=int(input(msg))
            if valor > min-1 and valor < max+1:
                return valor
            error(f"Valor invalido, tiene que estar entre {min} y {max}")
            continue
        except ValueError:
            error(f"Valor invalido, tiene que estar entre {min} y {max}")
            continue
def menu():
    lista_opciones=["Añadir_cliente","Modificar","Eliminar","Hacer Reportes","Añadir_tarjeta","Salir"]
    print("="*30)
    print("\tMENÚ TARJETAS DE CREDITO")
    print("\t")
    [print(f"\t{i+1} --> {elemento}")for i,elemento in enumerate(lista_opciones)]
    op=leer_rango("\tDigite la accion a realizar por indice",1,7)
    return op

def inicializar_json():
    data={"clientes":{}}
    print(data)
    with open("tarjetas.json","w") as file:
        json.dump(data,file,indent=4)   
def leer_json():
    with open("tarjetas.json","r") as file:
        data=json.load(file)
    return data
def upload_json(data):
    with open("tarjetas.json","w") as file:
        json.dump(data,file,indent=4)
def validar_otro_ciclo(msg):
    while True:
        try:
            s=input(msg)
            if s.lower() == "si":
                return True
            if s.lower() == "no":
                return False
            error("Valor invalido ,(si/no)")
            continue
        except ValueError:
            error("Valor invalido ,(si/no)")
            continue

def leer_lista(msg1,msg,lista):
    while True:
        print(msg1)
        [print(f"\t{i+1} -> {elemento}")for i,elemento in enumerate(lista)]
        valor=leer_numero(msg)
        if valor in lista:
            return valor
        if valor <= len(lista):
            return lista[valor-1]
        
        print("@Valor incorrecto, solo se admiten los indices o su respectivo valor: ")
        [print(f"\t{i+1} -> {elemento}",end=" ")for i,elemento in enumerate(lista)]
        
        input("\nDigite cualquier tecla para continuar")
        continue
def leer_fecha(msg):
    while True:
        fecha=leer_string(msg)
        partes=fecha.split("/")
        print(partes)
        if len(partes) == 2 and (len(partes[0])==2 or len(partes[0])==1) and len(partes[1])==4 and partes[0].isdigit() and partes[1].isdigit() and int(partes[0])>0 and int(partes[0])<13 and int(partes[1])>2023:
            return f"{partes[0]:0>2}/{partes[1]}"
        error("feha invalida, el formato es mm/yyyy , tenga en cuenta que el año debe ser mayor al actual")
        continue
def validar_cedula(msg,data):
    while True:
        cedula=leer_numero(msg)
        if cedula in data["clientes"].keys():
            error("cedula existente")
            continue
        return cedula
def Añadir_cliente(id):
    var=False
    if id==0:
        var=True
    data=leer_json()
    
    while True:
        nombre=leer_string("Digite el nombre del cliente")
        cedula=validar_cedula("Digite la cédula del cliente",data) if var==True else id
        numero=leer_numero("Digite el numero telefonico")
        sexo=leer_string("Digite el sexo")
        if var==True:
            datos_cliente={
                "nombre":nombre,
                "numero":numero,
                "sexo":sexo,
                "tarjetas":{}
            }
            data["clientes"][cedula]=datos_cliente
            print(data)
            if validar_otro_ciclo("Desea agregar la tarjeta de una vez?(si/no)"):
                upload_json(data)
                Añadir_tarjeta(cedula,False)
                break
            if validar_otro_ciclo("Desea agregar otro cliente?"):
                continue
            upload_json(data)
            break

        else:
            datos_cliente={
                "nombre":nombre,
                "numero":numero,
                "sexo":sexo,
                "tarjetas":data["clientes"][cedula]["tarjetas"]
            }
            data["clientes"][cedula]=datos_cliente
            #upload_json(data)
            print(data)
            if len(data["clientes"][cedula]["tarjetas"])==0:
                if validar_otro_ciclo("No se encuentran tarjetas, Desea agregar la tarjeta de una vez?(si/no)"):
                    upload_json(data)
                    Añadir_tarjeta(cedula,False)
                    break
                upload_json(data)
                break
            else:
                if validar_otro_ciclo("Desea modificar las tarjetas asociadas de una vez?(si/no)"):
                    upload_json(data)
                    Modificar_tarjeta(cedula,True)
                    break
               
                upload_json(data)
                break

def validar_tarjeta(msg,data):
    while True:
        lista_tarjetas=[]
        [lista_tarjetas.extend(dic_cedula["tarjetas"].keys()) for cedula,dic_cedula in data["clientes"].items()]
        print(lista_tarjetas)
        nume_tar=str(leer_numero(msg))
        if nume_tar in lista_tarjetas:
            error("Numero de tarjeta existente")
            continue
        return nume_tar
def Añadir_tarjeta(cedula,viene_de_modificar:bool):
    data=leer_json()
    var=True
    
    if len(data["clientes"])==0:
        print("\t NO SE PUEDE GENERAR TARJETAS DE CREDITO SI NO EXISTEN CLIENTES")
        input("Digite cualquier tecla para regresar al menu")
        var=False
    
       
    while var:
        if len(data["clientes"][f"{cedula}"]["tarjetas"])==0 and viene_de_modificar==True:
            print(f"Para el cliente con {cedula} no existen tarjetas, a continuacion agregue una antes de modificar -->")
        if viene_de_modificar==True and len(data["clientes"][f"{cedula}"]["tarjetas"])!=0:
            num_tarjeta=leer_lista(f"Para el cliente {cedula} las tarjetas son ","Digite el indice o el id de la tarjeta que quiere modificar",[key for key, value in data["clientes"][f"{cedula}"]["tarjetas"].items()])
            tipo=leer_lista("Los tipos de tarjetas son: ","Digite el tipo de tarjeta: ",["Master Card","Visa","Amércian Expres"])
        else:
            tipo=leer_lista("Los tipos de tarjetas son: ","Digite el tipo de tarjeta: ",["Master Card","Visa","Amércian Expres"])
            num_tarjeta=validar_tarjeta("Digite el número de tarjeta: ",data)
        fecha=leer_fecha("Digite la fehca (mm/yyyy)")
        codigo=random.randint(100,999)
        
        id=leer_lista("Los ids de clientes existentes son:","Digite el indice del cliente que quiere buscar",[ids for ids,dic_cliente in data["clientes"].items()]) if cedula ==0 else cedula
        tarjeta={
            "tipo":tipo,
            "fecha":fecha,
            "codigo":codigo
        }
        
        data["clientes"][f"{id}"]["tarjetas"][num_tarjeta]=tarjeta
        print(data)
        if viene_de_modificar==True:
            upload_json(data)
            break
        else:
            if validar_otro_ciclo("Desea agregar otra tarjeta?"):
                continue
            upload_json(data)
            break
def Modificar_cliente(id):
    Añadir_cliente(id)
    

def Modificar_tarjeta(id,validar):
    Añadir_tarjeta(id,validar)
    

def Modificar():
    data=leer_json()
    
    while True:
        s=leer_lista("Hay dos opciones para modificar","Digite el indice o el texto de la opcion",["Modificar Cliente","Modificar Tarjeta"])
        i=""
        while True:
            if s == "Modificar Cliente":
                i="otro cliente"
                id=leer_lista("Los ids de clientes existentes son:","Digite el indice o la opcion del cliente que quiere Modificar",[ids for ids,dic_cliente in data["clientes"].items()]) 
                Modificar_cliente(id)
                
            else:
                print("Para modificar una tarjeta, primero necesitamos saber el id del cliente")
                id=leer_lista("Los ids de clientes existentes son:","Digite el indice o el id a modificar tarjeta",[ids for ids,dic_cliente in data["clientes"].items()]) 
                i="otra tarjeta"
                Modificar_tarjeta(id,True)
            print("Modificaciones guardadas")
            if validar_otro_ciclo(f"Desea modificar {i}"):
                continue
            break
        if validar_otro_ciclo("Desea modifitar otra cosa?"):
            continue
        break

def Eliminar():
    data=leer_json()
    while True:
        s=leer_lista("Hay dos opciones para Eliminar","Digite el indice o el texto de la opcion",["Eliminar Cliente","Eliminar Tarjeta"])
        i=""
        while True:
                
            if s =="Eliminar Cliente":
                i="otro cliente"
                id=leer_lista("Los ids de clientes existentes son:","Digite el indice o la opcion del cliente que quiere Eliminar",[ids for ids,dic_cliente in data["clientes"].items()]) 
                del data["clientes"][f"{id}"]
                upload_json(data)
                print("Eliminado corectamente")
            else:
                print("Para Eliminar una tarjeta, primero necesitamos saber el id del cliente")
                i="otra tarjeta"
                id=leer_lista("Los ids de clientes existentes son:","Digite el indice o la opcion del cliente que quiere eliminarle alguna tarjeta",[ids for ids,dic_cliente in data["clientes"].items()]) 
                numero_tarjeta=leer_lista("Los ids de las tarjetas son: ","Digite el indice o el numero de la tarjeta a eliminar",[key for key,value in data["clientes"][f"{id}"]["tarjetas"].items()])
                del data["clientes"][f"{id}"]["tarjetas"][f"{numero_tarjeta}"]
                upload_json(data)
                print("Eliminado correctamente")
            
            if validar_otro_ciclo(f"Desa eliminar {i}?"):
                continue
            break
        if validar_otro_ciclo("Desea eliminar otra cosa?"):
            continue
        break
def mostrar_cedula(cedula,dic_cedula):
    print("="*30)
    print(f"@@para el cliente con cedula {cedula}")
    [print(keys," ---> ",value) if keys != "tarjetas" else [mostrar_tarjeta(tar,datos_tar) for tar,datos_tar in value.items()]for keys,value in dic_cedula.items()]
    
def mostrar_tarjeta(numero_tarjeta,diccionario_tarjeta):
    print(f"\tTarjeta con número {numero_tarjeta}")
    [print(keys,"  --> ",values) for keys,values in diccionario_tarjeta.items()]
def Hacer_reportes():
    data=leer_json()
    print("="*30)
    print("\tHacer reportes")
    
    [
       mostrar_cedula(cedula,dic_cedula)
     for cedula,dic_cedula in data["clientes"].items()]#CICLO POR PERSONA
    print("="*30)
    input("Digite cualquier tecla para continuar con el menu")

def main():
    inicializar_json()
    while True:
        op =menu()
        if op==1:
            Añadir_cliente(0)
        elif op==2:
            Modificar()
            print("que hace perrro")
        elif op==3:
            Eliminar()
            print("que hace perrro")
        elif op==4:
            Hacer_reportes()
        elif op==5:
            Añadir_tarjeta(0,False)
        elif op==6:
            print("Good Bye")
            break
        
main()