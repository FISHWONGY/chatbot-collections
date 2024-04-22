import re
import logging

from webex_bot.models.command import Command
from webex_bot.models.response import Response
import adaptivecardbuilder as adcb

from helpers.f1api import F1Scraper
import helpers.adaptive_cards as adaptive_cards

logger = logging.getLogger(__name__)

f1api = F1Scraper()


class Ping(Command):
    def __init__(self):
        super().__init__(
            command_keyword="!ping",
            help_message="!ping - a simple ping command",
            card=None,
        )

    def execute(self, message, attachment_actions, activity):
        return "pong!"


class Driver(Command):
    def __init__(self):
        super().__init__(
            command_keyword="!f1",
            help_message="!f1 - get f1 driver points",
            card=adaptive_cards.DRIVER_CARD,
        )

    def execute(self, message, attachment_actions, activity):
        driver = attachment_actions.inputs["driver"]
        logger.info(f"{activity['actor']['emailAddress']} enquiring driver: {driver}")

        details = f1api.get_driver_points(driver)
        logger.info(f"Resposne: {details}")

        match = re.compile(r"(.*) has (\d+) points").search(details)

        card = adcb.AdaptiveCard()

        card.add(
            [
                adcb.ColumnSet(),
                    adcb.Column(width="auto"),
                        adcb.Image(
                            url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/F1.svg/1200px-F1.svg.png",
                            size="Medium",
                            height="20px",
                        ),
                    "<",
                    adcb.Column(width="stretch"),
                        adcb.TextBlock(text="Formula1 App", color="Accent", weight="Lighter"),
                        adcb.TextBlock(
                            text=f"Driver Statistics: {driver}",
                            size="Large",
                            weight="Bolder",
                            color="Light",
                        ),
                    "<",
                "<",
                adcb.ColumnSet(),
                    adcb.Column(width="stretch"),
                        adcb.FactSet(),
                            adcb.Fact(title="Driver:", value=f"{match.group(1)}"),
                            adcb.Fact(title="Points: ", value=f"{match.group(2)}"),
                "^",
                adcb.ActionSet(),
                    adcb.ActionShowCard(title="More Details", style="positive"),
                        adcb.ColumnSet(),
                            adcb.Column(width="stretch"),
                                adcb.FactSet(),
                                    adcb.Fact(
                                        title="Visit official website",
                                        value="[Click here](https://www.formula1.com/)",
                                    ),
            ]
        )

        card_data = adcb.json.loads(adcb.asyncio.run(card.to_json()))

        card_payload = {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": card_data,
        }
        response = Response()
        response.text = "F1 Card"
        response.attachments = card_payload

        return response
