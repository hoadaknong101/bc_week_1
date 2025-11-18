import ast
import time
import pandas as pd
import streamlit as st
from core import Blockchain

# Cấu hình trang
st.set_page_config(page_title="Blockchain Demo Project", layout="wide")

st.title("🔗 Build a Simple Blockchain from Scratch")
st.markdown("### Mô phỏng Blockchain")

if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()

blockchain = st.session_state.blockchain

# --- SIDEBAR: TẠO GIAO DỊCH ---
st.sidebar.header("1. Tạo Giao Dịch Mới")
sender = st.sidebar.text_input("Người gửi (Sender)", "Ánh")
receiver = st.sidebar.text_input("Người nhận (Receiver)", "Thịnh")
amount = st.sidebar.number_input("Số tiền (Amount)", min_value=0.0, value=10.0)

if st.sidebar.button("Thêm Giao Dịch"):
    blockchain.add_data(sender, receiver, amount)
    st.sidebar.success(f"Đã thêm giao dịch: {sender} -> {receiver}: {amount}")

# --- SIDEBAR: ĐÀO BLOCK ---
st.sidebar.header("2. Mining (Đào Block)")
difficulty = st.sidebar.slider("Độ khó (Difficulty - Số số 0)", 1, 5, 2)

if st.sidebar.button("⛏️ Đào Block (Mine)"):
    if not blockchain.pending_data:
        st.sidebar.warning("Chưa có giao dịch nào để đào!")
    else:
        with st.spinner('Đang đào block (Proof of Work)...'):
            start_time = time.time()
            block = blockchain.mine(difficulty)
            end_time = time.time()
        
        st.sidebar.success(f"Đã đào xong Block #{block.index}!")
        st.sidebar.info(f"Thời gian đào: {end_time - start_time:.4f} giây")
        st.sidebar.code(f"Hash: {block.hash}")

# --- MAIN: HIỂN THỊ ---
st.divider()
st.subheader("⏳ Hàng đợi giao dịch")
if blockchain.pending_data:
    pending_df = pd.DataFrame(blockchain.pending_data)
    pending_df = pending_df.rename(columns={
        'sender': 'Sender',
        'recipient': 'Recipient',
        'amount': 'Amount'
    })

    # Select and order columns explicitly
    display_cols = ['Sender', 'Recipient', 'Amount']

    st.dataframe(
        pending_df[display_cols],
        use_container_width=True,
        hide_index=True,
        column_order=display_cols,
        column_config={
            'Sender': st.column_config.TextColumn('Sender', width='small'),
            'Recipient': st.column_config.TextColumn('Recipient', width='small'),
            'Amount': st.column_config.NumberColumn('Amount', format='$%.2f', width='small')
        }
    )
else:
    st.info("Hiện không có giao dịch nào đang chờ.")

st.divider()
st.subheader("📜 Sổ Blockchain (Ledger)")

chain_data = []
for block in blockchain.chain:
    # Format lại thời gian
    readable_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block.timestamp))
    
    # Format lại hiển thị Transaction cho gọn gàng
    # Chuyển list dict thành list string dạng: "Sender -> Recipient: Amount"
    formatted_txs = [
        f"{tx['sender']} ➝ {tx['recipient']}: ${tx['amount']}" 
        for tx in block.data
    ]
    
    chain_data.append({
        "Index": block.index,
        "Transactions": formatted_txs, # Streamlit sẽ hiển thị cái này dưới dạng List đẹp mắt
        "Nonce": block.nonce,
        "Timestamp": readable_time,
        "Hash": block.hash,
        "Previous Hash": block.previous_hash
    })

df = pd.DataFrame(chain_data)

# 2. Hiển thị DataFrame với cấu hình tùy chỉnh
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    column_order=["Index", "Transactions", "Timestamp", "Previous Hash", "Hash",  "Nonce"],
    column_config={
        "Index": st.column_config.NumberColumn(
            "Block ID", 
            format="%d", 
            width="small"
        ),
        "Timestamp": st.column_config.TextColumn(
            "Created at",
            width="medium"
        ),
        "Transactions": st.column_config.ListColumn(
            "Transactions Data",
            width="large",
            help="Danh sách các giao dịch trong khối"
        ),
        "Hash": st.column_config.TextColumn(
            "Current Hash",
            width="medium",
            help="Mã băm của khối hiện tại"
        ),
        "Previous Hash": st.column_config.TextColumn(
            "Prev Hash",
            width="medium",
            help="Mã băm của khối trước đó"
        ),
    }
)

st.divider()
st.header("🕵️ Kiểm thử bảo mật (Tampering Test)")
st.write("Thử thay đổi dữ liệu của một Block trong quá khứ để xem hệ thống phát hiện như thế nào.")

col1, col2 = st.columns(2)

with col1:
    block_index_to_hack = st.number_input("Chọn Index Block để hack", min_value=0, max_value=len(blockchain.chain)-1, value=0)
    new_data = st.text_input("Thay đổi thông tin giao dịch thành:", placeholder="Ví dụ: [{'sender': 'Thịnh', 'recipient': 'Ánh', 'amount': 1000000}]")
    
    if st.button("🚨 TẤN CÔNG (HACK BLOCK)"):
        try:
            data = ast.literal_eval(new_data)
            
            if not isinstance(data, list):
                st.error("Dữ liệu không hợp lệ! Vui lòng nhập danh sách các giao dịch dưới dạng [{'sender': 'X', 'recipient': 'Y', 'amount': Z}, ...]")
            else:
                blockchain.chain[block_index_to_hack].data = data
                st.error(f"Đã thay đổi dữ liệu Block #{block_index_to_hack}!")
        except SyntaxError:
            st.error("Dữ liệu không hợp lệ! Vui lòng nhập danh sách các giao dịch dưới dạng [{'sender': 'X', 'recipient': 'Y', 'amount': Z}, ...]")

with col2:
    if st.button("🔍 Validate Chain"):
        is_valid = blockchain.is_chain_valid()
        if is_valid:
            st.success("✅ Chuỗi hợp lệ (Blockchain Valid).")
        else:
            st.error("❌ CẢNH BÁO: Chuỗi không hợp lệ! Phát hiện thay đổi dữ liệu!")
            st.write("Hệ thống phát hiện Hash của block bị sửa không khớp với dữ liệu, hoặc liên kết previous_hash bị gãy.")

# --- VISUALIZATION (Dạng JSON Pretty) ---
with st.expander("Xem chi tiết cấu trúc JSON (Raw Data)"):
    st.json([b.__dict__ for b in blockchain.chain])