import Vacancies

def save_to_csv():
    """
Функция, в которой получаем уникальные идентификаторы, через которые получаем данные и сохраняем их в CSV файл.
    """
    ids_SPb = Vacancies.get_vacancies_id("2")
    with open('SPb_ids.txt', 'w') as filehandle:
        for listitem in ids_SPb:
            filehandle.write('%s\n' % listitem)
    Vacancies.get_vacancies_info(ids_SPb, "SPb.csv")

save_to_csv()