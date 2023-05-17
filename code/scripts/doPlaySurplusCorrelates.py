import sys
import pandas as pd
import plotly.graph_objects as go

def plot_counts(group_col, unique_count_col, counts_by_group,
                fig_filename_pattern):
    fig = go.Figure()
    for i, count_col_item in enumerate(unique_count_col):
        trace = go.Bar(x=counts_by_group[i].index, y=counts_by_group[i],
                       name=unique_count_col[i])
        fig.add_trace(trace)
    fig.update_layout(
        xaxis_title=group_col,
        yaxis_title="Count",
    )
    fig.write_image(fig_filename_pattern.format("png"))
    fig.write_html(fig_filename_pattern.format("html"))


def get_counts_by_group(count_col, group_col, df):
    unique_count_col = df[count_col].unique()
    counts_by_group = [float("nan")] * len(unique_count_col)

    # counts by group
    for i, count_col_item in enumerate(unique_count_col):
        df_item_subset = df.loc[df[count_col] == count_col_item]
        counts_by_group[i] = df_item_subset.groupby([group_col])[count_col].count()
    return unique_count_col, counts_by_group


def main(argv):
    # read data
    data_filename = "../../../data/Surplus model data 05.01.22.csv"
    df = pd.read_csv(data_filename)

    count_col = "Surplus/Not Surplus"
    group_cols = ["Research Group", "Sex", "Age (w)", "Mutation 1",
                  "Mutation 2", "Mutation 2"]

    for group_col in group_cols:
        # get counts
        unique_count_col, counts_by_group = get_counts_by_group(
            count_col=count_col, group_col=group_col, df=df)

        # plot
        group_col_no_special_chars = group_col.replace(" ", "_").\
            replace("(", "_").replace(")", "_")
        fig_filename_pattern = f"../../figures/surplus_by_{group_col_no_special_chars}." "{:s}"
        plot_counts(group_col=group_col, unique_count_col=unique_count_col,
                    counts_by_group=counts_by_group,
                    fig_filename_pattern=fig_filename_pattern)

    breakpoint()

if __name__ == "__main__":
    main(sys.argv)
