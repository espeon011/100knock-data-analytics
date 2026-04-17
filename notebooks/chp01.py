import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium", auto_download=["ipynb"])

with app.setup:
    import polars
    import altair
    import matplotlib.pyplot as plt


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 第 1 章: ウェブからの注文数を分析する 10 本ノック
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 1: データを読み込んでみよう
    """)
    return


@app.cell
def _():
    customer_master = polars.read_csv("./data/1章/customer_master.csv")
    customer_master.head()
    return (customer_master,)


@app.cell
def _():
    item_master = polars.read_csv("./data/1章/item_master.csv")
    item_master.head()
    return (item_master,)


@app.cell
def _():
    transaction_1 = polars.read_csv("./data/1章/transaction_1.csv")
    transaction_1.head()
    return (transaction_1,)


@app.cell
def _():
    transaction_detail_1 = polars.read_csv("./data/1章/transaction_detail_1.csv")
    transaction_detail_1.head()
    return (transaction_detail_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 2: データを結合 (ユニオン) してみよう
    """)
    return


@app.cell
def _(transaction_1):
    transaction_2 = polars.read_csv("./data/1章/transaction_2.csv")
    transaction = polars.concat([transaction_1, transaction_2])

    print(f"{len(transaction_1)=}")
    print(f"{len(transaction_2)=}")
    print(f"{len(transaction)=}")

    transaction.head()
    return (transaction,)


@app.cell
def _(transaction_detail_1):
    transaction_detail_2 = polars.read_csv("./data/1章/transaction_detail_2.csv")
    transaction_detail = polars.concat([transaction_detail_1, transaction_detail_2])

    print(f"{len(transaction_detail_1)=}")
    print(f"{len(transaction_detail_2)=}")
    print(f"{len(transaction_detail)=}")

    transaction_detail.head()
    return (transaction_detail,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 3: 売上データ同士を結合 (ジョイン) してみよう
    """)
    return


@app.cell
def _(transaction, transaction_detail):
    join_data1 = transaction_detail.join(
        transaction[["transaction_id", "payment_date", "customer_id"]],
        on="transaction_id",
        how="left",
    )

    print(f"{len(transaction_detail)=}")
    print(f"{len(transaction)=}")
    print(f"{len(join_data1)=}")

    join_data1.head()
    return (join_data1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 4: マスターデータを結合 (ジョイン) してみよう
    """)
    return


@app.cell
def _(customer_master, item_master, join_data1):
    join_data2 = join_data1.join(customer_master, on="customer_id", how="left").join(
        item_master, on="item_id", how="left"
    )

    join_data2.head()
    return (join_data2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 5: 必要なデータ列を作ろう
    """)
    return


@app.cell
def _(join_data2):
    join_data3 = join_data2.with_columns(
        (polars.col("quantity") * polars.col("item_price")).alias("price")
    )

    join_data3.select(["quantity", "item_price", "price"]).head()
    return (join_data3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 6: データ検算をしよう
    """)
    return


@app.cell
def _(join_data3, transaction):
    print(f"{join_data3["price"].sum()=}")
    print(f"{transaction["price"].sum()=}")
    assert join_data3["price"].sum() == transaction["price"].sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 7: 各種統計量を把握しよう
    """)
    return


@app.cell
def _(join_data3):
    join_data3.null_count()
    return


@app.cell
def _(join_data3):
    join_data3.select(["quantity", "age", "item_price", "price"]).describe()
    return


@app.cell
def _(join_data3):
    print(f"{join_data3['payment_date'].min()=}")
    print(f"{join_data3['payment_date'].max()=}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 8: 月別でデータを集計してみよう
    """)
    return


@app.cell
def _(join_data3):
    polars.DataFrame(
        {
            "header": join_data3.columns,
            "dtype": join_data3.dtypes,
        }
    )
    return


@app.cell
def _(join_data3):
    join_data4 = join_data3.with_columns(
        polars.col("payment_date").str.to_datetime().alias("payment_date")
    )
    join_data5 = join_data4.with_columns(
        (
            polars.col("payment_date").dt.year() * 100
            + polars.col("payment_date").dt.month()
        ).alias("payment_month")
    )

    join_data5.select(["payment_date", "payment_month"])
    return (join_data5,)


@app.cell
def _(join_data5):
    join_data5.group_by("payment_month").agg([polars.sum("price")])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 9: 月別, 商品別でデータを集計してみよう
    """)
    return


@app.cell
def _(join_data5):
    join_data5.group_by(["payment_month", "item_name"]).agg(
        [polars.sum("price"), polars.sum("quantity")]
    ).sort(["payment_month", "item_name"])
    return


@app.cell
def _(join_data5):
    join_data5.sort("payment_month").group_by(
        ["payment_month", "item_name"], maintain_order=True
    ).agg([polars.sum("price"), polars.sum("quantity")]).pivot(
        on="payment_month",
        index="item_name",
        values=["price", "quantity"],
    ).sort("item_name")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ノック 10: 商品別の売上推移を可視化してみよう
    """)
    return


@app.cell
def _(join_data5):
    graph_data = (
        join_data5.sort("item_name")
        .group_by(["payment_month", "item_name"], maintain_order=True)
        .agg(polars.sum("price"))
        .pivot(
            on="item_name",
            index="payment_month",
            values=["price"],
        )
        .sort("payment_month")
    )

    graph_data
    return (graph_data,)


@app.cell
def _(graph_data):
    for _col in graph_data.columns:
        if _col.startswith("PC-"):
            plt.plot(graph_data["payment_month"], graph_data[_col], label=_col)
    plt.legend()
    return


@app.cell
def _(graph_data, mo):
    for _col in graph_data.columns:
        if _col.startswith("PC-"):
            plt.plot(graph_data["payment_month"], graph_data[_col], label=_col)
    plt.legend()
    mo.ui.matplotlib(plt.gca())
    return


@app.cell
def _(join_data5):
    # graph_data2 = join_data5.sort("item_name").group_by(
    #     ["payment_month", "item_name"], maintain_order=True
    # ).agg(polars.sum("price"))
    graph_data2 = join_data5.group_by(["payment_month", "item_name"]).agg(
        polars.sum("price")
    )

    graph_data2
    return (graph_data2,)


@app.cell
def _(graph_data2):
    altair.Chart(graph_data2).mark_line().encode(
        x="payment_month:T", y="price:Q", color="item_name:N"
    )
    return


@app.cell
def _(graph_data2, mo):
    mo.ui.altair_chart(
        altair.Chart(graph_data2)
        .mark_line()
        .encode(x="payment_month:T", y="price:Q", color="item_name:N")
    )
    return


if __name__ == "__main__":
    app.run()
