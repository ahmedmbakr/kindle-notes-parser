'''
This HTML parser is intended to get a list of notes from the HTML file provided as input
For more information about xpath, check the following link: https://docs.python.org/3/library/xml.etree.elementtree.html#xpath-support
'''

from lxml import etree
import csv
import xlwt
from xlwt import Workbook

class Html_book_parser:
    def __init__(self, html_file_name):
        file_content = None
        with open(html_file_name, "r",encoding="utf8") as file:
            file_content = file.read()
        self.__tree = None
        if file_content != None:
            self.__tree = etree.HTML(file_content)

    def __get_div_text_for_element(self, className):
        if self.__tree is None:
            return None
        
        r = self.__tree.xpath('.//div[@class="{}"]'.format(className))
        if len(r) > 0:
            return r[0].text.strip() # strip function removes trailing and leading spaces
        return None

    def get_book_name(self):
        return self.__get_div_text_for_element("bookTitle")

    def get_author_name(self):
        return self.__get_div_text_for_element("authors")

    def get_highlights(self):
        listOfHighlights = []
        if self.__tree is None:
            return None

        r = self.__tree.xpath('.//div[@class="noteText"]')
        for element in r:
            listOfHighlights.append(element.text.strip())

        return listOfHighlights

# Returns the highlights of a book as follows: (book_name, author, highlighted_note)
def get_html_book_highlights_entries(html_file_full_path, return_list):
    html_parser = Html_book_parser(html_file_full_path)
    book_name = html_parser.get_book_name().replace(",", "")
    author_name = html_parser.get_author_name().replace(",","")
    highlights_list = html_parser.get_highlights()
    for highlight in highlights_list:
        return_list.append((book_name, author_name, highlight))

def html_book_highlights_to_csv(html_file_names, excel_file_name):
    return_list = []
    # Workbook is created
    wb = Workbook()
    # add_sheet is used to create sheet.
    sheet1 = wb.add_sheet('Sheet 1')
    for html_file_full_path in html_file_names:
        html_parser = Html_book_parser(html_file_full_path)
        book_name = html_parser.get_book_name().replace(",", "")
        author_name = html_parser.get_author_name().replace(",","")
        highlights_list = html_parser.get_highlights()
        get_html_book_highlights_entries(html_file_full_path, return_list)
        print("transformed the file: {} successfully to excel rows".format(html_file_full_path))

    row_idx = 0
    for list_item in return_list:
        col_idx = 0
        for item in list_item:
            sheet1.write(row_idx, col_idx, item)
            col_idx += 1
        row_idx += 1
    wb.save(excel_file_name)
    print('Save to excel sheet with name {} complete'.format(html_file_full_path))

if __name__ == '__main__':
    html_file_names = ['Atomic Habits_ The life-changing million copy bestseller - Notebook.html', 'Show Your Work!_ 10 Ways to Share Your Creativity and Get Discovered - Notebook.html', 'Sleep Smarter_ 21 Essential Strategies to Sleep Your Way to A Better Body, Better Health, and Bigger Success - Notebook.html', 'Steal Like an Artist_ 10 Things Nobody Told You About Being Creative - Notebook.html', 'The Subtle Art of Not Giving a F_ck_ A Counterintuitive Approach to Living a Good Life (Mark Manson Collection Book 1) - Notebook.html']
    excel_file_name = 'output.xls'
    html_book_highlights_to_csv(html_file_names, excel_file_name)
    
    
