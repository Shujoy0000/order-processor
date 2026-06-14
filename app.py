import streamlit as st
import pandas as pd
import io
import os

st.set_page_config(page_title="Bigganbaksho Order Converter", layout="wide", page_icon="🚀")

# বিজ্ঞানবাক্স লোগো এবং টাইটেল
col1, col2 = st.columns([1, 6])
with col1:
    # যদি logo.png ফোল্ডারে থাকে তবে দেখাবে, নয়তো টেক্সট দেখাবে
    if os.path.exists("logo.png"):
        st.image("logo.png", width=120)
with col2:
    st.title("Bigganbaksho Order Converter (Web App Developed By-Shujoy Shaha)")

# আপনার দেওয়া স্লোগান ও সাবটাইটেল
st.markdown("### ম্যানুয়েল কাজের দিন শেষ, বিজ্ঞানবাক্সে বাংলাদেশ")
st.write("অন্যরকম বাংলাদেশের স্বপ্ন নিয়ে")

# ১. প্রোডাক্ট ম্যাপিং ডিকশনারি
MAPPING = {
    "আলোর ঝলক": "ALOR JHALAK",
    "চুম্বকের চমক": "CHUMBAKER CHAMAK",
    "তড়িৎ তাণ্ডব": "TARIT TANDOB",
    "রসায়ন রহস্য": "RASHAYON RAHOSSHO",
    "অদ্ভুত মাপজোখ": "ODVUT MAPJOKH",
    "ট্যানগ্রাম": "MAGNETIC TANGRAM",
    "পঞ্চম শ্রেণি": "CLASS FIVE Kit",
    "ফোকাস চ্যালেঞ্জ": "FOCUS CHALLENGE- BANGLA VERSION",
    "ফোকাস চ্যালেঞ্জ কিট": "FOCUS CHALLENGE- BANGLA VERSION",
    "মজার পেরিস্কোপ": "MOJAR PERISCOPE",
    "Mystery of Chemistry": "MYSTERY OF CHEMISTRY",
    "Amazing Electricity": "AMAZING ELECTRICITY",
    "Fun with Measurement": "FUN WITH MEASUREMENT",
    "Magic of Magnet": "MAGIC OF MAGNET",
    "Color of Light": "COLOR OF LIGHT",
    "Focus Challenge": "FOCUS CHALLENGE- ENGLISH VERSION",
    "মহাকাশের জগৎ": "MOHAKASHER JAGAT",
    "ব্রেইন বুস্টার": "Brain Booster",
    "Power Of Personality": "Power Of Personality"
}

# ফোন নম্বর ঠিক করার ফাংশন
def clean_phone(phone):
    if not phone: return ""
    p = str(phone).strip()
    if p.endswith('.0'): p = p[:-2]
    if p.startswith('880'): p = '0' + p[3:]
    if p.startswith('+880'): p = '0' + p[4:]
    if not p.startswith('0') and len(p) > 5: p = '0' + p
    return p

# ফাইল আপলোড সেকশন
uploaded_file = st.file_uploader("ওয়েবসাইটের এক্সেল ফাইলটি আপলোড করুন", type=['xlsx', 'csv'])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, dtype={'Phone (Billing)': str, 'Order Number': str})
        else:
            df = pd.read_excel(uploaded_file, dtype={'Phone (Billing)': str, 'Order Number': str})
        
        df = df.fillna("")
        grouped = df.groupby('Order Number', sort=False)
        final_data = []
        
        for order_id, group in grouped:
            first_row = group.iloc[0]
            
            # নাম ও ফোন প্রসেসিং
            first_n = str(first_row.get('First Name (Billing)', '')).strip()
            last_n = str(first_row.get('Last Name (Billing)', '')).strip()
            full_name = f"{first_n} {last_n}".strip()
            phone_num = clean_phone(first_row.get('Phone (Billing)', ''))
            
            row_dict = {
                "Name": full_name,
                "Contact Number": phone_num,
                "Address": first_row.get('Address 1&2 (Billing)', ''),
                "District": first_row.get('City (Billing)', ''),
                "Sub District": "",
                "Total Amount": "", 
                "Shipping Charge": first_row.get('Order Shipping Amount', 0),
                "Discount": first_row.get('Cart Discount Amount', 0),
                "Invoice ID": order_id,
                "Order Collector": "",
                "Source": "Website Bigganbaksho.com",
                "AD ID": first_row.get('Customer Note', ''),
                "Profession": "", "Class": "", "Age": "", "User Name": "", "Birth Date": ""
            }
            
            slot = 1
            for _, item in group.iterrows():
                raw_name = str(item.get('Item Name', '')).replace('- additional', '').strip()
                qty = item.get('Quantity (- Refund)', 0)

                if raw_name == "ব্রেইন ডেভেলপমেন্ট প্যাকেজ":
                    bundle = ["MAGNETIC TANGRAM", "FOCUS CHALLENGE- BANGLA VERSION", "Brain Booster"]
                    for b_name in bundle:
                        if slot <= 15:
                            row_dict[f"Product Name-{slot}"] = b_name
                            row_dict[f"Product Price-{slot}"] = ""
                            row_dict[f"Product QTY-{slot}"] = qty
                            slot += 1
                else:
                    if slot <= 15:
                        final_name = MAPPING.get(raw_name, raw_name)
                        row_dict[f"Product Name-{slot}"] = final_name
                        row_dict[f"Product Price-{slot}"] = ""
                        row_dict[f"Product QTY-{slot}"] = qty
                        slot += 1
            
            final_data.append(row_dict)
            
        output_columns = [
            "Name", "Contact Number", "Address", "District", "Sub District", 
            "Total Amount", "Shipping Charge", "Discount", "Invoice ID", 
            "Order Collector", "Source", "Product Name-1", "Product Price-1", "Product QTY-1",
            "Profession", "Class", "Age", "User Name", "Birth Date", "AD ID",
            "Product Name-2", "Product Price-2", "Product QTY-2",
            "Product Name-3", "Product Price-3", "Product QTY-3",
            "Product Name-4", "Product Price-4", "Product QTY-4",
            "Product Name-5", "Product Price-5", "Product QTY-5",
            "Product Name-6", "Product Price-6", "Product QTY-6",
            "Product Name-7", "Product Price-7", "Product QTY-7",
            "Product Name-8", "Product Price-8", "Product QTY-8",
            "Product Name-9", "Product Price-9", "Product QTY-9",
            "Product Name-10", "Product Price-10", "Product QTY-10",
            "Product Name-11", "Product Price-11", "Product QTY-11",
            "Product Name-12", "Product Price-12", "Product QTY-12",
            "Product Name-13", "Product Price-13", "Product QTY-13",
            "Product Name-14", "Product Price-14", "Product QTY-14",
            "Product Name-15", "Product Price-15", "Product QTY-15"
        ]
        
        result_df = pd.DataFrame(final_data).reindex(columns=output_columns, fill_value="")
        result_df.index = result_df.index + 1

        st.success(f"সফলভাবে {len(result_df)} টি অর্ডার প্রসেস করা হয়েছে!")
        st.dataframe(result_df)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            result_df.to_excel(writer, index=False, sheet_name='Orders')
            workbook  = writer.book
            worksheet = writer.sheets['Orders']
            text_format = workbook.add_format({'num_format': '@'})
            worksheet.set_column('B:B', 20, text_format)

        st.download_button(label="গুগল শীট ফাইল ডাউনলোড করুন", data=output.getvalue(), 
                           file_name="Bigganbaksho_Final_Orders.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        
    except Exception as e:
        st.error(f"Error: {e}")
