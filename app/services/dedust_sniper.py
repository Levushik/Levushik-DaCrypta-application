import asyncio

from dedust import Asset, Factory, PoolType
from pytoniq import LiteBalancer, WalletV4R2

import dedust_swapper

TON = Asset.native()
swapper = dedust_swapper.DedustSwapper()


async def snipe(wallet: WalletV4R2, jetton_addr: str, ton_amount: int):
    jetton = Asset.jetton(jetton_addr)
    pool = await Factory.get_pool(
        PoolType.VOLATILE,
        [TON, jetton],
        wallet.provider
    )
    print(f"Pool: {pool.address.to_str()}")
    print(f"Ready: {await pool.get_readiness_status()}")


async def main():
    client = LiteBalancer.from_mainnet_config(trust_level=1)
    await client.start_up()
    wallet = await WalletV4R2.from_mnemonic(mnemonics=mnemonics, provider=client)

    # jetton = input("Jetton to snipe: ")
    # ton_amount = int(input("Ton amount to snipe: "))
    jetton = "EQCIjedTOPMPCnMcskby87y1tOhawx99lKMUIqbaJkuI4Z6a"
    ton_amount = 0
    await snipe(wallet, jetton, ton_amount)


asyncio.get_event_loop().run_until_complete(main())
