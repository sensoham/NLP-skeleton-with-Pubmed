import os
print "Starting script 1, Processing data from Pubmed...."
os.system("Querrying_biopython_api_NLP.py")
print("Script 1 ended")
print "Starting script 2, Preprocessing..."
os.system("case_cleaning.py")
print("Script 2 ended")
print "Starting script 3, Preprocessing...."
os.system("case_cleaning_cat.py")
print("Script 3 ended")
print "Starting script 4, Preprocessing...."
os.system("Patterns_in_frequency.py")
print("Script 4 ended")
print "Starting script 5, Preprocessing... Almost done!"
os.system("Patterns_in_frequency_cat.py")
print("Script 5 ended")
print "Starting script 6, Assigning values to words..."
os.system("norm_scoring.py")
print("Script 6 ended")
print "Starting script 7, Plotting of NLP terms..."
os.system("adjusted_text.py")
print("Script 7 ended")
print "Starting script 8, Finding Co-occurences..."
os.system("Coocurrence_mat.py")
print("Script 8 ended")
print "Starting script 9, Creating Heatmap..."
os.system("heat_map_cooccur.py")
print("Script 9 ended")
print "Running Dictionary Scripts"
print "Starting script 10, Finding dictionary terms..."
os.system("flashtext_wordfind_pubmed.py")
print("Script 10 ended")
print "Starting script 11, Plotting of Dictionary terms..."
os.system("dict_plot.py")
print("Script 11 ended")
