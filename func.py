import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


import Source
import Wave

sources_info = Source.parse_source("sources.csv")
waves_info = Wave.parse_wave("waves.csv")
sources_df = pd.DataFrame(t.__dict__ for t in sources_info)
waves_df = pd.DataFrame(t.__dict__ for t in waves_info)


def map_source_country():
    sources_by_country = pd.DataFrame({'count': sources_df['country_s'].value_counts()})
    map1 = px.choropleth(sources_by_country, locations=sources_by_country.index, locationmode='country names',
                         color_continuous_scale=[[0, 'yellow'], [0.1, 'rgb(255,145,0)'], [0.2, 'red'],
                                                 [0.3, 'rgb(247,0,255)'], [0.6, 'blue'], [1, 'green']],
                         hover_data=['count'], color='count', title="Number of sources by country",
                         labels={"count": "Sources number"}
                         )
    map1.update_layout(title={
        'x': 0.5,
        'xanchor': 'center'
    })
    map1.update_geos(showcountries=True,
                     countrycolor="black"
                     )
    map1.update_layout(margin={'r': 50, 't': 50, 'l': 50, 'b': 50, 'pad': 0},
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)')
    return map1


def map_waves_country():
    waves_by_country = pd.DataFrame({'count': waves_df['country_w'].value_counts()})
    map2 = px.choropleth(waves_by_country, locations=waves_by_country.index, locationmode='country names',
                         color_continuous_scale=[[0, 'rgb(239,255,0)'], [0.01, 'rgb(43,255,0)'],
                                                 [0.04, 'rgb(0,255,179)'], [0.08, 'rgb(0,188,255)'],
                                                 [0.12, 'rgb(0,0,255)'], [0.5, 'rgb(213,0,255)'], [1, 'rgb(255,0,26)']],
                         hover_data=['count'], color='count', title="Number of waves by country",
                         labels={"count": "Waves number"}
                         )
    map2.update_layout(title={
        'x': 0.5,
        'xanchor': 'center'
    })
    map2.update_geos(showcountries=True,
                     countrycolor="black"
                     )
    map2.update_layout(margin={'r': 50, 't': 50, 'l': 50, 'b': 50, 'pad': 0},
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)')
    return map2


def wave_height_japan():
    japan = waves_df.loc[waves_df['country_w'] == 'JAPAN']
    japan = japan.replace(r'^\s*$', np.nan, regex=True)
    height_state_japan = pd.DataFrame(
        {"state": japan["state_w"], "max_height": japan["max_height_w"].astype(float),
         "latitude": japan["latitude_w"].astype(float),
         "longitude": japan["longitude_w"].astype(float)}).groupby('state').mean().dropna()

    fig = px.scatter_mapbox(height_state_japan, lat="latitude", lon="longitude",
                            hover_name=height_state_japan.index, hover_data=["max_height"],
                            color="max_height", size="max_height",
                            color_continuous_scale=px.colors.cyclical.IceFire, size_max=50, zoom=3)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


def distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat1 - lat2
    dlon = lon1 - lon2
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    distance = 6371 * c
    return distance


def waves_source_distance():
    waves_place = waves_df[['id_s', 'latitude_w', 'longitude_w']]
    source = sources_df[['id_s', 'latitude_s', 'longitude_s']]
    waves_place = pd.merge(source, waves_place, on='id_s')
    waves_place = waves_place.replace(r'^\s*$', np.nan, regex=True).dropna()
    waves_place['distance'] = distance(waves_place['latitude_s'].astype(float),
                                       waves_place['longitude_s'].astype(float),
                                       waves_place['latitude_w'].astype(float),
                                       waves_place['longitude_w'].astype(float))
    waves_place.dropna()
    bins = []
    for i in range(0, 500, 100):
        bins.append(i)
    for i in range(501, int(waves_place['distance'].mean()), 300):
        bins.append(i)

    for i in range(int(waves_place['distance'].mean()) + 1, int(waves_place['distance'].max()) + 1000, 1000):
        bins.append(i)
    fig = pd.cut(waves_place["distance"], bins=bins)
    fig.value_counts(sort=False).plot.bar(color='blue')
    plt.xticks(fontsize=7, rotation=90)
    plt.title("Wave distance from the source")
    plt.xlabel("Distance")
    plt.ylabel("Waves amount")
    plt.tight_layout()
    plt.show()


