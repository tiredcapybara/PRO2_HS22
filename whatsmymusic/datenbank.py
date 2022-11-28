import json


def auslesen():
    file = open("databasesongs.json")
    songs = json.load(file)
    return songs


def song_speichern(daten):
    songs = auslesen()
    id_song = songs[-1]["id"]

    song = {
        "id": id_song + 1,
        "titel": daten["titel"],
        "intepret": daten["intepret"],
        "genre": daten["genre"],
        "gehoert": daten["gehoert"],
        "release": daten["release"],
        "rating": daten["rating"]
    }
    songs.append(song)
    print(songs)

    songs_json = json.dumps(songs)
    file = open("databasesongs.json", "w")
    file.write(songs_json)
    file.close()
    return


def auslesenalb():
    file = open("databasealb.json.")
    alben = json.load(file)
    print(alben)
    return alben


def album_speichern(datenalb):
    alben = auslesenalb()
    id_album = alben[-1]["id"]

    album = {
        "id": id_album + 1,
        "titel": datenalb["albtitel"],
        "intepret": datenalb["albintepret"],
        "genre": datenalb["albgenre"],
        "gehoert": datenalb["albgehoert"],
        "release": datenalb["albrelease"],
        "rating": datenalb["albrating"]
    }
    alben.append(album)
    print(album)

    alben_json = json.dumps(alben)
    file = open("databasealb.json", "w")
    file.write(alben_json)
    file.close()
    return
