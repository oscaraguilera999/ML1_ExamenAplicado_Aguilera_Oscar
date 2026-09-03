from __future__ import annotations

import base64
import contextlib
import io
import json
import os
import sys
import traceback
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")


def source_text(cell):
    src = cell.get("source", "")
    return "".join(src) if isinstance(src, list) else src


def main(path_str: str):
    path = Path(path_str).resolve()
    nb = json.loads(path.read_text(encoding="utf-8"))
    os.chdir(path.parent)

    ns = {"__name__": "__main__"}
    execution_count = 0

    for idx, cell in enumerate(nb["cells"]):
        if cell.get("cell_type") != "code":
            continue
        execution_count += 1
        cell["execution_count"] = execution_count
        cell["outputs"] = []
        stdout = io.StringIO()
        stderr = io.StringIO()
        display_outputs = []

        def captured_display(*objects, **kwargs):
            for obj in objects:
                data = {}
                if obj.__class__.__name__ == "Markdown" and hasattr(obj, "data"):
                    data["text/markdown"] = str(obj.data)
                    data["text/plain"] = str(obj.data)
                elif hasattr(obj, "to_html") and obj.__class__.__name__ == "Styler":
                    data["text/html"] = obj.to_html()
                    data["text/plain"] = str(obj.data)
                elif hasattr(obj, "_repr_html_"):
                    try:
                        html = obj._repr_html_()
                        if html:
                            data["text/html"] = html
                    except Exception:
                        pass
                    data["text/plain"] = str(obj)
                else:
                    data["text/plain"] = str(obj)
                display_outputs.append({"output_type": "display_data", "metadata": {}, "data": data})

        if "display" in ns:
            ns["display"] = captured_display

        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exec(compile(source_text(cell), f"cell_{idx}", "exec"), ns)
        except Exception as exc:
            tb = traceback.format_exc()
            cell["outputs"].append(
                {
                    "output_type": "error",
                    "ename": exc.__class__.__name__,
                    "evalue": str(exc),
                    "traceback": tb.splitlines(),
                }
            )
            path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
            print(tb, file=sys.stderr)
            raise

        if stdout.getvalue():
            cell["outputs"].append({"output_type": "stream", "name": "stdout", "text": stdout.getvalue()})
        if stderr.getvalue():
            cell["outputs"].append({"output_type": "stream", "name": "stderr", "text": stderr.getvalue()})
        cell["outputs"].extend(display_outputs)

        # Capture every figure produced by the cell so the executed notebook is self-contained.
        try:
            import matplotlib.pyplot as plt
            for fig_num in plt.get_fignums():
                fig = plt.figure(fig_num)
                image = io.BytesIO()
                fig.savefig(image, format="png", dpi=110, bbox_inches="tight")
                encoded = base64.b64encode(image.getvalue()).decode("ascii")
                cell["outputs"].append(
                    {"output_type": "display_data", "metadata": {}, "data": {"image/png": encoded}}
                )
            plt.close("all")
        except Exception:
            pass

        # The imports cell brings in IPython.display.display; override it for subsequent cells.
        ns["display"] = captured_display

    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Executed {execution_count} code cells: {path}")


if __name__ == "__main__":
    main(sys.argv[1])
