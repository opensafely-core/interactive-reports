import argparse

import pandas as pd
import seaborn as sns
from report_utils import deciles_chart, plot_measures


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", help="output directory", required=True)
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    sns.set_style("darkgrid")

    df = pd.read_csv(
        f"{ args.output_dir }/joined/measure_all.csv", parse_dates=["date"]
    )
    breakdowns = df["group"].unique().tolist()
    breakdowns = [
        b
        for b in breakdowns
        if b not in ("total", "practice", "event_1_code", "event_2_code")
    ]

    df = df.loc[df["value"] != "[Redacted]", :]
    df["value"] = df["value"].astype(float)

    df_total = df.loc[df["group"] == "total", :]

    if not df_total.empty:
        plot_measures(
            df_total,
            filename=f"{ args.output_dir }/plot_measures",
            column_to_plot="value",
            y_label="Rate per 1000",
            category=None,
        )

    for breakdown in breakdowns:
        df_subset = df.loc[df["group"] == breakdown, :]

        if breakdown == "imd":
            plot_measures(
                df_subset,
                filename=f"{ args.output_dir }/plot_measures_{breakdown}",
                column_to_plot="value",
                y_label="Rate per 1000",
                category="group_value",
                category_order=[
                    "Most deprived",
                    "2",
                    "3",
                    "4",
                    "Least deprived",
                ],
            )

        elif breakdown == "age":
            plot_measures(
                df_subset,
                filename=f"{ args.output_dir }/plot_measures_{breakdown}",
                column_to_plot="value",
                y_label="Rate per 1000",
                category="group_value",
                category_order=[
                    "0-5",
                    "6-10",
                    "11-17",
                    "0-17",
                    "18-29",
                    "30-39",
                    "40-49",
                    "50-59",
                    "60-69",
                    "70-79",
                    "80+",
                ],
            )

        else:
            plot_measures(
                df_subset,
                filename=f"{ args.output_dir }/plot_measures_{breakdown}",
                column_to_plot="value",
                y_label="Rate per 1000",
                category="group_value",
            )

    practice_df = pd.read_csv(
        f"{ args.output_dir }/joined/measure_practice_rate_deciles.csv",
        parse_dates=["date"],
    )
    deciles_chart(
        practice_df,
        f"{ args.output_dir }/deciles_chart.png",
        period_column="date",
        column="value",
        ylabel="rate per 1000",
    )


if __name__ == "__main__":
    main()
