import Vacancies

def save_to_csv():
    """
Функция, в которой получаем уникальные идентификаторы, через которые получаем данные и сохраняем их в CSV файл.
    """
    ids_Ekaterinburg = Vacancies.get_vacancies_id("3")
    with open('Ekaterinburg_ids.txt', 'w') as filehandle:
        for listitem in ids_Ekaterinburg:
            filehandle.write('%s\n' % listitem)
    Vacancies.get_vacancies_info(ids_Ekaterinburg, "Ekaterinburg.csv")

save_to_csv()
