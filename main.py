from crawler import Crawler
from args import get_args
import csv

if __name__ == '__main__':
    args = get_args()
    crawler = Crawler()
    content = crawler.crawl(args.start_date, args.end_date)
    # TODO: write content to file according to spec
    with open('{}'.format(args.output), 'w', newline="",encoding='utf-8') as fp:
        fper = csv.writer(fp)
        fper.writerow(["Post Date","Title","Content"])
        for data in content:
            if (type(data))==str:
                ##data=data.replace('"','""')
                fp.write(data) 
            else:
                fp.write(str(data))
