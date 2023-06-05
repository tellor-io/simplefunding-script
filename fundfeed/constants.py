from dataclasses import dataclass
import os
from dotenv import find_dotenv
from dotenv import load_dotenv
from eth_utils import to_checksum_address

print(f"env loaded: {load_dotenv(find_dotenv())}")

GAS = os.getenv("GAS")
GAS_MULTIPLIER = int(os.getenv("GAS_MULTIPLIER", 1))


@dataclass
class Directory:
    network: str
    autopay_address: str
    token_address: str
    node: str

    def __post_init__(self):
        self.autopay_address = to_checksum_address(self.autopay_address)
        self.token_address = to_checksum_address(self.token_address)


CHAINS: dict[int, Directory] = {
    1: Directory(
        network="Mainnet",
        autopay_address="0x9BE9B0CFA89Ea800556C6efbA67b455D336db1D0",
        token_address="0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0",
        node="MAINNET_NODE",
    ),
    5: Directory(
        network="Görli",
        autopay_address="0x9BE9B0CFA89Ea800556C6efbA67b455D336db1D0",
        token_address="0x51c59c6cAd28ce3693977F2feB4CfAebec30d8a2",
        node="GOERLI_NODE",
    ),
    11155111: Directory(
        network="Sepolia",
        autopay_address="0x7E7b96d13D75bc7DaF270A491e2f1e571147d4DA",
        token_address="0x80fc34a2f9FfE86F41580F47368289C402DEc660",
        node="SEPOLIA_NODE",
    ),
    137: Directory(
        network="Polygon",
        autopay_address="0x9BE9B0CFA89Ea800556C6efbA67b455D336db1D0",
        token_address="0xE3322702BEdaaEd36CdDAb233360B939775ae5f1",
        node="POLYGON_NODE",
    ),
    80001: Directory(
        network="Mumbai",
        autopay_address="0x9be9b0cfa89ea800556c6efba67b455d336db1d0",
        token_address="0xCE4e32fE9D894f8185271Aa990D2dB425DF3E6bE",
        node="MUMBAI_NODE",
    ),
    100: Directory(
        network="Gnosis",
        autopay_address="0x9BE9B0CFA89Ea800556C6efbA67b455D336db1D0",
        token_address="0xAAd66432d27737ecf6ED183160Adc5eF36aB99f2",
        node="GNOSIS_CHAIN_NODE",
    ),
    10200: Directory(
        network="Chiado",
        autopay_address="0x9BE9B0CFA89Ea800556C6efbA67b455D336db1D0",
        token_address="0xe7147C5Ed14F545B4B17251992D1DB2bdfa26B6d",
        node="CHIADO_NODE",
    ),
    10: Directory(
        network="Optimism",
        autopay_address="0x9BE9B0CFA89Ea800556C6efbA67b455D336db1D0",
        token_address="0xaf8cA653Fa2772d58f4368B0a71980e9E3cEB888",
        node="OPTIMISM_NODE",
    ),
    420: Directory(
        network="Optimism Goerli",
        autopay_address="0x9BE9B0CFA89Ea800556C6efbA67b455D336db1D0",
        token_address="0xd71F72C18767083e4e3FE84F9c62b8038C1Ef4f6",
        node="OPTIMISM_GOERLI_NODE",
    ),
    42161: Directory(
        network="Arbitrum",
        autopay_address="0x9BE9B0CFA89Ea800556C6efbA67b455D336db1D0",
        token_address="0xd58D345Fd9c82262E087d2D0607624B410D88242",
        node="ARBITRUM_ONE_NODE",
    ),
    421613: Directory(
        network="Arbitrum Goerli",
        autopay_address="0x60cBf3991F05a0671250e673Aa166e9D1A0C662E",
        token_address="0x8d1bB5eDdFce08B92dD47c9871d1805211C3Eb3C",
        node="ARBITRUM_GOERLI_NODE",
    ),
    314: Directory(
        network="Filecoin",
        autopay_address="0x60cBf3991F05a0671250e673Aa166e9D1A0C662E",
        token_address="0x045CE60839d108B43dF9e703d4b25402a6a28a0d",
        node="FILECOIN_NODE",
    ),
    3141: Directory(
        network="Hyperspace",
        autopay_address="0x60cBf3991F05a0671250e673Aa166e9D1A0C662E",
        token_address="0x045CE60839d108B43dF9e703d4b25402a6a28a0d",
        node="FILECOIN_HYPERSPACE_NODE",
    ),
}
