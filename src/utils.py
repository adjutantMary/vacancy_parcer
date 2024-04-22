
from src.classes import ApiConnector, Save


def get_search():
    '''
    Метод для ввода поискового запроса вакансий из hh.ru
    :return:
    '''

    user_input = input('Введите название вакансии: ')
    search_param = input('Введите ключевые слова для фильтрации вакансий: ').split()
    users_salary = int(input('Введите старт зп: '))
    hh_object = ApiConnector()
    users_vacancies = hh_object.get_vacancies(user_input)
    filtered_vacancies = hh_object.filter_by_description(users_vacancies, search_param)
    vacancies_by_salary = hh_object.get_vacancies_by_salary(filtered_vacancies, users_salary)
    return vacancies_by_salary


def make_top_n(sorted_vacancies: list):
    '''
    Метод для сортировки вакансий по введенному N
    :param sorted_vacancies:
    :return:
    '''
    top_n = int(input('Введите количество вакансий для вывода: '))
    return sorted(sorted_vacancies, key=lambda x: top_n, reverse=True)


def get_save_data(vacancies):
    '''
    Метод сохранения полученных вакансий в JSON
    :param vacancies:
    :return:
    '''
    save_object = Save('data.json')

    json_data = save_object.save_vacancies_to_json(vacancies)
    return json_data


print(get_save_data(make_top_n(get_search())))
