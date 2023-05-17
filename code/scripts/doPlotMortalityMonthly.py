
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
    parser.add_argument("--start_date", help="start of analysis date", default="01/06/2020")
    parser.add_argument("--end_date", help="end of analysis date", default="16/12/2021")
    parser.add_argument("--data_filename", help="data filename",
                        default="../../../data/mortalityRatesIncludingImportsAndExports16.12.21.csv")
    parser.add_argument("--fig_filename_pattern",
                        help="figure filename_pattern",
                        default="../../figures/mortalityMonthly.{:s}")

    args = parser.parse_args()
    min_age = args.min_age
    max_age = args.max_age
    start_date = datetime.datetime.strptime(args.start_date, "%d/%m/%Y")
    end_date = datetime.datetime.strptime(args.end_date, "%d/%m/%Y")
    data_filename = args.data_filename
    fig_filename_pattern = args.fig_filename_pattern

    data = pd.read_csv(data_filename, parse_dates=["DOB", "Sacrifice date", "Import date", "Export date"], dayfirst=True)
    data = data.rename(columns={"Age (w)": "Age"})
    dates = pd.date_range(start_date, end_date, freq='MS')

    colony_size = [None]*(len(dates)-1)
    period_deaths = [None]*(len(dates)-1)
    assert len(dates)>1
    for i in range(len(dates)-1):
        min_date = dates[i]
        max_date = dates[i+1]
        alive_subset = data.query('(@min_age<=`Age`) and (`Age`<=@max_age) and (DOB<@min_date) and ((`Import date`<@min_date) or (`Import date`!=`Import date`)) and ((`Export date`>@max_date) or (`Export date`!=`Export date`)) and ((`Sacrifice date`>@max_date) | (`Sacrifice date`!=`Sacrifice date`))')
        colony_size[i] = alive_subset.shape[0]
        foundDead_subset = data.query('(`Sacrifice date`>=@min_date) and (`Sacrifice date`<=@max_date) and (`Sacrifice reason`=="Found dead")')
        period_deaths[i] = foundDead_subset.shape[0]

    period_mortality_rate = np.array(period_deaths, dtype=np.double)/np.array(colony_size)
    month_names = [date.strftime("%B") for date in dates[:-1]]

    colony_size_np = np.array(colony_size)
    period_deaths_np = np.array(period_deaths)
    period_mortality_rate_np = np.array(period_mortality_rate)
    titles = [
        "mean: {:.02f}, std: {:.02f}".format(
                  colony_size_np.mean(), colony_size_np.std()),
        "mean: {:.02f}, std: {:.02f}".format(
                  period_deaths_np.mean(), period_deaths_np.std()),
        "mean: {:.06f}, std: {:.06f}".format(
                  period_mortality_rate_np.mean(),
                  period_mortality_rate_np.std())
             ]

    fig = plotly.subplots.make_subplots(rows=3, cols=1, shared_xaxes=True,
                                       subplot_titles=titles)

    trace_colonySize = go.Scatter(x=dates[:-1], y=colony_size,
                                  name="colony size",
                                  mode="lines+markers")
    trace_periodDeaths = go.Scatter(x=dates[:-1], y=period_deaths,
                                   name="period deaths", mode="lines+markers")
    trace_period_mortality_rate = go.Scatter(x=dates[:-1],
                                             y=period_mortality_rate,
                                             name="period mortality rate",
                                             mode="lines+markers")
    fig.add_trace(trace_colonySize, row=1, col=1)
    fig.add_trace(trace_periodDeaths, row=2, col=1)
    fig.add_trace(trace_period_mortality_rate, row=3, col=1)
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
