import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from datetime import datetime

# --- PHẦN 1: LOGIC BACKEND (Dựa trên code của bạn, có chỉnh sửa nhỏ) ---

def ket_noi_db(sv, db):
    """Hàm kết nối tới Microsoft SQL Server."""
    try:
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={sv};"
            f"DATABASE={db};"
            f"Trusted_Connection=yes;"
        )
        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as err:
        messagebox.showerror("Lỗi Kết nối", f"Không thể kết nối tới database:\n{err}")
        return None

def lay_tat_ca_chi_tieu(sv, db):
    """Hàm này LẤY và TRẢ VỀ danh sách chi tiêu thay vì in ra."""
    conn = ket_noi_db(sv, db)
    if conn is None:
        return [] # Trả về danh sách rỗng nếu kết nối lỗi
    
    cursor = conn.cursor()
    cursor.execute("SELECT id, noi_dung, so_tien, ngay_chi FROM CHITIEU ORDER BY id DESC")
    results = cursor.fetchall()
    conn.close()
    return results

def them_chi_tieu_moi(sv, db, noi_dung, so_tien):
    """Hàm thêm chi tiêu và trả về True/False."""
    ngay_hom_nay = datetime.now().date()
    conn = ket_noi_db(sv, db)
    if conn is None:
        return False

    cursor = conn.cursor()
    sql_query = "INSERT INTO CHITIEU (noi_dung, so_tien, ngay_chi) VALUES (?, ?, ?)"
    values = (noi_dung, so_tien, ngay_hom_nay)
    try:
        cursor.execute(sql_query, values)
        conn.commit()
        conn.close()
        return True
    except pyodbc.Error as err:
        messagebox.showerror("Lỗi Database", f"Không thể thêm chi tiêu:\n{err}")
        conn.close()
        return False

def xoa_chi_tieu_theo_id(sv, db, id_can_xoa):
    """Hàm xóa chi tiêu theo ID và trả về True/False."""
    conn = ket_noi_db(sv, db)
    if conn is None:
        return False
        
    cursor = conn.cursor()
    sql_query = "DELETE FROM CHITIEU WHERE id = ?"
    try:
        cursor.execute(sql_query, (id_can_xoa,))
        conn.commit()
        conn.close()
        return True
    except pyodbc.Error as err:
        messagebox.showerror("Lỗi Database", f"Không thể xóa chi tiêu:\n{err}")
        conn.close()
        return False


# --- PHẦN 2: GIAO DIỆN NGƯỜI DÙNG (GUI) ---

class AppQuanLyChiTieu:
    def __init__(self, root, server_name, db_name):
        self.root = root
        self.server = server_name
        self.db = db_name
        
        self.root.title("Trình Quản Lý Chi Tiêu")
        self.root.geometry("800x600")

        # --- Tạo các khung giao diện ---
        # Khung nhập liệu
        input_frame = tk.LabelFrame(self.root, text="Thêm Chi tiêu mới", padx=10, pady=10)
        input_frame.pack(padx=10, pady=10, fill="x")

        # Khung hiển thị danh sách
        list_frame = tk.LabelFrame(self.root, text="Danh sách Chi tiêu", padx=10, pady=10)
        list_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # --- Các widget trong khung nhập liệu ---
        tk.Label(input_frame, text="Nội dung:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_noidung = tk.Entry(input_frame, width=50)
        self.entry_noidung.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Số tiền:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_sotien = tk.Entry(input_frame, width=30)
        self.entry_sotien.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Button(input_frame, text="Thêm", command=self.add_expense).grid(row=0, column=2, rowspan=2, padx=10, ipady=10)

        # --- Các widget trong khung danh sách ---
        # Tạo bảng hiển thị (TreeView)
        self.tree = ttk.Treeview(list_frame, columns=("ID", "Nội dung", "Số tiền", "Ngày"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nội dung", text="Nội dung")
        self.tree.heading("Số tiền", text="Số tiền (VND)")
        self.tree.heading("Ngày", text="Ngày chi")
        
        # Định dạng cột
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nội dung", width=300)
        self.tree.column("Số tiền", width=150, anchor="e") # anchor='e' để căn phải
        self.tree.column("Ngày", width=120, anchor="center")

        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Các nút bấm chức năng
        button_frame = tk.Frame(list_frame)
        button_frame.pack(side="left", fill="y", padx=10)

        tk.Button(button_frame, text="Làm mới", command=self.load_expenses).pack(pady=5, fill="x")
        tk.Button(button_frame, text="Xóa mục đã chọn", command=self.delete_expense).pack(pady=5, fill="x")
        
        # Tải dữ liệu lần đầu
        self.load_expenses()

    def load_expenses(self):
        # Xóa dữ liệu cũ trên bảng
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Lấy dữ liệu mới từ backend
        expenses = lay_tat_ca_chi_tieu(self.server, self.db)
        for expense in expenses:
            # Định dạng lại dữ liệu trước khi hiển thị
            so_tien_formatted = f"{expense.so_tien:,.0f}"
            ngay_chi_formatted = expense.ngay_chi.strftime('%Y-%m-%d')
            self.tree.insert("", "end", values=(expense.id, expense.noi_dung, so_tien_formatted, ngay_chi_formatted))

    def add_expense(self):
        noi_dung = self.entry_noidung.get()
        so_tien_str = self.entry_sotien.get()

        if not noi_dung or not so_tien_str:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ nội dung và số tiền.")
            return

        try:
            so_tien = float(so_tien_str)
        except ValueError:
            messagebox.showerror("Lỗi", "Số tiền không hợp lệ.")
            return

        success = them_chi_tieu_moi(self.server, self.db, noi_dung, so_tien)
        if success:
            messagebox.showinfo("Thành công", "Đã thêm chi tiêu mới.")
            self.entry_noidung.delete(0, tk.END)
            self.entry_sotien.delete(0, tk.END)
            self.load_expenses() # Tải lại danh sách

    def delete_expense(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một mục trong danh sách để xóa.")
            return

        item_data = self.tree.item(selected_items[0])
        expense_id = item_data['values'][0]

        if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa chi tiêu có ID={expense_id}?"):
            success = xoa_chi_tieu_theo_id(self.server, self.db, expense_id)
            if success:
                messagebox.showinfo("Thành công", "Đã xóa chi tiêu.")
                self.load_expenses() # Tải lại danh sách

# --- PHẦN 3: KHỞI CHẠY ỨNG DỤNG ---
if __name__ == "__main__":
    # --- Cửa sổ phụ để nhập thông tin kết nối ---
    # (Đây là một cách đơn giản, có thể cải tiến thêm)
    server = input("Nhập tên Server SQL của bạn: ")
    database = input("Nhập tên Database: ")

    if server and database:
        # Tạo cửa sổ chính của ứng dụng
        root = tk.Tk()
        app = AppQuanLyChiTieu(root, server, database)
        # Chạy vòng lặp của giao diện
        root.mainloop()