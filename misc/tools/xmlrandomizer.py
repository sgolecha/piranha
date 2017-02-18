#!/usr/bin/python3.5

import pprint
import sys
import random
import re
import xml.etree.ElementTree as ET
import xml.dom.minidom

class Randomizer:
    """
    a simple xml file randomizer - given a
    valid xml file, returns a random subtree
    when getRandomSubTree is called.
    """
    def __init__(self, xmlFile, **kwargs):
        self._parser = PCParser()
        self._file = xmlFile
        self._tree = ET.parse(xmlFile, parser=self._parser)

    def getRandomSubTree(self, outFile=None):
        """
        returns a random subtree as a string.
        will write it outFile as well
        """
        newTree = self._createEmptyTree(self._tree.getroot())
        while (len(newTree.getroot().keys()) == 0 and
                len(list(newTree.getroot())) == 0):
            self._buildRandomTree(
                    self._tree.getroot(),
                    newTree.getroot()
                    )

        parsedStr = xml.dom.minidom.parseString(ET.tostring(newTree.getroot()))
        lines = [line.rstrip() for line in parsedStr.toprettyxml().splitlines()
                                    if line.strip()]

        xmlStr = '\n'.join(lines)
        xmlStr = xmlStr.replace('&quot;', '"')
        if outFile:
            with open(outFile, 'w') as fileHandler:
                fileHandler.write(xmlStr)
        return xmlStr

    def getFullTree(self):
        """
        returns the entire tree as a string
        """
        parsedStr = xml.dom.minidom.parseString(
                            ET.tostring(self._tree.getroot())
                            )
        return '\n'.join([line.rstrip()
                            for line in parsedStr.toprettyxml().splitlines()
                                if line.strip()])

    def _createEmptyTree(self, oldRoot):
        rtreeRoot = ET.Element(oldRoot.tag)
        rtreeRoot.text = oldRoot.text
        for k, v in oldRoot.items():
            rtreeRoot.set(k, v)
        return ET.ElementTree(rtreeRoot)

    def _buildRandomTree(self, oldRoot, newRoot):
        for child in self._getRandomChildren(oldRoot):
            newChild = ET.SubElement(newRoot, child.tag)
            newChild.text = child.text
            for k, v in child.items():
                newChild.set(k, v)
            self._buildRandomTree(child, newChild)

    def _getRandomChildren(self, oldRoot):
        for child in list(oldRoot):
            random.seed()
            if random.uniform(0.0, 1.0) < 0.6:
                yield child

# Special XML parser to handle comments in XML
# Credit: Jon Thomason (stackoverflow)
class PCParser(ET.XMLTreeBuilder):
    def __init__(self):
        ET.XMLTreeBuilder.__init__(self)
        self._parser.CommentHandler = self.handle_comment

    def handle_comment(self, data):
        self._target.start(ET.Comment, {})
        self._target.data(data)
        self._target.end(ET.Comment)


if __name__ == "__main__":
    randomizer = Randomizer('./sample.xml')
    print(randomizer.getRandomSubTree())
