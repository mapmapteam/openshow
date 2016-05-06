#!/usr/bin/env python
# -*- coding: utf-8; tab-width: 4; mode: python -*-
# -*- test-case-name: mindlab.test.test_config -*-
"""
Configuration options.
"""
from xml.dom import minidom
from xml.parsers.expat import ExpatError
import os
import pprint

DEFAULT_CONFIG_FILE_DIR = "~/.mindlab"
DEFAULT_CONFIG_FILE_NAME = "config.xml"
DEFAULT_XML_CONTENTS = """<?xml version="1.0"?>
<mindlab_configuration>
    <!-- Version of the format standard for this file -->
    <version value="2.0" />

    <!-- Option entries -->
    <option key="mongodb_host" value="localhost" />
    <option key="mongodb_port" value="27017" />
    <option key="mongodb_database" value="mindlab" />

    <option key="verbose" value="True" />

    <option key="elasticsearch_host" value="localhost" />
    <option key="elasticsearch_port" value="9200" />
    <option key="elasticsearch_database" value="mindlab" />

    <option key="word2vecservice_host" value="163.172.5.251" />
    <option key="word2vecservice_port" value="8888" />

    <option key="number_of_nlptookit_managers_in_parallel" value="1" />
    <option key="number_of_pages_to_parse_in_parallel" value="1" />
</mindlab_configuration>
"""

# TODO: <option key="mongodb_user" value="default" />
# TODO: <option key="mongodb_password" value="" />
# TODO: <option key="elasticsearch_user" value="default" />
# TODO: <option key="elasticsearch_password" value="" />


class Configuration(object):

    """
    Configuration options for this application.

    Loads from an XML file.
    """

    def __init__(self):
        # public attributes
        self.mongodb_host = "localhost"
        self.mongodb_port = 27017
        # TODO self.mongodb_user = "default"
        # TODO self.mongodb_password = ""
        self.mongodb_database = "mindlab"

        self.elasticsearch_host = "localhost"
        self.elasticsearch_port = 9200
        self.elasticsearch_database = "default"
        # TODO self.elasticsearch_user = "default"
        # TODO self.elasticsearch_password = ""

        self.word2vecservice_host = "163.172.5.251"
        self.word2vecservice_port = 8888

        self.number_of_nlptookit_managers_in_parallel = 1
        self.number_of_pages_to_parse_in_parallel = 1

        self.verbose = False
        self._config_file_path = ""

    def __str__(self):
        return pprint.pformat(self.__dict__)

    def parse_config_file(self, config_file_path):
        """
        Make sure to set_screen_identifier first.
        Make sure the config_file_path exists.
        :raise: RuntimeError
        """
        if not os.path.exists(config_file_path):
            raise RuntimeError(
                "Config file does not exist: %s." %
                (config_file_path))

        self._config_file_path = config_file_path
        try:
            doc = minidom.parse(self._config_file_path)
            self._parse_options(doc)
        except ExpatError as e:
            msg = "Failed to parse XML file %s %s" % (
                self._config_file_path, e)
            print(msg)
            raise RuntimeError(msg)

    def _parse_options(self, doc):
        """
        @param doc: xml.dom.minidom.Document instance
        @param screen: int from 1 to 8
        """
        # ret = []
        option_elements = doc.getElementsByTagName("option")
        for option_element in option_elements:
            key = ""
            value = ""
            is_valid = True
            if option_element.hasAttribute("key"):
                key = option_element.getAttribute("key")
            if option_element.hasAttribute("value"):
                value = option_element.getAttribute("value")
            if key in self.__dict__:
                # get type
                typ = type(self.__dict__[key])

                # cast value
                if typ == bool:
                    value = value.lower().strip() in [
                        "true", "yes", "oui", "1"]
                elif typ == int:
                    try:
                        value = int(value)
                    except ValueError as e:
                        print("Invalid int %s" % (e))
                        value = ""
                        is_valid = False

                elif typ == str:
                    value = str(value)

                # Assign value
                if is_valid:
                    self.__dict__[key] = value


def load_config_from_file(file_path):
    # Create dir and file if they don't exist
    file_path = os.path.expanduser(file_path)
    dir_name = os.path.dirname(file_path)
    if not os.path.exists(dir_name):
        # TODO: error handling
        os.mkdir(dir_name)
    if not os.path.exists(file_path):
        # TODO: error handling
        with open(file_path, 'w') as f:
            f.write(DEFAULT_XML_CONTENTS)

    ret = Configuration()
    ret.parse_config_file(file_path)
    return ret


def load_config_from_default_file():
    file_path = os.path.join(DEFAULT_CONFIG_FILE_DIR, DEFAULT_CONFIG_FILE_NAME)
    return load_config_from_file(file_path)


if __name__ == "__main__":
    # Example usage:
    config = load_config_from_default_file()
    pprint.pprint(config.__dict__)
