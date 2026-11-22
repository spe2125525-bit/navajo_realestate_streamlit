import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Navajo County, AZ Real Estate Trends",
    layout="wide"
)

COUNTY_NAME = "Navajo, AZ"
DATA_COLUMNS = (
    "Month",
    "Median_Listing_Price",
    "Active_Listing_Count",
    "Median_Days_on_Market",
    "Price_Per_SqFt",
    "New_Listing_Count",
    "Price_Reduced_Count",
)

# Monthly RDC data: month, median price, active listings, days on market,
# price per square foot, new listings, and price reductions.
INVENTORY_RECORDS = [
    ('201607', 259839.0, 1164, 84.0, 144.0, 196, 254.0),
    ('201608', 259357.0, 1124, 95.0, 142.0, 184, 222.0),
    ('201609', 257000.0, 1068, 110.0, 140.0, 170, 190.0),
    ('201610', 259900.0, 973, 117.0, 141.0, 120, 148.0),
    ('201611', 254925.0, 865, 119.0, 140.0, 122, 74.0),
    ('201612', 249900.0, 777, 134.0, 139.0, 76, 56.0),
    ('201701', 249575.0, 705, 140.0, 140.0, 110, 40.0),
    ('201702', 249450.0, 695, 142.0, 139.0, 132, 84.0),
    ('201703', 259950.0, 727, 123.0, 141.0, 242, 90.0),
    ('201704', 259900.0, 872, 64.0, 142.0, 276, 104.0),
    ('201705', 265000.0, 996, 61.0, 144.0, 304, 160.0),
    ('201706', 267000.0, 1016, 66.0, 146.0, 242, 176.0),
    ('201707', 269900.0, 1003, 78.0, 145.0, 256, 192.0),
    ('201708', 269925.0, 985, 86.0, 146.0, 200, 222.0),
    ('201709', 270000.0, 907, 91.0, 148.0, 188, 188.0),
    ('201710', 275000.0, 817, 102.0, 149.0, 124, 134.0),
    ('201711', 269000.0, 744, 111.0, 148.0, 98, 82.0),
    ('201712', 269450.0, 664, 124.0, 149.0, 80, 56.0),
    ('201801', 269675.0, 616, 135.0, 148.0, 98, 54.0),
    ('201802', 271717.0, 591, 127.0, 150.0, 128, 50.0),
    ('201803', 269900.0, 605, 106.0, 150.0, 200, 88.0),
    ('201804', 282000.0, 679, 69.0, 151.0, 238, 72.0),
    ('201805', 287875.0, 716, 61.0, 152.0, 254, 120.0),
    ('201806', 293000.0, 757, 64.0, 157.0, 232, 172.0),
    ('201807', 289975.0, 796, 61.0, 155.0, 262, 182.0),
    ('201808', 297250.0, 791, 72.0, 157.0, 236, 224.0),
    ('201809', 294900.0, 752, 78.0, 154.0, 188, 172.0),
    ('201810', 299300.0, 681, 93.0, 156.0, 128, 126.0),
    ('201811', 299900.0, 606, 100.0, 153.0, 110, 82.0),
    ('201812', 295750.0, 552, 114.0, 153.0, 92, 60.0),
    ('201901', 284975.0, 509, 119.0, 152.0, 116, 60.0),
    ('201902', 281950.0, 520, 117.0, 154.0, 150, 64.0),
    ('201903', 291500.0, 552, 97.0, 156.0, 156, 64.0),
    ('201904', 297125.0, 596, 72.0, 157.0, 220, 96.0),
    ('201905', 298663.0, 674, 55.0, 164.0, 310, 100.0),
    ('201906', 294450.0, 735, 58.0, 164.0, 224, 144.0),
    ('201907', 279769.0, 749, 66.0, 161.0, 222, 190.0),
    ('201908', 283555.0, 711, 76.0, 163.0, 168, 192.0),
    ('201909', 289430.0, 649, 85.0, 164.0, 150, 146.0),
    ('201910', 293347.0, 593, 93.0, 165.0, 134, 116.0),
    ('201911', 289900.0, 524, 99.0, 164.0, 108, 84.0),
    ('201912', 285975.0, 473, 112.0, 165.0, 42, 42.0),
    ('202001', 283925.0, 421, 120.0, 164.0, 114, 48.0),
    ('202002', 289000.0, 423, 104.0, 165.0, 136, 68.0),
    ('202003', 289125.0, 445, 70.0, 168.0, 164, 64.0),
    ('202004', 289925.0, 482, 63.0, 169.0, 138, 60.0),
    ('202005', 309250.0, 467, 71.0, 170.0, 192, 96.0),
    ('202006', 328119.0, 421, 63.0, 175.0, 232, 92.0),
    ('202007', 346900.0, 357, 46.0, 177.0, 236, 102.0),
    ('202008', 324900.0, 292, 39.0, 181.0, 248, 84.0),
    ('202009', 325000.0, 262, 35.0, 184.0, 206, 84.0),
    ('202010', 325000.0, 227, 41.0, 187.0, 196, 44.0),
    ('202011', 322500.0, 205, 48.0, 188.0, 116, 40.0),
    ('202012', 331250.0, 175, 65.0, 188.0, 64, 20.0),
    ('202101', 355000.0, 155, 73.0, 184.0, 96, 20.0),
    ('202102', 371750.0, 125, 64.0, 190.0, 112, 18.0),
    ('202103', 391150.0, 132, 30.0, 191.0, 154, 18.0),
    ('202104', 384325.0, 161, 26.0, 196.0, 176, 48.0),
    ('202105', 399900.0, 171, 29.0, 211.0, 188, 36.0),
    ('202106', 419074.0, 210, 25.0, 222.0, 208, 48.0),
    ('202107', 399900.0, 250, 31.0, 225.0, 228, 72.0),
    ('202108', 397000.0, 247, 33.0, 233.0, 258, 62.0),
    ('202109', 449375.0, 243, 39.0, 242.0, 174, 68.0),
    ('202110', 460000.0, 200, 49.0, 246.0, 136, 64.0),
    ('202111', 446900.0, 177, 39.0, 245.0, 142, 48.0),
    ('202112', 444725.0, 168, 45.0, 252.0, 82, 34.0),
    ('202201', 454450.0, 146, 54.0, 260.0, 108, 24.0),
    ('202202', 477225.0, 151, 41.0, 263.0, 122, 30.0),
    ('202203', 484950.0, 161, 36.0, 259.0, 154, 38.0),
    ('202204', 495000.0, 210, 32.0, 270.0, 184, 68.0),
    ('202205', 499651.0, 274, 30.0, 272.0, 252, 128.0),
    ('202206', 498722.0, 372, 30.0, 270.0, 260, 218.0),
    ('202207', 474900.0, 438, 38.0, 271.0, 204, 220.0),
    ('202208', 469450.0, 421, 53.0, 268.0, 128, 216.0),
    ('202209', 457000.0, 393, 65.0, 269.0, 194, 196.0),
    ('202210', 467000.0, 373, 71.0, 270.0, 132, 132.0),
    ('202211', 491500.0, 348, 67.0, 272.0, 102, 96.0),
    ('202212', 494425.0, 314, 77.0, 277.0, 76, 76.0),
    ('202301', 471975.0, 298, 88.0, 270.0, 56, 82.0),
    ('202302', 499000.0, 275, 94.0, 273.0, 74, 50.0),
    ('202303', 495725.0, 284, 71.0, 274.0, 128, 64.0),
    ('202304', 485000.0, 360, 45.0, 285.0, 164, 116.0),
    ('202305', 491342.0, 433, 43.0, 295.0, 234, 150.0),
    ('202306', 489450.0, 472, 50.0, 288.0, 178, 180.0),
    ('202307', 499000.0, 475, 54.0, 288.0, 192, 208.0),
    ('202308', 499000.0, 478, 60.0, 288.0, 204, 198.0),
    ('202309', 499000.0, 478, 62.0, 284.0, 152, 244.0),
    ('202310', 492450.0, 471, 66.0, 275.0, 126, 160.0),
    ('202311', 495000.0, 467, 71.0, 276.0, 88, 140.0),
    ('202312', 495000.0, 416, 86.0, 283.0, 52, 80.0),
    ('202401', 497000.0, 316, 103.0, 282.0, 72, 80.0),
    ('202402', 500000.0, 336, 92.0, 285.0, 134, 76.0),
    ('202403', 499900.0, 412, 46.0, 290.0, 192, 124.0),
    ('202404', 499000.0, 542, 51.0, 291.0, 190, 152.0),
    ('202405', 499000.0, 669, 55.0, 293.0, 230, 192.0),
    ('202406', 499500.0, 731, 65.0, 295.0, 140, 272.0),
    ('202407', 499900.0, 629, 69.0, 295.0, 154, 282.0),
    ('202408', 499999.0, 586, 78.0, 291.0, 204, 216.0),
    ('202409', 514875.0, 549, 86.0, 297.0, 116, 220.0),
    ('202410', 512237.0, 529, 80.0, 295.0, 112, 160.0),
    ('202411', 495000.0, 479, 93.0, 289.0, 88, 100.0),
    ('202412', 472450.0, 374, 105.0, 286.0, 54, 66.0),
    ('202501', 457250.0, 342, 106.0, 285.0, 102, 64.0),
    ('202502', 480875.0, 359, 97.0, 288.0, 134, 118.0),
    ('202503', 497000.0, 429, 51.0, 289.0, 188, 116.0),
    ('202504', 499950.0, 554, 48.0, 291.0, 228, 162.0),
    ('202505', 529000.0, 674, 52.0, 298.0, 264, 188.0),
    ('202506', 522000.0, 719, 63.0, 298.0, 176, 280.0),
    ('202507', 514725.0, 735, 70.0, 297.0, 174, 306.0),
    ('202508', 515000.0, 754, 78.0, 297.0, 196, 280.0),
    ('202509', 520200.0, 751, 79.0, 297.0, 156, 210.0),
    ('202510', 498650.0, 715, 84.0, 297.0, 118, 234.0),
    ('202511', 495000.0, 670, 95.0, 296.0, 96, 152.0),
    ('202512', 489450.0, 584, 111.0, 298.0, 62, 62.0),
    ('202601', 489950.0, 532, 115.0, 297.0, 96, 92.0),
    ('202602', 479250.0, 500, 96.0, 291.0, 152, 114.0),
    ('202603', 487000.0, 597, 57.0, 296.0, 276, 166.0),
    ('202604', 493588.0, 725, 49.0, 300.0, 234, 186.0),
    ('202605', 494450.0, 822, 58.0, 300.0, 260, 248.0),
    ('202606', 491950.0, 900, 70.0, 297.0, 216, 312.0),
    ('202607', 485000.0, 907, 76.0, 293.0, 170, 384.0),
    ('202608', 480000.0, 885, 85.0, 290.0, 188, 328.0),
    ('202609', 482425.0, 844, 88.0, 287.0, 164, 270.0),
    ('202610', 480000.0, 823, 95.0, 287.0, 136, 228.0),
]


