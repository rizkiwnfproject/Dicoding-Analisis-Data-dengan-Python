import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='white')

# Load Data
day_df = pd.read_csv("dashboard/main_data.csv")
# Convert to datetime
day_df["dteday"] = pd.to_datetime(day_df["dteday"])

# function for get season and the sum
def get_season(df):
    return df.groupby("season")["cnt"].agg(["mean", "sum"]).reset_index()

# function for get working day and the sum
def get_workingday(df):
    return df.groupby("workingday")["cnt"].agg(["mean", "sum"]).reset_index()

# function for get holiday and the sum
def get_holiday(df):
    return df.groupby("holiday")["cnt"].agg(["mean", "sum"]).reset_index()

# function for get weekday and the sum
def get_weekday(df):
    return df.groupby("weekday")["cnt"].agg(["mean", "sum"]).reset_index()

# function for get month and the sum
def get_monthly(df):
    return df.groupby("mnth")["cnt"].agg(["mean", "sum"]).reset_index()

# function for get temprature and the sum
def get_temp_correlation(df):
    return df[["temp", "cnt"]].corr().iloc[0, 1]

def get_weathersit(df):
    return df.groupby("weathersit")["cnt"].agg(["mean", "sum"]).reset_index()

def categorize_rentals(cnt, avg):
    if cnt > avg * 1:
        return "Ramai"
    elif cnt < avg * 0.8:
        return "Sepi"
    else:
        return "Sedang"


######### Sidebar Filter
# add logo
st.sidebar.image("logo.jpeg", use_container_width=True)
st.sidebar.header("Range Date")
start_date, end_date = st.sidebar.date_input("Choose the range date : ", [day_df["dteday"].min(), day_df["dteday"].max()])

# Filter by date
filtered_day_df = day_df[(day_df["dteday"] >= str(start_date)) & (day_df["dteday"] <= str(end_date))]

# Header Dashboard
st.title("Bikes Sharing Analysis Dashboard 🚲 (By Days)")


# 1. Distribusi Penyewaan Sepeda Berdasarkan Musim
st.header("Analisis Keterkaitan Musim dengan Jumlah Penyewa Sepeda")
season = get_season(filtered_day_df).rename(columns={
    "season": "Season",
    "mean": "Rata-rata Per Hari",
    "sum": "Total Sewa Per Hari"
})
season["Season"] = season.Season.apply(lambda x: "Spinger" if x == 1 else ("Summer" if x == 2 else ("Fall" if x == 3 else "Winter")))
st.dataframe(season)

fig, ax = plt.subplots(figsize=(8, 5))
sns.set_style("whitegrid")
custom_palette = sns.color_palette("icefire", n_colors=4)
sns.barplot(data=season, x="Season", y="Rata-rata Per Hari", ax=ax, palette=custom_palette)

ax.set_title("Rata-rata Per Hari Sepeda per Musim", fontsize=14, fontweight="bold")
ax.set_xlabel("Musim", fontsize=12)
ax.set_ylabel("Rata-rata Jumlah Penyewaan", fontsize=12)
st.pyplot(fig)

st.write("### Kesimpulan:")
st.write("- Adanya musim sangat berpengaruh pada penyewaan sepeda. contohnya pada musim gugur atau fall, rata-rata jumlah penyewaan sepedanya tertinggi dibandingkan dengan musim lainnya. Hal ini kemungkinan disebabkan karena cuaca yang sedang hangat, tidak terlalu panas dan tidak terlalu dingin. sedangkan pada musim salju atau winter kemudian musim semi, cenderung jumlah penyewanya rendah.")


# 2. Pola Penyewaan Sepeda Berdasarkan Hari Kerja & Hari Libur
st.header("Analisis Keterkaitan Pola Hari Kerja terhadap Jumlah Penyewa Sepeda")
st.subheader("Working Day")
workingday = get_workingday(filtered_day_df).rename(columns={
    "workingday": "working day",
    "mean": "Rata-rata Per Hari",
    "sum": "Total Sewa Per Hari"
})
workingday["working day"] = workingday["working day"].apply(lambda x: "Bukan Hari Kerja" if x == 0 else "Hari Kerja")
st.dataframe(workingday)

fig, ax = plt.subplots()
sns.set_style("whitegrid")
sns.barplot(data=workingday, x="working day", y="Rata-rata Per Hari", ax=ax, palette=custom_palette)
ax.set_title("Rata-rata Penyewa Sepeda per Hari Kerja", fontsize=14, fontweight="bold")
ax.set_xlabel("Hari Kerja")
ax.set_ylabel("Rata-rata Per Hari")
st.pyplot(fig)


