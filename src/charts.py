"""負責使用 Plotly 繪製互動式資料分析圖表的模組。"""

from typing import Optional
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class ChartError(Exception):
    """當圖表參數無效或欄位不存在時拋出的自訂例外。"""


def _validate_column(df: pd.DataFrame, column: str) -> None:
    """檢查欄位是否存在於 DataFrame 中。"""
    if column not in df.columns:
        raise ChartError(f"找不到指定的欄位：「{column}」。")


def create_histogram(
    df: pd.DataFrame,
    column: str,
    bins: int = 20,
) -> go.Figure:
    """繪製單一數值欄位的直方圖 (Histogram)。

    Args:
        df: 資料來源 DataFrame。
        column: 要繪製的數值欄位名稱。
        bins: 直方圖的分箱數量，預設為 20。

    Returns:
        Plotly Figure 物件。
    """
    _validate_column(df, column)
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ChartError(f"欄位「{column}」不是數值型態，無法繪製直方圖。")

    fig = px.histogram(
        df,
        x=column,
        nbins=bins,
        title=f"「{column}」數值分佈直方圖",
        labels={column: column},
         marginal="box",
    )
    fig.update_layout(yaxis_title="筆數 (Count)", bargap=0.05)
    return fig


def create_box_plot(
    df: pd.DataFrame,
    y_column: str,
    x_column: Optional[str] = None,
) -> go.Figure:
    """繪製數值欄位的盒鬚圖 (Box Plot)，可選擇性依類別欄位分組比較。

    Args:
        df: 資料來源 DataFrame。
        y_column: 要觀察分佈的數值欄位名稱。
        x_column: 選擇性的分組類別欄位名稱。

    Returns:
        Plotly Figure 物件。
    """
    _validate_column(df, y_column)
    if not pd.api.types.is_numeric_dtype(df[y_column]):
        raise ChartError(f"欄位「{y_column}」不是數值型態，無法繪製盒鬚圖。")

    if x_column is not None:
        _validate_column(df, x_column)
        title = f"依「{x_column}」分組的「{y_column}」盒鬚圖"
    else:
        title = f"「{y_column}」盒鬚圖"

    fig = px.box(
        df,
        x=x_column,
        y=y_column,
        color=x_column,
        points="all",
        title=title,
    )
    return fig


def create_scatter_plot(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    color_column: Optional[str] = None,
    show_trendline: bool = False,
) -> go.Figure:
    """繪製兩個數值欄位的散佈圖 (Scatter Plot)，可選擇性疊加線性迴歸趨勢線。

    Args:
        df: 資料來源 DataFrame。
        x_column: X 軸數值欄位名稱。
        y_column: Y 軸數值欄位名稱。
        color_column: 選擇性的顏色分組欄位名稱。
        show_trendline: 是否使用最小平方法計算並繪製全體線性迴歸趨勢線 (y = ax + b)。

    Returns:
        Plotly Figure 物件。
    """
    _validate_column(df, x_column)
    _validate_column(df, y_column)
    if not pd.api.types.is_numeric_dtype(df[x_column]):
        raise ChartError(f"X 軸欄位「{x_column}」不是數值型態。")
    if not pd.api.types.is_numeric_dtype(df[y_column]):
        raise ChartError(f"Y 軸欄位「{y_column}」不是數值型態。")

    if color_column is not None:
        _validate_column(df, color_column)

    fig = px.scatter(
        df,
        x=x_column,
        y=y_column,
        color=color_column,
        title=f"「{x_column}」與「{y_column}」關係散佈圖",
    )

    if show_trendline:
        valid_df = df[[x_column, y_column]].dropna()
        if len(valid_df) >= 2 and valid_df[x_column].nunique() >= 2:
            x_vals = valid_df[x_column].to_numpy(dtype=float)
            y_vals = valid_df[y_column].to_numpy(dtype=float)
            slope, intercept = np.polyfit(x_vals, y_vals, 1)
            x_line = np.array([float(x_vals.min()), float(x_vals.max())])
            y_line = slope * x_line + intercept
            sign_str = "+" if intercept >= 0 else "-"
            trend_label = f"線性趨勢線 (y = {slope:.2f}x {sign_str} {abs(intercept):.2f})"
            fig.add_trace(
                go.Scatter(
                    x=x_line,
                    y=y_line,
                    mode="lines",
                    name=trend_label,
                    line={"dash": "dash", "width": 2, "color": "#EF553B"},
                )
            )

    return fig


def create_bar_chart(
    df: pd.DataFrame,
    column: str,
    top_n: int = 10,
) -> go.Figure:
    """計算類別（或文字）欄位中各項目出現次數，並繪製長條圖 (Bar Chart)。

    Args:
        df: 資料來源 DataFrame。
        column: 要統計次數的欄位名稱。
        top_n: 最多顯示前幾名，預設為 10。

    Returns:
        Plotly Figure 物件。
    """
    _validate_column(df, column)
    counts = (
        df[column]
        .fillna("(缺失值)")
        .astype(str)
        .value_counts()
        .head(top_n)
        .reset_index()
    )
    counts.columns = [column, "筆數"]

    fig = px.bar(
        counts,
        x=column,
        y="筆數",
        text="筆數",
        color=column,
        title=f"「{column}」各項目筆數統計（前 {top_n} 名）",
    )
    fig.update_traces(textposition="outside")
    return fig


def create_correlation_heatmap(df: pd.DataFrame) -> go.Figure:
    """計算所有數值欄位的皮爾森相關係數矩陣，並繪製互動式熱力圖 (Heatmap)。

    Args:
        df: 資料來源 DataFrame。

    Returns:
        Plotly Figure 物件。

    Raises:
        ChartError: 當數值欄位少於 2 個時。
    """
    numeric_df = df.select_dtypes(include="number")
    if len(numeric_df.columns) < 2:
        raise ChartError("需要至少 2 個數值欄位才能計算並繪製相關係數熱力圖。")

    corr_matrix = numeric_df.corr().round(2)
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        title="數值欄位相關係數熱力圖 (Correlation Heatmap)",
    )
    return fig

