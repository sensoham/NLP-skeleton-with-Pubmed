import pandas as pd
from Bio import Entrez
import unicodecsv as csv
from flashtext import KeywordProcessor
from Querrying_biopython_api_NLP import term as main_term

df = pd.read_csv('Dictionary.txt', delimiter = '\t', header = 'infer')

term_dict = dict(zip(df['TERM'],df['Category']))
trm = main_term
filename = '\Dict_match_titplusabs_flashtext.csv'   #name of o/p file


def search(query):
    Entrez.email = 'soham12ka4@gmail.com'
    handle = Entrez.esearch(db='pubmed', sort='relevance', retmax='5', retmode='xml', term=query)
    results = Entrez.read(handle)
    return results


def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'your.email@gmail.com'
    handle = Entrez.efetch(db='pubmed', retmode='xml', id=ids)
    results = Entrez.read(handle)
    return results




def dict_creator(trm,dict_choice):
    dict_title = {}
    dict_abstract = {}
    dict_date1 = {}
    dict_date2 = {}
    results = search(trm)
    id_list = results['IdList']
    papers = fetch_details(id_list)
    titles = []
    months = []
    years = []
    pmid_list = []
    abstracts = []
    for paper in papers['PubmedArticle']:
        pmid = paper['MedlineCitation']['PMID']
        pmid_list.append(pmid)
        title = paper['MedlineCitation']['Article']['ArticleTitle']
        dict_title[pmid] = title
        titles.append(title)
        abstract = ''
        if len(paper['MedlineCitation']['Article']['ArticleDate']) == 0:
            month = 'No Date'
            year = 'No Date'
            months.append(month)
            years.append(year)
        else:
            for item in paper['MedlineCitation']['Article']['ArticleDate']:
                month = item['Month']
                year = item['Year']
                months.append(month)
                years.append(year)
        for text in paper['MedlineCitation']['Article']['Abstract']['AbstractText']:
            abstract = abstract +'\t'+ text
        abstracts.append(abstract)

    dict_title = dict(zip(pmid_list, titles))
    dict_abstract = dict(zip(pmid_list, abstracts))
    dict_date1 = dict(zip(pmid_list, months))
    dict_date2 = dict(zip(pmid_list, years))
    if dict_choice == 0:
        return dict_title
    elif dict_choice == 2:
        return dict_date1
    elif dict_choice == 3:
        return dict_date2
    else:
        return dict_abstract






def savetocsv(lista, filename):
    with open(filename, 'wb') as csv_file:
        writer = csv.writer(csv_file, encoding = 'utf-8')
        for val in lista:
            val1 =  [v for v in val]
            writer.writerow(val)

    


def main():
    print_list = []
    dictA = dict_creator(trm, 0)
    dictB = dict_creator(trm, 1)
    dictC = dict_creator(trm, 2)
    dictD = dict_creator(trm, 3)
    keyword_processor = KeywordProcessor()
    keyword_processor.add_keywords_from_list(list(df['TERM']))
    for key in dictA.keys():
        total_text = dictA[key] + '\n' + dictB[key]
        key_words = keyword_processor.extract_keywords(total_text)
        if len(key_words)>0:
            for term in set(key_words):
                list_temp = [term, term_dict[term], key_words.count(term),key, dictC[key], dictD[key]]
                print_list.append(list_temp)
    savetocsv(print_list, filename)
main()
