import json

import pandas
import requests


# Планируется поиск вакансий со специализацией = 1 в Москве, Санкт-Петербурге, Казани, Екатеринбурге,
# Тюмени и Ханты-Мансийске. По каждой area найдется 2000 (100 * 20) вакансий * 20 похожих вакансий = 40000 вакансий.
# 40000 * 6 = 240000 вакансий - скорей всего с повторами.
# area 1 - Москва area 2 - Санкт-Петербург area 3 - Екатеринбург area 88 - Казань area 95 -
# Тюмень area 147 - Ханты-Мансийск
# UPD: Упираюсь в лимит по запросам на API, поэтому использовал csv файл с 17 тыс вакансий

def append_similar_vacancies_id(vacancy_id, area, list):
    """
По уникальному номеру вакансии ищется 20 похожих вакансий
    :param vacancy_id: уникальный номер вакансии
    :param area: Область, в нашем случае это город
    :param list: список с уникальными номерами вакансий
    """
    r = requests.get("https://api.hh.ru/vacancies/" + str(vacancy_id) + "/similar_vacancies",
                     params={"specialization": "1", "per_page": "20", "area": area})
    if r.status_code == 200:
        data_json = json.loads(r.text)
        append_ids(list, data_json["items"])
        print(len(list))
        for index in range(1, 1):  # data_json["pages"]):
            r = requests.get("https://api.hh.ru/vacancies/" + str(vacancy_id) + "/similar_vacancies",
                             params={"specialization": "1", "per_page": "100", "area": area, "page": index})
            data_json = json.loads(r.text)
            append_ids(list, data_json["items"])
            print(len(list))


def append_ids_and_similar(list, items, area):
    """
Добавляет уникальные номера из JSON файла ответа в список. Создан с целью захода в функцию поиска похожих вакансий
    :param list: Список с уникальными идентификаторами вакансий
    :param items: JSON файл
    :param area: Область, в нашем случае это город
    """
    for item in items:
        list.append(item["id"])
        append_similar_vacancies_id(item["id"], area, list)


def append_ids(list, items):
    """
Добавляет уникальные номера из JSON файла ответа в список
    :param list: Список с уникальными номерами вакансий
    :param items: JSON файл ответа API HeadHunter
    """
    for item in items:
        list.append(item["id"])


def get_vacancies_id(area):
    """
Получить уникальные номера вакансий.
    :param area: Область, в нашем случае это город
    :return: Список уникальный номеров вакансий по области(городу)
    """
    r = requests.get("https://api.hh.ru/vacancies",
                     params={"specialization": "1", "per_page": "100", "area": area})
    list = []
    if r.status_code == 200:
        data_json = json.loads(r.text)
        # Получаем список id вакансий
        append_ids_and_similar(list, data_json["items"], area)
        for index in range(1, data_json["pages"]):
            r = requests.get("https://api.hh.ru/vacancies",
                             params={"specialization": "1", "per_page": "100", "area": area, "page": index})
            data_json = json.loads(r.text)
            append_ids_and_similar(list, data_json["items"], area)
        print("Получено " + str(len(list)) + " записей");
        return list


