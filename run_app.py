import streamlit as st
import pandas as pd

def transform_to_brand_view(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes the raw DataFrame with 'Top Clicked Brand #1', 'Top Clicked Product #1: ...'
    etc. and creates a brand-level DataFrame where each brand-keyword-product
    combination is a single row.
    """
    rows = []

    # Go row by row. Each row = a particular Search Term + up to 3 top-clicked brands/products.
    for i, r in df.iterrows():
        search_term = r["Search Term"]

        # BRAND 1
        brand1 = r["Top Clicked Brand #1"]
        prod_asin1 = r["Top Clicked Product #1: ASIN"]
        prod_title1 = r["Top Clicked Product #1: Product Title"]
        click_share1 = r["Top Clicked Product #1: Click Share"]
        conv_share1 = r["Top Clicked Product #1: Conversion Share"]
        rows.append({
            "Search Term": search_term,
            "Brand": brand1,
            "ASIN": prod_asin1,
            "Product Title": prod_title1,
            "Click Share": click_share1,
            "Conversion Share": conv_share1
        })

        # BRAND 2
        brand2 = r["Top Clicked Brands #2"]
        prod_asin2 = r["Top Clicked Product #2: ASIN"]
        prod_title2 = r["Top Clicked Product #2: Product Title"]
        click_share2 = r["Top Clicked Product #2: Click Share"]
        conv_share2 = r["Top Clicked Product #2: Conversion Share"]
        rows.append({
            "Search Term": search_term,
            "Brand": brand2,
            "ASIN": prod_asin2,
            "Product Title": prod_title2,
            "Click Share": click_share2,
            "Conversion Share": conv_share2
        })

        # BRAND 3
        brand3 = r["Top Clicked Brands #3"]
        prod_asin3 = r["Top Clicked Product #3: ASIN"]
        prod_title3 = r["Top Clicked Product #3: Product Title"]
        click_share3 = r["Top Clicked Product #3: Click Share"]
        conv_share3 = r["Top Clicked Product #3: Conversion Share"]
        rows.append({
            "Search Term": search_term,
            "Brand": brand3,
            "ASIN": prod_asin3,
            "Product Title": prod_title3,
            "Click Share": click_share3,
            "Conversion Share": conv_share3
        })

    # Convert the list of dicts into a new DataFrame
    brand_df = pd.DataFrame(rows)

    # Clean up data types if needed
    brand_df["Click Share"] = pd.to_numeric(brand_df["Click Share"], errors="coerce")
    brand_df["Conversion Share"] = pd.to_numeric(brand_df["Conversion Share"], errors="coerce")

    return brand_df

def main():
    st.title("Saw Palmetto Brand-Keyword Analysis")

    uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file:
        # Read the file
        if uploaded_file.name.endswith(".csv"):
            # If your CSV has a “Reporting Range” line above the header:
            df = pd.read_csv(uploaded_file, header=1, encoding="utf-8-sig")
        else:
            # for XLSX
            df = pd.read_excel(uploaded_file)

        # Clean up column names (remove quotes, trim whitespace)
        df.columns = df.columns.str.replace('"', '', regex=False)
        df.columns = df.columns.str.strip()

        st.subheader("Raw Data Preview")
        st.dataframe(df.head())

        # Transform the data to brand-level
        brand_df = transform_to_brand_view(df)

        st.subheader("Brand-Level Data")
        st.dataframe(brand_df.head(10))

        # Group by brand to list all keywords driving their sales
        # We'll just display them by brand. You can do advanced stats (sum or avg).
        unique_brands = brand_df["Brand"].dropna().unique()

        for brand in unique_brands:
            st.markdown(f"## Brand: **{brand}**")

            # Filter brand-specific data
            brand_data = brand_df[brand_df["Brand"] == brand]

            # Sort by click share descending if you want
            brand_data_sorted = brand_data.sort_values(by="Click Share", ascending=False)

            # Display top N or everything
            st.write(brand_data_sorted[[
                "Search Term",
                "ASIN",
                "Product Title",
                "Click Share",
                "Conversion Share"
            ]])

    else:
        st.info("Please upload your CSV/Excel file to continue.")

if __name__ == "__main__":
    main()
