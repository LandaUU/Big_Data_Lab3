import Vacancies

def save_to_csv():
    """
Функция, в которой получаем уникальные идентификаторы, через которые получаем данные и сохраняем их в CSV файл.
    """
    ids_Moscow = Vacancies.get_vacancies_id("1")
    with open('Moscow_ids.txt', 'w') as filehandle:
        for listitem in ids_Moscow:
            filehandle.write('%s\n' % listitem)
    Vacancies.get_vacancies_info(ids_Moscow, "Moscow.csv")

save_to_csv()