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
    1: Directory(network="Mainnet", autopay_address="0x9BE9B0CFA89Ea800556C6efbA67b455D336db1D0", token_address='0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0', node='MAINNET_NODE'),
    5: Directory(network="Görli", autopay_address='0x9BE9B0CFA89Ea800556C6efbA67b455D336db1D0', token_address='0x51c59c6cAd28ce3693977F2feB4CfAebec30d8a2', node='GOERLI_NODE'),
    137: Directory(network="Polygon", autopay_address='0x9BE9B0CFA89Ea800556C6efbA67b455D336db1D0', token_address='0xE3322702BEdaaEd36CdDAb233360B939775ae5f1', node='POLYGON_NODE'),
    80001: Directory(network="Mumbai", autopay_address='0x9BE9B0CFA89Ea800556C6efbA67b455D336db1D0', token_address='0xce4e32fe9d894f8185271aa990d2db425df3e6be', node='MUMBAI_NODE'),
    10200: Directory(network="Chiado", autopay_address='0x9BE9B0CFA89Ea800556C6efbA67b455D336db1D0', token_address='0xe7147C5Ed14F545B4B17251992D1DB2bdfa26B6d', node='CHIADO_NODE'),
    100: Directory(network="Gnosis Chain", autopay_address='0x18274f81f683fdd8739888a877a3a1f591009e35', token_address='0xaad66432d27737ecf6ed183160adc5ef36ab99f2', node='GNOSIS_CHAIN_NODE'),
    10: Directory(network="Optimism", autopay_address='0x9BE9B0CFA89Ea800556C6efbA67b455D336db1D0', token_address='0xaf8cA653Fa2772d58f4368B0a71980e9E3cEB888', node='OPTIMISM_NODE'),
    421613: Directory(network="Arbitrum Goerli", autopay_address='0x60cBf3991F05a0671250e673Aa166e9D1A0C662E', token_address='0x8d1bB5eDdFce08B92dD47c9871d1805211C3Eb3C', node='ARBITRUM_GOERLI_NODE'),
    42161: Directory(network="Arbitrum One", autopay_address='0xd844B26dfAfB0776E70aF12C19189b740329A266', token_address='0xd58d345fd9c82262e087d2d0607624b410d88242', node='ARBITRUM_ONE_NODE'),
    3141: Directory(network="Filecoin Hyperspace", autopay_address='0x60cBf3991F05a0671250e673Aa166e9D1A0C662E', token_address='0xe7147C5Ed14F545B4B17251992D1DB2bdfa26B6d', node='FILECOIN_HYPERSPACE_NODE'),
}
