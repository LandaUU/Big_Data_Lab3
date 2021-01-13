import Vacancies

def save_to_csv():
    """
Функция, в которой получаем уникальные идентификаторы, через которые получаем данные и сохраняем их в CSV файл.
    """
    ids_Krasnodar = Vacancies.get_vacancies_id("53")
    with open('Krasnodar_ids.txt', 'w') as filehandle:
        for listitem in ids_Krasnodar:
            filehandle.write('%s\n' % listitem)
    Vacancies.get_vacancies_info(ids_Krasnodar, "Krasnodar.csv")

save_to_csv()
