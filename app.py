from flask import Flask, render_template, request, send_file
import pandas as pd
import joblib
import os
from google import genai
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

app = Flask(__name__)

load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

UPLOAD_FOLDER = "uploads"
MODEL_PATH = "model/anomaly_model.pkl"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = joblib.load(MODEL_PATH)


def generate_ai_report(total_logs, normal_logs, anomaly_logs, risk):

    prompt = f"""
You are an Expert Cloud Security Analyst.

Analyze the following cloud security report.

Total Logs: {total_logs}
Normal Logs: {normal_logs}
Anomaly Logs: {anomaly_logs}
Risk Level: {risk}

Generate:

1. Executive Summary
2. Threat Analysis
3. Risk Score out of 100
4. Security Recommendations

Keep response professional.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"AI Report Error: {e}"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("index.html")


@app.route("/detect", methods=["POST"])
def detect():

    if "file" not in request.files:
        return "No file uploaded."

    file = request.files["file"]

    if file.filename == "":
        return "No file selected."

    filename = secure_filename(file.filename)

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    try:
        df = pd.read_csv(filepath)

    except Exception as e:
        return f"CSV Error : {e}"

    features = df.select_dtypes(include=["number"])

    if features.empty:
        return "CSV must contain numeric columns."

    prediction = model.predict(features)

    df["Prediction"] = prediction

    df["Prediction"] = df["Prediction"].replace(
        {-1: "Anomaly", 1: "Normal"}
    )

    total_logs = len(df)

    anomaly_logs = len(
        df[df["Prediction"] == "Anomaly"]
    )

    normal_logs = len(
        df[df["Prediction"] == "Normal"]
    )

    anomaly_percent = (
        anomaly_logs / total_logs
    ) * 100

    if anomaly_percent < 20:
        risk = "Low"

    elif anomaly_percent < 50:
        risk = "Medium"

    else:
        risk = "High"

    ai_report = generate_ai_report(
        total_logs,
        normal_logs,
        anomaly_logs,
        risk
    )
    result_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "result.csv"
    )

    df.to_csv(
        result_path,
        index=False
    )

    table = df.to_html(
        classes="table table-dark table-striped",
        index=False
    )

    return render_template(
        "result.html",
        table=table,
        total_logs=total_logs,
        normal_logs=normal_logs,
        anomaly_logs=anomaly_logs,
        risk=risk,
        ai_report=ai_report
    )


@app.route("/download")
def download():

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "result.csv"
    )

    if os.path.exists(file_path):

        return send_file(
            file_path,
            as_attachment=True,
            download_name="anomaly_report.csv"
        )

    return "Result file not found."


@app.errorhandler(404)
def page_not_found(error):

    return (
        """
        <center>
        <h1>404</h1>
        <h3>Page Not Found</h3>
        </center>
        """,
        404
    )


@app.errorhandler(500)
def internal_server_error(error):

    return (
        f"""
        <center>
        <h1>500</h1>
        <h3>Internal Server Error</h3>
        <p>{error}</p>
        </center>
        """,
        500
    )



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )