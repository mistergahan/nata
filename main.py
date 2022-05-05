import streamlit as st
import docx2txt
import sqlite3
from sqlite3 import Connection
import pandas as pd

from natasha import (
    NamesExtractor,
    LocationExtractor,
    AddressExtractor,
    DatesExtractor,
    MoneyExtractor,

)

URI_SQLITE_DB = "vkrb.db"
#Connecting to sqlite
conn = sqlite3.connect('vkrb.db')
#Creating a cursor object using the cursor() method
cursor = conn.cursor()
#Doping EMPLOYEE table if already exists.
cursor.execute("DROP TABLE IF EXISTS DOCDetails")

# Подсоединяем БД
def init_db(conn: Connection):
    conn.execute(
        """CREATE TABLE IF NOT EXISTS vkrb
            (
                FIO CHAR,
                ADRESS CHAR,
                DAT CHAR ,
                MONEY CHAR,
                FILE CHAR 
                 
            );"""
    )
    conn.commit()


def get_data(conn: Connection):
    df = pd.read_sql("SELECT * FROM vkrb", con=conn)
    return df


def display_data(conn: Connection):
    if st.checkbox("Показать Базу данных SQLite"):
        st.dataframe(get_data(conn))


class NatashaExtractor:
    '''This class used library Natasha for search entities in text

    https://github.com/natasha/natasha
    '''

    def __init__(self, text):
        self.text = text

    def get_names(self):
        extractor = NamesExtractor()
        matches = extractor(self.text)
        facts = [_.fact.as_json for _ in matches]
        return facts

    def get_locations(self):
        extractor = LocationExtractor()
        matches = extractor(self.text)
        facts = [_.fact.as_json for _ in matches]
        return facts

    def get_addresses(self):
        extractor = AddressExtractor()
        matches = extractor(self.text)
        facts = [_.fact.as_json for _ in matches]
        return facts

    def get_dates(self):
        extractor = DatesExtractor()
        matches = extractor(self.text)
        facts = [_.fact.as_json for _ in matches]
        return facts

    def get_money(self):
        extractor = MoneyExtractor()
        matches = extractor(self.text)
        facts = [_.fact.normalized.as_json for _ in matches]
        return facts


def main():
    '''conn = get_connection(URI_SQLITE_DB)
    init_db(conn)'''
    st.markdown('''<p style="font-size: 80px;
                    background: -webkit-linear-gradient(#FFA500, #FF4500);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    font-family: verdana;
                    font-weight: bold;
                    font-size:42px">
                    Система извлечния сущностей из текстовых документов
                    </p>''', unsafe_allow_html=True)

    menu = ["Домашняя страница", "База Данных", "О сервисе"]
    choice = st.sidebar.selectbox("Меню", menu)

    if choice == "Домашняя страница":
        st.subheader("Выберите  документ:")
        col1, col2 = st.columns((9, 1))

        with col1:
            content_file = st.file_uploader("Выберите документ для обработки", ['docx'],
                                            help="Перетащите или выберите файл, ""ограничение размера - 25 Мб на файл\n\n"" • Формат файлa - DOCX.")
            if content_file is not None:
                file_details = {"FileName": content_file.name, "FileType": content_file.type}
                fname = content_file.name
                if content_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    text = docx2txt.process(content_file)
        #

        col7, col8, col9 = st.columns((2, 2, 2))
        with col8:
            style_transfer_button = st.button("Начать обработку")
            if style_transfer_button:
                if content_file is None:
                    st.error("Ошибка: Документ не загружен.")
                else:
                    st.success("Ожидайте, идет обработка.")

                    a = NatashaExtractor(text)
                    # st.write("Даты")
                    for i in a.get_dates():
                        #st.write(i)
                        dat = i
                        cursor.execute(f"INSERT INTO vkrb (DAT, FILE) VALUES ({dat, fname})")
                        conn.commit()
                    # st.write("ФИО")
                    for n in a.get_names():
                        #st.write(n)
                        nam = n
                        cursor.execute(f"INSERT INTO vkrb (FIO, FILE) VALUES ({nam, fname})")
                        conn.commit()
                    # st.write("Адрес")
                    for k in a.get_addresses():
                        #st.write(k)
                        addr = k
                        conn.execute(f"INSERT INTO vkrb (ADRESS, FILE) VALUES ({addr, fname})")
                        conn.commit()
                    # st.write("Деньги")
                    for m in a.get_money():
                        #st.write(m)
                        mon = m
                        cursor.execute(f"INSERT INTO vkrb (MONEY, FILE) VALUES ({mon, fname})")
                        conn.commit()




    elif choice == "База Данных":
        st.subheader("База Данных")
        display_data(conn)

    elif choice == "О сервисе":
        st.subheader("О сервисе")
        st.text("Алгоритм заложенный в основу сервиса позволяет пользовтеляю")
        st.text("извлекать из текстовых документов в формате DOCX Адреса, ФИО, Даты и Денежные суммы")
        st.text("_______________________________________________________")
        st.text("Сервис разработан студентом группы ИУ5-81Б")
        st.text("Карповым Даниилом")
        st.text("МГТУ им. Н.Э. Баумана, 2022")


def get_connection(path: str):
    """Put the connection in cache to reuse if path does not change between Streamlit reruns.
    NB : https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
    """
    return sqlite3.connect(path, check_same_thread=False)


if __name__ == '__main__':
    main()


def small_title(x):
    text = f'''<p style="background: -webkit-linear-gradient(#FF4500, #FFA500);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        font-family: verdana;
                        font-weight: bold;
                        font-size:24px">
                        {x}
                        </p>'''
    return text


text = f'''{small_title('Общая информация')}
<p>
Этот webapp использует возможности библиотеки Natasha и Yagy-парсера для извлечения информации из текстовых документов.
Пользователи могут отправить файл в формате DOCX и получить таблицу с ключевыми данными, которые содержит данный документ.</p >
<div>
</div>
'''
st.sidebar.markdown(text, unsafe_allow_html=True)
