from search import keyword_to_titles, title_to_info, search, article_length,key_by_author, filter_to_author, filter_out, articles_from_year
from search_tests_helper import get_print, print_basic, print_advanced, print_advanced_option
from wiki import article_metadata
from unittest.mock import patch
from unittest import TestCase, main

class TestSearch(TestCase):

    ##############
    # UNIT TESTS #
    ##############

    def test_example_unit_test(self):
        dummy_keyword_dict = {
            'cat': ['title1', 'title2', 'title3'],
            'dog': ['title3', 'title4']
        }
        expected_search_results = ['title3', 'title4']
        self.assertEqual(search('dog', dummy_keyword_dict), expected_search_results)


    def test_keyword_to_title(self):
        metadata1 = [
            ["Title 1", "Author 1", 123456789, 500, ["keyword1"]],
            ["Title 2", "Author 2", 123456788, 600, ["keyword2"]]  
        ]
        expected_metadata1 ={
            "keyword1": ["Title 1"],
            "keyword2": ["Title 2"]
        }

        # Check for multiple keyword and case sensitivity
        metadata2 = [
            ["Title 1", "Author 1", 123456789, 500, ["keyword1"]],
            ["Title 2", "Author 2", 123456788, 600, ["keyword2", "keyword3"]],
            ["Title 3", "Author 3", 123456787, 700,["keyword3", "keyword4", "keyword5"]],
            ["Title 4", "Author 4", 123456786, 700, ["KeYword4"]]

        ]
        expected_metadata2 = {
            "keyword1":["Title 1"],
            "keyword2":["Title 2"],
            "keyword3":["Title 2", "Title 3"],
            "keyword4":["Title 3"],
            "keyword5":["Title 3"],
            "KeYword4":["Title 4"],
        }
        # Check for article without relevant keywords
        metadata3 = [
            ["Title 1", "Author 1", 123456789, 500, []],
            ["Title 2", "Author 2", 123456788, 600, ["keyword2"]]
        ]
        expected_metadata3 = {
            "keyword2": ["Title 2"]
        }
        self.assertEqual(keyword_to_titles(metadata1), expected_metadata1)
        self.assertEqual(keyword_to_titles(metadata2), expected_metadata2)
        self.assertEqual(keyword_to_titles(metadata3), expected_metadata3)


    def test_title_to_info(self):
            metadata1 =[
                ["Title 1", "Author 1", 123456789, 500, ["keyword1"]],
                ["Title 2", "Author 2", 123456788, 600, ["keyword2"]]
            ]
            expected_metadata1 ={
                "Title 1":{"author": "Author 1", "timestamp": 123456789, "length":500},
                "Title 2": { "author":"Author 2", "timestamp": 123456788, "length":600}
            }
            metadata2 =[
                ["Title 1", "Author 1", 123456789, 500, ["keyword1"]],
                ["Title 2", "Author 2", 123456788, 600, ["keyword2", "keyword3"]],
                ["Title 3", "Author 3", 123456787, 700, ["keyword3", "keyword4", "keyword5"]],
                ["Title 4", "Author 4", 123456786, 700, ["KeYword4"]]

            ]

            expected_metadata2 ={
                "Title 1":{"author":"Author 1", "timestamp": 123456789, "length": 500},
                "Title 2":{"author":"Author 2", "timestamp": 123456788, "length": 600},
                "Title 3":{"author":"Author 3", "timestamp": 123456787, "length": 700},
                "Title 4":{"author":"Author 4", "timestamp": 123456786, "length": 700},

            }

            self.assertEqual(title_to_info(metadata1), expected_metadata1)
            self.assertEqual(title_to_info(metadata2), expected_metadata2)
            # Test for empty metadata
            self.assertEqual(title_to_info([]),{})

    def test_search(self):
        keyword_to_titles = {
            "keyword1":["Title 1", "Title 2"],
            "keyword2":["Title 2", "Title 3"],
            "keyword3":["Title 3", "Title 4"]

        }
        # Test for present keyword
        self.assertEqual(search("keyword1",keyword_to_titles),["Title 1","Title 2"])
       
        # Test for absent keyword
        self.assertEqual(search("nonExistingKeyword",keyword_to_titles),[])
       
        #Test  empty dicitonary mapping to list of all articles
        self.assertEqual(search("anyKeyword",{}),[])
   

    def test_article_length(self):
        title_to_info ={
            "Title 1":{"author":"Author 1","timestamp":1234567890, "length":800},
            "Title 2":{"author":"Author 2","timestamp":1234567891, "length":900},
            "Title 3":{"author":"Author 3","timestamp":1234567892, "length":700},

        }
        article_titles1 = ["Title 1","Title 2","Title 3"]
        # Test for all articles within the max length limit
        self.assertEqual(article_length(1000,article_titles1,title_to_info),["Title 1","Title 2","Title 3"])
       
        #Test for all articles beyond the max limit
        self.assertEqual(article_length(100,article_titles1,title_to_info),[])
       
        # Test for some article within the reach
        self.assertEqual(article_length(850,article_titles1,title_to_info),["Title 1","Title 3"])
       
        # Test for empty article title
        self.assertEqual(article_length(100,[],title_to_info),[])
       
        # Test for empty dictionary
        self.assertEqual(article_length(1000,article_titles1,{}),[])

    def test_key_by_author(self):
        article_titles_1 =["Title 1","Title 2","Title 3","Title 4"]
        title_to_info = {
            "Title 1":{"author":"Author 1","timestamp":1234567890,"length":80},
            "Title 2":{"author":"Author 2","timestamp":1234567891,"length":90},
            "Title 3":{"author":"Author 3","timestamp":1234567892,"length":70},
            "Title 4":{"author":"Author 3","timestamp":1234567892,"length":70},

        }
        expected_1 = {
            "Author 1":["Title 1"],
            "Author 2":["Title 2"],
            "Author 3":["Title 3","Title 4"]
        }
        # Test for articles with differnt and same authors
        self.assertEqual(key_by_author(article_titles_1,title_to_info),expected_1)
       
        # Test for empty article title
        self.assertEqual(key_by_author([],title_to_info),{})
       
        # Test for empty title key to title or absence of requested title
        self.assertEqual(key_by_author(article_titles_1,{}),{})



    def test_filter_to_author(self):
        article_titles_1 = ["Title 1","Title 2","Title 3","Title 4"]
        title_to_info ={
           "Title 1":{"author":"Author 1","timestamp": 1234567890, "length":80},
           "Title 2":{"author":"Author 2","timestamp": 1234567891, "length":90},
           "Title 3":{"author":"Author 3","timestamp": 1234567892, "length":70},
           "Title 4":{"author":"Author 3","timestamp": 1234567892, "length":70},
        }
        self.assertEqual(filter_to_author("Author 1",article_titles_1,title_to_info),["Title 1"])
        self.assertEqual(filter_to_author("Non exsistent",article_titles_1,title_to_info),[])
        self.assertEqual(filter_to_author("Anything",[],title_to_info),[])
        self.assertEqual(filter_to_author("Anything",article_titles_1,{}),[])



    def test_filter_out(self):
        keyword_to_titles= {
            "keyword1":["Title 1","Title 2"],
            "keyword2":["Title 2"],
            "keyword3":["Title 2","Title 3"],
            "keyword4":["Title 3"],
            "keyword5":["Title 3","Title 4"],
            "keyword4":["Title 4"]

        }
        article_titles_1 = ["Title 1", "Title 2","Title 3", "Title 4"]
        expected_1 = ["Title 1","Title 3", "Title 4"]


        self.assertEqual(filter_out("keyword2",article_titles_1,keyword_to_titles),expected_1)

        # Test for empty title
        self.assertEqual(filter_out("keyword2",[],keyword_to_titles),[])

        #Test for empty keyword to titles
        self.assertEqual(filter_out("keyword2",article_titles_1,{}),article_titles_1)



    def test_articles_from_year(self):
        title_to_info ={
            # For year 2022
            "Title 1":{"author":"Author 1","timestamp":1668690000, "length":800},

            # For year 2021
            "Title 2":{"author":"Author 2","timestamp":1637154000, "length":900},

            # For year 2020
            "Title 3":{"author":"Author 3","timestamp":1605618000, "length":700},
            "Title 4":{"author":"Author 4","timestamp":1605618000, "length":700}

        }
        article_titles =["Title 1","Title 2","Title 3","Title 4"]

        # Test for single article from a given  year
        self.assertEqual(articles_from_year(2021, article_titles, title_to_info),["Title 2"])

        #Test for multiple articles form a given year.
        self.assertEqual(articles_from_year(2020, article_titles, title_to_info),["Title 3","Title 4"])

        # Test for no article from a given year.
        self.assertEqual(articles_from_year(2000, article_titles, title_to_info),[])

        # Test for empty article title.
        self.assertEqual(articles_from_year(2001, [], title_to_info),[])

        #Test for empty title to info or absence of requested title in a dictionary.
        self.assertEqual(articles_from_year(2002, article_titles, {}),[])

       
    #####################
    # INTEGRATION TESTS #
    #####################

    @patch('builtins.input')
    def test_example_integration_test(self, input_mock):
        keyword = 'soccer'
        advanced_option = 5
        advanced_response = 2009

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Spain national beach soccer team', 'Steven Cohen (soccer)']\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_basic_search_integration_test(self, input_mock):
        keyword = 'canada'
        advanced_option = 6

        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option)  + "\n\nHere are your articles: ['List of Canadian musicians', 'Lights (musician)', 'Old-time music', 'Will Johnson (soccer)']\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_article_length_integration_test(self, input_mock):
        keyword = 'list'
        advanced_option = 1
        advanced_response = 10000

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['List of gospel musicians', 'Covariance and contravariance (computer science)']\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_key_by_author_integration_test(self, input_mock):
        keyword = 'france'
        advanced_option = 2

        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + "\n\nHere are your articles: {'Mack Johnson': ['French pop music']}\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_filter_to_author_integration_test(self, input_mock):
        keyword = 'kasai'
        advanced_option = 3
        advanced_response = 'jack johnson'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Edogawa, Tokyo']\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_filter_out_integration_test(self, input_mock):
        keyword = 'high'
        advanced_option = 4
        advanced_response = 'this'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Edogawa, Tokyo']\n"

        self.assertEqual(output, expected)

# Write tests above this line. Do not remove.
if __name__ == "__main__":
    main()