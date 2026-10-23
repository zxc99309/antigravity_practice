"""針對 src.analyzer、src.charts 與 src.exporter 的單元測試。"""

import io
from pathlib import Path
import pandas as pd
import pytest
from src.analyzer import (
    CSVLoadError,
    clean_missing_values,
    filter_dataframe,
    generate_auto_insights,
    get_basic_info,
    get_groupby_summary,
    get_missing_summary,
    get_numeric_summary,
    load_csv,
)
from src.charts import (
    ChartError,
    create_bar_chart,
    create_box_plot,
    create_correlation_heatmap,
    create_histogram,
    create_scatter_plot,
)
from src.exporter import generate_markdown_report


def test_load_sample_csv_success() -> None:
    """測試是否能成功讀取內建的 sample.csv 並取得正確概況。"""
    sample_path = Path(__file__).parent.parent / "sample_data" / "sample.csv"
    df = load_csv(str(sample_path))
    info = get_basic_info(df)

    assert info["rows"] == 10
    assert info["columns"] == 6
    assert "姓名" in info["column_names"]
    assert "月薪" in info["column_names"]


def test_load_empty_csv_raises_error() -> None:
    """測試傳入完全空白的檔案時，是否會拋出 CSVLoadError。"""
    empty_buffer = io.BytesIO(b"")
    with pytest.raises(CSVLoadError, match="空的"):
        load_csv(empty_buffer)


def test_load_header_only_csv_raises_error() -> None:
    """測試只有標題列、沒有任何資料列的 CSV 時，是否會拋出 CSVLoadError。"""
    header_only_buffer = io.BytesIO("姓名,年齡\n".encode("utf-8"))
    with pytest.raises(CSVLoadError, match="沒有任何資料列"):
        load_csv(header_only_buffer)


def test_load_big5_encoded_csv_success() -> None:
    """測試台灣常見的 Big5/CP950 編碼 CSV 是否能自動識別並成功讀取。"""
    csv_text = "商品,價格\n珍珠奶茶,65\n雞排,85\n"
    big5_buffer = io.BytesIO(csv_text.encode("cp950"))
    df = load_csv(big5_buffer)
    info = get_basic_info(df)

    assert info["rows"] == 2
    assert info["columns"] == 2
    assert info["column_names"] == ["商品", "價格"]


def test_get_missing_summary_counts_and_percentage() -> None:
    """測試缺失值統計的數量與百分比計算是否正確。"""
    sample_path = Path(__file__).parent.parent / "sample_data" / "sample.csv"
    df = load_csv(str(sample_path))
    missing_df = get_missing_summary(df)

    # sample.csv 共 10 筆，其中「姓名」無缺失、「年齡」缺 1 筆 (10.0%)
    name_row = missing_df[missing_df["欄位名稱"] == "姓名"].iloc[0]
    age_row = missing_df[missing_df["欄位名稱"] == "年齡"].iloc[0]

    assert name_row["缺失值數量"] == 0
    assert name_row["缺失比例 (%)"] == 0.0
    assert name_row["有效筆數"] == 10

    assert age_row["缺失值數量"] == 1
    assert age_row["缺失比例 (%)"] == 10.0
    assert age_row["有效筆數"] == 9


def test_get_numeric_summary_with_numeric_columns() -> None:
    """測試數值欄位統計摘要是否只包含數值欄位，且數值計算正確。"""
    df = pd.DataFrame(
        {
            "部門": ["A", "B", "C"],
            "分數": [80.0, 90.0, 100.0],
        }
    )
    num_df = get_numeric_summary(df)

    assert len(num_df) == 1
    row = num_df.iloc[0]
    assert row["欄位名稱"] == "分數"
    assert row["有效筆數"] == 3
    assert row["平均數"] == 90.0
    assert row["最小值"] == 80.0
    assert row["中位數 (50%)"] == 90.0
    assert row["最大值"] == 100.0


def test_get_numeric_summary_without_numeric_columns() -> None:
    """測試當 DataFrame 完全沒有數值欄位時，是否安全回傳空 DataFrame。"""
    df = pd.DataFrame({"姓名": ["小王", "小李"], "城市": ["台北", "台中"]})
    num_df = get_numeric_summary(df)

    assert num_df.empty


