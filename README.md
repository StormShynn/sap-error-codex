# SAP Error Codex

Sổ tay tra cứu lỗi triển khai **SAP Fiori / UI5, ABAP Extensibility, Transport và Integration** — tìm theo **message ID**, không phải theo tiêu đề.

Khi bạn gặp lỗi, thứ bạn có trong tay là `/UI2/UI5_REP_LOAD-039` hoặc `HTTP 403`, không phải một câu mô tả. Kho này index theo đúng thứ đó.

**Trang tra cứu:** https://stormshynn.github.io/sap-error-codex/

---

## Nội dung hiện có

| Mảng | Số mục |
|---|---|
| SAP Fiori / UI5 | 12 |
| Basis / Auth | 5 |
| Transport & Release | 2 |
| Integration / OData | 2 |
| ABAP / Extensibility | 1 |
| **Tổng** | **22** |

Một vài mục tiêu biểu:

- `ladi-package-conflict` — *SAPUI5 application can only be deployed to the previous package* (xung đột LADI, không phải package)
- `http-403-repository-srv` — 403 do service `/UI5/ABAP_REPOSITORY_SRV` chưa activate hoặc thiếu `S_DEVELOP`
- `testmode-pass-deploy-fail` — vì sao `--testMode` báo OK mà deploy thật vẫn fail
- `self-signed-cert-deploy` — `unable to get local issuer certificate`
- `unknown-file-type-upload` — file bị bỏ qua khi upload (`.Ui5RepositoryTextFiles`)

---

## Nguyên tắc: cờ "Đã xác minh"

Mỗi mục có trường `verified`:

| Giá trị | Nghĩa |
|---|---|
| `true` | Cách xử lý đã chạy thành công trên hệ thống thật, có người chứng kiến |
| `false` | Soạn từ tài liệu, blog, hoặc kinh nghiệm chung — **kiểm tra trước khi áp dụng** |

Hiện tại **4/22** mục ở mức `true`. Con số này quan trọng hơn tổng số mục: một kho 200 mục không rõ độ tin cậy thì vô dụng trong lúc đang chữa cháy.

Trong từng cách xử lý, phần `body` cũng ghi rõ "Đã xác minh" hay "Chưa xác minh".

---

## Cấu trúc dữ liệu

Nguồn sự thật là các file trong `issues/` — mỗi lỗi một file JSON. `data/issues.json` là bản gộp do script sinh ra, dùng cho trang web.

```
issues/<id>.json     ← sửa ở đây
data/issues.json     ← sinh ra, đừng sửa tay
index.html           ← trang tra cứu tĩnh
scripts/build.py     ← gộp issues/ thành data/issues.json
```

### Schema một mục

```json
{
  "title": "Tiêu đề ngắn, nêu đúng hiện tượng người dùng gặp",
  "module": "SAP Fiori / UI5",
  "severity": "Blocker | Cao | Trung bình | Thấp",
  "status": "Mở | Đang điều tra | Đã giải quyết",
  "verified": false,
  "msgKeys": ["/UI2/UI5_REP_LOAD-039", "HTTP 400"],
  "symptom": "Dán đúng dòng log quyết định — đó là thứ người sau sẽ tìm",
  "rootCause": "Vì sao xảy ra. Nếu chưa chắc, ghi rõ 'Chưa xác minh'",
  "solutions": [
    { "label": "Tên cách xử lý", "body": "Các bước cụ thể", "recommended": true }
  ],
  "prevention": "Làm gì để lần sau không gặp lại",
  "refs": ["SAP Note 1797736", "https://..."],
  "createdAt": "2026-09-17T10:00:00.000Z",
  "updatedAt": "2026-09-17T10:00:00.000Z"
}
```

`module` phải là một trong: `SAP Fiori / UI5`, `ABAP / Extensibility`, `Transport & Release`, `Integration / OData`, `Power BI`, `Microsoft Fabric`, `Basis / Auth`.

---

## Chạy local

```bash
python3 scripts/build.py     # gộp issues/ → data/issues.json
python3 -m http.server 8000  # mở http://localhost:8000
```

Mở `index.html` trực tiếp bằng `file://` sẽ không chạy — trình duyệt chặn `fetch` trên giao thức đó.

---

## Đóng góp

Xem [CONTRIBUTING.md](CONTRIBUTING.md). Ba cách, từ nhẹ đến nặng:

1. **Mở issue** — dùng template, không cần biết git
2. **Pull request** — thêm hoặc sửa file trong `issues/`, chạy `scripts/build.py`, commit cả hai
3. **Bật cờ verified** — khi bạn đã chạy thật một cách xử lý và nó hoạt động, đổi `verified` thành `true` và ghi ngày vào `updatedAt`

Đóng góp giá trị nhất không phải mục mới, mà là **xác minh mục đã có**.

---

## Giới hạn đã biết

- Phần lớn tài liệu chính thức của SAP (help.sap.com, launchpad.support.sap.com) chặn truy cập tự động, nên nội dung ở đây tổng hợp từ log thực tế, tài liệu mở của SAP-samples, và SAP Community. Luôn đối chiếu SAP Note gốc trước khi áp dụng lên PRD.
- Các mục về Power BI và Microsoft Fabric chưa có nội dung — schema đã sẵn sàng.
- Không chứa thông tin hệ thống cụ thể: không hostname, không tenant ID, không tên người dùng, không transport number thật. Giữ nguyên nguyên tắc này khi đóng góp.

---

## Giấy phép

MIT — xem [LICENSE](LICENSE).
