
# Bikes Sharing Analysis Dashboard

Dalam analisis ini bertujuan meneliti data bike sharing untuk memahami pola penyewaan sepeda berdasarkan berbagai faktor seperti hari, bulan, cuaca, dan waktu. Dengan fokus utama adalah menjawab beberapa pertanyaan bisnis yang dapat membantu mengidentifikasi tren penggunaan sepeda serta faktor-faktor yang memengaruhinya. Pertanyaan tersebut antara lain : 
1. Bagaimana pengaruh musim(season) terhadap jumlah penyewaan sepeda?
2. Apakah ada perbedaan pola penyewaan antara hari kerja dan sewaktu libur?
3. Adakah bulan yang diminati oleh pengguna, dan kenapa?
4. Bagaimana hubungan antara suhu dan jumlah penyewaan sepeda?

## Installation Conda
- Buka Website Anaconda : https://www.anaconda.com/download#Downloads atau Miniconda : https://www.anaconda.com/docs/getting-started/miniconda/install#quickstart-install-instructions
- Ikuti step-step pada halaman instalasinya
- Buka Environtment Variables
- Klik path, lalu klik new, tambahkan :
  - C:\Users\<YourUsername>\anaconda3\Scripts\
  - C:\Users\<YourUsername>\anaconda3\
- Kemudian restart Command Prompt
- Coba Jalankan  : 
  ```bash
  $ conda create --name main-ds python=3.9
  $ conda activate main-ds
  $ pip install numpy pandas matplotlib seaborn
  ```

## Run steamlit app on local device
Masuk kedalam folder submission -> dashboard, kemudian jalankan : 
  ```bash
  $ streamlit run dashboard.py
  ```

## Run steamlit app on browser
  ```bash
  https://rizkiwnfanlpython.streamlit.app/
  ```
    
