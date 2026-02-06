from pathlib import Path

def build_output_filename(
    input_path: Path,
    suffix: str = "_1k",
):
    """
    入力ファイル名の末尾に suffix を付与した Path を返す

    例：
    input : data.csv
    output: data_1k.csv
    """

    if input_path.suffix == "":
        raise ValueError("拡張子がないファイルは非対応")

    output_name = input_path.stem + suffix + input_path.suffix
    return input_path.with_name(output_name)