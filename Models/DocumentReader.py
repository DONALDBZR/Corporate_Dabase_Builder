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
            company_details: Dict[str, Union[str, int]] = self.extractCompanyDetails(portable_document_file_data_result_set)
            business_details: Dict[str, str] = self.extractBusinessDetails(portable_document_file_data_result_set)
            share_capital: Dict[str, Union[str, int]] = self.extractShareCapital(portable_document_file_data_result_set)
            print(f"Dataset: {portable_document_file_data_result_set}\n----------\nCompany Details: {company_details}\nBusiness Details: {business_details}\nShare Capital: {share_capital}")
            exit()
            # Extracting the data from the portable document file.
        else:
            self.getLogger().error(f"The portable document file has not been generated correctly!  The application will abort the extraction.\nStatus: {status}\nFile Location: {file_name}\nDocument File Identifier: {dataset.identifier}\nCompany Detail Identifier: {dataset.company_detail}")
            exit()

    def extractShareCapital(self, result_set: List[str]) -> Dict[str, Union[str, int]]:
        """
        Extracting the data for the share capital from the result
        set.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}
        """
        type: str = " ".join([result_set[result_set.index("Type of Shares") + 4], result_set[result_set.index("Type of Shares") + 5]])
        amount: int = int(result_set[[index for index, value in enumerate(result_set) if "No. of Shares" in value][0] + 5].split(" ")[0])
        currency: str = " ".join([result_set[[index for index, value in enumerate(result_set) if "No. of Shares" in value][0] + 5].split(" ")[1], result_set[[index for index, value in enumerate(result_set) if "No. of Shares" in value][0] + 5].split(" ")[2]])
        stated_capital: int = int(result_set[result_set.index("Stated Capital") + 5].replace(",", ""))
        amount_unpaid: int = int(result_set[[index for index, value in enumerate(result_set) if "Amount Unpaid" in value][0] + 5].split(" ")[0])
        par_value: int = int(result_set[[index for index, value in enumerate(result_set) if "Par Value" in value][0] + 5].split(" ")[1])
        return {
            "type": type,
            "amount": amount,
            "currency": currency,
            "stated_capital": stated_capital,
            "amount_unpaid": amount_unpaid,
            "par_value": par_value,
        }

    def extractBusinessDetails(self, result_set: List[str]) -> Dict[str, str]:
        """
        Extracting the data for the business details from the result
        set.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {registered_address: string, name: string, nature: string, operational: string}
        """
        registered_address: str = result_set[[index for index, value in enumerate(result_set) if "Registered Office Address:" in value][0]].split(": ")[-1]
        name: str = result_set[result_set.index("Business Name") + 3]
        nature: str = ' '.join([result_set[result_set.index("Nature of Business") + 3], result_set[result_set.index("Nature of Business") + 4], result_set[result_set.index("Nature of Business") + 5]])
        operational_address: str = result_set[result_set.index("Principal Place of Business") + 5]
        return {
            "registered_address": registered_address,
            "name": name,
            "nature": nature,
            "operational_address": operational_address
        }

    def extractCompanyDetails(self, result_set: List[str]) -> Dict[str, Union[str, int]]:
        """
        Extracting the data for the company details from the result
        set.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}
        """
        business_registration_number: str = result_set[[index for index, value in enumerate(result_set) if "Business Registration No.:" in value][0]].split(" ")[-1]
        name: str = result_set[result_set.index("Name:") + 2]
        file_number: str = result_set[result_set.index("File No.:") + 1]
        category: str = result_set[result_set.index("Category:") + 1]
        date_incorporation: int = int(datetime.strptime(result_set[result_set.index("Date Incorporated:") + 1], "%d/%m/%Y").timestamp())
        nature: str = result_set[result_set.index("Nature:") + 3]
        status: str = result_set[result_set.index("Status:") + 3]
        return {
            "business_registration_number": business_registration_number,
            "name": name,
            "file_number": file_number,
            "category": category,
            "date_incorporation": date_incorporation,
            "nature": nature,
            "status": status
        }