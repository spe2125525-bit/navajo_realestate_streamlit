import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

st.set_page_config(
    page_title="Navajo County, AZ Real Estate Trends",
    layout="wide"
)

INVENTORY_CSV = Path(__file__).resolve().with_name(
    "Navajo_County_Inventory.csv"
)
METRIC_COLUMNS = {
    "county_fips": "County_FIPS",
    "median_listing_price": "Median_Listing_Price",
    "active_listing_count": "Active_Listing_Count",
    "median_days_on_market": "Median_Days_on_Market",
    "median_listing_price_per_square_foot": "Price_Per_SqFt",
    "new_listing_count": "New_Listing_Count",
    "price_reduced_count": "Price_Reduced_Count",
}


@st.cache_data
def parse_realtor_csv(uploaded_file, county_filter=None, source_version=None):
    relevant_columns = {"month_date_yyyymm", "county_name", *METRIC_COLUMNS}
    raw_df = pd.read_csv(
        uploaded_file,
        usecols=lambda column: column.strip().lower() in relevant_columns,
    )
    if (
        source_version is not None
        and Path(uploaded_file).stat().st_mtime_ns != source_version
    ):
        raise RuntimeError(
            "The inventory CSV changed while it was being loaded. Rerun the app."
        )
    raw_df.columns = [c.strip().lower() for c in raw_df.columns]

    if county_filter is not None:
        raw_df = raw_df[
            raw_df["county_name"].fillna("").str.strip().str.casefold()
            == county_filter.casefold()
        ]

    raw_df["Date"] = pd.to_datetime(
        raw_df["month_date_yyyymm"].astype(str),
        format="%Y%m",
        errors="coerce",
    )
    raw_df = raw_df.dropna(subset=["Date"])

    def format_county(name):
        county, separator, state = str(name).partition(",")
        if not separator:
            return county.title()
        return f"{county.strip().title()}, {state.strip().upper()}"

    cleaned_df = pd.DataFrame({
        "Date": raw_df["Date"],
        "County": raw_df["county_name"].apply(format_county),
    })
    for source, target in METRIC_COLUMNS.items():
        values = raw_df[source] if source in raw_df else np.nan
        cleaned_df[target] = pd.to_numeric(values, errors="coerce")

    cleaned_df["Year"] = cleaned_df["Date"].dt.year
    return cleaned_df.sort_values("Date").reset_index(drop=True)


def calculate_summary_metrics(df):
    prices = df["Median_Listing_Price"]
    start_price, latest_price = prices.iloc[0], prices.iloc[-1]
    price_change = (latest_price - start_price) / start_price * 100 if start_price > 0 else 0
    return (
        latest_price,
        price_change,
        df["Median_Days_on_Market"].mean(),
        df["Active_Listing_Count"].iloc[-1],
    )

st.title("Navajo County, AZ Real Estate Market Explorer")
st.markdown(
    "Analyze multi-year housing market trends, listing prices, active inventory, "
    "and days on market using Realtor.com county historical metrics."
)

st.sidebar.header("1. Data Source")
uploaded_file = st.sidebar.file_uploader(
    "Upload a replacement Realtor.com County CSV",
    type=["csv"],
    help="Supports Realtor.com County Historical Inventory CSV files."
)

try:
    if uploaded_file is not None:
        df = parse_realtor_csv(uploaded_file)
        if df.empty:
            raise ValueError("The uploaded CSV contains no valid county records.")
    else:
        if not INVENTORY_CSV.is_file():
            raise FileNotFoundError(f"Inventory CSV not found: {INVENTORY_CSV}")
        file_modified_time = INVENTORY_CSV.stat().st_mtime_ns
        df = parse_realtor_csv(
            str(INVENTORY_CSV),
            county_filter="navajo, az",
            source_version=file_modified_time,
        )
        if df.empty:
            raise ValueError("The inventory CSV does not contain Navajo County records.")
except Exception as error:
    st.error(f"Could not load market data: {error}")
    st.stop()

st.sidebar.success(f"Loaded {len(df):,} records.")

st.sidebar.header("2. Filter Controls")

available_counties = sorted(df["County"].unique())
default_county = "Navajo, AZ"
default_index = (
    available_counties.index(default_county)
    if default_county in available_counties
    else 0
)
selected_county = st.sidebar.selectbox(
    "Select County",
    available_counties,
    index=default_index,
)

county_df = df[df["County"] == selected_county].copy()
min_year, max_year = int(county_df["Year"].min()), int(county_df["Year"].max())

if min_year < max_year:
    year_range = st.sidebar.slider(
        "Select Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
    )
    filtered_df = county_df[county_df["Year"].between(*year_range)]
else:
    year_range = (min_year, max_year)
    filtered_df = county_df

if filtered_df.empty:
    st.warning("No records found for the selected filters.")
    st.stop()

latest_price, total_growth, avg_dom, latest_inv = calculate_summary_metrics(filtered_df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Latest Median Listing Price", f"${latest_price:,.0f}")
col2.metric(f"Price Change ({year_range[0]}-{year_range[1]})", f"{total_growth:+.1f}%")
col3.metric("Avg. Days on Market", f"{avg_dom:.0f} days")
col4.metric("Latest Active Listings", f"{latest_inv:,.0f} homes")

st.divider()

tab1, tab2, tab3 = st.tabs([
    "Listing Price Trends",
    "Inventory and Days on Market",
    "Filtered Data Table",
])
chart_df = filtered_df.set_index("Date")

with tab1:
    st.subheader(f"{selected_county} - Median Listing Price ($)")
    st.line_chart(chart_df["Median_Listing_Price"])
    
    if chart_df["Price_Per_SqFt"].notna().any():
        st.subheader(f"{selected_county} - Median Price per Square Foot ($)")
        st.line_chart(chart_df["Price_Per_SqFt"])

with tab2:
    left_col, right_col = st.columns(2)
    with left_col:
        st.subheader("Active Listing Count")
        st.bar_chart(chart_df["Active_Listing_Count"])
    with right_col:
        st.subheader("Median Days on Market")
        st.line_chart(chart_df["Median_Days_on_Market"])

with tab3:
    st.subheader(f"{selected_county} Filtered Records")
    display_df = filtered_df.drop(columns="Year").copy()
    display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    csv_bytes = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Filtered County Data (CSV)",
        data=csv_bytes,
        file_name=f"{selected_county.lower().replace(', ', '_')}_housing_trends.csv",
        mime="text/csv",
    )
