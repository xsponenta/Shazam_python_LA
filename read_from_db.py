import pickle



with open("song_index.pickle", "rb") as index_file:
    song_index = pickle.load(index_file)

# Print the song index
for index, filename in song_index.items():
    print(f"Index: {index}, Filename: {filename}")