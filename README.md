# 🔗 Build a Simple Blockchain from Scratch

> Dự án mô phỏng cơ chế hoạt động cốt lõi của Blockchain (Bitcoin Core) từ đầu.
> Bao gồm: Proof-of-Work (PoW), Mining, Transaction Pool và Demo tấn công dữ liệu (Tampering).

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red.svg)
![Status](https://img.shields.io/badge/Status-Completed-success.svg)

## 📋 Thành viên thực hiện
1. Trần Thị Minh Ánh
2. Phạm Đinh Quốc Hoà
3. Nguyễn Phương Thịnh

## 📋 Giới thiệu

Dự án thực hiện cài đặt mô phỏng một Blockchain cơ bản. Mục tiêu là minh họa trực quan cách các khối liên kết với nhau, cách thợ đào (miner) giải thuật toán và điều gì xảy ra khi hacker cố tình sửa đổi dữ liệu quá khứ.

### 🌟 Tính năng nổi bật (Highlights)

1.  **Core Blockchain Engine:**
    * Cấu trúc OOP (Class `Block`, `Blockchain`).
    * Thuật toán băm SHA-256.
    * Cơ chế **Proof-of-Work** (Đào coin) với độ khó (Difficulty) tùy chỉnh.
2.  **Interactive Dashboard (Streamlit UI):**
    * Giao diện web tương tác thời gian thực.
    * Xem Sổ cái (Ledger) trực quan dưới dạng bảng.
3.  **Security Simulation (Tính năng sáng tạo):**
    * **Hack/Tamper Data:** Cho phép người dùng đóng vai Hacker sửa đổi dữ liệu giao dịch trong bộ nhớ.
    * **Chain Validation:** Hệ thống tự động phát hiện và cảnh báo khi chuỗi bị thay đổi (Invalid Chain).

---

## 📂 Cấu trúc dự án

Dự án được tổ chức theo mô hình phân lớp để dễ quản lý và mở rộng:

```text
MainFolder/
├── core.py                   # Chứa Class Block, Blockchain và thuật toán Mining
├── ui.py                     # Giao diện người dùng (Streamlit Dashboard)
├── requirements.txt          # Danh sách thư viện phụ thuộc
└── README.md                 # Tài liệu hướng dẫn