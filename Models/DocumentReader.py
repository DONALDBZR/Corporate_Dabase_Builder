"""
The module which will have the model needed to generate the
portable document file version of the corporate registry, as
well as extracting the data from it before deleting it from
the cache of the server of the application.

Authors:
    Darkness4869
"""


from Models.Logger import Corporate_Database_Builder_Logger
from Data.DocumentFiles import DocumentFiles
from Data.CompanyDetails import CompanyDetails
from Environment import Environment
from typing import Dict, Tuple, Union, List
from pdfminer.high_level import extract_text
from datetime import date, datetime
from json import dumps
from re import L, findall, search, split
from Models.OfficeBearers import Office_Bearers
from Models.Shareholders import Shareholders
from pdfminer.pdfparser import PDFSyntaxError
from Models.CompanyDetails import Company_Details
from Models.DocumentFiles import Document_Files
from os import remove
from time import time


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
    __office_bearers: Office_Bearers
    """
    The model which will interact exclusively with the Office
    Bearers.
    """
    __shareholders: Shareholders
    """
    The model which will interact exclusively with the
    Shareholders.
    """
    __company_details: Company_Details
    """
    The model which will interact exclusively with the Company
    Details.
    """
    __document_files: Document_Files
    """
    The model which will interact exclusively with the Document
    Files table.
    """

    def __init__(self) -> None:
        """
        Initializing the document reader which will import and
        initialize the dependencies.
        """
        self.ENV = Environment()
        self.setLogger(Corporate_Database_Builder_Logger())
        self.setOfficeBearer(Office_Bearers())
        self.setShareholder(Shareholders())
        self.setCompanyDetails(Company_Details())
        self.setDocumentFiles(Document_Files())
        self.getLogger().inform("The builder has been initialized and all of its dependencies are injected!")

    def getDocumentFiles(self) -> Document_Files:
        return self.__document_files

    def setDocumentFiles(self, document_files: Document_Files) -> None:
        self.__document_files = document_files

    def getCompanyDetails(self) -> Company_Details:
        return self.__company_details

    def setCompanyDetails(self, company_details: Company_Details) -> None:
        self.__company_details = company_details

    def getLogger(self) -> Corporate_Database_Builder_Logger:
        return self.__logger

    def setLogger(self, logger: Corporate_Database_Builder_Logger) -> None:
        self.__logger = logger

    def getOfficeBearer(self) -> Office_Bearers:
        return self.__office_bearers

    def setOfficeBearer(self, office_bearer: Office_Bearers) -> None:
        self.__office_bearers = office_bearer

    def getShareholder(self) -> Shareholders:
        return self.__shareholders

    def setShareholder(self, shareholders: Shareholders) -> None:
        self.__shareholders = shareholders

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

    def extractData(self, status: int, dataset: DocumentFiles, company_detail: CompanyDetails) -> Union[Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]], Dict[str, Union[int, Dict[str, Union[str, int]], Dict[str, str], List[Dict[str, Union[str, int]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]], Dict[str, Union[Dict[str, str], List[Dict[str, int]]]]]], None]:
        """
        Extracting the data from the portable document file version
        of the corporate registry based on the status of the file
        generation as well as on the dataset.

        Parameters:
            status: int: The status of the file generation.
            dataset: {identifier: int, file_data: bytes, company_detail: int}: The dataset of the corporate registry retrieved from the relational database server.
            company_detail: {identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int, is_extracted: int, company_identifier: int, company_type: string}: The data of the Company Details.

        Returns:
            {status: int, company_details: {business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}, business_details: [{registered_address: string, name: string, nature: string, operational: string}], certificates: [{certificate: string, type: str, date_effective: int, date_expiry: int}], office_bearers: [{position: string, name: string, address: string, date_appointment: int}], shareholders: [{name: string, amount: int, type: string, currency: string}], members: [{name: string, amount: int, date_start: int, currency: string}], annual_return: [{date_annual_return: int, date_annual_meeting: int, date_filled: int}], financial_summaries: [{financial_year: int, currency: string, date_approved: int, unit: int}], profit_statement: {financial_summary: {financial_year: int, currency: string, date_approved: int, unit: int}, turnover: float, cost_of_sales: float, gross_profit: float, other_income: float, distribution_cost: float, administration_cost: float, expenses: float, finance_cost: float, net_profit_before_taxation: float, taxation: float, net_profit: float}, state_capital: {type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}, balance_sheet: {balance_sheet: {financial_year: int, currency: string, unit: int}, assets: {non_current_assets: {property_plant_equipment: float, investment_properties: float, intangible_assets: float, other_investments: float, subsidiaries_investments: float, biological_assets: float, others: float, total: float}, current_assets: {inventories: float, trade: float, cash: float, others: float, total: float}, total: float}, liabilities: {equity_and_liabilities: {share_capital: float, other_reserves: float, retained_earnings: float, others: float, total: float}, non_current: {long_term_borrowings: float, deferred_tax: float, long_term_provisions: float, others: float, total: float}, current: {trade: float, short_term_borrowings: float, current_tax_payable: float, short_term_provisions: float, others: float, total: float}, total_liabilities: float, total_equity_and_liabilities: float}}, charges: [{volume: int, property: string, nature: string, amount: int, date_charged: int, date_filled: int, currency: string}], liquidators: {liquidator: {name: string, appointed_date: int, address: string}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}, receivers: {receiver: {name: string, date_appointed: int, address: string}, reports: [{date_filled: int, date_from: int, date_to: int}], affidavits: [{date_filled: int, date_from: int, date_to: int}]}, administrators: {administrator: {name: string, date_appointed: int, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}, details: [{type: string, date_start: int, date_end: int, status: string}], objections: [{date_objection: int, objector: string}]}
        """
        if company_detail.category.upper() == "DOMESTIC":
            return self.extractDataDomestic(status, dataset, company_detail)
        if company_detail.category.upper() == "AUTHORISED COMPANY":
            return self.extractDataAuthorisedCompany(status, dataset)
        if company_detail.category.upper() == "GLOBAL BUSINESS COMPANY":
            return self.extractDataGlobalBusinessCompany(status, dataset)
        if company_detail.category.upper() == "FOREIGN(DOM BRANCH)":
            return self.extractDataForeignDomestic(status, dataset)
        if company_detail.category == None or company_detail.category == "None":
            return None
        self.getLogger().error(f"The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractData()\nCategory: {company_detail.category}")
        exit()

    def extractDataForeignDomestic(self, status: int, dataset: DocumentFiles) -> Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]]:
        """
        Extracting the data from the portable document file version
        of the corporate registry based on the status of the file
        generation as well as on the dataset for a foreign domestic
        company.

        Parameters:
            status: int: The status of the file generation.
            dataset: {identifier: int, file_data: bytes, company_detail: int}: The dataset of the corporate registry retrieved from the relational database server.

        Returns:
            {status: int, company_details: {business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}, business_details: [{name: string, nature: string, operational_address: string}], state_capital: [{type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}], certificates: [{certificate: string, type: str, date_effective: int, date_expiry: int}], office_bearers: [{position: string, name: string, address: string, date_appointment: int}], shareholders: [{name: string, amount: int, type: string, currency: string}], members: [{name: string, amount: int, date_start: int, currency: string}], annual_return: [{date_annual_return: int, date_annual_meeting: int, date_filled: int}], financial_summaries: [{financial_year: int, currency: string, date_approved: int, unit: int}], profit_statement: {financial_summary: {financial_year: int, currency: string, date_approved: int, unit: int}, turnover: float, cost_of_sales: float, gross_profit: float, other_income: float, distribution_cost: float, administration_cost: float, expenses: float, finance_cost: float, net_profit_before_taxation: float, taxation: float, net_profit: float}, balance_sheet: {balance_sheet: {financial_year: int, currency: string, unit: int}, assets: {non_current_assets: {property_plant_equipment: float, investment_properties: float, intangible_assets: float, other_investments: float, subsidiaries_investments: float, biological_assets: float, others: float, total: float}, current_assets: {inventories: float, trade: float, cash: float, others: float, total: float}, total: float}, liabilities: {equity_and_liabilities: {share_capital: float, other_reserves: float, retained_earnings: float, others: float, total: float}, non_current: {long_term_borrowings: float, deferred_tax: float, long_term_provisions: float, others: float, total: float}, current: {trade: float, short_term_borrowings: float, current_tax_payable: float, short_term_provisions: float, others: float, total: float}, total_liabilities: float, total_equity_and_liabilities: float}}, charges: [{volume: int, property: string, nature: string, amount: int, date_charged: int, date_filled: int, currency: string}], liquidators: {liquidator: {name: string, appointed_date: int, address: string}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}, receivers: {receiver: {name: string, date_appointed: int, address: string}, reports: [{date_filled: int, date_from: int, date_to: int}], affidavits: [{date_filled: int, date_from: int, date_to: int}]}, administrators: {administrator: {name: string, date_appointed: int, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}, details: [{type: string, date_start: int, date_end: int, status: string}], objections: [{date_objection: int, objector: string}]}
        """
        response: Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]]
        file_name: str = f"{self.ENV.getDirectory()}Cache/CorporateDocumentFile/Documents/{dataset.company_detail}.pdf"
        cache_data_file_name: str = f"{self.ENV.getDirectory()}Cache/CorporateDocumentFile/Metadata/{dataset.company_detail}.json"
        if status != 201:
            self.getLogger().error(f"The portable document file has not been generated correctly!  The application will abort the extraction.\nStatus: {status}\nFile Location: {file_name}\nDocument File Identifier: {dataset.identifier}\nCompany Detail Identifier: {dataset.company_detail}")
            return {
                "status": 404
            }
        try:
            portable_document_file_data: str = extract_text(file_name)
            cache_file = open(cache_data_file_name, "w")
            portable_document_file_data_result_set: List[str] = list(filter(None, portable_document_file_data.split("\n")))
            company_details: Dict[str, Union[str, int]] = self.extractCompanyDetails(portable_document_file_data_result_set)
            business_details: List[Dict[str, str]] = self.extractDataForeignDomesticBusinessDetails(portable_document_file_data_result_set)
            state_capital: List[Dict[str, Union[str, int, float]]] = self.extractStateCapital(portable_document_file_data_result_set)
            certificates: List[Dict[str, Union[str, int]]] = self.extractCertificates(portable_document_file_data_result_set)
            office_bearers: List[Dict[str, Union[str, int]]] = self.extractDataForeignDomesticOfficeBearers(portable_document_file_data_result_set)
            shareholders: List[Dict[str, Union[str, int]]] = self.extractShareholders(portable_document_file_data_result_set)
            members: List[Dict[str, Union[str, int]]] = self.extractMembers(portable_document_file_data_result_set)
            annual_return: List[Dict[str, int]] = self.extractAnnualReturns(portable_document_file_data_result_set)
            financial_summaries: List[Dict[str, Union[int, str]]] = self.extractFinancialSummaries(portable_document_file_data_result_set)
            profit_statement: Dict[str, Union[Dict[str, Union[int, str]], float]] = self.extractProfitStatements(portable_document_file_data_result_set)
            balance_sheet: Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]] = self.extractBalanceSheet(portable_document_file_data_result_set)
            charges: List[Dict[str, Union[int, str]]] = self.extractCharges(portable_document_file_data_result_set)
            liquidators: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]] = self.extractLiquidators(portable_document_file_data_result_set)
            receivers: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]] = self.extractReceivers(portable_document_file_data_result_set)
            administrators: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]] = self.extractAdministrators(portable_document_file_data_result_set)
            details: List[Dict[str, Union[str, int, None]]] = self.extractDetails(portable_document_file_data_result_set)
            objections: List[Dict[str, Union[int, str]]] = self.extractObjections(portable_document_file_data_result_set)
            response = {
                "status": 200,
                "company_details": company_details,
                "business_details": business_details,
                "certificates": certificates,
                "office_bearers": office_bearers,
                "shareholders": shareholders,
                "members": members,
                "annual_return": annual_return,
                "financial_summaries": financial_summaries,
                "profit_statement": profit_statement,
                "state_capital": state_capital, # type: ignore
                "balance_sheet": balance_sheet,
                "charges": charges,
                "liquidators": liquidators,
                "receivers": receivers,
                "administrators": administrators,
                "details": details,
                "objections": objections
            }
            cache_file.write(dumps(response, indent=4))
            cache_file.close()
            self.getLogger().inform(f"Data has been extracted from the portable document file version of the corporate registry.\nStatus: {response['status']}\nDocument File Identifier: {dataset.identifier}\nFile Location: {file_name}\nCompany Details Identifier: {dataset.company_detail}")
            return response
        except PDFSyntaxError as error:
            status = self.getCompanyDetails().invalidateCompany(dataset.company_detail)
            status = self.getDocumentFiles().deleteDocumentFile(dataset.company_detail) if status == 202 else status
            remove(file_name) if status == 204 else None
            status = 403 if status == 204 else status
            self.getLogger().error(f"Data cannot be extracted due to an error in the file type.\nStatus: {status}\nDocument File Identifier: {dataset.identifier}\nFile Location: {file_name}\nCompany Details Identifier: {dataset.company_detail}\nError: {error}")
            return {
                "status": status
            }

    def extractDataForeignDomesticOfficeBearers(self, result_set: List[str]) -> List[Dict[str, Union[str, int]]]:
        """
        Extracting the data for the office bearers of a foreign
        domestic company from the corporate registry.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{position: string, name: string, address: string, date_appointment: int}]
        """
        response: List[Dict[str, Union[str, int]]] = []
        start_index: int = result_set.index("Office Bearers") + 1
        end_index: int = result_set.index("Shareholders")
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if "Position" not in value]
        result_set = [value for value in result_set if "Name" not in value]
        result_set = [value for value in result_set if "Service Address" not in value]
        result_set = [value for value in result_set if "Appointed Date" not in value]
        result_set = [value for value in result_set if "Shareholders" not in value]
        date_appointments: List[str] = self.extractOfficeBearersDateAppointments(result_set)
        result_set = [value for value in result_set if value not in date_appointments]
        positions: List[str] = self.extractDataForeignDomesticOfficeBearersPositions(result_set)
        result_set = [value for value in result_set if value not in positions]
        names: List[str] = self.extractOfficeBearersNames(result_set)
        result_set = [value for value in result_set if value not in names]
        addresses: List[str] = self.extractDataForeignDomesticOfficeBearersAddresses(result_set)
        if len(addresses) > 0:
            response = self._extractDataForeignDomesticOfficeBearersWithAddress(date_appointments, positions, names, addresses)
        else:
            response = self._extractDataForeignDomesticOfficeBearersWithoutAddress(date_appointments, positions, names)
        return response

    def _extractDataForeignDomesticOfficeBearersWithAddress(self, date_appointments: List[str], positions: List[str], names: List[str], addresses: List[str]) -> List[Dict[str, Union[str, int]]]:
        """
        Building the response needed for the data about the office
        bearers of a foreign domestic company when there are
        addresses.

        Parameters:
            date_appointments: [string]: The date at which the office bearer was appointed.
            positions: [string]: The position of the office bearer.
            names: [string]: The name of the office bearer.
            addresses: [string]: The service address of the office bearer.

        Returns:
            [{position: string, name: string, address: string, date_appointment: int}]
        """
        response: List[Dict[str, Union[str, int]]] = []
        limitation: int = min([len(date_appointments), len(positions), len(names), len(addresses)])
        for index in range(0, limitation, 1):
            response.append({
                "position": positions[index].title(),
                "name": names[index].title(),
                "address": addresses[index].title(),
                "date_appointment": int(datetime.strptime(date_appointments[index], "%d/%m/%Y").timestamp())
            })
        return response

    def _extractDataForeignDomesticOfficeBearersWithoutAddress(self, date_appointments: List[str], positions: List[str], names: List[str]) -> List[Dict[str, Union[str, int]]]:
        """
        Building the response needed for the data about the office
        bearers of a foreign domestic company when there are no
        addresses.

        Parameters:
            date_appointments: [string]: The date at which the office bearer was appointed.
            positions: [string]: The position of the office bearer.
            names: [string]: The name of the office bearer.

        Returns:
            [{position: string, name: string, date_appointment: int}]
        """
        response: List[Dict[str, Union[str, int]]] = []
        limitation: int = min([len(date_appointments), len(positions), len(names)])
        for index in range(0, limitation, 1):
            response.append({
                "position": positions[index].title(),
                "name": names[index].title(),
                "date_appointment": int(datetime.strptime(date_appointments[index], "%d/%m/%Y").timestamp())
            })
        return response

    def extractDataForeignDomesticOfficeBearersAddresses(self, result_set: List[str]) -> List[str]:
        """
        Extracting the addresses of the office bearers of a foreign
        domestic company.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [string]
        """
        response: List[str] = [value for value in result_set if "Court" in value.title() or "Street" in value.title() or "Mauritius".upper() in value or "Rodrigues".upper() in value]
        return response

    def extractDataForeignDomesticOfficeBearersPositions(self, result_set: List[str]) -> List[str]:
        """
        Extracting the positions of the office bearers of a foreign
        domestic company.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [string]
        """
        possible_positions: List[str] = list(set(self.getOfficeBearer().getPossiblePositions() + ["AUTHORISED AGENT"]))
        response: List[str] = [value for value in result_set if value in possible_positions]
        return response

    def extractDataForeignDomesticBusinessDetails(self, result_set: List[str]) -> List[Dict[str, str]]:
        """
        Extracting the data for the business details of a foreign
        domestic company from the corporate registry.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{name: string, nature: string, operational: string}]
        """
        response: List[Dict[str, str]] = []
        start_index: int = result_set.index("Business Details")
        end_index: int = result_set.index("Particulars of Stated Capital")
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if "Business Details" not in value]
        result_set = [value for value in result_set if "Business Registration No" not in value]
        result_set = [value for value in result_set if "Business Name" not in value]
        result_set = [value for value in result_set if "Nature of Business" not in value]
        result_set = [value for value in result_set if "Principal Place of Business" not in value]
        result_set = [value for value in result_set if "Particulars of Stated Capital" not in value]
        result_set = [value for value in result_set if ":" not in value]
        result_set = [value for value in result_set if "/" not in value]
        result_set = [value for value in result_set if "Private" not in value]
        result_set = [value for value in result_set if "Live" not in value]
        dataset: List[str] = [value for value in result_set if "Court" in value.title() or "Street" in value.title() or "Mauritius".upper() in value or "Rodrigues".upper() in value]
        operational_addresses: List[str] = self.extractBusinessDetailsOperationalAddresses(result_set)
        result_set = [value for value in result_set if value not in dataset]
        dataset = [value for value in result_set if bool(search(r"[A-Z]+", value)) == True and bool(search(r"[a-z]+", value)) == True and "/" in value]
        natures: List[str] = self.extractBusinessDetailsNatures(result_set)
        names: List[str] = [value for value in result_set if value not in dataset]
        limitation: int = min([len(names), len(natures), len(operational_addresses)])
        for index in range(0, limitation, 1):
            response.append({
                "name": names[index].title(),
                "nature": natures[index].title(),
                "operational_address": operational_addresses[index].title()
            })
        return response

    def extractDataGlobalBusinessCompany(self, status: int, dataset: DocumentFiles) -> Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]]:
        """
        Extracting the data from the portable document file version
        of the corporate registry based on the status of the file
        generation as well as on the dataset for a global business
        company.

        Parameters:
            status: int: The status of the file generation.
            dataset: {identifier: int, file_data: bytes, company_detail: int}: The dataset of the corporate registry retrieved from the relational database server.

        Returns:
            {status: int, company_details: {file_number: string, name: string, category: string, date_incorporation: int, nature: string, status: string}, business_details: {registered_address: string}, office_bearers: [{position: string, name: string, address: string, date_appointment: int}], receivers:  {receiver: {name: string, date_appointed: int, address: string}, reports: [{date_filled: int, date_from: int, date_to: int}], affidavits: [{date_filled: int, date_from: int, date_to: int}]}, administrators: {administrator: {name: string, designation: string, address: string, date_appointed: int}, accounts: [{date_filled: int, date_from: int, date_to: int}]}, liquidators: {liquidator: {name: string, designation: string, address: string, date_appointed: int}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}}
        """
        response: Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]]
        file_name: str = f"{self.ENV.getDirectory()}Cache/CorporateDocumentFile/Documents/{dataset.company_detail}.pdf"
        cache_data_file_name: str = f"{self.ENV.getDirectory()}Cache/CorporateDocumentFile/Metadata/{dataset.company_detail}.json"
        if status != 201:
            self.getLogger().error(f"The portable document file has not been generated correctly!  The application will abort the extraction.\nStatus: {status}\nFile Location: {file_name}\nDocument File Identifier: {dataset.identifier}\nCompany Detail Identifier: {dataset.company_detail}")
            return {
                "status": 404
            }
        try:
            portable_document_file_data: str = extract_text(file_name)
            cache_file = open(cache_data_file_name, "w")
            portable_document_file_data_result_set: List[str] = list(filter(None, portable_document_file_data.split("\n")))
            company_details: Dict[str, Union[str, int]] = self.extractDataGlobalBusinessCompanyCompanyDetails(portable_document_file_data_result_set)
            business_details: Dict[str, str] = self.extractDataGlobalBusinessCompanyBusinessDetails(portable_document_file_data_result_set)
            state_capital: List[Dict[str, Union[str, int, float]]] = self.extractDataGlobalBusinessCompanyStatedCapital(portable_document_file_data_result_set)
            office_bearers: List[Dict[str, Union[str, int]]] = self.extractDataGlobalBusinessCompanyOfficeBearers(portable_document_file_data_result_set)
            receivers: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]] = self.extractDataGlobalBusinessCompanyReceivers(portable_document_file_data_result_set)
            administrators: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]] = self.extractDataGlobalBusinessCompanyAdministrators(portable_document_file_data_result_set)
            liquidators: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]] = self.extractDataGlobalBusinessCompanyLiquidators(portable_document_file_data_result_set)
            response = {
                "status": 200,
                "company_details": company_details,
                "business_details": business_details, # type: ignore
                "state_capital": state_capital,
                "office_bearers": office_bearers,
                "receivers": receivers,
                "administrators": administrators,
                "liquidators": liquidators
            }
            cache_file.write(dumps(response, indent=4))
            cache_file.close()
            self.getLogger().inform(f"Data has been extracted from the portable document file version of the corporate registry.\nStatus: {response['status']}\nDocument File Identifier: {dataset.identifier}\nFile Location: {file_name}\nCompany Details Identifier: {dataset.company_detail}")
            return response
        except PDFSyntaxError as error:
            status = self.getCompanyDetails().invalidateCompany(dataset.company_detail)
            status = self.getDocumentFiles().deleteDocumentFile(dataset.company_detail) if status == 202 else status
            remove(file_name) if status == 204 else None
            status = 403 if status == 204 else status
            self.getLogger().error(f"Data cannot be extracted due to an error in the file type.\nStatus: {status}\nDocument File Identifier: {dataset.identifier}\nFile Location: {file_name}\nCompany Details Identifier: {dataset.company_detail}\nError: {error}")
            return {
                "status": status
            }

    def extractDataGlobalBusinessCompanyStatedCapital(self, result_set: List[str]) -> List[Dict[str, Union[str, int, float]]]:
        """
        Extracting the stated capital of a global business company.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{type: string, amount: int, currency: string, state_capital: int, amount_unpaid: float}]
        """
        response: List[Dict[str, Union[str, int, float]]] = []
        if "Particulars of Stated Capital" in result_set:
            start_index: int = result_set.index("Particulars of Stated Capital")
            end_index: int = result_set.index("Certificate (Issued by Other Institutions)")
            result_set = result_set[start_index:end_index]
            result_set = [value for value in result_set if "Particulars of Stated Capital" not in value]
            result_set = [value for value in result_set if "Type of Shares" not in value]
            result_set = [value for value in result_set if "No. of Shares Currency" not in value]
            result_set = [value for value in result_set if "Stated Capital" not in value]
            result_set = [value for value in result_set if "Amount Unpaid Par Value" not in value]
            dataset: List[str] = [value for value in result_set if bool(search(r"[A-Z]+", value)) == True and bool(search(r"[a-z]+", value)) == False]
            types: List[str] = self.extractDataGlobalBusinessCompanyStatedCapitalTypes(result_set)
            result_set = [value for value in result_set if value not in dataset]
            dataset = [value for value in result_set if bool(search(r"[\d]+", value)) == True and bool(search(r"[A-z]+", value)) == True]
            amounts: List[int] = self.extractDataGlobalBusinessCompanyStatedCapitalAmounts(result_set)
            currencies: List[str] = self.extractDataGlobalBusinessCompanyStatedCapitalCurrencies(result_set)
            result_set = [value for value in result_set if value not in dataset]
            dataset = [value for value in result_set if bool(search(r"[\d]+", value)) == True and " " not in value]
            stated_capital: List[float] = self.extractDataGlobalBusinessCompanyStatedCapitalStatedCapital(result_set)
            result_set = [value for value in result_set if value not in dataset]
            amount_unpaid: List[float] = self.extractDataGlobalBusinessCompanyStatedCapitalAmountUnpaid(result_set)
            response = self._extractDataGlobalBusinessCompanyStatedCapital(types, amounts, currencies, stated_capital, amount_unpaid)
        else:
            response = []
        return response

    def _extractDataGlobalBusinessCompanyStatedCapital(self, types: List[str], amounts: List[int], currencies: List[str], stated_capitals: List[float], amount_unpaids: List[float]) -> List[Dict[str, Union[str, int, float]]]:
        """
        Building the response for the stated capital of a global
        business company.

        Parameters:
            types: [string]: The types of the stated capital.
            amounts: [int]: The amounts of shares of the stated capital.
            currencies: [string]: The currencies of the stated capital.
            stated_capitals: [float]: The capitals that have been stated.
            amount_unpaids: [float]: The amount unpaids of the stated capital.

        Returns:
            [{type: string, amount: int, currency: string, state_capital: int, amount_unpaid: float}]
        """
        limitation: int = min([len(types), len(amounts), len(currencies), len(stated_capitals), len(amount_unpaids)])
        response: List[Dict[str, Union[str, int, float]]] = []
        for index in range(0, limitation, 1):
            response.append({
                "type": types[index],
                "amount": amounts[index],
                "currency": currencies[index],
                "stated_capital": stated_capitals[index],
                "amount_unpaid": amount_unpaids[index]
            })
        return response

    def extractDataGlobalBusinessCompanyStatedCapitalAmountUnpaid(self, result_set: List[str]) -> List[float]:
        """
        Extracting the amount unpaid of the stated capital of a
        global business company.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [float]
        """
        response: List[float] = []
        for index in range(0, len(result_set), 1):
            response.append(float(result_set[index].split(" ")[0]))
        return response

    def extractDataGlobalBusinessCompanyStatedCapitalStatedCapital(self, result_set: List[str]) -> List[float]:
        """
        Extracting the stated capital of the stated capital of a
        global business company.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [float]
        """
        dataset: List[str] = [value for value in result_set if bool(search(r"[\d]+", value)) == True and " " not in value]
        dataset = ["".join(value.split(",")) for value in dataset if "," in value]
        response: List[float] = [float(value) for value in dataset]
        return response

    def extractDataGlobalBusinessCompanyStatedCapitalCurrencies(self, result_set: List[str]) -> List[str]:
        """
        Extracting the currencies of the stated capital of a global
        business company.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [string]
        """
        response: List[str] = []
        dataset: List[str] = [value for value in result_set if bool(search(r"[\d]+", value)) == True and bool(search(r"[A-z]+", value)) == True]
        for index in range(0, len(dataset), 1):
            response.append(" ".join([value for value in dataset[index].split(" ") if bool(search(r"[A-z]+", value)) == True]))
        return response

    def extractDataGlobalBusinessCompanyStatedCapitalAmounts(self, result_set: List[str]) -> List[int]:
        """
        Extracting the amounts of shares of the stated capital of a
        global business company.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [int]
        """
        response: List[int] = []
        dataset: List[str] = [value for value in result_set if bool(search(r"[\d]+", value)) == True and bool(search(r"[A-z]+", value)) == True]
        for index in range(0, len(dataset), 1):
            response.append(int("".join([value for value in dataset[index].split(" ") if bool(search(r"[\d]+", value)) == True])))
        return response

    def extractDataGlobalBusinessCompanyStatedCapitalTypes(self, result_set: List[str]) -> List[str]:
        """
        Extracting the types of the stated capital of a global
        business company.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [string]
        """
        response: List[str] = []
        dataset: List[str] = [value for value in result_set if bool(search(r"[A-Z]+", value)) == True and bool(search(r"[a-z]+", value)) == False and "SHARES" not in value]
        for index in range(0, len(dataset), 1):
            response.append(f"{dataset[index].title()} Shares")
        return response

    def extractDataGlobalBusinessCompanyLiquidators(self, result_set: List[str]) -> Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]:
        """
        Extracting the liquidator of a global business company from
        the corporate registry.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {liquidator: {name: string, designation: string, address: string, date_appointed: int}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}
        """
        start_header: str = "Liquidators"
        response: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]] = {}
        if start_header not in result_set:
            return response
        start_index: int = result_set.index(start_header)
        result_set = result_set[start_index:]
        start_header = "Appointed Date:"
        start_index = result_set.index(start_header) if start_header in result_set else next((index for index, value in enumerate(result_set) if value.startswith(start_header)), -1)
        end_index: int = start_index + 4
        date_appointeds: List[str] = [value for value in result_set[start_index:end_index] if ":" in value or "/" in value]
        start_index = int(len(date_appointeds) / 2)
        date_appointeds = date_appointeds[start_index:]
        liquidator: Dict[str, Union[str, int]] = self._extractDataGlobalBusinessCompanyLiquidators(result_set, date_appointeds)
        affidavits: List[Dict[str, int]] = self.extractDataGlobalBusinessCompanyLiquidatorsAffidavits(result_set)
        if not liquidator and len(affidavits) == 0:
            return response
        self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractDataGlobalBusinessCompanyLiquidators()")
        exit()

    def extractDataGlobalBusinessCompanyLiquidatorsAffidavits(self, result_set: List[str]) -> List[Dict[str, int]]:
        """
        Extracting the affidavits of the liquidator of a global
        business company from the corporate registry.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{date_filled: int, date_from: int, date_to: int}]
        """
        response: List[Dict[str, int]] = []
        start_index: int = result_set.index("Affidavits of Liquidator") + 1
        end_index: int = result_set.index("Receivers") if "Receivers" in result_set else result_set.index("This is a Computer Generated Document.")
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if "Appointed Date:" not in value]
        result_set = [value for value in result_set if "Date Filed" not in value]
        result_set = [value for value in result_set if "From" not in value]
        result_set = [value for value in result_set if "To" not in value]
        if len(result_set) < 3:
            return response
        self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractDataGlobalBusinessCompanyLiquidatorsAffidavits()")
        exit()
        return response

    def _extractDataGlobalBusinessCompanyLiquidators(self, result_set: List[str], date_appointed: List[str]) -> Dict[str, Union[str, int]]:
        """
        Extracting the liquidator of the liquidator of a global
        business company from the corporate registry.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {name: string, designation: string, address: string, date_appointed: int}
        """
        response: Dict[str, Union[str, int]] = {}
        start_header: str = "Liquidators"
        end_header: str = "Affidavits of Liquidator"
        start_index: int = result_set.index(start_header)
        end_index: int = result_set.index(end_header)
        result_set = [value for value in result_set[start_index:end_index] + date_appointed if ":" not in value]
        result_set = [value for value in result_set if start_header not in value]
        if len(result_set) < 3:
            return response
        self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader._extractDataGlobalBusinessCompanyLiquidators()")
        exit()

    def extractDataGlobalBusinessCompanyAdministrators(self, result_set: List[str]) -> Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]:
        """
        Extracting the administrators of a global business company
        from the corporate registry.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {administrator: {name: string, designation: string, address: string, date_appointed: int}, accounts: [{date_filled: int, date_from: int, date_to: int}]}
        """
        response: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]] = {}
        if "Administrators" not in result_set:
            return response
        start_index: int = result_set.index("Administrators")
        date_appointeds: List[str] = result_set[start_index:]
        start_index = date_appointeds.index("Appointed Date:")
        end_index: int = start_index + 6
        date_appointeds = [value for value in date_appointeds[start_index:end_index] if "Appointed Date:" in value or "/" in value]
        start_index = int(len(date_appointeds) * (2 / 3)) - 1
        end_index = start_index + 2 - 1
        date_appointeds = date_appointeds[start_index:end_index]
        start_index = result_set.index("Administrators")
        end_index = result_set.index("Accounts of Administrator")
        dataset: List[str] = result_set[start_index:end_index] + date_appointeds
        dataset = [value for value in dataset if "Administrators" not in value]
        dataset = [value for value in dataset if "To" not in value]
        administrator: Dict[str, Union[str, int]] = self._extractDataGlobalBusinessCompanyAdministrators(dataset)
        start_index = result_set.index("Accounts of Administrator")
        end_index = result_set.index("Liquidators")
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if "Accounts of Administrator" not in value]
        accounts: List[Dict[str, int]] = self.extractDataGlobalBusinessCompanyAdministratorsAccounts(result_set)
        if (not administrator and len(accounts) == 0) or (not administrator and len(accounts) > 0):
            return response
        self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractDataGlobalBusinessCompanyAdministrators()")
        exit()

    def extractDataGlobalBusinessCompanyAdministratorsAccounts(self, result_set: List[str]) -> List[Dict[str, int]]:
        """
        Extracting the accounts of the administrators of a global
        business company from the corporate registry.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{date_filled: int, date_from: int, date_to: int}]
        """
        set_amount: int = 3
        response: List[Dict[str, int]] = []
        result_set = [value for value in result_set if "/" in value]
        result_set = [value for value in result_set if bool(search(r"[A-z]+", value)) == False]
        if len(result_set) < 3:
            return response
        dates: List[List[str]] = [result_set[index:index+set_amount] for index in range(0, len(result_set), 3)]
        for index in range(0, len(dates), 1):
            if len(dates[index]) == 3:
                response.append({
                    "date_filled": int(datetime.strptime(dates[index][0], "%d/%m/%Y").timestamp()),
                    "date_from": int(datetime.strptime(dates[index][1], "%d/%m/%Y").timestamp()),
                    "date_to": int(datetime.strptime(dates[index][2], "%d/%m/%Y").timestamp())
                })
        return response

    def _extractDataGlobalBusinessCompanyAdministrators(self, result_set: List[str]) -> Dict[str, Union[str, int]]:
        """
        Extracting the administrator of the administrators of a
        global business company from the corporate registry.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {name: string, designation: string, address: string, date_appointed: int}
        """
        response: Dict[str, Union[str, int]]
        result_set = [value for value in result_set if ":" not in value]
        result_set = [value for value in result_set if "Page" not in value]
        result_set = [value for value in result_set if " of " not in value]
        result_set = [value for value in result_set if "Appointed Date" not in value]
        validateds: List[str] = [value for value in result_set if "/" not in value]
        if len(validateds) == 0:
            return {}
        self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader._extractDataGlobalBusinessCompanyAdministrators()")
        exit()
        return response

    def extractDataGlobalBusinessCompanyReceivers(self, result_set: List[str]) -> Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]:
        """
        Extracting the receivers of a global business company from
        the corporate registry.

        Parameters:
            result_set: [string]: The data of the corporate registry.

        Returns:
            {receiver: {name: string, date_appointed: int, address: string}, reports: [{date_filled: int, date_from: int, date_to: int}], affidavits: [{date_filled: int, date_from: int, date_to: int}]}
        """
        response: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]] = {}
        if "Receivers" not in result_set:
            return response
        start_index: int = result_set.index("Receivers")
        date_appointeds: List[str] = result_set[start_index:]
        start_index = date_appointeds.index("Appointed Date:")
        end_index: int = start_index + 2
        date_appointeds = [value for value in date_appointeds[start_index:end_index] if "Page" not in value]
        start_index = result_set.index("Receivers")
        date_tos: List[str] = result_set[start_index:]
        start_index = date_tos.index("To")
        end_index = start_index + 4
        date_tos = [value for value in date_tos[start_index:end_index] if ":" not in value and "Page" not in value]
        start_index = result_set.index("Receivers")
        end_index = result_set.index("Administrators")
        result_set = result_set[start_index:end_index]
        receiver: Dict[str, Union[str, int]] = self._extractDataGlobalBusinessCompanyReceivers(result_set, date_appointeds)
        reports: List[Dict[str, int]] = self.extractDataGlobalBusinessCompanyReceiversReports(result_set, date_tos)
        affidavits: List[Dict[str, int]] = self.extractDataGlobalBusinessCompanyReceiversAffidavits(result_set, date_tos)
        if not receiver and len(reports) == 0 and len(affidavits) == 0:
            return response
        self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractDataGlobalBusinessCompanyReceivers()")
        exit()

    def extractDataGlobalBusinessCompanyReceiversAffidavits(self, result_set: List[str], date_tos: List[str]) -> List[Dict[str, int]]:
        """
        Extracting the affidavits of the receivers of a global
        business company from the corporate registry.

        Parameters:
            result_set: [string]: The data of the corporate registry.
            date_tos: [string]: The data about the date to for the reports.


        Returns:
            [{date_filled: int, date_from: int, date_to: int}]
        """
        response: List[Dict[str, int]]
        start_index: int = int(len(date_tos) / 2)
        date_tos = date_tos[start_index:]
        date_tos = [value for value in date_tos if "Appointed Date" not in value]
        start_index = result_set.index("Affidavits of Receiver") + 1
        result_set = result_set[start_index:] + date_tos
        result_set = [value for value in result_set if "Date Filed" not in value and "From" not in value and "To" not in value]
        if len(result_set) < 3:
            return []
        self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractDataGlobalBusinessCompanyReceiversAffidavits()")
        response = []
        return response

    def extractDataGlobalBusinessCompanyReceiversReports(self, result_set: List[str], date_tos: List[str]) -> List[Dict[str, int]]:
        """
        Extracting the reports of the receivers of a global business
        company from the corporate registry.

        Parameters:
            result_set: [string]: The data of the corporate registry.
            date_tos: [string]: The data about the date to for the reports.

        Returns:
            [{date_filled: int, date_from: int, date_to: int}]
        """
        response: List[Dict[str, int]]
        end_index: int = int(len(date_tos) / 2)
        date_tos = date_tos[:end_index]
        start_index: int = result_set.index("Reports of Receiver") + 1
        end_index = result_set.index("Affidavits of Receiver")
        result_set = result_set[start_index:end_index] + date_tos
        result_set = [value for value in result_set if "Date Filed" not in value and "From" not in value and "To" not in value]
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractDataGlobalBusinessCompanyReceiversReports()")
            exit()
        else:
            response = []
        return response

    def _extractDataGlobalBusinessCompanyReceivers(self, result_set: List[str], date_appointeds: List[str]) -> Dict[str, Union[str, int]]:
        """
        Extracting the receiver of the receivers of a global
        business company from the corporate registry.

        Parameters:
            result_set: [string]: The data of the corporate registry.
            date_appointeds: [string]: The data about the date of appointments of the receiver.

        Returns:
            {name: string, date_appointed: int, address: string}
        """
        response: Dict[str, Union[str, int]]
        start_index: int = result_set.index("Name:")
        end_index: int = result_set.index("Reports of Receiver")
        result_set = [value for value in result_set[start_index:end_index] + date_appointeds if ":" not in value]
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader._extractDataGlobalBusinessCompanyReceivers()")
            response = {}
        else:
            response = {}
        return response

    def extractDataGlobalBusinessCompanyOfficeBearers(self, result_set: List[str]) -> List[Dict[str, Union[str, int]]]:
        """
        Extracting the office bearers of a global business company
        from the corporate registry.

        Parameters:
            result_set: [string]: The data of the corporate registry.

        Returns:
            [{position: string, name: string, address: string, date_appointment: int}]
        """
        response: List[Dict[str, Union[str, int]]] = []
        names: List[str]
        possible_positions: List[str] = self.getOfficeBearer().getPossiblePositions()
        start_index: int = result_set.index("Office Bearers") + 1
        end_index: int = result_set.index("Liquidators") if "Liquidators" in result_set else len(result_set)
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if "Position" not in value]
        result_set = [value for value in result_set if "Name" not in value]
        result_set = [value for value in result_set if "Service Address" not in value]
        result_set = [value for value in result_set if "Appointed Date" not in value]
        result_set = [value for value in result_set if "Receivers" not in value]
        result_set = [value for value in result_set if ":" not in value]
        result_set = [value for value in result_set if "Reports of Receiver" not in value]
        result_set = [value for value in result_set if "Date Filed" not in value]
        result_set = [value for value in result_set if "From" not in value]
        result_set = [value for value in result_set if "Affidavits of Receiver" not in value]
        result_set = [value for value in result_set if "Administrators" not in value]
        result_set = [value for value in result_set if value != "To"]
        result_set = [value for value in result_set if "Page" not in value]
        result_set = [value for value in result_set if " of " not in value]
        result_set = [value for value in result_set if "Accounts of Administrator" not in value]
        result_set = [value for value in result_set if "Date Filed" not in value]
        result_set = [value for value in result_set if "This is a Computer Generated Document." not in value]
        result_set = [value for value in result_set if "DISCLAIMER NOTICE" not in value]
        result_set = [value for value in result_set if "While we endeavour to keep the information up to date and as far as possible accurate, we cannot give any guarantee about the completeness, accuracy," not in value]
        result_set = [value for value in result_set if "\x0c" not in value]
        date_appointments: List[str] = [value for value in result_set if "/" in value and bool(search(r"[\d]+", value)) == True and bool(search(r"[A-Z]+", value)) == False]
        result_set = [value for value in result_set if value not in date_appointments]
        positions: List[str] = [value for value in result_set if  value in possible_positions]
        result_set = [value for value in result_set if value not in positions]
        dataset: List[str] = [value for value in result_set if bool(search(r"[\w]+", value)) == True and ("Street".upper() in value.upper() or "Court".upper() in value.upper() or "Avenue".upper() in value.upper() or "Tower".upper() in value.upper() or "Floor".upper() in value.upper())]
        addresses: List[str] = self.extractDataGlobalBusinessCompanyOfficeBearersAddress(result_set)
        result_set = [value for value in result_set if value not in dataset]
        names = [value for value in result_set if bool(search(r"[A-Z]+", value)) == True and "Mauritius".upper() not in value]
        names = [value for value in names if "MANAGEMENT" not in value]
        names = [value for value in names if "COMPANY" not in value]
        result_set = [value for value in result_set if value not in names]
        result_set = [value for value in result_set if "MANAGEMENT" not in value]
        result_set = [value for value in result_set if "COMPANY" not in value]
        if len(result_set) > 0:
            dataset = [value.replace("Mauritius".upper(), "") for value in addresses]
            addresses = [value_address + value_result_set for value_address, value_result_set in zip(dataset, result_set)]
        limit: int = min([len(date_appointments), len(positions), len(addresses), len(names)])
        for index in range(0, limit, 1):
            response.append({
                "position": positions[index].title(),
                "name": names[index].title(),
                "address": addresses[index].title(),
                "date_appointment": int(datetime.strptime(date_appointments[index], "%d/%m/%Y").timestamp())
            })
        return response

    def extractDataGlobalBusinessCompanyOfficeBearersAddress(self, result_set: List[str]) -> List[str]:
        """
        Extracting the addresses of the office bearers of a global
        business company.

        Parameters:
            result_set: [string]: The data of the corporate registry.

        Returns:
            [string]
        """
        response: List[str] = []
        result_set = [value.upper() for value in result_set]
        addresses: List[str] = [value for value in result_set if bool(search(r"[\w]+", value)) == True and ("Street".upper() in value or "Court".upper() in value or "Avenue".upper() in value or "Tower".upper() in value or "Floor".upper() in value or "Level".upper() in value)]
        for index in range(0, len(addresses), 1):
            response.append(f"{addresses[index]} MAURITIUS")
        return response

    def extractDataGlobalBusinessCompanyBusinessDetails(self, result_set: List[str]) -> Dict[str, str]:
        """
        Extracting the business details of a global business company
        from the corporate registry.

        Parameters:
            result_set: [string]: The data of the corporate registry.

        Returns:
            {registered_address: string}
        """
        response: Dict[str, str] = {
            "registered_address": result_set[[index for index, value in enumerate(result_set) if "Registered Office Address:" in value][0]].split(": ")[-1].title()
        }
        return response

    def extractDataGlobalBusinessCompanyCompanyDetails(self, result_set: List[str]) -> Dict[str, Union[str, int]]:
        """
        Extracting the company details of a global business company
        from the corporate registry.

        Parameters:
            result_set: [string]: The data of the corporate registry.

        Returns:
            {file_number: string, name: string, category: string, date_incorporation: int, nature: string, status: string}
        """
        response: Dict[str, Union[str, int]]
        start_index: int = result_set.index("Company Details") + 1
        end_index: int = result_set.index("Office Bearers")
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if ":" not in value]
        date_of_incorporation: str = [value for value in result_set if "/" in value][0]
        response = {
            "file_number": result_set[0],
            "name": result_set[1].title(),
            "category": result_set[3].title(),
            "date_incorporation": int(datetime.strptime(date_of_incorporation, "%d/%m/%Y").timestamp()),
            "nature": result_set[5].title(),
            "status": result_set[6].title(),
        }
        return response

    def extractDataAuthorisedCompany(self, status: int, dataset: DocumentFiles) -> Dict[str, Union[int, Dict[str, Union[str, int]], Dict[str, str], List[Dict[str, Union[str, int]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]], Dict[str, Union[Dict[str, str], List[Dict[str, int]]]]]]:
        """
        Extracting the data from the portable document file version
        of the corporate registry based on the status of the file
        generation as well as on the dataset for an authorised
        company.

        Parameters:
            status: int: The status of the file generation.
            dataset: {identifier: int, file_data: bytes, company_detail: int}: The dataset of the corporate registry retrieved from the relational database server.

        Returns:
            {status: int, company_details: {name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}, business_details: {registered_address: string}, office_bearers: [{position: string, name: string, address: string, date_appointment: int}], receivers: {receiver: {name: string, date_appointed: int, address: string}, reports: [{date_filled: int, date_from: int, date_to: int}], affidavits: [{date_filled: int, date_from: int, date_to: int}]}, administrators: {administrator: {name: string, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}, liquidators: {liquidator: {name: string, address: string}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}}
        """
        response: Dict[str, Union[int, Dict[str, Union[str, int]], Dict[str, str], List[Dict[str, Union[str, int]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]], Dict[str, Union[Dict[str, str], List[Dict[str, int]]]]]]
        file_name: str = f"{self.ENV.getDirectory()}Cache/CorporateDocumentFile/Documents/{dataset.company_detail}.pdf"
        cache_data_file_name: str = f"{self.ENV.getDirectory()}Cache/CorporateDocumentFile/Metadata/{dataset.company_detail}.json"
        if status != 201:
            self.getLogger().error(f"The portable document file has not been generated correctly!  The application will abort the extraction.\nStatus: {status}\nFile Location: {file_name}\nDocument File Identifier: {dataset.identifier}\nCompany Detail Identifier: {dataset.company_detail}")
            return {
                "status": 404
            }
        try:
            portable_document_file_data: str = extract_text(file_name)
            cache_file = open(cache_data_file_name, "w")
            portable_document_file_data_result_set: List[str] = list(filter(None, portable_document_file_data.split("\n")))
            company_details: Dict[str, Union[str, int]] = self._extractDataAuthorisedCompanyCompanyDetails(portable_document_file_data_result_set)
            business_details: Dict[str, str] = self._extractDataAuthorisedCompanyBusinessDetails(portable_document_file_data_result_set)
            office_bearers: List[Dict[str, Union[str, int]]] = self._extractDataAuthorisedCompanyOfficeBearers(portable_document_file_data_result_set)
            receivers: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]] = self.extractReceivers(portable_document_file_data_result_set)
            administrators: Dict[str, Union[Dict[str, str], List[Dict[str, int]]]] = self._extractDataAuthorisedCompanyAdministrators(portable_document_file_data_result_set)
            liquidators: Dict[str, Union[Dict[str, str], List[Dict[str, int]]]] = self._extractDataAuthorisedCompanyLiquidators(portable_document_file_data_result_set)
            response = {
                "status": 200,
                "company_details": company_details,
                "business_details": business_details,
                "office_bearers": office_bearers,
                "receivers": receivers,
                "administrators": administrators,
                "liquidators": liquidators
            }
            cache_file.write(dumps(response, indent=4))
            cache_file.close()
            self.getLogger().inform(f"Data has been extracted from the portable document file version of the corporate registry.\nStatus: {response['status']}\nDocument File Identifier: {dataset.identifier}\nFile Location: {file_name}\nCompany Details Identifier: {dataset.company_detail}")
            return response
        except PDFSyntaxError as error:
            status = self.getCompanyDetails().invalidateCompany(dataset.company_detail)
            status = self.getDocumentFiles().deleteDocumentFile(dataset.company_detail) if status == 202 else status
            remove(file_name) if status == 204 else None
            status = 403 if status == 204 else status
            self.getLogger().error(f"Data cannot be extracted due to an error in the file type.\nStatus: {status}\nDocument File Identifier: {dataset.identifier}\nFile Location: {file_name}\nCompany Details Identifier: {dataset.company_detail}\nError: {error}")
            return {
                "status": status
            }

    def _extractDataAuthorisedCompanyLiquidators(self, portable_document_file_data: List[str]) -> Dict[str, Union[Dict[str, str], List[Dict[str, int]]]]:
        """
        Extracting the liquidators that are linked to the authorised
        company.

        Parameters:
            portable_document_file_data: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {liquidator: {name: string, address: string}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}
        """
        start_header: str = "Liquidators"
        end_header: str = "This is a Computer Generated Document."
        response: Dict[str, Union[Dict[str, str], List[Dict[str, int]]]] = {}
        if start_header not in portable_document_file_data:
            return response
        start_index: int = portable_document_file_data.index(start_header)
        end_index: int = portable_document_file_data.index(end_header)
        result_set: List[str] = portable_document_file_data[start_index:end_index]
        liquidator: Dict[str, str] = self.__extractDataAuthorisedCompanyLiquidators(result_set)
        affidavits: List[Dict[str, int]] = self._extractDataAuthorisedCompanyLiquidatorsAffidavits(result_set)
        if not liquidator and len(affidavits) == 0:
            return response
        self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader._extractDataAuthorisedCompanyLiquidators()")
        exit()

    def _extractDataAuthorisedCompanyLiquidatorsAffidavits(self, result_set: List[str]) -> List[Dict[str, int]]:
        """
        Extracting the affidavits that are linked to the liquidator
        that is related to an authorised company.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{date_filled: int, date_from: int, date_to: int}]
        """
        start_index: int = result_set.index("Affidavits of Liquidator") + 1
        result_set = result_set[start_index:]
        result_set = [value for value in result_set if ":" not in value]
        result_set = [value for value in result_set if "Date Filed" not in value]
        result_set = [value for value in result_set if "From" not in value]
        result_set = [value for value in result_set if "To" not in value]
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader._extractDataAuthorisedCompanyLiquidatorsAffidavits()")
            exit()
        else:
            return []

    def __extractDataAuthorisedCompanyLiquidators(self, result_set: List[str]) -> Dict[str, str]:
        """
        Extracting the liquidators of an authorised company.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {name: string, address: string}
        """
        start_index: int = result_set.index("Liquidators") + 1
        end_index: int = result_set.index("Affidavits of Liquidator")
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if ":" not in value]
        result_set = [value for value in result_set if "/" not in value]
        result_set = [value for value in result_set if "Page" not in value]
        result_set = [value for value in result_set if "of" not in value]
        result_set = [value for value in result_set if "Appointed Date" not in value]
        if len(result_set) == 0:
            return {}
        self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.__extractDataAuthorisedCompanyLiquidators()")
        exit()

    def _extractDataAuthorisedCompanyAdministrators(self, portable_document_file_data: List[str]) -> Dict[str, Union[Dict[str, str], List[Dict[str, int]]]]:
        """
        Extracting the administrators from an authorised company.

        Parameters:
            portable_document_file_data: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {administrator: {name: string, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}
        """
        start_header: str = "Administrators"
        end_header: str = "Liquidators"
        response: Dict[str, Union[Dict[str, str], List[Dict[str, int]]]] = {}
        if start_header not in portable_document_file_data:
            return response
        start_index: int = portable_document_file_data.index(start_header)
        end_index: int = portable_document_file_data.index(end_header)
        result_set: List[str] = portable_document_file_data[start_index:end_index]
        administrator: Dict[str, str] = self.__extractDataAuthorisedCompanyAdministrators(result_set)
        accounts: List[Dict[str, int]] = self._extractDataAuthorisedCompanyAdministratorsAccounts(result_set)
        if (not administrator and len(accounts) == 0) or (not administrator and len(accounts) != 0):
            return response
        self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader._extractDataAuthorisedCompanyAdministrators()")
        exit()

    def _extractDataAuthorisedCompanyAdministratorsAccounts(self, result_set: List[str]) -> List[Dict[str, int]]:
        """
        Extracting the accounts that are linked to the
        administrators of an authorised company.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{date_filled: int, date_from: int, date_to: int}]
        """
        set_amount: int = 3
        response: List[Dict[str, int]] = []
        start_index: int = result_set.index("Accounts of Administrator") + 1
        result_set = [value for value in result_set[start_index:] if ":" not in value and "Page" not in value and "of" not in value]
        result_set = [value for value in result_set if "/" in value]
        if len(result_set) < 3:
            return response
        dates: List[List[str]] = [result_set[index:index+set_amount] for index in range(0, len(result_set), set_amount)]
        for index in range(0, len(dates), 1):
            if len(dates[index]) == 3:
                response.append({
                    "date_filled": int(datetime.strptime(dates[index][0], "%d/%m/%Y").timestamp()),
                    "date_from": int(datetime.strptime(dates[index][1], "%d/%m/%Y").timestamp()),
                    "date_to": int(datetime.strptime(dates[index][2], "%d/%m/%Y").timestamp())
                })
        return response

    def __extractDataAuthorisedCompanyAdministrators(self, result_set: List[str]) -> Dict[str, str]:
        """
        Extracting the name of the administrator which is related to
        an authorised company.

        Parameters:
            result_set: [string]: The result set containing the data needed.

        Returns:
            {name: string, designation: string, address: string}
        """
        start_index: int = result_set.index("Administrators") + 1
        end_index: int = result_set.index("Accounts of Administrator")
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if "To" not in value]
        result_set = [value for value in result_set if ":" not in value]
        result_set = [value for value in result_set if "/" not in value]
        result_set = [value for value in result_set if "Page" not in value]
        result_set = [value for value in result_set if "of" not in value]
        if len(result_set) == 0:
            return {}
        self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.__extractDataAuthorisedCompanyAdministrators()")
        exit()

    def _extractDataAuthorisedCompanyOfficeBearers(self, portable_document_file_data: List[str]) -> List[Dict[str, Union[str, int]]]:
        """
        Extracting the data for the office bearers from the result
        set.

        Parameters:
            portable_document_file_data: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{position: string, name: string, address: string, date_appointment: int}]
        """
        start_header: str = "Office Bearers"
        end_header: str = "Receivers"
        response: List[Dict[str, Union[str, int]]] = []
        start_index: int = portable_document_file_data.index(start_header)
        end_index: int = portable_document_file_data.index(end_header) if end_header in portable_document_file_data else len(portable_document_file_data)
        result_set: List[str] = portable_document_file_data[start_index:end_index]
        result_set = [value for value in result_set if start_header not in value]
        result_set = [value for value in result_set if end_header not in value]
        result_set = [value for value in result_set if "Computer Generated Document" not in value]
        result_set = [value for value in result_set if "DISCLAIMER NOTICE" not in value]
        result_set = [value for value in result_set if "While we endeavour to keep the information up to date and as far as possible accurate, we cannot give any guarantee about the completeness, accuracy," not in value]
        result_set = [value for value in result_set if "reliability of the information contained on the report." not in value]
        result_set = [value for value in result_set if "Page" not in value]
        result_set = [value for value in result_set if "of" not in value]
        result_set = [value for value in result_set if "\x0c" not in value]
        result_set = [value for value in result_set if "Position" not in value]
        result_set = [value for value in result_set if "Name" not in value]
        result_set = [value for value in result_set if "Appointed Date" not in value]
        result_set = [value for value in result_set if "Service Address" not in value]
        dataset: List[str] = [value for value in result_set if "/" in value and bool(search(r"[\d]+", value)) == True and bool(search(r"[A-Z]+", value)) == False]
        date_appointments: List[str] = self.extractOfficeBearersDateAppointments(result_set)
        result_set = [value for value in result_set if value not in dataset]
        positions: List[str] = self.extractOfficeBearersPositions(result_set)
        result_set = [value for value in result_set if value not in positions]
        dataset = [value for value in result_set if "Lane" in value or "Street" in value or "Road" in value or "Floor" in value or "Tower" in value or "Lane".upper() in value or "Street".upper() in value or "Road".upper() in value or "Floor".upper() in value or "Tower".upper() in value]
        addresses: List[str] = self._extractDataAuthorisedCompanyOfficeBearersAddresses(result_set)
        result_set = [value for value in result_set if value not in dataset]
        names: List[str] = [value for value in result_set if value not in addresses]
        limitation: int = min([len(date_appointments), len(positions), len(addresses), len(names)])
        for index in range(0, limitation, 1):
            response.append({
                "position": positions[index].title(),
                "name": names[index].title(),
                "address": addresses[index].title(),
                "date_appointment": int(datetime.strptime(date_appointments[index], "%d/%m/%Y").timestamp())
            })
        return response

    def _extractDataAuthorisedCompanyOfficeBearersAddresses(self, result_set: List[str]) -> List[str]:
        """
        Extracting the addresses of the office bearers for an
        authorised company.

        Parameters:
            result_set: [string]: The result set containing the data needed.

        Returns:
            [string]
        """
        response: List[str] = []
        dataset: List[str] = [value for value in result_set if "Lane" in value or "Street" in value or "Road" in value or "Floor" in value or "Tower" in value or "Lane".upper() in value or "Street".upper() in value or "Road".upper() in value or "Floor".upper() in value or "Tower".upper() in value]
        for index in range(0, len(dataset), 1):
            data: str = " ".join([value for value in dataset[index].replace("MAURITIUS", "").split(" ") if value != ""]) + " Mauritius"
            response.append(data)
        return response

    def _extractDataAuthorisedCompanyBusinessDetails(self, portable_document_file_data: List[str]) -> Dict[str, str]:
        """
        Extracting the data for the business details from the result
        set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {registered_address: string}
        """
        response: Dict[str, str]
        start_index: int = [index for index, value in enumerate(portable_document_file_data) if "Registered Office Address:" in value][0]
        end_index: int = portable_document_file_data.index("Office Bearers")
        result_set: List[str] = portable_document_file_data[start_index:end_index]
        response = {
            "registered_address": " ".join([value.split(": ")[-1] for value in result_set]).title()
        }
        return response

    def _extractDataAuthorisedCompanyCompanyDetails(self, portable_document_file_data: List[str]) -> Dict[str, Union[str, int]]:
        """
        Extracting the data for the company details from the result
        set for an authorised company.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}
        """
        response: Dict[str, Union[str, int]]
        start_index: int = portable_document_file_data.index("Company Details") + 1
        end_index: int = portable_document_file_data.index("Office Bearers")
        result_set: List[str] = portable_document_file_data[start_index:end_index]
        result_set = [value for value in result_set if ":" not in value]
        result_set = [value for value in result_set if "Registrar of Companies" not in value]
        response = {
            "name": result_set[1],
            "file_number": result_set[0],
            "category": result_set[3].title(),
            "date_incorporation": int(datetime.strptime(result_set[4], "%d/%m/%Y").timestamp()) if "/" in result_set[4] and bool(search(r"[\d]+", result_set[4])) == True else int(time()),
            "nature": result_set[5],
            "status": result_set[6]
        }
        return response

    def extractDataDomestic(self, status: int, dataset: DocumentFiles, company_detail: CompanyDetails) -> Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]]:
        """
        Extracting the data from the portable document file version
        of the corporate registry based on the status of the file
        generation as well as on the dataset for a domestic company.

        Parameters:
            status: int: The status of the file generation.
            dataset: {identifier: int, file_data: bytes, company_detail: int}: The dataset of the corporate registry retrieved from the relational database server.
            company_detail: {identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int, is_extracted: int, company_identifier: int, company_type: string}: The data of the Company Details.

        Returns:
            {status: int, company_details: {business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}, business_details: [{registered_address: string, name: string, nature: string, operational: string}], certificates: [{certificate: string, type: str, date_effective: int, date_expiry: int}], office_bearers: [{position: string, name: string, address: string, date_appointment: int}], shareholders: [{name: string, amount: int, type: string, currency: string}], members: [{name: string, amount: int, date_start: int, currency: string}], annual_return: [{date_annual_return: int, date_annual_meeting: int, date_filled: int}], financial_summaries: [{financial_year: int, currency: string, date_approved: int, unit: int}], profit_statement: {financial_summary: {financial_year: int, currency: string, date_approved: int, unit: int}, turnover: float, cost_of_sales: float, gross_profit: float, other_income: float, distribution_cost: float, administration_cost: float, expenses: float, finance_cost: float, net_profit_before_taxation: float, taxation: float, net_profit: float}, state_capital: {type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}, balance_sheet: {balance_sheet: {financial_year: int, currency: string, unit: int}, assets: {non_current_assets: {property_plant_equipment: float, investment_properties: float, intangible_assets: float, other_investments: float, subsidiaries_investments: float, biological_assets: float, others: float, total: float}, current_assets: {inventories: float, trade: float, cash: float, others: float, total: float}, total: float}, liabilities: {equity_and_liabilities: {share_capital: float, other_reserves: float, retained_earnings: float, others: float, total: float}, non_current: {long_term_borrowings: float, deferred_tax: float, long_term_provisions: float, others: float, total: float}, current: {trade: float, short_term_borrowings: float, current_tax_payable: float, short_term_provisions: float, others: float, total: float}, total_liabilities: float, total_equity_and_liabilities: float}}, charges: [{volume: int, property: string, nature: string, amount: int, date_charged: int, date_filled: int, currency: string}], liquidators: {liquidator: {name: string, appointed_date: int, address: string}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}, receivers: {receiver: {name: string, date_appointed: int, address: string}, reports: [{date_filled: int, date_from: int, date_to: int}], affidavits: [{date_filled: int, date_from: int, date_to: int}]}, administrators: {administrator: {name: string, date_appointed: int, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}, details: [{type: string, date_start: int, date_end: int, status: string}], objections: [{date_objection: int, objector: string}]}
        """
        response: Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]]
        if company_detail.nature.upper() == "PRIVATE":
            response = self.extractDataDomesticPrivate(status, dataset)
        elif company_detail.nature.upper() == "CIVIL":
            response = self.extractDataDomesticCivil(status, dataset)
        elif company_detail.nature.upper() == "PUBLIC":
            response = self.extractDataDomesticPublic(status, dataset)
        elif company_detail.nature.upper() == "COMMERCIAL":
            response = self.extractDataDomesticCommercial(status, dataset)
        else:
            self.getLogger().error(f"The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractDataDomestic()\nNature: {company_detail.nature}")
            exit()
        return response

    def extractDataDomesticPublic(self, status: int, dataset: DocumentFiles) -> Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]]:
        """
        Extracting the data from the portable document file version
        of the corporate registry based on the status of the file
        generation as well as on the dataset for a domestic company
        which is also a public company.

        Parameters:
            status: int: The status of the file generation.
            dataset: {identifier: int, file_data: bytes, company_detail: int}: The dataset of the corporate registry retrieved from the relational database server.

        Returns:
            {status: int, company_details: {business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}, business_details: [{registered_address: string, name: string, nature: string, operational: string}], certificates: [{certificate: string, type: str, date_effective: int, date_expiry: int}], office_bearers: [{position: string, name: string, address: string, date_appointment: int}], shareholders: [{name: string, amount: int, type: string, currency: string}], members: [{name: string, amount: int, date_start: int, currency: string}], annual_return: [{date_annual_return: int, date_annual_meeting: int, date_filled: int}], financial_summaries: [{financial_year: int, currency: string, date_approved: int, unit: int}], profit_statement: {financial_summary: {financial_year: int, currency: string, date_approved: int, unit: int}, turnover: float, cost_of_sales: float, gross_profit: float, other_income: float, distribution_cost: float, administration_cost: float, expenses: float, finance_cost: float, net_profit_before_taxation: float, taxation: float, net_profit: float}, state_capital: {type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}, balance_sheet: {balance_sheet: {financial_year: int, currency: string, unit: int}, assets: {non_current_assets: {property_plant_equipment: float, investment_properties: float, intangible_assets: float, other_investments: float, subsidiaries_investments: float, biological_assets: float, others: float, total: float}, current_assets: {inventories: float, trade: float, cash: float, others: float, total: float}, total: float}, liabilities: {equity_and_liabilities: {share_capital: float, other_reserves: float, retained_earnings: float, others: float, total: float}, non_current: {long_term_borrowings: float, deferred_tax: float, long_term_provisions: float, others: float, total: float}, current: {trade: float, short_term_borrowings: float, current_tax_payable: float, short_term_provisions: float, others: float, total: float}, total_liabilities: float, total_equity_and_liabilities: float}}, charges: [{volume: int, property: string, nature: string, amount: int, date_charged: int, date_filled: int, currency: string}], liquidators: {liquidator: {name: string, appointed_date: int, address: string}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}, receivers: {receiver: {name: string, date_appointed: int, address: string}, reports: [{date_filled: int, date_from: int, date_to: int}], affidavits: [{date_filled: int, date_from: int, date_to: int}]}, administrators: {administrator: {name: string, date_appointed: int, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}, details: [{type: string, date_start: int, date_end: int, status: string}], objections: [{date_objection: int, objector: string}]}
        """
        response: Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]]
        file_name: str = f"{self.ENV.getDirectory()}Cache/CorporateDocumentFile/Documents/{dataset.company_detail}.pdf"
        cache_data_file_name: str = f"{self.ENV.getDirectory()}Cache/CorporateDocumentFile/Metadata/{dataset.company_detail}.json"
        if status == 201:
            portable_document_file_data: str = extract_text(file_name)
            cache_file = open(cache_data_file_name, "w")
            portable_document_file_data_result_set: List[str] = list(filter(None, portable_document_file_data.split("\n")))
            company_details: Dict[str, Union[str, int]] = self.extractCompanyDetails(portable_document_file_data_result_set)
            business_details: List[Dict[str, str]] = self.extractDataDomesticPublicBusinessDetails(portable_document_file_data_result_set)
            certificates: List[Dict[str, Union[str, int]]] = self.extractCertificates(portable_document_file_data_result_set)
            office_bearers: List[Dict[str, Union[str, int]]] = self.extractOfficeBearers(portable_document_file_data_result_set)
            shareholders: List[Dict[str, Union[str, int]]] = self.extractDataDomesticPublicShareholder(portable_document_file_data_result_set)
            members: List[Dict[str, Union[str, int]]] = self.extractMembers(portable_document_file_data_result_set)
            annual_return: List[Dict[str, int]] = self.extractAnnualReturns(portable_document_file_data_result_set)
            financial_summaries: List[Dict[str, Union[int, str]]] = self.extractFinancialSummaries(portable_document_file_data_result_set)
            profit_statement: Dict[str, Union[Dict[str, Union[int, str]], float]] = self.extractProfitStatements(portable_document_file_data_result_set)
            state_capital: List[Dict[str, Union[str, int, float]]] = self.extractStateCapital(portable_document_file_data_result_set)
            balance_sheet: Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]] = self.extractBalanceSheet(portable_document_file_data_result_set)
            charges: List[Dict[str, Union[int, str]]] = self.extractCharges(portable_document_file_data_result_set)
            liquidators: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]] = self.extractLiquidators(portable_document_file_data_result_set)
            receivers: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]] = self.extractReceivers(portable_document_file_data_result_set)
            administrators: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]] = self.extractAdministrators(portable_document_file_data_result_set)
            details: List[Dict[str, Union[str, int, None]]] = self.extractDetails(portable_document_file_data_result_set)
            objections: List[Dict[str, Union[int, str]]] = self.extractObjections(portable_document_file_data_result_set)
            response = {
                "status": 200,
                "company_details": company_details,
                "business_details": business_details,
                "certificates": certificates,
                "office_bearers": office_bearers,
                "shareholders": shareholders,
                "members": members,
                "annual_return": annual_return,
                "financial_summaries": financial_summaries,
                "profit_statement": profit_statement,
                "state_capital": state_capital, # type: ignore
                "balance_sheet": balance_sheet,
                "charges": charges,
                "liquidators": liquidators,
                "receivers": receivers,
                "administrators": administrators,
                "details": details,
                "objections": objections
            }
            cache_file.write(dumps(response, indent=4))
            cache_file.close()
            self.getLogger().inform(f"Data has been extracted from the portable document file version of the corporate registry.\nStatus: {response['status']}\nDocument File Identifier: {dataset.identifier}\nFile Location: {file_name}\nCompany Details Identifier: {dataset.company_detail}")
        else:
            response = {
                "status": 404
            }
            self.getLogger().error(f"The portable document file has not been generated correctly!  The application will abort the extraction.\nStatus: {response['status']}\nFile Location: {file_name}\nDocument File Identifier: {dataset.identifier}\nCompany Detail Identifier: {dataset.company_detail}")
        return response

    def extractDataDomesticPublicShareholder(self, portable_document_file_result_set: List[str]) -> List[Dict[str, Union[str, int]]]:
        """
        Extracting the data for the shareholders of a private
        domestic company.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{name: string, amount: int, type: string, currency: string}]
        """
        response: List[Dict[str, Union[str, int]]] = []
        start_index: int = portable_document_file_result_set.index("Shareholders") + 1
        end_index: int = portable_document_file_result_set.index("Members (Applicable for Company Limited by Guarantee or Shares and Guarantee)")
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        result_set = [value for value in result_set if "Name" not in value]
        result_set = [value for value in result_set if "Type of Shares" not in value]
        result_set = [value for value in result_set if "Currency" not in value]
        dataset: List[str] = [value for value in result_set if bool(search(r"[\d]+", value)) == True and bool(search(r"[A-Z]+", value)) == True and bool(search(r"[^\w\s]+", value)) == False]
        amount_of_shares: List[int] = self.extractShareholdersAmountShares(result_set)
        type_of_shares: List[str] = self.extractShareholdersTypeShares(result_set)
        result_set = [value for value in result_set if value not in dataset]
        names: List[str] = [value for value in result_set if bool(search(r"[A-z\s]+", value)) == True and "Mauritius" not in value]
        names = [name for index, name in enumerate(names) if all(name not in names for name in names[:index])]
        dataset = [value for value in result_set if bool(search(r"[A-z\s]+", value)) == True and "Mauritius" not in value]
        currencies: List[str] = [value for value in result_set if value not in dataset]
        for index in range(0, min([len(names), len(amount_of_shares), len(type_of_shares), len(currencies)]), 1):
            response.append({
                "name": names[index].title(),
                "amount_shares": amount_of_shares[index],
                "type_shares": type_of_shares[index].title(),
                "currency": currencies[index].title()
            })
        return response

    def extractDataDomesticPublicBusinessDetails(self, portable_document_file_result_set: List[str]) -> List[Dict[str, str]]:
        """
        Extracting the data for the business details of a public
        domestic company from the result set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{registered_address: string, name: string, nature: string, operational: string}]
        """
        response: List[Dict[str, str]] = []
        registered_address: str = " ".join([value for value in portable_document_file_result_set[[index for index, value in enumerate(portable_document_file_result_set) if "Registered Office Address" in value][0]].split(": ")[-1].split(" ") if value != ""])
        start_index: int = portable_document_file_result_set.index("Business Details")
        end_index: int = portable_document_file_result_set.index("Particulars of Stated Capital")
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        result_set = [value for value in result_set if "Business" not in value]
        dataset: List[str] = [value for value in result_set if bool(search(r"[A-Z]+", value)) == True and "Mauritius".upper() in value]
        operational_addresses: List[str] = self.extractBusinessDetailsOperationalAddresses(result_set)
        result_set = [value for value in result_set if value not in dataset]
        dataset = [value for value in result_set if (bool(search(r"[A-Z]+", value)) == True or bool(search(r"[a-z]+", value)) == True) and bool(search(r"[\w]+", value)) == True]
        natures: List[str] = [value for value in result_set if (bool(search(r"[A-Z]+", value)) == True or bool(search(r"[a-z]+", value)) == True) and bool(search(r"[\w]+", value)) == True]
        names: List[str] = [value for value in result_set if value not in dataset]
        for index in range(0, min([len(names), len(natures), len(operational_addresses)]), 1):
            response.append({
                "registered_address": registered_address.title(),
                "name": names[index].title(),
                "nature": natures[index].title(),
                "operational_address": operational_addresses[index].title()
            })
        return response

    def extractDataDomesticCommercial(self, status: int, dataset: DocumentFiles) -> Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]]:
        """
        Extracting the data from the portable document file version
        of the corporate registry based on the status of the file
        generation as well as on the dataset for a domestic company
        which is also a commercial company.

        Parameters:
            status: int: The status of the file generation.
            dataset: {identifier: int, file_data: bytes, company_detail: int}: The dataset of the corporate registry retrieved from the relational database server.

        Returns:
            {status: int, company_details: {name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}, business_details: [{registered_address: string, name: string, nature: string, operational: string}] | {registered_address: string, name: string, nature: string, operational: string}, state_capital: [{type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}], office_bearers: [{position: string, name: string, address: string, date_appointed: int}], shareholders: [{name: string, amount: int, type: string, currency: string}], liquidators: {liquidator: {name: string, appointed_date: int, address: string}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}, receivers: {receiver: {name: string, date_appointed: int, address: string}, reports: [{date_filled: int, date_from: int, date_to: int}], affidavits: [{date_filled: int, date_from: int, date_to: int}]}, administrators: {administrator: {name: string, date_appointed: int, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}, details: [{type: string, date_start: int, date_end: int, status: string}], objections: [{date_objection: int, objector: string}]}
        """
        response: Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]]
        file_name: str = f"{self.ENV.getDirectory()}Cache/CorporateDocumentFile/Documents/{dataset.company_detail}.pdf"
        cache_data_file_name: str = f"{self.ENV.getDirectory()}Cache/CorporateDocumentFile/Metadata/{dataset.company_detail}.json"
        if status != 201:
            status = 404
            self.getLogger().error(f"The portable document file has not been generated correctly!  The application will abort the extraction.\nStatus: {status}\nFile Location: {file_name}\nDocument File Identifier: {dataset.identifier}\nCompany Detail Identifier: {dataset.company_detail}")
            return {
                "status": 404
            }
        try:
            portable_document_file_data: str = extract_text(file_name)
            cache_file = open(cache_data_file_name, "w")
            portable_document_file_data_result_set: List[str] = list(filter(None, portable_document_file_data.split("\n")))
            business_registration_number: Union[str, None] = self.extractDataDomesticCivilBusinessRegistrationNumber(portable_document_file_data_result_set)
            response = self._extractDataDomesticCivil(portable_document_file_data_result_set, business_registration_number)
            cache_file.write(dumps(response, indent=4))
            cache_file.close()
            self.getLogger().inform(f"Data has been extracted from the portable document file version of the corporate registry.\nStatus: {response['status']}\nDocument File Identifier: {dataset.identifier}\nFile Location: {file_name}\nCompany Details Identifier: {dataset.company_detail}")
            return response
        except PDFSyntaxError as error:
            status = self.getCompanyDetails().invalidateCompany(dataset.company_detail)
            status = self.getDocumentFiles().deleteDocumentFile(dataset.company_detail) if status == 202 else status
            remove(file_name) if status == 204 else None
            status = 403 if status == 204 else status
            self.getLogger().error(f"Data cannot be extracted due to an error in the file type.\nStatus: {status}\nDocument File Identifier: {dataset.identifier}\nFile Location: {file_name}\nCompany Details Identifier: {dataset.company_detail}\nError: {error}")
            return {
                "status": status
            }

    def extractDataDomesticCivil(self, status: int, dataset: DocumentFiles) -> Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]]:
        """
        Extracting the data from the portable document file version
        of the corporate registry based on the status of the file
        generation as well as on the dataset for a domestic company
        which is also a civil company.

        Parameters:
            status: int: The status of the file generation.
            dataset: {identifier: int, file_data: bytes, company_detail: int}: The dataset of the corporate registry retrieved from the relational database server.

        Returns:
            {status: int, company_details: {name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}, business_details: [{registered_address: string, name: string, nature: string, operational: string}] | {registered_address: string, name: string, nature: string, operational: string}, state_capital: [{type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}], office_bearers: [{position: string, name: string, address: string, date_appointed: int}], shareholders: [{name: string, amount: int, type: string, currency: string}], liquidators: {liquidator: {name: string, appointed_date: int, address: string}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}, receivers: {receiver: {name: string, date_appointed: int, address: string}, reports: [{date_filled: int, date_from: int, date_to: int}], affidavits: [{date_filled: int, date_from: int, date_to: int}]}, administrators: {administrator: {name: string, date_appointed: int, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}, details: [{type: string, date_start: int, date_end: int, status: string}], objections: [{date_objection: int, objector: string}]}
        """
        response: Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]]
        file_name: str = f"{self.ENV.getDirectory()}Cache/CorporateDocumentFile/Documents/{dataset.company_detail}.pdf"
        cache_data_file_name: str = f"{self.ENV.getDirectory()}Cache/CorporateDocumentFile/Metadata/{dataset.company_detail}.json"
        if status != 201:
            status = 404
            self.getLogger().error(f"The portable document file has not been generated correctly!  The application will abort the extraction.\nStatus: {status}\nFile Location: {file_name}\nDocument File Identifier: {dataset.identifier}\nCompany Detail Identifier: {dataset.company_detail}")
            return {
                "status": 404
            }
        try:
            portable_document_file_data: str = extract_text(file_name)
            cache_file = open(cache_data_file_name, "w")
            portable_document_file_data_result_set: List[str] = list(filter(None, portable_document_file_data.split("\n")))
            business_registration_number: Union[str, None] = self.extractDataDomesticCivilBusinessRegistrationNumber(portable_document_file_data_result_set)
            response = self._extractDataDomesticCivil(portable_document_file_data_result_set, business_registration_number)
            cache_file.write(dumps(response, indent=4))
            cache_file.close()
            self.getLogger().inform(f"Data has been extracted from the portable document file version of the corporate registry.\nStatus: {response['status']}\nDocument File Identifier: {dataset.identifier}\nFile Location: {file_name}\nCompany Details Identifier: {dataset.company_detail}")
            return response
        except PDFSyntaxError as error:
            status = self.getCompanyDetails().invalidateCompany(dataset.company_detail)
            status = self.getDocumentFiles().deleteDocumentFile(dataset.company_detail) if status == 202 else status
            remove(file_name) if status == 204 else None
            status = 403 if status == 204 else status
            self.getLogger().error(f"Data cannot be extracted due to an error in the file type.\nStatus: {status}\nDocument File Identifier: {dataset.identifier}\nFile Location: {file_name}\nCompany Details Identifier: {dataset.company_detail}\nError: {error}")
            return {
                "status": status
            }

    def _extractDataDomesticCivil(self, result_set: List[str], business_registration_number: Union[str, None]) -> Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]]:
        """
        Extracting the data from the portable document file version
        of the corporate registry based on the status of the file
        generation as well as on the dataset for a domestic company
        which is also a civil company to determine whether the
        company is a société civile or a société commerciale.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.
            business_registration_number: string | null: The registration number of a company which is allowed to do business domestically.

        Returns:
            {status: int, company_details: {name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}, business_details: [{registered_address: string, name: string, nature: string, operational: string}] | {registered_address: string, name: string, nature: string, operational: string}, state_capital: [{type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}], office_bearers: [{position: string, name: string, address: string, date_appointed: int}], shareholders: [{name: string, amount: int, type: string, currency: string}], liquidators: {liquidator: {name: string, appointed_date: int, address: string}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}, receivers: {receiver: {name: string, date_appointed: int, address: string}, reports: [{date_filled: int, date_from: int, date_to: int}], affidavits: [{date_filled: int, date_from: int, date_to: int}]}, administrators: {administrator: {name: string, date_appointed: int, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}, details: [{type: string, date_start: int, date_end: int, status: string}], objections: [{date_objection: int, objector: string}]}
        """
        response: Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]]
        if business_registration_number == None:
            response = self._extractDataDomesticCivilCivil(result_set)
        else:
            self.getLogger().error(f"The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader._extractDataDomesticCivil()\nCivil Company Type: Société Commerciale")
            exit()
        return response

    def _extractDataDomesticCivilCivil(self, result_set: List[str]) -> Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]]:
        """
        Extracting the data from the portable document file version
        of the corporate registry based on the status of the file
        generation as well as on the dataset for a domestic company
        which is also a civil company which is also a société
        civile.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {status: int, company_details: {name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}, business_details: [{registered_address: string, name: string, nature: string, operational: string}] | {registered_address: string, name: string, nature: string, operational: string}, state_capital: [{type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}], office_bearers: [{position: string, name: string, address: string, date_appointed: int}], shareholders: [{name: string, amount: int, type: string, currency: string}], liquidators: {liquidator: {name: string, appointed_date: int, address: string}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}, receivers: {receiver: {name: string, date_appointed: int, address: string}, reports: [{date_filled: int, date_from: int, date_to: int}], affidavits: [{date_filled: int, date_from: int, date_to: int}]}, administrators: {administrator: {name: string, date_appointed: int, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}, details: [{type: string, date_start: int, date_end: int, status: string}], objections: [{date_objection: int, objector: string}]}
        """
        company_details: Dict[str, Union[str, int, None]] = self._extractDataDomesticCivilCivilCompanyDetails(result_set)
        business_details: Union[List[Dict[str, str]], Dict[str, str]] = self._extractDataDomesticCivilCivilBusinessDetails(result_set)
        state_capital: List[Dict[str, Union[str, int]]] = self._extractDataDomesticCivilCivilStateCapital(result_set)
        office_bearers: List[Dict[str, Union[str, int]]] = self._extractDataDomesticCivilCivilOfficeBearers(result_set)
        shareholders: List[Dict[str, Union[str, int]]] = self._extractDataDomesticCivilCivilShareholders(result_set)
        liquidators: Dict[str, Union[Dict[str, Union[str, int]], List[int]]] = self._extractDataDomesticCivilCivilLiquidators(result_set)
        receivers: Dict[str, Union[Dict[str, Union[str, int]], List[int]]] = self._extractDataDomesticCivilCivilReceivers(result_set)
        administrators: Dict[str, Union[Dict[str, Union[str, int]], List[int]]] = self._extractDataDomesticCivilCivilAdministrators(result_set)
        details: List[Dict[str, Union[str, int]]] = self._extractDataDomesticCivilCivilDetails(result_set)
        objections: List[Dict[str, Union[str, int]]] = self._extractDataDomesticCivilCivilObjections(result_set)
        return {
            "status": 200,
            "company_details": company_details,
            "business_details": business_details,
            "state_capital": state_capital,
            "office_bearers": office_bearers,
            "shareholders": shareholders,
            "liquidators": liquidators,
            "receivers": receivers,
            "administrators": administrators,
            "details": details,
            "objections": objections
        } # type: ignore

    def _extractDataDomesticCivilCivilObjections(self, result_set: List[str]) -> List[Dict[str, Union[str, int]]]:
        """
        Extracting the objections of a société civile.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{date_objection: int, objector: string}]
        """
        start_index: int = result_set.index("Objection Date")
        end_index: int = result_set.index("Last Annual Registration Fee Paid:")
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if "Object" not in value]
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader._extractDataDomesticCivilCivilObjections()")
            exit()
        else:
            return []

    def _extractDataDomesticCivilCivilDetails(self, result_set: List[str]) -> List[Dict[str, Union[str, int]]]:
        """
        Extracting the details of a société civile.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{type: string, date_start: int, date_end: int, status: string}]
        """
        start_header: str = "Winding Up Details"
        end_header: str = "Objections"
        response: List[Dict[str, Union[str, int]]] = []
        start_index: int = result_set.index(start_header)
        end_index: int = result_set.index(end_header)
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if start_header not in value]
        result_set = [value for value in result_set if end_header not in value]
        result_set = [value for value in result_set if "Type" not in value]
        result_set = [value for value in result_set if "Start Date" not in value]
        result_set = [value for value in result_set if "End Date" not in value]
        result_set = [value for value in result_set if "Status" not in value]
        result_set = [value for value in result_set if "Currency" not in value]
        result_set = [value for value in result_set if "PART" not in value]
        result_set = [value for value in result_set if "Mauritius Rupee" not in value]
        result_set = [value for value in result_set if "Name" not in value]
        result_set = [value for value in result_set if "Service Address" not in value]
        result_set = [value for value in result_set if "Appointed Date" not in value]
        if len(result_set) == 0:
            return response
        if len(result_set) < 4:
            return response
        for index in range(0, len(result_set), 4):
            response.append({
                "type": str(result_set[index]).capitalize(),
                "date_start": int(datetime.strptime(result_set[index + 1], "%d/%m/%Y").timestamp()) if "/" in result_set[index + 1] else 0,
                "date_end": int(datetime.strptime(result_set[index + 2], "%d/%m/%Y").timestamp()) if "/" in result_set[index + 2] else 0,
                "status": str(result_set[index + 3]).capitalize()
            })
        response = [detail for detail in response if int(detail["date_start"]) != 0 and int(detail["date_end"]) != 0]
        return response

    def _extractDataDomesticCivilCivilAdministrators(self, result_set: List[str]) -> Dict[str, Union[Dict[str, Union[str, int]], List[int]]]:
        """
        Extracting the administrators of a société civile.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {administrator: {name: string, date_appointed: int, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}
        """
        start_header: str = "Administrators"
        end_header: str = "Start Date"
        response: Dict[str, Union[Dict[str, Union[str, int]], List[int]]] = {}
        if start_header not in result_set:
            return response
        start_index: int = result_set.index(start_header)
        end_index: int = result_set.index(end_header)
        result_set = result_set[start_index:end_index]
        administrator: Dict[str, Union[str, int]] = self.__extractDataDomesticCivilCivilAdministrators(result_set)
        accounts: List[Dict[str, int]] = self._extractDataDomesticCivilCivilAdministratorsAccounts(result_set)
        if not administrator and len(accounts) == 0:
            return response
        self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractAdministrators()")
        exit()

    def _extractDataDomesticCivilCivilAdministratorsAccounts(self, result_set: List[str]) -> List[Dict[str, int]]:
        """
        Extracting the accounts of the administrators of a société
        civile.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{date_filled: int, date_from: int, date_to: int}]
        """
        start_index: int = result_set.index("Accounts of Administrator") + 1
        end_index: int = result_set.index("Winding Up Details")
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if "Date Filed" not in value]
        result_set = [value for value in result_set if "From" not in value]
        result_set = [value for value in result_set if "To" not in value]
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader._extractDataDomesticCivilCivilAdministratorsAccounts()")
            exit()
        else:
            return []

    def __extractDataDomesticCivilCivilAdministrators(self, result_set: List[str]) -> Dict[str, Union[str, int]]:
        """
        Extracting the administrators of a société civile.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {name: string, date_appointed: int, designation: string, address: string}
        """
        start_index: int = result_set.index("Appointed Date:")
        end_index: int = result_set.index("Appointed Date:") + 4
        date_appointeds: List[str] = result_set[start_index:end_index]
        end_index = int(len(date_appointeds) / 2)
        date_appointeds = date_appointeds[:end_index]
        start_index = result_set.index("Administrators") + 1
        end_index = result_set.index("Address:") + 2
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if "To" not in value]
        result_set = result_set + date_appointeds
        result_set = [value for value in result_set if ":" not in value]
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.__extractDataDomesticCivilCivilAdministrators()")
            exit()
        else:
            return {}

    def _extractDataDomesticCivilCivilReceivers(self, result_set: List[str]) -> Dict[str, Union[Dict[str, Union[str, int]], List[int]]]:
        """
        Extracting the receivers of a société civile.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {receiver: {name: string, date_appointed: int, address: string}, reports: [{date_filled: int, date_from: int, date_to: int}], affidavits: [{date_filled: int, date_from: int, date_to: int}]}
        """
        start_header: str = "Receivers"
        end_header: str = "Accounts of Administrator"
        response: Dict[str, Union[Dict[str, Union[str, int]], List[int]]] = {}
        if start_header not in result_set:
            return response
        start_index: int = result_set.index(start_header)
        end_index: int = result_set.index(end_header)
        result_set = result_set[start_index:end_index]
        start_index = result_set.index("Name:")
        result_set = result_set[start_index:]
        result_set = [value for value in result_set if "Page" not in value]
        result_set = [value for value in result_set if "Date Issued" not in value]
        result_set = [value for value in result_set if " of " not in value]
        receiver: Dict[str, Union[str, int]] = self.__extractDataDomesticCivilCivilReceivers(result_set)
        reports: List[Dict[str, int]] = self._extractDataDomesticCivilCivilReports(result_set)
        affidavits: List[Dict[str, int]] = self._extractDataDomesticCivilCivilAffidavits(result_set)
        if not receiver and len(reports) == 0 and len(affidavits) == 0:
            return response
        self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader._extractDataDomesticCivilCivilReceivers()")
        exit()

    def _extractDataDomesticCivilCivilAffidavits(self, result_set: List[str]) -> List[Dict[str, int]]:
        """
        Extracting the affidavits that are related to the receivers
        of a société civile.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{date_filled: int, date_from: int, date_to: int}]
        """
        start_index: int = result_set.index("Date Filed")
        result_set = result_set[start_index:]
        start_index = result_set.index("Date Filed")
        end_index: int = result_set.index("Date Filed") + 4
        dataset: List[str] = result_set[start_index:end_index]
        start_index = int(len(dataset) / 2)
        dataset = dataset[start_index:]
        start_index = result_set.index("To")
        end_index = result_set.index("To") + 4
        date_to: List[str] = result_set[start_index:end_index]
        end_index = int(len(date_to) / 2)
        date_to = date_to[:end_index]
        result_set = dataset + date_to
        result_set = [value for value in result_set if "Date Filed" not in value]
        result_set = [value for value in result_set if "From" not in value]
        result_set = [value for value in result_set if "To" not in value]
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader._extractDataDomesticCivilCivilAffidavits()")
            exit()
        else:
            return []

    def _extractDataDomesticCivilCivilReports(self, result_set: List[str]) -> List[Dict[str, int]]:
        """
        Extracting the reports that are related to the receivers of
        a société civile.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{date_filled: int, date_from: int, date_to: int}]
        """
        start_index: int = result_set.index("Date Filed")
        result_set = result_set[start_index:]
        start_index = result_set.index("Date Filed")
        end_index: int = result_set.index("Date Filed") + 4
        dataset: List[str] = result_set[start_index:end_index]
        end_index = int(len(dataset) / 2)
        dataset = dataset[:end_index]
        start_index = result_set.index("To")
        end_index = result_set.index("To") + 4
        date_to: List[str] = result_set[start_index:end_index]
        end_index = int(len(date_to) / 2)
        date_to = date_to[:end_index]
        result_set = dataset + date_to
        result_set = [value for value in result_set if "Date Filed" not in value]
        result_set = [value for value in result_set if "From" not in value]
        result_set = [value for value in result_set if "To" not in value]
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader._extractDataDomesticCivilCivilReports()")
            exit()
        else:
            return []

    def __extractDataDomesticCivilCivilReceivers(self, result_set: List[str]) -> Dict[str, Union[str, int]]:
        """
        Extracting the receiver that is related to the receivers of
        a société civile.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {name: string, date_appointed: int, address: string}
        """
        start_index: int = result_set.index("Name:")
        end_index: int = result_set.index("Date Filed")
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if ":" not in value]
        if len(result_set) >= 3:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.__extractDataDomesticCivilCivilReceivers()")
            exit()
        else:
            return {}

    def _extractDataDomesticCivilCivilLiquidators(self, result_set: List[str]) -> Dict[str, Union[Dict[str, Union[str, int]], List[int]]]:
        """
        Extracting the liquidators of a société civile.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {liquidator: {name: string, appointed_date: int, address: string}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}
        """
        start_header: str = "Liquidators"
        end_header: str = "Reports of Receiver"
        response: Dict[str, Union[Dict[str, Union[str, int]], List[int]]] = {}
        if start_header not in result_set:
            return response
        start_index: int = result_set.index(start_header)
        end_index: int = result_set.index(end_header)
        result_set = result_set[start_index:end_index]
        liquidator: Dict[str, Union[str, int]] = self._extractLiquidators(result_set)
        affidavits: List[Dict[str, int]] = self.extractLiquidatorsAffidavits(result_set)
        if not liquidator and len(affidavits) == 0:
            return response
        self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader._extractDataDomesticCivilCivilLiquidators()")
        exit()

    def _extractDataDomesticCivilCivilShareholders(self, result_set: List[str]) -> List[Dict[str, Union[str, int]]]:
        """
        Extracting the shareholders of a société civile.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{name: string, amount: int, type: string, currency: string}]
        """
        names: List[str]
        start_header: str = "Associes"
        end_header: str = "Winding Up Details"
        response: List[Dict[str, Union[str, int]]] = []
        start_index: int = result_set.index(start_header)
        end_index: int = result_set.index(end_header)
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if start_header not in value]
        result_set = [value for value in result_set if end_header not in value]
        result_set = [value for value in result_set if "Name" not in value]
        result_set = [value for value in result_set if "Service Address" not in value]
        result_set = [value for value in result_set if "Appointed Date" not in value]
        result_set = [value for value in result_set if "/" not in value]
        result_set = [value for value in result_set if "Shares" not in value]
        result_set = [value for value in result_set if "Currency" not in value]
        result_set = [value for value in result_set if "REUNION" not in value]
        result_set = [value for value in result_set if "MAURITIUS" not in value]
        names = [name for name in result_set if bool(search(r"[\d]+", name)) == False]
        names = [name for name in names if bool(search(r"[a-z]+", name)) == False]
        result_set = [value for value in result_set if value not in names]
        amounts: List[int] = self._extractDataDomesticCivilCivilShareholdersAmount(result_set)
        shareholders_types: Dict[str, List[str]] = self._extractDataDomesticCivilCivilShareholdersType(result_set)
        types: List[str] = shareholders_types["types"]
        result_set = shareholders_types["result_set"]
        currencies: List[str] = [currency for currency in result_set if bool(search(r"[\d]+", currency)) == False]
        limitation: int = min([len(amounts), len(types), len(names), len(currencies)])
        for index in range(0, limitation, 1):
            response.append({
                "name": names[index].title(),
                "amount_shares": amounts[index],
                "type_shares": types[index].title(),
                "currency": currencies[index].title()
            })
        return response

    def _extractDataDomesticCivilCivilShareholdersType(self, result_set: List[str]) -> Dict[str, List[str]]:
        """
        Extracting the type of the shares for a shareholder of a
        société civile.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {types: [string], result_set: [string]}
        """
        types: List[str] = []
        dataset = [value for value in result_set if bool(search(r"[\d]+", value)) == True and bool(search(r"[a-z]+", value)) == False and "/" not in value]
        for index in range(0, len(dataset), 1):
            type: str = " ".join([value for value in split(" ", dataset[index]) if bool(search(r"[\d]+", value)) == False])
            types.append(type)
        for index in range(0, len(types), 1):
            result_set = [value for value in result_set if types[index] not in value]
        response: Dict[str, List[str]] = {
            "types": types,
            "result_set": result_set
        }
        return response

    def _extractDataDomesticCivilCivilShareholdersAmount(self, result_set: List[str]) -> List[int]:
        """
        Extracting the amount of shares of the shareholders of a
        société civile.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [int]
        """
        response: List[int] = []
        amounts: List[str] = [value for value in result_set if bool(search(r"[\d]+", value)) == True and bool(search(r"[a-z]+", value)) == False and "/" not in value]
        for index in range(0, len(amounts), 1):
            amount: int = int("".join(findall(r"[\d]+", amounts[index])))
            response.append(amount)
        return response

    def _extractDataDomesticCivilCivilOfficeBearers(self, result_set: List[str]) -> List[Dict[str, Union[str, int]]]:
        """
        Extracting the office bearers of a société civile.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{position: string, name: string, address: string, date_appointed: int}]
        """
        response: List[Dict[str, Union[str, int]]] = []
        start_header: str = "Office Bearers"
        end_header: str = "Associes"
        start_index: int = result_set.index(start_header)
        end_index: int = result_set.index(end_header)
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if start_header not in value]
        result_set = [value for value in result_set if end_header not in value]
        result_set = [value for value in result_set if "Name" not in value]
        result_set = [value for value in result_set if "Service Address" not in value]
        result_set = [value for value in result_set if "Appointed Date" not in value]
        result_set = [value for value in result_set if "Position" not in value]
        result_set = [value for value in result_set if "Office Bearers" not in value]
        result_set = [value for value in result_set if "Associes" not in value]
        date_appointeds: List[str] = self._extractDataDomesticCivilCivilOfficeBearersDateAppointed(result_set)
        result_set = [value for value in result_set if value not in date_appointeds]
        office_bearers_addresses: Dict[str, List[str]] = self._extractDataDomesticCivilCivilOfficeBearersAddresses(result_set)
        result_set = office_bearers_addresses["result_set"]
        addresses: List[str] = office_bearers_addresses["addresses"]
        positions: List[str] = self._extractDataDomesticCivilCivilOfficeBearersPositions(result_set)
        names: List[str] = [value for value in result_set if value not in positions]
        limitation: int = min([len(date_appointeds), len(addresses), len(positions), len(names)])
        for index in range(0, limitation, 1):
            response.append({
                "position": positions[index].title(),
                "name": names[index].title(),
                "address": addresses[index].title(),
                "date_appointment": int(datetime.strptime(date_appointeds[index], "%d/%m/%Y").timestamp())
            })
        return response

    def _extractDataDomesticCivilCivilOfficeBearersPositions(self, result_set: List[str]) -> List[str]:
        """
        Extracting the positions of the office bearers of a société
        civile.

        Parameters:
            result_set: [string]: The result set of the office bearers.

        Returns:
            [string]
        """
        possible_positions: List[str] = self.getOfficeBearer().getPossiblePositions()
        possible_positions.append("GERANT")
        possible_positions = list(set(possible_positions))
        response: List[str] = [value for value in result_set if value in possible_positions]
        return response

    def _extractDataDomesticCivilCivilOfficeBearersAddresses(self, result_set: List[str]) -> Dict[str, List[str]]:
        """
        Extracting the addresses of the office bearers of a société
        civile.

        Parameters:
            result_set: [string]: The result set of the office bearers.

        Returns:
            {result_set: [string], addresses: [string]}
        """
        localities: List[str] = []
        cities: List[str] = []
        response: Dict[str, List[str]]
        addresses: List[str] = []
        for index in range(0, len(result_set), 1):
            locality: str = " ".join(findall(r"[A-Z\s\d,]+", result_set[index]))
            locality = self._extractDataDomesticCivilCivilOfficeBearersAddressesLocality(locality)
            localities = self.__extractDataDomesticCivilCivilOfficeBearersAddressesLocality(localities, locality)
        for index in range(0, len(result_set), 1):
            city: str = " ".join(findall(r"[A-Z,]+", result_set[index]))
            city = self._extractDataDomesticCivilCivilOfficeBearersAddressesCity(city)
            cities = self.__extractDataDomesticCivilCivilOfficeBearersAddressesCity(cities, city)
        for index in range(0, min([len(localities), len(cities)]), 1):
            addresses.append(f"{localities[index]} {cities[index]}")
        result_set = [value for value in result_set if value not in localities]
        result_set = [value for value in result_set if value not in cities]
        result_set = [value for value in result_set if "MAURITIUS" not in value]
        response = {
            "result_set": result_set,
            "addresses": addresses
        }
        return response

    def __extractDataDomesticCivilCivilOfficeBearersAddressesCity(self, cities: List[str], city: str) -> List[str]:
        """
        Building the list of the cities based on the result set.

        Parameters:
            cities: [string]: The data to be returned.
            city: string: The city of the address of the office bearers.

        Returns:
            [string]
        """
        if city != "NaC":
            cities.append(city)
        return cities

    def _extractDataDomesticCivilCivilOfficeBearersAddressesCity(self, city: str) -> str:
        """
        Extracting the city needed for the address of the office
        bearers.

        Parameters:
            city: string: The city of the address.

        Returns:
            string
        """
        if "MAURITIUS" in city:
            return city
        else:
            return "NaC"

    def __extractDataDomesticCivilCivilOfficeBearersAddressesLocality(self, localities: List[str], locality: str) -> List[str]:
        """
        Building the list of the localities based on the result set.

        Parameters:
            localities: [string]: The data to be returned.
            locality: string: The locality of the address of the office bearers.

        Returns:
            [string]
        """
        if locality != "NaL":
            localities.append(locality)
        return localities

    def _extractDataDomesticCivilCivilOfficeBearersAddressesLocality(self, locality: str) -> str:
        """
        Extracting the locality needed for the address of the office
        bearers.

        Parameters:
            locality: string: The locality of the address.

        Returns:
            string
        """
        if bool(search(r"[\d]+", locality)):
            return locality
        else:
            return "NaL"

    def _extractDataDomesticCivilCivilOfficeBearersDateAppointed(self, result_set: List[str]) -> List[str]:
        """
        Extracting the date appointed of the office bearers of a
        société civile.

        Parameters:
            result_set: [string]: The result set of the office bearers.

        Returns:
            [string]
        """
        response: List[str] = []
        dates_appointed: List[str] = [date_appointed for date_appointed in result_set if bool(search(r"[\d]+", date_appointed)) == True and "/" in date_appointed and bool(search(r"[A-z]+", date_appointed)) == False]
        for index in range(0, len(dates_appointed), 1):
            dates: List[str] = dates_appointed[index].split(" ")
            date: str = [date for date in dates if bool(search(r"[0-9]", date)) == True and "/" in date][0] if len(dates) > 1 else dates_appointed[index]
            response.append(date)
        return response

    def _extractDataDomesticCivilCivilStateCapital(self, result_set: List[str]) -> List[Dict[str, Union[str, int]]]:
        """
        Extracting the state capital of a socitété civile.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}]
        """
        response: List[Dict[str, Union[str, int]]] = []
        start_header: str = "Particulars of Stated Capital"
        end_header: str = "Office Bearers"
        start_index: int = result_set.index(start_header) + 1
        end_index: int = result_set.index(end_header)
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if "Type of Shares" not in value]
        result_set = [value for value in result_set if "No. of Shares Currency" not in value]
        result_set = [value for value in result_set if "Stated Capital" not in value]
        result_set = [value for value in result_set if "Amount Unpaid" not in value]
        result_set = [value for value in result_set if "Valeur" not in value]
        result_set = [value for value in result_set if "Nominale" not in value]
        result_set = [value for value in result_set if "Name" not in value]
        result_set = [value for value in result_set if "Service Address" not in value]
        result_set = [value for value in result_set if "Appointed Date" not in value]
        result_set = [value for value in result_set if "Currency" not in value]
        result_set = [value for value in result_set if "Start Date" not in value]
        result_set = [value for value in result_set if "End Date" not in value]
        result_set = [value for value in result_set if "Status" not in value]
        types: List[str] = self._extractDataDomesticCivilCivilStateCapitalTypes(result_set)
        result_set = [value for value in result_set if value not in types]
        amounts: List[int] = self._extractDataDomesticCivilCivilStateCapitalAmount(result_set)
        currencies: List[str] = self._extractDataDomesticCivilCivilStateCapitalCurrency(result_set)
        result_set = [value for value in result_set if value not in currencies]
        stated_capitals: List[int] = self._extractDataDomesticCivilCivilStateCapitalStatedCapital(result_set)
        result_set = [value for value in result_set if value not in str(amounts)]
        amount_unpaids: List[int] = self._extractDataDomesticCivilCivilStateCapitalAmountUnpaid(result_set)
        par_values: List[int] = self._extractDataDomesticCivilCivilStateCapitalParValue(result_set)
        for index in range(0, min([len(types), len(amounts), len(currencies), len(stated_capitals), len(amount_unpaids), len(par_values)]), 1):
            response.append({
                "type": types[index].title(),
                "amount": amounts[index],
                "currency": currencies[index],
                "stated_capital": stated_capitals[index],
                "amount_unpaid": amount_unpaids[index],
                "par_value": par_values[index]
            })
        return response

    def _extractDataDomesticCivilCivilStateCapitalParValue(self, result_set: List[str]) -> List[int]:
        """
        Extracting the share value of the stated capital of an
        authorised company.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [int]
        """
        response: List[int] = []
        for index in range(0, len(result_set), 1):
            share_value: str = " ".join(findall(r"[\d\sA-Z]+", result_set[index]))
            share_value: str = self.__extractDataDomesticCivilCivilStateCapitalParValue(share_value)
            response = self.___extractDataDomesticCivilCivilStateCapitalParValue(response, share_value)
        return response

    def ___extractDataDomesticCivilCivilStateCapitalParValue(self, response: List[int], share_value: str) -> List[int]:
        """
        Building the response needed for the share value of the
        state capital of an authorised company.

        Parameters:
            response: [int]: The data to be returned.
            share_value: string: The value of the share

        Returns:
            [int]
        """
        if share_value != "NaSV":
            response.append(int(share_value))
        return response

    def __extractDataDomesticCivilCivilStateCapitalParValue(self, share_value: str) -> str:
        """
        Sanitizing the share value of the state capital of an
        authorised company.

        Parameters:
            share_value: string: The data to be processed

        Returns:
            string
        """
        if bool(search(r"[A-z]+", share_value)) == False:
            return share_value.split(" ")[-1]
        else:
            return "NaSV"

    def _extractDataDomesticCivilCivilStateCapitalAmountUnpaid(self, result_set: List[str]) -> List[int]:
        """
        Extracting the amount unpaid of the stated capital of an
        authorised company.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [int]
        """
        processed_amount_unpaids: List[str] = []
        amount_unpaids: List[str] = [" ".join(findall(r"[\d\sA-Z]+", amount_unpaid)) for amount_unpaid in result_set]
        for index in range(0, len(amount_unpaids), 1):
            processed_amount_unpaids.append(amount_unpaids[index].split(" ")[0] if bool(search(r"[A-z]+", amount_unpaids[index])) == False else "NaAU")
        amount_unpaids = processed_amount_unpaids
        amount_unpaids = [amount_unpaid for amount_unpaid in amount_unpaids if amount_unpaid != ""]
        response: List[int] = [int(amount_unpaid) for amount_unpaid in amount_unpaids if amount_unpaid != "NaAU"]
        return response

    def _extractDataDomesticCivilCivilStateCapitalStatedCapital(self, result_set: List[str]) -> List[int]:
        """
        Extracting the stated capital of the stated capital of an
        authorised company.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [int]
        """
        stated_capitals: List[str]
        processed_stated_capitals: List[str] = []
        stated_capitals: List[str] = [" ".join(findall(r"[\d\sA-Z]+", state_capital)) for state_capital in result_set]
        for index in range(0, len(stated_capitals), 1):
            processed_stated_capitals.append(stated_capitals[index] if bool(search(r"[\s]", stated_capitals[index])) == False else "NaSC")
        stated_capitals = processed_stated_capitals
        processed_stated_capitals = []
        for index in range(0, len(stated_capitals), 1):
            processed_stated_capitals.append(stated_capitals[index] if bool(search(r"[A-Z]", stated_capitals[index])) == False else "NaSC")
        stated_capitals = processed_stated_capitals
        response: List[int] = [int(stated_capital) for stated_capital in stated_capitals if stated_capital != "NaSC"]
        return response

    def _extractDataDomesticCivilCivilStateCapitalTypes(self, result_set: List[str]) -> List[str]:
        """
        Extracting the types from the state capital of a société
        civile.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [string]
        """
        result_set = [value for value in result_set if bool(search(r"[A-Z]+", value)) == True]
        result_set = [value for value in result_set if bool(search(r"[\d]", value)) == False]
        response: List[str] = [value for value in result_set if bool(search(r"[a-z]+", value)) == False]
        return response

    def _extractDataDomesticCivilCivilStateCapitalCurrency(self, result_set: List[str]) -> List[str]:
        """
        Extracting the currencies of the shares of the stated
        capital of a société civile.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [str]
        """
        response: List[str] = []
        for index in range(0, len(result_set), 1):
            currencies: str = " ".join(findall(r"[\d\sA-z]+", result_set[index]))
            currency: str = self.__extractDataDomesticCivilCivilStateCapitalCurrency(currencies)
            response = self.___extractDataDomesticCivilCivilStateCapitalCurrency(response, currency)
        return response

    def ___extractDataDomesticCivilCivilStateCapitalCurrency(self, response: List[str], currency: str) -> List[str]:
        """
        Building the array which contains the currencies of shares
        of the stated capital for a société civile.

        Parameters:
            response: [string]: The array to be returned.
            currency: string: The currency to be processed.

        Returns:
            [string]
        """
        if currency != "NaC":
            response.append(currency)
        return response

    def __extractDataDomesticCivilCivilStateCapitalCurrency(self, currencies: str) -> str:
        """
        Extracting the correct currency to be used for the
        processing.

        Parameters:
            currencies: string: THe value to be processed.

        Returns:
            string
        """
        if bool(search(r"[\d]+", currencies)) and bool(search(r"[A-z\s]+", currencies)) and bool(search(r"[A-z]+", currencies)):
            return " ".join(findall(r"[A-z]+", currencies))
        else:
            return "NaC"

    def _extractDataDomesticCivilCivilStateCapitalAmount(self, result_set: List[str]) -> List[int]:
        """
        Extracting the amount of shares of the stated capital of a
        société civile.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [int]
        """
        result_set = [value for value in result_set if bool(search(r"[\d\sA-z]+", value)) == True]
        result_set = [value for value in result_set if "/" not in value]
        result_set = [value for value in result_set if bool(search(r"[\d]+", value)) == True]
        result_set = [value for value in result_set if bool(search(r"[a-z]+", value)) == True]
        result_set = [value for value in result_set if "Page" not in value]
        result_set = [value for value in result_set if "of" not in value]
        response: List[int] = [int(value.split(" ")[0]) for value in result_set if bool(search(r"[\d]+", value)) == True]
        return response

    def _extractDataDomesticCivilCivilBusinessDetails(self, result_set: List[str]) -> Union[List[Dict[str, str]], Dict[str, str]]:
        """
        Extracting the business details of société civile.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{registered_address: string, name: string, nature: string, operational: string}] | {registered_address: string, name: string, nature: string, operational: string}
        """
        response: Union[List[Dict[str, str]], Dict[str, str]] = []
        registered_address: str = result_set[[index for index, value in enumerate(result_set) if "Siege Social Address:" in value][0]].split(": ")[-1]
        start_index: int = result_set.index("Business Details") + 1
        end_index: int = result_set.index("Particulars of Stated Capital")
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if ":" not in value]
        result_set = [value for value in result_set if "Business" not in value]
        if len(result_set) > 0:
            self.getLogger().error(f"The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader._extractDataDomesticCivilCivilBusinessDetails()\nAmount of Data: {len(result_set)}")
            exit()
        else:
            response = {
                "registered_address": registered_address.title()
            }
        return response

    def _extractDataDomesticCivilCivilCompanyDetails(self, result_set: List[str]) -> Dict[str, Union[str, int, None]]:
        """
        Extracting the company details of a société civile.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}
        """
        response: Dict[str, Union[str, int, None]]
        start_header: str = "Partnership Details"
        end_header: str = "Business Details"
        start_index: int = result_set.index(start_header)
        end_index: int = result_set.index(end_header)
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if start_header not in value]
        result_set = [value for value in result_set if end_header not in value]
        result_set = [value for value in result_set if "Registrar of Companies" not in value]
        category: str = result_set[[index for index, value in enumerate(result_set) if "Category" in value][0]].split(": ")[-1]
        result_set = [value for value in result_set if ":" not in value]
        file_number: str = [value for value in result_set if bool(search(r"[A-Z]+", value)) == True and bool(search(r"[0-9]+", value)) == True][0]
        result_set = [value for value in result_set if file_number not in value]
        if len(result_set) == 1:
            response = {
                "name": result_set[0].title(),
                "file_number": file_number,
                "category": None,
                "date_incorporation": int(time()),
                "nature": None,
                "status": None
            }
            return response
        response = {
            "name": result_set[0].title(),
            "file_number": file_number,
            "category": category.title(),
            "date_incorporation": int(datetime.strptime(result_set[1], "%d/%m/%Y").timestamp()) if "/" in result_set[1] else int(time()),
            "nature": result_set[2].title(),
            "status": result_set[3].title()
        }
        return response

    def extractDataDomesticCivilBusinessRegistrationNumber(self, result_set: List[str]) -> Union[str, None]:
        """
        Extracting the business registration number of a domestic
        civil company.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            string | null
        """
        business_registration_numbers: List[str] = findall(r"\b[A-Z][0-9]+\b", result_set[[index for index, value in enumerate(result_set) if "Business Registration No" in value][0]])
        if len(business_registration_numbers) == 1:
            return business_registration_numbers[0]
        else:
            return None

    def extractDataDomesticPrivate(self, status: int, dataset: DocumentFiles) -> Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]]:
        """
        Extracting the data from the portable document file version
        of the corporate registry based on the status of the file
        generation as well as on the dataset for a domestic company
        which is also a private company.

        Parameters:
            status: int: The status of the file generation.
            dataset: {identifier: int, file_data: bytes, company_detail: int}: The dataset of the corporate registry retrieved from the relational database server.

        Returns:
            {status: int, company_details: {business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}, business_details: [{registered_address: string, name: string, nature: string, operational: string}], certificates: [{certificate: string, type: str, date_effective: int, date_expiry: int}], office_bearers: [{position: string, name: string, address: string, date_appointment: int}], shareholders: [{name: string, amount: int, type: string, currency: string}], members: [{name: string, amount: int, date_start: int, currency: string}], annual_return: [{date_annual_return: int, date_annual_meeting: int, date_filled: int}], financial_summaries: [{financial_year: int, currency: string, date_approved: int, unit: int}], profit_statement: {financial_summary: {financial_year: int, currency: string, date_approved: int, unit: int}, turnover: float, cost_of_sales: float, gross_profit: float, other_income: float, distribution_cost: float, administration_cost: float, expenses: float, finance_cost: float, net_profit_before_taxation: float, taxation: float, net_profit: float}, state_capital: {type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}, balance_sheet: {balance_sheet: {financial_year: int, currency: string, unit: int}, assets: {non_current_assets: {property_plant_equipment: float, investment_properties: float, intangible_assets: float, other_investments: float, subsidiaries_investments: float, biological_assets: float, others: float, total: float}, current_assets: {inventories: float, trade: float, cash: float, others: float, total: float}, total: float}, liabilities: {equity_and_liabilities: {share_capital: float, other_reserves: float, retained_earnings: float, others: float, total: float}, non_current: {long_term_borrowings: float, deferred_tax: float, long_term_provisions: float, others: float, total: float}, current: {trade: float, short_term_borrowings: float, current_tax_payable: float, short_term_provisions: float, others: float, total: float}, total_liabilities: float, total_equity_and_liabilities: float}}, charges: [{volume: int, property: string, nature: string, amount: int, date_charged: int, date_filled: int, currency: string}], liquidators: {liquidator: {name: string, appointed_date: int, address: string}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}, receivers: {receiver: {name: string, date_appointed: int, address: string}, reports: [{date_filled: int, date_from: int, date_to: int}], affidavits: [{date_filled: int, date_from: int, date_to: int}]}, administrators: {administrator: {name: string, date_appointed: int, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}, details: [{type: string, date_start: int, date_end: int, status: string}], objections: [{date_objection: int, objector: string}]}
        """
        response: Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]]
        file_name: str = f"{self.ENV.getDirectory()}Cache/CorporateDocumentFile/Documents/{dataset.company_detail}.pdf"
        cache_data_file_name: str = f"{self.ENV.getDirectory()}Cache/CorporateDocumentFile/Metadata/{dataset.company_detail}.json"
        if status != 201:
            status = 404
            self.getLogger().error(f"The portable document file has not been generated correctly!  The application will abort the extraction.\nStatus: {status}\nFile Location: {file_name}\nDocument File Identifier: {dataset.identifier}\nCompany Detail Identifier: {dataset.company_detail}")
            return {
                "status": status
            }
        try:
            portable_document_file_data: str = extract_text(file_name)
            cache_file = open(cache_data_file_name, "w")
            portable_document_file_data_result_set: List[str] = list(filter(None, portable_document_file_data.split("\n")))
            company_details: Dict[str, Union[str, int]] = self.extractCompanyDetails(portable_document_file_data_result_set)
            business_details: List[Dict[str, str]] = self.extractBusinessDetails(portable_document_file_data_result_set)
            certificates: List[Dict[str, Union[str, int]]] = self.extractCertificates(portable_document_file_data_result_set)
            office_bearers: List[Dict[str, Union[str, int]]] = self.extractOfficeBearers(portable_document_file_data_result_set)
            shareholders: List[Dict[str, Union[str, int]]] = self.extractShareholders(portable_document_file_data_result_set)
            members: List[Dict[str, Union[str, int]]] = self.extractMembers(portable_document_file_data_result_set)
            annual_return: List[Dict[str, int]] = self.extractAnnualReturns(portable_document_file_data_result_set)
            financial_summaries: List[Dict[str, Union[int, str]]] = self.extractFinancialSummaries(portable_document_file_data_result_set)
            profit_statement: Dict[str, Union[Dict[str, Union[int, str]], float]] = self.extractProfitStatements(portable_document_file_data_result_set)
            state_capital: List[Dict[str, Union[str, int, float]]] = self.extractStateCapital(portable_document_file_data_result_set)
            balance_sheet: Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]] = self.extractBalanceSheet(portable_document_file_data_result_set)
            charges: List[Dict[str, Union[int, str]]] = self.extractCharges(portable_document_file_data_result_set)
            liquidators: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]] = self.extractLiquidators(portable_document_file_data_result_set)
            receivers: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]] = self.extractReceivers(portable_document_file_data_result_set)
            administrators: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]] = self.extractAdministrators(portable_document_file_data_result_set)
            details: List[Dict[str, Union[str, int, None]]] = self.extractDetails(portable_document_file_data_result_set)
            objections: List[Dict[str, Union[int, str]]] = self.extractObjections(portable_document_file_data_result_set)
            status = 200
            response = {
                "status": status,
                "company_details": company_details,
                "business_details": business_details,
                "certificates": certificates,
                "office_bearers": office_bearers,
                "shareholders": shareholders,
                "members": members,
                "annual_return": annual_return,
                "financial_summaries": financial_summaries,
                "profit_statement": profit_statement,
                "state_capital": state_capital, # type: ignore
                "balance_sheet": balance_sheet,
                "charges": charges,
                "liquidators": liquidators,
                "receivers": receivers,
                "administrators": administrators,
                "details": details,
                "objections": objections
            }
            cache_file.write(dumps(response, indent=4))
            cache_file.close()
            self.getLogger().inform(f"Data has been extracted from the portable document file version of the corporate registry.\nStatus: {response['status']}\nDocument File Identifier: {dataset.identifier}\nFile Location: {file_name}\nCompany Details Identifier: {dataset.company_detail}")
            return response
        except PDFSyntaxError as error:
            status = self.getCompanyDetails().invalidateCompany(dataset.company_detail)
            status = self.getDocumentFiles().deleteDocumentFile(dataset.company_detail) if status == 202 else status
            remove(file_name) if status == 204 else None
            status = 403 if status == 204 else status
            self.getLogger().error(f"Data cannot be extracted due to an error in the file type.\nStatus: {status}\nDocument File Identifier: {dataset.identifier}\nFile Location: {file_name}\nCompany Details Identifier: {dataset.company_detail}\nError: {error}")
            return {
                "status": status
            }

    def extractObjections(self, portable_document_file_result_set: List[str]) -> List[Dict[str, Union[int, str]]]:
        """
        Extracting the objections from the result set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{date_objection: int, objector: string}]
        """
        response: List[Dict[str, Union[int, str]]] = []
        start_index: int = portable_document_file_result_set.index("Objections")
        end_index: int = next((index for index, value in enumerate(portable_document_file_result_set) if value.startswith("Last Annual Registration Fee Paid:")), len(portable_document_file_result_set))
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        result_set = [value for value in result_set if "Object" not in value]
        if len(result_set) < 2:
            return response
        for index in range(0, len(result_set), 2):
            response.append({
                "date_objection": int(datetime.strptime(result_set[index], "%d/%m/%Y").timestamp()),
                "objector": str(result_set[index + 1]).capitalize()
            })
        return response

    def extractDetails(self, portable_document_file_result_set: List[str]) -> List[Dict[str, Union[str, int, None]]]:
        """
        Extracting the details of a private domestic company from
        the result set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{type: string, date_start: int, date_end: int, status: string}]
        """
        response: List[Dict[str, Union[str, int, None]]] = []
        start_header: str = "Winding Up Details"
        end_header: str = "Objections"
        start_index: int = portable_document_file_result_set.index(start_header)
        end_index: int = portable_document_file_result_set.index(end_header)
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        result_set = [value for value in result_set if start_header not in value]
        result_set = [value for value in result_set if end_header not in value]
        result_set = [value for value in result_set if "Object" not in value]
        result_set = [value for value in result_set if ":" not in value]
        result_set = [value for value in result_set if "Type" not in value]
        result_set = [value for value in result_set if "Start Date" not in value]
        result_set = [value for value in result_set if "End Date" not in value]
        result_set = [value for value in result_set if "Status" not in value]
        if len(result_set) < 3:
            return response
        if len(result_set) == 3:
            response.append({
                "type": result_set[0].capitalize(),
                "date_start": int(datetime.strptime(result_set[1], "%d/%m/%Y").timestamp()),
                "date_end": None,
                "status": result_set[2].capitalize()
            })
            return response
        for index in range(0, len(result_set), 4):
            is_inbounds: bool = True if index + 3 < len(result_set) else False
            response.append({
                "type": result_set[index].capitalize() if is_inbounds else "",
                "date_start": int(datetime.strptime(result_set[index + 1], "%d/%m/%Y").timestamp()) if is_inbounds else 0,
                "date_end": int(datetime.strptime(result_set[index + 2], "%d/%m/%Y").timestamp()) if is_inbounds else 0,
                "status": result_set[index + 3].capitalize() if is_inbounds else ""
            })
        response = [detail for detail in response if detail["date_start"] != 0]
        return response

    def extractAdministrators(self, portable_document_file_result_set: List[str]) -> Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]:
        """
        Extracting the administrators from the result set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {administrator: {name: string, date_appointed: int, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}
        """
        start_header: str = "Administrators"
        end_header: str = "Page 6"
        response: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]] = {}
        if start_header not in portable_document_file_result_set:
            return response
        start_index: int = portable_document_file_result_set.index(start_header)
        end_index: int = portable_document_file_result_set.index(end_header)
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        administrator: Dict[str, Union[str, int]] = self._extractAdministrators(result_set)
        accounts: List[Dict[str, int]] = self.extractAdministratorsAccounts(result_set)
        if not administrator and len(accounts) == 0:
            return response
        self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractAdministrators()")
        exit()

    def extractAdministratorsAccounts(self, result_set: List[str]) -> List[Dict[str, int]]:
        """
        Extracting the accounts of the administrators.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{date_filled: int, date_from: int, date_to: int}]
        """
        start_index: int = result_set.index("Date Filed")
        end_index: int = result_set.index("Winding Up Details")
        result_set = result_set[start_index:end_index]
        result_set.remove("Date Filed")
        result_set.remove("From")
        result_set.remove("To")
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractAdministratorsAccounts()")
            exit()
        else:
            return []

    def _extractAdministrators(self, result_set: List[str]) -> Dict[str, Union[str, int]]:
        """
        Extracting the administrator that is linked to the
        administrators.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {name: string, date_appointed: int, designation: string, address: string}
        """
        start_index: int = result_set.index("Name:")
        end_index: int = result_set.index("Start Date")
        result_set = result_set[start_index:end_index]
        date_appointeds: List[str] = [value for value in result_set if "Appointed Date" in value]
        start_index = result_set.index("Name:")
        end_index = result_set.index("To")
        result_set = result_set[start_index:end_index]
        date_appointeds = [date_appointeds[0]]
        result_set = result_set + date_appointeds
        result_set = [value for value in result_set if ":" not in value]
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader._extractAdministrators()")
            exit()
        else:
            return {}

    def extractReceivers(self, portable_document_file_result_set: List[str]) -> Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]:
        """
        Extracting the receivers from the result set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {receiver: {name: string, date_appointed: int, address: string}, reports: [{date_filled: int, date_from: int, date_to: int}], affidavits: [{date_filled: int, date_from: int, date_to: int}]}
        """
        start_header: str = "Receivers"
        end_header: str = "Accounts of Administrator"
        response: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]] = {}
        if start_header not in portable_document_file_result_set:
            return response
        start_index: int = portable_document_file_result_set.index(start_header)
        end_index: int = portable_document_file_result_set.index(end_header) + 1
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        receiver: Dict[str, Union[str, int]] = self._extractReceivers(result_set)
        reports: List[Dict[str, int]] = self.extractReceiversReports(result_set)
        affidavits: List[Dict[str, int]] = self.extractReceiversAffidavits(result_set)
        if not receiver and len(reports) == 0 and len(affidavits) == 0:
            return response
        self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractReceivers()")
        exit()

    def extractReceiversAffidavits(self, result_set: List[str]) -> List[Dict[str, int]]:
        """
        Extracting the affidavits that are related to the receivers.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{date_filled: int, date_from: int, date_to: int}]
        """
        start_index: int = result_set.index("Affidavits of Receiver")
        end_index: int = result_set.index("Accounts of Administrator")
        result_set = result_set[start_index:end_index]
        start_index = result_set.index("To")
        end_index = result_set.index("To") + 3
        date_to: List[str] = result_set[start_index:end_index]
        start_index = int(len(date_to) / 2)
        date_to = date_to[start_index:]
        date_to = [value for value in date_to if ":" not in value]
        start_index: int = result_set.index("Affidavits of Receiver") + 1
        end_index: int = result_set.index("Administrators")
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if "Appointed" not in value]
        result_set = [value for value in result_set if "Page" not in value]
        result_set = [value for value in result_set if " of " not in value]
        result_set = [value for value in result_set if "Date Issued" not in value]
        result_set = result_set + date_to
        result_set = [value for value in result_set if "Date Filed" not in value]
        result_set = [value for value in result_set if "From" not in value]
        result_set = [value for value in result_set if "To" not in value]
        if len(result_set) >= 3:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractReceiversAffidavits()")
            exit()
        else:
            return []

    def extractReceiversReports(self, result_set: List[str]) -> List[Dict[str, int]]:
        """
        Extracting the reports that are related to the receivers.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{date_filled: int, date_from: int, date_to: int}]
        """
        start_index: int = result_set.index("Date Filed")
        end_index: int = result_set.index("Accounts of Administrator")
        result_set = result_set[start_index:end_index]
        start_index = result_set.index("To")
        end_index = result_set.index("To") + 3
        date_to: List[str] = result_set[start_index:end_index]
        end_index = int(len(date_to) / 2)
        date_to = date_to[0:end_index]
        start_index = result_set.index("Date Filed")
        end_index = result_set.index("Affidavits of Receiver")
        result_set = result_set[start_index:end_index]
        result_set = result_set + date_to
        result_set.remove("Date Filed")
        result_set.remove("From")
        result_set.remove("To")
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractReceiversReports()")
            exit()
        else:
            return []

    def _extractReceivers(self, result_set: List[str]) -> Dict[str, Union[str, int]]:
        """
        Extracting the receiver that is related to the receivers.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {name: string, date_appointed: int, address: string}
        """
        start_index: int = result_set.index("Receivers") + 1
        end_index: int = result_set.index("From")
        result_set = result_set[start_index:end_index]
        result_set.remove("Name:")
        result_set.remove("Address:")
        result_set.remove("Reports of Receiver")
        result_set.remove("Date Filed")
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader._extractReceivers()")
            exit()
        else:
            return {}

    def extractLiquidators(self, portable_document_file_result_set: List[str]) -> Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]:
        """
        Extracting the liquidators from the result set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {liquidator: {name: string, appointed_date: int, address: string}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}
        """
        start_header: str = "Liquidators"
        end_header: str = "Receivers"
        response: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]] = {}
        if start_header not in portable_document_file_result_set:
            return response
        start_index: int = portable_document_file_result_set.index(start_header)
        end_index: int = portable_document_file_result_set.index(end_header)
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        start_index = portable_document_file_result_set.index("Appointed Date:")
        end_index = start_index + 6
        date_appointeds = [value for value in portable_document_file_result_set[start_index:end_index] if "Appointed Date:" in value or "/" in value]
        start_index = int(len(date_appointeds) * (2 / 3)) - 1
        end_index = int(len(date_appointeds) / 3) + start_index
        date_appointeds = date_appointeds[start_index:end_index]
        start_index = result_set.index(start_header)
        end_index = result_set.index("Affidavits of Liquidator") + 1
        liquidator_dataset: List[str] = result_set[start_index:end_index] + date_appointeds
        liquidator: Dict[str, Union[str, int]] = self._extractLiquidators(liquidator_dataset)
        affidavits: List[Dict[str, int]] = self.extractLiquidatorsAffidavits(result_set)
        if not liquidator and len(affidavits) == 0:
            return response
        self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractLiquidators()")
        exit()

    def extractLiquidatorsAffidavits(self, result_set: List[str]) -> List[Dict[str, int]]:
        """
        Extracting the affidavits that is related to the
        liquidators.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{date_filled: int, date_from: int, date_to: int}]
        """
        start_index: int = result_set.index("Affidavits of Liquidator") + 1
        result_set = result_set[start_index:]
        result_set = [value for value in result_set if "Affidavits of Liquidator" not in value]
        result_set = [value for value in result_set if "Date Filed" not in value]
        result_set = [value for value in result_set if "From" not in value]
        result_set = [value for value in result_set if "To" not in value]
        result_set = [value for value in result_set if "Appointed Date:" not in value]
        result_set = [value for value in result_set if "Receivers" not in value]
        result_set = [value for value in result_set if "Page" not in value]
        result_set = [value for value in result_set if " of " not in value]
        result_set = [value for value in result_set if ":" not in value]
        result_set = [value for value in result_set if "/" in value]
        if len(result_set) <= 3:
            return []
        self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractLiquidatorsAffidavits()")
        exit()

    def _extractLiquidators(self, result_set: List[str]) -> Dict[str, Union[str, int]]:
        """
        Extracting the liquidator that is related to the
        liquidators.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {name: string, date_appointed: int, address: string}
        """
        start_index: int = result_set.index("Appointed Date:") if "Appointed Date:" in result_set else 0
        end_index: int = start_index + 2 if start_index != 0 else len(result_set) - 1
        date_appointeds: List[str] = [value for value in result_set[start_index:end_index] if "/" in value]
        start_index: int = result_set.index("Liquidators") + 1
        end_index: int = result_set.index("Affidavits of Liquidator")
        dataset = result_set[start_index:end_index]
        dataset = [value for value in dataset if bool(search(r"[0-9]", value)) == False]
        dataset = [value for value in dataset if ":" not in value]
        dataset = [value for value in dataset if "Name" not in value]
        dataset = [value for value in dataset if "Service Address" not in value]
        dataset = [value for value in dataset if "Appointed Date" not in value]
        dataset = [value for value in dataset if "No. of Shares Type of Shares" not in value]
        dataset = [value for value in dataset if "Currency" not in value]
        dataset = [value for value in dataset if "Mauritius Rupee" not in value]
        if len(dataset) <= 2 or len(date_appointeds) == 0:
            return {}
        self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader._extractLiquidators()")
        exit()


    def extractCharges(self, portable_document_file_result_set: List[str]) -> List[Dict[str, Union[int, str]]]:
        """
        Extracting the charges from the result set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{volume: int, property: string, nature: string, amount: int, date_charged: int, date_filled: int, currency: string}]
        """
        start_header: str = "Charges"
        end_header: str = "Liquidators" if "Liquidators" in portable_document_file_result_set else "Winding Up Details"
        response: List[Dict[str, Union[int, str]]] = []
        start_index: int = portable_document_file_result_set.index(start_header)
        end_index: int = portable_document_file_result_set.index(end_header) if end_header in portable_document_file_result_set else len(portable_document_file_result_set)
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        result_set = [value for value in result_set if "Winding Up Details" not in value]
        result_set = [value for value in result_set if "Type" not in value]
        result_set = [value for value in result_set if "Objections" not in value]
        result_set = [value for value in result_set if "Objection Date" not in value]
        result_set = [value for value in result_set if "Objector" not in value]
        result_set = [value for value in result_set if ":" not in value]
        result_set = [value for value in result_set if "Start Date" not in value]
        result_set = [value for value in result_set if "End Date" not in value]
        result_set = [value for value in result_set if "Status" not in value]
        result_set = [value for value in result_set if "Computer Generated Document" not in value]
        result_set = [value for value in result_set if "DISCLAIMER NOTICE" not in value]
        result_set = [value for value in result_set if "While we endeavour to keep the information up to date and as far as possible accurate, we cannot give any guarantee about the completeness, accuracy," not in value]
        result_set = [value for value in result_set if "reliability of the information contained on the report." not in value]
        result_set = [value for value in result_set if "Page" not in value]
        result_set = [value for value in result_set if "of" not in value]
        result_set = [value for value in result_set if "\x0c" not in value]
        result_set = [value for value in result_set if "Charges" not in value]
        result_set = [value for value in result_set if "Volume" not in value]
        result_set = [value for value in result_set if "Property" not in value]
        result_set = [value for value in result_set if "Nature" not in value]
        result_set = [value for value in result_set if "Amount Date Charged" not in value]
        result_set = [value for value in result_set if "Amount" not in value]
        result_set = [value for value in result_set if "Date Charged" not in value]
        result_set = [value for value in result_set if "Date Filed" not in value]
        result_set = [value for value in result_set if "Currency" not in value]
        if len(result_set) == 0:
            return response
        processed_volume: Dict[str, List[str]] = self.extractChargesVolumes(result_set)
        volumes: List[str] = processed_volume["volumes"]
        result_set = processed_volume["result_set"]
        result_set = " ".join(result_set).split(" ")
        processed_date: Dict[str, List[str]] = self.extractChargesDates(result_set)
        dates_charged: List[str] = processed_date["dates_charged"]
        dates_filled: List[str] = processed_date["dates_filled"]
        result_set: List[str] = processed_date["result_set"]
        amounts: List[int] = [int(value.replace(",", "")) for value in result_set if bool(search(r"[0-9]+", value)) == True]
        result_set = [value for value in result_set if bool(search(r"[0-9]+", value)) == False]
        natures: List[str] = [value for value in result_set if bool(search(r"[A-Z]+", value)) == True and bool(search(r"[a-z]+", value)) == False]
        result_set = [value for value in result_set if value not in natures]
        result_set = self.extractChargesProcessedResultSet(result_set)
        properties: List[str] = self.extractChargesProperties(result_set)
        result_set = [value for value in result_set if value not in properties]
        currencies: List[str] = self.extractChargesCurrencies(result_set, len(properties))
        limitation: int = min(len(volumes), len(dates_charged), len(dates_filled), len(amounts), len(natures), len(properties), len(currencies))
        for index in range(0, limitation, 1):
            response.append({
                "volume": volumes[index],
                "property": properties[index],
                "nature": natures[index].title(),
                "amount": amounts[index],
                "date_charged": int(datetime.strptime(dates_charged[index], "%d/%m/%Y").timestamp()),
                "date_filled": int(datetime.strptime(dates_filled[index], "%d/%m/%Y").timestamp()),
                "currency": currencies[index]
            })
        return response

    def extractChargesCurrencies(self, result_set: List[str], properties_amount: int) -> List[str]:
        """
        Extracting the currencies of the charges.

        Parameters:
            result_set: [string]: The dataset
            properties_amount: int: The amount of properties.

        Returns:
            [string]
        """
        currencies: List[str] = []
        for index in range(0, properties_amount, 1):
            currencies.append(result_set[index]) if len(result_set) > 0 else currencies.append("")
        currencies = [currency for currency in currencies if currency != ""]
        return currencies

    def extractChargesProperties(self, result_set: List[str]) -> List[str]:
        """
        Extracting the properties of the charges.

        Parameters:
            result_set: [string]: The dataset

        Returns:
            [string]
        """
        properties: List[str] = []
        for index in range(0, len(result_set), 1):
            properties = self._extractChargesProperties(properties, result_set[index])
        return properties

    def extractChargesProcessedResultSet(self, result_set: List[str]) -> List[str]:
        """
        Sanitizing the result set for better processing.

        Parameters:
            result_set: [string]: The dataset

        Returns:
            [string]
        """
        processed_result_set: List[str] = []
        for index, value in enumerate(result_set):
            processed_result_set.append(value) if index == 0 or "Mauritius" in value or "Rupee" in value else processed_result_set.append(value.lower())
        result_set = processed_result_set
        data: str = " ".join(result_set)
        result_set = split(r'\s(?=[A-Z])', data)
        return result_set

    def extractChargesDates(self, result_set: List[str]) -> Dict[str, List[str]]:
        """
        Extracting the dates for the charges.

        Parameters:
            result_set: [string]: The dataset

        Returns:
            {dates_charged: [string], dates_filled: [string], result_set: [string]}
        """
        dates: List[str] = [value for value in result_set if bool(search(r"[0-9]+", value)) == True and "/" in value]
        result_set = [value for value in result_set if value not in dates]
        dates_charged: List[str] = []
        dates_filled: List[str] = []
        for index in range(0, len(dates), 2):
            dates_charged.append(dates[index])
            dates_filled.append(dates[index + 1])
        return {
            "dates_charged": dates_charged,
            "dates_filled": dates_filled,
            "result_set": result_set
        }

    def extractChargesVolumes(self, result_set: List[str]) -> Dict[str, List[str]]:
        """
        Extracting the volumes for the charges.

        Parameters:
            result_set: [string]: The dataset

        Returns:
            {volumes: [string], result_set: [string]}
        """
        volumes: List[str] = []
        volume_first_part: List[str] = [value for value in result_set if bool(search(r"[0-9]+", value)) == True and "/" in value and bool(search(r"[A-Z]+", value)) == True]
        result_set = [value for value in result_set if value not in volume_first_part]
        volume_second_part: List[str] = [value for value in result_set if bool(search(r"[0-9]+", value)) == True and "/" not in value]
        result_set = [value for value in result_set if value not in volume_second_part]
        volumes_limitation: int = min(len(volume_first_part), len(volume_second_part))
        for index in range(0, volumes_limitation, 1):
            volumes.append(f"{volume_first_part[index]}{volume_second_part[index]}")
        return {
            "volumes": volumes,
            "result_set": result_set
        }

    def _extractChargesProperties(self, properties: List[str], property: str) -> List[str]:
        """
        Extracting the properties for the charges.

        Parameters:
            properties: [string]: The list of the properties.
            property: string: The property.

        Returns:
            [string]
        """
        if len(split(r"\s", property)) > 1:
            properties.append(property)
        return properties

    def extractBalanceSheet(self, portable_document_file_result_set: List[str]) -> Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]]:
        """
        Extracting the data for the balance sheets from the result
        set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {balance_sheet: {financial_year: int, currency: string, unit: int}, assets: {non_current_assets: {property_plant_equipment: float, investment_properties: float, intangible_assets: float, other_investments: float, subsidiaries_investments: float, biological_assets: float, others: float, total: float}, current_assets: {inventories: float, trade: float, cash: float, others: float, total: float}, total: float}, liabilities: {equity_and_liabilities: {share_capital: float, other_reserves: float, retained_earnings: float, others: float, total: float}, non_current: {long_term_borrowings: float, deferred_tax: float, long_term_provisions: float, others: float, total: float}, current: {trade: float, short_term_borrowings: float, current_tax_payable: float, short_term_provisions: float, others: float, total: float}, total_liabilities: float, total_equity_and_liabilities: float}}
        """
        start_header: str = "BALANCE SHEET"
        end_header: str = "Charges"
        start_index: int = portable_document_file_result_set.index(start_header)
        end_index: int = portable_document_file_result_set.index(end_header)
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        balance_sheet: Dict[str, Union[int, str]] = self._extractBalanceSheet(result_set)
        assets: Dict[str, Union[Dict[str, float], float]] = self.extractBalanceSheetAssets(result_set)
        liabilities: Dict[str, Union[Dict[str, float], float]] = self.extractBalanceSheetLiabilities(result_set)
        if not balance_sheet and not assets and not liabilities:
            return {}
        return {
            "balance_sheet": balance_sheet,
            "assets": assets,
            "liabilities": liabilities
        }

    def extractBalanceSheetLiabilities(self, result_set: List[str]) -> Dict[str, Union[Dict[str, float], float]]:
        """
        Extracting the liabilities that is linked to the balance
        sheet.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {equity_and_liabilities: {share_capital: float, other_reserves: float, retained_earnings: float, others: float, total: float}, non_current: {long_term_borrowings: float, deferred_tax: float, long_term_provisions: float, others: float, total: float}, current: {trade: float, short_term_borrowings: float, current_tax_payable: float, short_term_provisions: float, others: float, total: float}, total_liabilities: float, total_equity_and_liabilities: float}
        """
        start_header: str = "EQUITY AND LIABILITIES"
        start_index: int = result_set.index(start_header)
        result_set = result_set[start_index:]
        equity: Dict[str, float] = self.extractBalanceSheetLiabilitiesEquity(result_set)
        non_current: Dict[str, float] = self.extractBalanceSheetLiabilitiesNonCurrent(result_set)
        current: Dict[str, float] = self.extractBalanceSheetLiabilitiesCurrent(result_set)
        if not equity and not non_current and not current:
            return {}
        result_set = [value for value in result_set if bool(search(r"[A-z]+", value)) == False]
        result_set = [value for value in result_set if "/" not in value]
        data: List[float] = [float(data.replace(",", "")) for data in result_set][-2:]
        total_liabilities: float = data[0]
        total_equity_and_liabilities: float = data[1]
        return {
            "equity_and_liabilities": equity,
            "non_current": non_current,
            "current": current,
            "total_liabilities": total_liabilities,
            "total_equity_and_liabilities": total_equity_and_liabilities
        }

    def extractBalanceSheetLiabilitiesCurrent(self, result_set: List[str]) -> Dict[str, float]:
        """
        Extracting the current liabilities that is linked to the
        liabilities.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {trade: float, short_term_borrowings: float, current_tax_payable: float, short_term_provisions: float, others: float, total: float}
        """
        result_set = [value for value in result_set if bool(search(r"[A-z]+", value)) == False]
        result_set = [value for value in result_set if "/" not in value]
        start_index: int = 10
        end_index: int = start_index + 6
        if len(result_set) == 0:
            return {}
        data: List[float] = [float(data.replace(",", "")) for data in result_set][start_index:end_index]
        return {
            "trade": data[0],
            "short_term_borrowings": data[1],
            "current_tax_payable": data[2],
            "short_term_provisions": data[3],
            "others": data[4],
            "total": data[5]
        }

    def extractBalanceSheetLiabilitiesNonCurrent(self, result_set: List[str]) -> Dict[str, float]:
        """
        Extracting the non-current liabilities that is linked to the
        liabilities.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {long_term_borrowings: float, deferred_tax: float, long_term_provisions: float, others: float, total: float}
        """
        result_set = [value for value in result_set if bool(search(r"[A-z]+", value)) == False]
        result_set = [value for value in result_set if "/" not in value]
        start_index: int = 5
        end_index: int = start_index + 5
        if len(result_set) == 0:
            return {}
        data: List[float] = [float(data.replace(",", "")) for data in result_set][start_index:end_index]
        return {
            "long_term_borrowings": data[0],
            "deferred_tax": data[1],
            "long_term_provisions": data[2],
            "others": data[3],
            "total": data[4]
        }

    def extractBalanceSheetLiabilitiesEquity(self, result_set: List[str]) -> Dict[str, float]:
        """
        Extracting the equities that is linked to the liabilities.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {share_capital: float, other_reserves: float, retained_earnings: float, others: float, total: float}
        """
        end_index: int = 5
        result_set = [value for value in result_set if bool(search(r"[A-z]+", value)) == False]
        result_set = [value for value in result_set if "/" not in value]
        if len(result_set) == 0:
            return {}
        data: List[float] = [float(data.replace(",", "")) for data in result_set][:end_index]
        return {
            "share_capital": data[0],
            "other_reserves": data[1],
            "retained_earnings": data[2],
            "others": data[3],
            "total": data[4]
        }

    def extractBalanceSheetAssets(self, result_set: List[str]) -> Dict[str, Union[Dict[str, float], float]]:
        """
        Extracting the assets that is linked to the balance sheet.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {non_current_assets: {property_plant_equipment: float, investment_properties: float, intangible_assets: float, other_investments: float, subsidiaries_investments: float, biological_assets: float, others: float, total: float}, current_assets: {inventories: float, trade: float, cash: float, others: float, total: float}, total: float}
        """
        start_header: str = "NON-CURRENT ASSETS"
        end_header: str = "BALANCE SHEET (Continued)"
        start_index: int = result_set.index(start_header)
        end_index: int = result_set.index(end_header)
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if start_header not in value]
        result_set = [value for value in result_set if end_header not in value]
        non_current: Dict[str, float] = self.extractBalanceSheetAssetsNonCurrent(result_set)
        current: Dict[str, float] = self.extractBalanceSheetAssetsCurrent(result_set)
        if not non_current and not current:
            return {}
        result_set = [value for value in result_set if bool(search(r"[A-z]+", value)) == False]
        result_set = [value for value in result_set if "/" not in value]
        result_set.pop(0)
        result_set = [value.replace(",", "") for value in result_set]
        data: List[float] = [float(data) for data in result_set]
        total: float = data[-1]
        return {
            "non_current_assets": non_current,
            "current_assets": current,
            "total": total
        }

    def extractBalanceSheetAssetsCurrent(self, result_set: List[str]) -> Dict[str, float]:
        """
        Extracting the current assets that is linked to the assets.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {inventories: float, trade: float, cash: float, others: float, total: float}
        """
        start_index: int = 8
        result_set = [value for value in result_set if bool(search(r"[A-z]+", value)) == False]
        result_set = [value for value in result_set if "/" not in value]
        if len(result_set) == 0:
            return {}
        result_set.pop(0)
        result_set = [value.replace(",", "") for value in result_set]
        data: List[float] = [float(data) for data in result_set][start_index:]
        return {
            "inventories": data[0],
            "trade": data[1],
            "cash": data[2],
            "others": data[3],
            "total": data[4]
        }

    def extractBalanceSheetAssetsNonCurrent(self, result_set: List[str]) -> Dict[str, float]:
        """
        Extracting the non-current assets that is linked to the
        assets.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {property_plant_equipment: float, investment_properties: float, intangible_assets: float, other_investments: float, subsidiaries_investments: float, biological_assets: float, others: float, total: float}
        """
        result_set = [value for value in result_set if bool(search(r"[A-z]+", value)) == False]
        result_set = [value for value in result_set if "/" not in value]
        if len(result_set) == 0:
            return {}
        result_set.pop(0)
        result_set = [value.replace(",", "") for value in result_set]
        data: List[float] = [float(data) for data in result_set]
        return {
            "property_plant_equipment": data[0],
            "investment_properties": data[1],
            "intangible_assets": data[2],
            "other_investments": data[3],
            "subsidiaries_investments": data[4],
            "biological_assets": data[5],
            "others": data[6],
            "total": data[7],
        }

    def _extractBalanceSheet(self, result_set: List[str]) -> Dict[str, Union[int, str]]:
        """
        Extracting the balance sheet that is linked to the balance
        sheet.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {financial_year: int, currency: string, unit: int}
        """
        start_header: str = "BALANCE SHEET"
        end_header: str = "NON-CURRENT ASSETS"
        start_index: int = result_set.index(start_header)
        end_index: int = result_set.index(end_header)
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if start_header not in value]
        result_set = [value for value in result_set if end_header not in value]
        result_set = [value for value in result_set if ":" not in value]
        if len(result_set) == 0:
            return {}
        if len(result_set) > 0 and len(result_set) < 3:
            result_set.append("1")
        financial_year_end_date: str = [date for date in result_set if bool(search(r"[\d]+", date)) == True and "/" in date][0]
        financial_year: int = datetime.strptime(financial_year_end_date, "%d/%m/%Y").year - 1
        result_set = [value for value in result_set if financial_year_end_date not in value]
        currency: str = [currency for currency in result_set if bool(search(r"[A-z]+", currency)) == True][0]
        result_set = [value for value in result_set if currency not in value]
        unit: int = int([unit for unit in result_set if bool(search(r"[\d]+", unit)) == True][0])
        return {
            "financial_year": financial_year,
            "currency": currency,
            "unit": unit
        }

    def _extractProfitStatements(self, result_set: List[str]) -> Dict[str, Union[int, str]]:
        """
        Extracting the financial summary that is linked to the
        profit statement.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {financial_year: int, currency: string, date_approved: int, unit: int}
        """
        start_header: str = "Last Financial Summary Filed"
        end_header: str = "PROFIT AND LOSS STATEMENT"
        start_index: int = result_set.index(start_header)
        end_index: int = result_set.index(end_header)
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if start_header not in value]
        result_set = [value for value in result_set if end_header not in value]
        result_set = [value for value in result_set if ":" not in value]
        if len(result_set) < 4:
            return {}
        financial_year: int = datetime.strptime(result_set[0], "%d/%m/%Y").year - 1
        currency: str = result_set[1]
        date_approved_unixtime: int = int(datetime.strptime(result_set[2], "%d/%m/%Y").timestamp())
        unit: int = int(result_set[3])
        return {
            "financial_year": financial_year,
            "currency": currency,
            "date_approved": date_approved_unixtime,
            "unit": unit
        }

    def extractProfitStatements(self, portable_document_file_result_set: List[str]) -> Dict[str, Union[Dict[str, Union[int, str]], float]]:
        """
        Extracting the profit data for the profit statements from
        the result set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {financial_summary: {financial_year: int, currency: string, date_approved: int, unit: int}, turnover: float, cost_of_sales: float, gross_profit: float, other_income: float, distribution_cost: float, administration_cost: float, expenses: float, finance_cost: float, net_profit_before_taxation: float, taxation: float, net_profit: float}
        """
        start_header: str = "Last Financial Summary Filed"
        end_header: str = "BALANCE SHEET"
        start_index: int = portable_document_file_result_set.index(start_header)
        end_index: int = portable_document_file_result_set.index(end_header)
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        line_break: str = "-" * 10
        financial_summary: Dict[str, Union[int, str]] = self._extractProfitStatements(result_set)
        start_header = "PROFIT AND LOSS STATEMENT"
        end_header = "BALANCE SHEET"
        start_index = result_set.index(start_header)
        end_index = result_set.index(end_header) if end_header in result_set else len(result_set)
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if start_header not in value]
        result_set = [value for value in result_set if end_header not in value]
        result_set = [value for value in result_set if bool(search(r"[A-z]+", value)) == False]
        result_set = [value for value in result_set if "/" not in value]
        if not financial_summary and len(result_set) == 0:
            return {}
        data: List[float] = [float(data.replace(",", "")) for data in result_set]
        turnover: float = data[0]
        cost_of_sales: float = data[1]
        gross_profit: float = data[2]
        other_income: float = data[3]
        distribution_cost: float = data[4]
        administration_cost: float = data[5]
        expenses: float = data[6]
        finance_cost: float = data[7]
        net_profit_before_taxation: float = data[8]
        taxation: float = data[9]
        net_profit: float = data[10]
        return {
            "financial_summary": financial_summary,
            "turnover": turnover,
            "cost_of_sales": cost_of_sales,
            "gross_profit": gross_profit,
            "other_income": other_income,
            "distribution_cost": distribution_cost,
            "administration_cost": administration_cost,
            "expenses": expenses,
            "finance_cost": finance_cost,
            "net_profit_before_taxation": net_profit_before_taxation,
            "taxation": taxation,
            "net_profit": net_profit
        }

    def extractFinancialSummaries(self, portable_document_file_result_set: List[str]) -> List[Dict[str, Union[int, str]]]:
        """
        Extracting the data for the financial summaries from the
        result set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{financial_year: int, currency: string, date_approved: int, unit: int}]
        """
        response: List[Dict[str, Union[int, str]]] = []
        start_header: str = "Financial Summary/Statements filed for last 3 years"
        end_header: str = "Last Financial Summary Filed"
        start_index: int = portable_document_file_result_set.index(start_header)
        end_index: int = portable_document_file_result_set.index(end_header)
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        result_set = [value for value in result_set if start_header not in value]
        result_set = [value for value in result_set if end_header not in value]
        result_set = [value for value in result_set if "Page" not in value]
        result_set = [value for value in result_set if " of " not in value]
        result_set = [value for value in result_set if "Date Issued" not in value]
        result_set = [value for value in result_set if "Financial Year Ended" not in value]
        result_set = [value for value in result_set if "Currency" not in value]
        result_set = [value for value in result_set if "Date Approved" not in value]
        if len(result_set) < 3:
            return response
        for index in range(0, len(result_set), 3):
            is_in_bound: bool = True if index + 3 < len(result_set) else False
            response.append({
                "financial_year": int(datetime.strptime(result_set[index], "%d/%m/%Y").year - 1) if is_in_bound == True else 0,
                "currency": str(result_set[index + 1]) if is_in_bound == True else "",
                "date_approved": int(datetime.strptime(result_set[index + 3], "%d/%m/%Y").timestamp()) if is_in_bound == True else 0
            })
        response = [value for value in response if value["financial_year"] != 0]
        return response

    def extractAnnualReturns(self, portable_document_file_result_set: List[str]) -> List[Dict[str, int]]:
        """
        Extracting the data for the annual returns from the result
        set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{date_annual_return: int, date_annual_meeting: int, date_filled: int}]
        """
        response: List[Dict[str, int]] = []
        start_header: str = "Annual Return filed for last 3 years"
        end_header: str = "Financial Summary/Statements filed for last 3 years"
        start_index: int = portable_document_file_result_set.index(start_header)
        end_index: int = portable_document_file_result_set.index(end_header)
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        result_set = [value for value in result_set if "/" in value and bool(search(r"[0-9]+", value)) == True]
        if len(result_set) < 3:
            return response
        for index in range(0, len(result_set), 3):
            is_inbounds: bool = True if index + 2 <= len(result_set) else False
            response.append({
                "date_annual_return": int(datetime.strptime(result_set[index], "%d/%m/%Y").timestamp()) if is_inbounds else 0,
                "date_annual_meeting": int(datetime.strptime(result_set[index + 1], "%d/%m/%Y").timestamp()) if is_inbounds else 0,
                "date_filled": int(datetime.strptime(result_set[index + 2], "%d/%m/%Y").timestamp()) if is_inbounds else 0
            })
        response = [annual_return for annual_return in response if annual_return["date_annual_return"] != 0 and annual_return["date_annual_meeting"] != 0 and annual_return["date_filled"] != 0]
        return response

    def extractMembers(self, portable_document_file_result_set: List[str]) -> List[Dict[str, Union[str, int]]]:
        """
        Extracting the data for the members from the result set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{name: string, amount: int, date_start: int, currency: string}]
        """
        response: List[Dict[str, Union[str, int]]]
        start_index: int = portable_document_file_result_set.index("Members (Applicable for Company Limited by Guarantee or Shares and Guarantee)") + 1
        end_index: int = portable_document_file_result_set.index("Annual Return filed for last 3 years")
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        result_set = [value for value in result_set if "Date" not in value]
        result_set = [value for value in result_set if "Page" not in value]
        result_set = [value for value in result_set if " of " not in value]
        result_set = [value for value in result_set if "Name" not in value]
        result_set = [value for value in result_set if "Amount" not in value]
        result_set = [value for value in result_set if "Currency" not in value]
        if len(result_set) > 0:
            response = self._extractMembers(result_set)
        else:
            response = []
        return response

    def _extractMembers(self, result_set: List[str]) -> List[Dict[str, Union[str, int]]]:
        """
        Extracting the members of a domestic private company when
        there are listed in the corporate registry.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{name: string, amount: int, date_start: int, currency: string}]
        """
        response: List[Dict[str, Union[str, int]]] = []
        possible_currencies: List[str] = self.getShareholder().getPossibleCurrencies()
        dataset: List[str] = [value for value in result_set if bool(search(r"[\d]+", value)) == True and "/" not in value]
        amounts: List[int] = [int(value.replace(",", "")) for value in result_set if bool(search(r"[\d]+", value)) == True and "/" not in value]
        result_set = [value for value in result_set if value not in dataset]
        date_starts: List[str] = [value for value in result_set if bool(search(r"[\d]+", value)) == True]
        result_set = [value for value in result_set if value not in date_starts]
        currencies: List[str] = [value for value in result_set if value in possible_currencies]
        names: List[str] = [value for value in result_set if value not in currencies]
        limitation: int = min([len(amounts), len(date_starts), len(currencies), len(names)])
        for index in range(0, limitation, 1):
            response.append({
                "name": names[index].title(),
                "amount": amounts[index],
                "date_start": int(datetime.strptime(date_starts[index], "%d/%m/%Y").timestamp()),
                "currency": currencies[index].title()
            })
        return response

    def extractCertificates(self, portable_document_file_result_set: List[str]) -> List[Dict[str, Union[str, int]]]:
        """
        Extracting the data for the certificates from the result
        set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{certificate: string, type: str, date_effective: int, date_expiry: int}]
        """
        start_index: int = portable_document_file_result_set.index("Certificate (Issued by Other Institutions)")
        end_index: int = portable_document_file_result_set.index("Office Bearers")
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        end_index = result_set.index("Name") if "Name" in result_set else len(result_set)
        result_set = result_set[:end_index] if "Name" in result_set else result_set
        result_set = [value for value in result_set if "Certificate (Issued by Other Institutions)" not in value]
        result_set = [value for value in result_set if "Certificate" not in value]
        result_set = [value for value in result_set if "Type" not in value]
        result_set = [value for value in result_set if "Effective Date" not in value]
        result_set = [value for value in result_set if "Expiry Date" not in value]
        result_set = [value for value in result_set if "Page" not in value]
        result_set = [value for value in result_set if " of " not in value]
        result_set = [value for value in result_set if "Date Issued" not in value]
        result_set = [value for value in result_set if bool(search(r"[A-z]+", value)) == True]
        if len(result_set) < 4:
            return []
        self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractCertificates()")
        exit()

    def _extractShareholdersTypeShares(self, type_shares: List[str]) -> str:
        """
        Building the type of the shares of the shareholders.

        Parameters:
            type_shares: [string]: The list of the types of the shares of the shareholders.

        Returns:
            string
        """
        if len(type_shares) > 0:
            return " ".join(type_shares)
        else:
            return "NaTS"

    def __extractShareholdersTypeShares(self, type_shares: List[str], type_share: str) -> List[str]:
        """
        Setting all of the type of shares into the response.

        Parameters:
            type_shares: [string]: The response to be returned
            type_share: string: The type of share of the shareholder

        Returns:
            [string]
        """
        if type_share != "NaTS":
            type_shares.append(type_share)
        return type_shares

    def extractShareholdersTypeShares(self, result_set: List[str]) -> List[str]:
        """
        Extracting the type of shares of the shareholders of a
        private domestic company.

        Parameters:
            result_set: [string]: The result set to be used as a dataset.

        Returns:
            [string]
        """
        response: List[str] = []
        possible_types: List[str] = self.getShareholder().getPossibleShareTypes()
        types: List[str] = [value for value in result_set if bool(search(r"[\d]+", value)) == True and bool(search(r"[A-Z]+", value)) == True and bool(search(r"[^\w\s]+", value)) == False]
        processed_types: List[str] = []
        for index in range(0, len(types), 1):
            processed_types.append(" ".join([value for value in types[index].split(" ") if bool(search(r"[A-Z]+", value)) == True and bool(search(r"[\d]+", value)) == False]))
        response = [value for value in processed_types if value in possible_types]
        return response

    def extractShareholdersAmountShares(self, result_set: List[str]) -> List[int]:
        """
        Extracting the amount of shares of the shareholders of a
        private domestic company.

        Parameters:
            result_set: [string]: The result set to be used as a dataset.

        Returns:
            [int]
        """
        response: List[int] = []
        amounts: List[str] = [value for value in result_set if bool(search(r"[\d]+", value)) == True and bool(search(r"[A-Z]+", value)) == True and bool(search(r"[^\w\s]+", value)) == False]
        processed_amounts: List[str] = []
        for index in range(0, len(amounts), 1):
            processed_amounts.append("".join([value for value in amounts[index].split(" ") if bool(search(r"[\d]+", value)) == True and bool(search(r"[A-z]+", value)) == False]))
        response = [int(value) for value in [value for value in processed_amounts if "" != value]]
        return response

    def extractShareholders(self, portable_document_file_result_set: List[str]) -> List[Dict[str, Union[str, int]]]:
        """
        Extracting the data for the shareholders of a private
        domestic company.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{name: string, amount: int, type: string, currency: string}]
        """
        response: List[Dict[str, Union[str, int]]] = []
        start_index: int = portable_document_file_result_set.index("Shareholders") + 1
        end_index: int = portable_document_file_result_set.index("Members (Applicable for Company Limited by Guarantee or Shares and Guarantee)")
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        result_set = [value for value in result_set if "Name" not in value]
        result_set = [value for value in result_set if "Type of Shares" not in value]
        result_set = [value for value in result_set if "Currency" not in value]
        result_set = [value for value in result_set if "Service Address" not in value]
        result_set = [value for value in result_set if "Appointed Date" not in value]
        result_set = [value for value in result_set if "/" not in value]
        dataset: List[str] = [value for value in result_set if bool(search(r"[\d]+", value)) == True and bool(search(r"[A-Z]+", value)) == True and bool(search(r"[^\w\s]+", value)) == False]
        amount_of_shares: List[int] = self.extractShareholdersAmountShares(result_set)
        type_of_shares: List[str] = self.extractShareholdersTypeShares(result_set)
        result_set = [value for value in result_set if value not in dataset]
        names: List[str] = [value for value in result_set if bool(search(r"[A-Z]+", value)) == True and "Mauritius" not in value]
        names = [name for index, name in enumerate(names) if all(name not in names for name in names[:index])]
        dataset = [value for value in result_set if bool(search(r"[A-Z]+", value)) == True and "Mauritius" not in value]
        result_set = [value for value in result_set if value not in dataset]
        currencies: List[str] = [value for value in result_set if bool(search(r"[A-Z]+", value)) == True and bool(search(r"[a-z]+", value)) == True]
        for index in range(0, min([len(names), len(amount_of_shares), len(type_of_shares), len(currencies)]), 1):
            response.append({
                "name": names[index].title(),
                "amount_shares": amount_of_shares[index],
                "type_shares": type_of_shares[index].title(),
                "currency": currencies[index].title()
            })
        return response

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
        if len(dataset) == 1 and dataset[0] != "MAURITIUS" and len(dataset[0]) > 1 and (dataset[0] == "DIRECTOR" or dataset[0] == "SECRETARY" or dataset[0] == "REGISTERED AGENT"):
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
            positions: List[str] = findall(r"\b[A-Z\s]+\b", result_set[index])
            position: str = self._extractOfficeBearersPositions(positions)
            response = self.__extractOfficeBearersPositions(response, position)
        return response

    def __extractNames(self, names: List[str], name: str) -> List[str]:
        """
        Setting all of the names into the response.

        Parameters:
            names: [string]: The response to be returned
            name: string: The name.

        Returns:
            [string]
        """
        if name != "NaN":
            names.append(name)
        return names

    def _extractOfficeBearersNames(self, dataset: List[str]) -> str:
        """
        Building the name of an office bearer.

        Parameters:
            dataset: [string]: The dataset containing the name.

        Returns:
            string
        """
        if len(dataset) > 0 and "MAURITIUS" not in dataset:
            return " ".join(dataset)
        else:
            return "NaN"

    def extractOfficeBearersNames(self, result_set: List[str]) -> List[str]:
        """
        Retrieving the names of the office bearers.

        Parameters:
            result_set: [string]: The result set of the office bearers.

        Returns:
            [string]
        """
        response: List[str] = []
        result_set = [value for value in result_set if bool(search(r"[A-Z]+", value.upper())) == True and "MAURITIUS" not in value.upper()]
        for index in range(0, len(result_set), 1):
            response.append(result_set[index])
        return response

    def _extractOfficeBearersAddresses(self, address: str) -> str:
        """
        Building the address of an office bearer.

        Parameters:
            dataset: [string]: The dataset containing the address.

        Returns:
            string
        """
        if "MAURITIUS" not in address:
            address = address + "MAURITIUS"
        return address

    def extractOfficeBearersAddresses(self, result_set: List[str]) -> List[str]:
        """
        Extracting the addresses of the office bearers.

        Parameters:
            result_set: [string]: The result set of the office bearers.

        Returns:
            [string]
        """
        response: List[str] = []
        address_result_set = " ".join(result_set)
        result_set = address_result_set.split("MAURITIUS ")
        for index in range(0, len(result_set), 1):
            address: str = self._extractOfficeBearersAddresses(result_set[index])
            response.append(address)
        return response

    def extractOfficeBearers(self, portable_document_file_result_set: List[str]) -> List[Dict[str, Union[str, int]]]:
        """
        Extracting the data for the office bearers from the result
        set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{position: string, name: string, address: string, date_appointment: int}]
        """
        response: List[Dict[str, Union[str, int]]] = []
        start_index: int = portable_document_file_result_set.index("Office Bearers") + 1
        end_index: int = portable_document_file_result_set.index("No. of Shares Type of Shares")
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        result_set = [value for value in result_set if "Position" not in value]
        result_set = [value for value in result_set if "Name" not in value]
        result_set = [value for value in result_set if "Service Address" not in value]
        result_set = [value for value in result_set if "Appointed Date" not in value]
        result_set = [value for value in result_set if "Shareholders" not in value]
        date_appointments: List[str] = self.extractOfficeBearersDateAppointments(result_set)
        result_set = [value for value in result_set if value not in date_appointments]
        positions: List[str] = self.extractOfficeBearersPositions(result_set)
        result_set = [value for value in result_set if value not in positions]
        names: List[str] = self.extractOfficeBearersNames(result_set)
        result_set = [value for value in result_set if value not in names]
        addresses: List[str] = self.extractOfficeBearersAddresses(result_set)
        limitation: int = min([len(date_appointments), len(positions), len(names), len(addresses)])
        for index in range(0, limitation, 1):
            position: str = positions[index].title()
            name: str = names[index].title()
            address: str = addresses[index].title()
            date_appointment: int = int(datetime.strptime(date_appointments[index], "%d/%m/%Y").timestamp())
            office_bearer: Dict[str, Union[str, int]] = {
                "position": position,
                "name": name,
                "address": address,
                "date_appointment": date_appointment
            }
            response.append(office_bearer)
        return response

    def extractStateCapital(self, portable_document_file_result_set: List[str]) -> List[Dict[str, Union[str, int, float]]]:
        """
        Extracting the data for the share capital from the result
        set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{type: string, amount: int, currency: string, state_capital: int, amount_unpaid: float}]
        """
        response: List[Dict[str, Union[str, int, float]]] = []
        start_index: int = portable_document_file_result_set.index("Type of Shares")
        end_index: int = portable_document_file_result_set.index("Certificate (Issued by Other Institutions)")
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        result_set = [value for value in result_set if "Type of Shares" not in value]
        result_set = [value for value in result_set if "No. of Shares Currency" not in value]
        result_set = [value for value in result_set if "Stated Capital" not in value]
        result_set = [value for value in result_set if "Amount Unpaid Par Value" not in value]
        result_set = [value for value in result_set if "Page " not in value]
        result_set = [value for value in result_set if " of " not in value]
        result_set = [value for value in result_set if "Date" not in value]
        result_set = [value for value in result_set if "/" not in value]
        types: List[str] = [f"{value} SHARES" for value in " ".join([value for value in result_set if bool(search(r"[A-Z]+", value)) == True and bool(search(r"[a-z]+", value)) == False]).split(" SHARES") if value != ""]
        dataset: List[str] = [value for value in result_set if bool(search(r"[A-Z]+", value)) == True and bool(search(r"[a-z]+", value)) == False]
        result_set = [value for value in result_set if value not in dataset]
        amounts: List[int] = self.extractStateCapitalAmount(result_set)
        currencies: List[str] = self.extractStateCapitalCurrency(result_set)
        dataset = [value for value in result_set if bool(search(r"[\d]+", value)) == True and bool(search(r"[A-z]+", value)) == True]
        result_set = [value for value in result_set if value not in dataset]
        stated_capitals: List[float] = self.extractStateCapitalStatedCapital(result_set)
        dataset = [value for value in result_set if bool(search(r"[\d]+", value)) == True and "," in value]
        result_set = [value for value in result_set if value not in dataset]
        amount_unpaids: List[float] = self.extractStateCapitalAmountUnpaid(result_set)
        limitation: int = min([len(types), len(amounts), len(currencies), len(stated_capitals), len(amount_unpaids)])
        for index in range(0, limitation, 1):
            response.append({
                "type": types[index].title(),
                "amount": amounts[index],
                "currency": currencies[index].title(),
                "stated_capital": stated_capitals[index],
                "amount_unpaid": amount_unpaids[index]
            })
        return response

    def extractStateCapitalShareValue(self, result_set: List[str]) -> List[int]:
        """
        Extracting the share value of the stated capital of a
        private domestic company.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [int]
        """
        response: List[int] = []
        for index in range(0, len(result_set), 1):
            response.append(int(result_set[index].split(" ")[-1]))
        return response

    def extractStateCapitalAmountUnpaid(self, result_set: List[str]) -> List[float]:
        """
        Extracting the amount unpaid of the stated capital of a
        private domestic company.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [float]
        """
        response: List[float] = []
        for index in range(0, len(result_set), 1):
            response.append(float(result_set[index].split(" ")[0]))
        return response

    def extractStateCapitalStatedCapital(self, result_set: List[str]) -> List[float]:
        """
        Extracting the stated capital of the stated capital of a
        private domestic company.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [float]
        """
        response: List[float] = []
        stated_capitals: List[str] = [value for value in result_set if bool(search(r"[\d]+", value)) == True and "," in value]
        for index in range(0, len(stated_capitals), 1):
            stated_capital: float = float(stated_capitals[index].replace(",", ""))
            response.append(stated_capital)
        return response

    def extractStateCapitalCurrency(self, result_set: List[str]) -> List[str]:
        """
        Extracting the currencies of the stated capital of a private
        domestic company.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [string]
        """
        response: List[str] = []
        currencies: List[str] = [value for value in result_set if bool(search(r"[\d]+", value)) == True and bool(search(r"[A-z]+", value)) == True]
        for index in range(0, len(currencies), 1):
            currency: str = " ".join(findall(r"[A-z]+", currencies[index]))
            response.append(currency)
        return response

    def extractStateCapitalAmount(self, result_set: List[str]) -> List[int]:
        """
        Extracting the amount of shares of the stated capital of a
        private domestic company.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [int]
        """
        response: List[int] = []
        amounts: List[str] = [value for value in result_set if bool(search(r"[\d\s]+", value)) == True and bool(search(r"[A-z]+", value)) == True]
        for index in range(0, len(amounts), 1):
            amount: int = int("".join(findall(r"[\d]+", amounts[index])))
            response.append(amount)
        return response

    def extractBusinessDetails(self, portable_document_file_result_set: List[str]) -> List[Dict[str, str]]:
        """
        Extracting the data for the business details from the result
        set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{registered_address: string, name: string, nature: string, operational: string}]
        """
        response: List[Dict[str, str]] = []
        registered_address: str = " ".join([value for value in portable_document_file_result_set[[index for index, value in enumerate(portable_document_file_result_set) if "Registered Office Address" in value][0]].split(": ")[-1].split(" ") if value != ""])
        start_index: int = portable_document_file_result_set.index("Business Details")
        end_index: int = portable_document_file_result_set.index("Type of Shares")
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        result_set = [value for value in result_set if "Business Details" not in value]
        result_set = [value for value in result_set if "Business Registration No" not in value]
        result_set = [value for value in result_set if "Business Name" not in value]
        result_set = [value for value in result_set if "Nature of Business" not in value]
        result_set = [value for value in result_set if "Principal Place of Business" not in value]
        result_set = [value for value in result_set if "Particulars of Stated Capital" not in value]
        operational_addresses: List[str] = self.extractBusinessDetailsOperationalAddresses(result_set)
        dataset: List[str] = [value for value in result_set if bool(search(r"[A-Z]+", value)) == True and "Mauritius".upper() in value]
        result_set = [value for value in result_set if value not in dataset]
        dataset = [value for value in result_set if bool(search(r"[A-Z]+", value)) == True and bool(search(r"[a-z]+", value)) == True and "/" in value]
        natures: List[str] = self.extractBusinessDetailsNatures(result_set)
        names: List[str] = [value for value in result_set if value not in dataset]
        limitation: int = min([len(names), len(natures), len(operational_addresses)])
        for index in range(0, limitation, 1):
            response.append({
                "registered_address": registered_address.title(),
                "name": names[index].title(),
                "nature": natures[index].title(),
                "operational_address": operational_addresses[index].title()
            })
        return response

    def extractBusinessDetailsNatures(self, result_set: List[str]) -> List[str]:
        """
        Extracting the natures that are linked to the business
        details of a private domestic company.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [string]
        """
        response: List[str] = []
        natures: List[str] = [value for value in result_set if bool(search(r"[A-Z]+", value)) == True]
        for index in range(0, len(natures), 1):
            response.append(natures[index])
        return response

    def extractBusinessDetailsOperationalAddresses(self, result_set: List[str]) -> List[str]:
        """
        Extracting the operational addresses that are linked to the
        business details of private domestic companies and foreign
        domestic companies.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [string]
        """
        response: List[str] = []
        operational_addresses: List[str] = [value for value in result_set if "Court" in value.title() or "Street" in value.title() or "Mauritius".upper() in value or "Rodrigues".upper() in value]
        for index in range(0, len(operational_addresses), 1):
            response.append(f"{' '.join([value for value in operational_addresses[index].split(' ') if value != '']).title().replace('Mauritius', '')} Mauritius".title())
        return response

    def extractCompanyDetails(self, portable_document_file_result_set: List[str]) -> Dict[str, Union[str, int]]:
        """
        Extracting the data for the company details of a private
        domestic company from the result set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}
        """
        response: Dict[str, Union[str, int]]
        business_registration_number: str = portable_document_file_result_set[[index for index, value in enumerate(portable_document_file_result_set) if "Business Registration No.:" in value][0]].split(" ")[-1]
        start_index: int = portable_document_file_result_set.index("Company Details") + 1
        end_index: int = portable_document_file_result_set.index("Business Name")
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        result_set = [value for value in result_set if ":" not in value]
        result_set = [value for value in result_set if "Registrar of Companies" not in value]
        result_set = [value for value in result_set if "Business Details" not in value]
        file_number: str = result_set[0]
        result_set = [value for value in result_set if file_number not in value]
        name: str = [value for value in result_set if bool(search(r"[A-Z]+", value)) == True][0]
        result_set = [value for value in result_set if name not in value]
        category: str = [value for value in result_set if bool(search(r"[A-Z]+", value)) == True and bool(search(r"[a-z]+", value)) == False and "Limited By".upper() not in value][0] if len([value for value in result_set if bool(search(r"[A-Z]+", value)) == True and bool(search(r"[a-z]+", value)) == False and "Limited By".upper() not in value]) > 0 else "Domestic"
        result_set = [value for value in result_set if category not in value]
        date_incorporation: int = int(datetime.strptime([value for value in result_set if bool(search(r"[\d]", value)) == True and "/" in value][0], "%d/%m/%Y").timestamp())
        nature: str = [value for value in result_set if bool(search(r"[A-Z]+", value)) == True and bool(search(r"[a-z]+", value)) == True and "Live" not in value and "Defunct" not in value][0]
        status: str = [value for value in result_set if (bool(search(r"[A-Z]+", value)) == True and bool(search(r"[a-z]+", value)) == True) and ("Live" in value or "Defunct" in value)][0]
        response = {
            "business_registration_number": business_registration_number,
            "name": name.title(),
            "file_number": file_number,
            "category": category.title(),
            "date_incorporation": date_incorporation,
            "nature": nature.title(),
            "status": status.title()
        }
        return response