import json
from flask import Blueprint, Response, render_template, url_for, request, redirect
from src.mainAPI.Expansions import Sequence, Expansion
from src.utils.Utils import series_index_page_params, round_values_in_list
series = Blueprint("series", __name__, url_prefix="/series")


@series.route(
    "/series", methods=["GET", "POST"], endpoint="index"
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
        if rounding is None:
            rounding = 9
        if n is None:
            n = int(x)

        return redirect(
            url_for('series.result', sequence_name=sequence_name, x=x, n=n, rounding=rounding)
        )
    else:
        return render_template("/series/index.html")


@series.route(
    "/series/result/<sequence_name>/<x>/<n>/<rounding>", endpoint="result"
)
def result(sequence_name, x, n, rounding):
    sequence = Sequence(sequence_name=sequence_name)
    expansion = Expansion(sequence=sequence, x=x, n=n)

    all_results = expansion.get_all_results()
    data_frame = all_results["data_frame"].to_html(
        index=False, justify="center", col_space=250, show_dimensions=True
    ).replace("class=\"dataframe\"", "class =\"table table-responsive\"")
    linear_space = list(all_results["iterations"])
    graph_result_y = round_values_in_list(all_results["results"], rounding)
    graph_error_y = round_values_in_list(all_results["errors"], rounding)
    formulas = expansion.seq.formulas_mat_jax

    return render_template(
        "/series/result.html", data_frame=data_frame, x=expansion.x, n=expansion.n,
        formula_0=formulas[0], formula_1=formulas[1], formula_2=formulas[2],
        linear_space=linear_space, graph_result_y=graph_result_y,
        graph_error_y=graph_error_y, last_iteration=graph_result_y[-1]
    )
