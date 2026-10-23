"""CSV 資料分析助手 - Streamlit 網頁主程式（第六階段：互動式資料清理）。"""

import importlib
from pathlib import Path
import pandas as pd
import streamlit as st
import src.analyzer
import src.charts
import src.exporter

# 確保 Streamlit 熱重載 (Hot-Reload) 時，同步重新載入 src 子模組的最新程式碼
importlib.reload(src.analyzer)
importlib.reload(src.charts)
importlib.reload(src.exporter)

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

SAMPLE_CSV_PATH = Path(__file__).parent / "sample_data" / "sample.csv"


def render_charts_section(df: pd.DataFrame) -> None:
    """渲染 Plotly 互動式圖表區塊。"""
    st.subheader("📈 互動式圖表分析")

    numeric_cols = list(df.select_dtypes(include="number").columns)
    categorical_cols = list(df.select_dtypes(exclude="number").columns)
    all_cols = list(df.columns)

    tab_hist, tab_box, tab_scatter, tab_bar, tab_corr = st.tabs(
        [
            "📊 直方圖 (分佈)",
            "📦 盒鬚圖 (分位數/離群值)",
            "🔵 散佈圖 (雙變數關係)",
            "📊 長條圖 (類別計數)",
            "🔥 相關係數熱力圖",
        ]
    )

    # 分頁 1：直方圖
    with tab_hist:
        if not numeric_cols:
            st.info("此份資料沒有數值欄位，無法繪製直方圖。")
        else:
            col_a, col_b = st.columns([2, 1])
            selected_num = col_a.selectbox(
                "選擇要觀察分佈的數值欄位",
                options=numeric_cols,
                key="hist_col",
            )
            bins = col_b.slider("分箱數量 (Bins)", min_value=5, max_value=50, value=15)
            try:
                fig = create_histogram(df, selected_num, bins=bins)
                st.plotly_chart(fig, width="stretch")
            except ChartError as err:
                st.error(str(err))

    # 分頁 2：盒鬚圖
    with tab_box:
        if not numeric_cols:
            st.info("此份資料沒有數值欄位，無法繪製盒鬚圖。")
        else:
            col_a, col_b = st.columns(2)
            box_y = col_a.selectbox(
                "選擇數值欄位 (Y 軸)",
                options=numeric_cols,
                key="box_y",
            )
            group_options = ["(不分組)"] + categorical_cols
            box_x_choice = col_b.selectbox(
                "選擇分組類別欄位 (X 軸，可選)",
                options=group_options,
                key="box_x",
            )
            box_x = None if box_x_choice == "(不分組)" else box_x_choice
            try:
                fig = create_box_plot(df, y_column=box_y, x_column=box_x)
                st.plotly_chart(fig, width="stretch")
            except ChartError as err:
                st.error(str(err))

    # 分頁 3：散佈圖
    with tab_scatter:
        if len(numeric_cols) < 2:
            st.info("需要至少 2 個數值欄位才能繪製雙變數散佈圖。")
        else:
            col_a, col_b, col_c = st.columns(3)
            scatter_x = col_a.selectbox(
                "選擇 X 軸數值欄位",
                options=numeric_cols,
                index=0,
                key="scatter_x",
            )
            scatter_y = col_b.selectbox(
                "選擇 Y 軸數值欄位",
                options=numeric_cols,
                index=min(1, len(numeric_cols) - 1),
                key="scatter_y",
            )
            color_options = ["(不區分顏色)"] + all_cols
            color_choice = col_c.selectbox(
                "選擇顏色標記欄位 (可選)",
                options=color_options,
                key="scatter_color",
            )
            color_col = None if color_choice == "(不區分顏色)" else color_choice
            show_trend = st.checkbox(
                "📈 顯示全體線性迴歸趨勢線 (y = ax + b)",
                value=True,
                key="scatter_trend",
            )
            try:
                fig = create_scatter_plot(
                    df,
                    x_column=scatter_x,
                    y_column=scatter_y,
                    color_column=color_col,
                    show_trendline=show_trend,
                )
                st.plotly_chart(fig, width="stretch")
            except ChartError as err:
                st.error(str(err))

    # 分頁 4：類別長條圖
    with tab_bar:
        default_bar_cols = categorical_cols if categorical_cols else all_cols
        col_a, col_b = st.columns([2, 1])
        bar_col = col_a.selectbox(
            "選擇要統計出現次數的欄位",
            options=default_bar_cols,
            key="bar_col",
        )
        top_n = col_b.slider("最多顯示前幾名", min_value=3, max_value=30, value=10)
        try:
            fig = create_bar_chart(df, column=bar_col, top_n=top_n)
            st.plotly_chart(fig, width="stretch")
        except ChartError as err:
            st.error(str(err))

    # 分頁 5：相關係數熱力圖
    with tab_corr:
        if len(numeric_cols) < 2:
            st.info("需要至少 2 個數值欄位才能計算並繪製相關係數熱力圖。")
        else:
            st.caption(
                "💡 相關係數介於 -1 到 +1 之間：越接近 +1 代表高度正相關（同增同減），越接近 -1 代表高度負相關。"
            )
            try:
                fig = create_correlation_heatmap(df)
                st.plotly_chart(fig, width="stretch")
            except ChartError as err:
                st.error(str(err))


