#Funcion que encuentra el número máximo de página

from .Librerias import *

## Función para encontrar el nº máximo de páginas de un hilo, referente a la esquina inferior derecha de la navegación

def find_max_pag(soup): 
    num_pags = soup.find("ul", attrs = {"class": "pg"}) ##Localizamos La parte inferior der para navegar por las páginas
    
    if num_pags != None: ## Si no ha comentado en tantos hilos como para tener páginas que recorrer en su usuario o no ha comentado más de 30 vaces en un hilo será None
        tam_iconos = len(num_pags) #Tamaño del bloque, 1,2,...,X puede variar de 2 a 4 
        num_iconos = num_pags.find_all("li") ## Encuentre el numero de iconitos
        max_pag = int(num_iconos[tam_iconos-1].text) #El ultimo icono hace referencia a la página máxima que tiene. Pasamos el texto a int
        return max_pag
    else: 
        max_pag = 1 ## Si no hay páginas pues nos dirá que el máximo de páginas será 1
        return max_pag


#Función que saca todos los hilos en los que ha comentado el usuario (solo para analisis_usuario())

def saca_hilos(user):
    url = "https://www.mediavida.com/id/"+user+"/posts" #Vamos a la parte de posts del usuario
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    retardo = 0.5  
    hilos_list = [] # Unicializamos la array que contendrá el enlace a todos los hilos comentarios
    max_pag = find_max_pag(soup) ## Sacamos el numero máximo de páginas  
    
    ## SACAMOS LAS PAGINAS DEL USUARIO   
    for pag in range(1,max_pag+1): #Recorre 
        
        time.sleep(retardo) # No hay que cargarse el servidor xD
    
        if pag != 1: # Si hay más de 1 página modificará la url con la página correspondiente
            url2 = url+"/"+str(pag) #pasamos a string el número de página
            response = requests.get(url2)
            soup = BeautifulSoup(response.text, "html.parser")
            print("Recopilando hilos comentados...", round((pag*100/max_pag),2),"%  ",end="\r")
    
        hilos = soup.find_all("div", attrs = {"class":"thread"}) 
        for hilo in hilos:
            
            id_hilo = hilo.a["id"][1:] ## Sacamos la id del hilo
            hilo_url = hilo.find("a")["href"] ## Sacamos la url
    
            hilo_url = hilo_url.split("-") ## Spliteamos para construir el enlace quitando la parte final del guion en el for siguiente
            new_url = "" ## Creamos la nueva url formada
            
            for i in range(len(hilo_url)-1): #Constuimos la url  
                new_url += hilo_url[i]+"-"
        
            new_url ="https://www.mediavida.com/"+ new_url + id_hilo +"?u="+user #Le añadimos lo que falta
            hilos_list.append(new_url) #La metemos en la lista
            
    return hilos_list ## Devuelve todos los hilos en los que el usuario ha comentado


# EXTRACCION DATOS DE UN USUARIO EN CONCRETO

def analisis_usuario(user):
    print("Analizando al usuario:",user)
    retardo = 0.1
    Info = [] 
    
    #Función que recopila todo los hilos comentados
    hilos_list = saca_hilos(user)
    conteo_hilos = len(hilos_list)
    print("                                                                       ",end="\r") #Limpiamos la entrada anterior
    
    #Por cada hilo en el que se ha comentado...
    for hilo in hilos_list:
        url = hilo
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        print("Quedan por analizar:",conteo_hilos,"hilos    ",end="\r")
        idHilo = url.split("-")[-1]
        idHilo = idHilo.split("?")[0]
        
        #Puede no existir una etiqueta (tag)
        try:
            Etiqueta = soup.find("ul", attrs={"class": "tag-list"}).find("span").text
        except AttributeError:
            Etiqueta = "None"

        conteo_hilos -= 1
        time.sleep(retardo) # Para no saturar el servidor
        
        ## Sacamos el numero de páginas de ese hilo
        max_pag = find_max_pag(soup)
        
        for pag in range(1,max_pag+1): #Recorrera todas las páginas de comentarios
               
            if pag != 1: #Si el número de páginas es mayor que 1 nos irá actualizando la url con la página correspondiente     
                url = hilo+"&pagina="+str(pag) #pasamos a string el número de página
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "html.parser")
    
            bloque = soup.find_all("div", attrs = {"data-autor":user}) ## todo el bloque de comentarios del usuario. 30 para cada página completa 
            
            for tag in bloque: ## Recorremos cada comentario del bloque de comentarios
                InfoPost = [] ## Inicializamos cada vez que recorre un post
                
                #Usuario
                Usuario = tag.find("div", attrs = {"class":"post-avatar"}).find("a").get("href")[4:] ## Si el usuario estaba activo era muy engorroso coger su nombre
                InfoPost.append(Usuario)

                #Subforo
                SubForo = url.split("/")[5]
                InfoPost.append(SubForo)
                
                #Id del hilo
                InfoPost.append(idHilo)
                
                #Titulo del hilo
                NombreHiloRaw = url.split("/")[6].split("-") #Dividimos en parte, sabemos que a partir de la 5º / divide bien
                NombreHiloRaw = NombreHiloRaw[0:len(NombreHiloRaw)-1] ##Quitamos la ultima parte referente a la id del hilo
                NombreHilo = ""
                for palabra in NombreHiloRaw: #Construimos el nombre del hilo
                    NombreHilo +=palabra + "-"
                InfoPost.append(NombreHilo)
                
                #Etiqueta
                InfoPost.append(Etiqueta)
                
                #Numero de comentario
                NumComent = tag.find("a")["name"]
                InfoPost.append(NumComent)
                
                #Comentarios
                Comentario = tag.find("div", attrs = {"class":"post-contents"}).text
                InfoPost.append(Comentario)
                
                #Manitas
                manitas = tag.find("div", attrs = {"class":"post-controls"}).span.text ## manitas
                manitas = int(manitas) ## Las pasamos a int
                InfoPost.append(manitas)
                
                #Fecha
                fecha_str = tag.find("span", attrs = {"class":"rd"}).get("title")## Cogemos la fecha, con el get pillamos el titulo
                fecha_limpia = fecha_str.replace(" a las ", " ")            
                formato = "%d/%m/%y %H:%M"              
                FechaPost = datetime.strptime(fecha_limpia, formato)   
                InfoPost.append(FechaPost)
                
                #Introducimos toda la información obtenida
                Info.append(InfoPost)           
                InfoPost = []

    #CREACION DEL DATASET Y GUARDADO DE ESTE
    print("Analisis finalizado, guardando dataset...")
    columnas = ["Usuario", "Subforo","idHilo", "Hilo","Etiqueta", "NumComent", "Comentario", "Likes", "Fecha"]
    # Crear un DataFrame vacío con las columnas especificadas
    df = pd.DataFrame(columns=columnas)

    for fila in Info: #Por cada lista individual dentro de conjunto de listas
        df_nueva_fila = pd.DataFrame([fila], columns=columnas) #Crea un df con esa fila
        df = pd.concat([df, df_nueva_fila], ignore_index=True) #Añadelo al conjunto total
    
    df.to_csv(os.path.join("Usuarios", user + ".csv"), index=False)
    print("Dataset guardado")


