import PyPDF2
import os
from os import walk, path
import random
import re
import pandas as pd
from IPython.display import display

import warnings
warnings.filterwarnings("ignore")

def read_pdf(file):
    try:
        #TB: according to PyPDF2 docs, strict default value is now False; why not set strict=True in a try/except loop?
        pdfFile = PyPDF2.PdfReader(open(file, "rb"), strict=False)
        text = ""
        for page in pdfFile.pages:
            text += " " + page.extract_text()
        return text
    except:
        return ""

import openai
from transformers import GPT2TokenizerFast
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

import tiktoken
ENCODING = "gpt2"
encoding = tiktoken.get_encoding(ENCODING)
    
filepath = "/Users/tillybrooks/Library/CloudStorage/Box-Box/2024Spring/ra/data/2-2-2024/" # this is where we'll be looking for files
f = []
for (dirpath, dirnames, filenames) in walk(filepath): # create a list of file names
    f.extend(filenames)
    break

print(f)

sample = len(f)

df = pd.DataFrame()

token_counts = []
#for file in random.choices(f,k=sample): # for each file in the list of file names, do some stuff

for file in f:
    tokens_used = 0

    column_names = ["file"]
    column_values = [file]

    fileloc = filepath+file
    text = read_pdf(fileloc)
    #print("text here: ", text)
    words = len(text.split())

    #print(words)

    #print("Parsing ~{} words ({} tokens) from: \"{}\"\n".format(words,len(encoding.encode(text)),fileloc))
#TB: for now let's just focus on getting the case numbers out with regex
    try:
      # ---------------------------------------------------------
      # case Number
      # ---------------------------------------------------------
      #case_no = re.search("^Case No\W+\w{3}\d{7}",text).groups(0)[0].strip()
      #case_no = re.search("^Case No\W+\w{3}\d{7}",text)
      case_no = re.search("Case\s*No.*\s*\w*\d{7,}",text, flags=re.IGNORECASE).group(0)
      #case_no = re.match("Case\s*No.\s*\w*\d{7}",text, flags=re.IGNORECASE).group(0)
      column_names.append("case_no")
      column_values.append(case_no)
    except:
      column_names.append("case_no")
      column_values.append("NA")

    df = pd.concat([df,pd.DataFrame([column_values],columns=column_names)], ignore_index=True,sort=False)


#current issue with regex search: it's successfully pulling case number, but only the last
    # current theory is that I'm overwriting matches as I go
    
#df = pd.concat([df,pd.DataFrame([column_values],columns=column_names)], ignore_index=True,sort=False)

os.getcwd()
display(df)