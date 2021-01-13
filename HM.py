import Vacancies

def save_to_csv():
    """
Функция, в которой получаем уникальные идентификаторы, через которые получаем данные и сохраняем их в CSV файл.
    """
    ids_H_M = Vacancies.get_vacancies_id("147")
    with open('H_M_ids.txt', 'w') as filehandle:
        for listitem in ids_H_M:
            filehandle.write('%s\n' % listitem)
    Vacancies.get_vacancies_info(ids_H_M, "H_M.csv")

save_to_csv()
