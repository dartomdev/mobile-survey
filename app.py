import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

if not firebase_admin._apps:
    try:
        import json
        key_dict = json.loads(st.secrets["FIREBASE_KEY"])
        cred = credentials.Certificate(key_dict)
        firebase_admin.initialize_app(cred)
    except:
        KEY_PATH = "serviceAccountKey.json"
        if os.path.exists(KEY_PATH):
            cred = credentials.Certificate(KEY_PATH)
            firebase_admin.initialize_app(cred)
        else:
            st.error("Ошибка: не найден ключ Firebase!")
            st.stop()

db = firestore.client()

st.set_page_config(page_title="Мобильная зависимость", layout="wide")
st.title("Исследование мобильной зависимости среди студентов")
st.caption("Экранное время, отвлечение, попытки контроля")
st.markdown("---")

with st.form("survey_form"):
    st.subheader("1. Основная информация")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        age = st.radio("Ваш возраст", ["до 18 лет", "18-25 лет", "26-45 лет", "46-55 лет", "55 лет и старше"])
    with col2:
        gender = st.radio("Пол", ["Мужской", "Женский", "Не хочу указывать"])
    with col3:
        study_format = st.radio("Форма обучения", ["Очная", "Заочная", "Очно-заочная (вечерняя)"])
    with col4:
        work_status = st.radio("Работаете ли вы сейчас?", ["Да, совмещаю с учёбой", "Да, работаю (не учусь)", "Нет, но хочу работать", "Нет, не работаю и не хочу", "Планирую начать работать"])

    st.markdown("---")
    st.subheader("2. Экранное время")

    col5, col6 = st.columns(2)
    with col5:
        q4 = st.slider("Сколько часов в день вы проводите в телефоне?", 0, 20, 0)
        q5 = st.slider("Сколько часов в день вы проводите в соцсетях?", 0, 15, 0)
        q6 = st.slider("Сколько часов в день вы играете в игры на телефоне?", 0, 12, 0)
        q7 = st.slider("Сколько часов в день вы смотрите видео/TikTok/Reels?", 0, 15, 0)
        q8 = st.number_input("Сколько раз за день вы проверяете телефон?", 0, 300, 0)
        q9 = st.radio("Берёте ли вы телефон сразу после пробуждения?", ["Да, всегда", "Часто", "Иногда", "Редко", "Нет"])

    with col6:
        q10 = st.radio("Используете ли телефон перед сном в постели?", ["Да, всегда", "Часто", "Иногда", "Редко", "Нет"])
        q11 = st.select_slider("Сколько времени вы проводите в телефоне за один непрерывный сеанс?", options=["До 15 мин", "15-30 мин", "30-60 мин", "1-2 часа", "Более 2 часов"])
        q12 = st.radio("Просыпаетесь ли вы ночью, чтобы проверить телефон?", ["Да, регулярно", "Иногда", "Редко", "Никогда"])
        q13 = st.radio("Используете ли телефон во время еды?", ["Да, всегда", "Часто", "Иногда", "Редко", "Нет"])
        q14 = st.radio("Используете ли телефон в туалете?", ["Да, всегда", "Часто", "Иногда", "Редко", "Нет"])
        q15 = st.radio("Можете ли вы оставить телефон дома и не вернуться за ним?", ["Да, спокойно", "С трудом", "Нет, не могу", "Не пробовал(а)"])

    st.markdown("---")
    st.subheader("3. Отвлечение и концентрация")

    col7, col8 = st.columns(2)
    with col7:
        q16 = st.select_slider("Как часто телефон отвлекает вас от учёбы/работы?", options=["Никогда", "Очень редко", "Иногда", "Часто", "Очень часто", "Постоянно"])
        q17 = st.radio("Проверяете ли вы телефон во время выполнения важных задач?", ["Да, постоянно", "Часто", "Иногда", "Редко", "Нет"])
        q18 = st.radio("Проверяете ли вы телефон без конкретной причины?", ["Каждые 5-10 мин", "Каждые 15-30 мин", "Раз в час", "Реже", "Никогда"])
        q19 = st.radio("Используете ли телефон на парах/лекциях не по учёбе?", ["Да, постоянно", "Да, часто", "Иногда", "Редко", "Никогда"])
        q20 = st.radio("Мешает ли телефон вашему сну?", ["Да, сильно", "Да, немного", "Нет", "Не уверен(а)"])

    with col8:
        q21 = st.radio("Можете ли вы смотреть фильм/сериал, не отвлекаясь на телефон?", ["Да, легко", "С трудом", "Нет, постоянно отвлекаюсь", "Не пробовал(а)"])
        q22 = st.radio("Отвлекаетесь ли вы на уведомления во время разговора с людьми?", ["Да, постоянно", "Часто", "Иногда", "Редко", "Нет"])
        q23 = st.radio("Чувствуете ли вы тревогу, когда не можете найти телефон?", ["Да, сильную", "Да, лёгкую", "Нет", "Не замечал(а)"])
        q24 = st.radio("Проверяете ли вы телефон во время вождения/перехода дороги?", ["Да, часто", "Иногда", "Редко", "Никогда", "Не вожу"])
        q25 = st.radio("Снизилась ли ваша успеваемость из-за телефона?", ["Да, значительно", "Да, немного", "Нет", "Не уверен(а)"])

    st.markdown("---")
    st.subheader("4. Попытки контроля зависимости")

    col9, col10 = st.columns(2)
    with col9:
        q26 = st.radio("Пытались ли вы сократить экранное время?", ["Да, успешно", "Да, но безуспешно", "Планирую попробовать", "Нет, не вижу проблемы", "Нет, не нужно"])
        q27 = st.multiselect("Какие методы вы использовали для контроля?", ["Встроенный Screentime/Digital Wellbeing", "Лимиты на приложения", "Режим Не беспокоить", "Удаление приложений", "Приложения-таймеры (Forest и др.)", "Телефон в другой комнате", "Ничего не использовал", "Другое"])
        q28 = st.select_slider("Оцените ваш успех в контроле экранного времени", options=["Полный провал", "Небольшой прогресс", "Умеренный успех", "Большой успех", "Полный успех", "Не пытался(ась)"])
        q29 = st.radio("Как вы реагируете, если остались без телефона на час?", ["Спокойствие", "Лёгкое беспокойство", "Тревога", "Паника"])
        q30 = st.number_input("Какое было бы идеальное экранное время в день (в часах)?", 0, 10, 0)

    with col10:
        q31 = st.radio("Установлены ли у вас лимиты на приложения?", ["Да, на все соцсети", "Да, на некоторые", "Нет, но хочу", "Нет, не нужно"])
        q32 = st.radio("Выключаете ли вы уведомления для ненужных приложений?", ["Да, для всех ненужных", "Да, для некоторых", "Нет, все включены", "Не знал(а), что можно"])
        q33 = st.radio("Используете ли вы режим Не беспокоить во время учёбы?", ["Да, всегда", "Часто", "Иногда", "Редко", "Нет"])
        q34 = st.radio("Готовы ли вы пройти цифровой детокс (без телефона 24 часа)?", ["Да, легко", "Да, но страшно", "Нет, не смогу", "Не уверен(а)"])
        q35 = st.radio("Считаете ли вы себя зависимым от телефона?", ["Да, сильно", "Да, умеренно", "Скорее да", "Скорее нет", "Нет", "Не уверен(а)"])

    st.markdown("---")
    comment = st.text_area("Дополнительный комментарий или совет по контролю экранного времени")

    submitted = st.form_submit_button("Отправить ответ", use_container_width=True)

    if submitted:
        if not st.session_state.get("submitted_flag", False):
             st.session_state.submitted_flag = True

        doc_data = {
            "age": age,
            "gender": gender,
            "study_format": study_format,
            "work_status": work_status,
            "screen_time_hours": int(q4),
            "social_media_hours": int(q5),
            "games_hours": int(q6),
            "video_hours": int(q7),
            "phone_checks_per_day": int(q8),
            "morning_phone": q9,
            "night_phone": q10,
            "session_duration": q11,
            "night_wake_up": q12,
            "phone_during_meal": q13,
            "phone_in_toilet": q14,
            "leave_phone_home": q15,
            "distraction_study": q16,
            "distraction_tasks": q17,
            "check_without_reason": q18,
            "during_lectures": q19,
            "sleep_disruption": q20,
            "focus_on_movie": q21,
            "distraction_conversation": q22,
            "anxiety_without_phone": q23,
            "phone_while_driving": q24,
            "academic_decline": q25,
            "attempt_to_reduce": q26,
            "control_methods": q27,
            "control_success": q28,
            "reaction_without_phone": q29,
            "ideal_screen_time": int(q30),
            "app_limits_set": q31,
            "notifications_off": q32,
            "do_not_disturb": q33,
            "digital_detox_ready": q34,
            "self_assessment_addicted": q35,
            "comment": comment,
            "timestamp": datetime.utcnow()
        }
        try:
            db.collection("mobile_addiction_responses").add(doc_data)
            st.success("Спасибо! Ваш ответ сохранён.")
        except Exception as e:
            st.error(f"Ошибка сохранения: {e}")
            st.session_state.submitted_flag = False
    
