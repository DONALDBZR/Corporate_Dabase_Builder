"""
The module which will have the main corporate database
builder.

Authors:
    Andy Ewen Gaspard
"""


from Data.CompanyDetails import CompanyDetails
from Data.FinancialCalendar import FinancialCalendar
from Data.FinCorpLogs import FinCorpLogs
from Data.DocumentFiles import DocumentFiles
from Models.Crawler import Crawler
from Models.DatabaseHandler import Database_Handler
from Models.Logger import Corporate_Database_Builder_Logger
from Models.FinancialCalendar import Financial_Calendar
from Models.FinCorpLogs import FinCorp_Logs
from Models.DocumentFiles import Document_Files
from Models.CompanyDetails import Company_Details
from Models.DocumentReader import Document_Reader
from Models.BusinessDetails import Business_Details
from Models.StateCapital import State_Capital
from Models.OfficeBearers import Office_Bearers
from Models.Shareholders import Shareholders
from datetime import datetime, timedelta
from Environment import Environment
from typing import List, Tuple, Union, Dict
from time import time
from re import findall
import os


class Builder:
    """
    The builder which will build the database.
    """
    __crawler: Crawler
    """
    The main web-scrapper which will scrape the data from the
    database needed.
    """
    __Database_Handler: Database_Handler
    """
    The database handler that will communicate with the database
    server.
    """
    __logger: Corporate_Database_Builder_Logger
    """
    The logger that will all the action of the application.
    """
    __data: List[Dict[str, Union[str, None]]]
    """
    The data that is fed from the Crawler.
    """
    ENV: Environment
    """
    The ENV file of the application which stores the important
    information which allows the application to operate
    smoothly.
    """
    __financial_calendar: Financial_Calendar
    """
    The model which will interact exclusively with the Financial
    Calendar.
    """
    __fincorp_logs: FinCorp_Logs
    """
    The model which will interact exclusively with the FinCorp
    Logs.
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
    __document_reader: Document_Reader
    """
    The model needed to generate the portable document file
    version of the corporate registry, as well as extracting the
    data from it before deleting it from the cache of the server
    of the application.
    """
    __business_details: Business_Details
    """
    The model which will interact exclusively with the Business
    Details.
    """
    __state_capital: State_Capital
    """
    The model which will interact exclusively with the State
    Capital.
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

    def __init__(self) -> None:
        """
        Initializing the builder which will import and initialize
        the dependencies.
        """
        self.ENV = Environment()
        self.setLogger(Corporate_Database_Builder_Logger())
        self.setDatabaseHandler(Database_Handler())
        self.setFinancialCalendar(Financial_Calendar())
        self.setFinCorpLogs(FinCorp_Logs())
        self.setCompanyDetails(Company_Details())
        self.setDocumentFiles(Document_Files())
        self.setDocumentReader(Document_Reader())
        self.setBusinessDetails(Business_Details())
        self.setStateCapital(State_Capital())
        self.setOfficeBearers(Office_Bearers())
        self.setShareholders(Shareholders())
        self.getLogger().inform("The builder has been initialized and all of its dependencies are injected!")

    def getCrawler(self) -> Crawler:
        return self.__crawler

    def setCrawler(self, crawler: Crawler) -> None:
        self.__crawler = crawler

    def getDatabaseHandler(self) -> Database_Handler:
        return self.__Database_Handler

    def setDatabaseHandler(self, database_handler: Database_Handler) -> None:
        self.__Database_Handler = database_handler

    def getLogger(self) -> Corporate_Database_Builder_Logger:
        return self.__logger

    def setLogger(self, logger: Corporate_Database_Builder_Logger) -> None:
        self.__logger = logger

    def getData(self) -> List[Dict[str, Union[str, None]]]:
        return self.__data

    def setData(self, data: List[Dict[str, Union[str, None]]]) -> None:
        self.__data = data

    def getFinancialCalendar(self) -> Financial_Calendar:
        return self.__financial_calendar

    def setFinancialCalendar(self, financial_calendar: Financial_Calendar) -> None:
        self.__financial_calendar = financial_calendar

    def getFinCorpLogs(self) -> FinCorp_Logs:
        return self.__fincorp_logs

    def setFinCorpLogs(self, fincorp_logs: FinCorp_Logs) -> None:
        self.__fincorp_logs = fincorp_logs

    def getCompanyDetails(self) -> Company_Details:
        return self.__company_details

    def setCompanyDetails(self, company_details: Company_Details) -> None:
        self.__company_details = company_details

    def getDocumentFiles(self) -> Document_Files:
        return self.__document_files

    def setDocumentFiles(self, document_files: Document_Files) -> None:
        self.__document_files = document_files

    def getDocumentReader(self) -> Document_Reader:
        return self.__document_reader

    def setDocumentReader(self, document_reader: Document_Reader) -> None:
        self.__document_reader = document_reader

    def getBusinessDetails(self) -> Business_Details:
        return self.__business_details

    def setBusinessDetails(self, business_details: Business_Details) -> None:
        self.__business_details = business_details

    def getStateCapital(self) -> State_Capital:
        return self.__state_capital

    def setStateCapital(self, state_capital: State_Capital) -> None:
        self.__state_capital = state_capital

    def getOfficeBearers(self) -> Office_Bearers:
        return self.__office_bearers

    def setOfficeBearers(self, office_bearers: Office_Bearers) -> None:
        self.__office_bearers = office_bearers

    def getShareholders(self) -> Shareholders:
        return self.__shareholders

    def setShareholders(self, shareholders: Shareholders) -> None:
        self.__shareholders = shareholders

    def getDateDownloadCorporateFile(self, fin_corp_logs: List[FinCorpLogs]) -> str:
        """
        Retrieving the date to be used as a parameter for the date
        of incorporation.

        Parameters:
            fin_corp_logs: [{identifier: int, method_name: string, year: int, quarter: string, date_start: int, date_to: int, status: int, amount: int}]: The list of the logs.

        Returns:
            string
        """
        start_date: str = datetime.strftime(
            datetime.strptime(
                self.getDateStart(fin_corp_logs),
                "%m/%d/%Y"
            ),
            "%Y-%m-%d"
        )
        end_date: str = datetime.strftime(
            datetime.strptime(
                self.getDateEnd(fin_corp_logs),
                "%m/%d/%Y"
            ),
            "%Y-%m-%d"
        )
        start_date_timestamp: int = int(
            datetime.strptime(
                start_date,
                "%Y-%m-%d"
            ).timestamp()
        )
        if start_date_timestamp <= int(time()):
            return start_date
        else:
            return end_date

    def getDateExtractCorporateData(self, fin_corp_logs: List[FinCorpLogs]) -> str:
        """
        Retrieving the date to be used as a parameter for the date
        of incorporation.

        Parameters:
            fin_corp_logs: [{identifier: int, method_name: string, year: int, quarter: string, date_start: int, date_to: int, status: int, amount: int}]: The list of the logs.

        Returns:
            string
        """
        start_date: str = datetime.strftime(
            datetime.strptime(
                self.getDateStart(fin_corp_logs),
                "%m/%d/%Y"
            ),
            "%Y-%m-%d"
        )
        end_date: str = datetime.strftime(
            datetime.strptime(
                self.getDateEnd(fin_corp_logs),
                "%m/%d/%Y"
            ),
            "%Y-%m-%d"
        )
        start_date_timestamp: int = int(
            datetime.strptime(
                start_date,
                "%Y-%m-%d"
            ).timestamp()
        )
        if start_date_timestamp <= int(time()):
            return start_date
        else:
            return end_date

    def _getDateDownloadCorporateFile(self, fin_corp_logs: List[FinCorpLogs], quarter: FinancialCalendar) -> str:
        """
        Retrieving the date to be used as a parameter for the date
        of incorporation.

        Parameters:
            fin_corp_logs: [{identifier: int, method_name: string, year: int, quarter: string, date_start: int, date_to: int, status: int, amount: int}]: The list of the logs.
            quarter: {year: int, quarter: string, start_date: string, end_date: string}: The current quarter

        Returns:
            string
        """
        if len(fin_corp_logs) == 1 and fin_corp_logs[0].status == 204:
            return datetime.strftime(
                datetime.strptime(quarter.start_date, "%m/%d/%Y"),
                "%Y-%m-%d"
            )
        else:
            return self.getDateDownloadCorporateFile(fin_corp_logs)

    def _getDateExtractCorporateData(self, fin_corp_logs: List[FinCorpLogs], quarter: FinancialCalendar) -> str:
        """
        Retrieving the date to be used as a parameter for the date
        of incorporation.

        Parameters:
            fin_corp_logs: [{identifier: int, method_name: string, year: int, quarter: string, date_start: int, date_to: int, status: int, amount: int}]: The list of the logs.
            quarter: {year: int, quarter: string, start_date: string, end_date: string}: The current quarter

        Returns:
            string
        """
        if len(fin_corp_logs) == 1 and fin_corp_logs[0].status == 204:
            return datetime.strftime(
                datetime.strptime(quarter.start_date, "%m/%d/%Y"),
                "%Y-%m-%d"
            )
        else:
            return self.getDateExtractCorporateData(fin_corp_logs)

    def extractCorporateData(self) -> None:
        """
        The third run consists of extracting the data from the
        corporate document files that are stored in the corporate
        database.

        Returns:
            void
        """
        quarter: FinancialCalendar = self.getFinancialCalendar().getCurrentQuarter()  # type: ignore
        successful_logs: List[FinCorpLogs] = self.getFinCorpLogs().getSuccessfulRunsLogs("extractCorporateData")
        date: str = self._getDateExtractCorporateData(successful_logs, quarter)
        document_files: List[DocumentFiles] = self.getDocumentFiles().getCorporateRegistries(date)
        amount: int = self.getDocumentFiles().getAmount(date)
        amount_found: int = self.getDocumentFiles().getAmountFound(date)
        self.getLogger().inform(f"The corporate registries have been retrieved from the relational database server and they will be used for the extracttion of the data about the companies.\nDate of Incorporation: {date}\nCorporate Registries Amount: {amount}\nAmount Downloaded: {amount_found}")
        for index in range(0, len(document_files), 1):
            file_generation_status: int = self.getDocumentReader().generatePortableDocumentFile(document_files[index])
            data_extraction: Dict[str, Union[int, Dict[str, Union[str, int]], Dict[str, str], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]] = self.getDocumentReader().extractData(file_generation_status, document_files[index])
            data_manipulation: int = self.storeCorporateData(data_extraction, document_files[index])
            # exit()
            # Deleting the generated portable document file.

    def storeCorporateData(self, dataset: Dict[str, Union[int, Dict[str, Union[str, int]], Dict[str, str], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]], document_file: DocumentFiles) -> int:
        """
        Storing the corporate data that is extracted from the
        corporate registry.

        Parameters:
            dataset: {status: int, company_details: {business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}, business_details: {registered_address: string, name: string, nature: string, operational: string}, certificates: [{certificate: string, type: str, date_effective: int, date_expiry: int}], office_bearers: [{position: string, name: string, address: string, date_appointment: int}], shareholders: [{name: string, amount: int, type: string, currency: string}], members: [{name: string, amount: int, date_start: int, currency: string}], annual_return: [{date_annual_return: int, date_annual_meeting: int, date_filled: int}], financial_summaries: [{financial_year: int, currency: string, date_approved: int, unit: int}], profit_statement: {financial_summary: {financial_year: int, currency: string, date_approved: int, unit: int}, turnover: float, cost_of_sales: float, gross_profit: float, other_income: float, distribution_cost: float, administration_cost: float, expenses: float, finance_cost: float, net_profit_before_taxation: float, taxation: float, net_profit: float}, state_capital: {type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}, balance_sheet: {balance_sheet: {financial_year: int, currency: string, unit: int}, assets: {non_current_assets: {property_plant_equipment: float, investment_properties: float, intangible_assets: float, other_investments: float, subsidiaries_investments: float, biological_assets: float, others: float, total: float}, current_assets: {inventories: float, trade: float, cash: float, others: float, total: float}, total: float}, liabilities: {equity_and_liabilities: {share_capital: float, other_reserves: float, retained_earnings: float, others: float, total: float}, non_current: {long_term_borrowings: float, deferred_tax: float, long_term_provisions: float, others: float, total: float}, current: {trade: float, short_term_borrowings: float, current_tax_payable: float, short_term_provisions: float, others: float, total: float}, total_liabilities: float, total_equity_and_liabilities: float}}, charges: [{volume: int, property: string, nature: string, amount: int, date_charged: int, date_filled: int, currency: string}], liquidators: {liquidator: {name: string, appointed_date: int, address: string}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}, receivers: {receiver: {name: string, date_appointed: int, address: string}, reports: [{date_filled: int, date_from: int, date_to: int}], affidavits: [{date_filled: int, date_from: int, date_to: int}]}, administrators: {administrator: {name: string, date_appointed: int, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}, details: [{type: string, date_start: int, date_end: int, status: string}], objections: [{date_objection: int, objector: string}]}: The data that has been extracted from the corporate registry.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        print(f"{dataset=}")
        response: int
        data_extraction_status: int = dataset["status"] # type: ignore
        if data_extraction_status == 200:
            company_detail_response: int = self.storeCorporateDataCompanyDetail(data_extraction_status, dataset["company_details"], document_file) # type: ignore
            business_detail_response: int = self.storeCorporateDataBusinessDetail(company_detail_response, dataset["business_details"], document_file) # type: ignore
            certificate_response: int = self.storeCorporateDataCertificate(business_detail_response, dataset["certificates"], document_file) # type: ignore
            office_bearers_response: int = self.storeCorporateDataOfficeBearers(certificate_response, dataset["office_bearers"], document_file) # type: ignore
            shareholder_response: int = self.storeCorporateDataShareholders(office_bearers_response, dataset["shareholders"], document_file) # type: ignore
            member_response: int = self.storeCorporateDataMembers(shareholder_response, dataset["members"], document_file) # type: ignore
            annual_return_response: int = self.storeCorporateDataAnnualReturn(member_response, dataset["annual_return"], document_file) # type: ignore
            financial_summary_response: int = self.storeCorporateDataFinancialSummary(annual_return_response, dataset["financial_summaries"], document_file) # type: ignore
            profit_statement_response: int = self.storeCorporateDataProfitStatement(financial_summary_response, dataset["profit_statement"], document_file) # type: ignore
            state_capital_response: int = self.storeCorporateDataStateCapital(profit_statement_response, dataset["state_capital"], document_file) # type: ignore
            balance_sheet_response: int = self.storeCorporateDataBalanceSheet(state_capital_response, dataset["balance_sheet"], document_file) # type: ignore
            charges_response: int = self.storeCorporateDataCharges(balance_sheet_response, dataset["charges"], document_file) # type: ignore
            liquidators_response: int = self.storeCorporateDataLiquidators(charges_response, dataset["liquidators"], document_file) # type: ignore
            print(f"{liquidators_response=}")
            exit()
        else:
            response = 500
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {data_extraction_status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataLiquidators(self, status: int, liquidators: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on liquidators result set.

        Parameters:
            status: int: The status of the data manipulation.
            liquidators: {liquidator: {name: string, appointed_date: int, address: string}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}: The data that has been extracted for the liquidators table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        if status >= 200 and status <= 299 and not liquidators:
            response = 200
            self.getLogger().inform(f"There is no data to be inserted into the Liquidators table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {liquidators}")
        elif status >= 200 and status <= 299 and len(liquidators) != 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Builder.storeCorporateDataLiquidators()")
            exit()
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataCharges(self, status: int, charges: List[Dict[str, Union[int, str]]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on the charges result set.

        Parameters:
            status: int: The status of the data manipulation.
            charges: [{volume: int, property: string, nature: string, amount: int, date_charged: int, date_filled: int, currency: string}]: The data that has been extracted for the charges table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        if status >= 200 and status <= 299 and len(charges) == 0:
            response = 200
            self.getLogger().inform(f"There is no data to be inserted into the Charges table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {charges}")
        elif status >= 200 and status <= 299 and len(charges) != 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Builder.storeCorporateDataCharges()")
            exit()
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataBalanceSheet(self, status: int, balance_sheet: Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on the balance sheet result set.

        Parameters:
            status: int: The status of the data manipulation.
            balance_sheet: {balance_sheet: {financial_year: int, currency: string, unit: int}, assets: {non_current_assets: {property_plant_equipment: float, investment_properties: float, intangible_assets: float, other_investments: float, subsidiaries_investments: float, biological_assets: float, others: float, total: float}, current_assets: {inventories: float, trade: float, cash: float, others: float, total: float}, total: float}, liabilities: {equity_and_liabilities: {share_capital: float, other_reserves: float, retained_earnings: float, others: float, total: float}, non_current: {long_term_borrowings: float, deferred_tax: float, long_term_provisions: float, others: float, total: float}, current: {trade: float, short_term_borrowings: float, current_tax_payable: float, short_term_provisions: float, others: float, total: float}, total_liabilities: float, total_equity_and_liabilities: float}}: The data that has been extracted for the balance sheet table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        if status >= 200 and status <= 299 and not balance_sheet:
            response = 200
            self.getLogger().inform(f"There is no data to be inserted into the Balance Sheet table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {balance_sheet}")
        elif status >= 200 and status <= 299 and len(balance_sheet) != 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Builder.storeCorporateDataBalanceSheet()")
            exit()
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataProfitStatement(self, status: int, profit_statement: Dict[str, Union[Dict[str, Union[int, str]], float]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on the profit statement result
        set.

        Parameters:
            status: int: The status of the data manipulation.
            profit_statement: {financial_summary: {financial_year: int, currency: string, date_approved: int, unit: int}, turnover: float, cost_of_sales: float, gross_profit: float, other_income: float, distribution_cost: float, administration_cost: float, expenses: float, finance_cost: float, net_profit_before_taxation: float, taxation: float, net_profit: float}: The data that has been extracted for the profit statement table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        if status >= 200 and status <= 299 and not profit_statement:
            response = 200
            self.getLogger().inform(f"There is no data to be inserted into the Profit Statement table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {profit_statement}")
        elif status >= 200 and status <= 299 and len(profit_statement) != 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Builder.storeCorporateDataProfitStatement()")
            exit()
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataFinancialSummary(self, status: int, financial_summaries: List[Dict[str, Union[int, str]]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on the financial summary result
        set.

        Parameters:
            status: int: The status of the data manipulation.
            financial_summaries: [{financial_year: int, currency: string, date_approved: int, unit: int}]: The data that has been extracted for the financial summary table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        if status >= 200 and status <= 299 and len(financial_summaries) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Builder.storeCorporateDataFinancialSummary()")
            exit()
        elif status >= 200 and status <= 299 and len(financial_summaries) == 0:
            response = 200
            self.getLogger().inform(f"There is no data to be inserted into the Financial Summaries table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {financial_summaries}")
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataAnnualReturn(self, status: int, annual_return: List[Dict[str, int]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on the annual return result set.

        Parameters:
            status: int: The status of the data manipulation.
            annual_return: [{date_annual_return: int, date_annual_meeting: int, date_filled: int}]: The data that has been extracted for the annual return table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        if status >= 200 and status <= 299 and len(annual_return) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Builder.storeCorporateDataAnnualReturn()")
            exit()
        elif status >= 200 and status <= 299 and len(annual_return) == 0:
            response = 200
            self.getLogger().inform(f"There is no data to be inserted into the Annual Return table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {annual_return}")
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataMembers(self, status: int, members: List[Dict[str, Union[str, int]]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on the members result set.

        Parameters:
            status: int: The status of the data manipulation.
            certificates: [{name: string, amount: int, date_start: int, currency: string}]: The data that has been extracted for the members table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        if status == 201 and len(members) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Builder.storeCorporateDataMembers()")
            exit()
        elif status == 201 and len(members) == 0:
            response = 200
            self.getLogger().inform(f"There is no data to be inserted into the Members table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {members}")
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataCertificate(self, status: int, certificates: List[Dict[str, Union[str, int]]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on the certificates result set.

        Parameters:
            status: int: The status of the data manipulation.
            certificates: [{certificate: string, type: str, date_effective: int, date_expiry: int}]: The data that has been extracted for the shareholders table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        if status == 201 and len(certificates) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Builder.storeCorporateDataCertificate()")
            exit()
        elif status == 201 and len(certificates) == 0:
            response = 200
            self.getLogger().inform(f"There is no data to be inserted into the Certificate table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {certificates}")
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataShareholders(self, status: int, shareholders: List[Dict[str, Union[str, int]]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on the Shareholders result set.

        Parameters:
            status: int: The status of the data manipulation.
            shareholders: [{name: string, amount_shares: int, type_shares: string, currency: string}]: The data that has been extracted for the shareholders table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        if status == 201:
            response = self._storeCorporateDataShareholders(shareholders, document_file.company_detail)
            self.getLogger().inform(f"The data has been successfully updated into the State Capital table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {shareholders}")
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def _storeCorporateDataShareholders(self, shareholders: List[Dict[str, Union[str, int]]], company_detail: int) -> int:
        """
        Storing the shareholders.

        Parameters:
            shareholders: [{name: string, amount_shares: int, type_shares: string, currency: string}]: The data that has been extracted for the shareholders table.
            company_detail: int: The identifier of the company.

        Returns:
            int
        """
        response: int
        responses: List[int] = []
        for index in range(0, len(shareholders), 1):
            relational_database_response: int = self.getShareholders().addShareholders(shareholders[index], company_detail)
            responses.append(relational_database_response)
        responses = list(set(responses))
        if len(responses) == 1 and responses[0] == 201:
            response = 201
        else:
            response = 503
        return response

    def storeCorporateDataOfficeBearers(self, status: int, office_bearers: List[Dict[str, Union[str, int]]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on the Office Bearers result
        set.

        Parameters:
            status: int: The status of the data manipulation.
            office_bearers: [{position: string, name: string, address: string, date_appointment: int}]: The data that has been extracted for the office bearers table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        if status >= 200 and status <= 299:
            response = self._storeCorporateDataOfficeBearers(office_bearers, document_file)
            self.getLogger().inform(f"The data has been successfully updated into the Office Bearers table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {office_bearers}")
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def _storeCorporateDataOfficeBearers(self, office_bearers: List[Dict[str, Union[str, int]]], document_file: DocumentFiles) -> int:
        """
        Storing the office bearers in its respective table.

        Parameters:
            office_bearers: [{position: string, name: string, address: string, date_appointment: int}]: The data that has been extracted for the office bearers table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        responses: List[int] = []
        for index in range(0, len(office_bearers), 1):
            relational_database_response: int = self.getOfficeBearers().addDirectors(office_bearers[index], document_file.company_detail)
            responses.append(relational_database_response)
        responses = list(set(responses))
        if len(responses) == 1 and responses[0] == 201:
            response = 201
        else:
            response = 503
        return response

    def storeCorporateDataStateCapital(self, status: int, state_capital: Dict[str, Union[str, int]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation State Capital result set.

        Parameters:
            status: int: The status of the data manipulation.
            state_capital: {type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}: The data that has been extracted for the shareholder table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        if status >= 200 and status <= 299 and not state_capital:
            response = 200
            self.getLogger().inform(f"There is no data to be inserted into the State Capital table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {state_capital}")
        elif status >= 200 and status <= 299 and len(state_capital) > 0:
            response = self.getStateCapital().addStateCapital(state_capital, document_file.company_detail)
            self.getLogger().inform(f"The data has been successfully updated into the State Capital table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {state_capital}")
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataBusinessDetail(self, company_detail: int, business_details: Dict[str, str], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on the Business Details result
        set.

        Parameters:
            company_detail: int: The status of the data manipulation.
            business_details: {registered_address: string, name: string, nature: string, operational_address: string}: The data that has been extracted for the business details table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        if company_detail == 202:
            response = self.getBusinessDetails().addBusinessDetails(business_details, document_file.company_detail)
            self.getLogger().inform(f"The data has been successfully updated into the Business Details table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {business_details}")
        else:
            response = company_detail
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {company_detail}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataCompanyDetail(self, data_extraction: int, company_details: Dict[str, Union[str, int]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on the Company Details result
        set.

        Parameters:
            data_extraction: int: The status of the data extraction.
            company_details: {business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}: The data that has been extracted for the company details table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        date_verified: int = int(time())
        is_extracted: int = 1
        company_identifier: int = int("".join(findall(r"\d+", str(company_details["file_number"]))))
        company_type: str = "".join(findall(r"[A-Z]+", str(company_details["file_number"])))
        if data_extraction == 200:
            company_details["date_verified"] = date_verified
            company_details["is_extracted"] = is_extracted
            company_details["company_identifier"] = company_identifier
            company_details["company_type"] = company_type
            response = self.getCompanyDetails().updateCorporateMetadata(company_details, document_file.company_detail)
            self.getLogger().inform(f"The data has been successfully updated into the Company Details table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {company_details}")
        else:
            response = data_extraction
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {data_extraction}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def downloadCorporateFile(self) -> None:
        """
        The second run consists of retrieving the corporate document
        file of the corporate metadata that is in the corporate
        database.

        Returns:
            void
        """
        quarter: FinancialCalendar = self.getFinancialCalendar().getCurrentQuarter()  # type: ignore
        successful_logs: List[FinCorpLogs] = self.getFinCorpLogs().getSuccessfulRunsLogs("downloadCorporateFile")
        date: str = self._getDateDownloadCorporateFile(successful_logs, quarter)
        company_details: List[CompanyDetails] = self.getCompanyDetails().getCompanyDetailsForDownloadCorporateDocumentFile(date)
        amount: int = self.getCompanyDetails().getAmount(date)
        amount_found: int = self.getCompanyDetails().getAmountDownloadedCorporateDocuments(date)
        self.getLogger().inform(f"The data that will be used as payloads for retrieving the corporate document files from the Mauritius Network Services Online Search platform.\nDate of Incorporation: {date}\nCompany Details Amount: {len(company_details)}\nAmount Downloaded: {amount_found}")
        for index in range(0, len(company_details), 1):
            self.setCrawler(Crawler())
            crawler_response: Dict[str, Union[int, Dict[str, Union[str, None, int]], bytes, None]] = self.getCrawler().retrieveCorporateDocumentFile(company_details[index], 0)
            self.getCrawler().getDriver().quit()
            self.getLogger().inform(f"The portable document file has been downloaded as well as the company details has been verified!\nIdentifier: {company_details[index].identifier}\nName: {company_details[index].name}")
            self.getCompanyDetails().updateCompany(crawler_response["CompanyDetails"]) # type: ignore
            amount_found = self.getDocumentFiles().addDocumentFile(crawler_response, amount_found)
        logs: Tuple[str, str, int, int, int, int, int] = (
            "downloadCorporateFile",
            quarter.quarter,
            int(datetime.strptime(date, "%Y-%m-%d").timestamp()),
            int(datetime.strptime(date, "%Y-%m-%d").timestamp()),
            200,
            amount,
            amount_found
        )
        self.getFinCorpLogs().postSuccessfulCorporateDataCollectionRun(logs) # type: ignore

    def collectCorporateMetadata(self) -> None:
        """
        The first run consists of retrieving the metadata needed of
        any existing company in Mauritius.

        Returns:
            void
        """
        request: Dict[str, str] = {}
        quarter: FinancialCalendar = self.getFinancialCalendar().getCurrentQuarter()  # type: ignore
        successful_logs: List[FinCorpLogs] = self.getFinCorpLogs().getSuccessfulRunsLogs("collectCorporateMetadata")
        if len(successful_logs) == 1 and successful_logs[0].status == 204:
            date_to = datetime.strftime(
                datetime.strptime(quarter.start_date, "%m/%d/%Y") + timedelta(weeks=1),
                "%m/%d/%Y"
            )
            request = {
                "start_date": quarter.start_date,
                "end_date": date_to
            }
        else:
            request = self.handleRequestCollectCorporateMetadata(successful_logs)
        self.setCrawler(Crawler())
        response: Dict[str, int] = self.getCrawler().retrieveCorporateMetadata(str(request["start_date"]), str(request["end_date"]), 0)
        self.validateCorporateMetadata(response, request, quarter)  # type: ignore
        self.cleanCache()

    def cleanCache(self) -> None:
        """
        Cleaning the cache database after having retrieved the
        corporate metadata and storing them into the relational
        database server.

        Returns:
            void
        """
        files = os.listdir(
            f"{self.ENV.getDirectory()}/Cache/CorporateDataCollection"
        )
        if len(files) > 0:
            self._cleanCache(files)

    def _cleanCache(self, files: List[str]) -> None:
        """
        Cleaning the Cache database based on the amount of files in
        it.

        Returns:
            void
        """
        for index in range(0, len(files), 1):
            os.remove(
                f"{self.ENV.getDirectory()}/Cache/CorporateDataCollection/{files[index]}"
            )

    def _getDateEndFinCorpLogs(self, log: FinCorpLogs, date_end: int) -> int:
        """
        Retrieving the date end from the log data and comparing to
        retrieve the latest one.

        Parameters:
            log: FinCorpLogs
            date_end: int

        Returns:
            int
        """
        if log.date_to > date_end:
            return log.date_to
        else:
            return date_end

    def getDateStart(self, logs: List[FinCorpLogs]) -> str:
        """
        Retrieving the next start date for the data collection which
        will be based on the latest end date that is in the logs.

        Parameters:
            logs: array

        Returns:
            string
        """
        date_end: int = 0
        for index in range(0, len(logs), 1):
            date_end = self._getDateEndFinCorpLogs(logs[index], date_end)
        return datetime.strftime(
            datetime.strptime(
                datetime.fromtimestamp(date_end).strftime("%m/%d/%Y"),
                "%m/%d/%Y"
            ) + timedelta(
                days=1
            ),
            "%m/%d/%Y"
        )

    def _getDateStartFinCorpLogs(self, log: FinCorpLogs, date_start: int) -> int:
        """
        Retrieving the date start from the log data and comparing to
        retrieve the earliest one.

        Parameters:
            log: FinCorpLogs
            date_start: int

        Returns:
            int
        """
        if log.date_start < date_start:
            return log.date_start
        else:
            return date_start

    def getDateEnd(self, logs: List[FinCorpLogs]) -> str:
        """
        Retrieving the next end date for the data collection which
        will be based on the earliest start date that is in the
        logs.

        Parameters:
            logs: array

        Returns:
            string
        """
        date_start: int = int(time())
        for index in range(0, len(logs), 1):
            date_start = self._getDateStartFinCorpLogs(logs[index], date_start)
        return datetime.strftime(
            datetime.strptime(
                datetime.fromtimestamp(date_start).strftime("%m/%d/%Y"),
                "%m/%d/%Y"
            ) - timedelta(
                days=1
            ),
            "%m/%d/%Y"
        )

    def handleRequestCollectCorporateMetadata(self, logs: List[FinCorpLogs]) -> Dict[str, str]:
        """
        Handling the request for the collection of corporate
        metadata before that it is sent to the Crawler.

        Parameters:
            logs: [{identifier: int, method_name: string, year: int, quarter: string, date_start: int, date_to: int, status: int, amount: int}]: The log's data from the relational database server.

        Returns:
            {start_date: string, end_date: string}
        """
        date_start: str
        date_end: str
        date_start = self.getDateStart(logs)
        date_end = datetime.strftime(
            datetime.strptime(date_start, "%m/%d/%Y") + timedelta(weeks=1),
            "%m/%d/%Y"
        )
        date_end_unixtime: float = datetime.strptime(date_end, "%m/%d/%Y").timestamp()
        current_date: datetime = datetime.now() - timedelta(days=1)
        current_time: float = current_date.timestamp()
        if date_end_unixtime > current_time:
            date_end = self.getDateEnd(logs)
            date_start = datetime.strftime(
                datetime.strptime(date_end, "%m/%d/%Y") - timedelta(weeks=1),
                "%m/%d/%Y"
            )
        return {
            "start_date": date_start,
            "end_date": date_end
        }

    def validateCorporateMetadata(self, response: Dict[str, int], request: Dict[str, str], quarter: FinancialCalendar) -> None:
        """
        Validating the response from the Crawler to save the data
        into the database server.

        Parameters:
            response: object
            request: object
            quarter: FinancialCalendar

        Returns:
            void
        """
        method_name: str = "collectCorporateMetadata"
        date_start = int(datetime.strptime(
            str(request["start_date"]),
            "%m/%d/%Y"
        ).timestamp())
        date_end = int(datetime.strptime(
            str(request["end_date"]),
            "%m/%d/%Y"
        ).timestamp())
        if response["status"] == 200:
            parameters: Tuple[str, str, int, int, int, int, int] = (
                method_name,
                quarter.quarter,
                date_start,
                date_end,
                int(response["status"]),
                int(response["amount"]),
                len(self.getCrawler().getCorporateMetadata())
            )
            self.setData(self.getCrawler().getCorporateMetadata())
            self.getCrawler().getDriver().quit()
            self.getLogger().inform("Storing the corporate metadata!")
            self.storeCorporateMetadata()
            self.getFinCorpLogs().postSuccessfulCorporateDataCollectionRun(
                parameters)  # type: ignore
        else:
            parameters: Tuple[str, str, int, int, int, int, int] = (
                method_name,
                quarter.quarter,
                date_start,
                date_end,
                int(response["status"]),
                0,
                0
            )
            self.getCrawler().getDriver().quit()
            self.getFinCorpLogs().postFailedCorporateDataCollectionRun(parameters)  # type: ignore
            self.getLogger().error(
                f"The application has failed to collect the data!  Please check the logs!\nStatus: {response['status']}"
            )
            raise Exception(
                f"The application has failed to collect the data!  Please check the logs!\nStatus: {response['status']}"
            )

    def storeCorporateMetadata(self) -> None:
        """
        Storing the metadata into the database server.

        Returns:
            void
        """
        for index in range(0, len(self.getData()), 1):
            CompanyDetails = self.getData()[index]
            parameters: Tuple[str, str, str, int, str, str] = (
                str(CompanyDetails["name"]),
                str(CompanyDetails["file_number"]),
                str(CompanyDetails["category"]),
                int(datetime.strptime(
                    str(CompanyDetails["date_incorporation"]),
                    "%d/%m/%Y"
                ).timestamp()),
                str(CompanyDetails["nature"]),
                str(CompanyDetails["status"])
            )
            self.getCompanyDetails().addCompany(parameters)  # type: ignore
