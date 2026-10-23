"""產生 1,000 筆擬真台灣企業員工範例資料 (sample_data/sample.csv) 的腳本。"""

from pathlib import Path
import numpy as np
import pandas as pd


def generate_sample_csv(output_path: Path, n_rows: int = 1000) -> None:
    """使用固定隨機種子產生具備統計相關性、缺失值與離群值的 1,000 筆員工資料。"""
    rng = np.random.default_rng(42)

    last_names = [
        "陳", "林", "黃", "張", "李", "王", "吳", "劉", "蔡", "楊",
        "許", "鄭", "謝", "郭", "洪", "曾", "邱", "廖", "賴", "周",
    ]
    first_chars = [
        "家", "志", "宗", "雅", "怡", "詩", "承", "宇", "冠", "心",
        "佳", "佩", "俊", "建", "淑", "美", "文", "明", "偉", "哲",
    ]
    second_chars = [
        "豪", "婷", "君", "涵", "穎", "翰", "恩", "軒", "廷", "瑜",
        "玲", "芬", "宏", "傑", "華", "明", "衛", "榮", "樺", "安",
    ]

    names = [
        f"{rng.choice(last_names)}{rng.choice(first_chars)}{rng.choice(second_chars)}"
        for _ in range(n_rows)
    ]

    departments = rng.choice(
        ["研發部", "業務部", "行銷部", "人資部", "財務部", "客服部"],
        size=n_rows,
        p=[0.30, 0.25, 0.15, 0.10, 0.10, 0.10],
    )

    cities = rng.choice(
        ["台北", "新北", "新竹", "台中", "台南", "高雄"],
        size=n_rows,
        p=[0.35, 0.18, 0.17, 0.13, 0.08, 0.09],
    ).astype(object)

    # 年齡介於 22 ~ 58 歲
    ages = rng.integers(22, 59, size=n_rows).astype(float)

    # 讓月薪與年齡、部門呈現明顯正相關 (確保皮爾森相關係數 r >= 0.75)
    dept_bonus = {
        "研發部": 12000,
        "業務部": 6000,
        "財務部": 4000,
        "行銷部": 2000,
        "人資部": 0,
        "客服部": -2000,
    }
    base_salaries = (
        20000
        + ages * 1600
        + np.array([dept_bonus[d] for d in departments])
        + rng.normal(0, 4500, size=n_rows)
    )
    salaries = np.round(base_salaries / 100) * 100

    # 加入少數高薪資深主管離群值 (讓盒鬚圖與 IQR 離群值偵測更有教學效果)
    outlier_indices = rng.choice(n_rows, size=8, replace=False)
    salaries[outlier_indices] = rng.choice([145000.0, 158000.0, 165000.0], size=8)

    # 績效分數 (60 ~ 99 分，常態分佈)
    scores = np.clip(np.round(rng.normal(84.0, 6.5, size=n_rows), 1), 60.0, 99.5)

    # 刻意加入擬真缺失值（年齡缺 50 筆 = 5.0% 最多、月薪缺 30 筆、績效缺 25 筆、城市缺 20 筆）
    age_missing_idx = rng.choice(n_rows, size=50, replace=False)
    salary_missing_idx = rng.choice(n_rows, size=30, replace=False)
    score_missing_idx = rng.choice(n_rows, size=25, replace=False)
    city_missing_idx = rng.choice(n_rows, size=20, replace=False)

    ages[age_missing_idx] = np.nan
    salaries[salary_missing_idx] = np.nan
    scores[score_missing_idx] = np.nan
    cities[city_missing_idx] = None

    df = pd.DataFrame(
        {
            "姓名": names,
            "部門": departments,
            "年齡": ages,
            "月薪": salaries,
            "績效分數": scores,
            "入職城市": cities,
        }
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"成功產生 {len(df)} 筆範例資料至：{output_path}")


if __name__ == "__main__":
    target = Path(__file__).parent.parent / "sample_data" / "sample.csv"
    generate_sample_csv(target, n_rows=1000)
