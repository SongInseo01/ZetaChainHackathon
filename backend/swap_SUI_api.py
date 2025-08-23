import os
import uvicorn
from fastapi import FastAPI
from web3 import Web3
from eth_account import Account
from eth_abi import encode as abi_encode

# ==== 환경 변수 세팅 ====
RPC_URL = "http://localhost:8545"
CHAIN_ID = 31337  # EVM
GATEWAY = "0x68b1d87f95878fe05b998f19b66f4baba5de1aed"
UNIVERSAL = "0x4bf010f1b9beDA5450a8dD702ED602A104ff65EE"
PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

ZRC20_SUI = "0x777915D031d1e8144c90D025C594b3b8Bf07a08d"
RECIPIENT = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"

# ==== Web3 연결 ====
w3 = Web3(Web3.HTTPProvider(RPC_URL))
acct = Account.from_key(PRIVATE_KEY)
sender = acct.address

# ==== Gateway ABI 최소 정의 ====
gateway_abi = [
    {
        "name": "depositAndCall",
        "type": "function",
        "stateMutability": "payable",
        "inputs": [
            {"name": "receiver", "type": "address"},
            {"name": "payload", "type": "bytes"},
            {"name": "revertOptions", "type": "tuple", "components": [
                {"name": "revertAddress", "type": "address"},
                {"name": "callOnRevert", "type": "bool"},
                {"name": "abortAddress", "type": "address"},
                {"name": "revertMessage", "type": "bytes"},
                {"name": "onRevertGasLimit", "type": "uint256"}
            ]}
        ],
        "outputs": []
    }
]
gateway = w3.eth.contract(address=Web3.to_checksum_address(GATEWAY), abi=gateway_abi)

# ==== FastAPI 앱 ====
app = FastAPI()

@app.get("/")
async def hello():
    print("hello")

@app.get("/ethswapsui")
async def swap_bnb():
    # ==== payload 인코딩 ====
    payload = abi_encode(
        ['address','bytes','bool'],
        [Web3.to_checksum_address(ZRC20_SUI), bytes.fromhex(RECIPIENT[2:]), True]
    )

    # revert 옵션 기본값
    revert_options = (
        "0x0000000000000000000000000000000000000000",
        False,
        "0x0000000000000000000000000000000000000000",
        b"",
        0
    )

    # ==== 트랜잭션 구성 ====
    tx = gateway.functions.depositAndCall(
        Web3.to_checksum_address(UNIVERSAL),
        payload,
        revert_options
    ).build_transaction({
        "from": sender,
        "value": w3.to_wei(0.001, "ether"),  # 고정값
        "chainId": CHAIN_ID,
        "nonce": w3.eth.get_transaction_count(sender),
        "gas": 500000,
        "maxFeePerGas": w3.to_wei("30", "gwei"),
        "maxPriorityFeePerGas": w3.to_wei("1", "gwei"),
    })

    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)

    return {"tx_hash": tx_hash.hex()}

# ==== main() ====
def main():
    uvicorn.run("swap_SUI_api:app", host="0.0.0.0", port=8887, reload=True)

if __name__ == "__main__":
    main()
