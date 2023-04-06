from packages import *

#Nettoyage texte 

def create_columns(df):
    df.columns = ['mentions','tweet_id','author_id', 'author_username', 'author_name', 'author_created_at', 'author_description', 
            'author_followers_count', 'author_following_count', 'author_tweet_count', 'author_listed_count',
            'author_verified', 'created_at', 'geo', 'like_count',
            'quote_count', 'reply_count', 'retweet_count', 'quote_status', 'source', 'text']

def clean_hashtags(df, hashtags = ''):## (ex:"metoo|Metoo|me too|Me Too")
    df = df[df["hashtags"].str.contains(hashtags) == True]
    return (df.dropna(subset = ['hashtags'])[df.lang=='fr'])
          

def remove_rt(df): ## enleve les RT 
    return (df[df.is_retweet == False].drop(['is_retweet','retweeted_status.id','retweeted_status.user.id',
                                      'retweeted_status.user.screen_name','url'],axis=1))

def clean_text(s): ## (utiliser apply)
    return (s.replace("’"," ").replace("'"," ").replace('"'," ").replace("(", " ").replace(")", " ").replace("[", " ").replace("/", " ")
             .replace(":", " ").replace("?"," ").replace("]", " ").replace("\r", " ").replace('\n',' ').replace('\xa0',' ').replace('.',' ')
             .replace('!',' ').replace(","," ").replace("é","e").replace('é','e').replace("è","e").replace("ê","e").replace("à","a")
             .replace("ù","u").replace("û","u").replace("ü","u").replace("ï",'i').replace("â","a").replace("ç","c").replace("ï","i")
             .replace('…','').replace('(','').replace(')','').lower())
    
    
def ban_words(df, limit_inf=-np.inf, limit_sup=np.inf, stemming=False):
    stop_words = stopwords.words('french')
    french_stopwords = list(set(stopwords.words('french')))
    #french_stopwords.extend([])
    banned_words = []

    for word in french_stopwords:
        word = word.replace("é","e").replace("è","e").replace("ê","e").replace("à","a").replace("ù","u").replace("û","u").replace("ç","c").replace("ï","i")
        if stemming : 
          banned_words.append(stemmer.stem(word))
        else :
          banned_words.append(word)

    dic = {}

    for i, row in df.iterrows():
        l = row['text']
        for k, word in enumerate(l):
            if len(word) <= 2:
                continue
            if not(word in l[:k]):
                if word in dic:
                    dic[word] += 1
                else:
                    dic[word] = 1

    banned_words += [k for k,v in dic.items() if (v <= limit_inf or v > limit_sup)]
    return banned_words

def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) 
             if word not in banned_words] for doc in texts]
    return [[word for word in simple_preprocess(str(doc)) 
             if word not in french_stopwords] for doc in texts]

def find_age(text, mineur = False): ## trouve le premier age dans le tweet (utiliser apply)
    if text is not None:
        if mineur == True:
            if 'ans' in text :  
                text[text.index('ans') - 1] = clean_mot2chiffre(text[text.index('ans') - 1])
                #text[text.index('ans') - 1] = (text[text.index('ans') - 1]).apply(clean_mot2chiffre)
                if text[text.index('ans') - 1] != '':
                    if int(text[text.index('ans') - 1]) < 18:
                        return str(text[text.index('ans') - 1])
            else:
                return None
        if mineur == False:
            if 'ans' in text :
                text[text.index('ans') - 1] = clean_mot2chiffre(text[text.index('ans') - 1])
                return str(text[text.index('ans') - 1])
            else:
                return None
    


def find_ages(text): ## trouve tous les ages et les mots autour (nombre suivi de 'ans') (utiliser apply)
    ages = []
    for word in text[:-1]:
        #if word.isnumeric() == True:
            if ((text[text.index(word)+1]=='ans') and (text[text.index(word) - 1]!='depuis') and (text[text.index(word) - 1]!='pendant')):
                ages.append(text[text.index(word)-5:text.index(word)+3])
    return ages
    #return None
    
def find_digits(text): ## trouve tous les ages (nombre suivi de 'ans') (utiliser apply)
    digits = []
    for word in text[:-1]:
        if word.isnumeric() == True:
            digits.append(text[text.index(word)-2:text.index(word)+3])
    return digits
    #return None

def age_victime(text):
    words = ("avais", "agee", "avait", "moi", "ages",'age')
    for age in text:
        if any(s in age for s in words):
            return age
        else:
            return None
        
def clean_mot2chiffre(text):
    #chiffres = []
    if text is not None:        
        if "/" in text:
            text = text[0]
            
        if "-" in text:
            text = text[0]
            
        text = (text.replace('un','1').replace('deux','2').replace('trois','3').replace('quatre','4').replace('cinq','5')
             .replace('six','6').replace('sept','7').replace('huit','8').replace('neuf','9').replace('dix','10')
             .replace('onze','11').replace('douze','12').replace('treize','13').replace('quatorze','14')
             .replace('quinze','15').replace('seize','16').replace('3456789101112131415','3').replace('91011','9').replace('1012','10')
             .replace('trente','30').replace('vingt','20').replace('quarante','40').replace('cinquante','50').replace('soixante','60'))
        
        emp_str = ""
        for m in text:
            if m.isdigit():
                emp_str = emp_str + m
        text = emp_str
        
        #chiffres.append(text)
        
        return text
            
        
def extract_hashtags(df, column):
    # Créer une expression régulière pour trouver les hashtags
    pattern = r"#\w+"
    
    # Appliquer l'expression régulière à chaque chaîne de caractères dans la colonne spécifiée
    hashtags = df[column].apply(lambda x: re.findall(pattern, x))
    
    # Ajouter une nouvelle colonne contenant la liste de hashtags pour chaque ligne
    df['hashtags_extract'] = hashtags
    
    return df
        
        
            