import streamlit as st
from pathlib import Path
import tempfile

# core
from core.loader import load_accel_xyz_from_csv
from core.resampler import upsample_xyz_linear
from core.formatter import build_output_dataframe
from core.filename import build_output_filename
from core.notes import get_usage_notes

# viz
from viz.timeseries import build_xyz_timeseries_figure


def main():
    st.set_page_config(page_title="Sonas Upsampler", layout="wide")

    # ===== Sidebar =====
    st.sidebar.header("ファイル操作")
    uploaded_file = st.sidebar.file_uploader(
        "CSVファイルをアップロード",
        type=["csv"]
    )

    download_placeholder = st.sidebar.empty()

    # ===== Main =====
    st.title("Sonas アップサンプラー")
    st.subheader("サンプリング周波数：400Hz -> 1,000Hz")

    if uploaded_file is None:
        st.info("左のサイドバーからCSVファイルをアップロードしてください。")
        return

    try:
        # 一時ファイルとして保存（Path前提関数用）
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            tmp.write(uploaded_file.getvalue())
            input_path = Path(tmp.name)

        # --- A: load ---
        x, y, z = load_accel_xyz_from_csv(input_path)

        # 入力データ可視化
        fig_in = build_xyz_timeseries_figure(
            x, y, z,
            fs=400,
            title="Input Data (400Hz)"
        )
        st.plotly_chart(fig_in, width="stretch")

        # --- Resample ---
        x_u, y_u, z_u = upsample_xyz_linear(x, y, z)

        # --- B: format ---
        df_out = build_output_dataframe(x_u, y_u, z_u)

        # --- C: filename ---
        out_name = build_output_filename(Path(uploaded_file.name))
        out_csv = df_out.to_csv(index=False, header=False).encode("utf-8")

        # 完了メッセージ
        st.success("アップサンプリングが完了しました。")

        # 出力データ可視化
        fig_out = build_xyz_timeseries_figure(
            x_u, y_u, z_u,
            fs=1000,
            title="Output Data (1000Hz)"
        )
        st.plotly_chart(fig_out, width="stretch")

        # ダウンロードボタン
        download_placeholder.download_button(
            label="変換後CSVをダウンロード",
            data=out_csv,
            file_name=out_name.name,
            mime="text/csv"
        )

        # ★追加：ダウンロードファイル名表示
        st.sidebar.caption(f"保存ファイル名：{out_name.name}")

        # 注意書き
        st.markdown("### 取扱上の注意")
        for note in get_usage_notes():
            st.markdown(f"- {note}")

    except Exception as e:
        st.error(f"エラーが発生しました：{e}")


if __name__ == "__main__":
    main()