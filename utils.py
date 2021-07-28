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
    valid_query_from = ((df.region.str.contains(region)) &
                        (df.date.str.contains(desde))).sum()
    valid_query_to = ((df.region.str.contains(region)) &
                      (df.date.str.contains(hasta))).sum()

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
