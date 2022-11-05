from dataclasses import dataclass
import os
from dotenv import find_dotenv
from dotenv import load_dotenv

print(f"env loaded: {load_dotenv(find_dotenv())}")

GAS = int(os.getenv("GAS",900000))
GAS_MULTIPLIER = int(os.getenv("GAS_MULTIPLIER", 1))

def fallback_input(_key: str):
    """Prompt input if no .env setup"""
    val = os.getenv(_key, None)
    if not val:
        return input(f"Enter {_key}:\n")
    print(f"{_key} set!")
    return val

@dataclass
class Directory:
    network: str
    autopay_address: str
    token_address: str
    node: str

CHAINS: dict[int, Directory] = {
    1: Directory(network="Mainnet", autopay_address="0x1F033Cb8A2Df08a147BC512723fd0da3FEc5cCA7", token_address='0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0', node='MAINNET_NODE'),
    5: Directory(network="Görli", autopay_address='0x1F033Cb8A2Df08a147BC512723fd0da3FEc5cCA7', token_address='0x51c59c6cAd28ce3693977F2feB4CfAebec30d8a2', node='GOERLI_NODE'),
    137: Directory(network="Polygon", autopay_address='0xb1BA09F56F3E6A58680b88e0af7e32F30A61C1Bb', token_address='0xE3322702BEdaaEd36CdDAb233360B939775ae5f1', node='POLYGON_NODE'),
    80001: Directory(network="Mumbai", autopay_address='0x1775704809521D4D7ee65B6aFb93816af73476ec', token_address='0xce4e32fe9d894f8185271aa990d2db425df3e6be', node='MUMBAI_NODE'),
}
