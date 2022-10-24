from . import jump_bp
from flask import render_template, request


@jump_bp.route("/", methods=["GET"])
def jump():
    print("jump")
    reason = request.args["reason"]
    target = request.args["target"]
    return render_template("jump.html", redirect_reason=reason, redirect_target=target)
