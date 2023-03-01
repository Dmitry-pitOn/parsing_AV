import requests
from bs4 import BeautifulSoup
from datetime import date
import os

# заголовки не менял
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}

all_auto_list = []
def start_pages():
    resp_list = []
    page_number = int(input("Введите количество страниц: "))
    for number in range(1, page_number + 1):

        url = f"https://cars.av.by/filter?place_city[0]=7&place_region[0]=1002&page={number}&sort=4"
        src = requests.get(url, headers=headers)
        result = src.text

        soup = BeautifulSoup(result, "lxml")

        id_link = soup.find_all(class_="listing-item__link")

        for i in id_link:
            id_list = i.get("href").split("/")
            link_with_id = f"https://api.av.by/offers/{id_list[-1]}/phones"
            response = requests.get(link_with_id).json()
            if isinstance(response, list):
                resp_list.append(response[0])
        print(f"INFO: {number}/{page_number}")

    tel_numbers = []
    for i in resp_list:
        tel_numbers.append(f"{i['country']['code']}{i['number']}")
    print(f"Спарсено номеров: {len(tel_numbers)}")

    with open(r"D:\Python\parcer_AV\Vitebsk AV\vitebsk_numbers.txt", 'w', encoding='utf-8') as file:
        for number in tel_numbers:
            file.write(f"{number}\n")

def list_with_phones():
    # создаём два списка - с общими номерами и собранными
    for root, dirs, files in os.walk(r"d:\Python\parcer_AV\Все номера"):
        with open(f"{root}\\{files[0]}", 'r', encoding='utf-8') as file:
            all_start_list = file.read().split()
    with open("vitebsk_numbers.txt", "r") as file:
        raw_number_list = file.read().split('\n')
    raw_number_list = list(set(raw_number_list))  # удаляем дубликаты из собранных номеров

    # записываем все собранные номера в файл
    with open(rf"D:\Python\parcer_AV\Собранные номера\all_new_numbers {len(raw_number_list)}.txt", "w") as file:
        for i in raw_number_list:
            file.write(f"{i}\n")

    # удаляем дубликаты, сравнивая с общим списком
    duble = 0
    new_list_other_dublicates = []
    for i in raw_number_list:
        if i in all_start_list:
            duble += 1
        else:
            new_list_other_dublicates.append(i)
    print(f"""Дубликатов: {duble}
Новых номеров: {len(new_list_other_dublicates)}
    """)
    print('-' * 60)

    # добавляем в общий список новые номера и переименовываем файл
    for root, dirs, files in os.walk(r"d:\Python\parcer_AV\Все номера"):
        with open(f"{root}\\{files[0]}", 'a', encoding='utf-8') as file:
            for number in new_list_other_dublicates:
                file.write(f"{number}\n")
        os.rename(f"{root}\\{files[0]}", f"{root}\\all_numbers ({len(all_start_list) + len(new_list_other_dublicates)}).txt")

    # добавляем новые номера в файл
    current_date = date.today()
    with open(rf"D:\Python\parcer_AV\Vitebsk AV\Новые фильтр номера\new_numbers_vitebsk_AV_{current_date}.txt", "w") as file:
        for i in new_list_other_dublicates:
            file.write(f"{i}\n")

    print(f"""Скрипт завершён успешно
Новых номеров: {len(new_list_other_dublicates)}
Файл "new_numbers_vitebsk.txt" создан
    """)


def main():
    start_pages()
    list_with_phones()


if __name__ == "__main__":
    main()
