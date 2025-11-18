import hashlib
import json
import time
from typing import List, Dict, Optional

class Block:
    """
    Đại diện cho một khối (Block) trong chuỗi.
    """
    def __init__(self, index: int, data: List[Dict], timestamp: float, previous_hash: str, nonce: int = 0):
        self.index = index
        self.data = data
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        # Lưu ý: Không tính hash ngay tại __init__ nếu chưa đào, 
        # nhưng để đơn giản ta tạm tính hash với nonce=0
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        """
        Tính toán mã băm SHA-256 của khối.
        QUAN TRỌNG: Phải loại bỏ thuộc tính 'hash' ra khỏi dữ liệu trước khi băm 
        để tránh lỗi vòng lặp (hash chứa chính nó).
        """
        # 1. Copy dictionary của object để không ảnh hưởng dữ liệu thật
        block_data = self.__dict__.copy()
        
        # 2. Xóa key 'hash' nếu tồn tại (đây là bước fix lỗi quan trọng nhất)
        if 'hash' in block_data:
            del block_data['hash']

        # 3. Sắp xếp key để đảm bảo tính nhất quán (Deterministic)
        # Nếu json không sort, {a:1, b:2} sẽ khác {b:2, a:1} -> sai hash
        block_string = json.dumps(block_data, sort_keys=True).encode()
        
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.pending_data: List[Dict] = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Tạo khối nguyên thủy (Block 0)."""
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash() 
        self.chain.append(genesis_block)

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def add_data(self, sender: str, recipient: str, amount: float):
        """Thêm dữ liệu vào hàng đợi."""
        data = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'timestamp': time.time()
        }
        self.pending_data.append(data)

    def proof_of_work(self, block: Block, difficulty: int) -> str:
        """
        Thuật toán đào (Mining).
        Thay đổi nonce liên tục cho đến khi hash thỏa mãn điều kiện difficulty.
        """
        block.nonce = 0
        computed_hash = block.compute_hash()
        
        target = '0' * difficulty
        
        # Vòng lặp đào
        while not computed_hash.startswith(target):
            block.nonce += 1
            computed_hash = block.compute_hash()
            
        return computed_hash

    def mine(self, difficulty: int = 2):
        """Đóng gói dữ liệu và đào khối mới."""
        last_block = self.last_block
        new_block = Block(
            index=last_block.index + 1,
            data=self.pending_data, # Lấy hết pending tx
            timestamp=time.time(),
            previous_hash=last_block.hash
        )

        # Thực hiện đào
        proof_hash = self.proof_of_work(new_block, difficulty)
        
        # Sau khi tìm được hash hợp lệ, gán vào block
        new_block.hash = proof_hash
        
        # Thêm vào chuỗi
        self.chain.append(new_block)
        
        # Reset hàng đợi dữ liệu
        self.pending_data = []
        
        return new_block

    def is_chain_valid(self) -> bool:
        """
        Kiểm tra tính toàn vẹn của toàn bộ chuỗi.
        Đây là chức năng cốt lõi để phát hiện 'Hack'.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # CHECK 1: Hash Integrity
            if current_block.hash != current_block.compute_hash():
                print(f"Lỗi tại Block {current_block.index}: Dữ liệu bị thay đổi!")
                return False

            # CHECK 2: Chain Linkage
            if current_block.previous_hash != previous_block.hash:
                print(f"Lỗi tại Block {current_block.index}: Liên kết chuỗi bị gãy!")
                return False

        return True