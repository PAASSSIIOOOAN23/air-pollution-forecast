
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Прогнозування забруднення",
    page_icon="🚗",
    layout="centered"
)

st.title("🚗🏞️ Прогнозування забруднення атмосфери")
st.write("Розрахунок шкідливих викидів автотранспорту")

# Коефіцієнти викидів (кг/км)
vehicle_types = {
    "Легковий автомобіль": 0.18,
    "Вантажний автомобіль": 0.65,
    "Автобус": 0.85,
    "Мотоцикл": 0.09
}

vehicle_ids = {
    "Легковий автомобіль": 1,
    "Вантажний автомобіль": 2,
    "Автобус": 3,
    "Мотоцикл": 4
}

st.header("Введення даних")

vehicle = st.selectbox(
    "Тип транспортного засобу",
    list(vehicle_types.keys())
)

count = st.number_input(
    "Кількість автомобілів",
    min_value=1,
    value=100
)

distance = st.number_input(
    "Відстань руху (км)",
    min_value=0.1,
    value=10.0
)

speed = st.number_input(
    "Середня швидкість (км/год)",
    min_value=1,
    value=50
)

save_to_db = st.checkbox(
    "Зберігати результат у PostgreSQL",
    value=False
)

if st.button("Розрахувати викиди"):
    factor = vehicle_types[vehicle]
    emissions = count * distance * factor

    if save_to_db:
        try:
            from database import save_traffic

            record_id = save_traffic(
                vehicle_ids[vehicle],
                count,
                speed,
                distance
            )

            st.success(
                f"Запис №{record_id} збережено в PostgreSQL!"
            )

        except Exception:
            st.error(
                "Не вдалося зберегти дані в PostgreSQL."
            )
    else:
        st.info("Демонстраційний режим без збереження.")

    st.success("Розрахунок виконано!")

    st.metric(
        "Загальний обсяг викидів",
        f"{emissions:.2f} кг"
    )

    data = pd.DataFrame({
        "Показник": [
            "Тип транспорту",
            "Кількість",
            "Відстань (км)",
            "Швидкість (км/год)",
            "Обсяг викидів (кг)"
        ],
        "Значення": [
            vehicle,
            count,
            distance,
            speed,
            round(emissions, 2)
        ]
    })

    st.subheader("Результати розрахунку")
    st.dataframe(data, hide_index=True)

    st.subheader("Залежність викидів від кількості авто")

    chart_data = pd.DataFrame({
        "Кількість автомобілів": range(1, count + 1),
        "Викиди (кг)": [
            i * distance * factor
            for i in range(1, count + 1)
        ]
    }).set_index("Кількість автомобілів")

    st.line_chart(chart_data)
