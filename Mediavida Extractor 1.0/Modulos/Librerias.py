# Librerias
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from bs4 import BeautifulSoup
import math
import time
from datetime import datetime
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
import unicodedata
import re
import os 

#Librerias necesarias para hacer funcionar la parte de las palabras más frecuentes (en ExtraccionDatos.py)
#import nltk
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')