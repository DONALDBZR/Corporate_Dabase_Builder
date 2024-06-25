"""
The module which will have the model needed to generate the
portable document file version of the corporate registry, as
well as extracting the data from it before deleting it from
the cache of the server of the application.

Authors:
    Andy Ewen Gaspard
"""


from Models.Logger import Corporate_Database_Builder_Logger
from Data.DocumentFiles import DocumentFiles
from Environment import Environment
from typing import Dict, Union, List
from pdfminer.high_level import extract_text
from datetime import datetime


class Document_Reader:
    """
    The model needed to generate the portable document file
    version of the corporate registry, as well as extracting the
    data from it before deleting it from the cache of the server
    of the application.
    """
    __logger: Corporate_Database_Builder_Logger
    """
    The logger that will all the action of the application.
    """
    ENV: Environment
    """
    The ENV file of the application which stores the important
    information which allows the application to operate
    smoothly.
    """

    def __init__(self) -> None:
        """
        Initializing the document reader which will import and
        initialize the dependencies.
        """
        self.ENV = Environment()
        self.setLogger(Corporate_Database_Builder_Logger())
        self.getLogger().inform("The builder has been initialized and all of its dependencies are injected!")

    def getLogger(self) -> Corporate_Database_Builder_Logger:
        return self.__logger

    def setLogger(self, logger: Corporate_Database_Builder_Logger) -> None:
        self.__logger = logger

    def generatePortableDocumentFile(self, dataset: DocumentFiles) -> int:
        """
        Generating the portable document file based on the dataset
        passed as parameter.

        Parameters:
            dataset: {identifier: int, file_data: bytes, company_detail: int}: The dataset of the corporate registry retrieved from the relational database server.

        Returns:
            int
        """
        file_name: str = f"{self.ENV.getDirectory()}Cache/CorporateDocumentFile/Documents/{dataset.company_detail}.pdf"
        file = open(file_name, "wb")
        file.write(dataset.file_data)
        file.close()
        status: int = 201
        self.getLogger().inform(f"The portable document file of the corporate registry has been generated!\nLocation: {file_name}\nDocument File Identifier: {dataset.identifier}\nCompany Detail Identifier: {dataset.company_detail}\nStatus: {status}")
        return status

    def extractData(self, status: int, dataset: DocumentFiles) -> Dict:
        """
        Extracting the data from the portable document file version
        of the corporate registry based on the status of the file
        generation as well as on the dataset.

        Parameters:
            status: int: The status of the file generation.
            dataset: {identifier: int, file_data: bytes, company_detail: int}: The dataset of the corporate registry retrieved from the relational database server.

        Returns:
            {status: int}
        """
        file_name: str = f"{self.ENV.getDirectory()}Cache/CorporateDocumentFile/Documents/{dataset.company_detail}.pdf"
        if status == 201:
            portable_document_file_data: str = extract_text(file_name)
            portable_document_file_data_result_set: List[str] = list(filter(None, portable_document_file_data.split("\n")))
            business_registration_number: str = portable_document_file_data_result_set[[index for index, value in enumerate(portable_document_file_data_result_set) if "Business Registration No.:" in value][0]].split(" ")[-1]
            name: str = portable_document_file_data_result_set[portable_document_file_data_result_set.index("Name:") + 2]
            file_number: str = portable_document_file_data_result_set[portable_document_file_data_result_set.index("File No.:") + 1]
            category: str = portable_document_file_data_result_set[portable_document_file_data_result_set.index("Category:") + 1]
            date_incorporation: int = int(datetime.strptime(portable_document_file_data_result_set[portable_document_file_data_result_set.index("Date Incorporated:") + 1], "%d/%m/%Y").timestamp())
            nature: str = portable_document_file_data_result_set[portable_document_file_data_result_set.index("Nature:") + 3]
            company_status: str = portable_document_file_data_result_set[portable_document_file_data_result_set.index("Status:") + 3]
            print(f"Dataset: {portable_document_file_data_result_set}\n----------\nBusiness Registration Number: {business_registration_number}\nName: {name}\nFile Number: {file_number}\nCategory: {category}\nDate of Incorporation (Timestamp): {date_incorporation}\nNature: {nature}\nStatus: {company_status}")
            exit()
            # Extracting the data from the portable document file.
        else:
            self.getLogger().error(f"The portable document file has not been generated correctly!  The application will abort the extraction.\nStatus: {status}\nFile Location: {file_name}\nDocument File Identifier: {dataset.identifier}\nCompany Detail Identifier: {dataset.company_detail}")
            exit()