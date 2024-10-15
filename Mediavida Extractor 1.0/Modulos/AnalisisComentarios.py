#Lista de palabras extra irrelevantes que no queremos que nos salgan en las frecuencias

from .Librerias import *

extra_stopwords = {"dejar","hecho","dicho","q","x","to","van"
                   ,"quieres","quiero","bueno","hoy","pa","ano","sale","ahi"
                   ,"nadie","vaya","dice","cosas","alguien","tan","puedes","aun",
                   "luego","da","bastante","nunca","parece","aunque","menos","cada",
                   "creo","estan","gracias","puede","igual","mismo","vida","do","mismo",
                   "igual","foro","tambien","voy","verdad","seguro","gente","gran","ver",
                   "vez","siempre","toda","mejor","pues","hace","sigame","mientras",
                   "buena","hilo","bien","buen","aqui","contenido","leader",
                   "the","asi","usuario","necesitas","necesario","va","dia","ahora",'si',
                   'solo', 'ser', 'haber', 'estar', 'ir', 'tener', 'hacer', 'poder', 'decir',
                   "ma","nsfw","acceder","cuenta","web","mail","registrate","identificate","i","buenas","buenos"}

def carga_datos(datos):

    #Buscamos si el archivo está en users o hilos
    try:
        df = pd.read_csv("Hilos/"+datos)
        print("Archivo cargado")
    except FileNotFoundError:
        try:
            df = pd.read_csv("Usuarios/"+datos)
            print("Archivo cargado")
        except FileNotFoundError:
            print("No existe el archivo")
    return df

def normalize_text(text):
    # Convertir a minúsculas
    text = text.lower()
    # Remover acentos
    text = ''.join(
        c for c in unicodedata.normalize('NFKD', text)
        if not unicodedata.combining(c)
    )
    # Remover caracteres no deseados (opcional, dependiendo de la limpieza que necesites)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

def lemmatize_and_count(text, extra_stopwords):
    # Normalizar el texto
    text = normalize_text(text)
    
    # Tokenizar el texto
    tokens = word_tokenize(text)
    
    # Eliminar palabras irrelevantes (stop words)
    stop_words = set(stopwords.words('spanish')).union(extra_stopwords)
    tokens = [word for word in tokens if word not in stop_words]
    
    # Lematizar las palabras
    lemmatizer = WordNetLemmatizer()
    lemas = [lemmatizer.lemmatize(token) for token in tokens]
    
    # Eliminar stopwords adicionales después de la lematización
    lemas = [lema for lema in lemas if lema not in stop_words]
    
    # Contar la frecuencia de cada lema
    frecuencia = Counter(lemas)
    
    return frecuencia

#Top palabras mas usadas
def top_palabras(df,n):
#Limpiamos los /n y metemos todos los comentarios en un string
    df['Comentario'] = df['Comentario'].str.replace('\n', ' ')
    Todos_Coment = ""
    Todos_Coment = ' '.join(df['Comentario'])
    frecuencias = lemmatize_and_count(Todos_Coment,extra_stopwords)

    top_words = frecuencias.most_common(n)

    # Crear un DataFrame con las palabras y sus frecuencias
    df_frec = pd.DataFrame(top_words, columns=['Palabra', 'Frecuencia'])
    
    #Ordenamos de mayor a menor
    df_frec = df_frec.sort_values(by='Frecuencia', ascending=True)
    
    #Contruimos el grafico de barras
    plt.figure(figsize=(10,6))
    plt.barh(df_frec["Palabra"], df_frec["Frecuencia"], color='skyblue')

    # Agregar títulos y etiquetas
    plt.title('Frecuencia de Palabras')
    plt.xlabel('Frecuencia')
    plt.ylabel('Palabras')

    # Mostrar el gráfico
    plt.xticks(rotation=0)  # Rotar etiquetas del eje X si son muchas palabras
    plt.show()

    


    #print(df_frecuencias.to_string(index=False))

#Funcion que busca palabras clave en un post
def busca_palabras(df,palabra):

    #Buscar las filas donde se menciona una determinada palabra
    palabra_buscada = palabra

    df['Comentario'] = df['Comentario'].apply(normalize_text)
    # Crear una máscara booleana donde True indica que la palabra está presente
    df["Palabra"] = df['Comentario'].str.contains(palabra_buscada, case=False, na=False)
    # Filtrar el DataFrame usando la máscara
    df_filtrado = df[df['Palabra']]
    return df_filtrado

#Ranking de comentarios con más manitas
def top_manitas(df,n):
    #Filtramos los comentarios más votados
    df_sorted_na = df.sort_values(by='Likes', ascending=False, na_position='first').head(n)
    df_sorted_na

    #Creamos el url al comentario
    for j in range(len(df_sorted_na)):
        fila = df_sorted_na.iloc[j]
        print("TOP",j+1,"-",fila.Usuario+":", fila.Likes,"manitas")
        link = "https://www.mediavida.com/foro/"+fila.Subforo+"/"+str(fila.Hilo)+str(fila.idHilo)+"/"+str(math.ceil((fila.NumComent/30)))+"#"+str(fila.NumComent)
        print(link)