st.subheader("Weekday")
weekday = get_weekday(filtered_day_df).rename(columns={
    "weekday": "Weekday",
    "mean": "Rata-rata Per Hari",
    "sum": "Total Sewa Per Hari"
})
weekday["Weekday"] = weekday["Weekday"].apply(lambda x: "Monday" if x == 1 else ("Tuesday" if x == 2 else ("Wednesday" if x == 3 else ("Thursday" if x == 4 else ("Friday" if x == 5 else ("Saturday" if x == 6 else "Sunday"))))))
st.dataframe(weekday)

fig, ax = plt.subplots()
sns.set_style("whitegrid")
custom_palette_2 = sns.color_palette("rocket_r", n_colors=12)
sns.barplot(data=weekday, x="Weekday", y="Rata-rata Per Hari", ax=ax, palette=custom_palette_2)
ax.set_title("Rata-rata Penyewa Sepeda per Hari", fontsize=14, fontweight="bold")
ax.set_xlabel("Day")
ax.set_ylabel("Rata-rata Per Hari")
ax.set_xticklabels(weekday["Weekday"], rotation=45, fontsize="9")
st.pyplot(fig)

st.subheader("Holiday")
holiday = get_holiday(filtered_day_df).rename(columns={
    "holiday": "Holiday",
    "mean": "Rata-rata Per Hari",
    "sum": "Total Sewa Per Hari"
})
holiday["Holiday"] = holiday["Holiday"].apply(lambda x: "Bukan Hari Libur" if x == 0 else "Hari Libur")
st.dataframe(holiday)

fig, ax = plt.subplots()
sns.set_style("whitegrid")
sns.barplot(data=holiday, x="Holiday", y="Rata-rata Per Hari", ax=ax, palette=custom_palette)
ax.set_title("Rata-rata Penyewa Sepeda per Hari Libur", fontsize=14, fontweight="bold")
ax.set_xlabel("Hari Kerja")
ax.set_ylabel("Rata-rata Per Hari")
st.pyplot(fig)

st.write("### Kesimpulan:")
st.write("- Perbedaan hari juga berpengaruh pada penyewaan sepeda. Pada hari kerja seperti senin-jum'at penyewaannya lebih tinggi dibandingkan hari minggu atau hari libur. Saat hari libur, cenderung terjadi penurunan penyewaan sepeda. Hal ini kemungkinan disebabkan karena sepeda menjadi alat transportasi untuk pergi ke kantor atau transportasi biasa dibandingkan dengan alat untuk pergi liburan atau rekreasi.")



# 3. Pola Penyewaan Sepeda Berdasarkan Bulan
st.header("Analisis Keterkaitan Bulan terhadap Jumlah Penyewa Sepeda")
monthly = get_monthly(filtered_day_df).rename(columns={
    "mnth": "Month",
    "mean": "Rata-rata Per Bulan",
    "sum": "Total Sewa Per Bulan"
})
monthly["Month"] = monthly["Month"].apply(lambda x: "January" if x == 1 else ("February" if x == 2 else ("March" if x == 3 else ("April" if x == 4 else ("May" if x == 5 else ("June" if x == 6 else ("July" if x == 7 else ("August" if x == 8 else ("September" if x == 9 else ("October" if x == 10 else ("November" if x == 11 else "December")))))))))))

st.dataframe(monthly)

fig, ax = plt.subplots()
sns.set_style("whitegrid")
sns.barplot(data=monthly, x="Month", y="Rata-rata Per Bulan", ax=ax, palette=custom_palette_2)
ax.set_title("Rata-rata Penyewa Sepeda per Bulan", fontsize=14, fontweight="bold")
ax.set_xlabel("Month")
ax.set_ylabel("Rata-rata Per Bulan")
ax.set_xticklabels(monthly["Month"], rotation=45, fontsize="9")
st.pyplot(fig)

st.write("### Kesimpulan:")
st.write("- Setiap bulan juga menunjukkan perbedaan minat penyewa. setelah dicari tahu, ternyata terkait dengan musim, untuk maret-september itu musim semi, panas kemudian dilanjut oleh musim gugur, ini menjadi bulan yang ramai untuk penyewa sepeda. Berbeda halnya dengan bulan desember sampai Februari karena saat itu musim dingin, sehingga kurang mendukung aktivitas untuk bersepeda. Sehingga kemungkinan Cuaca juga menjadi faktor untuk naik turunnya jumlah penyepeda.")


