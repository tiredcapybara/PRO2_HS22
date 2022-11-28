def auslesenalb():
    with open("database-alb.csv", "r") as open_file:
        inhalt = open_file.read()
        return inhalt


def abspeichernalb(albtitel, albintepret, albgenre, albgehoert, albrelease, albrating):
    current_content = auslesenalb()
    new_content = current_content + f"\n{albtitel}, {albintepret}, {albgenre}, {albgehoert}, {albrelease}, {albrating}"
    with open("database-alb.csv", "w") as open_file:
        open_file.write(new_content)
