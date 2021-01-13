import Vacancies

def save_to_csv():
    """
Функция, в которой получаем уникальные идентификаторы, через которые получаем данные и сохраняем их в CSV файл.
    """
    ids_Kazan = Vacancies.get_vacancies_id("88")
    with open('Kazan_ids.txt', 'w') as filehandle:
        for listitem in ids_Kazan:
            filehandle.write('%s\n' % listitem)
    Vacancies.get_vacancies_info(ids_Kazan, "Kazan.csv")

save_to_csv()
