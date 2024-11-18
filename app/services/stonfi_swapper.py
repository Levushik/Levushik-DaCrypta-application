from pytoniq import WalletV4R2
from stonfi import RouterV1

from app.services.swapper import Swapper


class StonfiSwapper(Swapper):

    async def swap_to_jetton(wallet: WalletV4R2, jetton_address: str, amount: float,
                             actual_for=60 * 5):
        router = RouterV1()
        amount = int(amount * 1e9)
        params = await router.build_swap_ton_to_jetton_tx_params(wallet.address,
                                                                 jetton_address,
                                                                 amount,
                                                                 1,
                                                                 wallet.provider)
        resp = await wallet.transfer(
            params['to'],
            params['amount'],
            params['payload']
        )
        return resp

    async def swap_to_native(wallet, jetton_address: str, amount: float):
        router = RouterV1()
        amount = int(amount * 1e9)
        params = await router.build_swap_jetton_to_ton_tx_params(
            user_wallet_address=wallet.address,
            offer_jetton_address=jetton_address,
            offer_amount=amount,
            min_ask_amount=1,
            provider=wallet.provider,
        )

        resp = await wallet.transfer(
            params['to'],
            params['amount'],
            params['payload']
        )
        return resp
