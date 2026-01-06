import streamlit as st
import pikepdf
import io

# 1. Page Configuration
st.set_page_config(page_title="PDF Unlocker", page_icon="🔓")

st.title("🔓 Free PDF Unlocker")
st.write("Upload password-protected PDF files to remove the password instantly.")

# 2. File Uploader (Replaces tkinter filedialog)
uploaded_files = st.file_uploader(
    "Choose PDF files", 
    type="pdf", 
    accept_multiple_files=True
)

# 3. Password Input (Replaces tkinter simpledialog)
password = st.text_input("Enter PDF Password", type="password")

# 4. Process Button
if st.button("Unlock Files"):
    if not uploaded_files:
        st.warning("Please upload at least one file.")
    elif not password:
        st.warning("Please enter the password.")
    else:
        success_count = 0
        
        # Create a visual spinner while processing
        with st.spinner('Unlocking files...'):
            for uploaded_file in uploaded_files:
                try:
                    # Streamlit uploads are bytes, so we open them directly
                    with pikepdf.Pdf.open(uploaded_file, password=password) as pdf:
                        
                        # Save the unlocked PDF to a memory buffer (RAM) instead of disk
                        output_buffer = io.BytesIO()
                        pdf.save(output_buffer)
                        output_buffer.seek(0)
                        
                        # Create a download button for the new file
                        new_filename = f"{uploaded_file.name.replace('.pdf', '')}_unlocked.pdf"
                        
                        st.success(f"✅ Successfully unlocked: {uploaded_file.name}")
                        
                        # Show the download button
                        st.download_button(
                            label=f"⬇️ Download {new_filename}",
                            data=output_buffer,
                            file_name=new_filename,
                            mime="application/pdf"
                        )
                        success_count += 1
                        
                except pikepdf.PasswordError:
                    st.error(f"❌ Incorrect password for: {uploaded_file.name}")
                except Exception as e:
                    st.error(f"❌ Error processing {uploaded_file.name}: {e}")

        if success_count == len(uploaded_files):
            st.balloons()  # Fun animation on total success