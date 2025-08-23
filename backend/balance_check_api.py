import uvicorn
from fastapi import FastAPI
from web3 import Web3

# ==== RPC 연결 ====
RPC_URL = "http://localhost:8545"  # ZetaChain 로컬 EVM RPC
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# ==== 조회 대상 기본 주소 (고정) ====
DEFAULT_ADDR = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"

# ==== ZRC-20 BNB 컨트랙트 ====
ZRC20_BNB = "0x65a45c57636f9BcCeD4fe193A602008578BcA90b"
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function",
    }
]

zrc20_bnb = w3.eth.contract(address=Web3.to_checksum_address(ZRC20_BNB), abi=ERC20_ABI)

# ==== FastAPI 앱 ====
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "ZetaChain balance API. Try /balance/eth or /balance/bnb"}


@app.get("/balance")
async def get_all_balances():
    try:
        checksum_addr = Web3.to_checksum_address(DEFAULT_ADDR)

        # ETH 잔고
        evm_balance_wei = w3.eth.get_balance(checksum_addr)
        evm_balance_eth = w3.from_wei(evm_balance_wei, "ether")

        # BNB 잔고
        zrc20_balance = zrc20_bnb.functions.balanceOf(checksum_addr).call()

        return {
                "ETH": str(evm_balance_eth),
                "BNB": str(zrc20_balance)
            
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/balance/{symbol}")
async def get_balance(symbol: str):
    try:
        checksum_addr = Web3.to_checksum_address(DEFAULT_ADDR)

        if symbol.lower() == "eth":
            # EVM 네이티브 잔고
            evm_balance_wei = w3.eth.get_balance(checksum_addr)
            evm_balance_eth = w3.from_wei(evm_balance_wei, "ether")
            return {
                "address": checksum_addr,
                "symbol": "ETH",
                "balance": str(evm_balance_eth)
            }

        elif symbol.lower() == "bnb":
            # ZRC-20 BNB 잔고
            zrc20_balance = zrc20_bnb.functions.balanceOf(checksum_addr).call()
            return {
                "address": checksum_addr,
                "symbol": "BNB",
                "balance": str(zrc20_balance)
            }

        else:
            return {"error": f"Unsupported symbol '{symbol}'. Use 'eth' or 'bnb'."}

    except Exception as e:
        return {"error": str(e)}

# ==== main() ====
def main():
    uvicorn.run("balance_check_api:app", host="0.0.0.0", port=8876, reload=True)

if __name__ == "__main__":
    main()
