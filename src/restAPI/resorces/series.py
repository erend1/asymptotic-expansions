import json
from flask import Blueprint, Response, render_template, url_for, request, redirect
from src.mainAPI.Expansions import Sequence, Expansion
from src.utils.Utils import series_index_page_params, round_values_in_list
series = Blueprint("series", __name__, url_prefix="/series")


@series.route(
    rule="/series",
    methods=["GET", "POST"],
    endpoint="index"
)
def index():
    if request.method == "POST":
        sequence_name, x, n, rounding = series_index_page_params(form=request.form)
        try:
            x = float(x)
        except ValueError:
            return render_template("/series/index.html")

        if sequence_name is None:
            sequence_name = "exponential"

        return redirect(
            url_for('series.result', sequence_name=sequence_name, x=x, n=n, rounding=rounding)
        )
    else:
        return render_template("/series/index.html")


@series.route(
    rule="/series/result/<string:sequence_name>/<float:x>/",
    defaults={'n': None, 'rounding': None},
    endpoint="result"
)
@series.route(
    rule="/series/result/<string:sequence_name>/<float:x>/<n>/",
    defaults={'rounding': None},
    endpoint="result"
)
@series.route(
    rule="/series/result/<string:sequence_name>/<float:x>/<rounding>/",
    defaults={'n': None},
    endpoint="result"
)
@series.route(
    rule="/series/result/<string:sequence_name>/<float:x>/<n>/<rounding>",
    endpoint="result"
)
def result(sequence_name: str, x: float, n=None, rounding=None):
    sequence = Sequence(sequence_name=sequence_name)
    expansion = Expansion(sequence=sequence, x=x, n=n)

    mat_jax_mapper = {
        "iter": r"\( n \)",
        "value": r"\(S_n(x)\)",
        "error": r"\(|S_{n+1}(x)-S_n(x)|\)"
    }

    data_frame = expansion.get_data_frame()
    linear_space = list(data_frame["iter"])
    graph_result_y = round_values_in_list(list(data_frame["value"]), rounding)
    graph_error_y = round_values_in_list(list(data_frame["error"]), rounding)
    data_frame = data_frame.rename(columns=mat_jax_mapper).to_html(
        index=False, justify="center", col_space=120, show_dimensions=True
    ).replace("class=\"dataframe\"", "class =\"table table-responsive\"")

    formulas = expansion.seq.formulas_mat_jax

    return render_template(
        "/series/result.html", data_frame=data_frame, x=expansion.x, n=expansion.n,
        formula_0=formulas[0], formula_1=formulas[1], formula_2=formulas[2],
        linear_space=linear_space, graph_result_y=graph_result_y,
        graph_error_y=graph_error_y, last_iteration=graph_result_y[-1]
    )