# 4. Hubungan antara Suhu dan Penyewaan Sepeda
st.header("Analisis Keterkaitan Suhu terhadap Jumlah Penyewa Sepeda")
st.subheader("Temprature")
corr_value = get_temp_correlation(filtered_day_df)
st.metric("Korelasi antara Suhu dan Penyewaan", f"{corr_value:.2f}")
fig, ax = plt.subplots()
sns.set_style("whitegrid")
sns.scatterplot(data=filtered_day_df, x="temp", y="cnt", ax=ax, palette=custom_palette)
ax.set_title("Rata-rata Penyewa Sepeda per Temprature", fontsize=14, fontweight="bold")
ax.set_xlabel("Suhu")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

st.subheader("Weathersit")
weathersit = get_weathersit(filtered_day_df).rename(columns={
    "weathersit": "Weather",
    "mean": "Rata-rata Per Cuaca",
    "sum": "Total Sewa Per Cuaca"
})
weathersit["Weather"] = weathersit["Weather"].apply(lambda x: "Clear" if x == 1 else ("Cloudy" if x == 2 else ("Light Snow" if x == 3 else "Heavy Rain") ))
st.dataframe(weathersit)

fig, ax = plt.subplots()
sns.set_style("whitegrid")
sns.barplot(data=weathersit, x="Weather", y="Rata-rata Per Cuaca", ax=ax, palette=custom_palette)
ax.set_title("Rata-rata Penyewa Sepeda per Cuaca", fontsize=14, fontweight="bold")
ax.set_xlabel("Weather")
ax.set_ylabel("Rata-rata Per Cuaca")
st.pyplot(fig)

st.write("### Kesimpulan:")
st.write("- Semakin tinggi suhu, semakin banyak penyewa sepeda, namun hanya sampai titik tertentu. Hal ini membuktikan bahwa penyepeda lebih suka di suhu hangat dibandingkan suhu dingin atau saat panas. Kemungkinan pada saat suhu dingin, penyepeda menggunakan kendaraan lainnya yang lebih tertutup dan lebih hangat.")



# Pengelompokan suasana berdasarkan rata-rata jumlah penyewa dengan rata-rata pertahun
st.header("Pengelompokan Suasana Berdasarkan Rata-rata Jumlah Penyewa Sepeda")
year_avg = day_df.groupby("yr")["cnt"].mean().reset_index()
year_avg.rename(columns={"cnt": "rata_rata_pertahun"}, inplace=True)
if "rata_rata_tahun" in day_df.columns:
    day_df.drop(columns=["rata_rata_tahun"], inplace=True)
day_df = day_df.merge(year_avg, on="yr", how="left")
day_df["Kategori_Penyewaan"] = day_df.apply(lambda row: categorize_rentals(row["cnt"], row["rata_rata_pertahun"]), axis=1)


fig, ax = plt.subplots()
sns.countplot(x=day_df["mnth"], hue=day_df["Kategori_Penyewaan"], palette="viridis")
ax.set_title("Distribusi Kategori Penyewaan Sepeda per Bulan")
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Hari selama 2 tahun")
ax.legend(title="Kategori Penyewaan", loc='upper right')
st.pyplot(fig)

st.write("### Kesimpulan:")
st.write("Tujuan dari Pengelompokan dengan kategori 'sepi', 'sedang', 'ramai' adalah untuk memudahkan dalam membaca bagaimana keadaan bulan tersebut. Dengan disatukannya hari dalam sebulan pada tahun 2011-2012. sehingga dalam 1 bulan setidaknya ada 60 hari. untuk grafiknya itu dibaca perhari. contohnya adalah pada bulan januari 60 hari sepi dan 2 hari sedang. kemudian untuk analisisnya seperti berikut : ")
st.write("- Untuk kategori sepi, bulan januari sampai maret sangat meningkat dibandingkan dengan bulan-bulan sebelumnya. bahkan tidak ramai")
st.write("- Untuk bulan yang ramai itu mulai bulan april sampai oktober. kemudian turun lagi grafiknya pada bulan oktober")


st.write("### Kesimpulan Umum:")
st.write("- Musim, cuaca, suhu, serta perbedaan hari kerja dan hari libur sangat berpengaruh pada intesitas dan pola dari penyewaan sepeda. ")
st.write("- Pada musim yang paling banyak penyewa sepeda yaitu musim gugur. ")
st.write("- Pada cuaca, penyewa sepeda lebih memilih untuk bersepeda di cuaca hangat")
st.write("- Pada hari, penyewa sepeda lebih suka bersepeda pada hari kerja dari pada hari weekend atau hari libur.")
st.write("Dengan hal ini dapat dijadikan peluang untuk bisnis penyewaan sepeda, kemudian dapat dilakukan promosi pada saat bulan desember-februari untuk meningkatkan jumlah penyewa sepeda.")
