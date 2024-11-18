import time

from dedust import Asset, Factory, PoolType, SwapParams, VaultNative, JettonRoot, VaultJetton
from pytoniq import WalletV4R2

from app.services.swapper import Swapper

GAS_VALUE = int(0.25 * 1e9)
DEDUST_NATIVE_VAULT = "EQDa4VOnTYlLvDJ0gZjNYm5PXfSmmtL6Vs6A_CZEtXCNICq_"
TON = Asset.native()


class DedustSwapper(Swapper):
    async def swap_to_jetton(wallet: WalletV4R2,
                             jetton_address: str,
                             amount: float,
                             actual_for=60 * 5):
        """Method swaps toncoins to jetton on dedust.
        
        Parameters
        ----------
        wallet : WalletV4R2, required
            Ton wallet which will swap ton to jetton

        jetton_address : str, required
            Contract address of wanted jetton

        amount : float, required
            Amount of ton to be swapped

        actual_for : int, optional
            Time in seconds for which request is actual
            (default is 5 minutes)
        """

        jetton = Asset.jetton(jetton_address)
        pool = await Factory.get_pool(PoolType.VOLATILE,
                                      [TON, jetton],
                                      wallet.provider)

        swap_params = SwapParams(deadline=int(time.time() + actual_for),
                                 recipient_address=wallet.address)
        swap_amount = int(amount * 1e9)  # Conversion to the format used by TON

        swap = VaultNative.create_swap_payload(amount=swap_amount,
                                               pool_address=pool.address,
                                               swap_params=swap_params)

        swap_amount = int(swap_amount) + GAS_VALUE

        await wallet.transfer(destination=DEDUST_NATIVE_VAULT,
                              amount=swap_amount,
                              body=swap)

    # Not sure it works
    async def swap_to_native(wallet: WalletV4R2, jetton_address: str, amount: float):
        """Method swaps jetoon to ton on dedust.
        
        Parameters
        ----------
        wallet : WalletV4R2, required
            Ton wallet which will swap ton to jetton

        jetton_address : str, required
            Contract address of wanted jetton

        amount : float, required
            Amount of jetton to be swapped
        """
        jetton = Asset.jetton(jetton_address)

        pool = await Factory.get_pool(PoolType.VOLATILE,
                                      [TON, jetton],
                                      wallet.provider)

        jetton_vault = await Factory.get_jetton_vault(jetton_address, wallet.provider)
        jetton_root = JettonRoot.create_from_address(jetton_address)
        jetton_wallet = await jetton_root.get_wallet(wallet.address, wallet.provider)

        swap_amount = int(amount * 1e9)

        swap = jetton_wallet.create_transfer_payload(
            destination=jetton_vault.address,
            amount=swap_amount,
            response_address=wallet.address,
            forward_amount=GAS_VALUE,
            forward_payload=VaultJetton.create_swap_payload(pool_address=pool.address)
        )

        await wallet.transfer(destination=jetton_wallet.address,
                              amount=int(0.3*1e9),
                              body=swap)
