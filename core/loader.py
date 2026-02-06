import pandas as pd
import numpy as np
from pathlib import Path

def load_accel_xyz_from_csv(csv_path: Path):
    """
    入力CSVから加速度XYZを読み込む
    1行目がヘッダでも数値でも対応する
    """

    df = pd.read_csv(csv_path)

    if df.shape[1] < 5:
        raise ValueError("CSVの列数が不足している（最低5列必要）")

    # 位置指定は維持、数値変換は安全側で
    x = pd.to_numeric(df.iloc[:, 2], errors="coerce")
    y = pd.to_numeric(df.iloc[:, 3], errors="coerce")
    z = pd.to_numeric(df.iloc[:, 4], errors="coerce")

    # ヘッダ由来のNaNを除去（＝先頭1行）
    mask = ~(x.isna() | y.isna() | z.isna())
    x = x[mask].to_numpy()
    y = y[mask].to_numpy()
    z = z[mask].to_numpy()

    return x, y, z