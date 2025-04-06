import streamlit as st

def apply_mobile_styles():
    st.markdown("""
        <style>
            @media (max-width: 768px) {
                section[data-testid="stSidebar"] {
                    display: none !important;
                }
                .main .block-container {
                    padding: 1rem 1rem 10rem;
                    width: 100% !important;
                }
                h1 {
                    font-size: 1.5rem !important;
                }
                h2 {
                    font-size: 1.3rem !important;
                }
                .stButton button {
                    min-width: 100px;
                    padding: 0.5rem;
                }
            }
        </style>
    """, unsafe_allow_html=True)
