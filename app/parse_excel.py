from openpyxl import load_workbook
from copy import copy
HEADERS_COUNT = 11
HEADERS = {'Название', 'Авторы', 'Серия', 'Категории', 'Дата публикации', 'Издательство', 'Количество страниц', 'ISBN', 'Комментарии', 'Краткое содержание', 'Ссылка'}       
def parse_excel(file) -> list | bool:
    wb = load_workbook(file)
    sheet = wb[wb.active.title]
    data = list(); columns_count = sheet.max_column
    if columns_count != HEADERS_COUNT:
        return False
    # count = 0
    # head_row = 0
    # for header_elem in sheet[head_row]:
    #     headers[str(header_elem.value).strip()] = count
    #     count += 1
    
    row_index = 0; headers_set = set()
    for row in sheet:  
        # проверяем на соответствие нашим ожиданиям входной файл 
        if not row_index:
            for index in range(HEADERS_COUNT):  
                headers_set.add(row[index].value)
            row_index += 1
            if headers_set != HEADERS:
                return False
            continue
        
        cur_book = list(); count = 1  
        for index in range(HEADERS_COUNT):  
            if (index == 8 and row[index].value != "Комментарии"):  
                val = str(row[index].value).split(",")[-1]
                if "экземпляра" in val or "экземпляров" in val or "экземпляр" in val:  
                    count = int(val.strip().split(" ")[0])
                     
            val = row[index].value
            if type(val) == int or type(val) == float:
                cur_book.append(val)
            else:
                cur_book.append(str(val).strip().lower())
           
        cur_book.append(count)    
        data.append(copy(cur_book)) 
    
    del data[0]
    return data
     
            