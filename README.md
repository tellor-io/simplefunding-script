# Simple Feed Funding Script

Use for funding autopay through cli

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

### Usage
**To tip single query**
```sh
autopay my-acct <chain id> tip
```

**To fund a single existing feed**
```sh
autopay my-acct <chain id> fundfeed --fund-only
```

**To setup and fund a single feed**
```sh 
autopay my-acct <chain id> fundfeed --setup-datafeed
```

**To tip all queries in fundfeed/catalog.py**
```sh
autopay my-acct <chain id> tip --tip-all
```

**To approve a specific autopay spending**
```sh
autopay my-acct <chain id> approve-autopay
```

**Available for testing**
```sh
autopay my-acct <chain id> setupdatafeed
```

**Build query data for ease access**
- Note: doesn't handle all cases right now only uint and string
- Also working on removing my-acct and chain id from cmd since not needed
```sh
autopay my-acct <chain id> build-query
```