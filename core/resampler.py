import numpy as np

def upsample_xyz_linear(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    fs_src: float = 400.0,
    fs_dst: float = 1000.0,
):
    """
    等間隔サンプリングされたXYZ加速度を
    線形補間で fs_src → fs_dst にアップサンプリングする

    Returns
    -------
    x_u, y_u, z_u : np.ndarray
        アップサンプリング後データ（同一長）
    """

    n_src = len(x)
    assert len(y) == n_src and len(z) == n_src, "XYZの長さが一致していない"

    # 元時間軸（サンプル番号基準）
    t_src = np.arange(n_src) / fs_src

    # 新時間軸
    t_end = t_src[-1]
    t_dst = np.arange(0, t_end, 1.0 / fs_dst)

    x_u = np.interp(t_dst, t_src, x)
    y_u = np.interp(t_dst, t_src, y)
    z_u = np.interp(t_dst, t_src, z)

    return x_u, y_u, z_u