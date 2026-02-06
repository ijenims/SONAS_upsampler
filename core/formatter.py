import numpy as np
import pandas as pd

def build_output_dataframe(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
):
    """
    アップサンプリング後のXYZ配列から
    出力仕様どおりのDataFrameを生成する（ヘッダなし前提）

    出力列：
    1: "ags"（文字列）
    2: カウンタ（0,1,2,...）
    3: x
    4: y
    5: z
    6: 0
    7: 0
    8: 0
    """

    n = len(x)
    assert len(y) == n and len(z) == n, "XYZの長さが一致していない"

    df_out = pd.DataFrame({
        0: ["ags"] * n,
        1: np.arange(n, dtype=int),
        2: x,
        3: y,
        4: z,
        5: np.zeros(n),
        6: np.zeros(n),
        7: np.zeros(n),
    })

    return df_out