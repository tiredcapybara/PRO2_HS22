import plotly.express as px


# fig = px.pie(labels=[1, 2, 3, 4, 5], values=[6, 7, 8, 5, 3])
#
# fig.show()

from datetime import datetime
import time

def test():
    date = "2022-03-31"
    date = datetime.strptime(date, "%Y-%m-%d")
    print(str(date))
    print(date.month)
    date = date.strftime("%m.%Y")
    print(date)

if __name__ == "__main__":
    test()
