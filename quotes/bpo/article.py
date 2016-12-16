

from lxml import etree


class Article:

    def __init__(self, path: str):

        """
        Parse the XML.
        """

        with open(path, 'r') as fh:
            self.xpath = etree.XPathEvaluator(etree.parse(fh))

    def record_id(self) -> int:
        return int(self.xpath('RecordID/text()')[0])

    def record_title(self) -> str:
        return self.xpath('RecordTitle/text()')[0]

    def publication_id(self) -> int:
        return int(self.xpath('Publication/PublicationID/text()')[0])

    def publication_title(self) -> str:
        return self.xpath('Publication/Title/text()')[0]

    def publication_qualifier(self) -> str:
        return self.xpath('Publication/Qualifier/text()')[0]

    def contributor_role(self) -> str:
        return self.xpath('Contributor/ContribRole/text()')[0]

    def contributor_last_name(self) -> str:
        return self.xpath('Contributor/LastName/text()')[0]

    def contributor_first_name(self) -> str:
        return self.xpath('Contributor/FirstName/text()')[0]

    def contributor_person_name(self) -> str:
        return self.xpath('Contributor/PersonName/text()')[0]

    def contributor_original_form(self) -> str:
        return self.xpath('Contributor/OriginalForm/text()')[0]

    def language_code(self) -> str:
        return self.xpath('LanguageCode/text()')[0]

    def full_text(self) -> str:
        return self.xpath('FullText/text()')[0]
