# Đóng góp

## Nguyên tắc trên hết: đừng đoán

Nếu bạn không chắc nguyên nhân, viết ra phần mình chắc và ghi rõ phần mình đoán:

> Chưa xác minh. Khả năng: ...

Một mục ghi rõ ranh giới giữa "biết" và "đoán" hữu ích hơn nhiều một mục nghe chắc chắn nhưng sai. Người đọc mục này thường đang chữa cháy và sẽ làm theo ngay.

## Không đưa thông tin hệ thống thật vào

Không hostname, tenant ID, tên người dùng, transport number thật, không dán log chứa token hay cookie phiên.

Thay bằng placeholder:

```
https://<host>/sap/bc/ui5_ui5/sap/<appname>/index.html
Transport Request "<TRANSPORT>" has been determined ...
```

## Cách 1 — Mở issue (không cần git)

Vào tab Issues → New issue → chọn template. Điền được bao nhiêu thì điền; maintainer sẽ chuyển thành file JSON.

Dán **nguyên văn dòng log quyết định** — đó là thứ có giá trị nhất, đừng diễn giải lại.

## Cách 2 — Pull request

```bash
git checkout -b them-loi-<mo-ta-ngan>
# tạo hoặc sửa issues/<id>.json
python3 scripts/build.py
git add issues/ data/issues.json
git commit -m "Thêm: <tiêu đề lỗi>"
git push origin them-loi-<mo-ta-ngan>
```

Quy ước đặt `id` (tên file): chữ thường, nối bằng gạch ngang, mô tả hiện tượng chứ không mô tả app.

- ✅ `http-403-repository-srv`, `ladi-package-conflict`, `transport-not-modifiable`
- ❌ `loi-zqm04`, `bug-2`, `issue-thang-9`

## Cách 3 — Xác minh mục đã có

Đây là đóng góp giá trị nhất.

Khi bạn chạy thật một cách xử lý và nó hoạt động:

1. Đổi `"verified": false` → `true`
2. Trong `solutions[].body`, đổi "Chưa xác minh" → "Đã xác minh: <ngày>, <môi trường>"
3. Cập nhật `updatedAt`
4. Chạy `python3 scripts/build.py` rồi commit

Nếu cách xử lý **không** hoạt động, cũng có giá trị ngang: ghi vào `body` điều kiện nào làm nó thất bại.

## Cách viết từng trường

**`symptom`** — dán đúng dòng log quyết định, không phải toàn bộ log. Với lỗi deploy Fiori, dòng quyết định gần như luôn nằm ngay sau `* Updating the Application Index *` hoặc trong khối `* Operations *`.

**`solutions`** — xếp theo thứ tự nên thử. Đúng một cách được đánh `recommended: true`. Mỗi `body` phải có lệnh hoặc đường dẫn transaction cụ thể, không viết chung chung kiểu "kiểm tra cấu hình".

Nêu cả cái giá phải trả: downtime, cần quyền gì, phải nhờ ai.

**`prevention`** — điều gì đáng thay đổi trong quy trình để lỗi này không lặp lại. Nếu không nghĩ ra, để trống còn hơn viết cho có.

**`refs`** — SAP Note, KBA, link tài liệu, tên transaction. URL đầy đủ sẽ tự thành link trên trang web.

## Review

Maintainer sẽ kiểm: có thông tin hệ thống thật không, cờ `verified` có tương xứng với bằng chứng không, `module` và `severity` có hợp lệ không, và `data/issues.json` đã được build lại chưa.