def get_vacancy_info(vacancy_id):
    """
По уникальному номеру вакансии получить данные и обработать их.
    :param vacancy_id: уникальный номер вакансии
    :return: Словарь с данными вакансии
    """
    r = requests.get("https://api.hh.ru/vacancies/" + str(vacancy_id))
    dict = {}
    if r.status_code == 200:
        data_json = json.loads(r.text)

        desc = str(data_json["description"]).replace("<p>", '').replace("</p>", "").replace('</li> <li>', '').replace(
            '</strong>', '').replace('<ul> <li>', '').replace('</li> </ul>', '').split('<strong>')

        # Название
        name = data_json["name"]
        # Город
        if data_json["address"] is not None and "city" in data_json["address"]:
            city = data_json["address"]["city"]
        else:
            city = None
        if "salary" in data_json and data_json["salary"] is not None:
            # Минимальная зарплата
            min_salary = data_json["salary"]["from"]
            # Максимальная зарплата
            max_salary = data_json["salary"]["to"]
        else:
            # Минимальная зарплата
            min_salary = data_json["salary"]
            # Максимальная зарплата
            max_salary = data_json["salary"]

        # Название компании
        company_name = data_json["employer"]["name"]
        # Дата размещения вакансии
        published_date = data_json["published_at"]
        # Требуемый опыт работы (Можно распарсить и найти min max)
        experience = data_json["experience"]["name"]
        # Тип занятости
        employment = data_json["employment"]["name"]
        # Рабочий график
        schedule = data_json["schedule"]["name"]
        # Описание
        description = desc[0]
        # Обязанности (в hh.ru находится в описании вакансии, нужно думать как вытаскивать)
        duty_list = [x for x in desc if x.__contains__("Обязанности") or x.__contains__("обязанности")]
        if len(duty_list) > 0:
            duty = duty_list[0]
        else:
            duty = None

        # Требования (аналогично обязанностям)
        requirments_list = [x for x in desc if x.__contains__("Требования") or x.__contains__("требования")]
        if len(requirments_list) > 0:
            requirements = requirments_list[0]
        else:
            requirements = None;
        # Условия (аналогично обязанностям)
        terms_list = [x for x in desc if x.__contains__("Условия") or x.__contains__("условия")]
        if len(terms_list) > 0:
            terms = terms_list[0]
        else:
            terms = None
        # Ключевые навыки (скорей всего в описании)
        skills = list(data_json["key_skills"])
        key_skills = ''
        if len(skills) > 0:
            for skill in skills:
                name = str(skill["name"])
                key_skills = key_skills + name + "|"
            key_skills.rstrip('|')
        # <strong>([А-я]*.[А-я]:) - маска для поиска заголовков
        # Нужно находить заголовки и делить строку на линии, каждая линия соответствует заголовку.
        # Линию очищать от тегов и вставлять линию без заголовка в столбец

        dict = {"name": name, "city": city, "min_salary": min_salary, "max_salary": max_salary,
                "company_name": company_name, "published_date": published_date, "experience": experience,
                "employment": employment, "schedule": schedule, "description": description, "duty": duty,
                "requirements": requirements, "terms": terms, "skills": key_skills}
        print(dict)
        return dict

def get_vacancies_info(ids, path):
    ids_unique = list(set(ids))
    df = pandas.DataFrame()
    for id in ids_unique:
        vacancy_dict = get_vacancy_info(id)
        df = df.append(vacancy_dict, ignore_index=True)
    df.to_csv(path)
    return df

def save_to_csv():
    """
Функция, в которой получаем уникальные идентификаторы, через которые получаем данные и сохраняем их в CSV файл.
    """
    ids_Moscow = get_vacancies_id("1")
    df_Moscow = get_vacancies_info(ids_Moscow, "Moscow.csv")
    ids_SPb = get_vacancies_id("2")
    df_SPb = get_vacancies_info(ids_SPb, "SPb.csv")
    ids_Kazan = get_vacancies_id("88")
    df_Kazan = get_vacancies_info(ids_Kazan, "Kazan.csv")
    ids_Ekaterinburg = get_vacancies_id("3")
    df_Ekaterinburg = get_vacancies_info(ids_Ekaterinburg, "Kazan.csv")
    ids_Tyumen = get_vacancies_id("95")
    df_Tyumen = get_vacancies_info(ids_Tyumen, "Tyumen.csv")
    ids_H_M = get_vacancies_id("147")
    df_H_M = get_vacancies_info(ids_H_M, "H_M.csv")
    df = df_Moscow.append(df_SPb).append(df_Kazan).append(df_Ekaterinburg).append(df_Tyumen).append(df_H_M)
    df.to_csv("Vacancies_full.csv")