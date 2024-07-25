from argparse import ArgumentParser
from datetime import datetime
from hankyung_scraper import HanKyungScraper
import json
import logging

def create_parser() -> ArgumentParser:
    today = datetime.today().strftime("%Y%m%d")

    parser = ArgumentParser()
    parser.add_argument("-s", "--start_date", type=str, required=True, help="example: 20240504")
    parser.add_argument("-e", "--end_date", type=str, default=today, help=f"example: {today}")
    parser.add_argument("-o", "--output", type=str, default="output.json", help="output json file path")
    return parser

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    scraper = HanKyungScraper(args.start_date, args.end_date)
    articles = scraper.get_articles()

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)

    logging.info(f"Data saved to {args.output}")
