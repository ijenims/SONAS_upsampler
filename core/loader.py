import pandas as pd
import numpy as np
from pathlib import Path

def load_accel_xyz_from_csv(
    csv_path: Path,
):
    """
    入力CSVから加速度XYZを読み込む

    入力フォーマット前提：
    1列目: epoch（使わない）
    2列目: datetime（使わない）
    3列目: x
    4列目: y
    5列目: z

    Returns
    -------
    x, y, z : np.ndarray
        加速度データ（float）
    """

    df = pd.read_csv(csv_path, header=None)

    if df.shape[1] < 5:
        raise ValueError("CSVの列数が不足している（最低5列必要）")

    # 列位置で固定取得（仕様どおり）
    x = df.iloc[:, 2].to_numpy(dtype=float)
    y = df.iloc[:, 3].to_numpy(dtype=float)
    z = df.iloc[:, 4].to_numpy(dtype=float)

    return x, y, z