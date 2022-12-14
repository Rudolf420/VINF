# Import the required modules
import json
import lucene
from java.nio.file import Paths
from java.io import File
from org.apache.lucene.store import NIOFSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader, IndexReader
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.document import Document, Field, StringField, TextField, StoredField, FieldType
from org.apache.lucene.queryparser.classic import MultiFieldQueryParser
from org.apache.lucene.search import IndexSearcher
from deep_translator import GoogleTranslator


#function called indexData() that is used to index some data stored in a JSON file called data.json.
#The function uses the PyLucene library to create an index for the data and store it in a
#directory called index. The function loops through each item in the JSON data, and creates a document
#for each item containing several fields (title, text, username, ip). The fields are added to the document,
#and the document is then added to the index. Finally, the index is closed.

def menu(x):
    if x == '1':
            indexData()
            print("data boli zindexované")

    elif x == '2':
        print("Zadajte hladané slovo:")
        searcher_word = input()
        search(searcher_word)

    elif x == '3':
        test_indexData()

    elif x == '4':
        test_search()

    else:
            return 0
def indexData():
    with open('data.json') as user_file:
      json_data = json.load(user_file)

    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    # Create the PyLucene index
    index_dir = "index"
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    writer = IndexWriter(NIOFSDirectory(Paths.get(index_dir)), config)

    # Loop through the JSON data and add each item to the index
    for key, value in json_data.items():
        doc = Document()


        # Add the fields to the document
        ip = value['ip'] if value['ip'] is not None else ''
        username = value['username'] if value['username'] is not None else ''
        text = value['text'] if value['text'] is not None else ''

        doc.add(Field('title', key, TextField.TYPE_STORED))
        doc.add(Field('text', text, TextField.TYPE_STORED))
        doc.add(Field('username', username, TextField.TYPE_STORED))
        doc.add(Field('ip', ip, TextField.TYPE_STORED))

        # Add the document to the index
        writer.addDocument(doc)

    # Close the index
    writer.commit()
    writer.close()

#function called search() that is used to search an index created by the indexData() function.
#The function takes an input string (called input) and uses the PyLucene library to search the index
#for documents that match the input string. The function creates a MultiFieldQueryParser that searches
#multiple fields in the index (title, text, username) and uses the StandardAnalyzer to analyze the input string.
#The function then searches the index using the IndexSearcher object, and prints the fields of the matching documents.

def search(input):
    lucene.initVM()
    # create an IndexSearcher for the index
    index = NIOFSDirectory.open(Paths.get("index"))
    reader = DirectoryReader.open(NIOFSDirectory.open(Paths.get("index")))
    searcher = IndexSearcher(reader)
    analyzer = StandardAnalyzer()

    # create a list of fields to search
    fields = ["title", "text", "username"]
    # parse the query string and search the index

    translated_words = translation(input)

    query = MultiFieldQueryParser.parse(MultiFieldQueryParser(fields, analyzer), input)
    results = searcher.search(query, 10)

    # loop over the results and print the fields for each matching document
    for score in results.scoreDocs:
        doc = searcher.doc(score.doc)
        print("Field 1: " + doc.get("title"))
        print("Field 2: " + doc.get("text"))
        print("Field 3: " + doc.get("username"))

def translation(input):
    translatedEs = GoogleTranslator(source='sk', target='es').translate(text=input)
    translatedEn = GoogleTranslator(source='sk', target='en').translate(text=input)
    print("Spanish: " + translatedEs)
    print("English: " + translatedEn)

    return [input, translatedEn, translatedEs]

def test_indexData(self):
     # Test that indexData() creates an index with the correct number of documents
    indexData()
    index_dir = "index"
    reader = DirectoryReader.open(NIOFSDirectory.open(Paths.get(index_dir)))
    self.assertEqual(reader.numDocs(), len(json_data))
    reader.close()

def test_search(self):
      # Test that search() returns the correct number of documents
    indexData()
    results = search('hello')
    self.assertEqual(len(results), 2)

print("Choose option:\n"
          "1 - indexuj data\n"
          "2 - hladaj v dátach\n"
      "3 - otestuj indexx\n"
      "4 - otestuj search\n")
x = input()
menu(x)



