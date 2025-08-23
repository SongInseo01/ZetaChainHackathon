import { ethers } from "hardhat";

async function main() {
    const [signer] = await ethers.getSigners();

    // localnet 출력에 나온 Gateway 주소
    const gatewayAddr = "0x2279B7A0a67DB372996a5FaB50D91eAA73d2eBe6";

    // Gateway ABI 연결
    const gateway = await ethers.getContractAt("ZetaGateway", gatewayAddr, signer);

    // 대상 체인 ID (SUI = 104)
    const toChainId = 104;

    // 로컬넷에서 출력된 SUI 수신 주소
    const suiRecipient = "0x2fec3fafe08d2928a6b8d9a6a77590856c458d984ae090ccbd4177ac13729e65";

    // ETH 0.1 전송
    const tx = await gateway.deposit(toChainId, suiRecipient, {
        value: ethers.utils.parseEther("0.1"),
    });

    console.log("Swap Tx submitted:", tx.hash);

    const receipt = await tx.wait();
    console.log("Swap confirmed in block:", receipt.blockNumber);
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
