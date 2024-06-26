# Property Search

## One-time setup
```shell
pyenv deactivate                                                                                                                                         master  ✭ ✱
pyenv activate experimental-propsearch
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Download ChromeDriver, maybe: https://googlechromelabs.github.io/chrome-for-testing/

## Sourcing Addresses
Go to [Overpass Turbo](https://overpass-turbo.eu). Draw a Bounding Box. Run the query: 
```text
[out:csv("addr:street", "addr:housenumber"; false)];
(
  node["addr:housenumber"]["addr:street"]({{bbox}});
);
out;
```

Save results (select all, copy, paste) into `base.tsv`.

Clean the data 
`sed 's/ 1\/2//g' base.tsv | sort | uniq > base_clean.tsv`

## Sourcing Properties' Properties

https://chatgpt.com/c/72a1481b-0679-4f75-be51-8983b813d077

```shell
python crawler.py
```


