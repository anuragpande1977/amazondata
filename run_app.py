import streamlit as st
import pandas as pd

def main():
    st.title("Saw Palmetto Data Analysis")

    # 1. File Upload
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv", "xlsx"])
    if uploaded_file is not None:
        # 2. Read the file
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # 3. Show a preview
        st.subheader("Data Preview")
        st.dataframe(df.head(10))

        # 4. Top-clicked product (#1) per search term
        #    For each row, you have "Search Term" and "Top Clicked Product #1: Product Title".
        st.subheader("Top Clicked Product #1 by Search Term")
        for idx, row in df.iterrows():
            st.write(f"**Search Term**: {row['Search Term']}")
            st.write(f"- **Product Title**: {row['Top Clicked Product #1: Product Title']}")
            st.write(f"- **Brand**: {row['Top Clicked Brand #1']}")
            st.write(f"- **Click Share**: {row['Top Clicked Product #1: Click Share']}")
            st.write("---")

        # 5. Find the single highest-clicked product (#1) across all rows
        #    (the row with the maximum “Top Clicked Product #1: Click Share”)
        df['Top Clicked Product #1: Click Share'] = pd.to_numeric(
            df['Top Clicked Product #1: Click Share'], errors='coerce'
        )
        max_click_share_idx = df['Top Clicked Product #1: Click Share'].idxmax()
        top_clicked = df.loc[max_click_share_idx]

        st.subheader("Overall Highest-Clicked Product (#1) in the Dataset")
        st.write(f"**Search Term**: {top_clicked['Search Term']}")
        st.write(f"**Product Title**: {top_clicked['Top Clicked Product #1: Product Title']}")
        st.write(f"**Brand**: {top_clicked['Top Clicked Brand #1']}")
        st.write(f"**Click Share**: {top_clicked['Top Clicked Product #1: Click Share']}")

        # 6. Optional: Show keywords associated with that top product
        #    We’ll look for all rows containing the same Product ASIN or Title
        st.subheader("Keywords Associated with this Top-Clicked Product")
        top_clicked_asin = top_clicked['Top Clicked Product #1: ASIN']
        # Filter to see if the same ASIN appears in other search terms
        associated_keywords = df[df['Top Clicked Product #1: ASIN'] == top_clicked_asin]['Search Term'].unique()
        st.write(", ".join(associated_keywords))

    else:
        st.info("Please upload your CSV/Excel file to analyze.")

if __name__ == "__main__":
    main()
