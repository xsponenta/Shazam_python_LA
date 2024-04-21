import pickle

# Відкриття файлу для читання
with open("song_index.pickle", "rb") as file:
    # Завантаження даних з файлу
    database = pickle.load(file)
    print(database)
# Тепер ви можете використовувати зміну database для доступу до даних
