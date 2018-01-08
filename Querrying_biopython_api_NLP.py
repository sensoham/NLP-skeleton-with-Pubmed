from Bio import Entrez
import nltk
import unicodecsv as csv

term = 'Flu'                #Test by changing this value
filename1 = 'Term_categories_complete.csv'
filename2 = 'Term_details_complete.csv'

def search(query):
    Entrez.email = 'soham12ka4@gmail.com'
    handle = Entrez.esearch(db='pubmed', sort='relevance', retmax='20', retmode='xml', term=query)
    results = Entrez.read(handle)
    return results


def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'your.email@gmail.com'
    handle = Entrez.efetch(db='pubmed', retmode='xml', id=ids)
    results = Entrez.read(handle)
    return results




def dict_creator(term,dict_choice):
    dict_title = {}
    dict_abstract = {}
    dict_date1 = {}
    dict_date2 = {}
    results = search(term)
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






def savetocsv1(lista, filename):
    with open(filename, 'wb') as csv_file:
        writer = csv.writer(csv_file, encoding = 'utf-8')
        for val in lista:
            val1 =  [v for v in val]
            writer.writerow(val)

def process_content(tokenized):    
    list_nouns = []
    try:
        for i in tokenized:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            chunkGram = r'''Chunk: {<NN.?>*}'''
            chunkParser = nltk.RegexpParser(chunkGram)
            chunked = chunkParser.parse(tagged)
            all_chnks = chunk_joining(chunked)
            list_nouns.append(all_chnks)
        return list_nouns

    except Exception as e:
        return str(e)


def chunk_joining(chunked):
    list_chunks = []
    nodelist = ['NN','NNP', 'NNS']
    for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Chunk'):
        list_chunks.append(" ".join([a for (a,b) in subtree.leaves()]))
    return list_chunks


def tokenizing_parsedfile(article_dict):
    token_dict = {}
    for key, val in article_dict.items():
        sent = article_dict[key]
        sent_token = nltk.sent_tokenize(sent)
        sent_noun_chunked = process_content(sent_token)
        token_dict[key] = sent_noun_chunked
    return token_dict

def concat_lists(dict1, dict2, key):
    concat_list = []
    for list_terms in dict1[key]:
        for terms in list_terms:
            concat_list.append(terms)
    for list_terms in dict2[key]:
        for terms in list_terms:
            concat_list.append(terms)
    return concat_list       

def term_count(dict1, dict2, key, termlist):
    term_det = []
    title = dict1[key]
    abstract = dict2[key]
    for term in termlist:
        term_count = 0
        term_count_tit1 = 0
        term_count_tit2 = 0
        term_count_abs1 = 0
        term_count_abs2 = 0
        stemmer = nltk.stem.SnowballStemmer("english")
        stem_term = stemmer.stem(term)
        if term.lower() in title.lower():
            term_count_tit1 = title.lower().count(term.lower())
        elif stem_term.lower() in title.lower():
            term_count_tit2 = title.lower().count(stem_term.lower())
        if term.lower() in abstract.lower():  
            term_count_abs1 = abstract.lower().count(term.lower())
        elif stem_term.lower() in abstract.lower():
            term_count_abs2 = abstract.lower().count(stem_term.lower())

        total_count = term_count_tit1 + term_count_tit2 + term_count_abs1 + term_count_abs2
        term_det.append([term, total_count, key])
    return term_det

def count_category(term_det):
    term_cat = []
    for item in term_det:
        if item[1] == 0:
            rel = 'IRRELEVANT'
        elif item[1] < 3:
            rel = 'LOW FREQUENCY'
        elif item[1] > 2 and item[1] < 7:
            rel = 'MEDIUM FREQUENCY'
        else:
            rel = 'HIGH FREQUENCY'

        term_cat.append([item[0], rel, item[2]])
    return term_cat

def Smoother_main():
    print_list1 = []
    print_list2 = []
    print_list3 = []
    abs_dict = dict_creator(term, 1)
    tit_dict = dict_creator(term, 0)
    date_dict = dict_creator(term, 2)
    month_dict = dict_creator(term, 3)

    for key in tit_dict.keys():
        final_list1 = concat_lists(tokenizing_parsedfile(tit_dict), tokenizing_parsedfile(abs_dict), key)
        fl_set = set(final_list1)
        final_list = list(fl_set)
        term_det = term_count(tit_dict, abs_dict, key, final_list)
        term_category = count_category(term_det)
        for item in term_category:

            if key in date_dict.keys():      #parsing has rendered this condition sort of redundant
                item.append(date_dict[key])
                item.append(month_dict[key])
                print_list1.append(item)

            else:
                item.append('No Date')
                print_list1.append(item)


        for item2 in term_det:
            if key in date_dict.keys():
                item2.append(date_dict[key])
                item2.append(month_dict[key])
                print_list3.append(item2)
            else:
                item2.append('No Date')
                print_list3.append(item2)

    savetocsv1(print_list1, filename1)
    savetocsv1(print_list3, filename2)

Smoother_main()            
