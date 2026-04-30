import marimo

__generated_with = "0.23.4"
app = marimo.App(width="medium", auto_download=["ipynb", "html"])

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
    # 第 2 章: 小売店のデータでデータ加工を行う 10 本ノック
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 11: データを読み込んでみよう
    """)
    return


@app.cell
def _():
    uriage_data1 = polars.read_csv(Path.cwd() / "data" / "2章" / "uriage.csv")

    uriage_data1.head()
    return (uriage_data1,)


@app.cell
def _():
    kokyaku_data1 = polars.read_excel(Path.cwd() / "data" / "2章" / "kokyaku_daicho.xlsx")

    kokyaku_data1.head()
    return (kokyaku_data1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 12: データの揺れを見てみよう
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### データの揺れ: 商品名
    """)
    return


@app.cell
def _(uriage_data1):
    uriage_data1["item_name"].head(n=5)
    return


@app.cell
def _(uriage_data1):
    _s = uriage_data1["item_name"].unique()
    _s.filter(_s.str.contains(r"[Aa]"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### データの揺れ: 商品金額
    """)
    return


@app.cell
def _(uriage_data1):
    uriage_data1["item_price"].head(n=5)
    return


@app.cell
def _(uriage_data1):
    uriage_data1["item_price"].describe()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 13: データに揺れがあるまま集計してみよう
    """)
    return


@app.cell
def _(uriage_data1):
    uriage_data2 = uriage_data1.with_columns(
        polars.col("purchase_date").str.to_datetime().alias("purchase_date")
    ).with_columns(
        (
            polars.col("purchase_date").dt.year() * 100
            + polars.col("purchase_date").dt.month()
        ).alias("purchase_month")
    )

    uriage_data2
    return (uriage_data2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### データ補正前の集計結果 (商品毎)
    """)
    return


@app.cell
def _(uriage_data2):
    uriage_data2.select(["purchase_month", "item_name"]).pivot(
        index="purchase_month",
        on="item_name",
        values=["item_name"],
        aggregate_function=polars.len(),
    ).sort("purchase_month")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### データ補正前の集計結果 (金額)
    """)
    return


@app.cell
def _(uriage_data2):
    uriage_data2.select(["purchase_month", "item_name", "item_price"]).pivot(
        index="purchase_month",
        on="item_name",
        values=["item_price"],
        aggregate_function=polars.element().sum(),
    ).sort("purchase_month")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 14: 商品名の揺れを補正しよう
    """)
    return


@app.cell
def _(uriage_data2):
    uriage_data2["item_name"].unique().len()
    return


@app.cell
def _(uriage_data2):
    uriage_data3 = uriage_data2.with_columns(
        polars.col("item_name").str.to_uppercase().str.replace_all(" ", "").str.replace_all("　", "")
    ).sort("item_name")

    uriage_data3
    return (uriage_data3,)


@app.cell
def _(uriage_data3):
    print(uriage_data3["item_name"].unique())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 15: 金額欠損値の補完をしよう
    """)
    return


@app.cell
def _(uriage_data3):
    uriage_data3.null_count()
    return


@app.cell
def _(uriage_data3):
    _name_to_price: dict[str, int] = {}
    for _row in uriage_data3.iter_rows(named=True):
        if _row["item_price"] is not None:
            _name_to_price[_row["item_name"]] = _row["item_price"]

    _item_price_df = polars.DataFrame(
        {
            "item_name": list(_name_to_price.keys()),
            "item_price": list(_name_to_price.values()),
        }
    )

    uriage_data4 = uriage_data3.drop("item_price").join(_item_price_df, on="item_name", how="left")

    uriage_data4.head()
    return (uriage_data4,)


@app.cell
def _(uriage_data4):
    uriage_data4.null_count()
    return


@app.cell
def _(uriage_data4):
    for _trg in uriage_data4["item_name"].unique().sort():
        print(f"{_trg}", end=": ")
        print(f"最大額: {uriage_data4.filter(polars.col('item_name') == _trg)['item_price'].max()}", end=", ")
        print(f"最小額: {uriage_data4.filter(polars.col('item_name') == _trg)['item_price'].min()}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 16: 顧客名の揺れを補正しよう
    """)
    return


@app.cell
def _(kokyaku_data1):
    kokyaku_data1["顧客名"].head()
    return


@app.cell
def _(uriage_data4):
    uriage_data4["customer_name"].head()
    return


@app.cell
def _(kokyaku_data1):
    kokyaku_data2 = kokyaku_data1.with_columns(
        polars.col("顧客名").str.replace_all(" ", "").str.replace("　", "")
    )

    kokyaku_data2["顧客名"].head()
    return (kokyaku_data2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 17 日付の揺れを補正しよう
    """)
    return


@app.cell
def _(kokyaku_data2):
    kokyaku_data2["登録日"].head()
    return


@app.cell
def _(kokyaku_data2):
    kokyaku_data2.filter(
        polars.col("登録日").str.contains(r"^\d+$")
    )["登録日"].len()
    return


@app.cell
def _(kokyaku_data2):
    kokyaku_data2.filter(
        polars.col("登録日").str.contains(r"^\d+$")
    ).with_columns(
        (
            polars.duration(days=polars.col("登録日").cast(polars.Int64) - 2)
            + polars.date(year=1900, month=1, day=1)
        ).alias("登録日")
    )["登録日"].head()
    return


