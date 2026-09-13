const form = document.getElementById("predictionForm");

form.addEventListener("submit", async function (event) {

    event.preventDefault();

    const button = document.getElementById("predictBtn");

    button.innerText = "⏳ Predicting...";
    button.disabled = true;

    const data = {
        Hours_Studied: Number(document.getElementById("Hours_Studied").value),
        Attendance: Number(document.getElementById("Attendance").value),

        Parental_Involvement: document.getElementById("Parental_Involvement").value,
        Access_to_Resources: document.getElementById("Access_to_Resources").value,

        Extracurricular_Activities:
            document.getElementById("Extracurricular_Activities").value,

        Sleep_Hours: Number(document.getElementById("Sleep_Hours").value),
        Previous_Scores: Number(document.getElementById("Previous_Scores").value),

        Motivation_Level:
            document.getElementById("Motivation_Level").value,

        Internet_Access:
            document.getElementById("Internet_Access").value,

        Tutoring_Sessions:
            Number(document.getElementById("Tutoring_Sessions").value),

        Family_Income:
            document.getElementById("Family_Income").value,

        Teacher_Quality:
            document.getElementById("Teacher_Quality").value,

        School_Type:
            document.getElementById("School_Type").value,

        Peer_Influence:
            document.getElementById("Peer_Influence").value,

        Physical_Activity:
            Number(document.getElementById("Physical_Activity").value),

        Learning_Disabilities:
            document.getElementById("Learning_Disabilities").value,

        Parental_Education_Level:
            document.getElementById("Parental_Education_Level").value,

        Distance_from_Home:
            document.getElementById("Distance_from_Home").value,

        Gender:
            document.getElementById("Gender").value,

        Grade_Level:
            Number(document.getElementById("Grade_Level").value),

        Current_Semester:
            Number(document.getElementById("Current_Semester").value),

        Class_Participation_Score:
            Number(document.getElementById("Class_Participation_Score").value)
    };

    try {

        const response = await fetch("http://127.0.0.1:8000/api/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error("Prediction request failed");
        }

        const result = await response.json();

        document.getElementById("result").classList.remove("hidden");

        document.getElementById("score").innerText =
            result.prediction;

        document.getElementById("category").innerText =
            result.category;

        document.getElementById("progressBar").style.width =
            Math.min(result.prediction, 100) + "%";

        document.getElementById("resultMessage").innerText =
            "The AI model predicts this student's performance as " +
            result.category + ".";

        document.getElementById("result").scrollIntoView({
            behavior: "smooth"
        });

    } catch (error) {

        alert(
            "Unable to connect to the prediction API. " +
            "Please make sure the backend is running."
        );

        console.error(error);

    } finally {

        button.innerText = "🚀 Predict Student Performance";
        button.disabled = false;

    }

});