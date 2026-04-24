from __future__ import annotations

import base64
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from core.filename import build_output_filename
from core.formatter import build_output_dataframe
from core.loader import load_accel_xyz_from_csv
from core.notes import get_usage_notes
from core.resampler import upsample_xyz_linear
from viz.timeseries import build_xyz_timeseries_figure

app = FastAPI(title="Sonas Upsampler (HTML)")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "error": None,
            "success": None,
            "fig_in_json": None,
            "fig_out_json": None,
            "download_name": None,
            "download_b64": None,
            "notes": get_usage_notes(),
        },
    )


@app.post("/", response_class=HTMLResponse)
async def convert(request: Request, file: UploadFile = File(...)):
    context = {
        "error": None,
        "success": None,
        "fig_in_json": None,
        "fig_out_json": None,
        "download_name": None,
        "download_b64": None,
        "notes": get_usage_notes(),
    }

    if not file.filename:
        context["error"] = "CSVファイルを選択してください。"
        return templates.TemplateResponse(request, "index.html", context)

    if not file.filename.lower().endswith(".csv"):
        context["error"] = "CSVファイルのみ対応しています。"
        return templates.TemplateResponse(request, "index.html", context)

    try:
        raw = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            tmp.write(raw)
            input_path = Path(tmp.name)

        x, y, z = load_accel_xyz_from_csv(input_path)
        fig_in = build_xyz_timeseries_figure(x, y, z, fs=400, title="Input Data (400Hz)")

        x_u, y_u, z_u = upsample_xyz_linear(x, y, z)
        df_out = build_output_dataframe(x_u, y_u, z_u)
        fig_out = build_xyz_timeseries_figure(x_u, y_u, z_u, fs=1000, title="Output Data (1000Hz)")

        out_name = build_output_filename(Path(file.filename))
        out_csv = df_out.to_csv(index=False, header=False).encode("utf-8")
        out_b64 = base64.b64encode(out_csv).decode("ascii")

        context.update(
            {
                "success": "アップサンプリングが完了しました。",
                "fig_in_json": fig_in.to_json(),
                "fig_out_json": fig_out.to_json(),
                "download_name": out_name.name,
                "download_b64": out_b64,
            }
        )
    except Exception as exc:
        context["error"] = f"エラーが発生しました: {exc}"

    return templates.TemplateResponse(request, "index.html", context)
