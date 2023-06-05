# Simple Feed Funding Script

Use for funding autopay through cli

### Clone repo and cd
```sh
git clone https://github.com/tellor-io/simplefunding-script.git
```
```sh
cd simplefunding-script
```
```sh
mv .env.example .env
```

Before further setup, add node urls to .env file.

### Setup

```sh
python3 -m venv venv
```
```sh
source venv/bin/activate
```

```sh
pip install -e .
```

**To add account**
```sh
chained add <my-new-account-name> <private key> <chain ids>
```
ex. 
```sh
chained add my-eth-acct 0x57fe7105302229455bcfd58a8b531b532d7a2bb3b50e1026afa455cd332bf706 1 4
```

### Usage
**To tip single query**
```sh
autopay <my-account-name> <chain id> tip
```
Then follow the prompts in the CLI...here's an example.
```sh
env loaded: True
Enter funding amount: 2
Repeat for confirmation: 2
GOERLI_NODE set!
Build query data? Enter y if query data not available [y/N]: y
Enter query type: SpotPrice
Enter parameter types separated by space: string string
Enter parameters separated by space: eth usd
Allowance: 0
Approving token spend...
Enter encryption password for <my-account-name>: 
approve txn: 0x586bc308473b4ce5429dd4236b27822dee8c1de8ac325e1821981265669bb251
tip txn: 0xd4d9ab618b8589178d0fc1b932e60ee0144556b475aef4c87f7388b06002b4ba
```


**To setup and fund a single feed**
```sh 
autopay <my-account-name> <chain id> fundfeed --setup-datafeed
```

Then follow the prompts in the CLI...here's an example.
```sh
autopay <my-account-name> 5 fundfeed --setup-datafeed
env loaded: True
Enter funding amount: 11
Repeat for confirmation: 11
GOERLI_NODE set!
Reward: 5
Window: 300
Current time: 1672859111
Start time: 1672859111
Interval: 3600
Price threshold (hint: enter 0.01 for 1% price change): 0.01
Reward increase (hint: 0 for flat reward): 1
Build query data? Enter y if query data not available [y/N]: y
Enter query type: SpotPrice
Enter parameter types separated by space: string string
Enter parameters separated by space: eth usd
Allowance: 0
Approving token spend...
Enter encryption password for <my-account-name>: 
approve txn: 0x83ed50be4778149302420b589191615d629e3b8e369bc7627ee151e3f73c7de8
setupDataFeed txn: 0x41299e3c6cc821f73bf8c319a0e2c12f58d7879691de304b3c2548c21f1096da
```

**To fund a single existing feed**

Please reference see the documentation on [funding-a-feed](https://docs.tellor.io/tellor/getting-data/funding-a-feed#recurring-data-feed) for info on input arguments.
```sh
autopay <my-account-name> <chain id> fundfeed --fund-only
```



**To approve a specific amount for autopay spending**
```sh
autopay <my-account-name> <chain id> approve-autopay
```

**To tip all queries in fundfeed/catalog.py**
```sh
autopay <my-account-name> <chain id> tip --tip-all
```


**Build query data for ease access**
- Note: doesn't handle all cases right now only uint and string
```sh
autopay <my-account-name> <chain id> build-query
```

**To delete account**
```sh
chained delete <account-name-to-delete>
```
