#!/usr/bin/env python
""" Use Baidu search via terminal command """

import argparse
import requests
from bs4 import BeautifulSoup
from result import Result

baidu_search_url = 'http://www.baidu.com/s?wd='
baidu_headers = {
    'Accept-Encoding': 'identity'
}
results_store_file_name = 'baidu.html'


def main():
    parse = argparse.ArgumentParser(prog='PY_Baidu', description="Use Baidu Search via Terminal command.")
    
    parse.add_argument('-c', '--config', required=False, help="Config for PY_Baidu.", default='baidu.conf')
    parse.add_argument('query', type=str, nargs='+', default="")
    
    args = parse.parse_args()
    
    query_words = get_query_words(args.query)
    request_url = get_search_request_url(query_words)
    results = get_search_results_from_baidu(request_url)
    
    # load_config(args.config)
    
    print("Baidu: {user_query} ".format(user_query=query_words))
    print("Query URL: {url}".format(url=request_url))
    print("\n")
    
    # with open(results_store_file_name, 'w') as file:
    #     file.write(results)
    #     file.close()

    soup = BeautifulSoup(results, features='html.parser')
    raw_results = soup.find_all(class_='result')

    results = []
    for index, raw_result in enumerate(raw_results):
        title = raw_result.find('h3').find('a').get_text()
        link = raw_result.find('h3').find('a', href=True)['href']
        abstract_element = raw_result.find(class_='c-abstract');
        abstract = abstract_element.get_text() if abstract_element is not None else "(No abstract.)"
        
        # result = Result(title, link, abstract);
        # results.append(result)
        
        # print(title)
        
        print("{index}: {title}\n\tURL: {link}\n\t{abstract}\n".format(
            index=index + 1,
            title=title,
            link=link,
            abstract=abstract))


def load_config(config):
    """ Load config for searching. """
    # TODO
    print("Load Config from: {}".format(config))


def get_query_words(word_array):
    """ Generate query words from user input word arguments. """
    if len(word_array) == 0 or word_array is None:
        return ""
    return " ".join(word_array)


def get_search_request_url(query_words):
    """ Concat Baidu search url and user's search words. """
    return baidu_search_url + query_words


def get_search_results_from_baidu(search_request_url):
    """ Send search request and get web content return. """
    response = requests.get(search_request_url, headers=baidu_headers)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    return response.text


if __name__ == '__main__':
    main()
