# Importing modules
import pandas as pd

# Reading in dataset (edges)
book1 = 'datasets/book1.csv'
book2 = 'datasets/book2.csv'
book3 = 'datasets/book3.csv'
book4 = 'datasets/book4.csv'
book5 = 'datasets/book5.csv'
headers = ['Source','Target','Type','weight','book']
book1_frame = pd.read_csv(book1) 

# Printing out the head of the dataset
book1_frame.head()

# Importing modules
import networkx as nx
import nxviz as nv
import matplotlib.pyplot as plt

# Creating an empty graph object
G_book1 = nx.Graph()

# Iteration through the DataFrame for book 1 to add edges
bk1 = [G_book1]
for _, edge in book1_frame.iterrows():
        G_book1.add_edge(edge['Source'], edge['Target'], weight=edge['weight'])
bk1.append(G_book1)

# Creating a list of networks for all the books
books = [G_book1]
book_fnames = [book2, book3,book4, book5]
for book_fname in book_fnames:
    book = pd.read_csv(book_fname)
    G_book = nx.Graph()
    for _, edge in book.iterrows():
        G_book.add_edge(edge['Source'], edge['Target'], weight=edge['weight'])
    books.append(G_book)

ap = nv.ArcPlot(G_book1)
ap.draw()
plt.show()

#FINDING MOST IMPORTANT CHARACTER    
# Calculating the degree centrality of book 1
deg_cen_book1 = nx.degree_centrality(books[0])

# Calculating the degree centrality of book 5
deg_cen_book5 = nx.degree_centrality(books[4]) 

# Sorting the dictionaries according to their degree centrality and storing the top 10
sorted_deg_cen_book1 = sorted(deg_cen_book1.items(), key=lambda x:x[1], reverse=True)[0:10]
# Sorting the dictionaries according to their degree centrality and storing the top 10
sorted_deg_cen_book5 = sorted(deg_cen_book5.items(), key=lambda x:x[1], reverse=True)[0:10]

# Printing out the top 10 of book1 and book5
print(sorted_deg_cen_book1)
print(sorted_deg_cen_book5)

# Create a list of degree centrality of all the books
evol = [nx.degree_centrality(book) for book in books]
 
# Creating a DataFrame from the list of degree centralities in all the books
degree_evol_df = pd.DataFrame.from_records(evol)
#print(degree_evol_df)
# Plotting the degree centrality evolution of Eddard-Stark, Tyrion-Lannister and Jon-Snow
degree_evol_df[['Eddard-Stark', 'Tyrion-Lannister', 'Jon-Snow']].plot()

# Creating a list of betweenness centrality of all the books just like we did for degree centrality
evol = [nx.betweenness_centrality(book, weight = 'weight') for book in books]

# Making a DataFrame from the list, replacing NaN values with 0
betweenness_evol_df = pd.DataFrame.from_records(evol).fillna(0)

# Finding the top 4 characters in every book
set_of_char = set()
for i in range(5):
    set_of_char |= set(list(betweenness_evol_df.T[i].sort_values(ascending=False)[0:4].index))
list_of_char = list(set_of_char)

# Plotting the evolution of the top characters
betweenness_evol_df[list_of_char].plot(figsize=(13, 7))

# Creating a list of pagerank of all the characters in all the books
evol = [nx.pagerank(book, weight = 'weight') for book in books]

# Making a DataFrame from the list
pagerank_evol_df = pd.DataFrame.from_records(evol)

# Finding the top 4 characters in every book
set_of_char = set()
for i in range(5):
    set_of_char |= set(list(pagerank_evol_df.T[i].sort_values(ascending=False)[0:4].index))
list_of_char = list(set_of_char)

# Plotting the top characters
pagerank_evol_df[list_of_char].plot(figsize=(13, 7))

# Creating a list of pagerank, betweenness centrality, degree centrality
# of all the characters in the fifth book.
measures = [nx.pagerank(books[4]), 
            nx.betweenness_centrality(books[4], weight='weight'), 
            nx.degree_centrality(books[4])]

# Creating the correlation DataFrame
cor = pd.DataFrame.from_records(measures)
cor_T = cor.transpose()
# Calculating the correlation
cor_T.corr()

# Finding the most important character in the fifth book,  
# according to degree centrality, betweenness centrality and pagerank.
p_rank, b_cent, d_cent = cor.idxmax(axis=1)

# Printing out the top character accoding to the three measures
print(p_rank,b_cent,d_cent)

#bk = books
#bk = nx.barbell_graph(m1=5,m2=1)
#nx.find_cliques(bk) ; plt.show()

G = nx.erdos_renyi_graph(n = 20, p=0.2)
len(G)
len(G.edges())
len(G.nodes())
circ = nv.CircosPlot(G, node_color = 'key', node_group = 'key')
circ.draw()
#bk.nodes()
#nodes = bk.neighbors(8) 
#G_eight = bk.subgraph(nodes)
#nx.draw(G_eight, with_labels=True)
#plt.savefig("GOT_Network")
#plt.show()

