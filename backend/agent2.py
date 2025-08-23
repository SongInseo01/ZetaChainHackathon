import uvicorn
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from fastapi.middleware.cors import CORSMiddleware


# ==== LLM 초기화 ====
llm = ChatOllama(model="llama3.2:latest")

# ==== FastAPI 앱 ====
app = FastAPI()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 ["http://localhost:5173"]처럼 FE 주소만 허용
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, OPTIONS 등 모두 허용
    allow_headers=["*"],
)


class LLMRequest(BaseModel):
    user_input: str


@app.post("/llm")
async def llm_endpoint(req: LLMRequest):
    user_input = req.user_input

    # 현재 잔고 조회
    try:
        balance_resp = requests.get("http://0.0.0.0:8876/balance")
        balance_json = balance_resp.json()
    except Exception as e:
        return {"error": f"balance fetch failed: {str(e)}"}

    # ========== 1차 LLM 호출 (Reasoning) ==========
    prompt_reason = f"""
    You are an expert agent that helps decide swaps.
    You are an expert crypto trading agent that helps decide swaps.

    Here are the tokens:
    - ETH (Ethereum): the native cryptocurrency of the Ethereum network, commonly used for transactions and gas fees.
    - BNB (Binance Coin): the native token of Binance Smart Chain, often used for trading fees and DeFi applications.
    - SUI (Sui Token): the native token of the Sui blockchain, used for staking, governance, and transaction fees.
    
    Current balance: {balance_json}
    User request: "{user_input}"

    Explain in a short paragraph why the user should swap ETH to BNB or ETH to SUI.
    """
    reasoning_resp = llm.invoke(prompt_reason)
    reasoning_text = reasoning_resp.content.strip()

    # ========== 2차 LLM 호출 (최종 결정) ==========
    prompt_decision = f"""
    Based on the reasoning: "{reasoning_text}"

    Output strictly one of the following:
    - swap_bnb
    - swap_sui

    Do not output anything else.
    """
    decision_resp = llm.invoke(prompt_decision)
    decision = decision_resp.content.strip().lower().replace('"', '')

    # ========== API 호출 ==========
    if decision == "swap_bnb":
        url = "http://0.0.0.0:8886/ethswapbnb"
    elif decision == "swap_sui":
        url = "http://0.0.0.0:8887/ethswapsui"
    else:
        return {"error": f"Unexpected decision from LLM: {decision}"}

    try:
        tx_resp = requests.get(url)
        tx_json = tx_resp.json()
    except Exception as e:
        return {"error": f"swap request failed: {str(e)}"}

    # ========== 최종 반환 ==========
    return {
        "decision": decision,
        "tx_hash": tx_json.get("tx_hash"),
        "reason": reasoning_text,
    }


def main():
    uvicorn.run("agent2:app", host="0.0.0.0", port=7777, reload=True)


if __name__ == "__main__":
    main()
