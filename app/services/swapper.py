from abc import ABC

from pytoniq import WalletV4R2


class Swapper(ABC):

    async def swap_to_native(wallet: WalletV4R2,
                             jetton_address: str,
                             amount: float):
        pass

    async def swap_to_jetton(wallet,
                             jetton_address: str,
                             amount: float, actual_for=60 * 5):
        pass
