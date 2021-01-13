import Vacancies

def save_to_csv():
    """
Функция, в которой получаем уникальные идентификаторы, через которые получаем данные и сохраняем их в CSV файл.
    """
    ids_Tyumen = Vacancies.get_vacancies_id("95")
    with open('Tyumen_ids.txt', 'w') as filehandle:
        for listitem in ids_Tyumen:
            filehandle.write('%s\n' % listitem)
    Vacancies.get_vacancies_info(ids_Tyumen, "Tyumen.csv")

save_to_csv()
