Simplified Search Engine
A search engine takes a given search phrase or word and finds pages on the internet that are relevant, ranks the pages, and then displays the pages in the order of ranking.

In part 1 of this project, we searched a list of article titles to see if they contain a user provided keyword as a part of the title. In part 2, we searched through a 2D list of article metadata in order to find articles that are relevant to our keyword rather than having titles that strictly include it. In part 3 we will search through the same 2D list of metadata but before performing our searches, we will preprocess the data into dictionaries.

All article metadata can be fetched by calling the wiki.article_metadata(). It returns a 2D list where each individual "row" represents a single article. Each article is represented as a list with the following information provided in this exact order:

Article title (string)

Author name (string)

Timestamp of when the article was published (int). The timestamp is stored as the # of seconds since January 1st, 1970 (also known as Unix/Epoch Time)

The number of characters in the article (int)

A list of keywords that are related to the article content (list of strings)

To demonstrate, here is a potential example row in the 2D list:

['Spongebob - the legacy', 'Mr Jake', 1172208041, 5569, ['Spongebob', 'cartoon', 'pineapple', 'tv', 'sponge', 'nickelodean', 'legacy']]

We will use this data to create a more powerful search engine that returns results based on this metadata. Our search will have three parts:

Preprocessing

In order to help run different searches, there are two pre-processing functions you must implement: title_to_info(metadata) and keyword_to_titles(metadata), both of which take an entire 2D list of article metadata as arguments. As a reminder, each article’s metadata contains [title, author, timestamp, article length, keywords] in that order. The functions reorganize the data into dictionaries to make other search functions easier:

title_to_info - processes article metadata into a dictionary mapping an article title to its metadata, which is in turn a dictionary with the following keys: author, timestamp, and length.

keyword_to_titles - processes article metadata into a dictionary mapping a keyword to a list of all articles containing that keyword.

Basic Search

To run a basic search, ask the user for a keyword and use the keyword to find all article titles relevant to the keyword. For each article, include it in the search results if the user keyword is a (case-sensitive) match for one of the words in the article's relevant keywords list. For example, given the example article above ("Spongebob - the legacy"), it would be included in the search result if the user keyword was "Spongebob" or "tv" but excluded if the user keyword was "bob", "spongebob", or "TV". The function should return a 1D list of article titles where a match was found (note that this is different behavior from the basic search in part 2). To ease this search, it will take in the results from one of your preprocessing steps as an argument.

If the user does not enter anything or no results are found, return an empty list.

When running a search, the basic search will always be run, and it will always be run before the advanced search.

Advanced Search

The user is then prompted for different options to perform an advanced search. There will be 6 advanced search options:

Article title length - user provides a max article title length (in characters). Return a list of article titles from the basic search that do not exceed the max article length.

Key by author - returns a dictionary that remaps the articles from the basic search using authors as the key. The values are a list of all article titles written by that author.

Filter to author - user provides an author. Return the articles from the basic search written by that author.

Filter out - user provides another keyword. Return a list of article titles from the basic search that do not have the new keyword in their "related keywords".

Article year - user provides a year. Return a list of article titles from the basic search that were written in that year.

None - user does not want an advanced search. (There is no function for this

Starter Code
search.py: file for adding functionality to search

wiki.py: do not change this file. provides raw article metadata and functions to help you write the search code:

article_metadata(): returns complete list of article metadata our search engine will have access to

ask_search(): asks user for a keyword to search for

ask_advanced_search(): displays and asks user for advanced options search

search_tests.py: file for adding unit and integration tests

search_tests_helper.py: do not change this file. provided functions to help you write integration tests:

print_basic(): returns string to ask user for basic search keyword

print_advanced(): returns string to ask user for advanced search option

print_advanced_option(): returns string to ask user for advanced search question

get_print(): returns printed string when running entire search program

Instructions

keyword_to_titles(metadata): Takes a 2D list of article metadata as a parameter. Returns a dictionary mapping a keyword to a list of all articles containing that keyword.

title_to_info(metadata): Takes a 2D list of article metadata as a parameter. Returns a dictionary mapping an article title to its metadata, which is in turn a dictionary with the following keys: "author", "timestamp", and "length".

search(keyword, keyword_to_titles): Takes a keyword and a dictionary of keywords to titles (results from calling your preprocessing function #1) as parameters. Returns a list of all article titles containing this keyword. This search is case-sensitive, meaning it will only return results where the keyword matched exactly (ex: 'dog' and 'Dog' are not equal like in previous parts).

article_length(max_length, article_titles, title_to_info): Takes a max length, list of article titles from the basic search, and a dictionary of titles to info (results from calling your preprocessing function #2) as parameters. Returns a list of article titles for articles that are less than or equal to max_length in character count according to their metadata.

key_by_author(article_titles, title_to_info): Takes a list of article titles and a dictionary of titles to info (results from calling your preprocessing function #2) as parameters. Returns a dictionary that uses the author as a key (case-sensitive) and each value is a list of all articles by that author. 

filter_to_author(author, article_titles, title_to_info) : Takes an author name, list of article titles from the basic search, and a dictionary of titles to info (results from calling your preprocessing function #2) as parameters. Returns a list of article titles for only articles from the basic search that were written by the provided author (case-sensitive). If no articles were written by the author, return an empty list.

filter_out(keyword, article_titles, keyword_to_titles): Takes a new keyword, list of article titles from the basic search, and a dictionary of keyword to titles (results from calling your preprocessing function #1) as parameters. Returns a list of article titles from the basic search that do not include the new keyword.

articles_from_year(year, article_titles, title_to_info): Takes a year, a list of article titles from the basic search, and a dictionary of titles to info (results from calling your preprocessing function #2) as parameters. Returns the article titles that were published during the provided year. You may notice while playing with this function that most of the article data in wiki.py is from 2007, 2008, or 2009! Hint: to get the unix timestamp for a specific date, use a combination of datetime.date and time.mktime. Example: