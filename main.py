from pararius_scraper import ParariusScraper
from queries import DBQueries
from tables.emails import Email
from tables.houses import House
from tables.attempts import Attempt
import yahoo_mail
import os
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import logging
import time
load_dotenv(find_dotenv())

logging.basicConfig(level=logging.DEBUG,
                    filename=os.environ.get("LOGGING_FILEPATH"))


def email_houses(houses: list[House]) -> None:
    content = ''
    for house in houses:
        content += '\n'.join([house.link]) + '\n\n'

    yahoo_mail.send_email(
        yahoo_email=os.environ.get('YAHOO_EMAIL'),
        yahoo_app_password=os.environ.get('YAHOO_APP_PASSWORD'),
        subject=f"Found {len(houses)} new houses!",
        content=content,
        to=os.environ.get("TO_EMAIL"),
    )


def scrape_loop(scraper: ParariusScraper, dbqueries: DBQueries) -> None:

    current_timestamp = datetime.now()
    houses = scraper.scrape()
    logging.debug(f"Scraped {len(houses)} houses from Pararius.")

    for house in houses:
        dbqueries.add_house_if_not_exists(house)

    last_email_timestamp = dbqueries.get_last_email_timestamp()
    new_houses = dbqueries.get_houses_after_timestamp(last_email_timestamp)

    dbqueries.add_attempt(Attempt(timestamp=current_timestamp,
                                  total_houses=len(houses),
                                  totalnum_new_houses=len(new_houses)))

    if new_houses:
        email_houses(new_houses)
        dbqueries.add_email(Email(address=os.environ.get(
            "TO_EMAIL"), timestamp=datetime.now()))
        logging.debug(f"Found {len(new_houses)} new houses and emailed them!")
    else:
        logging.debug("Found no new houses.")


def main():

    scraper = ParariusScraper()
    dbqueries = DBQueries(
        host=os.environ.get('DB_POSTGRES_HOST'),
        database=os.environ.get('DB_POSTGRES_DATABASE'),
        username=os.environ.get('DB_POSTGRES_username'),
        password=os.environ.get('DB_POSTGRES_PASSWORD'),
    )

    minutes_between_scrape = int(os.environ.get("MINUTES_BETWEEN_SCRAPE"))

    while True:
        scrape_loop(scraper, dbqueries)
        time.sleep(minutes_between_scrape * 60)


if __name__ == "__main__":
    main()
