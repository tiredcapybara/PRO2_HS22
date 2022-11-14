def auslesen():
    with open("database.csv", "r") as open_file:
        inhalt = open_file.read()
        return inhalt


def abspeichern(titel, intepret, genre, gehoert, release, rating):
    current_content = auslesen()
    new_content = current_content + f"\n{titel}, {intepret}, {genre}, {gehoert}, {release}, {rating}"
    with open("database.csv", "w") as open_file:
        open_file.write(new_content)
