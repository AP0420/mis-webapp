import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="MIS Automation", layout="wide", page_icon="📊")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@800&display=swap');

    .holo-header {
        position: relative;
        font-family: 'Orbitron', sans-serif;
        font-size: 60px;
        color: #00ffcc;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 30px;
        opacity: 0;
        animation: fadeIn 2s ease forwards, floatHeader 4s ease-in-out infinite;
        text-shadow:
            0 0 5px #00ffcc,
            0 0 10px #00ffcc,
            0 0 20px #00ffcc,
            0 0 40px #00ffcc,
            0 0 80px #00e6b8,
            0 0 100px #00e6b8;
        overflow: hidden;
    }

    .holo-header::before {
        content: '';
        position: absolute;
        top: -100%;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            180deg,
            transparent 0%,
            rgba(0, 255, 204, 0.2) 50%,
            transparent 100%
        );
        animation: shimmer 3s linear infinite;
        pointer-events: none;
    }

    @keyframes floatHeader {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-12px); }
    }

    @keyframes fadeIn {
        to { opacity: 1; }
    }

    @keyframes shimmer {
        0% { top: -100%; }
        100% { top: 100%; }
    }

    textarea, .stTextArea textarea {
        background-color: black !important;
        color: white !important;
        font-family: 'Courier New', monospace;
    }

    .stTextInput input {
        background-color: black !important;
        color: white !important;
    }
    </style>

    <div class="holo-header">AP Solutions</div>
""", unsafe_allow_html=True)

st.markdown("### Upload Excel File")
uploaded_file = st.file_uploader("Choose a file", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.write("#### Preview of Uploaded Data:")
    st.dataframe(df)

    prompt = st.text_area("🧠 Prompt to Generate Script:", placeholder="e.g., Filter rows where BUH is 'Raoul Kapoor' and Mobile number length is 11–15...", height=150)

    if "generated_code" not in st.session_state:
        st.session_state.generated_code = ""

    if st.button("Generate Python Code"):
        if prompt:
            with st.spinner("Generating code from prompt..."):
                try:
                    import openai
                    openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else "sk-REPLACE-YOUR-API-KEY"

                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant that writes clean, working Python pandas code."},
                            {"role": "user", "content": f"DataFrame is named df. {prompt}"}
                        ]
                    )
                    code = response.choices[0].message.content.strip("`python\n")
                    st.session_state.generated_code = code
                except Exception as e:
                    st.error(f"Error generating code: {e}")

    edited_script = st.text_area("📝 Edit the Python script if needed", value=st.session_state.generated_code, height=300)

    if st.button("Run Script"):
        try:
            local_env = {"df": df.copy(), "pd": pd}
            exec(edited_script, local_env)
            result_df = local_env.get("df")
            st.success("Script executed successfully!")
            st.write("### Result Preview:")
            st.dataframe(result_df)

            towrite = io.BytesIO()
            result_df.to_excel(towrite, index=False, engine='openpyxl')
            towrite.seek(0)
            st.download_button("📥 Download Result", towrite, file_name="Filtered_MIS_Result.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        except Exception as e:
            st.error(f"Error running script: {e}")
