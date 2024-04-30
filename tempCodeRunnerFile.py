import pickle

# Open the pickle file in binary read mode
with open("database.pickle", "rb") as db_file:
    # Load the contents of the pickle file
    database = pickle.load(db_file)

print(database)