def height_magnitude():
    source_magnitude = sources_df[['id_s', 'primary_magnitude_s']].replace(r'^\s*$', np.nan,
                                                                           regex=True).dropna().astype(float).groupby(
        "id_s").sum()
    wave_height = waves_df[["id_s", 'max_height_w']].replace(r'^\s*$', np.nan, regex=True).dropna().astype(
        float).groupby('id_s').mean()
    magnitude_height = pd.concat([source_magnitude["primary_magnitude_s"], wave_height['max_height_w']],
                                 axis=1).dropna() \
        .groupby('primary_magnitude_s').mean().reset_index()
    x, y = magnitude_height["primary_magnitude_s"], magnitude_height["max_height_w"]

    plt.plot(x, y, 'o', color="red", label="maximum wave height for magnitude")
    m, b = np.polyfit(x, y, 1)
    f = lambda x: m * x + b
    x = np.array([0, 10])
    plt.plot(x, f(x), color="blue", label="regression line")
    plt.xticks(range(0, 10, 1))
    plt.legend()
    plt.show()


def waves_source(a: int):
    sources_by_year = pd.DataFrame({'year': sources_df['year_s'].sort_index()}).set_index(sources_df['id_s'])
    sources_by_year["count_waves"] = waves_df["id_s"].value_counts()
    sources_by_year["count_year"] = 1
    table = pd.DataFrame({"year": sources_by_year["year"].astype(int), "count_waves": sources_by_year["count_waves"],
                          "count_sources": sources_by_year["count_year"]}).groupby("year").sum().sort_values('year')

    table['mean'] = table["count_waves"] / table["count_sources"]
    table["year"] = table.index
    table['year'] = table['year'].replace(r'^\s*$', np.nan, regex=True).dropna().astype(float)
    table = table.tail(a)

    table.plot(x="year", y="mean")
    plt.title("Average waves amount caused by source in last " + str(a) + " years")
    plt.xlabel("Year")
    plt.ylabel("Number of waves")
    plt.xticks(range(min(table["year"].astype(int)), max(table["year"].astype(int)) + 4, int(a / 4)))
    plt.xticks(rotation=90)
    plt.show()


def source_country():
    source_countries = pd.DataFrame({"id_s": waves_df["id_s"].astype(float), "country": waves_df["country_w"]})
    dict = source_countries.groupby("id_s")[["country"]].apply(lambda g: g.values.tolist()).to_dict()
    for key in dict:
        list = dict[key]
        unique = []
        for i in list:
            if i in unique:
                continue
            else:
                unique.append(i)
        dict[key] = unique
        dict[key] = len(dict[key])
    source_countries_count = pd.DataFrame(dict.items(), columns=["id_s", "country_count"]).sort_values("country_count")
    source_countries_count = source_countries_count[source_countries_count["country_count"] != 1]
    source_countries_count.to_csv("SOURCE_COUNTRY_VALUE.csv")
    last_sources = pd.DataFrame({"id_s": sources_df["id_s"], "longitude": sources_df["longitude_s"],
                                 "latitude": sources_df["latitude_s"]}).replace(r'^\s*$', np.nan,
                                                                                regex=True).dropna().astype(float)

    last_sources = source_countries_count.merge(last_sources, on="id_s")
    fig = px.scatter_geo(last_sources, lon="longitude", lat="latitude", color='country_count', hover_name="id_s",
                         size="country_count", title="Sources of waves in more then one country")
    fig.update_layout(title={
        'x': 0.5,
        'xanchor': 'center'
    })
    return fig


