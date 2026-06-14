import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Bigganbaksho Order Processor", layout="wide")

st.title("📦 Bigganbaksho Order Converter (Final Version)")
st.markdown("এই অ্যাপটি আপনার গুগল শীটের ফরম্যাট অনুযায়ী ডাটা সাজাবে। 'Total Qty' কলামটি বাদ দেওয়া হয়েছে।")

# ১. সুনির্দিষ্ট প্রোডাক্ট ম্যাপিং ডিকশনারি
MAPPING = {
    "আলোর ঝলক": "ALOR JHALAK",
    "চুম্বকের চমক": "CHUMBAKER CHAMAK",
    "তড়িৎ তাণ্ডব": "TARIT TANDOB",
    "রসায়ন রহস্য": "RASHAYON RAHOSSHO",
    "অদ্ভুত মাপজোখ": "ODVUT MAPJOKH",
    "ট্যানগ্রাম": "MAGNETIC TANGRAM",
    "পঞ্চম শ্রেণি": "CLASS FIVE Kit",
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

# ২. ফাইল আপলোড
uploaded_file = st.file_uploader("ওয়েবসাইটের এক্সেল ফাইলটি আপলোড করুন", type=['xlsx', 'csv'])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        grouped = df.groupby('Order Number', sort=False)
        final_data = []
        
        for order_id, group in grouped:
            first_row = group.iloc[0]
            
            row_dict = {
                "Name": f"{str(first_row.get('First Name (Billing)', ''))} {str(first_row.get('Last Name (Billing)', ''))}".strip(),
                "Contact Number": first_row.get('Phone (Billing)', ''),
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
            
        # ৩. আউটপুট কলাম (Total Qty বাদ দিয়ে)
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
        st.success(f"সফলভাবে {len(result_df)} টি অর্ডার প্রসেস করা হয়েছে!")
        st.dataframe(result_df)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            result_df.to_excel(writer, index=False)
        
        st.download_button(label="গুগল শীট ফাইল ডাউনলোড করুন", data=output.getvalue(), 
                           file_name="Bigganbaksho_Final_Orders.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        
    except Exception as e:
        st.error(f"Error: {e}")