def main() -> None:
    """渲染 Streamlit 主頁面。"""
    st.set_page_config(
        page_title="CSV 資料分析助手",
        page_icon="📊",
        layout="wide",
    )

    st.title("📊 CSV 資料分析助手")
    st.write("上傳一個 CSV 檔案，或使用內建範例資料，快速檢視資料概況、缺失值統計與數值摘要。")

    # 側邊欄：資料來源選擇
    st.sidebar.header("📁 資料來源設定")
    use_sample = st.sidebar.checkbox("使用內建範例資料 (sample.csv)", value=False)
    uploaded_file = st.sidebar.file_uploader(
        "或上傳您的 CSV 檔案",
        type=["csv"],
        disabled=use_sample,
    )

    # 決定要讀取哪個資料來源
    file_source = None
    source_name = ""
    if use_sample:
        if SAMPLE_CSV_PATH.exists():
            file_source = str(SAMPLE_CSV_PATH)
            source_name = "內建範例資料 (sample.csv)"
        else:
            st.error("找不到內建範例檔案 `sample_data/sample.csv`。")
            return
    elif uploaded_file is not None:
        file_source = uploaded_file
        source_name = uploaded_file.name

    if file_source is None:
        st.info("👈 請從左側欄上傳 CSV 檔案，或勾選「使用內建範例資料」開始分析。")
        return

    # 嘗試讀取並顯示基本資訊
    try:
        raw_df = load_csv(file_source)
    except CSVLoadError as err:
        st.error(f"❌ 讀取檔案失敗：{err}")
        return

    # 側邊欄：資料清理設定（缺失值處理）
    st.sidebar.divider()
    st.sidebar.header("🧹 資料清理設定")
    strategy_map = {
        "不處理（保留原始缺失值）": "none",
        "刪除含缺失值的資料列 (dropna)": "drop_rows",
        "數值補中位數、文字補「未知」": "fill_median",
        "數值補平均數、文字補「未知」": "fill_mean",
    }
    selected_label = st.sidebar.selectbox(
        "選擇缺失值處理方式",
        options=list(strategy_map.keys()),
    )
    selected_strategy = strategy_map[selected_label]
    df = clean_missing_values(raw_df, strategy=selected_strategy)

    # 側邊欄：互動式條件篩選器
    st.sidebar.divider()
    st.sidebar.header("🔎 資料條件篩選")
    filter_cols = st.sidebar.multiselect(
        "選擇要加入篩選條件的欄位（可複選）",
        options=list(df.columns),
    )

    cat_filters = {}
    num_ranges = {}
    for col in filter_cols:
        if pd.api.types.is_numeric_dtype(df[col]):
            valid_series = df[col].dropna()
            if not valid_series.empty:
                min_v = float(valid_series.min())
                max_v = float(valid_series.max())
                if min_v < max_v:
                    selected_range = st.sidebar.slider(
                        f"「{col}」數值區間",
                        min_value=min_v,
                        max_value=max_v,
                        value=(min_v, max_v),
                    )
                    num_ranges[col] = selected_range
                else:
                    st.sidebar.caption(f"欄位「{col}」所有數值皆為 {min_v}，無須調整區間。")
        else:
            unique_vals = list(df[col].dropna().unique())
            selected_vals = st.sidebar.multiselect(
                f"「{col}」包含項目",
                options=unique_vals,
                default=unique_vals,
            )
            cat_filters[col] = selected_vals

    if cat_filters or num_ranges:
        df = filter_dataframe(
            df,
            categorical_filters=cat_filters,
            numeric_ranges=num_ranges,
        )

    st.success(f"✅ 成功載入：{source_name}")

    has_modification = (selected_strategy != "none") or bool(filter_cols)
    if has_modification:
        raw_missing = int(raw_df.isna().sum().sum())
        new_missing = int(df.isna().sum().sum())
        st.info(
            f"🛠️ **目前已套用清理或篩選條件**｜"
            f"清理策略：{selected_label}｜"
            f"篩選欄位：{', '.join(filter_cols) if filter_cols else '無'} \n\n"
            f"📊 **資料變化**：原始 {len(raw_df)} 筆 ➡️ 目前 **{len(df)}** 筆｜"
            f"缺失值總數：{raw_missing} ➡️ **{new_missing}** 個"
        )
        safe_stem = Path(source_name).stem if "." in source_name else "csv_data"
        # 使用 utf-8-sig 編碼（含 BOM），讓 Excel 直接雙擊開啟時中文不會亂碼
        cleaned_csv_bytes = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="⬇️ 下載處理後的 CSV 檔案 (.csv)",
            data=cleaned_csv_bytes,
            file_name=f"{safe_stem}_processed.csv",
            mime="text/csv",
        )

    if df.empty:
        st.warning("⚠️ 套用目前的清理或篩選條件後已無符合的資料列，請放寬左側的篩選條件。")
        return

    # 1. 顯示資料基本維度指標
    basic_info = get_basic_info(df)
    total_missing = int(df.isna().sum().sum())
    col1, col2, col3 = st.columns(3)
    col1.metric("總資料筆數 (Rows)", basic_info["rows"])
    col2.metric("總欄位數 (Columns)", basic_info["columns"])
    col3.metric("總缺失值數量 (Missing Values)", total_missing)

    with st.expander("查看所有欄位名稱"):
        st.write(", ".join(basic_info["column_names"]))

    # 1.5 自動統計洞察摘要區塊
    st.subheader("💡 自動資料洞察摘要")
    for item in generate_auto_insights(df):
        st.markdown(f"- {item}")

    # 2. 資料預覽區塊
    st.subheader("🔍 資料內容預覽")
    max_rows = max(1, min(50, basic_info["rows"]))
    default_rows = min(10, max_rows)
    preview_count = st.slider(
        "選擇預覽筆數",
        min_value=1,
        max_value=max_rows,
        value=default_rows,
    )
    st.dataframe(df.head(preview_count), width="stretch")

    # 3. 缺失值統計區塊
    st.subheader("📋 缺失值與欄位型態統計")
    missing_df = get_missing_summary(df)
    st.dataframe(missing_df, width="stretch")

    # 4. 數值欄位統計摘要區塊
    st.subheader("🔢 數值欄位統計摘要")
    numeric_df = get_numeric_summary(df)
    if numeric_df.empty:
        st.warning("⚠️ 此份資料沒有任何數值型態的欄位可供計算統計摘要。")
    else:
        st.dataframe(numeric_df, width="stretch")

    # 4.5 分組樞紐分析 (GroupBy) 區塊
    st.subheader("🧮 分組樞紐分析 (GroupBy)")
    numeric_cols = list(df.select_dtypes(include="number").columns)
    categorical_cols = list(df.select_dtypes(exclude="number").columns)
    selected_group = None
    selected_target = None
    if not numeric_cols or len(df.columns) < 2:
        st.info("需要至少 1 個數值欄位與 1 個分組欄位才能進行分組樞紐分析。")
    else:
        group_candidates = categorical_cols if categorical_cols else [
            c for c in df.columns if c != numeric_cols[0]
        ]
        col_g1, col_g2 = st.columns(2)
        selected_group = col_g1.selectbox(
            "選擇分組依據欄位（例如：部門、城市）",
            options=group_candidates,
            key="groupby_col",
        )
        target_candidates = [c for c in numeric_cols if c != selected_group]
        if not target_candidates:
            st.info("請選擇與分組欄位不同的數值欄位。")
        else:
            selected_target = col_g2.selectbox(
                "選擇要計算統計量的數值欄位（例如：月薪、績效分數）",
                options=target_candidates,
                key="groupby_target",
            )
            group_summary_df = get_groupby_summary(
                df,
                group_col=selected_group,
                target_col=selected_target,
            )
            st.dataframe(group_summary_df, width="stretch")

    # 5. Plotly 互動式圖表分析區塊
    render_charts_section(df)

    # 6. 匯出 Markdown 分析報告區塊
    st.subheader("📝 匯出 Markdown 分析報告")
    st.write("將上方的資料概況、缺失值統計、數值摘要與分組樞紐分析自動彙整成 Markdown (`.md`) 報告檔案。")
    report_md = generate_markdown_report(
        df,
        source_name=source_name,
        preview_rows=preview_count,
        group_col=selected_group,
        target_col=selected_target,
    )

    with st.expander("預覽 Markdown 報告原始碼"):
        st.code(report_md, language="markdown")

    safe_stem = Path(source_name).stem if "." in source_name else "csv_data"
    st.download_button(
        label="⬇️ 下載 Markdown 分析報告 (.md)",
        data=report_md.encode("utf-8"),
        file_name=f"{safe_stem}_analysis_report.md",
        mime="text/markdown",
    )


if __name__ == "__main__":
    main()