def test_create_charts_success() -> None:
    """測試四種 Plotly 圖表函式在正常資料下皆能成功產生 Figure 物件。"""
    sample_path = Path(__file__).parent.parent / "sample_data" / "sample.csv"
    df = load_csv(str(sample_path))

    fig_hist = create_histogram(df, "月薪", bins=10)
    fig_box = create_box_plot(df, y_column="月薪", x_column="部門")
    fig_scatter = create_scatter_plot(
        df, x_column="年齡", y_column="月薪", color_column="部門"
    )
    fig_bar = create_bar_chart(df, column="部門", top_n=5)

    assert "月薪" in fig_hist.layout.title.text
    assert "部門" in fig_box.layout.title.text
    assert "年齡" in fig_scatter.layout.title.text
    assert "部門" in fig_bar.layout.title.text


def test_create_chart_with_invalid_column_raises_error() -> None:
    """測試當傳入不存在的欄位或非數值欄位繪製直方圖時，是否拋出 ChartError。"""
    df = pd.DataFrame({"姓名": ["小王", "小李"], "月薪": [50000, 60000]})

    with pytest.raises(ChartError, match="找不到指定的欄位"):
        create_histogram(df, "不存在的欄位")

    with pytest.raises(ChartError, match="不是數值型態"):
        create_histogram(df, "姓名")


def test_generate_markdown_report_contains_all_sections() -> None:
    """測試產生的 Markdown 報告是否包含四大核心區塊與正確數據。"""
    sample_path = Path(__file__).parent.parent / "sample_data" / "sample.csv"
    df = load_csv(str(sample_path))
    report = generate_markdown_report(df, source_name="sample.csv", preview_rows=3)

    assert "# 📊 CSV 資料分析報告：sample.csv" in report
    assert "## 1. 資料基本概況" in report
    assert "總資料筆數 (Rows)**：10" in report
    assert "## 2. 資料內容預覽（前 3 筆）" in report
    assert "## 3. 缺失值與欄位型態統計" in report
    assert "## 4. 數值欄位統計摘要" in report
    assert "王小明" in report


def test_generate_markdown_report_without_numeric_columns() -> None:
    """測試當資料無數值欄位時，Markdown 報告能正常產生並顯示提示訊息。"""
    df = pd.DataFrame({"姓名": ["小王", "小李"], "部門": ["研發部", "業務部"]})
    report = generate_markdown_report(df, source_name="text_only.csv")

    assert "此份資料沒有任何數值型態的欄位可供計算統計摘要" in report


def test_load_binary_file_disguised_as_csv_raises_error() -> None:
    """測試當上傳含有 Null Byte 的二進位檔案（如假冒 .csv 的 .xlsx 或圖片）時，是否會拋出 CSVLoadError。"""
    binary_buffer = io.BytesIO(b"PK\x03\x04\x00\x00\x00fake_xlsx_content")
    with pytest.raises(CSVLoadError, match="二進位檔案"):
        load_csv(binary_buffer)


def test_clean_missing_values_drop_rows() -> None:
    """測試刪除含有缺失值的資料列後，筆數正確且不影響原始 DataFrame。"""
    sample_path = Path(__file__).parent.parent / "sample_data" / "sample.csv"
    raw_df = load_csv(str(sample_path))
    cleaned_df = clean_missing_values(raw_df, strategy="drop_rows")

    # 原始 sample.csv 共 10 筆，其中 4 筆含有缺失值，刪除後應剩 6 筆
    assert len(raw_df) == 10
    assert len(cleaned_df) == 6
    assert int(cleaned_df.isna().sum().sum()) == 0


def test_clean_missing_values_fill_median_and_mean() -> None:
    """測試以中位數或平均數填補數值缺失值，並以『未知』填補文字缺失值。"""
    df = pd.DataFrame(
        {
            "城市": ["台北", None, "台中"],
            "薪資": [40000.0, 50000.0, None],
        }
    )
    median_df = clean_missing_values(df, strategy="fill_median")
    mean_df = clean_missing_values(df, strategy="fill_mean")

    assert median_df.loc[1, "城市"] == "未知"
    assert median_df.loc[2, "薪資"] == 45000.0
    assert mean_df.loc[2, "薪資"] == 45000.0
    # 確認原始 df 未被修改
    assert pd.isna(df.loc[1, "城市"])


def test_clean_missing_values_invalid_strategy_raises_error() -> None:
    """測試傳入不支援的清理策略時，是否會拋出 ValueError。"""
    df = pd.DataFrame({"A": [1, 2]})
    with pytest.raises(ValueError, match="不支援的缺失值清理策略"):
        clean_missing_values(df, strategy="unknown_strategy")


