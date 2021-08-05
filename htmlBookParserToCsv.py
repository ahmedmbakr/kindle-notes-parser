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

def html_book_highlights_to_csv(html_file_full_path, excel_file_name):
    html_parser = Html_book_parser(html_file_full_path)
    book_name = html_parser.get_book_name().replace(",", "")
    author_name = html_parser.get_author_name().replace(",","")
    highlights_list = html_parser.get_highlights()

    # Workbook is created
    wb = Workbook()

    # add_sheet is used to create sheet.
    sheet1 = wb.add_sheet('Sheet 1')
    idx = 0
    for highlight in highlights_list:
        sheet1.write(idx, 0, book_name)
        sheet1.write(idx, 1, author_name)
        sheet1.write(idx, 2, highlight)
        idx += 1

    wb.save(excel_file_name)

    # # open the file in the write mode
    # f = open(csv_file_name, 'w',errors="ignore")
    # # create the csv writer
    # writer = csv.writer(f)
    # for highlight in highlights_list:
    #     highlight = highlight.replace(",", "")
    #     csv_row = book_name + "," + author_name + "," + highlight
    #     print(csv_row)
    #     writer.writerow(csv_row)
    # f.close()
    # print("printed successfully to the csv, whose name is " + csv_file_name)

if __name__ == '__main__':
    html_file_name = 'Atomic Habits_ The life-changing million copy bestseller - Notebook.html'
    excel_file_name = 'output.xls'
    html_book_highlights_to_csv(html_file_name, excel_file_name)
    
