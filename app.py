import streamlit as st
import json
from db import insert_quote, fetch_all_quotes
from generate_pdf import create_pdf
from llm_client import query_lm_studio

# Load brand/model config
with open("brand_models.json", "r") as f:
    brands = json.load(f)

st.set_page_config(page_title="Sales Quotation Generator", layout="centered")
st.title("📄 Sales Quotation Generator")

# ---------------- Sidebar Quote History ----------------
st.sidebar.subheader("🧾 Quote History")
if st.sidebar.button("View All Quotes"):
    try:
        quotes = fetch_all_quotes()
        if quotes:
            for q in quotes:
                st.sidebar.markdown(f"**#{q['id']} - {q['customer_name']}**")
                st.sidebar.markdown(f"- {q['brand']} {q['model']}")
                st.sidebar.markdown(f"- 💰 ${q['price']}")
                st.sidebar.markdown(f"- 🕒 {q['created_at'].strftime('%Y-%m-%d')}")
                st.sidebar.markdown("---")
        else:
            st.sidebar.info("No quotes found.")
    except Exception as e:
        st.sidebar.error(f"Error: {e}")

# ---------------- Main Form ----------------
customer_name = st.text_input("Customer Name")
brand = st.selectbox("Select Brand", list(brands.keys()))

contact = brands[brand]
models = contact["models"]
model_names = [m["model"] for m in models]
model_selected = st.selectbox("Select Model", model_names)

model_info = next(m for m in models if m["model"] == model_selected)
price = model_info["price"]
description = model_info.get("description", "")
category = model_info.get("category", "")

# Contact info
contact_name = contact["contact_name"]
contact_email = contact["email"]
contact_phone = contact["phone"]
company = contact["company"]

# Display product info
st.markdown(f"💰 **Price:** ${price:,}")
st.markdown(f"🏷️ **Category:** {category}")
st.markdown(f"📄 **Product Description:** {description}")
st.markdown("---")
st.markdown(f"""
**Sales Contact:**  
📇 {contact_name}  
📧 {contact_email}  
📞 {contact_phone}  
🏢 {company}
""")

# Prompt for LLM
prompt = f"""
Write a professional sales quotation email.

Include:
- Greeting: Dear {customer_name},
- Product: {model_selected}
- Description: {description}
- Category: {category}
- Brand: {brand}
- Price: ${price}
- Delivery estimate: 7–10 business days
- Contact: {contact_name}, {contact_email}, {contact_phone}, {company}
- Closing: thank-you and contact invitation
"""

# Load quote from session or init
if "quote_text" not in st.session_state:
    st.session_state.quote_text = ""

# Generate quote
if st.button("🔁 Generate Quote"):
    with st.spinner("Generating quote..."):
        try:
            quote = query_lm_studio(prompt)
            if len(quote.split()) < 20:
                st.warning("⚠️ Quote too short. Try again.")
            else:
                st.session_state.quote_text = quote
                st.success("✅ Quote generated successfully!")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# Show stored quote if available
if st.session_state.quote_text:
    st.markdown("### ✉️ Quotation Preview")
    st.text_area("Quotation Text", value=st.session_state.quote_text, height=300, key="quote_display")

    if st.button("✅ Save Quote & Generate PDF"):
        quote_id = insert_quote(customer_name, brand, model_selected, price, st.session_state.quote_text)
        pdf_path = create_pdf(quote_id, customer_name, brand, model_selected, price, st.session_state.quote_text)
        st.success(f"📌 Saved with ID #{quote_id}")
        with open(pdf_path, "rb") as f:
            st.download_button("📥 Download PDF", f, file_name=f"quote_{quote_id}.pdf")