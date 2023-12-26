import time
import threading
import socket

# Fungsi untuk memeriksa apakah NIK pelapor sudah ada dalam database
def load_database():
    with open('NIKData.txt', 'r') as file:
        return set(map(str.strip, file.readlines()))

def check_nik(nik):
    database = load_database()
    return nik in database

# Fungsi untuk memproses laporan kasus Covid-19 dari masyarakat
def process_report(nik, nama, nama_terduga, alamat_terduga, gejala):
    if check_nik(nik):
        # Jika NIK pelapor sudah ada dalam database, maka laporan valid
        print("Laporan valid")
        # Server merespon dengan informasi waktu, nama, dan jumlah orang yang akan melakukan penjemputan
        waktu = time.strftime("%Y-%m-%d %H:%M:%S")
        nama_penjemput = "Raja bajak laut, wakil raja bajak laut"
        jumlah_orang = 2
        response = f"{waktu}, Nama Penjemput : {nama_penjemput}; {jumlah_orang} orang akan melakukan penjemputan"
        print(f"Waktu penjemputan: {response}")
        print(f"NIK: {nik}, Nama: {nama}, Terduga: {nama_terduga}, Alamat Terduga: {alamat_terduga}, Gejala: {gejala}\n")
        # Menyimpan respon server dalam bentuk file teks
        with open("ResponServer.txt", "a") as f:
            f.write(f"{response}\n")

        # Menyimpan informasi ke dalam file CovidData.txt
        with open("CovidData.txt", "a") as f:
            f.write(f"NIK: {nik}, Nama: {nama}, Terduga: {nama_terduga}, Alamat Terduga: {alamat_terduga}, Gejala: {gejala}\n")

        return response
    else:
        # Jika NIK pelapor tidak ada dalam database, maka laporan tidak valid
        print("Laporan tidak valid")
        return "Laporan tidak valid"

# Fungsi untuk menangani koneksi dari client
def handle_client(client_socket):
    while True:
        # Menerima laporan kasus Covid-19 dari client
        data = client_socket.recv(1024).decode("utf-8")
        if not data:
            break

        # Memproses laporan kasus Covid-19 dari client
        report_data = data.split(",")
        response = process_report(*report_data)

        # Mengirim respon server ke client
        client_socket.send(response.encode("utf-8"))

# Fungsi untuk membuat server socket
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 5555))
    server_socket.listen()

    print("Server sedang mendengarkan...")
    
    while True:
        client_socket, client_addr = server_socket.accept()
        print(f"Terhubung dengan {client_addr}")

        # Memulai thread untuk menangani koneksi dari client
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

# Memulai server
start_server()
