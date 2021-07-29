import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def count_na(x):
    return x.isna().sum()


def plot_hist_precipitaciones(df, region=None, ax=None):
    if region:
        df = df.query('region == @region')
    sns.histplot(data=df, x="precipitaciones", ax=ax)


def plot_line_precipitaciones(df, region=None, desde=None, hasta=None, ax=None):
    """ Validamos por separado la combinación destino/desde y destino/hasta porque
    puede darse que exista un extremo pero no el otro"""
    valid_query_from = any((df.region == region) &
                           (df.date == desde))
    valid_query_to = any((df.region == region) &
                         (df.date == hasta))

    if not ((valid_query_from + valid_query_to) == 2):
        print("La región o fechas no son válidas")
    else:
        df = df.query(
            'region==@region and date >= @desde and date <= @hasta').sort_values('date')
        sns.lineplot(data=df, x='date', y='precipitaciones', ax=ax)
        ax.set_title(region)
        max_tick = max(ax.get_xticks())
        ax.set_xticks(
            range(0, max_tick + 1, round(max_tick * 0.05)))


def plot_precipitaciones_mensuales(df, region=None, years=None, ax=None):
    """ Validamos por separado la combinación destino/desde y destino/hasta porque
    puede darse que exista un extremo pero no el otro"""
    year0 = years[0]
    year1 = years[1]
    df['year'] = [int(x[0]) for x in df['date'].str.split("-")]
    df['month'] = [int(x[1]) for x in df['date'].str.split("-")]

    valid_query_from = any((df.region == region) &
                           (df.year == year0))
    valid_query_to = any((df.region == region) &
                         (df.year == year1))

    if not ((valid_query_from + valid_query_to) == 2):
        print("La región o fechas no son válidas")
    else:
        df = df.query(
            'region==@region and year in @years').sort_values('date')
        sns.lineplot(data=df, x='month',
                     y='precipitaciones', hue='year', palette="Reds", ax=ax)
        ax.set_title(region)
        ax.set_xticklabels(['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'])


def plot_pbi(df, series, desde, hasta, ax=None):
    df = df.query(
        'variable in @series and Periodo >= @desde and Periodo <= @hasta').sort_values('Periodo')

    sns.lineplot(data=df, x="Periodo", y="valor", hue="variable", ax=ax)
    ax.set_title(series)
