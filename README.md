# Do-An-Lap-Trinh-Game-Sudoku
* Đề tài: Lập trình game Sudoku

* Ngôn ngữ: Python

* Kỹ thuật: Socket lập trình mạng theo mô hình Multi Client - Server

* Giao diện: Web HTML (trình duyệt giao tiếp với server Python)

* Đảm bảo: Bao quát kiến thức lập trình mạng (socket, thread, client-server communication, đồng bộ, xử lý nhiều client).

* Kiến thức mạng được áp dụng

  - Socket TCP/IP: Client – Server truyền dữ liệu Sudoku.
  
  - Multi-client: Server dùng threading để xử lý nhiều client cùng lúc.
  
  - Protocol: Định nghĩa gói tin (JSON) gồm:
  
      + action: join_game, move, quit, result
      
      + data: tọa độ, số nhập, trạng thái thắng/thua
    
  - Đồng bộ dữ liệu: Server kiểm tra hợp lệ, gửi phản hồi cho tất cả client.
    
  - Timeout & Error handling: Xử lý client mất kết nối.
    
* Luồng hoạt động

  - Client vào web → chọn Độ khó.
    
  - Server gửi bảng Sudoku tương ứng.
    
  - Người chơi nhập tọa độ + số → gửi server.
    
  - Server kiểm tra:
    
      + Nếu sai → cảnh báo. Sai 3 lần → thua.
      
      + Nếu đúng → cập nhật bảng.
    
  - Khi hoàn thành → Server gửi kết quả thắng và thời gian.
    
  - Hiển thị kết quả trên web.

