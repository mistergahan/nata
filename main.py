import streamlit as st
import docx2txt
from natasha import (
    NamesExtractor,
    LocationExtractor,
    AddressExtractor,

    OrganisationExtractor,

    DatesExtractor,
    MoneyExtractor,

)


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

    def get_org(self):
        extractor = OrganisationExtractor()
        matches = extractor(self.text)
        facts = [_.fact.normalized.as_json for _ in matches]
        return facts


def main():
    st.markdown('''<p style="font-size: 80px;
                    background: -webkit-linear-gradient(#FFA500, #FF4500);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    font-family: verdana;
                    font-weight: bold;
                    font-size:42px">
                    Обработка
                    </p>''',unsafe_allow_html=True)
    # st.text(tf.executing_eagerly())
    menu = ["Домашняя страница", "О сервисе"]
    choice = st.sidebar.selectbox("Меню", menu)

    if choice == "Домашняя страница":
        st.subheader("Выберите  документ:")
        col1 = st.columns(1)

        with col1:
            content_file = st.file_uploader("Выберите документ для обработки", ['docx'],
                                             help="Перетащите или выберите файл, "
                                                  "ограничение размера - 25 Мб на файл\n\n"
                                                  " • Формат файлf - DOCX.")
            if content_file is not None:
                file_details = {"FileName": content_file.name, "FileType": content_file.type}
                if content_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    text = docx2txt.process(content_file)  # Parse in the uploadFile Class directory
                st.write(text)

        col7, col8, col9 = st.columns((2, 1, 2))
        with col8:
            style_transfer_button = st.button("Начать обработку")
            if style_transfer_button:
                if content_file is not None :
            else:
                st.subheader("About")
                st.info("Built with Streamlit")
                st.info("Jesus Saves @JCharisTech")
                st.text("Jesse E.Agbe(JCharis)")
                st.write(file_details)

            elif content_file is not None:
                st.error("Ошибка: Документ не загружен.")

    else:
        st.subheader("О сервисе")
        st.text("Алгоритм чегото там")
        st.text("-----------------------------------------------------------------------------")
        st.text("Сервис разработан студентом группы ИУ5Ц-102Б")
        st.text("Гусевым Сергеем")
        st.text("МГТУ им. Н.Э. Баумана, 2022")

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
Пользователи могут отправить файл в формате DOCX и скачать таблицу с ключевыми данными, которые содержит данный документ.</p >
<div>
</div>
'''
st.sidebar.markdown(text, unsafe_allow_html=True)