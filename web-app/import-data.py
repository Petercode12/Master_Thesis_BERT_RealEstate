import csv
import psycopg2

# Connecting to the geeks database
connection = psycopg2.connect(
    host="129.146.248.20",
    port="5432", #default
    database="ttndung",
    user="tdung",
    password="8M44Ck48wn3J")

# Creating a cursor object to execute
# SQL queries on a database table
cursor = connection.cursor()

# # Opening the data.csv file
# file = open('data_all_processed_id.csv', encoding="utf8")

# Reading the contents of the
# data_all_processed_id.csv file
# contents = csv.reader(file)
# contents = next(contents)  # skip the headers
# SQL query to insert data into the
# House_house table
delete_records = 'DELETE FROM house_houses'
insert_records_ancu = 'INSERT INTO house_houses (house_id, "LoaiHinh", "TacGia", "SoDienThoai", "Gia", "DienTich", "DiaChi") SELECT a.id, a.type, a.post_author, a.phone_number, a.price_with_unit, a.area ,a.address FROM app_ancu_scraper a'
insert_records_dangbannhadat = 'INSERT INTO house_houses (house_id, "LoaiHinh", "TacGia", "SoDienThoai", "Gia", "DienTich", "DiaChi") SELECT a.id, a.type, a.post_author, a.phone_number, a.price_with_unit, a.area ,a.address FROM app_dangbannhadat_scraper a WHERE a.type IS NOT NULL'
insert_records_nhadat24h = 'INSERT INTO house_houses (house_id, "LoaiHinh", "TacGia", "SoDienThoai", "Gia", "DienTich", "DiaChi", "ChungNhanSoHuu") SELECT a.id, a.type, a.post_author, a.phone_number, a.price_with_unit, a.area ,a.address, a.legal FROM app_nhadat24h_scraper a WHERE a.phone_number IS NOT NULL'
insert_records_muaban = 'INSERT INTO house_houses (house_id, "LoaiHinh", "TacGia", "SoDienThoai", "Gia", "DienTich", "DiaChi", "ChungNhanSoHuu") SELECT a.id, a.type, a.post_author, a.phone_number, a.price_with_unit, a.land_area ,a.address, a.legal FROM app_muabannet_scraper a'

# Importing the contents of the file
# into our house table
cursor.execute(delete_records)
cursor.execute(insert_records_ancu)
cursor.execute(insert_records_dangbannhadat)
cursor.execute(insert_records_nhadat24h)
cursor.execute(insert_records_muaban)

# cursor.execute(select_records)
# Committing the changes

connection.commit()

# closing the database connection
connection.close()
