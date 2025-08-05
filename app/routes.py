from flask import Blueprint, render_template, request
from .scraper import fetch_case_details, save_query

main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        case_type = request.form['case_type']
        case_no = request.form['case_no']
        filing_year = request.form['filing_year']

        result = fetch_case_details(case_type, case_no, filing_year)
        save_query(case_type, case_no, filing_year, result['raw'])

        return render_template("result.html", result=result)
    return render_template("index.html")
