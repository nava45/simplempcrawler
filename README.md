## SimpleMPCrawler
Simple Multi processing crawler in python


### Problem stmt:

Using python's multiprocessing and any one of threading/gevent module, task is to write a web-scraper which takes a huge file as an input ( 1Million rows ) which contains a url in each line.
The scraper then uses BeatuifulSoup to parse the content and finds if the content contains "jquery.js". If it does, dump the url into a file "accepted.csv" or if it doesn't, dump it into file "rejected.csv".

### install
```

    virtualenv env/
    source env/bin/activate
    pip install -r requirements.txt
    python crawler.py

```

### test
```
python test_crawler.py
```

### steps

`urls.csv` is the input file which has list of urls to be processed

output `accepted.csv`, `rejected.csv` files will be created and the respective urls are put in to the respective files
