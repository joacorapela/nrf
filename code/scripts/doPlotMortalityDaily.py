
import pdb
import sys
import argparse
import datetime
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.subplots

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--min_age", help="mininmum age in weeks", type=int, default=3)
    parser.add_argument("--max_age", help="maxinmum age in weeks", type=int, default=52)
    parser.add_argument("--start_date", help="start date", default="01/06/2020")
    parser.add_argument("--end_date", help="start date", default="16/12/2021")
    parser.add_argument("--data_filename", help="data filename",
                        default="../../../data/mortalityRatesIncludingImportsAndExports16.12.21.csv")
    parser.add_argument("--fig_filename_pattern",
                        help="figure filename_pattern",
                        default="../../figures/mortalityDaily.{:s}")

    args = parser.parse_args()
    min_age = args.min_age
    max_age = args.max_age
    start_date = datetime.datetime.strptime(args.start_date, "%d/%m/%Y")
    end_date = datetime.datetime.strptime(args.end_date, "%d/%m/%Y")
    data_filename = args.data_filename
    fig_filename_pattern = args.fig_filename_pattern

    data = pd.read_csv(data_filename, parse_dates=["DOB", "Sacrifice date", "Import date", "Export date"], dayfirst=True)
    data = data.rename(columns={"Age (w)": "Age"})
    dates = pd.date_range(start_date, end_date, freq='d')

    colony_size = [None]*len(dates)
    daily_deaths = [None]*len(dates)
    for i, query_date in enumerate(dates):
        alive_subset = data.query('(@min_age<=`Age`) and (`Age`<=@max_age) and (DOB<@query_date) and ((`Import date`<@query_date) or (`Import date`!=`Import date`)) and ((`Export date`>@query_date) or (`Export date`!=`Export date`)) and ((`Sacrifice date`>@query_date) | (`Sacrifice date`!=`Sacrifice date`))')
        colony_size[i] = alive_subset.shape[0]
        foundDead_subset = data.query('(`Sacrifice date`==@query_date) and (`Sacrifice reason`=="Found dead")')
        daily_deaths[i] = foundDead_subset.shape[0]

    daily_mortality_rate = np.array(daily_deaths, dtype=np.double)/np.array(colony_size)

    fig = plotly.subplots.make_subplots(rows=3, cols=1, shared_xaxes=True)

    trace_colonySize = go.Scatter(x=dates, y=colony_size, name="colony size",
                                  mode="lines+markers")
    trace_dailyDeaths = go.Scatter(x=dates, y=daily_deaths,
                                   name="daily deaths", mode="lines+markers")
    trace_daily_mortality_rate = go.Scatter(x=dates, y=daily_mortality_rate,
                                            name="daily mortality rate",
                                            mode="lines+markers")
    fig.add_trace(trace_colonySize, row=1, col=1)
    fig.add_trace(trace_dailyDeaths, row=2, col=1)
    fig.add_trace(trace_daily_mortality_rate, row=3, col=1)
    fig.write_image(fig_filename_pattern.format("png"))
    fig.write_html(fig_filename_pattern.format("html"))

    # data_subset = data.query('(@min_age<=`Age (w)`) and (`Age (w)`<=@max_age) and (DOB<@query_date) and ((`Import date`<@query_date) or (`Import date`!=`Import date`)) and ((`Export date`>@query_date) or (`Export date`!=`Export date`)) and ((`Sacrifice date`>@query_date) | (`Sacrifice date`!=`Sacrifice date`))')
    # data_subset = data.query('(DOB>@query_date) and ((`Import date`>@query_date) or (`Import date`!=`Export date`))')
    # data_subset = data.query('(DOB>@query_date) & `Import date`>@query_date & `Export date`>@query_date & `Sacrifice date`>@query_date')
    # data_subset = data.query('(DOB>@query_date) & `Import date`>@query_date')
    # data_subset = data[(data["DOB"]>query_date) & (pd.isnull(data["Import date"]) | data["Import date"]>query_date) & (pd.isnull(data["Export date"]) | data["Export date"]>query_date) & (pd.isnull(data["Sacrifice date"]) | data["Sacrifice date"]>query_date)]
    # data_subset = data[(data["DOB"]>query_date) & (data["Import date"]>query_date) & (data["Export date"]>query_date)]
    pdb.set_trace()

if __name__=="__main__":
    main(sys.argv)
