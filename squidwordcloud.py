import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

# read text
with open("text.csv", encoding="utf8", errors='ignore') as f:
    data = pd.read_csv(f)

text = " ".join(text for text in data.text)
text = text.upper()
stopwords = set(STOPWORDS)
stopwords.update(["HTTPS", "AMP"])

mask = np.array(Image.open("Squid-Game.png"))

def transform_format(val):
     if sum(val)>1:
         return 1
     else:
         return 255

# Transform your mask into a new one that will work with the function:
transformed_mask = np.ndarray((mask.shape[0],mask.shape[1]), np.int32)

for i in range(len(mask)):
    transformed_mask[i] = list(map(transform_format, mask[i]))

# print(transformed_mask)

# Create a word cloud image
wc = WordCloud(max_words=5000, 
               stopwords=stopwords, 
               font_path="COUR.ttf",
               prefer_horizontal=.7,
               min_font_size=5,
               max_font_size=70,
               background_color="white", 
               width=7680,
               height=4320,
               margin=2,
               collocations=False,
               mask=transformed_mask,            
               repeat=False,
               relative_scaling=0,
               scale=1,
               min_word_length=3,
               include_numbers=False,
               normalize_plurals = True,
               font_step=1
               )

# Generate a wordcloud
wc.generate(text)

# create coloring from image
image_colors = ImageColorGenerator(mask)
wc = wc.recolor(color_func=image_colors)

# Write wordcloud into data frame
df = pd.DataFrame(wc.layout_, columns = ['Name', "Size", "Coord", "Direction", "Color"])

# Convert rgb code to hexadecimal code
import re

def rgb2hex(rgb):
    r = int(re.search('\((.+?)\,', rgb).group(1))
    g = int(re.search('\,(.+?)\,', rgb).group(1))
    b = int(re.search('\,.*\,(.+?)\)', rgb).group(1))
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

for i in range(len(df)):
    df.Color[i] = "<color>"+rgb2hex(df.Color[i])+"</color>"

df.to_csv("wordcloud.csv")

# show
plt.figure(figsize=[20,10])
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()