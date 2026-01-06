import streamlit as st
import pikepdf
import io

st.set_page_config(page_title="PDF Unlocker", page_icon="🔓")
st.title("🔓 PDF Unlocker")

uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
password = st.text_input("Enter PDF Password", type="password")

if st.button("Unlock Files"):
    if uploaded_files and password:
        for uploaded_file in uploaded_files:
            try:
                with pikepdf.Pdf.open(uploaded_file, password=password) as pdf:
                    output_buffer = io.BytesIO()
                    pdf.save(output_buffer)
                    output_buffer.seek(0)
                    new_filename = f"{uploaded_file.name.replace('.pdf', '')}_unlocked.pdf"
                    st.download_button(f"⬇️ Download {new_filename}", data=output_buffer, file_name=new_filename)
            except:
                st.error(f"Error unlocking {uploaded_file.name}")