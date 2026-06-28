import marimo

__generated_with = "0.23.4"
app = marimo.App(width="medium", auto_download=["ipynb"])

with app.setup:
    from pathlib import Path
    import polars
    import altair


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 第 3 章: 顧客の全体像を把握する 10 本ノック
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 21: データを読み込んで把握しよう
    """)
    return


@app.cell
def _():
    uselog = polars.read_csv("./data/3章/use_log.csv")
    print(f"{len(uselog)=}")
    uselog.head()
    return (uselog,)


@app.cell
def _():
    customer = polars.read_csv("./data/3章/customer_master.csv")
    print(f"{len(customer)=}")
    customer.head()
    return (customer,)


@app.cell
def _():
    class_master = polars.read_csv("./data/3章/class_master.csv")
    print(f"{len(class_master)=}")
    class_master.head()
    return (class_master,)


@app.cell
def _():
    campaign_master = polars.read_csv("./data/3章/campaign_master.csv")
    print(f"{len(campaign_master)=}")
    campaign_master.head()
    return (campaign_master,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 22: 顧客データを整形しよう
    """)
    return


@app.cell
def _(campaign_master, class_master, customer):
    customer_join = customer.join(
        class_master, on="class", how="left"
    ).join(
        campaign_master, on="campaign_id", how="left"
    )

    print(f"{len(customer)=}")
    print(f"{len(customer_join)=}")
    customer_join.head()
    return (customer_join,)


@app.cell
def _(customer_join):
    customer_join.null_count()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 23: 顧客データの基礎集計をしよう
    """)
    return


@app.cell
def _(customer_join):
    customer_join.group_by(["class_name"]).len()
    return


@app.cell
def _(customer_join):
    customer_join.group_by(["campaign_name"]).len()
    return


@app.cell
def _(customer_join):
    customer_join.group_by(["gender"]).len()
    return


@app.cell
def _(customer_join):
    customer_join.group_by(["is_deleted"]).len()
    return


@app.cell
def _(customer_join):
    customer_join1 = customer_join.with_columns(
        polars.col("start_date").str.to_datetime().dt.date().alias("start_date")
    ).with_columns(
        polars.col("end_date").str.to_datetime().dt.date().alias("end_date")
    )

    customer_join1.head()
    return (customer_join1,)


@app.cell
def _(customer_join1):
    _customer_start = customer_join1.filter(polars.col("start_date") > polars.date(2018, 4, 1))
    print(f"{len(_customer_start)=}")
    return


@app.cell
def _(customer_join1):
    _customer_end = customer_join1.filter(polars.col("end_date") > polars.date(2018, 4, 1))
    print(f"{len(_customer_end)=}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ノック 24: 最新顧客データの基礎集計をしてみよう
    """)
    return


@app.cell
def _(customer_join1):
    customer_newer = customer_join1.filter(
        polars.col("end_date").is_null() | (polars.col("end_date") >= polars.date(2019, 3, 31))
    )

    print(f"{len(customer_newer)=}")
    customer_newer["end_date"].unique()
    return (customer_newer,)


@app.cell
def _(customer_newer):
    customer_newer.group_by(["class_name"]).len()
    return


@app.cell
def _(customer_newer):
    customer_newer.group_by(["campaign_name"]).len()
    return


@app.cell
def _(customer_newer):
    customer_newer.group_by(["gender"]).len()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 25: 利用履歴データを集計しよう
    """)
    return


@app.cell
def _(uselog):
    uselog1 = uselog.with_columns(
        polars.col("usedate").str.to_date()
    ).with_columns(
        (polars.col("usedate").dt.year() * 100 + polars.col("usedate").dt.month()).alias("年月")
    )

    uselog1.head()
    return (uselog1,)


@app.cell
def _(uselog1):
    uselog_months = uselog1.group_by(["年月", "customer_id"]).len()

    uselog_months.head()
    return (uselog_months,)


@app.cell
def _(uselog_months):
    uselog_customer = uselog_months.group_by(["customer_id"]).agg(
        polars.col("len").mean().alias("mean"),
        polars.col("len").median().alias("median"),
        polars.col("len").min().alias("min"),
        polars.col("len").max().alias("max"),
    )

    uselog_customer.sort(by="customer_id").head()
    return (uselog_customer,)


@app.cell
def _(uselog_customer):
    uselog_customer.sort(by="mean", descending=True).head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 26: 利用履歴データから定期利用フラグを作成しよう
    """)
    return


@app.cell
def _(uselog1):
    uselog2 = uselog1.with_columns(
        polars.col("usedate").dt.weekday().alias("weekday")
    )

    uselog2
    return (uselog2,)


@app.cell
def _(uselog2):
    uselog_weekday = uselog2.group_by(["customer_id", "年月", "weekday"]).len()

    uselog_weekday.sort(by=["customer_id", "年月", "weekday"]).head()
    return (uselog_weekday,)


@app.cell
def _(uselog_weekday):
    uselog_weekday1 = uselog_weekday.group_by(["customer_id"]).max().select(
        ["customer_id", "len"]
    ).with_columns(
        (polars.col("len") >= 4).alias("routine_flg")
    )

    uselog_weekday1.sort(by="customer_id").head()
    return (uselog_weekday1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 27: 顧客データと利用履歴を結合しよう
    """)
    return


@app.cell
def _(customer_join1, uselog_customer, uselog_weekday1):
    customer_join2 = customer_join1.join(
        uselog_customer, on="customer_id", how="left"
    ).join(
        uselog_weekday1.select(["customer_id", "routine_flg"]), on="customer_id", how="left"
    )

    customer_join2.head()
    return (customer_join2,)


@app.cell
def _(customer_join2):
    customer_join2.null_count()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 28: 会員期間を計算しよう
    """)
    return


@app.cell
def _(customer_join2):
    customer_join3 = customer_join2.with_columns(
        polars.col("end_date").alias("calc_date").fill_null(polars.date(2019, 4, 30))
    ).with_columns(
        (
            (polars.col("calc_date") - polars.col("start_date")).dt.total_days()
        ).alias("membership_period")
    )

    customer_join3.head()
    return (customer_join3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 29: 顧客行動の各種統計量を把握しよう
    """)
    return


@app.cell
def _(customer_join3):
    customer_join3.select(["mean", "median", "min", "max"]).describe()
    return


@app.cell
def _(customer_join3):
    customer_join3.group_by(["routine_flg"]).len()
    return


@app.cell
def _(customer_join3):
    _ = customer_join3.with_columns((polars.col("membership_period") / 30).alias("membership_period_month"))
    altair.Chart(_).mark_bar().encode(
        altair.X("membership_period_month:Q", bin=True),
        y='count()',
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 30: 退会ユーザーと継続ユーザーの違いを把握しよう
    """)
    return


@app.cell
def _(customer_join3):
    customer_end = customer_join3.filter(polars.col("is_deleted") == 1)

    customer_end.describe()
    return


@app.cell
def _(customer_join3):
    customer_stay = customer_join3.filter(polars.col("is_deleted") == 0)

    customer_stay.describe()
    return


@app.cell
def _(customer_join3):
    _out_file = Path(".") / "notebooks" / "03" / "customer_join.csv"
    _out_file.parent.mkdir(parents=True, exist_ok=True)
    customer_join3.write_csv(_out_file)
    return


if __name__ == "__main__":
    app.run()
