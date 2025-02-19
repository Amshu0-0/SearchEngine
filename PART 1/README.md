Search Engine: Part 1
Simplified Search Engine
Project Description
A search engine takes a given search phrase or word and finds pages on the internet that are relevant, ranks the pages, and then displays the pages in the order of ranking.

For this project, we’ll build a simplified search engine that returns articles in no particular order from searching one word, a keyword. Each search will have two parts:

Basic Search

To run a basic search, ask the user for a keyword and use the keyword to search through the complete list of articles (from wiki.article_titles()), and return the list of articles that contain the keyword. The search should not be case-sensitive (ie if a user enters “Dog”, the resulting list should return all titles with “Dog”, “dog”, "dOG", etc.). If the user does not enter anything or no results are found, return an empty list.

When running a search, the basic search will always be run, and it will always be run before the advanced search.

Advanced Search

The user is then prompted for different options to perform an advanced search. There will be 6 advanced search options:

Article title length - user provides a max article title length (in characters). After searching for article titles with the user’s keyword, return only the article titles that do not exceed the max article title length. For example, if the user searched for “dog” and wants a maximum article title length of 25 characters, only return article titles containing the word “dog” with a maximum article title length of 25 characters.

Number of articles - user provides a max number of articles to receive. After searching for article titles with the user’s keyword, return the number of articles requested by the user, starting from the first article. If the number of articles requested by the user exceeds the number of articles satisfying the keyword search, return the entire list.

Get one random article - user provides a random number. After searching for article titles with the user’s keyword, return only the article title at the index of the user’s random number. If there are no articles or the index is not within the bounds of the articles, return an empty string.

Check whether favorite article in list - user provides a favorite article title. After searching for article titles with the user’s keyword, return True if the provided article is included in the returned list of article titles and False otherwise. The search should not be case-sensitive (ex: if the favorite article title is "guide dog" and "Guide dog" is provided, returns True).

Multiple keywords - user provides another keyword to search. After searching for article titles with the user’s basic search keyword, search all of the articles again using this second keyword. Return a combined list of all articles from both search results, with the new search results coming after the initial results from the basic search.

None - user does not want an advanced search.


Starter Code
search.py: file for adding functionality to search

wiki.py: provides raw article data and functions to help you write the search code:

article_titles(): returns complete list of article titles our search engine will have access to

ask_search(): asks user for a keyword to search for

ask_advanced_search(): displays and asks user for advanced options search

search_tests.py: file for adding unit and integration tests

search_tests_helper.py: provided functions to help you write integration tests:

print_basic(): returns string to ask user for basic search keyword

print_advanced(): returns string to ask user for advanced search option

print_advanced_option(): returns string to ask user for advanced search question

get_print(): returns printed string when running entire search program

search(keyword): Searches all article titles from wiki.article_titles() and returns a list of all article titles that contain the keyword (case insensitive)

title_length(max_length, titles): Returns a list of titles that are less than or equal to max_length in character count.

article_count(count, titles) : Returns the first count articles from the titles. If count is larger than the length of the titles, just return all titles.

random_article(index, titles): Returns the article in titles at index or an empty string if index is invalid. Index is positive but must be within the length of the string.

favorite_article(favorite, titles): Returns True or False depending on if the titles contain your favorite article (case insensitive)

multiple_keywords(keyword, titles): Searches all article titles from wiki.article_titles() using keyword and returns a combined list of the basic search articles followed by the new articles.