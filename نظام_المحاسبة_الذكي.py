import pandas as pd
from sklearn.linear_model import LinearRegression
import streamlit as st


st.title(" نظام المحاسبة الذكي الذاتي")
st.markdown("رفع ملف Excel يحتوي على البيانات المالية وتحليلها وتنبؤ الأرباح")

excel_file = st.file_uploader("📁 اختر ملف Excel بالبيانات المالية", type=['xlsx'])

if excel_file is not None:

    data = pd.read_excel(excel_file)

    data['ربح'] = data['إيرادات'] - data['مصروفات']
    data['نسبة الربح'] = (data['ربح'] / data['إيرادات'] * 100).round(2)


    X = data[['مصروفات']]
    y = data['إيرادات']
    model = LinearRegression()
    model.fit(X, y)


    new_expense_value = st.slider("اختر مصروف الشهر الجديد:", int(data['مصروفات'].min()), int(data['مصروفات'].max()*2), int(data['مصروفات'].mean()))

    new_expense = pd.DataFrame({'مصروفات':[new_expense_value]})
    predicted_revenue = model.predict(new_expense)[0]
    predicted_profit = predicted_revenue - new_expense_value
    predicted_profit_percentage = round(predicted_profit / predicted_revenue * 100, 2)

    st.subheader("توقعات الشهر الجديد:")
    st.metric(label="الإيرادات المتوقعة", value=f"{predicted_revenue:.2f}")
    st.metric(label="الربح المتوقع", value=f"{predicted_profit:.2f}", delta=f"{predicted_profit_percentage}%")


    future_months = ['يونيو','يوليو','أغسطس','سبتمبر','أكتوبر','نوفمبر']
    future_expenses = [new_expense_value + i*100 for i in range(6)]
    future_data = pd.DataFrame({'شهر': future_months, 'مصروفات': future_expenses})
    future_data['إيرادات'] = model.predict(future_data[['مصروفات']])
    future_data['ربح'] = future_data['إيرادات'] - future_data['مصروفات']
    future_data['نسبة الربح'] = (future_data['ربح'] / future_data['إيرادات'] * 100).round(2)


    full_data = pd.concat([data, future_data], ignore_index=True)


    def risk_color(profit):
        if profit < 0:
            return '🔴 خسارة'
        elif profit < 500:
            return '🟠 مخاطر متوسطة'
        else:
            return '🟢 جيد'

    full_data['مؤشر المخاطر'] = full_data['ربح'].apply(risk_color)

    st.subheader("البيانات المالية مع التنبؤات:")
    st.dataframe(full_data)


    st.subheader("📈 الرسم البياني للأداء المالي")
    st.line_chart(full_data[['مصروفات', 'إيرادات', 'ربح']])


    latest_profit = future_data['ربح'].iloc[0]
    if latest_profit < 0:
        st.error("⚠️ تنبيه: الشهر القادم المتوقع فيه خسارة مالية!")
    elif latest_profit < 500:
        st.warning("⚠️ الشهر القادم فيه ربح منخفض، راقب المصروفات.")
    else:
        st.success("✅ الشهر القادم المتوقع ربح جيد. الوضع المالي مستقر.")

else:
    st.info("ℹ️ من فضلك قم برفع ملف Excel بالبيانات المالية للبدء.")
