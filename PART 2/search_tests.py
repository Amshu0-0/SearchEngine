from search import search, article_length, unique_authors, most_recent_article, favorite_author, title_and_author, refine_search, display_result
from search_tests_helper import get_print, print_basic, print_advanced, print_advanced_option
from wiki import article_metadata
from unittest.mock import patch
from unittest import TestCase, main

class TestSearch(TestCase):

    ##############
    # UNIT TESTS #
    ##############

    def test_example_unit_test(self):
        expected_search_soccer_results = [
            ['Spain national beach soccer team', 'jack johnson', 1233458894, 1526],
            ['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562],
            ['Steven Cohen (soccer)', 'Mack Johnson', 1237669593, 2117]
        ]
        self.assertEqual(search('soccer'), expected_search_soccer_results)

    def test_search(self):
        expected_search_canada_results = [
            ['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023],
            ['Lights (musician)', 'Burna Boy', 1213914297, 5898],
            ['Old-time music', 'Nihonjoe', 1124771619, 12755],
            ['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562]
        ]

        expected_search_koiwa_results = [
            ['Edogawa, Tokyo', 'jack johnson', 1222607041, 4526]
        ]

        self.assertEqual(search('CaNADA'), expected_search_canada_results)
        self.assertEqual(search('koiwa'), expected_search_koiwa_results)
        self.assertEqual(search(''), [])

    def test_article_length(self):
        metadata = [
            ['Article 1', 'Author 1', 1234567890, 500],
            ['Article 2', 'Author 2', 1234567891, 1000],
            ['Article 3', 'Author 3', 1234567892, 1500],
            ['Article 4', 'Author 4', 1234567893, 2000],
        ]

        expected_max_1000_result = [
            ['Article 1', 'Author 1', 1234567890, 500],
            ['Article 2', 'Author 2', 1234567891, 1000]
        ]

        expected_max_10_result = []
        empty_metadata = []
        expected_max_1_for_empty_result = []

        self.assertEqual (article_length(1000, metadata), expected_max_1000_result)
        self.assertEqual (article_length(10, metadata), expected_max_10_result)
        self.assertEqual (article_length(1, empty_metadata), expected_max_1_for_empty_result)

    def test_unique_authors(self):
        metadata = [
            ['Article 1', 'Author 1', 1234567890, 500],
            ['Article 2', 'author 1', 1234567891, 1000],
            ['Article 3', 'Author 3', 1234567892, 1500],
            ['Article 4', 'Author 4', 1234567893, 2000],
            ['Article 9', 'Author 9', 1234567899, 2023],
            ['Article 10', 'Author 9', 1234567899, 2023]
        ]

        expected_count_2_reult = [
            ['Article 1', 'Author 1', 1234567890, 500],
            ['Article 3', 'Author 3', 1234567892, 1500]
        ]

        expected_count_4_reult = [
            ['Article 1', 'Author 1', 1234567890, 500],
            ['Article 3', 'Author 3', 1234567892, 1500],
            ['Article 4', 'Author 4', 1234567893, 2000],
            ['Article 9', 'Author 9', 1234567899, 2023]  
        ]

        expected_count_40_reult = [
            ['Article 1', 'Author 1', 1234567890, 500],
            ['Article 3', 'Author 3', 1234567892, 1500],
            ['Article 4', 'Author 4', 1234567893, 2000],
            ['Article 9', 'Author 9', 1234567899, 2023]  
        ]

        self.assertEqual(unique_authors(2, metadata), expected_count_2_reult)
        self.assertEqual(unique_authors(4, metadata), expected_count_4_reult)
        self.assertEqual(unique_authors(40, metadata), expected_count_40_reult)
        self.assertEqual(unique_authors(0, metadata), [])
        self.assertEqual(unique_authors(-1, metadata), [])
        self.assertEqual(unique_authors(1, []), [])

    def test_most_recent_article(self):
        metadata1 = [
            ['Article 1', 'Author 1', 1234567890, 500],
            ['Article 2', 'Author 2', 1234567891, 1000],
            ['Article 3', 'Author 3', 1234567892, 1500],
            ['Article 4', 'Author 4', 1234567898, 2000],
            ['Article 9', 'Author 9', 1234567899, 2023],
            ['Article 10', 'Author 9', 123, 2024]
        ]

        expected_most_recent_metadata1 = ['Article 9', 'Author 9',  1234567899, 2023]

        #metadata_with_same_timestamps
        metadata2 = [
            ['Article 2', 'Author 2', 1, 1000],
            ['Article 1', 'Author 1', 1, 500],
            ['Article 3', 'Author 3', 1, 1500],
            ['Article 4', 'Author 4', 1, 2000],
            ['Article 9', 'Author 9', 1, 2023]
        ]
        expected_most_recent_metadata2 = ['Article 9', 'Author 9',  1, 2023]

        self.assertEqual(most_recent_article(metadata1), expected_most_recent_metadata1)
        self.assertEqual(most_recent_article(metadata2), expected_most_recent_metadata2)
        self.assertEqual(most_recent_article([]), '')

    def test_favorite_author(self):
        metadata = [
            ['Article 1', 'Author 1', 1234567890, 500],
            ['Article 2', 'Author 2', 1234567891, 1000],
            ['Article 3', 'Author 3', 1234567892, 1500],
            ['Article 4', 'Author 4', 1234567893, 2000],
        ]
        self.assertEqual(favorite_author('Author1', metadata), False)
        self.assertEqual(favorite_author('Author 1', metadata), True)
        self.assertEqual(favorite_author('aUTHOR 3', metadata), True)
        self.assertEqual(favorite_author('Author1', []), False)
        self.assertEqual(favorite_author('', metadata), False)

    def test_title_and_author(self):
        metadata1 = [
            ['Article 1', 'Author 1', 1234567890, 500],
            ['Article 2', 'Author 2', 1234567891, 1000],
            ['Article 3', 'Author 3', 1234567892, 1500],
            ['Article 4', 'Author 4', 1234567898, 2000],
            ['Article 9', 'Author 9', 1234567899, 2023],
            ['Article 10', 'Author 9', 123, 2024]
        ]
        
        expected_metadata1_result = [
            ('Article 1', 'Author 1'),
            ('Article 2', 'Author 2'),
            ('Article 3', 'Author 3'),
            ('Article 4', 'Author 4'),
            ('Article 9', 'Author 9'),
            ('Article 10', 'Author 9')
        ]
        #all the duplicated entries
        metadata2 = [
            ['Article 1', 'Author 1', 1234567890, 500],
            ['Article 1', 'Author 1', 1234567891, 1000],
            ['Article 1', 'Author 1', 1234567892, 1500],
        ]
        expected_metadata2_result =[('Article 1', 'Author 1'), ('Article 1', 'Author 1'), ('Article 1','Author 1')]

        self.assertEqual(title_and_author(metadata1), expected_metadata1_result)
        self.assertEqual(title_and_author(metadata2), expected_metadata2_result)
        self.assertEqual(title_and_author([]), [])

    def test_refine_search(self):
        metadata1 = [
            ['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023],
            ['Lights (musician)', 'Burna Boy', 1213914297, 5898],
            ['Old-time music', 'Nihonjoe', 1124771619, 12755],
            ['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562]
        ]
        expected_metadata1 = [
            ['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023],
            ['Lights (musician)', 'Burna Boy', 1213914297, 5898],
            ['Old-time music', 'Nihonjoe', 1124771619, 12755],
            ['Will Johnson (soccer)', 'Burna Boy', 1218489712, 3562]
        ]
        metadata2 = [
            ['Covariance and contravariance (computer science)', 'Bearcat', 1167547]
        ]
        self.assertEqual(refine_search('the', metadata1), expected_metadata1)
        self.assertEqual(refine_search('', metadata2), [])
        self.assertEqual(refine_search('boy', []), [])
        
        


    #####################
    # INTEGRATION TESTS #
    #####################

    @patch('builtins.input')
    def test_example_integration_test(self, input_mock):
        keyword = 'soccer'
        advanced_option = 1
        advanced_response = 3000

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: [['Spain national beach soccer team', 'jack johnson', 1233458894, 1526], ['Steven Cohen (soccer)', 'Mack Johnson', 1237669593, 2117]]\n"

        self.assertEqual(output, expected)

# Write tests above this line. Do not remove.
if __name__ == "__main__":
    main()