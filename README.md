# Do-An-Lap-Trinh-Game-Sudoku
* Đề tài: Lập trình game Sudoku

* Ngôn ngữ: Python

1. Lý do chọn đề tài

    Sudoku là một trò chơi trí tuệ phổ biến, đòi hỏi khả năng tư duy logic và kiên nhẫn. Việc triển khai trò chơi này trong mô hình lập trình mạng Client-Server giúp người chơi có thể kết nối và tham gia cùng lúc  từ nhiều máy tính khác nhau. Ngoài ra, việc kết hợp với giao diện Web HTML tạo ra trải nghiệm trực quan, dễ sử dụng và phù hợp với xu hướng phát triển ứng dụng hiện nay.

2. Mục tiêu của đồ án

   - Xây dựng ứng dụng Sudoku hỗ trợ nhiều người chơi cùng lúc qua mô hình Multi Client-Server.
    
   - Ứng dụng kỹ thuật Socket trong Python để truyền dữ liệu giữa Client và Server.
    
   - Đảm bảo đồng bộ dữ liệu trò chơi giữa các người chơi trong cùng một phiên kết nối.
    
   - Thiết kế giao diện Web HTML để người chơi có thể thao tác dễ dàng (chọn mức độ, nhập số, theo dõi thời gian, thông báo kết quả).
    
   - Xử lý đầy đủ các yêu cầu logic của game Sudoku (kiểm tra hợp lệ, thông báo sai, giới hạn số lần nhập sai, tính giờ, chiến thắng/thua cuộc).

3. Kỹ thuật được sử dụng
   
    * Lập trình mạng Python
    
      - Socket Programming (TCP/IP):
      
        + Server tạo socket và lắng nghe kết nối từ nhiều Client.
        
        + Client gửi/nhận dữ liệu (nước đi, kết quả, trạng thái bàn chơi) qua socket.
        
      - Multi-threading (đa luồng):
      
        Mỗi Client kết nối được xử lý bằng một luồng riêng biệt để đảm bảo nhiều người có thể chơi cùng lúc.
    
    *  Mô hình Multi Client-Server
    
      - Server chính: quản lý bàn Sudoku, xử lý logic game, đồng bộ trạng thái cho các Client.
        
      - Các Client: gửi yêu cầu điền số, nhận thông báo kết quả từ Server.
    
    *  Xử lý logic Sudoku
    
      - Sinh bàn Sudoku theo ba mức độ: Dễ – Trung bình – Khó.
      
      - Kiểm tra dữ liệu nhập hợp lệ (tọa độ, giá trị).
      
      - Giới hạn 3 lần nhập sai trước khi thua.
      
      - Hiển thị thời gian chơi và thông báo chiến thắng/thất bại.
      
    *  Giao diện Web (HTML + CSS + JavaScript)
    
      - Giao diện bảng Sudoku (9x9).
    
    - Chức năng chọn mức độ chơi.
    
    - Hiển thị thời gian, số lần sai.
    
    - Kết nối với server (qua WebSocket hoặc Flask SocketIO).
    
    - Hiển thị kết quả khi hoàn thành game.
