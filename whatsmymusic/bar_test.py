import plotly.express as px


fig = px.pie(labels=[1, 2, 3, 4, 5], values=[6, 7, 8, 5, 3])

fig.show()