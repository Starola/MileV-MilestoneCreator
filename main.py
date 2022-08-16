# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import xml.dom.minidom
import requests
from requests_jwt import JWTAuth


URL = "http://localhost:8090/milestone"


def get_all_milestones():
    """
    Returns a list of all mielstones that can be reached in a BPMN process
    :return:
    """
    # Use a breakpoint in the code line below to debug your script.
    document = read_xml_file("D:\Testmodelle\CommunicationByMilestone.bpmn");
    elements = document.getElementsByTagName("bpmn:signalEventDefinition")
    pretty_xml_as_string = document.toprettyxml()
    """
    Gets the signalRef of every element that has the type bpmn:signalEventDefinition of an event of the type bpmn:endEvent
    """
    elementList = []
    for endEvent in document.getElementsByTagName("bpmn:endEvent"):
        for element in endEvent.getElementsByTagName("bpmn:signalEventDefinition"):
            elementList.append(element.getAttribute("signalRef"))
    """
    Gets the name of every milestone (based on sending signal events
    """
    milestones = []
    for signal in document.getElementsByTagName("bpmn:signal"):
        signalId = signal.getAttribute("id")
        if signalId in elementList:
            signal_name = signal.getAttribute("name")
            signal_name_list = signal_name.partition("-")
            if signal_name_list[0] == "MS":
                milestone_name = signal_name_list[2].partition("-")[0]
                milestones.append(milestone_name)
    return milestones

def create_milestones(milestones):
    """
    Creates all found milestones
    :param milestones: A list of all milestones in the process (as string)
    """
    for milestone in milestones:
        PARAMS = createParams(milestone)
        r = requests.post(URL, json=PARAMS)
    print(r)


def createParams(milestone):
    PARAMS = {"milestoneName": milestone, "description": "misisng"}
    return PARAMS

def read_xml_file(filepath):
        """
        Reads BPMN XML file from given filepath.
        """
        dom_tree = xml.dom.minidom.parse(filepath)
        return dom_tree

def main():
    milestones = get_all_milestones()
    print(milestones)
    create_milestones(milestones)
if __name__ == "__main__":
    main()


