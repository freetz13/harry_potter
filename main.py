# Libraries used
import pandas as pd
import numpy as np
import bar_chart_race as bcr
import nltk
import warnings

warnings.filterwarnings("ignore")

# Reading of book by lines and storing to list file_rows
with open("Book 5 - The Order of the Phoenix.txt", "r", encoding='utf-8') as file:
    file_rows = file.readlines()

# Creation of a string with text of book
file_text = "".join(file_rows)

# Replacing of name of book from headings of pages
file_text = file_text.replace("Harry Potter and the Order of the Phoenix -J.K. Rowling", "")
file_text = file_text.replace("Harry Potter and the Order of the Phoenix - J.K. Rowling", "")

# Formatting of text to lower case
file_text = file_text.lower()

# Removing of punctuation and special characters
for i in ["- ", "-\n"]:
    file_text = file_text.replace(i, "-")

for i in ["\n", ",", "?", ".", '', '', ';', ':', 's', '', "!"]:
    file_text = file_text.replace(i, "")

# Removing of numbers
for i in ["1", "2", "3", "4", '5', '6', '7', '8', '9', '0']:
    file_text = file_text.replace(i, "")

# Splitting of text by pages and storing data to list
file_text = file_text.replace('page |', "@")
file_list = file_text.split("@")

# Splitting of pages to lists of words
lists_by_page = []
for i in file_list:
    lists_by_page.append(i.split())

# Removing of stopwords
common_words = nltk.corpus.stopwords.words('english') + ['dont', 'hadnt', 'didnt', 'youre']
for i in common_words:
    for j in range(0, len(lists_by_page)):
        for k in range(0, len(lists_by_page[j])):
            if i == lists_by_page[j][k]:
                lists_by_page[j][k] = np.nan


# Counting of accumulated frequency for top words after every page and storing to list result
result = []
accumulated_list = []
for i in range(0, len(lists_by_page)):
    accumulated_list = accumulated_list + lists_by_page[i]
    result.append(pd.Series(accumulated_list).value_counts()[0:20])

# Converting of list with result to pandas dataframe
final_dataframe = pd.DataFrame(columns = ['Word', 'Frequency', 'Page'])
for i in range(0, len(result)):
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
for i in range(0, len(final)):
    my_index.append("Pages read: " + str(i + 1))
final["Page"] = my_index
final = final.set_index('Page')
final = final.fillna(0)


# Bar chart race
bcr.bar_chart_race(df = final, filename='video.mp4', n_bars=20, title = "Accumulated frequency of top words in Harry Potter and the Order of the Phoenix", title_size = 9)
