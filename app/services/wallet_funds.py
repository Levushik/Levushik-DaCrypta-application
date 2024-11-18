from pytoncenter import get_client
from pytoncenter.v3.models import *

from app.core.config import settings
from app.schemas.wallet import WalletFunds, WalletJettonInfo

client = get_client(version="v3", network="mainnet",
                    api_key=settings.TONCENTER_API_KEY)


async def get_wallet_funds(address: str) -> WalletFunds:
    account = await client.get_account(GetAccountRequest(address=address))

    jetton_wallets = await client.get_jetton_wallets(
        GetJettonWalletsRequest(owner_address=address, limit=10))

    ton_balance = account.balance / 1e9
    jettons = []
    for wallet in jetton_wallets:
        if wallet.balance == 0:
            continue
        jetton = await client.get_jetton_masters(wallet.jetton)

        content = jetton.jetton_content
        symbol = content.symbol if content else None
        symbol = symbol if symbol != "None" else None
        decimals = (content.decimals if content else 0) or 9

        jettons.append(
            WalletJettonInfo(
                address=str(wallet.address),
                symbol=symbol,
                balance=wallet.balance / 10 ** decimals,
                name=content.name if content else None,
                description=content.description if content else None,
                image=content.image if content else None
            )
        )
    info = WalletFunds(ton=ton_balance, jettons=jettons)
    return info

# if __name__ == "__main__":
#     asyncio.run(get_wallet_funds("UQBpqp3ScjiymiZRVYwFbbAdHj5xLwI0o57P0J8UrK2v_VHQ"))