st.markdown("---")
st.markdown("---")
if st.checkbox("Показать аналитику"):
    docs = db.collection("mobile_addiction_responses").stream()
    data = [doc.to_dict() for doc in docs]
    
    if not data:
        st.info("Пока нет ни одного ответа. Заполните форму первым!")
    else:
        df = pd.DataFrame(data)
                
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
        
        st.success(f"Всего собрано ответов: {len(df)}")

        st.markdown("### Выводы по собранным данным")
        
        col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
        
        with col_metrics1:
            if "screen_time_hours" in df.columns:
                avg_screen = df["screen_time_hours"].mean()
                st.metric("Среднее экранное время", f"{avg_screen:.1f} ч/день")
        
        with col_metrics2:
            if "self_assessment_addicted" in df.columns:
                percent_addicted = (df["self_assessment_addicted"].isin(["Да, сильно", "Да, умеренно"]).mean() * 100)
                st.metric("Считают себя зависимыми", f"{percent_addicted:.0f}%")
        
        with col_metrics3:
            if "attempt_to_reduce" in df.columns:
                percent_tried = (df["attempt_to_reduce"].isin(["Да, успешно", "Да, но безуспешно"]).mean() * 100)
                st.metric("Пытались сократить время", f"{percent_tried:.0f}%")
                
        tab1, tab2, tab3 = st.tabs(["Данные", "Графики", "Экспорт CSV"])
        
        with tab1:
            st.dataframe(df, use_container_width=True)
        
        with tab2:
            st.subheader("Графики анализа")
            
            if "screen_time_hours" in df.columns:
                df_clean = df.dropna(subset=["screen_time_hours"])
                if len(df_clean) > 0:
                    fig1 = px.histogram(df_clean, x="screen_time_hours", nbins=20, 
                                       title="Распределение экранного времени (часы в день)")
                    fig1.update_layout(xaxis_title="Часы в телефоне", yaxis_title="Количество человек")
                    st.plotly_chart(fig1, use_container_width=True)
            
            col_g1, col_g2 = st.columns(2)

            with col_g1:
                if "self_assessment_addicted" in df.columns:
                    addicted_counts = df["self_assessment_addicted"].dropna().value_counts()
                    if len(addicted_counts) > 0:
                        fig2 = px.pie(values=addicted_counts.values, names=addicted_counts.index,
                                     title="Самооценка мобильной зависимости")
                        st.plotly_chart(fig2, use_container_width=True)
                
                if "age" in df.columns:
                    age_counts = df["age"].dropna().value_counts()
                    if len(age_counts) > 0:
                        fig3 = px.bar(x=age_counts.index, y=age_counts.values,
                                     title="Распределение респондентов по возрасту")
                        fig3.update_layout(xaxis_title="Возраст", yaxis_title="Количество")
                        st.plotly_chart(fig3, use_container_width=True)
            
            with col_g2:
                if "attempt_to_reduce" in df.columns:
                    attempt_counts = df["attempt_to_reduce"].dropna().value_counts().head(5)
                    if len(attempt_counts) > 0:
                        fig4 = px.bar(x=attempt_counts.index, y=attempt_counts.values,
                                     title="Попытки сократить экранное время")
                        fig4.update_layout(xaxis_title="Ответ", yaxis_title="Количество")
                        st.plotly_chart(fig4, use_container_width=True)
                
                if "morning_phone" in df.columns:
                    morning_counts = df["morning_phone"].dropna().value_counts()
                    if len(morning_counts) > 0:
                        fig5 = px.pie(values=morning_counts.values, names=morning_counts.index,
                                     title="Телефон сразу после пробуждения")
                        st.plotly_chart(fig5, use_container_width=True)
            
            st.markdown("---")
            st.markdown("### Интерпретация результатов")
            
            if "screen_time_hours" in df.columns:
                avg_screen = df["screen_time_hours"].mean()
                st.write(f"Экранное время: В среднем студенты проводят в телефоне **{avg_screen:.1f} часов** в день.")
                if avg_screen > 5:
                    st.write("Это выше рекомендуемой нормы (3-5 часов), что может указывать на риск мобильной зависимости.")
            
            if "self_assessment_addicted" in df.columns:
                percent_addicted = (df["self_assessment_addicted"].isin(["Да, сильно", "Да, умеренно"]).mean() * 100)
                if percent_addicted > 50:
                    st.write(f"Самооценка: **{percent_addicted:.0f}%** респондентов признают себя зависимыми от телефона.")
            
            if "morning_phone" in df.columns:
                percent_morning = (df["morning_phone"] == "Да, всегда").mean() * 100
                st.write(f"Утренняя привычка: **{percent_morning:.0f}%** берут телефон сразу после пробуждения.")
            
            if "attempt_to_reduce" in df.columns:
                percent_tried = (df["attempt_to_reduce"].isin(["Да, успешно", "Да, но безуспешно"]).mean() * 100)
                st.write(f"Контроль: **{percent_tried:.0f}%** пытались сократить экранное время.")
                
                percent_success = (df["attempt_to_reduce"] == "Да, успешно").mean() * 100
                st.write(f"Из них успешно: **{percent_success:.0f}%**.")

        with tab3:
            st.subheader("Экспорт данных в CSV")
                        
            df_export = df.copy()
            df_export = df_export.fillna("Не указано")
            
            for col in df_export.columns:
                if df_export[col].dtype == object:
                    df_export[col] = df_export[col].astype(str)
                    df_export[col] = df_export[col].str.replace(r'[^\w\s,.()-]', '', regex=True)

            rename_dict = {
                "age": "Возраст",
                "gender": "Пол",
                "study_format": "Форма_обучения",
                "work_status": "Трудоустройство",
                "screen_time_hours": "Часы_в_телефоне",
                "social_media_hours": "Часы_в_соцсетях",
                "games_hours": "Часы_в_играх",
                "video_hours": "Часы_в_видео",
                "phone_checks_per_day": "Проверок_в_день",
                "morning_phone": "Телефон_утром",
                "night_phone": "Телефон_перед_сном",
                "attempt_to_reduce": "Попытки_контроля",
                "self_assessment_addicted": "Самооценка_зависимости",
                "comment": "Комментарий"
            }
            for old, new in rename_dict.items():
                if old in df_export.columns:
                    df_export = df_export.rename(columns={old: new})
            
            try:
                csv = df_export.to_csv(index=False, sep=';', encoding='windows-1251').encode('windows-1251')
                st.download_button(
                    "Скачать CSV", 
                    csv, 
                    f"survey_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", 
                    "text/csv"
                )
                st.caption("CSV файл сохранится в папку Загрузки")
            except Exception as e:
                st.error(f"Ошибка при подготовке CSV: {e}")