# EXTRACCION DATOS DE UN HILO EN CONCRETO
    
def analisis_hilo (hilo):
    url = hilo
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    Info = []

    #Variables fijas: Subforo, idHilo, etiqueta Título del hilo
    SubForo = url.split("/")[4]
    idHilo = url.split("-")[-1]
    try:
        Etiqueta = soup.find("ul", attrs={"class": "tag-list"}).find("span").text
    except AttributeError:
        Etiqueta = "None"

    NombreHiloRaw = url.split("/")[5].split("-") #Dividimos en parte, sabemos que a partir de la 5º / divide bien
    NombreHiloRaw = NombreHiloRaw[0:len(NombreHiloRaw)-1] ##Quitamos la ultima parte referente a la id del hilo
    NombreHilo = ""
    for palabra in NombreHiloRaw: #Construimos el nombre del hilo
        NombreHilo +=palabra + "-"
        
    max_pag = find_max_pag(soup)

    for pag in range(1,max_pag+1): #Recorrera todas las páginas de comentarios
        print("Analizando página",pag,"/",max_pag,end="\r")    
        if pag != 1: #Si el número de páginas es mayor que 1 nos irá actualizando la url con la página correspondiente  
            
            time.sleep(0.1)   
            response = requests.get(url+"/"+str(pag))
            soup = BeautifulSoup(response.text, "html.parser")
        
    #Cogemos toda la información de la página referente al bloque de comentarios
    
        bloque = soup.find("div", attrs = {"id":"posts-wrap"})
        Comentarios = bloque.find_all("div", id=True)
                    
        for post in Comentarios:
            
            #Inicializamos la lista donde almacenamos toda la informacion del post
            InfoPost = []
            
            #Usuario
            Usuario = post["data-autor"]
            InfoPost.append(Usuario)
            
            #Subforo,id,título,etiqueta
            InfoPost.append(SubForo)
            InfoPost.append(idHilo)
            InfoPost.append(NombreHilo)  
            InfoPost.append(Etiqueta) 
            
            #Numero de comentario            
            NumComent = post.find("a")["name"]
            InfoPost.append(NumComent)
            
            #Comentarios            
            Comentario = post.find("div", attrs = {"class":"post-contents"}).text
            InfoPost.append(Comentario)
            
            #Manitas        
            Manitas = post.find("div", attrs = {"class":"post-controls"}).span.text ## Manitas
            Manitas = int(Manitas) ## Las pasamos a int
            InfoPost.append(Manitas)
                        
            #Fecha
            fecha_str = post.find("span", attrs = {"class":"rd"}).get("title")## Cogemos la fecha, con el get pillamos el titulo
            fecha_limpia = fecha_str.replace(" a las ", " ")            
            formato = "%d/%m/%y %H:%M"              
            FechaPost = datetime.strptime(fecha_limpia, formato)   
            InfoPost.append(FechaPost)
            
            #Metemos toda la info del post en la lista del hilo
            Info.append(InfoPost)
    
        
    #CREACION DEL DATASET Y GUARDADO DE ESTE
    columnas = ["Usuario", "Subforo","idHilo", "Hilo","Etiqueta", "NumComent", "Comentario", "Likes", "Fecha"]
        # Crear un DataFrame vacío con las columnas especificadas
    df = pd.DataFrame(columns=columnas)

    for fila in Info: #Por cada lista individual dentro de conjunto de listas
        df_nueva_fila = pd.DataFrame([fila], columns=columnas) #Crea un df con esa fila
        df = pd.concat([df, df_nueva_fila], ignore_index=True) #Añadelo al conjunto total
        
    df.to_csv(os.path.join("Hilos", NombreHilo + ".csv"), index=False)
    print("Dataset guardado")