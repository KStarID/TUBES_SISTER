import socket

# Fungsi untuk mengirim laporan kasus Covid-19 ke server
def send_report(nik, nama, nama_terduga, alamat_terduga, gejala):
    report_data = f"{nik},{nama},{nama_terduga},{alamat_terduga},{gejala}"
    
    # Membuat koneksi ke server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 5555))

    # Mengirim laporan ke server
    client_socket.send(report_data.encode("utf-8"))

    # Menerima respon dari server
    response = client_socket.recv(1024).decode("utf-8")
    if response == "Laporan tidak valid" :
        print(response)
    else :
        print(f"Waktu penjemputan: {response}")

    # Menutup koneksi
    client_socket.close()

# Perulangan untuk input dari pengguna
while True:
    # Input dari pengguna
    nik = input("Masukkan NIK pelapor (ketik 'exit' untuk keluar): ")
    
    # Keluar dari perulangan jika pengguna memasukkan 'exit'
    if nik.lower() == 'exit':
        break
    
    nama = input("Masukkan nama pelapor: ")
    nama_terduga = input("Masukkan nama terduga Covid-19: ")
    alamat_terduga = input("Masukkan alamat terduga Covid-19: ")
    gejala = input("Masukkan gejala yang dirasakan: ")

    # Mengirim laporan ke server
    send_report(nik, nama, nama_terduga, alamat_terduga, gejala)
