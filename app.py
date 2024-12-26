from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    credit_approved = None
    reason = ""
    monthly_payment = 0
    total_payment = 0
    payment_schedule = []
    form_submitted = request.method == "POST"

    if request.method == "POST":
        try:
            # Получаем данные из формы
            user_data = {
                "surname": request.form.get("surname"),
                "name": request.form.get("name"),
                "patronymic": request.form.get("patronymic"),
                "age": request.form.get("age"),
                "salary": request.form.get("salary"),
                "debt_status": request.form.get("debt_status"),
                "phone": request.form.get("phone"),
                "email": request.form.get("email"),
                "passport_series": request.form.get("passport_series"),
                "passport_number": request.form.get("passport_number"),
                "loan_amount": request.form.get("loanAmount"),
                "loan_term": request.form.get("loan_term"),
            }

            # Проверяем, что все поля заполнены
            for key, value in user_data.items():
                if not value:
                    raise ValueError(f"Поле {key} не заполнено.")

            # Преобразуем данные в числа
            user_data["age"] = int(user_data["age"])
            user_data["salary"] = float(user_data["salary"])
            user_data["debt_status"] = user_data["debt_status"] == "1"
            user_data["loan_amount"] = float(user_data["loan_amount"])
            user_data["loan_term"] = int(user_data["loan_term"])

            # Логика принятия решения по кредиту
            max_loan = user_data["salary"] * 5
            credit_approved = True
            reason = ""

            if user_data["salary"] < 15000:
                credit_approved = False
                reason = "Слишком низкая зарплата. Для получения кредита ваша зарплата должна быть не менее 15000 рублей."
            elif user_data["debt_status"]:
                credit_approved = False
                reason = "Невозможно предоставить кредит с непогашенными задолженностями."
            elif user_data["loan_amount"] > max_loan:
                credit_approved = False
                reason = f"Запрашиваемая сумма кредита превышает максимальную сумму кредита, которая составляет {max_loan:.2f} рублей."

            # Расчет платежей, если кредит одобрен
            if credit_approved:
                monthly_payment = calculate_monthly_payment(user_data["loan_amount"], 12.0, user_data["loan_term"])
                total_payment = calculate_total_payment(monthly_payment, user_data["loan_term"])
                payment_schedule = calculate_payment_schedule(user_data["loan_amount"], 12.0, user_data["loan_term"])

        except ValueError as e:
            credit_approved = False
            reason = str(e)

    return render_template(
        "index.html",
        form_submitted=form_submitted,
        credit_approved=credit_approved,
        monthly_payment=monthly_payment,
        total_payment=total_payment,
        reason=reason,
        payment_schedule=payment_schedule,
    )

def calculate_monthly_payment(loan_amount, annual_interest_rate, loan_term):
    monthly_interest_rate = annual_interest_rate / 12 / 100
    annuity_coefficient = (monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term) / ((1 + monthly_interest_rate) ** loan_term - 1)
    return loan_amount * annuity_coefficient

def calculate_total_payment(monthly_payment, loan_term):
    return monthly_payment * loan_term

def calculate_payment_schedule(loan_amount, annual_interest_rate, loan_term):
    monthly_interest_rate = annual_interest_rate / 12 / 100
    monthly_payment = calculate_monthly_payment(loan_amount, annual_interest_rate, loan_term)
    balance = loan_amount
    schedule = []

    for month in range(1, loan_term + 1):
        interest = balance * monthly_interest_rate
        principal = monthly_payment - interest
        balance -= principal
        schedule.append({
            "month": month,
            "balance": balance,
            "principal": principal,
            "interest": interest,
        })

    return schedule

if __name__ == "__main__":
    app.run(debug=True)