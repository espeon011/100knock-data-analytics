import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium", auto_download=["ipynb", "html"])


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 朝練
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 朝練 1: Google Colaboratory を使ってみよう
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ローカルで marimo を使っているので省略.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 朝練 2: プログラムを書いて実行してみよう
    """)
    return


@app.cell
def _():
    print("Hello World")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 朝練 3: 変数を使ってみよう
    """)
    return


@app.cell
def _():
    _a = 10
    _b = 20

    _c = _a * _b
    _c
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 朝練 4: ライブラリを使ってみよう
    """)
    return


@app.cell
def _():
    import numpy as np

    return (np,)


@app.cell
def _(np):
    _a = np.array([1, 2, 3])
    _a
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 朝練 5: コードセルを分けて効率よくプログラミングをしよう
    """)
    return


@app.cell
def _(np):
    a = np.array([1, 2, 3])
    return (a,)


@app.cell
def _(a):
    a
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 朝練 6: 本書のサンプルプログラムを Google Colaboratory で動かしてみよう
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Google Drive との接続を省略してデータの読み込みだけ行う.
    """)
    return


@app.cell
def _():
    import polars as pl

    return (pl,)


@app.cell
def _(pl):
    file = "./data/朝練/height_data.csv"
    df = pl.read_csv(file)
    return (df,)


@app.cell
def _(df):
    df.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 朝練 7: Google Drive からデータを参照してみよう
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ローカルで実行しているので省略.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 朝練 8: 絶対パスと相対パスについて
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    スキップ.
    """)
    return


if __name__ == "__main__":
    app.run()
