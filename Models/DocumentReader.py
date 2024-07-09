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
from Data.CompanyDetails import CompanyDetails
from Environment import Environment
from typing import Dict, Tuple, Union, List
from pdfminer.high_level import extract_text
from datetime import datetime
from json import dumps
from re import findall, search, split
from Models.OfficeBearers import Office_Bearers


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

    def __init__(self) -> None:
        """
        Initializing the document reader which will import and
        initialize the dependencies.
        """
        self.ENV = Environment()
        self.setLogger(Corporate_Database_Builder_Logger())
        self.setOfficeBearer(Office_Bearers())
        self.getLogger().inform("The builder has been initialized and all of its dependencies are injected!")

    def getLogger(self) -> Corporate_Database_Builder_Logger:
        return self.__logger

    def setLogger(self, logger: Corporate_Database_Builder_Logger) -> None:
        self.__logger = logger

    def getOfficeBearer(self) -> Office_Bearers:
        return self.__office_bearer

    def setOfficeBearer(self, office_bearer: Office_Bearers) -> None:
        self.__office_bearer = office_bearer

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

    def extractData(self, status: int, dataset: DocumentFiles, company_detail: CompanyDetails) -> Union[Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]], Dict[str, Union[int, Dict[str, Union[str, int]], Dict[str, str], List[Dict[str, Union[str, int]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]], Dict[str, Union[Dict[str, str], List[Dict[str, int]]]]]]]:
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
        response: Union[Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]], Dict[str, Union[int, Dict[str, Union[str, int]], Dict[str, str], List[Dict[str, Union[str, int]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]], Dict[str, Union[Dict[str, str], List[Dict[str, int]]]]]]]
        if company_detail.category.upper() == "DOMESTIC":
            response = self.extractDataDomestic(status, dataset, company_detail)
        elif company_detail.category.upper() == "AUTHORISED COMPANY":
            response = self.extractDataAuthorisedCompany(status, dataset)
        else:
            self.getLogger().error(f"The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractData()\nCategory: {company_detail.category}")
            exit()
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
        if status == 201:
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
        else:
            response = {
                "status": 404
            }
            self.getLogger().error(f"The portable document file has not been generated correctly!  The application will abort the extraction.\nStatus: {response['status']}\nFile Location: {file_name}\nDocument File Identifier: {dataset.identifier}\nCompany Detail Identifier: {dataset.company_detail}")
        return response

    def _extractDataAuthorisedCompanyLiquidators(self, portable_document_file_data: List[str]) -> Dict[str, Union[Dict[str, str], List[Dict[str, int]]]]:
        """
        Extracting the liquidators that are linked to the authorised
        company.

        Parameters:
            portable_document_file_data: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {liquidator: {name: string, address: string}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}
        """
        start_index: int = portable_document_file_data.index("Liquidators")
        end_index: int = portable_document_file_data.index("This is a Computer Generated Document.")
        result_set: List[str] = portable_document_file_data[start_index:end_index]
        liquidator: Dict[str, str] = self.__extractDataAuthorisedCompanyLiquidators(result_set)
        affidavits: List[Dict[str, int]] = self._extractDataAuthorisedCompanyLiquidatorsAffidavits(result_set)
        if not liquidator and len(affidavits) == 0:
            return {}
        else:
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
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.__extractDataAuthorisedCompanyLiquidators()")
            exit()
        else:
            return {}

    def _extractDataAuthorisedCompanyAdministrators(self, portable_document_file_data: List[str]) -> Dict[str, Union[Dict[str, str], List[Dict[str, int]]]]:
        """
        Extracting the administrators from an authorised company.

        Parameters:
            portable_document_file_data: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {administrator: {name: string, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}
        """
        start_index: int = portable_document_file_data.index("Administrators")
        end_index: int = portable_document_file_data.index("Liquidators")
        result_set: List[str] = portable_document_file_data[start_index:end_index]
        administrator: Dict[str, str] = self.__extractDataAuthorisedCompanyAdministrators(result_set)
        accounts: List[Dict[str, int]] = self._extractDataAuthorisedCompanyAdministratorsAccounts(result_set)
        if not administrator and len(accounts) == 0:
            return {}
        else:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractAdministrators()")
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
        start_index: int = result_set.index("Accounts of Administrator") + 1
        result_set = result_set[start_index:]
        result_set.remove("Date Filed")
        result_set.remove("From")
        result_set.remove("To")
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader._extractDataAuthorisedCompanyAdministratorsAccounts()")
            exit()
        else:
            return []

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
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.__extractDataAuthorisedCompanyAdministrators()")
            exit()
        else:
            return {}

    def _extractDataAuthorisedCompanyOfficeBearers(self, portable_document_file_data: List[str]) -> List[Dict[str, Union[str, int]]]:
        """
        Extracting the data for the office bearers from the result
        set.

        Parameters:
            portable_document_file_data: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{position: string, name: string, address: string, date_appointment: int}]
        """
        response: List[Dict[str, Union[str, int]]] = []
        start_index: int = portable_document_file_data.index("Office Bearers") + 1
        end_index: int = portable_document_file_data.index("Receivers")
        result_set: List[str] = portable_document_file_data[start_index:end_index]
        result_set = [value for value in result_set if "Position" not in value]
        result_set = [value for value in result_set if "Name" not in value]
        result_set = [value for value in result_set if "Appointed Date" not in value]
        result_set = [value for value in result_set if "Service Address" not in value]
        date_appointments: List[str] = self.extractOfficeBearersDateAppointments(result_set)
        result_set = [value for value in result_set if value not in date_appointments]
        positions: List[str] = self.extractOfficeBearersPositions(result_set)
        result_set = [value for value in result_set if value not in positions]
        addresses: List[str] = self._extractDataAuthorisedCompanyOfficeBearersAddresses(result_set)
        names: List[str] = [value for value in result_set if value not in addresses]
        for index in range(0, min([len(date_appointments), len(positions), len(addresses), len(names)]), 1):
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
        dataset: str = " ".join(result_set)
        response: List[str] = findall(r"\b\d.*?[A-Z]\b", dataset)
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
        result_set.remove("Registrar of Companies")
        response = {
            "name": result_set[1],
            "file_number": result_set[0],
            "category": result_set[3].title(),
            "date_incorporation": int(datetime.strptime(result_set[4], "%d/%m/%Y").timestamp()),
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
            response = self.extractDataDomesticCivil(status, dataset) # type: ignore
        else:
            self.getLogger().error(f"The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractData()\nNature: {company_detail.nature}")
            exit()
        return response

    def extractDataDomesticCivil(self, status: int, dataset: DocumentFiles) -> Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], Dict[str, str], List[Dict[str, Union[str, int]]], Dict[str, Union[Dict[str, Union[str, int]], List[int]]]]]:
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
        response: Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], Dict[str, str], List[Dict[str, Union[str, int]]], Dict[str, Union[Dict[str, Union[str, int]], List[int]]]]]
        file_name: str = f"{self.ENV.getDirectory()}Cache/CorporateDocumentFile/Documents/{dataset.company_detail}.pdf"
        cache_data_file_name: str = f"{self.ENV.getDirectory()}Cache/CorporateDocumentFile/Metadata/{dataset.company_detail}.json"
        if status == 201:
            portable_document_file_data: str = extract_text(file_name)
            cache_file = open(cache_data_file_name, "w")
            portable_document_file_data_result_set: List[str] = list(filter(None, portable_document_file_data.split("\n")))
            business_registration_number: Union[str, None] = self.extractDataDomesticCivilBusinessRegistrationNumber(portable_document_file_data_result_set)
            response = self._extractDataDomesticCivil(portable_document_file_data_result_set, business_registration_number)
            cache_file.write(dumps(response, indent=4))
            cache_file.close()
            self.getLogger().inform(f"Data has been extracted from the portable document file version of the corporate registry.\nStatus: {response['status']}\nDocument File Identifier: {dataset.identifier}\nFile Location: {file_name}\nCompany Details Identifier: {dataset.company_detail}")
        else:
            response = {
                "status": 404
            }
            self.getLogger().error(f"The portable document file has not been generated correctly!  The application will abort the extraction.\nStatus: {response['status']}\nFile Location: {file_name}\nDocument File Identifier: {dataset.identifier}\nCompany Detail Identifier: {dataset.company_detail}")
        return response

    def _extractDataDomesticCivil(self, result_set: List[str], business_registration_number: Union[str, None]) -> Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], Dict[str, str], List[Dict[str, Union[str, int]]], Dict[str, Union[Dict[str, Union[str, int]], List[int]]]]]:
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
        response: Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], Dict[str, str], List[Dict[str, Union[str, int]]], Dict[str, Union[Dict[str, Union[str, int]], List[int]]]]]
        if business_registration_number == None:
            response = self._extractDataDomesticCivilCivil(result_set)
        else:
            self.getLogger().error(f"The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractData()\nCivil Company Type: Société Commerciale")
            exit()
        return response

    def _extractDataDomesticCivilCivil(self, result_set: List[str]) -> Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], Dict[str, str], List[Dict[str, Union[str, int]]], Dict[str, Union[Dict[str, Union[str, int]], List[int]]]]]:
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
        company_details: Dict[str, Union[str, int]] = self._extractDataDomesticCivilCivilCompanyDetails(result_set)
        business_details: Union[List[Dict[str, str]], Dict[str, str]] = self._extractDataDomesticCivilCivilBusinessDetails(result_set)
        state_capital: List[Dict[str, Union[str, int]]] = self._extractDataDomesticCivilCivilStateCapital(result_set)
        office_bearers: List[Dict[str, Union[str, int]]] = self._extractDataDomesticCivilCivilOfficeBearers(result_set)
        shareholders: List[Dict[str, Union[str, int]]] = self._extractDataDomesticCivilCivilShareholders(result_set)
        liquidators: Dict[str, Union[Dict[str, Union[str, int]], List[int]]] = self._extractDataDomesticCivilCivilLiquidators(result_set)
        receivers: Dict[str, Union[Dict[str, Union[str, int]], List[int]]] = self._extractDataDomesticCivilCivilReceivers(result_set)
        administrators: Dict[str, Union[Dict[str, Union[str, int]], List[int]]] = self._extractDataDomesticCivilCivilAdministrators(result_set)
        details: List[Dict[str, Union[str, int]]] = self._extractDataDomesticCivilCivilDetails(result_set)
        objections: List[Dict[str, Union[str, int]]] = self._extractDataDomesticCivilCivilObjections(result_set)
        response: Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], Dict[str, str], List[Dict[str, Union[str, int]]], Dict[str, Union[Dict[str, Union[str, int]], List[int]]]]] = {
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
            }
        return response

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
        start_index: int = result_set.index("Winding Up Details") + 1
        end_index: int = result_set.index("This is a Computer Generated Document.")
        result_set = result_set[start_index:end_index]
        end_index = result_set.index("Type") + 2
        dataset: List[str] = result_set[:end_index]
        dataset = [value for value in dataset if "Objections" not in value]
        start_index = result_set.index("Start Date")
        result_set = result_set[start_index:]
        result_set = dataset + result_set
        result_set = [value for value in result_set if "Type" not in value]
        result_set = [value for value in result_set if "Start Date" not in value]
        result_set = [value for value in result_set if "End Date" not in value]
        result_set = [value for value in result_set if "Status" not in value]
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader._extractDataDomesticCivilCivilDetails()")
            exit()
        else:
            return []

    def _extractDataDomesticCivilCivilAdministrators(self, result_set: List[str]) -> Dict[str, Union[Dict[str, Union[str, int]], List[int]]]:
        """
        Extracting the administrators of a société civile.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {administrator: {name: string, date_appointed: int, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}
        """
        start_index: int = result_set.index("Administrators")
        end_index: int = result_set.index("Start Date")
        result_set = result_set[start_index:end_index]
        administrator: Dict[str, Union[str, int]] = self.__extractDataDomesticCivilCivilAdministrators(result_set)
        accounts: List[Dict[str, int]] = self._extractDataDomesticCivilCivilAdministratorsAccounts(result_set)
        if not administrator and len(accounts) == 0:
            return {}
        else:
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
        start_index: int = result_set.index("Receivers")
        end_index: int = result_set.index("Accounts of Administrator")
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if "Page" not in value]
        result_set = [value for value in result_set if "Date Issued" not in value]
        result_set = [value for value in result_set if " of " not in value]
        receiver: Dict[str, Union[str, int]] = self.__extractDataDomesticCivilCivilReceivers(result_set)
        reports: List[Dict[str, int]] = self._extractDataDomesticCivilCivilReports(result_set)
        affidavits: List[Dict[str, int]] = self._extractDataDomesticCivilCivilAffidavits(result_set)
        if not receiver and len(reports) == 0 and len(affidavits) == 0:
            return {}
        else:
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
        Extracting the receiver that is related to the receivers of a société civile.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {name: string, date_appointed: int, address: string}
        """
        start_index: int = result_set.index("Receivers") + 1
        end_index: int = result_set.index("Date Filed")
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if ":" not in value]
        if len(result_set) >= 3:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader._extractReceivers()")
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
        start_index: int = result_set.index("Liquidators")
        end_index: int = result_set.index("Receivers")
        result_set = result_set[start_index:end_index]
        liquidator: Dict[str, Union[str, int]] = self._extractLiquidators(result_set)
        affidavits: List[Dict[str, int]] = self.extractLiquidatorsAffidavits(result_set)
        if not liquidator and len(affidavits) == 0:
            return {}
        else:
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
        response: List[Dict[str, Union[str, int]]] = []
        start_index: int = result_set.index("Associes")
        result_set = result_set[start_index:]
        start_index = result_set.index("Currency") + 1
        end_index: int = result_set.index("Liquidators")
        result_set = result_set[start_index:end_index]
        amounts: List[int] = self._extractDataDomesticCivilCivilShareholdersAmount(result_set)
        shareholders_types: Dict[str, List[str]] = self._extractDataDomesticCivilCivilShareholdersType(result_set)
        types: List[str] = shareholders_types["types"]
        result_set = shareholders_types["result_set"]
        names: List[str] = [value for value in result_set if bool(search(r"[A-Z\s]+", value)) == True and bool(search(r"[a-z]+", value)) == False]
        currencies: List[str] = [value for value in result_set if value not in names]
        for index in range(0, min([len(amounts), len(types), len(names), len(currencies)]), 1):
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
        dataset = [value for value in result_set if bool(search(r"[\d]+", value)) == True]
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
        for index in range(0, len(result_set), 1):
            amounts: List[str] = findall(r"[\d]+", result_set[index])
            amount: Union[int, str] = self._extractShareholdersAmountShares(amounts) # type: ignore
            response = self.__extractShareholdersAmountShares(response, amount) # type: ignore
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
        start_index: int = result_set.index("Office Bearers") + 1
        end_index: int = result_set.index("Currency")
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if "Associes" not in value]
        result_set = [value for value in result_set if "Type of Shares" not in value]
        result_set = [value for value in result_set if "Position" not in value]
        result_set = [value for value in result_set if "Name" not in value]
        result_set = [value for value in result_set if "Service Address" not in value]
        result_set = [value for value in result_set if "Appointed Date" not in value]
        date_appointeds: List[str] = self._extractDataDomesticCivilCivilOfficeBearersDateAppointed(result_set)
        result_set = [value for value in result_set if value not in date_appointeds]
        office_bearers_addresses: Dict[str, List[str]] = self._extractDataDomesticCivilCivilOfficeBearersAddresses(result_set)
        result_set = office_bearers_addresses["result_set"]
        addresses: List[str] = office_bearers_addresses["addresses"]
        positions: List[str] = self._extractDataDomesticCivilCivilOfficeBearersPositions(result_set)
        names: List[str] = [value for value in result_set if value not in positions]
        for index in range(0, min([len(date_appointeds), len(addresses), len(positions), len(names)]), 1):
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
        for index in range(0, len(result_set), 1):
            date_appointed: str = " ".join(findall(r"[\d/]+", result_set[index]))
            date_appointed = self.__extractDataDomesticCivilCivilOfficeBearersDateAppointed(date_appointed)
            response = self.___extractDataDomesticCivilCivilOfficeBearersDateAppointed(response, date_appointed)
        return response

    def ___extractDataDomesticCivilCivilOfficeBearersDateAppointed(self, response: List[str], date_appointed: str) -> List[str]:
        """
        Building the response needed for the date appointed of an
        office bearer.

        Parameters:
            response: [string]: The data to be returned
            date_appointed: string: The date of appointment of the office bearer.

        Returns:
            [string]
        """
        if date_appointed != "NaDA":
            response.append(date_appointed)
        return response

    def __extractDataDomesticCivilCivilOfficeBearersDateAppointed(self, date_appointed: str) -> str:
        """
        Ensuring that the date appointed is retrieved from the
        result set.

        Parameters:
            date_appointed: string: The date at which the office bearer has been appointed.

        Returns:
            string
        """
        if "/" in date_appointed:
            return date_appointed
        else:
            return "NaDA"

    def _extractDataDomesticCivilCivilStateCapital(self, result_set: List[str]) -> List[Dict[str, Union[str, int]]]:
        """
        Extracting the state capital of a socitété civile.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}]
        """
        response: List[Dict[str, Union[str, int]]] = []
        start_index: int = result_set.index("Particulars of Stated Capital") + 1
        end_index: int = result_set.index("Office Bearers")
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if "Type of Shares" not in value]
        result_set = [value for value in result_set if "No. of Shares Currency" not in value]
        result_set = [value for value in result_set if "Stated Capital" not in value]
        result_set = [value for value in result_set if "Amount Unpaid" not in value]
        result_set = [value for value in result_set if "Valeur" not in value]
        result_set = [value for value in result_set if "Nominale" not in value]
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
        response: List[int] = []
        for index in range(0, len(result_set), 1):
            amount_unpaid: str = " ".join(findall(r"[\d\sA-Z]+", result_set[index]))
            amount_unpaid: str = self.__extractDataDomesticCivilCivilStateCapitalAmountUnpaid(amount_unpaid)
            response = self.___extractDataDomesticCivilCivilStateCapitalAmountUnpaid(response, amount_unpaid)
        return response

    def ___extractDataDomesticCivilCivilStateCapitalAmountUnpaid(self, response: List[int], amount_unpaid: str) -> List[int]:
        """
        Building the response needed for the amount unpaid of the
        state capital of an authorised company.

        Parameters:
            response: [int]: The data to be returned.
            amount_unpaid: string: The amount unpaid that has been processed.

        Returns:
            [int]
        """
        if amount_unpaid != "NaAU":
            response.append(int(amount_unpaid))
        return response

    def __extractDataDomesticCivilCivilStateCapitalAmountUnpaid(self, amount_unpaid: str) -> str:
        """
        Sanitizing the Amount Unpaid of the state capital of an
        authorised company.

        Parameters:
            amount_unpaid: string: The data to be processed/

        Returns:
            string
        """
        if bool(search(r"[A-z]+", amount_unpaid)) == False:
            return amount_unpaid.split(" ")[0]
        else:
            return "NaAU"

    def _extractDataDomesticCivilCivilStateCapitalStatedCapital(self, result_set: List[str]) -> List[int]:
        """
        Extracting the stated capital of the stated capital of an
        authorised company.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [int]
        """
        response: List[int] = []
        for index in range(0, len(result_set), 1):
            stated_capital: str = " ".join(findall(r"[\d\sA-Z]+", result_set[index]))
            stated_capital = self.__extractDataDomesticCivilCivilStateCapitalStatedCapital(stated_capital)
            response = self.___extractDataDomesticCivilCivilStateCapitalStatedCapital(response, stated_capital)
        return response

    def ___extractDataDomesticCivilCivilStateCapitalStatedCapital(self, response: List[int], stated_capital: str) -> List[int]:
        """
        Bulding the response to be returned for processing.

        Parameters:
            response: [int]: The data to be returned.
            stated_capital: string: The data to be verified.

        Returns:
            [int]
        """
        if stated_capital != "NaSC":
            response.append(int(stated_capital))
        return response

    def __extractDataDomesticCivilCivilStateCapitalStatedCapital(self, stated_capital: str) -> str:
        """
        Retrieving the correct stated capital from the processed
        dataset.

        Parameters:
            stated_capital: string: The stated capital that has been processed.

        Returns:
            string
        """
        if bool(search(r"[\s]", stated_capital)) == False:
            return stated_capital
        else:
            return "NaSC"

    def _extractDataDomesticCivilCivilStateCapitalTypes(self, result_set: List[str]) -> List[str]:
        """
        Extracting the types from the state capital of a société
        civile.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [string]
        """
        response: List[str] = []
        for index in range(0, len(result_set), 1):
            types: str = " ".join(findall(r"^[A-z\s]+", result_set[index]))
            type: str = self.__extractDataDomesticCivilCivilStateCapitalTypes(types)
            response = self.___extractDataDomesticCivilCivilStateCapitalTypes(response, type)
        return response

    def ___extractDataDomesticCivilCivilStateCapitalTypes(self, response: List[str], type: str) -> List[str]:
        """
        Building the response to be returned with the types of
        shares.

        Parameters:
            response: [string]: The data to be returned.
            type: string: The type of shares.

        Returns:
            [string]
        """
        if type != "NaT":
            response.append(type)
        return response

    def __extractDataDomesticCivilCivilStateCapitalTypes(self, types: str) -> str:
        """
        Processing the types of shares to be returned for
        processing.

        Parameters:
            types: string: The data to be processed.

        Returns:
            string
        """
        if types != "":
            return types
        else:
            return "NaT"

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
        response: List[int] = []
        for index in range(0, len(result_set), 1):
            amounts: str = " ".join(findall(r"[\d\sA-Z]+", result_set[index]))
            amount: str = self.__extractDataDomesticCivilCivilStateCapitalAmount(amounts)
            response = self.___extractDataDomesticCivilCivilStateCapitalAmount(response, amount)
        return response

    def ___extractDataDomesticCivilCivilStateCapitalAmount(self, response: List[int], amount: str) -> List[int]:
        """
        Building the array which contains the amount of shares of
        the stated capital for a société civile.

        Parameters:
            response: [int]: The array to be returned.
            amount: str: The amount to be processed.

        Returns:
            [int]
        """
        if amount != "NaA":
            response.append(int(amount))
        return response

    def __extractDataDomesticCivilCivilStateCapitalAmount(self, amount: str) -> str:
        """
        Retrieving the correct value for the amount of shares for a
        stated capital for a société civile.

        Parameters:
            amount: string: The value to be processed.

        Returns:
            string
        """
        if bool(search(r"[\d]+", amount)) and bool(search(r"[A-Z]+", amount)):
            return " ".join(findall(r"[\d]+", amount))
        else:
            return "NaA"

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

    def _extractDataDomesticCivilCivilCompanyDetails(self, result_set: List[str]) -> Dict[str, Union[str, int]]:
        """
        Extracting the company details of a société civile.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}
        """
        response: Dict[str, Union[str, int]]
        start_index: int = result_set.index("Partnership Details") + 1
        end_index: int = result_set.index("Business Details")
        result_set = result_set[start_index:end_index]
        result_set.remove("Registrar of Companies")
        category: str = result_set[[index for index, value in enumerate(result_set) if "Category" in value][0]].split(": ")[-1]
        result_set = result_set + [category]
        result_set = [value for value in result_set if ":" not in value]
        response = {
            "name": result_set[1].title(),
            "file_number": result_set[0],
            "category": result_set[5].title(),
            "date_incorporation": int(datetime.strptime(result_set[2], "%d/%m/%Y").timestamp()),
            "nature": result_set[3].title(),
            "status": result_set[4].title()
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
        if status == 201:
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
            state_capital: List[Dict[str, Union[str, int]]] = self.extractStateCapital(portable_document_file_data_result_set)
            balance_sheet: Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]] = self.extractBalanceSheet(portable_document_file_data_result_set)
            charges: List[Dict[str, Union[int, str]]] = self.extractCharges(portable_document_file_data_result_set)
            liquidators: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]] = self.extractLiquidators(portable_document_file_data_result_set)
            receivers: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]] = self.extractReceivers(portable_document_file_data_result_set)
            administrators: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]] = self.extractAdministrators(portable_document_file_data_result_set)
            details: List[Dict[str, Union[str, int]]] = self.extractDetails(portable_document_file_data_result_set)
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
                "state_capital": state_capital,
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

    def extractObjections(self, portable_document_file_result_set: List[str]) -> List[Dict[str, Union[int, str]]]:
        """
        Extracting the objections from the result set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{date_objection: int, objector: string}]
        """
        start_index: int = portable_document_file_result_set.index("Objection Date")
        end_index: int = portable_document_file_result_set.index("Last Annual Registration Fee Paid:")
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        result_set = [value for value in result_set if "Object" not in value]
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractObjections()")
            exit()
        else:
            return []

    def extractDetails(self, portable_document_file_result_set: List[str]) -> List[Dict[str, Union[str, int]]]:
        """
        Extracting the details from the result set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{type: string, date_start: int, date_end: int, status: string}]
        """
        start_index: int = portable_document_file_result_set.index("Winding Up Details")
        end_index: int = portable_document_file_result_set.index("Page 6")
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        result_set.remove("Winding Up Details")
        result_set.remove("Objections")
        result_set.remove("Objection Date")
        result_set.remove("Objector")
        result_set.remove("Type")
        result_set.remove("Start Date")
        result_set.remove("End Date")
        result_set.remove("Status")
        result_set = [value for value in result_set if ":" not in value]
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractDetails()")
            exit()
        else:
            return []

    def extractAdministrators(self, portable_document_file_result_set: List[str]) -> Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]:
        """
        Extracting the administrators from the result set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {administrator: {name: string, date_appointed: int, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}
        """
        start_index: int = portable_document_file_result_set.index("Administrators")
        end_index: int = portable_document_file_result_set.index("Page 6")
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        administrator: Dict[str, Union[str, int]] = self._extractAdministrators(result_set)
        accounts: List[Dict[str, int]] = self.extractAdministratorsAccounts(result_set)
        if not administrator and len(accounts) == 0:
            return {}
        else:
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
        start_index: int = portable_document_file_result_set.index("Receivers")
        end_index: int = portable_document_file_result_set.index("Accounts of Administrator") + 1
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        receiver: Dict[str, Union[str, int]] = self._extractReceivers(result_set)
        reports: List[Dict[str, int]] = self.extractReceiversReports(result_set)
        affidavits: List[Dict[str, int]] = self.extractReceiversAffidavits(result_set)
        if not receiver and len(reports) == 0 and len(affidavits) == 0:
            return {}
        else:
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
        start_index: int = result_set.index("Affidavits of Receiver") + 1
        end_index: int = result_set.index("Administrators")
        result_set = result_set[start_index:end_index]
        result_set = result_set + date_to
        result_set.remove("Date Filed")
        result_set.remove("From")
        result_set.remove("To")
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader._extractReceivers()")
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
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader._extractReceivers()")
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
        start_index: int = portable_document_file_result_set.index("Liquidators")
        end_index: int = portable_document_file_result_set.index("Receivers")
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        liquidator: Dict[str, Union[str, int]] = self._extractLiquidators(result_set)
        affidavits: List[Dict[str, int]] = self.extractLiquidatorsAffidavits(result_set)
        if not liquidator and len(affidavits) == 0:
            return {}
        else:
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
        start_index: int = result_set.index("Affidavits of Liquidator")
        end_index: int = result_set.index("To") + 2
        result_set = result_set[start_index:end_index]
        result_set.remove("Affidavits of Liquidator")
        result_set.remove("Date Filed")
        result_set.remove("From")
        result_set.remove("To")
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractLiquidatorsAffidavits()")
            exit()
        else:
            return []

    def _extractLiquidators(self, result_set: List[str]) -> Dict[str, Union[str, int]]:
        """
        Extracting the liquidator that is related to the
        liquidators.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {name: string, date_appointed: int, address: string}
        """
        start_index: int = result_set.index("Liquidators") + 1
        end_index: int = result_set.index("From")
        result_set = result_set[start_index:end_index]
        result_set.remove("Affidavits of Liquidator")
        result_set.remove("Name:")
        result_set.remove("Address:")
        result_set.remove("Date Filed")
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractCharges()")
            exit()
        else:
            return {}


    def extractCharges(self, portable_document_file_result_set: List[str]) -> List[Dict[str, Union[int, str]]]:
        """
        Extracting the charges from the result set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{volume: int, property: string, nature: string, amount: int, date_charged: int, date_filled: int, currency: string}]
        """
        start_index: int = portable_document_file_result_set.index("Charges")
        end_index: int = portable_document_file_result_set.index("Liquidators")
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        result_set.remove("Charges")
        result_set.remove("Volume")
        result_set.remove("Property")
        result_set.remove("Nature")
        result_set = [value for value in result_set if "Amount" not in value]
        result_set.remove("Date Filed")
        result_set.remove("Currency")
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractCharges()")
            exit()
        else:
            return []

    def extractBalanceSheet(self, portable_document_file_result_set: List[str]) -> Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]]:
        """
        Extracting the data for the balance sheets from the result
        set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {balance_sheet: {financial_year: int, currency: string, unit: int}, assets: {non_current_assets: {property_plant_equipment: float, investment_properties: float, intangible_assets: float, other_investments: float, subsidiaries_investments: float, biological_assets: float, others: float, total: float}, current_assets: {inventories: float, trade: float, cash: float, others: float, total: float}, total: float}, liabilities: {equity_and_liabilities: {share_capital: float, other_reserves: float, retained_earnings: float, others: float, total: float}, non_current: {long_term_borrowings: float, deferred_tax: float, long_term_provisions: float, others: float, total: float}, current: {trade: float, short_term_borrowings: float, current_tax_payable: float, short_term_provisions: float, others: float, total: float}, total_liabilities: float, total_equity_and_liabilities: float}}
        """
        start_index: int = portable_document_file_result_set.index("BALANCE SHEET")
        end_index: int = portable_document_file_result_set.index("Charges")
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        balance_sheet: Dict[str, Union[int, str]] = self._extractBalanceSheet(result_set)
        assets: Dict[str, Union[Dict[str, float], float]] = self.extractBalanceSheetAssets(result_set)
        liabilities: Dict[str, Union[Dict[str, float], float]] = self.extractBalanceSheetLiabilities(result_set)
        if not balance_sheet and not assets and not liabilities:
            return {}
        else:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractBalanceSheet()")
            exit()

    def extractBalanceSheetLiabilities(self, result_set: List[str]) -> Dict[str, Union[Dict[str, float], float]]:
        """
        Extracting the liabilities that is linked to the balance sheet.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {equity_and_liabilities: {share_capital: float, other_reserves: float, retained_earnings: float, others: float, total: float}, non_current: {long_term_borrowings: float, deferred_tax: float, long_term_provisions: float, others: float, total: float}, current: {trade: float, short_term_borrowings: float, current_tax_payable: float, short_term_provisions: float, others: float, total: float}, total_liabilities: float, total_equity_and_liabilities: float}
        """
        start_index: int = result_set.index("EQUITY AND LIABILITIES")
        end_index: int = result_set.index("TOTAL EQUITY AND LIABILITIES") + 2
        result_set = result_set[start_index:end_index]
        equity: Dict[str, float] = self.extractBalanceSheetLiabilitiesEquity(result_set)
        non_current: Dict[str, float] = self.extractBalanceSheetLiabilitiesNonCurrent(result_set)
        current: Dict[str, float] = self.extractBalanceSheetLiabilitiesCurrent(result_set)
        if not equity and not non_current and not current:
            return {}
        else:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractBalanceSheetLiabilities()")
            exit()

    def extractBalanceSheetLiabilitiesCurrent(self, result_set: List[str]) -> Dict[str, float]:
        """
        Extracting the current liabilities that is linked to the
        liabilities.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {trade: float, short_term_borrowings: float, current_tax_payable: float, short_term_provisions: float, others: float, total: float}
        """
        start_index: int = result_set.index("CURRENT LIABILITIES") + 1
        end_index: int = result_set.index("TOTAL LIABILITIES")
        result_set = result_set[start_index:end_index]
        result_set.remove("Trade and Other Payables")
        result_set.remove("Short Term Borrowings")
        result_set.remove("Current Tax Payable")
        result_set.remove("Short Term Provisions")
        result_set.remove("Others")
        result_set.remove("TOTAL CURRENT LIABILITIES")
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractBalanceSheetLiabilitiesCurrent()")
            exit()
        else:
            return {}

    def extractBalanceSheetLiabilitiesNonCurrent(self, result_set: List[str]) -> Dict[str, float]:
        """
        Extracting the non-current liabilities that is linked to the
        liabilities.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {long_term_borrowings: float, deferred_tax: float, long_term_provisions: float, others: float, total: float}
        """
        start_index: int = result_set.index("NON-CURRENT LIABILITIES") + 1
        end_index: int = result_set.index("CURRENT LIABILITIES")
        result_set = result_set[start_index:end_index]
        result_set.remove("Long Term Borrowings")
        result_set.remove("Deferred Tax")
        result_set.remove("Long Term Provisions")
        result_set.remove("Others")
        result_set.remove("TOTAL")
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractBalanceSheetLiabilitiesNonCurrent()")
            exit()
        else:
            return {}

    def extractBalanceSheetLiabilitiesEquity(self, result_set: List[str]) -> Dict[str, float]:
        """
        Extracting the equities that is linked to the liabilities.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {share_capital: float, other_reserves: float, retained_earnings: float, others: float, total: float}
        """
        start_index: int = result_set.index("EQUITY AND LIABILITIES") + 1
        end_index: int = result_set.index("NON-CURRENT LIABILITIES")
        result_set = result_set[start_index:end_index]
        result_set.remove("Share Capital")
        result_set.remove("Other Reserves")
        result_set.remove("Retained Earnings")
        result_set.remove("Others")
        result_set.remove("TOTAL")
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractBalanceSheetLiabilitiesEquity()")
            exit()
        else:
            return {}

    def extractBalanceSheetAssets(self, result_set: List[str]) -> Dict[str, Union[Dict[str, float], float]]:
        """
        Extracting the assets that is linked to the balance sheet.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {non_current_assets: {property_plant_equipment: float, investment_properties: float, intangible_assets: float, other_investments: float, subsidiaries_investments: float, biological_assets: float, others: float, total: float}, current_assets: {inventories: float, trade: float, cash: float, others: float, total: float}, total: float}
        """
        start_index: int = result_set.index("NON-CURRENT ASSETS")
        end_index: int = result_set.index("TOTAL ASSETS") + 2
        result_set = result_set[start_index:end_index]
        non_current: Dict[str, float] = self.extractBalanceSheetAssetsNonCurrent(result_set)
        current: Dict[str, float] = self.extractBalanceSheetAssetsCurrent(result_set)
        if not non_current and not current:
            return {}
        else:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractBalanceSheetAssets()")
            exit()

    def extractBalanceSheetAssetsCurrent(self, result_set: List[str]) -> Dict[str, float]:
        """
        Extracting the current assets that is linked to the assets.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {inventories: float, trade: float, cash: float, others: float, total: float}
        """
        start_index: int = result_set.index("CURRENT ASSETS") + 1
        end_index: int = result_set.index("TOTAL ASSETS") + 2
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if "Page" not in value]
        result_set.remove("Inventories")
        result_set.remove("Trade and Other Receivables")
        result_set.remove("Cash and Cash Equivalents")
        result_set.remove("Others")
        result_set.remove("TOTAL")
        result_set.remove("TOTAL ASSETS")
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractBalanceSheetAssetsCurrent()")
            exit()
        else:
            return {}

    def extractBalanceSheetAssetsNonCurrent(self, result_set: List[str]) -> Dict[str, float]:
        """
        Extracting the non-current assets that is linked to the
        assets.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {property_plant_equipment: float, investment_properties: float, intangible_assets: float, other_investments: float, subsidiaries_investments: float, biological_assets: float, others: float, total: float}
        """
        start_index: int = result_set.index("NON-CURRENT ASSETS") + 1
        end_index: int = result_set.index("CURRENT ASSETS")
        result_set = result_set[start_index:end_index]
        result_set.remove("Property, Plant and Equipment")
        result_set.remove("Investment Properties")
        result_set.remove("Intangible Assets")
        result_set.remove("Other Investments")
        result_set.remove("Investment in Subsidiaries")
        result_set.remove("Biological Assets")
        result_set.remove("Others")
        result_set.remove("TOTAL")
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractBalanceSheetAssetsNonCurrent()")
            exit()
        else:
            return {}

    def _extractBalanceSheet(self, result_set: List[str]) -> Dict[str, Union[int, str]]:
        """
        Extracting the balance sheet that is linked to the balance
        sheet.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {financial_year: int, currency: string, unit: int}
        """
        start_index: int = result_set.index("BALANCE SHEET") + 1
        end_index: int = result_set.index("NON-CURRENT ASSETS")
        result_set = result_set[start_index:end_index]
        result_set.remove("Financial Year Ended:")
        result_set.remove("Currency:")
        result_set.remove("Unit:")
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader._extractBalanceSheet()")
            exit()
        else:
            return {}

    def _extractProfitStatements(self, result_set: List[str]) -> Dict[str, Union[int, str]]:
        """
        Extracting the financial summary that is linked to the
        profit statement.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {financial_year: int, currency: string, date_approved: int, unit: int}
        """
        start_index: int = result_set.index("Last Financial Summary Filed") + 1
        end_index: int = result_set.index("Turnover")
        result_set = result_set[start_index:end_index]
        result_set.remove("PROFIT AND LOSS STATEMENT")
        result_set.remove("Financial Year Ended:")
        result_set.remove("Date Approved:")
        result_set.remove("Currency:")
        result_set.remove("Unit:")
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader._extractProfitStatements()")
            exit()
        else:
            return {}

    def extractProfitStatements(self, portable_document_file_result_set: List[str]) -> Dict[str, Union[Dict[str, Union[int, str]], float]]:
        """
        Extracting the profit data for the profit statements from
        the result set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            {financial_summary: {financial_year: int, currency: string, date_approved: int, unit: int}, turnover: float, cost_of_sales: float, gross_profit: float, other_income: float, distribution_cost: float, administration_cost: float, expenses: float, finance_cost: float, net_profit_before_taxation: float, taxation: float, net_profit: float}
        """
        start_index: int = portable_document_file_result_set.index("Last Financial Summary Filed")
        end_index: int = portable_document_file_result_set.index("BALANCE SHEET")
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        financial_summary: Dict[str, Union[int, str]] = self._extractProfitStatements(result_set)
        start_index = result_set.index("Turnover")
        end_index = result_set.index("PROFIT/(LOSS) FOR THE PERIOD") + 2
        result_set = result_set[start_index:end_index]
        result_set = [value for value in result_set if "Page" not in value]
        result_set.remove("Turnover")
        result_set.remove("Less Cost of Sales")
        result_set.remove("GROSS PROFIT")
        result_set.remove("Add Other Income")
        result_set.remove("Less: Distribution Costs")
        result_set.remove("Administration Costs")
        result_set.remove("Finance Costs")
        result_set.remove("PROFIT/(LOSS) BEFORE TAX")
        result_set.remove("Tax Expense")
        result_set.remove("Other Expenses")
        result_set.remove("PROFIT/(LOSS) FOR THE PERIOD")
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractProfitStatements()")
            exit()
        else:
            return {}

    def extractFinancialSummaries(self, portable_document_file_result_set: List[str]) -> List[Dict[str, Union[int, str]]]:
        """
        Extracting the data for the financial summaries from the
        result set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{financial_year: int, currency: string, date_approved: int, unit: int}]
        """
        start_index: int = portable_document_file_result_set.index("Financial Summary/Statements filed for last 3 years") + 1
        end_index: int = portable_document_file_result_set.index("Last Financial Summary Filed") - 4
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        result_set.remove("Financial Year Ended")
        result_set.remove("Currency")
        result_set.remove("Date Approved")
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractFinancialSummaries()")
            exit()
        else:
            return []

    def extractAnnualReturns(self, portable_document_file_result_set: List[str]) -> List[Dict[str, int]]:
        """
        Extracting the data for the annual returns from the result
        set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{date_annual_return: int, date_annual_meeting: int, date_filled: int}]
        """
        start_index: int = portable_document_file_result_set.index("Annual Return filed for last 3 years") + 1
        end_index: int = portable_document_file_result_set.index("Financial Summary/Statements filed for last 3 years")
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        result_set = [value for value in result_set if ":" not in value]
        result_set = [value for value in result_set if "Page" not in value]
        result_set = [value for value in result_set if "of" not in value]
        result_set.remove("Date Annual Return")
        result_set.remove("Annual Meeting Date")
        result_set.remove("Date Filed")
        if len(result_set) >= 3:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractAnnualReturns()")
            exit()
        else:
            return []

    def extractMembers(self, portable_document_file_result_set: List[str]) -> List[Dict[str, Union[str, int]]]:
        """
        Extracting the data for the members from the result set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{name: string, amount: int, date_start: int, currency: string}]
        """
        start_index: int = portable_document_file_result_set.index("Members (Applicable for Company Limited by Guarantee or Shares and Guarantee)") + 1
        end_index: int = portable_document_file_result_set.index("Annual Return filed for last 3 years")
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        result_set = [value for value in result_set if "Date" not in value]
        result_set = [value for value in result_set if "/" not in value]
        result_set = [value for value in result_set if "Page" not in value]
        result_set = [value for value in result_set if " of " not in value]
        result_set.remove("Name")
        result_set.remove("Amount")
        result_set.remove("Currency")
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractMembers()")
            exit()
        else:
            return []

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
        result_set.remove("Certificate (Issued by Other Institutions)")
        result_set.remove("Certificate")
        result_set.remove("Type")
        result_set.remove("Effective Date")
        result_set.remove("Expiry Date")
        if len(result_set) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Document_Reader.extractCertificates()")
            exit()
        else:
            return []

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
        types: List[str] = [value for value in result_set if bool(search(r"[\d]+", value)) == True]
        for index in range(0, len(types), 1):
            response.append(" ".join([value for value in types[index].split(" ") if bool(search(r"[A-Z]+", value)) == True]))
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
        amounts: List[str] = [value for value in result_set if bool(search(r"[\d]+", value)) == True]
        for index in range(0, len(amounts), 1):
            response.append(int("".join([value for value in amounts[index].split(" ") if bool(search(r"[\d]+", value)) == True])))
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
        dataset: List[str] = [value for value in result_set if bool(search(r"[\d]+", value)) == True]
        amount_of_shares: List[int] = self.extractShareholdersAmountShares(result_set)
        type_of_shares: List[str] = self.extractShareholdersTypeShares(result_set)
        result_set = [value for value in result_set if value not in dataset]
        names: List[str] = [value for value in result_set if bool(search(r"[A-Z\s]+", value)) == True and bool(search(r"[a-z]+", value)) == False]
        result_set = [value for value in result_set if value not in dataset]
        currencies: List[str] = [value for value in result_set if value not in names]
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
        for index in range(0, len(result_set), 1):
            names: List[str] = findall(r"\b[A-Z]+\b", result_set[index])
            names = [value for value in names if value != "MAURITIUS"]
            names = [value for value in names if len(value) > 1]
            name: str = self._extractOfficeBearersNames(names)
            response = self.__extractNames(response, name)
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
        result_set.remove("Position")
        result_set = [value for value in result_set if "Name" not in value]
        result_set.remove("Service Address")
        result_set.remove("Appointed Date")
        result_set.remove("Shareholders")
        date_appointments: List[str] = self.extractOfficeBearersDateAppointments(result_set)
        result_set = [value for value in result_set if value not in date_appointments]
        positions: List[str] = self.extractOfficeBearersPositions(result_set)
        result_set = [value for value in result_set if value not in positions]
        names: List[str] = self.extractOfficeBearersNames(result_set)
        result_set = [value for value in result_set if value not in names]
        addresses: List[str] = self.extractOfficeBearersAddresses(result_set)
        for index in range(0, len(date_appointments), 1):
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

    def extractStateCapital(self, portable_document_file_result_set: List[str]) -> List[Dict[str, Union[str, int]]]:
        """
        Extracting the data for the share capital from the result
        set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}]
        """
        response: List[Dict[str, Union[str, int]]] = []
        start_index: int = portable_document_file_result_set.index("Particulars of Stated Capital") + 1
        end_index: int = portable_document_file_result_set.index("Certificate (Issued by Other Institutions)")
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        result_set = [value for value in result_set if "Type of Shares" not in value]
        result_set = [value for value in result_set if "No. of Shares Currency" not in value]
        result_set = [value for value in result_set if "Stated Capital" not in value]
        result_set = [value for value in result_set if "Amount Unpaid Par Value" not in value]
        types: List[str] = [f"{value} SHARES" for value in " ".join([value for value in result_set if bool(search(r"[A-Z]+", value)) == True and bool(search(r"[a-z]+", value)) == False]).split(" SHARES") if value != ""]
        dataset: List[str] = [value for value in result_set if bool(search(r"[A-Z]+", value)) == True and bool(search(r"[a-z]+", value)) == False]
        result_set = [value for value in result_set if value not in dataset]
        amounts: List[int] = self.extractStateCapitalAmount(result_set)
        currencies: List[str] = self.extractStateCapitalCurrency(result_set)
        dataset = [value for value in result_set if bool(search(r"[\d]+", value)) == True and bool(search(r"[A-z]+", value)) == True]
        result_set = [value for value in result_set if value not in dataset]
        stated_capitals: List[int] = self.extractStateCapitalStatedCapital(result_set)
        dataset = [value for value in result_set if bool(search(r"[\d]+", value)) == True and "," in value]
        result_set = [value for value in result_set if value not in dataset]
        amount_unpaids: List[int] = self.extractStateCapitalAmountUnpaid(result_set)
        share_values: List[int] = self.extractStateCapitalShareValue(result_set)
        for index in range(0, min([len(types), len(amounts), len(currencies), len(stated_capitals), len(amount_unpaids), len(share_values)]), 1):
            response.append({
                "type": types[index],
                "amount": amounts[index],
                "currency": currencies[index],
                "stated_capital": stated_capitals[index],
                "amount_unpaid": amount_unpaids[index],
                "par_value": share_values[index]
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

    def extractStateCapitalAmountUnpaid(self, result_set: List[str]) -> List[int]:
        """
        Extracting the amount unpaid of the stated capital of a
        private domestic company.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [int]
        """
        response: List[int] = []
        for index in range(0, len(result_set), 1):
            response.append(int(result_set[index].split(" ")[0]))
        return response

    def extractStateCapitalStatedCapital(self, result_set: List[str]) -> List[int]:
        """
        Extracting the stated capital of the stated capital of a
        private domestic company.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [int]
        """
        response: List[int] = []
        stated_capitals: List[str] = [value for value in result_set if bool(search(r"[\d]+", value)) == True and "," in value]
        for index in range(0, len(stated_capitals), 1):
            stated_capital: int = int(stated_capitals[index].replace(",", ""))
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
        end_index: int = portable_document_file_result_set.index("Particulars of Stated Capital")
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        result_set = [value for value in result_set if "Business" not in value]
        operational_addresses: List[str] = self.extractBusinessDetailsOperationalAddresses(result_set)
        dataset: List[str] = [value for value in result_set if bool(search(r"[A-Z]+", value)) == True and bool(search(r"[a-z]+", value)) == False]
        result_set = [value for value in result_set if value not in dataset]
        dataset: List[str] = [value for value in result_set if bool(search(r"[A-Z]+", value)) == True and bool(search(r"[a-z]+", value)) == True]
        natures: List[str] = self.extractBusinessDetailsNatures(result_set)
        result_set = [value for value in result_set if value not in dataset]
        names: List[str] = result_set
        for index in range(0, min([len(names), len(natures), len(operational_addresses)]), 1):
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
        natures: List[str] = [value for value in result_set if bool(search(r"[A-Z]+", value)) == True and bool(search(r"[a-z]+", value)) == True]
        for index in range(0, len(natures), 1):
            response.append(natures[index])
        return response

    def extractBusinessDetailsOperationalAddresses(self, result_set: List[str]) -> List[str]:
        """
        Extracting the operational addresses that are linked to the
        business details of private domestic companies.

        Parameters:
            result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [string]
        """
        response: List[str] = []
        operational_addresses: List[str] = [value for value in result_set if bool(search(r"[A-Z]+", value)) == True and bool(search(r"[a-z]+", value)) == False]
        for index in range(0, len(operational_addresses), 1):
            response.append(" ".join([value for value in operational_addresses[index].split(" ") if value != ""]))
        return response

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
        business_registration_number: str = result_set[[index for index, value in enumerate(result_set) if "Business Registration No.:" in value][0]].split(" ")[-1]
        result_set = result_set + [business_registration_number]
        result_set = [value for value in result_set if ":" not in value]
        result_set.remove("Business Details")
        result_set.remove("Registrar of Companies")
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