import streamlit as st
import graphs as g
import counter as c
import ticket_sales as ts
import re

files = {}
names = []

st.markdown("""<div style='border:1px solid black; padding: 10px'><h1 style='text-align: center; color: black;'>Event Data Analysis Dashboard </h1></div>""", unsafe_allow_html=True)

title_alignment= """
    <style>
    h1 {
      text-align: center;
    }
    </style>
    """

st.write("Upload EventSalesReport file.")

uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)

# Iterate over uploaded files
for uploaded_file in uploaded_files:
    files[uploaded_file.name] = uploaded_file
    names.append(uploaded_file.name)


# Check if at least one file is uploaded
if len(files) >= 1:
    st.subheader("Data Analysis Options")
    # Show the 'Process' button

    if st.button("Process Sum of Prices"):
        file_found = False
        for name in names:
            if re.search("^EventSalesReportDetailed", name):

                c.build(files[name])
                file_found = True

        if not file_found:
                st.write("you do not have the correct files uploaded")

    if st.button("Process future events"):
        file_found = False
        for name in names:
            if re.search("^EventSalesReportDetailed", name):

                ts.build(files[name])
                file_found = True

        if not file_found:
                st.write("you do not have the correct files uploaded")

    if st.button("Process historic data"):
        file_found = False
        # Call the build function from the graphs module with the first file
        for name in names:
            if re.search("^EventSalesReportDetailed",name):

                g.build(files[name])
                file_found = True
        if not file_found:
                st.write("you do not have the correct files uploaded")
else:
    st.warning("Please upload a file and ensure it is the right file")

st.markdown(
    """
    <style>
        .stButton>button {
            background-color: #FFFFFF;
            color: #000000;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 10px auto;
            cursor: pointer;
            border-radius: 8px;
            border: 2px solid #000000;
            width: auto;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #000000;
            color: #FFFFFF;
        }
        .stButton>button:active {
            background-color: #000000;
            color: #FFFFFF;
        }
        .stButton>button:focus {
            outline: none;
        }
        .stButton>button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
