# Libraries used
import pandas as pd
import numpy as np
import bar_chart_race as bcr
import nltk
import warnings

warnings.filterwarnings("ignore")

# Reading of book by lines and storing to string file_text
with open("Book 5 - The Order of the Phoenix.txt", "r", encoding='utf-8') as file:
    file_text = file.read()

# Replacing of name of book from headings of pages
file_text = file_text.replace("Harry Potter and the Order of the Phoenix -J.K. Rowling", "")
file_text = file_text.replace("Harry Potter and the Order of the Phoenix - J.K. Rowling", "")

# Formatting of text to lower case
file_text = file_text.lower()

# Removing of punctuation and special characters
file_text = re.sub(r"- |-\n", "-", file_text)

file_text = re.sub(r"\n,\?\.;:s!", "", file_text)

# Removing of numbers
file_text = re.sub(r"\d+", "", file_text)

# Splitting of text by pages and storing data to list
file_list = file_text.split("page |")

# Splitting of pages to lists of words
lists_by_page = [i.split() for i in file_list]

# Removing of stopwords
common_words = nltk.corpus.stopwords.words('english') + ['dont', 'hadnt', 'didnt', 'youre']
for stopword in common_words:
    for i in range(len(lists_by_page)):
        for j in range(len(lists_by_page[i])):
            if stopword == lists_by_page[i][j]:
                lists_by_page[i][j] = np.nan


# Counting of accumulated frequency for top words after every page and storing to list result
result = []
accumulated_list = []
for list_by_page in lists_by_page:
    accumulated_list = accumulated_list + list_by_page
    result.append(pd.Series(accumulated_list).value_counts()[0:20])

# Converting of list with result to pandas dataframe
final_dataframe = pd.DataFrame(columns = ['Word', 'Frequency', 'Page'])
for i in range(len(result)):
    page_dataframe = pd.DataFrame({"Frequency":result[i]})
    page_dataframe["Word"] = page_dataframe.index
    page_dataframe = page_dataframe.reset_index(drop=True)
    page_dataframe["Page"] = i + 1
    final_dataframe = pd.concat([final_dataframe,page_dataframe])

# Formatting of column with frequency
final_dataframe['Frequency'] = final_dataframe['Frequency'].astype('int64')

# Preparing of dataset for plotting
final_pivot = pd.pivot_table(final_dataframe, values='Frequency', columns=['Word'], index=['Page'], aggfunc=np.sum)
final = pd.DataFrame(final_pivot.to_records())
final = final.drop(columns='Page')
my_index = []
for i in range(len(final)):
    my_index.append("Pages read: " + str(i + 1))
final["Page"] = my_index
final = final.set_index('Page')
final = final.fillna(0)


# Bar chart race
bcr.bar_chart_race(df = final, filename='video.mp4', n_bars=20, title = "Accumulated frequency of top words in Harry Potter and the Order of the Phoenix", title_size = 9)
