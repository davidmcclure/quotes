

from lxml import etree


class Article:

    def __init__(self, path: str):

        """
        Parse the XML.
        """

        with open(path, 'r') as fh:
            self.xpath = etree.XPathEvaluator(etree.parse(fh))

    def first(self, query, cast=None):

        """
        Run a query, take the first result, cast type.
        """

        results = self.xpath(query)

        value = results[0] if results else None

        return cast(value) if cast else value

    def record_id(self) -> int:
        return self.first('RecordID/text()', int)

    def record_title(self) -> str:
        return self.first('RecordTitle/text()')

    def publication_id(self) -> int:
        return self.first('Publication/PublicationID/text()', int)

    def publication_title(self) -> str:
        return self.first('Publication/Title/text()')

    def publication_qualifier(self) -> str:
        return self.first('Publication/Qualifier/text()')

    def year(self) -> int:
        stamp = self.first('NumericPubDate/text()')
        return int(stamp[:4]) if stamp else None

    def source_type(self) -> str:
        return self.first('SourceType/text()')

    def object_type(self) -> str:
        return self.first('ObjectType/text()')

    def contributor_role(self) -> str:
        return self.first('Contributor/ContribRole/text()')

    def contributor_last_name(self) -> str:
        return self.first('Contributor/LastName/text()')

    def contributor_first_name(self) -> str:
        return self.first('Contributor/FirstName/text()')

    def contributor_person_name(self) -> str:
        return self.first('Contributor/PersonName/text()')

    def contributor_original_form(self) -> str:
        return self.first('Contributor/OriginalForm/text()')

    def language_code(self) -> str:
        return self.first('LanguageCode/text()')

    def full_text(self) -> str:
        return self.first('FullText/text()')