def test_generate_auto_insights_detects_missing_and_correlation() -> None:
    """測試自動統計洞察是否能正確偵測缺失值與強相關欄位。"""
    sample_path = Path(__file__).parent.parent / "sample_data" / "sample.csv"
    df = load_csv(str(sample_path))
    insights = generate_auto_insights(df)
    joined_text = "\n".join(insights)

    assert "缺失值提醒" in joined_text
    assert "強相關欄位發現" in joined_text
    assert "年齡" in joined_text and "月薪" in joined_text


def test_create_correlation_heatmap_success_and_error() -> None:
    """測試相關係數熱力圖能正常生成，且在數值欄位少於 2 個時拋出 ChartError。"""
    sample_path = Path(__file__).parent.parent / "sample_data" / "sample.csv"
    df = load_csv(str(sample_path))
    fig = create_correlation_heatmap(df)
    assert "相關係數熱力圖" in fig.layout.title.text

    single_num_df = pd.DataFrame({"姓名": ["A", "B"], "年齡": [20, 30]})
    with pytest.raises(ChartError, match="至少 2 個數值欄位"):
        create_correlation_heatmap(single_num_df)


def test_filter_dataframe_categorical_and_numeric() -> None:
    """測試資料條件篩選器是否能同時依類別清單與數值區間正確過濾資料列。"""
    sample_path = Path(__file__).parent.parent / "sample_data" / "sample.csv"
    df = load_csv(str(sample_path))

    # 篩選「部門」為「研發部」且「月薪」介於 68000 到 90000 之間的員工
    filtered = filter_dataframe(
        df,
        categorical_filters={"部門": ["研發部"]},
        numeric_ranges={"月薪": (68000.0, 90000.0)},
    )

    assert len(filtered) == 2
    assert set(filtered["姓名"]) == {"張大衛", "吳家豪"}


def test_filter_dataframe_invalid_column_raises_key_error() -> None:
    """測試篩選不存在的欄位時，是否拋出 KeyError。"""
    df = pd.DataFrame({"部門": ["研發部"], "月薪": [60000]})
    with pytest.raises(KeyError, match="找不到指定的篩選欄位"):
        filter_dataframe(df, categorical_filters={"不存在欄位": ["A"]})


def test_get_groupby_summary_calculates_correctly() -> None:
    """測試分組樞紐分析 (GroupBy) 的筆數、平均數、中位數與總和計算是否正確。"""
    sample_path = Path(__file__).parent.parent / "sample_data" / "sample.csv"
    df = load_csv(str(sample_path))

    # 依「部門」分組計算「月薪」統計量
    grouped_df = get_groupby_summary(df, group_col="部門", target_col="月薪")

    # 研發部有 3 人：65000, 85000, 70000 -> 平均 73333.33, 中位數 70000, 總和 220000
    rd_row = grouped_df[grouped_df["部門"] == "研發部"].iloc[0]
    assert rd_row["有效筆數"] == 3
    assert rd_row["平均數"] == 73333.33
    assert rd_row["中位數"] == 70000.0
    assert rd_row["總和"] == 220000.0


def test_get_groupby_summary_invalid_columns_raise_error() -> None:
    """測試分組統計傳入不存在欄位或非數值目標欄位時，是否拋出正確例外。"""
    df = pd.DataFrame({"部門": ["研發部", "業務部"], "姓名": ["小王", "小李"], "月薪": [50000, 60000]})

    with pytest.raises(KeyError, match="找不到分組欄位"):
        get_groupby_summary(df, group_col="不存在", target_col="月薪")

    with pytest.raises(ValueError, match="不是數值型態"):
        get_groupby_summary(df, group_col="部門", target_col="姓名")


def test_create_scatter_plot_with_trendline() -> None:
    """測試散佈圖啟用 show_trendline=True 時，是否成功疊加線性趨勢線軌跡。"""
    sample_path = Path(__file__).parent.parent / "sample_data" / "sample.csv"
    df = load_csv(str(sample_path))
    fig = create_scatter_plot(df, x_column="年齡", y_column="月薪", show_trendline=True)

    # 應包含原始資料點與一條「線性趨勢線」trace
    trace_names = [trace.name for trace in fig.data if trace.name]
    assert any("線性趨勢線" in name for name in trace_names)


def test_generate_markdown_report_with_groupby_section() -> None:
    """測試當提供 group_col 與 target_col 時，Markdown 報告包含第 5 節分組樞紐分析。"""
    sample_path = Path(__file__).parent.parent / "sample_data" / "sample.csv"
    df = load_csv(str(sample_path))
    report = generate_markdown_report(
        df,
        source_name="sample.csv",
        group_col="部門",
        target_col="月薪",
    )

    assert "## 5. 分組樞紐分析（依「部門」統計「月薪」）" in report
    assert "研發部" in report
    assert "220000" in report