def load_inventory_data():
    df = pd.DataFrame.from_records(INVENTORY_RECORDS, columns=DATA_COLUMNS)
    df.insert(0, "Date", pd.to_datetime(df.pop("Month"), format="%Y%m"))
    df.insert(1, "County", COUNTY_NAME)
    df.insert(2, "County_FIPS", "04017")
    df["Year"] = df["Date"].dt.year
    return df


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

st.title("Navajo County Housing Market")
st.markdown(
    "Track home prices, listing activity, and time on market in Navajo County, "
    "Arizona. Use the year slider to explore monthly trends."
)
st.caption("Monthly Realtor.com county inventory data, July 2016–October 2026.")
st.caption("Data from: https://www.realtor.com/research/data/")

df = load_inventory_data()
st.sidebar.header("Explore")
min_year, max_year = int(df["Year"].min()), int(df["Year"].max())
year_range = st.sidebar.slider(
    "Years to show",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
)
filtered_df = df[df["Year"].between(*year_range)]

if filtered_df.empty:
    st.warning("No records found for the selected filters.")
    st.stop()

latest_price, price_change, average_days_on_market, active_listings = (
    calculate_summary_metrics(filtered_df)
)
period_start = filtered_df["Date"].iloc[0].strftime("%b %Y")
period_end = filtered_df["Date"].iloc[-1].strftime("%b %Y")