def des_houses():
    house_source = pd.DataFrame(
        sources_df[['id_s', 'house_damaged_s', 'house_destroyed_s']].replace(r'^\s*$', np.nan, regex=True).astype(
            float))
    houses_waves = pd.DataFrame(
        waves_df[['id_s', 'house_damaged_w', 'house_destroyed_w']].replace(r'^\s*$', np.nan, regex=True).astype(
            float).groupby('id_s').sum()).reset_index()
    houses_all = house_source.merge(houses_waves, on='id_s')
    houses_all["all"] = houses_all.iloc[:, -4:].sum(axis=1)
    houses_all = houses_all[houses_all["all"] != 0].sort_values("all").reset_index()
    houses_all = houses_all[['id_s', 'all']]
    houses_all.to_csv('ALL_HOUSES_DAMAGE_OR_DESTROYED.csv')


def waves_month_day():
    months = pd.DataFrame(waves_df[['id_s', 'month_w', 'day_w']]).replace(r'^\s*$', np.nan, regex=True).dropna()
    month_list = []
    for i in range(1, 13):
        month_list.append(i)
    day_list = []
    for i in range(1, 32):
        day_list.append(i)
    pomka = pd.DataFrame(day_list, columns=['Day'])
    for m in month_list:
        b_list = []
        a = months[months['month_w'].astype(int) == m]
        for d in day_list:
            b = a[a['day_w'].astype(int) == d]
            b_list.append(b['id_s'].count())
        pomka[m] = b_list

    pomka.loc[len(pomka)] = 0
    pomka = pomka.shift()
    pomka.loc[0] = ""
    pomka = pomka.rename(columns={"Day": "Month"})
    pomka.at[0, 'Month'] = "Day"
    pomka.to_csv('WAVES_BY_EVERY_MONTH_DAY.CSV')


def waves_month():
    months = pd.DataFrame(waves_df[['id_s', 'month_w']]).replace(r'^\s*$', np.nan, regex=True).dropna()
    months["count"] = 1
    months = months.groupby('month_w').sum().reset_index().astype(int).sort_values("month_w")
    month = ['January', 'February', 'March', 'April', 'May', "June", "July", 'August', 'September', 'October',
             'November', 'December']
    plt.bar(month, months['count'], color='blue')
    plt.xlabel("Month")
    plt.ylabel("Number of waves")
    plt.xticks(fontsize=7, rotation=90)
    plt.tight_layout()
    plt.show()

def source_validity_century():
    global fig
    source = pd.DataFrame(sources_df[['year_s', 'validity_s']])
    source['count'] = 1
    source = source.replace(r'^\s*$', np.nan, regex=True).dropna().astype(int)
    source_bar  = source.replace(r'^\s*$', np.nan, regex=True).astype(float)
    source_bar = source_bar.groupby(['year_s', 'validity_s']).sum().reset_index()
    source_bar = source_bar[source_bar['year_s'] > 1000]
    list = []
    for j in range(0, len(source_bar.year_s), 1):
        a = source_bar.iloc[j]['year_s']
        for i in range(0, 2200, 100):
            if (a<=i) and (a>i-100):
                list.append(i/100)

    source_bar['year_s'] = list
    source_bar = source_bar.sort_values('year_s')
    source_bar =source_bar.groupby(['year_s', 'validity_s']).sum().reset_index()
    century =[]
    validity =[]
    for i in range(11, 22,1 ):
        century.append(i)
    for i in range(-1, 5 ,1):
        validity.append(i)
    for i in century:
        list = []
        for j in range(0, len(source_bar.year_s), 1):
                a = source_bar.iloc[j]['year_s']
                if a == i:
                    list.append(source_bar.iloc[j]['count'])
        if(i==11):
            fig = go.Figure(go.Bar(x=validity, y=list, name=str(i)), layout=go.Layout(title= go.layout.Title(text="Source by validity and century")))
        else:
            fig.add_trace(go.Bar(x=validity, y=list, name=str(i)))
    fig.update_layout(barmode='stack')
    fig.update_xaxes(categoryorder='category ascending')
    return fig


# map_source_country()
# map_waves_country()
# wave_height_japan()
# waves_source_distance()
# height_magnitude()
# waves_source(10)
# source_country()
# des_houses()
# waves_month_day()
# waves_month()
#source_validity_century()