@app.cell
def _(kokyaku_data2):
    kokyaku_data3 = kokyaku_data2.with_columns(
        polars.when(polars.col("登録日").str.contains(r"^\d+$"))
            .then(
                polars.duration(days=polars.col("登録日").cast(polars.Int64, strict=False) - 2)
                + polars.date(year=1900, month=1, day=1)
            )
            .otherwise(polars.col("登録日").str.to_date(strict=False))
            .alias("登録日")
    )

    kokyaku_data3.head()
    return (kokyaku_data3,)


@app.cell
def _(kokyaku_data3):
    kokyaku_data4 = kokyaku_data3.with_columns(
        (polars.col("登録日").dt.year() * 100 + polars.col("登録日").dt.month()).alias("登録年月")
    )

    kokyaku_data4.head()
    return (kokyaku_data4,)


@app.cell
def _(kokyaku_data4):
    _result = kokyaku_data4.sort(by="登録年月").group_by("登録年月").len()

    print(f"{len(kokyaku_data4)=}, {_result['len'].sum()=}")

    _result
    return


@app.cell
def _(kokyaku_data4):
    kokyaku_data4.filter(polars.col("登録日").cast(polars.String).str.contains(r"^\d+$"))["登録日"].len()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 18: 顧客名をキーに 2 つのデータを結合 (ジョイン) しよう
    """)
    return


@app.cell
def _(kokyaku_data4, uriage_data4):
    join_data = uriage_data4.join(
        kokyaku_data4,
        left_on="customer_name",
        right_on="顧客名",
        how="left"
    ).rename(
        { "customer_name": "顧客名" }
    ).select(["purchase_date", "item_name", "purchase_month", "item_price", "顧客名", "かな", "地域", "メールアドレス", "登録日", "登録年月"])

    join_data.head()
    return (join_data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 19: クレンジングしたデータをダンプしよう
    """)
    return


@app.cell
def _(join_data):
    dump_data = join_data.select(["purchase_date", "purchase_month", "item_name", "item_price", "顧客名", "かな", "地域", "メールアドレス", "登録日"])

    dump_data.head()
    return (dump_data,)


@app.cell
def _(dump_data):
    filename = Path.cwd() / "notebooks" / "02" / "dump_data.csv"
    filename.parent.mkdir(parents=True, exist_ok=True)

    dump_data.write_csv(filename)
    return (filename,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 20: データを集計しよう
    """)
    return


@app.cell
def _(filename):
    import_data = polars.read_csv(filename)

    import_data.head()
    return (import_data,)


@app.function
def my_heatmap(_df: polars.DataFrame, x_axis: str, y_axis: str, value: str) -> altair.Chart:
    return altair.Chart(_df).mark_rect().encode(
        x=altair.X(field=x_axis, type='nominal'),
        y=altair.Y(field=y_axis, type='nominal'),
        color=altair.Color(field=value, type='quantitative'),
        tooltip=[
            altair.Tooltip(field=x_axis),
            altair.Tooltip(field=y_axis, format=',.0f'),
            altair.Tooltip(field=value, format=',.0f')
        ]
    ).properties(
        height=290,
        width='container',
        config={
            'axis': {
                'grid': False
            }
        }
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 購入年月・商品の集計結果
    """)
    return


@app.cell
def _(import_data):
    by_item = import_data.group_by(["purchase_month", "item_name"]).len().pivot(
        on="item_name",
        # on_columns=import_data["item_name"].unique().sort(),
        index="purchase_month",
        sort_columns=True,
    ).sort("purchase_month")

    by_item
    return


@app.cell
def _(import_data):
    my_heatmap(
        import_data.group_by(["purchase_month", "item_name"]).len().sort(["purchase_month", "item_name"]),
        x_axis="item_name",
        y_axis="purchase_month",
        value="len",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 購入年月・売上金額の集計結果
    """)
    return


@app.cell
def _(import_data):
    by_price = import_data.group_by(["purchase_month", "item_name"]).agg(
        polars.col("item_price").sum()
    ).pivot(
        on="item_name",
        index="purchase_month",
        sort_columns=True,
    ).sort("purchase_month")

    by_price
    return


@app.cell
def _(import_data):
    my_heatmap(
        import_data.group_by(["purchase_month", "item_name"]).agg(
            polars.col("item_price").sum()
        ).sort(["purchase_month", "item_name"]),
        x_axis="item_name",
        y_axis="purchase_month",
        value="item_price",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 購入年月・各顧客の購入数の集計結果
    """)
    return


@app.cell
def _(import_data):
    by_customer = import_data.group_by(["purchase_month", "顧客名"]).len().pivot(
        on="顧客名",
        index="purchase_month",
        sort_columns=True,
    ).sort("purchase_month")

    by_customer
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 購入年月・地域における販売数の集計結果
    """)
    return


@app.cell
def _(import_data):
    by_region = import_data.group_by(["purchase_month", "地域"]).len().pivot(
        on="地域",
        index="purchase_month",
        sort_columns=True,
    ).sort("purchase_month")

    by_region
    return


@app.cell
def _(import_data):
    my_heatmap(
        import_data.group_by(["purchase_month", "地域"]).len(),
        x_axis="地域",
        y_axis="purchase_month",
        value="len",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 集計期間内での離脱顧客
    """)
    return


@app.cell
def _(kokyaku_data4, uriage_data4):
    uriage_data4.join(
        kokyaku_data4,
        left_on="customer_name",
        right_on="顧客名",
        how="right",
    ).filter(
        polars.any_horizontal(polars.all().is_null())
    ).select(
        ["顧客名", "メールアドレス", "登録日"]
    )
    return


if __name__ == "__main__":
    app.run()
