from flask import Flask, render_template, request, redirect, session
from checklist_data import *
import json
import os
from logic.checklist_data import generate_checklist

print("HELLO FROM TRIP REPO")
app = Flask(__name__)
app.secret_key = "1642300Mb"  # حتما لازم

def load_data():
    with open("data.json", encoding="utf-8") as f:
        return json.load(f)
        
def rule_match(rules, form):
    for key, values in rules.items():
        if form.get(key) not in values:
            return False
    return True


def generate_checklist(form):
    data = load_data()
    result = {}

    for category in data["categories"]:
        rules = category.get("rules", {})

        if rules and not rule_match(rules, form):
            continue

        result[category["title"]] = [
            item["title"] for item in category["items"]
        ]

    return result
# ------------------------
# صفحه 1: فرم اصلی
# ------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["form"] = request.form.to_dict()
        return redirect("/review")

    return render_template("index.html", form=session.get("form"))


# ------------------------
# صفحه 2: بررسی اطلاعات
# ------------------------
@app.route("/review", methods=["GET"])
def review():
    form = session.get("form")
    if not form:
        return redirect("/")

    trip_type_map = {
        "solo": "انفرادی",
        "family": "خانوادگی"
    }

    accommodation_map = {
        "hotel": "هتل",
        "hostel": "هاستل",
        "villa": "ویلا",
        "suite": "سوئیت آپارتمان",
        "eco": "اقامتگاه بوم‌گردی",
        "camp": "چادر کمپ",
        "familyHome": "خانه اقوام"
    }

    travel_type = form.get("travel_type")
    hotel_type = form.get("hotel_type")

    trip_type_fa = trip_type_map.get(travel_type, travel_type)
    accommodation_fa = accommodation_map.get(hotel_type, hotel_type)

    return render_template(
        "review.html",
        form=form,
        trip_type=trip_type_fa,
        accommodation=accommodation_fa
    )



# ------------------------
# صفحه 3: نتیجه نهایی
# ------------------------
@app.route("/result", methods=["POST"])
def result():
    form = session.get("form")
    if not form:
        return redirect("/")

    travel_type_fa = {
        "solo": "به‌صورت انفرادی",
        "family": "به‌همراه خانواده"
    }

    transport_fa = {
        "plane": "با هواپیما",
        "train": "با قطار",
        "car": "با خودرو",
        "motor": "با موتور",
        "bus": "با اتوبوس"
    }

    season_fa = {
        "spring": "در بهار",
        "summer": "در تابستان",
        "autumn": "در پاییز",
        "winter": "در زمستان"
    }
    trip_type_map = {
        "solo": "انفرادی",
        "family": "خانوادگی"
    }

    accommodation_map = {
        "hotel": "هتل",
        "hostel": "هاستل",
        "villa": "ویلا",
        "familyHome": "خانه اقوام"
    }
   
    name = form.get("name")
    travel_type = form.get("travel_type")
    transport = form.get("transport")
    season = form.get("season")
    city_type = form.get("city_type")
    city = form.get("city_fa")
     
    hotel_type = form.get("hotel_type")
    try:
       stay_days = int(form.get("stay_days", 1))
    except:
        stay_days = 1
   
        
    checklist = generate_checklist(form)

       

    title = (
        f"چک‌لیست سفر {name} "
        f"{travel_type_fa.get(travel_type)} "
        f"{transport_fa.get(transport)} "
        f"{season_fa.get(season)} "
        f"به {city} ({stay_days} شب اقامت)"
    )
    
    

    session.pop("form", None)

    for category in checklist:
        checklist[category] = list(set(checklist[category]))
  

    return render_template(
        "result.html",
        checklist=checklist,
        title=title,
       
        
    )
    




# if __name__ == "__main__":
#    app.run(debug=True)
    
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)