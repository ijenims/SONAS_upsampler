import numpy as np
import plotly.graph_objects as go

def build_xyz_timeseries_figure(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    fs: float,
    title: str,
):
    """
    XYZ加速度の時系列を1枚のPlotlyグラフとして生成する

    Parameters
    ----------
    x, y, z : np.ndarray
        加速度データ
    fs : float
        サンプリング周波数 [Hz]
    title : str
        グラフタイトル

    Returns
    -------
    fig : plotly.graph_objects.Figure
    """

    n = len(x)
    assert len(y) == n and len(z) == n, "XYZの長さが一致していない"

    t = np.arange(n) / fs

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t, y=x,
        mode="lines",
        name="X",
    ))
    fig.add_trace(go.Scatter(
        x=t, y=y,
        mode="lines",
        name="Y",
    ))
    fig.add_trace(go.Scatter(
        x=t, y=z,
        mode="lines",
        name="Z",
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Time [s]",
        yaxis_title="Acceleration",
        legend=dict(orientation="h"),
        margin=dict(l=40, r=20, t=60, b=40),
    )

    return fig