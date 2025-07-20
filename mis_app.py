import streamlit as st
import pandas as pd
import io
import traceback
from datetime import datetime

st.set_page_config(page_title="AP Solutions", layout="centered")

st.markdown("# 🧾 AP Solutions")
st.markdown("### Your Personal Excel MIS Assistant")

# Session state to store uploaded data
if "df" not in st.session_state:
    st.session_state.df = None
if "code" not in st.session_state:
    st.session_state.code = ""
if "filename" not in st.session_state:
    st.session_state.filename = "MIS_Report.xlsx"

# File uploader
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"], label_visibility="visible")

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.session_state.df = df

        st.success("File uploaded successfully!")
        st.markdown("### 📊 File Information:")
        st.write("**Columns:**", list(df.columns))
        st.write(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")

        # Prompt input
        st.markdown("---")
        st.markdown("### ✍️ Add prompt")
        prompt = st.text_area("Describe the steps to generate the MIS report:", height=200)
        filename = st.text_input("Enter name for the final Excel file (with .xlsx):", "MIS_Report.xlsx")

        if st.button("Generate Python Script"):
            try:
                # Very basic prompt-to-code logic (static example)
                if "Role is Basic DMA" in prompt:
                    code = f"""import pandas as pd\n\ndf = pd.read_excel('{uploaded_file.name}')\nfiltered_df = df[df['Role'] == 'Basic DMA'].copy()\nsoft_code_idx = filtered_df.columns.get_loc('Soft Code')\ncol_H_name = filtered_df.columns[7]\nfiltered_df.insert(soft_code_idx + 1, 'length', filtered_df[col_H_name].astype(str).apply(len))\nfiltered_by_length = filtered_df[filtered_df['length'].isin([11, 12, 13, 14, 15])]\nfinal_result = filtered_by_length[filtered_by_length['BUH'] == 'Raoul Kapoor']\nrequired_columns = ['Id', 'Full Name', 'Role', 'Mobile', 'Email', 'Soft Code', 'City', 'State', 'Pincode', 'Reporting Manager', 'Reporting Manager Soft Code', 'Sernior Manager', 'BUH', 'Firm Name', 'Created Date', 'Pan']\nfinal_result = final_result[[col for col in required_columns if col in final_result.columns]]\nfinal_result.to_excel('{filename}', index=False)"""
                    st.session_state.code = code
                    st.code(code, language='python')

                    confirm = st.radio("Do you want to run this script?", ["Confirm", "Edit the prompt"])

                    if confirm == "Confirm":
                        try:
                            local_df = st.session_state.df
                            filtered_df = local_df[local_df['Role'] == 'Basic DMA'].copy()
                            soft_code_idx = filtered_df.columns.get_loc('Soft Code')
                            col_H_name = filtered_df.columns[7]
                            filtered_df.insert(soft_code_idx + 1, 'length', filtered_df[col_H_name].astype(str).apply(len))
                            filtered_by_length = filtered_df[filtered_df['length'].isin([11, 12, 13, 14, 15])]
                            final_result = filtered_by_length[filtered_by_length['BUH'] == 'Raoul Kapoor']
                            required_columns = ['Id', 'Full Name', 'Role', 'Mobile', 'Email', 'Soft Code', 'City', 'State', 'Pincode', 'Reporting Manager', 'Reporting Manager Soft Code', 'Sernior Manager', 'BUH', 'Firm Name', 'Created Date', 'Pan']
                            final_result = final_result[[col for col in required_columns if col in final_result.columns]]

                            towrite = io.BytesIO()
                            final_result.to_excel(towrite, index=False, engine='openpyxl')
                            towrite.seek(0)

                            st.success("MIS report generated successfully!")
                            st.download_button(label="📥 Download MIS Report", data=towrite, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

                        except Exception as e:
                            st.error("Error while running script:")
                            st.exception(traceback.format_exc())

                else:
                    st.warning("Prompt not recognized. Try describing the logic more clearly.")

            except Exception as e:
                st.error("Error while processing prompt:")
                st.exception(traceback.format_exc())

    except Exception as e:
        st.error("Failed to read Excel file:")
        st.exception(traceback.format_exc())
