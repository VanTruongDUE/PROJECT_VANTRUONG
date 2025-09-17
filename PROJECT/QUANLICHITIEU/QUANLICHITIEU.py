import pyodbc
from datetime import datetime


def nhap():
    print("Hay nhap vao ten server SQL Server: ")
    sv = input()
    print("Hay nhap vao ten database SQL Server: ")
    db = input()
    return sv, db
def ket_noi_db(sv,db):
    """Hàm kết nối tới Microsoft SQL Server."""
    try:
        # COPY VÀ DÁN TOÀN BỘ CHUỖI NÀY, KHÔNG SỬA GÌ NGOÀI TÊN SERVER
        conn_str = (
            fr'DRIVER={{ODBC Driver 17 for SQL Server}};'
            Fr'SERVER={sv};' # <-- Đảm bảo đây chính xác là 'VANTRUONG'
            Fr'DATABASE={db};' # Hoặc 'QUANLICHITIEU' tùy bạn đặt tên
            Fr'Trusted_Connection=yes;'
        )
        
        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as err:
        print(f"Lỗi kết nối database: {err}")
        return None

def them_chi_tieu(sv,db):
    """Hàm thêm chi tiêu, dùng placeholder '?'."""
    noi_dung = input("Nhập nội dung chi tiêu: ")
    try:
        so_tien = float(input("Nhập số tiền: "))
    except ValueError:
        print("Số tiền không hợp lệ.")
        return

    ngay_hom_nay = datetime.now().date()

    conn = ket_noi_db(sv,db)
    if conn is None:
        return

    cursor = conn.cursor()

    # 3. Placeholder đã đổi lại thành dấu '?'
    sql_query = "INSERT INTO CHITIEU (noi_dung, so_tien, ngay_chi) VALUES (?, ?, ?)"
    values = (noi_dung, so_tien, ngay_hom_nay)

    cursor.execute(sql_query, values)

    conn.commit()
    conn.close()
    print("=> Đã thêm chi tiêu thành công!\n")

def xem_chi_tieu(sv,db):
    """Hàm xem chi tiêu từ SQL Server."""
    conn = ket_noi_db(sv,db)
    if conn is None:
        return

    cursor = conn.cursor()

    cursor.execute("SELECT id, noi_dung, so_tien, ngay_chi FROM CHITIEU ORDER BY id DESC")
    cac_khoan_chi = cursor.fetchall()
    conn.close()

    if not cac_khoan_chi:
        print("Chưa có khoản chi nào được ghi lại.\n")
        return

    print("\n--- LỊCH SỬ CHI TIÊU ---")
    for khoan_chi in cac_khoan_chi:
        # Định dạng lại ngày tháng cho đúng
        ngay_dinh_dang = khoan_chi.ngay_chi.strftime('%Y-%m-%d')
        so_tien_format = f"{khoan_chi.so_tien:,.0f}"
        print(f"ID: {khoan_chi.id} | Ngày: {ngay_dinh_dang} | Nội dung: {khoan_chi.noi_dung} | Số tiền: {so_tien_format} VND")
    print("------------------------\n")
    
def xoa_chi_tieu(sv,db):
    conn = ket_noi_db(sv,db)
    if conn is None:
        return
    cursor = conn.cursor()
    sql_query = "DELETE FROM CHITIEU WHERE id = ?"
    id_xoa = int(input("Nhập ID chi tiêu cần xóa: "))
    cursor.execute(sql_query, (id_xoa,))
    conn.commit()
    conn.close()
    print("=> Đã xóa chi tiêu thành công!\n")

def main():
    """Hàm chính không cần thay đổi."""
    try:
        sv,db = nhap()
        while True:
            print("--- Trình quản lý chi tiêu (SQL Server) ---")
            print("1. Thêm chi tiêu mới")
            print("2. Xem tất cả chi tiêu")
            print("3. Thoát")
            print("4. Xóa chi tiêu (chức năng bổ sung)")
            
            lua_chon = input("Nhập lựa chọn của bạn (1/2/3): ")
        
            if lua_chon == '1':
                them_chi_tieu(sv,db)
            elif lua_chon == '2':
                xem_chi_tieu(sv,db)
            elif lua_chon == '3':
                print("Tạm biệt!")
                break
            elif lua_chon == '4':
                xoa_chi_tieu(sv,db)
            else:
                print("Lựa chọn không hợp lệ. Vui lòng thử lại.\n")
    finally:
        # Đoạn code này LUÔN LUÔN chạy cuối cùng
        print("\n------------------------")
        input("Nhấn Enter để thoát...")

if __name__ == "__main__":
    main()