col1, col2, col3, col4 = st.columns(4)
col1.metric(
    "Median listing price",
    f"${latest_price:,.0f}",
    help=f"At the end of the selected period ({period_end}).",
)
col2.metric(
    "Price change",
    f"{price_change:+.1f}%",
    help=f"Change from {period_start} to {period_end}.",
)
col3.metric(
    "Average days on market",
    f"{average_days_on_market:.0f} days",
    help="Average of the monthly median days on market in this period.",
)
col4.metric(
    "Homes listed",
    f"{active_listings:,.0f}",
    help=f"Active listings at the end of the selected period ({period_end}).",
)

st.divider()

tab1, tab2, tab3 = st.tabs([
    "Home prices",
    "Listings and time on market",
    "Monthly data",
])
chart_df = filtered_df.set_index("Date")

with tab1:
    st.subheader("Median listing price")
    st.line_chart(chart_df["Median_Listing_Price"])
    
    if chart_df["Price_Per_SqFt"].notna().any():
        st.subheader("Median price per square foot")
        st.line_chart(chart_df["Price_Per_SqFt"])

with tab2:
    left_col, right_col = st.columns(2)
    with left_col:
        st.subheader("Active listings")
        st.bar_chart(chart_df["Active_Listing_Count"])
    with right_col:
        st.subheader("Median days on market")
        st.line_chart(chart_df["Median_Days_on_Market"])

with tab3:
    st.subheader(f"Monthly market data for {COUNTY_NAME}")
    display_df = filtered_df.drop(columns="Year").rename(columns={
        "Date": "Month",
        "County_FIPS": "County FIPS",
        "Median_Listing_Price": "Median listing price",
        "Active_Listing_Count": "Active listings",
        "Median_Days_on_Market": "Median days on market",
        "Price_Per_SqFt": "Price per square foot",
        "New_Listing_Count": "New listings",
        "Price_Reduced_Count": "Price reductions",
    })
    display_df["Month"] = display_df["Month"].dt.strftime("%b %Y")
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    csv_bytes = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download selected data (CSV)",
        data=csv_bytes,
        file_name=f"navajo-market-{year_range[0]}-{year_range[1]}.csv",
        mime="text/csv",
    )
