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

    def extractData(self, status: int, dataset: DocumentFiles) -> Dict:
        """
        Extracting the data from the portable document file version
        of the corporate registry based on the status of the file
        generation as well as on the dataset.

        Parameters:
            status: int: The status of the file generation.
            dataset: {identifier: int, file_data: bytes, company_detail: int}: The dataset of the corporate registry retrieved from the relational database server.

        Returns:
            {status: int, company_details: {business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}, business_details: [{registered_address: string, name: string, nature: string, operational: string}], state_capital: {type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}, office_bearers: {position: string, name: string, address: string, date_appointment: int}, shareholders: [{name: string, amount: int, type: string, currency: string}]}
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
            certificates: List[Dict[str, Union[str, int]]] = self.extractCertificates(portable_document_file_data_result_set)
            office_bearers: List[Dict[str, Union[str, int]]] = self.extractOfficeBearers(portable_document_file_data_result_set)
            shareholders: List[Dict[str, Union[str, int]]] = self.extractShareholders(portable_document_file_data_result_set)
            members: List[Dict[str, Union[str, int]]] = self.extractMembers(portable_document_file_data_result_set)
            annual_return: List[Dict[str, int]] = self.extractAnnualReturns(portable_document_file_data_result_set)
            financial_summaries: List[Dict[str, Union[int, str]]] = self.extractFinancialSummaries(portable_document_file_data_result_set)
            profit_statement: Dict[str, Union[Dict[str, Union[int, str]], float]] = self.extractProfitStatements(portable_document_file_data_result_set)
            state_capital: Dict[str, Union[str, int]] = self.extractStateCapital(portable_document_file_data_result_set)
            balance_sheet: Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]] = self.extractBalanceSheet(portable_document_file_data_result_set)
            print(f"{portable_document_file_data_result_set=}\n{company_details=}\n{business_details=}\n{state_capital=}\n{certificates=}\n{office_bearers=}\n{shareholders=}\n{members=}\n{annual_return=}\n{financial_summaries=}\n{profit_statement=}\n----------")
            exit()
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
        print(f"{result_set=}\n{balance_sheet=}\n{assets=}")
        exit()

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
        result_set.remove("Date Annual Return")
        result_set.remove("Annual Meeting Date")
        result_set.remove("Date Filed")
        if len(result_set) > 0:
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
        result_set.remove("Name")
        result_set.remove("Amount")
        result_set.remove("Start Date")
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

    def _extractShareholdersNames(self, names: List[str]) -> str:
        """
        Building the name of the shareholders.

        Parameters:
            names: [string]: The list of the names of the shareholders.

        Returns:
            string
        """
        if len(names) > 0 and "SHARES" not in " ".join(names):
            return " ".join(names)
        else:
            return "NaN"

    def extractShareholdersNames(self, result_set: List[str]) -> List[str]:
        """
        Extracting the names of the shareholders from the dataset.

        Parameters:
            result_set: [string]: The result set to be used as a dataset.

        Returns:
            [string]
        """
        response: List[str] = []
        for index in range(0, len(result_set), 1):
            names: List[str] = findall(r"\b[A-Z]+\b", result_set[index])
            name: str = self._extractShareholdersNames(names)
            response = self.__extractNames(response, name)
        return response

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
        Extracting the type of shares from the result set.

        Parameters:
            result_set: [string]: The result set to be used as a dataset.

        Returns:
            [string]
        """
        response: List[str] = []
        for index in range(0, len(result_set), 1):
            type_shares: List[str] = findall(r"\b[A-Z]+\b", result_set[index])
            type_share: str = self._extractShareholdersTypeShares(type_shares)
            response = self.__extractShareholdersTypeShares(response, type_share)
        return response

    def _extractShareholdersAmountShares(self, amount_shares: List[str]) -> Union[int, str]:
        """
        Building the amount of shares.

        Parameters:
            amount_shares: [string]: The list of the amount of shares.

        Returns:
            string|int
        """
        if len(amount_shares) > 0:
            return int(amount_shares[0])
        else:
            return "NaAS"

    def __extractShareholdersAmountShares(self, amount_shares: List[int], amount_share: Union[int, str]) -> List[int]:
        """
        Building the response of the extraction of the amount of
        shares of the shareholders.

        Parameters:
            amount_shares: [int]: The response to be returned.
            amount_share: int|string: The amount of the shares.

        Returns:
            [int]
        """
        if type(amount_share) is int:
            amount_shares.append(amount_share)
        return amount_shares

    def extractShareholdersAmountShares(self, result_set: List[str]) -> List[int]:
        """
        Extracting the amount of shares from the result set.

        Parameters:
            result_set: [string]: The result set to be used as a dataset.

        Returns:
            [int]
        """
        response: List[int] = []
        for index in range(0, len(result_set), 1):
            amount_shares: List[str] = findall(r"\b\d+\b", result_set[index])
            amount_share: Union[int, str] = self._extractShareholdersAmountShares(amount_shares)
            response = self.__extractShareholdersAmountShares(response, amount_share)
        return response

    def extractShareholders(self, portable_document_file_result_set: List[str]) -> List[Dict[str, Union[str, int]]]:
        """
        Extracting the data for the shareholders from the result
        set.

        Parameters:
            portable_document_file_result_set: [string]: The result set which is based from the portable document file version of the corporate registry.

        Returns:
            [{name: string, amount: int, type: string, currency: string}]
        """
        response: List[Dict[str, Union[str, int]]] = []
        start_index: int = portable_document_file_result_set.index("Shareholders") + 1
        end_index: int = portable_document_file_result_set.index("Members (Applicable for Company Limited by Guarantee or Shares and Guarantee)")
        result_set: List[str] = portable_document_file_result_set[start_index:end_index]
        result_set = [value for value in result_set if value != "\x0cDate Issued:"]
        result_set = [value for value in result_set if value != "Shareholders"]
        result_set = [value for value in result_set if value != "Page 1"]
        result_set = [value for value in result_set if value != " of 7"]
        result_set = [value for value in result_set if value != "Name"]
        result_set = [value for value in result_set if value != "No. of Shares Type of Shares"]
        result_set = [value for value in result_set if value != "Currency"]
        result_set = [value for value in result_set if "/" not in value]
        names: List[str] = self.extractShareholdersNames(result_set)
        result_set = [value for value in result_set if value not in names]
        type_of_shares: List[str] = self.extractShareholdersTypeShares(result_set)
        amount_of_shares: List[int] = self.extractShareholdersAmountShares(result_set)
        currencies: List[str] = [value for value in result_set if type_of_shares[0] not in value]
        for index in range(0, len(names), 1):
            data: Dict[str, Union[str, int]] = {
                "name": names[index].title(),
                "amount_shares": amount_of_shares[index],
                "type_shares": type_of_shares[index].title(),
                "currency": currencies[index].title()
            }
            response.append(data)
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
        if len(dataset) > 1 and "MAURITIUS" not in dataset:
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