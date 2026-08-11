const form = document.getElementById("loanForm");

const predictBtn =
    document.getElementById("predictBtn");


form.addEventListener("submit", async function (event) {

    event.preventDefault();


    // ============================
    // 1. Lấy model người dùng chọn
    // ============================

    const selectedModel =
        document.querySelector(
            'input[name="model"]:checked'
        ).value;


    // ============================
    // 2. Thu thập dữ liệu form
    // ============================

    const customerData = {

        person_age:
            Number(
                document.getElementById(
                    "person_age"
                ).value
            ),

        person_income:
            Number(
                document.getElementById(
                    "person_income"
                ).value
            ),

        person_emp_length:
            Number(
                document.getElementById(
                    "person_emp_length"
                ).value
            ),

        loan_amnt:
            Number(
                document.getElementById(
                    "loan_amnt"
                ).value
            ),

        loan_int_rate:
            Number(
                document.getElementById(
                    "loan_int_rate"
                ).value
            ),

        loan_percent_income:
            Number(
                document.getElementById(
                    "loan_percent_income"
                ).value
            ),

        cb_person_cred_hist_length:
            Number(
                document.getElementById(
                    "cb_person_cred_hist_length"
                ).value
            ),

        person_home_ownership:
            document.getElementById(
                "person_home_ownership"
            ).value,

        loan_intent:
            document.getElementById(
                "loan_intent"
            ).value,

        loan_grade:
            document.getElementById(
                "loan_grade"
            ).value,

        cb_person_default_on_file:
            document.getElementById(
                "cb_person_default_on_file"
            ).value

    };


    // ============================
    // 3. Loading state
    // ============================

    predictBtn.disabled = true;
    predictBtn.textContent =
        "Analyzing application...";


    try {

        // ============================
        // 4. Gọi FastAPI
        // ============================

        const response = await fetch(
            `/api/predict/${selectedModel}`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body:
                    JSON.stringify(customerData)
            }
        );


        if (!response.ok) {

            throw new Error(
                "Prediction request failed"
            );

        }


        const result =
            await response.json();


        // ============================
        // 5. Hiển thị kết quả
        // ============================

        showResult(result);


    } catch (error) {

        console.error(error);

        alert(
            "Không thể chạy prediction. Hãy kiểm tra backend."
        );

    } finally {

        predictBtn.disabled = false;

        predictBtn.textContent =
            "Analyze Loan Risk";

    }

});


function showResult(result) {

    const resultSection =
        document.getElementById(
            "resultSection"
        );

    resultSection.classList.remove(
        "hidden"
    );


    const riskBadge =
        document.getElementById(
            "riskBadge"
        );


    riskBadge.textContent =
        `${result.risk_level} RISK`;


    riskBadge.classList.remove(
        "low-risk",
        "high-risk"
    );


    if (result.is_bad_loan) {

        riskBadge.classList.add(
            "high-risk"
        );

    } else {

        riskBadge.classList.add(
            "low-risk"
        );

    }


    document.getElementById(
        "riskProbability"
    ).textContent =
        `${result.risk_probability}%`;


    document.getElementById(
        "riskProgress"
    ).style.width =
        `${result.risk_probability}%`;


    document.getElementById(
        "resultModel"
    ).textContent =
        result.model;


    document.getElementById(
        "resultStrategy"
    ).textContent =
        result.strategy;


    document.getElementById(
        "resultThreshold"
    ).textContent =
        `${result.threshold}%`;


    document.getElementById(
        "recommendation"
    ).textContent =
        result.recommendation;


    resultSection.scrollIntoView({
        behavior: "smooth"
    });

}