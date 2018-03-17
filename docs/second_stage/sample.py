from lxml import etree


def parseXML(xmlFile):
    """Parsing XML"""
    with open(xmlFile) as fobj:
        xml = fobj.read()

    root = etree.fromstring(xml)

    for appt in root.getchildren():
        for elem in appt.getchildren():
            if not elem.text:
                text = "None"
            else:
                text = elem.text

            print(elem.tag + " => " + text)


if __name__ == "__main__":
    parseXML("example.xml")
