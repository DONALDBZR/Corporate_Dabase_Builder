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
from typing import Dict, Tuple, Union, List
from pdfminer.high_level import extract_text
from datetime import datetime
from json import dumps
from re import findall


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

    def extractData(self, status: int, dataset: DocumentFiles) -> Dict[str, Union[int, Dict[str, Union[str, int]]]]:
        """
        Extracting the data from the portable document file version
        of the corporate registry based on the status of the file
        generation as well as on the dataset.

        Parameters:
            status: int: The status of the file generation.
            dataset: {identifier: int, file_data: bytes, company_detail: int}: The dataset of the corporate registry retrieved from the relational database server.

        Returns:
            {status: int, company_details: {business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}, business_details: {registered_address: string, name: string, nature: string, operational: string}, state_capital: {type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}, office_bearers: {position: string, name: string, address: string, date_appointment: int}, shareholders: {name: string, amount: int, type: string, currency: string}}
        """
        response: Dict[str, Union[int, Dict[str, Union[str, int]]]]
        file_name: str = f"{self.ENV.getDirectory()}Cache/CorporateDocumentFile/Documents/{dataset.company_detail}.pdf"
        cache_data_file_name: str = f"{self.ENV.getDirectory()}Cache/CorporateDocumentFile/Metadata/{dataset.company_detail}.json"
        if status == 201:
            portable_document_file_data: str = extract_text(file_name)
            cache_file = open(cache_data_file_name, "w")
            portable_document_file_data_result_set: List[str] = list(filter(None, portable_document_file_data.split("\n")))
            company_details: Dict[str, Union[str, int]] = self.extractCompanyDetails(portable_document_file_data_result_set)
            business_details: Dict[str, str] = self.extractBusinessDetails(portable_document_file_data_result_set)
            certificate: Union[Dict[str, Union[str, int]], None] = self.extractCertificates(portable_document_file_data_result_set)
            office_bearers: Dict[str, Union[str, int]] = self.extractOfficeBearers(portable_document_file_data_result_set)
            print(f"Result Set: {portable_document_file_data_result_set}\nCompany Details: {company_details}\nBusiness Details: {business_details}\nCertificates: {certificate}\nOffice Bearers: {office_bearers}\n----------")
            exit()
            state_capital: Dict[str, Union[str, int]] = self.extractStateCapital(portable_document_file_data_result_set)
            shareholders: Dict[str, Union[str, int]] = self.extractShareholders(portable_document_file_data_result_set)
            response = {
                "status": 200,
                "company_details": company_details,
                "business_details": business_details, # type: ignore
                "state_capital": state_capital,
                "office_bearers": office_bearers,
                "shareholders": shareholders
            }
            cache_file.write(dumps(response, indent=4))
            cache_file.close()
            self.getLogger().inform(f"Data has been extracted from the portable document file version of the corporate registry.\nStatus: {response['status']}\nDocument File Identifier: {dataset.identifier}\nFile Location: {file_name}\nCompany Details Identifier: {dataset.company_detail}\nCompany Details: {company_details}\nBusiness Details: {business_details}\nShare Capital: {share_capital}\nOffice Bearers: {office_bearers}\nShareholders: {shareholders}")
        else:
            response = {
                "status": 404
            }
            self.getLogger().error(f"The portable document file has not been generated correctly!  The application will abort the extraction.\nStatus: {response['status']}\nFile Location: {file_name}\nDocument File Identifier: {dataset.identifier}\nCompany Detail Identifier: {dataset.company_detail}")
        return response

    def extractCertificates(self, portable_document_file_result_set: List[str]) -> Union[Dict[str, Union[str, int]], None]:
        """
        Extracting the data for the certificates from the result
        set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {certificate: string, type: str, date_effective: int, date_expiry: int}
        """
        start_index: int = portable_document_file_result_set.index("Certificate (Issued by Other Institutions)")
        end_index: int = portable_document_file_result_set.index("Office Bearers")
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        result_set.remove("Certificate (Issued by Other Institutions)")
        result_set.remove("Certificate")
        result_set.remove("Type")
        result_set.remove("Effective Date")
        result_set.remove("Expiry Date")
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractCertificates()")
            exit()
        else:
            return None

    def extractShareholders(self, result_set: List[str]) -> Dict[str, Union[str, int]]:
        """
        Extracting the data for the shareholders from the result
        set.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {name: string, amount: int, type: string, currency: string}
        """
        name: str = result_set[result_set.index("Name") + 9].title()
        amount_shares: int = int(result_set[[index for index, value in enumerate(result_set) if "No. of Shares" in value][1] + 3].split(" ")[0])
        type_shares: str = result_set[[index for index, value in enumerate(result_set) if "Type of Shares" in value][1] + 3].split(" ")[1].title()
        currency: str = result_set[result_set.index("Currency") + 3].title()
        return {
            "name": name,
            "amount_shares": amount_shares,
            "type_shares": type_shares,
            "currency": currency
        }

    def _extractOfficeBearersDateAppointments(self, dataset: List[Tuple[str, str, str]]) -> str:
        """
        Building the date of appointment of an office bearer.

        Parameters:
            dataset: [(string, string, string)]: The dataset containing the date of appointment.

        Returns:
            string
        """
        if len(dataset) > 0:
            return "/".join(list(dataset[0]))
        else:
            return "NaDA"

    def __extractOfficeBearersDateAppointments(self, date_appointments: List[str], date_appointment: str) -> List[str]:
        """
        Setting all of the dates of appointments into the response.

        Parameters:
            date_appointments: [string]: The response to be returned
            date_appointment: string: The date of appointment of the office bearer.

        Returns:
            [string]
        """
        if date_appointment != "NaDA":
            date_appointments.append(date_appointment)
        return date_appointments

    def extractOfficeBearersDateAppointments(self, result_set: List[str]) -> List[str]:
        """
        Retrieving the date of appointments of the office bearers.

        Parameters:
            result_set: [string]: The result set of the office bearers.

        Returns:
            [string]
        """
        response: List[str] = []
        for index in range(0, len(result_set), 1):
            date_appointments: List[Tuple[str, str, str]] = findall(r"\b([0-2][0-9]|3[01])/(0[1-9]|1[0-2])/(\d{4})\b", result_set[index])
            date_appointment: str = self._extractOfficeBearersDateAppointments(date_appointments)
            response = self.__extractOfficeBearersDateAppointments(response, date_appointment)
        return response

    def _extractOfficeBearersPositions(self, dataset: List[str]) -> str:
        """
        Building the position of an office bearer.

        Parameters:
            dataset: [string]: The dataset containing the position.

        Returns:
            string
        """
        if len(dataset) == 1 and dataset[0] != "MAURITIUS" and len(dataset[0]) > 1:
            return dataset[0]
        else:
            return "NaP"

    def __extractOfficeBearersPositions(self, positions: List[str], position: str) -> List[str]:
        """
        Setting all of the positions into the response.

        Parameters:
            positions: [string]: The response to be returned
            position: string: The position of the office bearer.

        Returns:
            [string]
        """
        if position != "NaP":
            positions.append(position)
        return positions

    def extractOfficeBearersPositions(self, result_set: List[str]) -> List[str]:
        """
        Retrieving the positions of the office bearers.

        Parameters:
            result_set: [string]: The result set of the office bearers.

        Returns:
            [string]
        """
        response: List[str] = []
        for index in range(0, len(result_set), 1):
            positions: List[str] = findall(r"\b[A-Z]+\b", result_set[index])
            position: str = self._extractOfficeBearersPositions(positions)
            response = self.__extractOfficeBearersPositions(response, position)
        return response

    def extractOfficeBearersNames(self, result_set: List[str]) -> List[str]:
        """
        Retrieving the names of the office bearers.

        Parameters:
            result_set: [string]: The result set of the office bearers.

        Returns:
            [string]
        """
        response: List[str] = []
        for index in range(0, len(result_set), 1):
            names: List[str] = findall(r"\b[A-Z]+\b", result_set[index])
            name: str = self._extractOfficeBearersNames(names)
            response = self.__extractOfficeBearersNames(response, name)
        return response

    def extractOfficeBearers(self, portable_document_file_result_set: List[str]) -> Dict[str, Union[str, int]]:
        """
        Extracting the data for the office bearers from the result
        set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {position: string, name: string, address: string, date_appointment: int}
        """
        start_index: int = portable_document_file_result_set.index("Office Bearers") + 1
        end_index: int = portable_document_file_result_set.index("Shareholders")
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        result_set.remove("Position")
        result_set.remove("Name")
        result_set.remove("Service Address")
        result_set.remove("Appointed Date")
        date_appointments: List[str] = self.extractOfficeBearersDateAppointments(result_set)
        result_set = [value for value in result_set if value not in date_appointments]
        positions: List[str] = self.extractOfficeBearersPositions(result_set)
        result_set = [value for value in result_set if value not in positions]
        names: List[str] = self.extractOfficeBearersNames(result_set)
        print(f"Result Set: {result_set}\nDate of Appointments: {date_appointments}\nPositions: {positions}")
        exit()
        position: str = result_set[result_set.index("Position") + 1].title()
        name: str = result_set[result_set.index("Name") + 4].title()
        address: str = result_set[result_set.index("Service Address") + 3].title()
        date_appointment: int = int(datetime.strptime(result_set[result_set.index("Appointed Date") + 3], "%d/%m/%Y").timestamp())
        return {
            "position": position,
            "name": name,
            "address": address,
            "date_appointment": date_appointment
        }

    def extractStateCapital(self, portable_document_file_result_set: List[str]) -> Dict[str, Union[str, int]]:
        """
        Extracting the data for the share capital from the result
        set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}
        """
        start_index: int = portable_document_file_result_set.index("Particulars of Stated Capital") + 1
        end_index: int = portable_document_file_result_set.index("Certificate (Issued by Other Institutions)")
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        type: str = " ".join([result_set[result_set.index("Type of Shares") + 4], result_set[result_set.index("Type of Shares") + 5]]).title()
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
            "par_value": par_value
        }

    def extractBusinessDetails(self, portable_document_file_result_set: List[str]) -> Dict[str, str]:
        """
        Extracting the data for the business details from the result
        set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {registered_address: string, name: string, nature: string, operational: string}
        """
        start_index: int = [index for index, value in enumerate(portable_document_file_result_set) if "Registered Office Address:" in value][0]
        end_index: int = portable_document_file_result_set.index("Particulars of Stated Capital")
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        result_set.remove("Business Details")
        result_set.remove("Business Name")
        result_set.remove("Nature of Business")
        result_set.remove("Principal Place of Business")
        registered_address: str = result_set[[index for index, value in enumerate(result_set) if "Registered Office Address:" in value][0]].split(": ")[-1].title()
        name: str = result_set[3]
        nature: str = ' '.join([result_set[3], result_set[4]])
        operational_address: str = ' '.join([result_set[5], result_set[6]]).title()
        return {
            "registered_address": registered_address,
            "name": name,
            "nature": nature,
            "operational_address": operational_address
        }

    def extractCompanyDetails(self, portable_document_file_result_set: List[str]) -> Dict[str, Union[str, int]]:
        """
        Extracting the data for the company details from the result
        set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}
        """
        start_index: int = portable_document_file_result_set.index("Company Details") + 1
        end_index: int = [index for index, value in enumerate(portable_document_file_result_set) if "Business Registration No.:" in value][0] + 1
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        result_set.remove("File No.:")
        result_set.remove("Name:")
        result_set.remove("Type:")
        result_set.remove("Category:")
        result_set.remove("Registrar of Companies")
        result_set.remove("Date Incorporated:")
        result_set.remove("Nature:")
        result_set.remove("Status:")
        result_set.remove("Sub Category:")
        result_set.remove("Business Details")
        business_registration_number: str = result_set[[index for index, value in enumerate(result_set) if "Business Registration No.:" in value][0]].split(" ")[-1]
        name: str = result_set[1]
        file_number: str = result_set[0]
        category: str = result_set[3].title()
        date_incorporation: int = int(datetime.strptime(result_set[4], "%d/%m/%Y").timestamp())
        nature: str = result_set[5]
        status: str = result_set[6]
        return {
            "business_registration_number": business_registration_number,
            "name": name,
            "file_number": file_number,
            "category": category,
            "date_incorporation": date_incorporation,
            "nature": nature,
            "status": status
        }