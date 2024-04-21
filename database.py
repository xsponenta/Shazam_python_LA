import glob
from typing import List, Dict, Tuple
from tqdm import tqdm
import pickle
from scipy.io.wavfile import read
from constellations import create_constellation
from hashes import create_hashes

songs = glob.glob('Rain Over Me.wav')

song_index = {}
database: Dict[int, List[Tuple[int, int]]] = {}

for index, filename in enumerate(tqdm(sorted(songs))):
    song_index[index] = filename
    Fs, audio_input = read(filename)
    constellation = create_constellation(audio_input, Fs)
    hashes = create_hashes(constellation, index)
    for hash, time_index_pair in hashes.items():
        if hash not in database:
            database[hash] = []
        database[hash].append(time_index_pair)

with open("database.pickle", 'wb') as db:
    pickle.dump(database, db, pickle.HIGHEST_PROTOCOL)
with open("song_index.pickle", 'wb') as songs:
    pickle.dump(song_index, songs, pickle.HIGHEST_PROTOCOL)
