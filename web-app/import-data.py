import csv
import sqlite3

# Connecting to the geeks database
connection = sqlite3.connect('data.db')

# Creating a cursor object to execute
# SQL queries on a database table
cursor = connection.cursor()

# Opening the data.csv file
file = open('data_all_processed_id.csv', encoding="utf8")

# Reading the contents of the
# data_all_processed_id.csv file
contents = csv.reader(file)
# contents = next(contents)  # skip the headers
# SQL query to insert data into the
# House_house table
insert_records = "INSERT INTO house_houses (house_id, LoaiHinh, TacGia, SoDienThoai, Gia, DienTich, DiaChi, ChungNhanSoHuu) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"

# Importing the contents of the file
# into our house table
cursor.executemany(insert_records, contents)

# Committing the changes
connection.commit()

# closing the database connection
connection.close()
