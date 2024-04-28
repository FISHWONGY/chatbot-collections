from lxml import html
import requests
import logging

logger = logging.getLogger(__name__)


class F1Scraper:
    def __init__(self):
        self.driver_stat_url = (
            "https://www.formula1.com/en/results.html/2024/drivers.html"
        )
        self.all_driver_data, self.driver_initials_to_full_name = (
            self.get_all_driver_pts()
        )

    @staticmethod
    def scrape_f1(web_url: str) -> list:
        page = requests.get(web_url)
        tree = html.fromstring(page.content)

        table_rows = tree.cssselect("table.resultsarchive-table tr")
        column_headers = [column.text_content().strip() for column in table_rows[0]]

        data_rows = []
        for row in table_rows[1:]:
            data = [column.text_content().strip() for column in row.iterchildren()]
            data_rows.append(dict(zip(column_headers, data)))

        return data_rows

    def get_all_driver_pts(self) -> (dict, dict):
        data_rows = self.scrape_f1(self.driver_stat_url)

        dr_pts = {}
        driver_full_names = {}
        for row in data_rows:
            dr_name_parts = row["Driver"].replace("\n", "").split()
            initials = (
                dr_name_parts[-1]
                if len(dr_name_parts) == 3
                else "".join([name[0] for name in dr_name_parts])
            )
            full_name = (
                " ".join(dr_name_parts[:-1])
                if len(dr_name_parts) == 3
                else " ".join(dr_name_parts)
            )
            pts = row["PTS"]
            dr_pts[initials] = pts
            driver_full_names[initials] = full_name

        logger.info("Driver scores retrieved")
        return dr_pts, driver_full_names

    def get_driver_points(self, initials: str) -> str:
        full_name = self.driver_initials_to_full_name.get(initials)
        pts = self.all_driver_data.get(initials)
        if full_name and pts:
            re = f"{full_name} has {pts} points"
        else:
            re = "Invalid driver initials. Please check the driver initials and try again."
        return re
