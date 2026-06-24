from flask import Flask, render_template, request, session, redirect
from logic.checklist import generate_checklist
from logic.mappings import travel_map, hotel_map, gender_map, transport_map, season_map
import os
import json

app = Flask(__name__)
app.secret_key = "1642300Mb"

# Cache برای جلوگیری از لود چندباره فایل
DATA_CACHE = None

def load_data():
    global DATA_CACHE
    if DATA_CACHE is None:
        base = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base, "data", "data.json")
        with open(file_path, "r", encoding="utf-8") as f:
            DATA_CACHE = json.load(f)
    return DATA_CACHE


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["form"] = request.form.to_dict()
        return redirect("/review")
    return render_template("index.html", form=session.get("form"))


@app.route("/review")
def review():
    form = session.get("form")
    if not form:
        return redirect("/")

    return render_template(
        "review.html",
        form=form,
        travel_type=travel_map.get(form.get("travel_type"), ""),
        accommodation=hotel_map.get(form.get("hotel_type"), ""),
        gender=gender_map.get(form.get("gender"), ""),
        transport=transport_map.get(form.get("transport"), ""),
        season=season_map.get(form.get("season"), "")
    )


@app.route("/result", methods=["GET", "POST"])
def result():
    form = session.get("form")
    if not form:
        return redirect("/")

    # نیاز به data اگر checklist از JSON بخواند
    data = load_data()

    categories = generate_checklist(form)

    title = (
        f"چک‌لیست سفر {form.get('name')} به {form.get('city_fa')} "
        f"{travel_map.get(form.get('travel_type'), '')} "
        f"به مدت {form.get('stay_days')} شب در "
        f"{hotel_map.get(form.get('hotel_type'), '')} "
        f"با {transport_map.get(form.get('transport'), '')} "
        f"در فصل {season_map.get(form.get('season'), '')}"
    )

    return render_template("result.html", categories=categories, title=title)


if __name__ == "__main__":
    app.run(debug=True)