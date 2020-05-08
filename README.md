# ScrapyKeeper

A scalable admin ui for scrapy spider service 

It's fork of [ScrapyKeeper](https://github.com/fliot/ScrapyKeeper) and [SpiderKeeper](https://github.com/DormyMo/SpiderKeeper)

Contains all of the previous versions and a number of updates:
  - requirements updated to latest versions
  - in the periodic task added items:
    - Max start tasks - The number of maximum tasks that can hang on the launch and be in work
    - Number of start-ups - The number of simultaneously launched copies of scrapy
  - You can add an entry to the log QUERY <<$MY TEXT$>> and show up in completed tasks
    - $MY TEXT$ - need change
    - It’s convenient when you start the parser several times with different input parameters and want to see what happens
  - fix any bugs 

## Screenshot
![job dashboard](https://raw.githubusercontent.com/fliot/ScrapyKeeper/master/screenshot/screenshot_1.png)
![periodic job](https://raw.githubusercontent.com/fliot/ScrapyKeeper/master/screenshot/screenshot_2.1.png)
![project stats](https://raw.githubusercontent.com/fliot/ScrapyKeeper/master/screenshot/screenshot_3.png)
![spider stats](https://raw.githubusercontent.com/fliot/ScrapyKeeper/master/screenshot/screenshot_4.png)

How to install ?
```sh
git clone https://github.com/fliot/ScrapyKeeper.git
cd ScrapyKeeper
pip install .
```

Running:
```sh
scrapykeeper -h

Usage: scrapykeeper [options]

Admin ui for scrapy spider service

Options:
  -h, --help            show this help message and exit
  --host=HOST           host, default:0.0.0.0
  --port=PORT           port, default:5000
  --username=USERNAME   basic auth username ,default: admin
  --password=PASSWORD   basic auth password ,default: admin
  --type=SERVER_TYPE    access spider server type, default: scrapyd
  --server=SERVERS      servers, default: ['http://localhost:6800']
  --database-url=DATABASE_URL
                        ScrapyKeeper metadata database default: sqlite://./ScrapyKeeper.db
  --no-auth             disable basic auth
  --no-sentry           disable sentry.io error reporting
  -v, --verbose         log level
```
