"""
The module which will have the main corporate database
builder.
"""


from Data.FinancialSummaries import FinancialSummaries
from Data.StateCapital import StateCapital
from Data.BusinessDetails import BusinessDetails
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
from Models.Members import Member as Member_Model
from datetime import datetime, timedelta
from Environment import Environment
from typing import List, Tuple, Union, Dict
from time import time, sleep
from re import L, findall, search
from Models.Mail import Mail
from Models.FinancialSummaries import Financial_Summaries
from Models.ProfitStatements import Profit_Statements
from Models.BalanceSheets import Balance_Sheets
from Data.BalanceSheets import BalanceSheets
from Models.Assets import Assets as Assets_Model
from Data.Assets import Assets
from Models.NonCurrentAssets import Non_Current_Assets
from Models.CurrentAssets import Current_Assets
from Models.Liabilities import Liabilities as Liabilities_Model
from Data.Liabilities import Liabilities
from Models.EquityAndLiabilities import Equity_And_Liabilities
from Models.NonCurrentLiabilities import Non_Current_Liabilities
from Models.CurrentLiabilities import Current_Liabilities
from Models.AnnualReturns import Annual_Returns
from Models.Objections import Objections
from Models.Details import Details
from Models.Charges import Charges
from Data.OfficeBearers import OfficeBearer
from Data.Shareholders import Shareholder
from Data.Members import Member
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
    __members: Member_Model
    """
    The model which will interact exclusively with the Members.
    """
    __mailer: Mail
    """
    The model which will communicate to the mail servers for the
    application for the sending of mail notifications.
    """
    __business_details_data: List[BusinessDetails]
    """
    The data of the Business Details.
    """
    __company_details_data: List[CompanyDetails]
    """
    The data of the Company Details.
    """
    __state_capital_data: List[StateCapital]
    """
    The Data Transfer Object for the State Capital.
    """
    __financial_summaries: Financial_Summaries
    """
    The model which will interact exclusively with the Financial
    Summaries table.
    """
    __profit_statements: Profit_Statements
    """
    The model which will interact exclusively with the Profit
    Statements table.
    """
    __balance_sheets: Balance_Sheets
    """
    The model which will interact exclusively with the Balance
    Sheets table.
    """
    __assets: Assets_Model
    """
    The model which will interact exclusively with the Assets
    table.
    """
    __non_current_assets: Non_Current_Assets
    """
    The model which will interact exclusively with the Non
    Current Assets table.
    """
    __current_assets: Current_Assets
    """
    The model which will interact exclusively with the Current
    Assets table.
    """
    __liabilities: Liabilities_Model
    """
    The model which will interact exclusively with the
    Liabilities table.
    """
    __equity_and_liabilities: Equity_And_Liabilities
    """
    The model which will interact exclusively with the Equity
    And Liabilities table.
    """
    __non_current_liabilities: Non_Current_Liabilities
    """
    The model which will interact exclusively with the Non
    Current Liabilities table.
    """
    __current_liabilities: Current_Liabilities
    """
    The model which will interact exclusively with the Current
    Liabilities table.
    """
    __annual_returns: Annual_Returns
    """
    The model which will interact exclusively with the Annual
    Returns table.
    """
    __objections: Objections
    """
    The model which will interact exclusively with the
    Objections table.
    """
    __details: Details
    """
    The model which will interact exclusively with the Details
    table.
    """
    __charges: Charges
    """
    The model which will interact exclusively with the Charges
    table.
    """
    __office_bearer_data: List[OfficeBearer]
    """
    The Data Transfer Object for the Office Bearer.
    """
    __shareholder_data: List[Shareholder]
    """
    The Data Transfer Object for the Shareholder.
    """
    __member_data: List[Member]
    """
    The data of the Members table.
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
        self.setMembers(Member_Model())
        self.setFinancialSummaries(Financial_Summaries())
        self.setProfitStatements(Profit_Statements())
        self.setBalanceSheets(Balance_Sheets())
        self.setAssets(Assets_Model())
        self.setNonCurrentAssets(Non_Current_Assets())
        self.setCurrentAssets(Current_Assets())
        self.setLiabilities(Liabilities_Model())
        self.setEquityAndLiabilities(Equity_And_Liabilities())
        self.setNonCurrentLiabilities(Non_Current_Liabilities())
        self.setCurrentLiabilities(Current_Liabilities())
        self.setAnnualReturns(Annual_Returns())
        self.setObjections(Objections())
        self.setDetails(Details())
        self.setCharges(Charges())
        self.getLogger().inform("The builder has been initialized and all of its dependencies are injected!")

    def getMemberData(self) -> List[Member]:
        return self.__member_data

    def setMemberData(self, member_data: List[Member]) -> None:
        self.__member_data = member_data

    def getShareholderData(self) -> List[Shareholder]:
        return self.__shareholder_data

    def setShareholderData(self, shareholder_data: List[Shareholder]) -> None:
        self.__shareholder_data = shareholder_data

    def getOfficeBearerData(self) -> List[OfficeBearer]:
        return self.__office_bearer_data

    def setOfficeBearerData(self, office_bearer_data: List[OfficeBearer]) -> None:
        self.__office_bearer_data = office_bearer_data

    def getCharges(self) -> Charges:
        return self.__charges

    def setCharges(self, charges: Charges) -> None:
        self.__charges = charges

    def getDetails(self) -> Details:
        return self.__details

    def setDetails(self, details: Details) -> None:
        self.__details = details

    def getObjections(self) -> Objections:
        return self.__objections

    def setObjections(self, objections: Objections) -> None:
        self.__objections = objections

    def getAnnualReturns(self) -> Annual_Returns:
        return self.__annual_returns

    def setAnnualReturns(self, annual_returns: Annual_Returns) -> None:
        self.__annual_returns = annual_returns

    def getCurrentLiabilities(self) -> Current_Liabilities:
        return self.__current_liabilities

    def setCurrentLiabilities(self, current_liabilities: Current_Liabilities) -> None:
        self.__current_liabilities = current_liabilities

    def getNonCurrentLiabilities(self) -> Non_Current_Liabilities:
        return self.__non_current_liabilities

    def setNonCurrentLiabilities(self, non_current_liabilities: Non_Current_Liabilities) -> None:
        self.__non_current_liabilities = non_current_liabilities

    def getEquityAndLiabilities(self) -> Equity_And_Liabilities:
        return self.__equity_and_liabilities

    def setEquityAndLiabilities(self, equity_and_liabilities: Equity_And_Liabilities) -> None:
        self.__equity_and_liabilities = equity_and_liabilities

    def getLiabilities(self) -> Liabilities_Model:
        return self.__liabilities

    def setLiabilities(self, liabilities: Liabilities_Model) -> None:
        self.__liabilities = liabilities

    def getCurrentAssets(self) -> Current_Assets:
        return self.__current_assets

    def setCurrentAssets(self, current_assets: Current_Assets) -> None:
        self.__current_assets = current_assets

    def getNonCurrentAssets(self) -> Non_Current_Assets:
        return self.__non_current_assets

    def setNonCurrentAssets(self, non_current_assets: Non_Current_Assets) -> None:
        self.__non_current_assets = non_current_assets

    def getAssets(self) -> Assets_Model:
        return self.__assets

    def setAssets(self, assets: Assets_Model) -> None:
        self.__assets = assets

    def getBalanceSheets(self) -> Balance_Sheets:
        return self.__balance_sheets

    def setBalanceSheets(self, balance_sheets: Balance_Sheets) -> None:
        self.__balance_sheets = balance_sheets

    def getProfitStatements(self) -> Profit_Statements:
        return self.__profit_statements

    def setProfitStatements(self, profit_statements: Profit_Statements) -> None:
        self.__profit_statements = profit_statements

    def getFinancialSummaries(self) -> Financial_Summaries:
        return self.__financial_summaries

    def setFinancialSummaries(self, financial_summaries: Financial_Summaries) -> None:
        self.__financial_summaries = financial_summaries

    def getStateCapitalData(self) -> List[StateCapital]:
        return self.__state_capital_data

    def setStateCapitalData(self, state_capital_data: List[StateCapital]) -> None:
        self.__state_capital_data = state_capital_data

    def getCompanyDetailsData(self) -> List[CompanyDetails]:
        return self.__company_details_data

    def setCompanyDetailsData(self, company_details_data: List[CompanyDetails]) -> None:
        self.__company_details_data = company_details_data

    def getBusinessDetailsData(self) -> List[BusinessDetails]:
        return self.__business_details_data

    def setBusinessDetailsData(self, business_details_data: List[BusinessDetails]) -> None:
        self.__business_details_data = business_details_data

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

    def getMembers(self) -> Member_Model:
        return self.__members

    def setMembers(self, members: Member_Model) -> None:
        self.__members = members

    def getMailer(self) -> Mail:
        return self.__mailer

    def setMailer(self, mailer: Mail) -> None:
        self.__mailer = mailer

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
        start_date: str = datetime.strftime(datetime.strptime(self.getDateStart(fin_corp_logs), "%m/%d/%Y"), "%Y-%m-%d")
        end_date: str = datetime.strftime(datetime.strptime(self.getDateEnd(fin_corp_logs), "%m/%d/%Y"), "%Y-%m-%d")
        start_date_timestamp: int = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
        return start_date if start_date_timestamp <= int(time()) else end_date

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
        return datetime.strftime(datetime.strptime(quarter.start_date, "%m/%d/%Y"), "%Y-%m-%d") if len(fin_corp_logs) == 1 and fin_corp_logs[0].status == 204 else self.getDateExtractCorporateData(fin_corp_logs)

    def extractCorporateData(self, status: int = 200) -> None:
        """
        The third run consists of extracting the data from the
        corporate document files that are stored in the corporate
        database.

        Parameters:
            status: int: The response status of the function.

        Returns:
            void
        """
        quarter: FinancialCalendar = self.getFinancialCalendar().getCurrentQuarter()  # type: ignore
        successful_logs: List[FinCorpLogs] = self.getFinCorpLogs().getSuccessfulRunsLogs("extractCorporateData")
        date: str = self._getDateExtractCorporateData(successful_logs, quarter)
        document_files: List[DocumentFiles] = self.getDocumentFiles().getCorporateRegistries(date)
        amount: int = self.getDocumentFiles().getAmount(date)
        amount_found: int = self.getDocumentFiles().getAmountFound(date)
        status = status if amount > 0 else 204
        response: int = status
        self.getLogger().inform(f"The corporate registries have been retrieved from the relational database server and they will be used for the extracttion of the data about the companies.\nDate of Incorporation: {date}\nCorporate Registries Amount: {amount}\nAmount Downloaded: {amount_found}")
        if status == 200:
            response = self._extractCorporateData(document_files)
            amount_extracted = self.getCompanyDetails().getAmountExtracted(date)
            final_amount = amount_extracted
        else:
            final_amount = amount_found
            response = status if amount_found > 0 else 200
        logs: Tuple[str, str, int, int, int, int, int] = ("extractCorporateData", quarter.quarter, int(datetime.strptime(date, "%Y-%m-%d").timestamp()), int(datetime.strptime(date, "%Y-%m-%d").timestamp()), response, amount, final_amount)
        self.getFinCorpLogs().postSuccessfulCorporateDataCollectionRun(logs) # type: ignore
        if response >= 500 and response <= 599:
            exit()

    def cleanExtractionCacheDirectory(self) -> None:
        """
        Cleaning all of the data that are in the extraction cache
        directory.

        Returns:
            void
        """
        portable_document_files_directory: str = f"{self.ENV.getDirectory()}Cache/CorporateDocumentFile/Documents/"
        data_directory: str = f"{self.ENV.getDirectory()}Cache/CorporateDocumentFile/Metadata/"
        portable_document_files: List[str] = os.listdir(portable_document_files_directory)
        data: List[str] = os.listdir(data_directory)
        for index in range(0, len(portable_document_files), 1):
            os.remove(f"{portable_document_files_directory}{portable_document_files[index]}")
        for index in range(0, len(data), 1):
            os.remove(f"{data_directory}{data[index]}")

    def _extractCorporateData(self, document_files: List[DocumentFiles]) -> int:
        """
        Extracting the corporate data as well as storing it in the
        relational database server.

        Parameters:
            document_files: [{identifier: int, file_data: bytes, company_detail: int}]: The list of corporate registries.

        Returns:
            int
        """
        data_manipulations: List[int] = []
        ok: int = 200
        service_unavailable: int = 503
        for index in range(0, len(document_files), 1):
            company_detail: CompanyDetails = self.getCompanyDetails().getSpecificCompanyDetails(document_files[index].company_detail)
            file_generation_status: int = self.getDocumentReader().generatePortableDocumentFile(document_files[index])
            data_extraction: Union[Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]], Dict[str, Union[int, Dict[str, Union[str, int]], Dict[str, str], List[Dict[str, Union[str, int]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]], Dict[str, Union[Dict[str, str], List[Dict[str, int]]]]]], None] = self.getDocumentReader().extractData(file_generation_status, document_files[index], company_detail)
            data_manipulations.append(self.storeCorporateData(data_extraction, document_files[index], company_detail))
        data_manipulations = list(set(data_manipulations))
        if len(data_manipulations) == 1 and data_manipulations[0] == 201:
            self.getLogger().inform(f"The corporate data has been extracted successfully and stored into the relational database server.\nStatus: {ok}")
            return ok
        self.getLogger().error(f"The corporate data has been extracted successfully and stored into the relational database server.\nStatus: {service_unavailable}")
        return service_unavailable

    def _storeCorporateData(self, dataset: Union[Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]], Dict[str, Union[int, Dict[str, Union[str, int]], Dict[str, str], List[Dict[str, Union[str, int]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]], Dict[str, Union[Dict[str, str], List[Dict[str, int]]]]]], None], document_file: DocumentFiles, company_detail: CompanyDetails) -> int:
        """
        Storing the corporate data that is extracted from the
        corporate registry.

        Parameters:
            dataset: {status: int, company_details: {business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}, business_details: {registered_address: string, name: string, nature: string, operational: string}, certificates: [{certificate: string, type: str, date_effective: int, date_expiry: int}], office_bearers: [{position: string, name: string, address: string, date_appointment: int}], shareholders: [{name: string, amount: int, type: string, currency: string}], members: [{name: string, amount: int, date_start: int, currency: string}], annual_return: [{date_annual_return: int, date_annual_meeting: int, date_filled: int}], financial_summaries: [{financial_year: int, currency: string, date_approved: int, unit: int}], profit_statement: {financial_summary: {financial_year: int, currency: string, date_approved: int, unit: int}, turnover: float, cost_of_sales: float, gross_profit: float, other_income: float, distribution_cost: float, administration_cost: float, expenses: float, finance_cost: float, net_profit_before_taxation: float, taxation: float, net_profit: float}, state_capital: {type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}, balance_sheet: {balance_sheet: {financial_year: int, currency: string, unit: int}, assets: {non_current_assets: {property_plant_equipment: float, investment_properties: float, intangible_assets: float, other_investments: float, subsidiaries_investments: float, biological_assets: float, others: float, total: float}, current_assets: {inventories: float, trade: float, cash: float, others: float, total: float}, total: float}, liabilities: {equity_and_liabilities: {share_capital: float, other_reserves: float, retained_earnings: float, others: float, total: float}, non_current: {long_term_borrowings: float, deferred_tax: float, long_term_provisions: float, others: float, total: float}, current: {trade: float, short_term_borrowings: float, current_tax_payable: float, short_term_provisions: float, others: float, total: float}, total_liabilities: float, total_equity_and_liabilities: float}}, charges: [{volume: int, property: string, nature: string, amount: int, date_charged: int, date_filled: int, currency: string}], liquidators: {liquidator: {name: string, appointed_date: int, address: string}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}, receivers: {receiver: {name: string, date_appointed: int, address: string}, reports: [{date_filled: int, date_from: int, date_to: int}], affidavits: [{date_filled: int, date_from: int, date_to: int}]}, administrators: {administrator: {name: string, date_appointed: int, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}, details: [{type: string, date_start: int, date_end: int, status: string}], objections: [{date_objection: int, objector: string}]}: The data that has been extracted from the corporate registry.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.
            company_detail: {identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int, is_extracted: int, company_identifier: int, company_type: string}: The data of the Company Details.

        Returns:
            int
        """
        no_content: int = 204
        service_unavailable: int = 503
        if dataset == None:
            return no_content
        if company_detail.category.upper() == "DOMESTIC":
            return self.storeCorporateDataDomestic(dataset, document_file, company_detail) # type: ignore
        if company_detail.category.upper() == "AUTHORISED COMPANY":
            return self.storeCorporateDataAuthorisedCompany(dataset, document_file) # type: ignore
        if company_detail.category.upper() == "GLOBAL BUSINESS COMPANY":
            return self.storeCorporateDataGlobalBusinessCompany(dataset, document_file) # type: ignore
        if company_detail.category.upper() == "FOREIGN(DOM BRANCH)":
            return self.storeCorporateDataForeignDomestic(dataset, document_file) # type: ignore
        self.getLogger().error(f"The application will abort the extraction as the function has not been implemented!\nStatus: {service_unavailable}\nFunction: Builder.storeCorporateData()\nCategory: {company_detail.category}")
        return service_unavailable

    def storeCorporateData(self, dataset: Union[Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]], Dict[str, Union[int, Dict[str, Union[str, int]], Dict[str, str], List[Dict[str, Union[str, int]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]], Dict[str, Union[Dict[str, str], List[Dict[str, int]]]]]], None], document_file: DocumentFiles, company_detail: CompanyDetails) -> int:
        """
        Storing the corporate data that is extracted from the
        corporate registry.

        Parameters:
            dataset: {status: int, company_details: {business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}, business_details: {registered_address: string, name: string, nature: string, operational: string}, certificates: [{certificate: string, type: str, date_effective: int, date_expiry: int}], office_bearers: [{position: string, name: string, address: string, date_appointment: int}], shareholders: [{name: string, amount: int, type: string, currency: string}], members: [{name: string, amount: int, date_start: int, currency: string}], annual_return: [{date_annual_return: int, date_annual_meeting: int, date_filled: int}], financial_summaries: [{financial_year: int, currency: string, date_approved: int, unit: int}], profit_statement: {financial_summary: {financial_year: int, currency: string, date_approved: int, unit: int}, turnover: float, cost_of_sales: float, gross_profit: float, other_income: float, distribution_cost: float, administration_cost: float, expenses: float, finance_cost: float, net_profit_before_taxation: float, taxation: float, net_profit: float}, state_capital: {type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}, balance_sheet: {balance_sheet: {financial_year: int, currency: string, unit: int}, assets: {non_current_assets: {property_plant_equipment: float, investment_properties: float, intangible_assets: float, other_investments: float, subsidiaries_investments: float, biological_assets: float, others: float, total: float}, current_assets: {inventories: float, trade: float, cash: float, others: float, total: float}, total: float}, liabilities: {equity_and_liabilities: {share_capital: float, other_reserves: float, retained_earnings: float, others: float, total: float}, non_current: {long_term_borrowings: float, deferred_tax: float, long_term_provisions: float, others: float, total: float}, current: {trade: float, short_term_borrowings: float, current_tax_payable: float, short_term_provisions: float, others: float, total: float}, total_liabilities: float, total_equity_and_liabilities: float}}, charges: [{volume: int, property: string, nature: string, amount: int, date_charged: int, date_filled: int, currency: string}], liquidators: {liquidator: {name: string, appointed_date: int, address: string}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}, receivers: {receiver: {name: string, date_appointed: int, address: string}, reports: [{date_filled: int, date_from: int, date_to: int}], affidavits: [{date_filled: int, date_from: int, date_to: int}]}, administrators: {administrator: {name: string, date_appointed: int, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}, details: [{type: string, date_start: int, date_end: int, status: string}], objections: [{date_objection: int, objector: string}]}: The data that has been extracted from the corporate registry.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.
            company_detail: {identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int, is_extracted: int, company_identifier: int, company_type: string}: The data of the Company Details.

        Returns:
            int
        """
        created: int = 201
        response: int = self._storeCorporateData(dataset, document_file, company_detail)
        return created if response >= 200 and response <= 299 else response

    def storeCorporateDataForeignDomestic(self, dataset: Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]], document_file: DocumentFiles) -> int:
        """
        Storing the corporate data that is extracted from the
        corporate registry for a foreign domestic company.

        Parameters:
            dataset: {status: int, company_details: {business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}, business_details: {registered_address: string, name: string, nature: string, operational: string}, certificates: [{certificate: string, type: str, date_effective: int, date_expiry: int}], office_bearers: [{position: string, name: string, address: string, date_appointment: int}], shareholders: [{name: string, amount: int, type: string, currency: string}], members: [{name: string, amount: int, date_start: int, currency: string}], annual_return: [{date_annual_return: int, date_annual_meeting: int, date_filled: int}], financial_summaries: [{financial_year: int, currency: string, date_approved: int, unit: int}], profit_statement: {financial_summary: {financial_year: int, currency: string, date_approved: int, unit: int}, turnover: float, cost_of_sales: float, gross_profit: float, other_income: float, distribution_cost: float, administration_cost: float, expenses: float, finance_cost: float, net_profit_before_taxation: float, taxation: float, net_profit: float}, state_capital: {type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}, balance_sheet: {balance_sheet: {financial_year: int, currency: string, unit: int}, assets: {non_current_assets: {property_plant_equipment: float, investment_properties: float, intangible_assets: float, other_investments: float, subsidiaries_investments: float, biological_assets: float, others: float, total: float}, current_assets: {inventories: float, trade: float, cash: float, others: float, total: float}, total: float}, liabilities: {equity_and_liabilities: {share_capital: float, other_reserves: float, retained_earnings: float, others: float, total: float}, non_current: {long_term_borrowings: float, deferred_tax: float, long_term_provisions: float, others: float, total: float}, current: {trade: float, short_term_borrowings: float, current_tax_payable: float, short_term_provisions: float, others: float, total: float}, total_liabilities: float, total_equity_and_liabilities: float}}, charges: [{volume: int, property: string, nature: string, amount: int, date_charged: int, date_filled: int, currency: string}], liquidators: {liquidator: {name: string, appointed_date: int, address: string}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}, receivers: {receiver: {name: string, date_appointed: int, address: string}, reports: [{date_filled: int, date_from: int, date_to: int}], affidavits: [{date_filled: int, date_from: int, date_to: int}]}, administrators: {administrator: {name: string, date_appointed: int, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}, details: [{type: string, date_start: int, date_end: int, status: string}], objections: [{date_objection: int, objector: string}]}: The data that has been extracted from the corporate registry.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        data_extraction_status: int = dataset["status"] # type: ignore
        if data_extraction_status == 200:
            company_detail_response: int = self.storeCorporateDataDomesticPrivateCompanyDetails(data_extraction_status, dataset["company_details"], document_file) # type: ignore
            business_detail_response: int = self.storeCorporateDataForeignDomesticBusinessDetails(company_detail_response, dataset["business_details"], document_file) # type: ignore
            certificate_response: int = self.storeCorporateDataDomesticCertificate(business_detail_response, dataset["certificates"], document_file) # type: ignore
            office_bearers_response: int = self.storeCorporateDataForeignDomesticOfficeBearers(certificate_response, dataset["office_bearers"], document_file) # type: ignore
            shareholder_response: int = self.storeCorporateDataDomesticShareholders(office_bearers_response, dataset["shareholders"], document_file) # type: ignore
            member_response: int = self.storeCorporateDataDomesticMembers(shareholder_response, dataset["members"], document_file) # type: ignore
            annual_return_response: int = self.storeCorporateDataDomesticAnnualReturn(member_response, dataset["annual_return"], document_file) # type: ignore
            financial_summary_response: int = self.storeCorporateDataDomesticFinancialSummary(annual_return_response, dataset["financial_summaries"], document_file) # type: ignore
            profit_statement_response: int = self.storeCorporateDataDomesticProfitStatement(financial_summary_response, dataset["profit_statement"], document_file) # type: ignore
            state_capital_response: int = self.storeCorporateDataDomesticStateCapital(profit_statement_response, dataset["state_capital"], document_file) # type: ignore
            balance_sheet_response: int = self.storeCorporateDataDomesticBalanceSheet(state_capital_response, dataset["balance_sheet"], document_file) # type: ignore
            charges_response: int = self.storeCorporateDataDomesticCharges(balance_sheet_response, dataset["charges"], document_file) # type: ignore
            liquidators_response: int = self.storeCorporateDataDomesticLiquidators(charges_response, dataset["liquidators"], document_file) # type: ignore
            receivers_response: int = self.storeCorporateDataDomesticReceivers(liquidators_response, dataset["receivers"], document_file) # type: ignore
            administrators_response: int = self.storeCorporateDataDomesticAdministrators(receivers_response, dataset["administrators"], document_file) # type: ignore
            details_response: int = self.storeCorporateDataDomesticDetails(administrators_response, dataset["details"], document_file) # type: ignore
            objections_response: int = self.storeCorporateDataDomesticObjections(details_response, dataset["objections"], document_file) # type: ignore
            response = objections_response
        else:
            response = 500
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {data_extraction_status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataForeignDomesticOfficeBearers(self, status: int, office_bearers: List[Dict[str, Union[str, int]]], document_file: DocumentFiles) -> int:
        """
        The data manipulation needed for the office bearers of a
        foreign domestic company.

        Parameters:
            status: int: The status of the data manipulation.
            office_bearers: [{position: string, name: string, address: string, date_appointment: int}]: The data that has been extracted for the office bearers table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        if status >= 200 and status <= 299:
            response = self._storeCorporateDataForeignDomesticOfficeBearers(office_bearers, document_file)
            self.getLogger().inform(f"The data has been successfully updated into the Office Bearers table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {office_bearers}")
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def _storeCorporateDataForeignDomesticOfficeBearers(self, office_bearers: List[Dict[str, Union[str, int]]], document_file: DocumentFiles) -> int:
        """
        Storing the office bearers of a foreign domesic company in
        its respective table in the correct form.

        Parameters:
            office_bearers: [{position: string, name: string, address: string, date_appointment: int}]: The data that has been extracted for the office bearers table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        responses: List[int] = []
        for index in range(0, len(office_bearers), 1):
            relational_database_response: int = self.__storeCorporateDataForeignDomesticOfficeBearers(office_bearers[index], document_file.company_detail)
            responses.append(relational_database_response)
        responses = list(set(responses))
        if len(responses) == 1 and responses[0] == 201:
            response = 201
        else:
            response = 503
        return response

    def __storeCorporateDataForeignDomesticOfficeBearers(self, office_bearer: Dict[str, Union[str, int]], company_detail: int) -> int:
        """
        Adding the business details of a foreign domestic company
        into the relational database server.

        Parameters:
            office_bearer: {position: string, name: string, address: string, date_appointment: int}: The data that has been extracted for the business details table.
            company_detail: int: The identifier of the company.

        Returns:
            int
        """
        if "address" in office_bearer:
            return self.getOfficeBearers().addDirectors(office_bearer, company_detail)
        else:
            return self.getOfficeBearers().addDirectorsForeignDomestic(office_bearer, company_detail)

    def storeCorporateDataForeignDomesticBusinessDetails(self, status: int, business_details: List[Dict[str, str]], document_file: DocumentFiles) -> int:
        """
        The data manipulation needed for the business details of a
        foreign domestic company.

        Parameters:
            status: int: The status of the data manipulation.
            business_details: [{name: string, nature: string, operational_address: string}]: The data that has been extracted for the business details table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        if status == 202:
            response = self._storeCorporateDataForeignDomesticBusinessDetails(business_details, document_file.company_detail)
            self.getLogger().inform(f"The data has been successfully updated into the Business Details table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {business_details}")
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def _storeCorporateDataForeignDomesticBusinessDetails(self, business_details: List[Dict[str, str]], company_detail: int) -> int:
        """
        Adding the business details into the relational database
        server.

        Parameters:
            business_details: [{name: string, nature: string, operational_address: string}]: The data that has been extracted for the business details table.
            company_detail: int: The identifier of the company.

        Returns:
            int
        """
        response: int
        responses: List[int] = []
        for index in range(0, len(business_details), 1):
            responses.append(self.__storeCorporateDataForeignDomesticBusinessDetails(business_details[index], company_detail))
        responses = list(set(responses))
        if len(responses) == 1 and responses[0] == 201:
            response = 201
            self.getLogger().inform(f"The data has been successfully updated into the Business Details table.\nStatus: {response}\nIdentifier: {company_detail}\nData: {business_details}")
        else:
            response = 503
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {response}\nCompany Detail Identifier: {company_detail}")
        return response

    def __storeCorporateDataForeignDomesticBusinessDetails(self, business_detail: Dict[str, str], company_detail: int) -> int:
        """
        Adding the business details of a foreign domestic company
        into the relational database server.

        Parameters:
            business_detail: {name: string, nature: string, operational_address: string}: The data that has been extracted for the business details table.
            company_detail: int: The identifier of the company.

        Returns:
            int
        """
        if "registered_address" in business_detail:
            return self.getBusinessDetails().addBusinessDetailsDomestic(business_detail, company_detail)
        else:
            return self.getBusinessDetails().addBusinessDetailsForeignDomestic(business_detail, company_detail)

    def storeCorporateDataGlobalBusinessCompany(self, dataset: Dict[str, Union[int, Dict[str, Union[str, int]], Dict[str, str], List[Dict[str, Union[str, int]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]], Dict[str, Union[Dict[str, str], List[Dict[str, int]]]]]], document_file: DocumentFiles) -> int:
        """
        Storing the corporate data that is extracted from the
        corporate registry for a global business company.

        Parameters:
            dataset: {status: int, company_details: {file_number: string, name: string, category: string, date_incorporation: int, nature: string, status: string}, business_details: {registered_address: string}, office_bearers: [{position: string, name: string, address: string, date_appointment: int}], receivers:  {receiver: {name: string, date_appointed: int, address: string}, reports: [{date_filled: int, date_from: int, date_to: int}], affidavits: [{date_filled: int, date_from: int, date_to: int}]}, administrators: {administrator: {name: string, designation: string, address: string, date_appointed: int}, accounts: [{date_filled: int, date_from: int, date_to: int}]}, liquidators: {liquidator: {name: string, designation: string, address: string, date_appointed: int}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}}: The data that has been extracted from the corporate registry.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        data_extraction_status: int = dataset["status"] # type: ignore
        if data_extraction_status == 200:
            company_detail_response: int = self.storeCorporateDataGlobalBusinessCompanyCompanyDetails(data_extraction_status, dataset["company_details"], document_file) # type: ignore
            business_detail_response: int = self.storeCorporateDataAuthorisedCompanyBusinessDetails(company_detail_response, dataset["business_details"], document_file) # type: ignore
            office_bearers_response: int = self.storeCorporateDataAuthorisedCompanyOfficeBearers(business_detail_response, dataset["office_bearers"], document_file) # type: ignore
            receivers_response: int = self.storeCorporateDataAuthorisedCompanyReceivers(office_bearers_response, dataset["receivers"], document_file) # type: ignore
            administrators_response: int = self.storeCorporateDataAuthorisedCompanyAdministrators(receivers_response, dataset["administrators"], document_file) # type: ignore
            liquidators_response: int = self.storeCorporateDataAuthorisedCompanyLiquidators(administrators_response, dataset["liquidators"], document_file) # type: ignore
            state_capital_response: int = self.storeCorporateDataDomesticStateCapital(liquidators_response, dataset["state_capital"], document_file) # type: ignore
            response = state_capital_response
        else:
            response = 500
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {data_extraction_status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataGlobalBusinessCompanyCompanyDetails(self, status: int, company_details: Dict[str, Union[str, int]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on the Company Details dataset
        of a global business company.

        Parameters:
            data_extraction: int: The status of the data extraction.
            company_details: {name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}: The data that has been extracted for the company details table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        date_verified: int = int(time())
        is_extracted: int = 1
        company_identifier: int = int("".join(findall(r"\d+", str(company_details["file_number"]))))
        company_type: str = "".join(findall(r"[A-Z]+", str(company_details["file_number"])))
        if status == 200:
            company_details["date_verified"] = date_verified
            company_details["is_extracted"] = is_extracted
            company_details["company_identifier"] = company_identifier
            company_details["company_type"] = company_type
            response = self.getCompanyDetails().updateCorporateMetadataAuthorisedCompany(company_details, document_file.company_detail)
            self.getLogger().inform(f"The data has been successfully updated into the Company Details table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {company_details}")
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataAuthorisedCompany(self, dataset: Dict[str, Union[int, Dict[str, Union[str, int]], Dict[str, str], List[Dict[str, Union[str, int]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]], Dict[str, Union[Dict[str, str], List[Dict[str, int]]]]]], document_file: DocumentFiles) -> int:
        """
        Storing the corporate data that is extracted from the
        corporate registry for an authorised company.

        Parameters:
            dataset: {status: int, company_details: {name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}, business_details: {registered_address: string}, office_bearers: [{position: string, name: string, address: string, date_appointment: int}], receivers: {receiver: {name: string, date_appointed: int, address: string}, reports: [{date_filled: int, date_from: int, date_to: int}], affidavits: [{date_filled: int, date_from: int, date_to: int}]}, administrators: {administrator: {name: string, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}, liquidators: {liquidator: {name: string, address: string}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}}: The data that has been extracted from the corporate registry.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        data_extraction_status: int = dataset["status"] # type: ignore
        if data_extraction_status == 200:
            company_detail_response: int = self.storeCorporateDataAuthorisedCompanyCompanyDetails(data_extraction_status, dataset["company_details"], document_file) # type: ignore
            business_detail_response: int = self.storeCorporateDataAuthorisedCompanyBusinessDetails(company_detail_response, dataset["business_details"], document_file) # type: ignore
            office_bearers_response: int = self.storeCorporateDataAuthorisedCompanyOfficeBearers(business_detail_response, dataset["office_bearers"], document_file) # type: ignore
            receivers_response: int = self.storeCorporateDataAuthorisedCompanyReceivers(office_bearers_response, dataset["receivers"], document_file) # type: ignore
            administrators_response: int = self.storeCorporateDataAuthorisedCompanyAdministrators(receivers_response, dataset["administrators"], document_file) # type: ignore
            liquidators_response: int = self.storeCorporateDataAuthorisedCompanyLiquidators(administrators_response, dataset["liquidators"], document_file) # type: ignore
            response = liquidators_response
        else:
            response = 500
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {data_extraction_status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataAuthorisedCompanyLiquidators(self, status: int, liquidators: Dict[str, Union[Dict[str, str], List[Dict[str, int]]]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on liquidators of an authorised
        company result set.

        Parameters:
            status: int: The status of the data manipulation.
            liquidators: {liquidator: {name: string, address: string}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}: The data that has been extracted for the liquidators table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        if status >= 200 and status <= 299 and not liquidators:
            response = 200
            self.getLogger().inform(f"There is no data to be inserted into the Liquidators table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {liquidators}")
        elif status >= 200 and status <= 299 and len(liquidators) != 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Builder.storeCorporateDataDomesticLiquidators()")
            exit()
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataAuthorisedCompanyAdministrators(self, status: int, administrators: Dict[str, Union[Dict[str, str], List[Dict[str, int]]]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on administrators of an
        authorised company result set.

        Parameters:
            status: int: The status of the data manipulation.
            administrators: {administrator: {name: string, date_appointed: int, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}: The data that has been extracted for the administrators table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        if status >= 200 and status <= 299 and not administrators:
            response = 200
            self.getLogger().inform(f"There is no data to be inserted into the Administrators table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {administrators}")
        elif status >= 200 and status <= 299 and len(administrators) != 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Builder.storeCorporateDataDomesticAdministrators()")
            exit()
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataAuthorisedCompanyReceivers(self, status: int, receivers: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on receivers result set.

        Parameters:
            status: int: The status of the data manipulation.
            receivers: {receiver: {name: string, date_appointed: int, address: string}, reports: [{date_filled: int, date_from: int, date_to: int}], affidavits: [{date_filled: int, date_from: int, date_to: int}]}: The data that has been extracted for the receivers table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        if status >= 200 and status <= 299 and not receivers:
            response = 200
            self.getLogger().inform(f"There is no data to be inserted into the Receivers table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {receivers}")
        elif status >= 200 and status <= 299 and len(receivers) != 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Builder.storeCorporateDataDomesticReceivers()")
            exit()
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataAuthorisedCompanyOfficeBearers(self, status: int, office_bearers: List[Dict[str, Union[str, int]]], document_file: DocumentFiles) -> int:
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
            response = self._storeCorporateDataAuthorisedCompanyOfficeBearers(office_bearers, document_file)
            self.getLogger().inform(f"The data has been successfully updated into the Office Bearers table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {office_bearers}")
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def _storeCorporateDataAuthorisedCompanyOfficeBearers(self, office_bearers: List[Dict[str, Union[str, int]]], document_file: DocumentFiles) -> int:
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

    def storeCorporateDataAuthorisedCompanyBusinessDetails(self, status: int, business_details: Dict[str, str], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on the Business Details result
        set.

        Parameters:
            status: int: The status of the data manipulation.
            business_details: {registered_address: string}: The data that has been extracted for the business details table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        if status == 202:
            response = self.getBusinessDetails().addBusinessDetailsAuthorisedCompany(business_details, document_file.company_detail)
            self.getLogger().inform(f"The data has been successfully updated into the Business Details table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {business_details}")
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataAuthorisedCompanyCompanyDetails(self, status: int, company_details: Dict[str, Union[str, int]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on the Company Details result
        set.

        Parameters:
            data_extraction: int: The status of the data extraction.
            company_details: {name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}: The data that has been extracted for the company details table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        date_verified: int = int(time())
        is_extracted: int = 1
        company_identifier: int = int("".join(findall(r"\d+", str(company_details["file_number"]))))
        company_type: str = "".join(findall(r"[A-Z]+", str(company_details["file_number"])))
        if status == 200:
            company_details["date_verified"] = date_verified
            company_details["is_extracted"] = is_extracted
            company_details["company_identifier"] = company_identifier
            company_details["company_type"] = company_type
            response = self.getCompanyDetails().updateCorporateMetadataAuthorisedCompany(company_details, document_file.company_detail)
            self.getLogger().inform(f"The data has been successfully updated into the Company Details table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {company_details}")
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataDomestic(self, dataset: Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]], document_file: DocumentFiles, company_detail: CompanyDetails) -> int:
        """
        Storing the corporate data that is extracted from the
        corporate registry for a domestic company.

        Parameters:
            dataset: {status: int, company_details: {business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}, business_details: {registered_address: string, name: string, nature: string, operational: string}, certificates: [{certificate: string, type: str, date_effective: int, date_expiry: int}], office_bearers: [{position: string, name: string, address: string, date_appointment: int}], shareholders: [{name: string, amount: int, type: string, currency: string}], members: [{name: string, amount: int, date_start: int, currency: string}], annual_return: [{date_annual_return: int, date_annual_meeting: int, date_filled: int}], financial_summaries: [{financial_year: int, currency: string, date_approved: int, unit: int}], profit_statement: {financial_summary: {financial_year: int, currency: string, date_approved: int, unit: int}, turnover: float, cost_of_sales: float, gross_profit: float, other_income: float, distribution_cost: float, administration_cost: float, expenses: float, finance_cost: float, net_profit_before_taxation: float, taxation: float, net_profit: float}, state_capital: {type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}, balance_sheet: {balance_sheet: {financial_year: int, currency: string, unit: int}, assets: {non_current_assets: {property_plant_equipment: float, investment_properties: float, intangible_assets: float, other_investments: float, subsidiaries_investments: float, biological_assets: float, others: float, total: float}, current_assets: {inventories: float, trade: float, cash: float, others: float, total: float}, total: float}, liabilities: {equity_and_liabilities: {share_capital: float, other_reserves: float, retained_earnings: float, others: float, total: float}, non_current: {long_term_borrowings: float, deferred_tax: float, long_term_provisions: float, others: float, total: float}, current: {trade: float, short_term_borrowings: float, current_tax_payable: float, short_term_provisions: float, others: float, total: float}, total_liabilities: float, total_equity_and_liabilities: float}}, charges: [{volume: int, property: string, nature: string, amount: int, date_charged: int, date_filled: int, currency: string}], liquidators: {liquidator: {name: string, appointed_date: int, address: string}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}, receivers: {receiver: {name: string, date_appointed: int, address: string}, reports: [{date_filled: int, date_from: int, date_to: int}], affidavits: [{date_filled: int, date_from: int, date_to: int}]}, administrators: {administrator: {name: string, date_appointed: int, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}, details: [{type: string, date_start: int, date_end: int, status: string}], objections: [{date_objection: int, objector: string}]}: The data that has been extracted from the corporate registry.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.
            company_detail: {identifier: int, business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string, date_verified: int, is_extracted: int, company_identifier: int, company_type: string}: The data of the Company Details.

        Returns:
            int
        """
        response: int
        if company_detail.nature.upper() == "PRIVATE":
            response = self.storeCorporateDataDomesticPrivate(dataset, document_file)
        elif company_detail.nature.upper() == "CIVIL" or company_detail.nature.upper() == "COMMERCIAL":
            response = self.storeCorporateDataDomesticCivil(dataset, document_file)
        elif company_detail.nature.upper() == "PUBLIC":
            response = self.storeCorporateDataDomesticPublic(dataset, document_file)
        else:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Builder.storeCorporateDataDomestic()")
            exit()
        return response

    def storeCorporateDataDomesticPublic(self, dataset: Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]], document_file: DocumentFiles) -> int:
        """
        Storing the corporate data that is extracted from the
        corporate registry for a private domestic company.

        Parameters:
            dataset: {status: int, company_details: {business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}, business_details: {registered_address: string, name: string, nature: string, operational: string}, certificates: [{certificate: string, type: str, date_effective: int, date_expiry: int}], office_bearers: [{position: string, name: string, address: string, date_appointment: int}], shareholders: [{name: string, amount: int, type: string, currency: string}], members: [{name: string, amount: int, date_start: int, currency: string}], annual_return: [{date_annual_return: int, date_annual_meeting: int, date_filled: int}], financial_summaries: [{financial_year: int, currency: string, date_approved: int, unit: int}], profit_statement: {financial_summary: {financial_year: int, currency: string, date_approved: int, unit: int}, turnover: float, cost_of_sales: float, gross_profit: float, other_income: float, distribution_cost: float, administration_cost: float, expenses: float, finance_cost: float, net_profit_before_taxation: float, taxation: float, net_profit: float}, state_capital: {type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}, balance_sheet: {balance_sheet: {financial_year: int, currency: string, unit: int}, assets: {non_current_assets: {property_plant_equipment: float, investment_properties: float, intangible_assets: float, other_investments: float, subsidiaries_investments: float, biological_assets: float, others: float, total: float}, current_assets: {inventories: float, trade: float, cash: float, others: float, total: float}, total: float}, liabilities: {equity_and_liabilities: {share_capital: float, other_reserves: float, retained_earnings: float, others: float, total: float}, non_current: {long_term_borrowings: float, deferred_tax: float, long_term_provisions: float, others: float, total: float}, current: {trade: float, short_term_borrowings: float, current_tax_payable: float, short_term_provisions: float, others: float, total: float}, total_liabilities: float, total_equity_and_liabilities: float}}, charges: [{volume: int, property: string, nature: string, amount: int, date_charged: int, date_filled: int, currency: string}], liquidators: {liquidator: {name: string, appointed_date: int, address: string}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}, receivers: {receiver: {name: string, date_appointed: int, address: string}, reports: [{date_filled: int, date_from: int, date_to: int}], affidavits: [{date_filled: int, date_from: int, date_to: int}]}, administrators: {administrator: {name: string, date_appointed: int, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}, details: [{type: string, date_start: int, date_end: int, status: string}], objections: [{date_objection: int, objector: string}]}: The data that has been extracted from the corporate registry.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        data_extraction_status: int = dataset["status"] # type: ignore
        if data_extraction_status == 200:
            company_detail_response: int = self.storeCorporateDataDomesticPrivateCompanyDetails(data_extraction_status, dataset["company_details"], document_file) # type: ignore
            business_detail_response: int = self.storeCorporateDataDomesticPrivateBusinessDetail(company_detail_response, dataset["business_details"], document_file) # type: ignore
            certificate_response: int = self.storeCorporateDataDomesticCertificate(business_detail_response, dataset["certificates"], document_file) # type: ignore
            office_bearers_response: int = self.storeCorporateDataDomesticOfficeBearers(certificate_response, dataset["office_bearers"], document_file) # type: ignore
            shareholder_response: int = self.storeCorporateDataDomesticShareholders(office_bearers_response, dataset["shareholders"], document_file) # type: ignore
            member_response: int = self.storeCorporateDataDomesticMembers(shareholder_response, dataset["members"], document_file) # type: ignore
            annual_return_response: int = self.storeCorporateDataDomesticAnnualReturn(member_response, dataset["annual_return"], document_file) # type: ignore
            financial_summary_response: int = self.storeCorporateDataDomesticFinancialSummary(annual_return_response, dataset["financial_summaries"], document_file) # type: ignore
            profit_statement_response: int = self.storeCorporateDataDomesticProfitStatement(financial_summary_response, dataset["profit_statement"], document_file) # type: ignore
            state_capital_response: int = self.storeCorporateDataDomesticStateCapital(profit_statement_response, dataset["state_capital"], document_file) # type: ignore
            balance_sheet_response: int = self.storeCorporateDataDomesticBalanceSheet(state_capital_response, dataset["balance_sheet"], document_file) # type: ignore
            charges_response: int = self.storeCorporateDataDomesticCharges(balance_sheet_response, dataset["charges"], document_file) # type: ignore
            liquidators_response: int = self.storeCorporateDataDomesticLiquidators(charges_response, dataset["liquidators"], document_file) # type: ignore
            receivers_response: int = self.storeCorporateDataDomesticReceivers(liquidators_response, dataset["receivers"], document_file) # type: ignore
            administrators_response: int = self.storeCorporateDataDomesticAdministrators(receivers_response, dataset["administrators"], document_file) # type: ignore
            details_response: int = self.storeCorporateDataDomesticDetails(administrators_response, dataset["details"], document_file) # type: ignore
            objections_response: int = self.storeCorporateDataDomesticObjections(details_response, dataset["objections"], document_file) # type: ignore
            response = objections_response
        else:
            response = 500
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {data_extraction_status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataDomesticCivil(self, dataset: Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]], document_file: DocumentFiles) -> int:
        """
        Storing the corporate data that is extracted from the
        corporate registry for a private domestic company.

        Parameters:
            dataset: {status: int, company_details: {business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}, business_details: {registered_address: string, name: string, nature: string, operational: string}, certificates: [{certificate: string, type: str, date_effective: int, date_expiry: int}], office_bearers: [{position: string, name: string, address: string, date_appointment: int}], shareholders: [{name: string, amount: int, type: string, currency: string}], members: [{name: string, amount: int, date_start: int, currency: string}], annual_return: [{date_annual_return: int, date_annual_meeting: int, date_filled: int}], financial_summaries: [{financial_year: int, currency: string, date_approved: int, unit: int}], profit_statement: {financial_summary: {financial_year: int, currency: string, date_approved: int, unit: int}, turnover: float, cost_of_sales: float, gross_profit: float, other_income: float, distribution_cost: float, administration_cost: float, expenses: float, finance_cost: float, net_profit_before_taxation: float, taxation: float, net_profit: float}, state_capital: {type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}, balance_sheet: {balance_sheet: {financial_year: int, currency: string, unit: int}, assets: {non_current_assets: {property_plant_equipment: float, investment_properties: float, intangible_assets: float, other_investments: float, subsidiaries_investments: float, biological_assets: float, others: float, total: float}, current_assets: {inventories: float, trade: float, cash: float, others: float, total: float}, total: float}, liabilities: {equity_and_liabilities: {share_capital: float, other_reserves: float, retained_earnings: float, others: float, total: float}, non_current: {long_term_borrowings: float, deferred_tax: float, long_term_provisions: float, others: float, total: float}, current: {trade: float, short_term_borrowings: float, current_tax_payable: float, short_term_provisions: float, others: float, total: float}, total_liabilities: float, total_equity_and_liabilities: float}}, charges: [{volume: int, property: string, nature: string, amount: int, date_charged: int, date_filled: int, currency: string}], liquidators: {liquidator: {name: string, appointed_date: int, address: string}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}, receivers: {receiver: {name: string, date_appointed: int, address: string}, reports: [{date_filled: int, date_from: int, date_to: int}], affidavits: [{date_filled: int, date_from: int, date_to: int}]}, administrators: {administrator: {name: string, date_appointed: int, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}, details: [{type: string, date_start: int, date_end: int, status: string}], objections: [{date_objection: int, objector: string}]}: The data that has been extracted from the corporate registry.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        data_extraction_status: int = dataset["status"] # type: ignore
        if data_extraction_status == 200:
            company_detail_response: int = self.storeCorporateDataDomesticCivilCompanyDetails(data_extraction_status, dataset["company_details"], document_file) # type: ignore
            business_detail_response: int = self.storeCorporateDataDomesticCivilBusinessDetail(company_detail_response, dataset["business_details"], document_file) # type: ignore
            office_bearers_response: int = self.storeCorporateDataDomesticOfficeBearers(business_detail_response, dataset["office_bearers"], document_file) # type: ignore
            state_capital_response: int = self.storeCorporateDataDomesticStateCapital(office_bearers_response, dataset["state_capital"], document_file) # type: ignore
            shareholder_response: int = self.storeCorporateDataDomesticShareholders(state_capital_response, dataset["shareholders"], document_file) # type: ignore
            liquidators_response: int = self.storeCorporateDataDomesticLiquidators(shareholder_response, dataset["liquidators"], document_file) # type: ignore
            receivers_response: int = self.storeCorporateDataDomesticReceivers(liquidators_response, dataset["receivers"], document_file) # type: ignore
            administrators_response: int = self.storeCorporateDataDomesticAdministrators(receivers_response, dataset["administrators"], document_file) # type: ignore
            details_response: int = self.storeCorporateDataDomesticDetails(administrators_response, dataset["details"], document_file) # type: ignore
            objections_response: int = self.storeCorporateDataDomesticObjections(details_response, dataset["objections"], document_file) # type: ignore
            response = objections_response
        else:
            response = 500
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {data_extraction_status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataDomesticCivilCompanyDetails(self, status: int, company_details: Dict[str, Union[str, int]], document_file: DocumentFiles) -> int:
        """
        Executing the data manipulation for the company details of a
        société civile.

        Parameters:
            status: int: The status of the previous operation.
            company_details: {name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}: The data that has been extracted for the company details table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        date_verified: int = int(time())
        is_extracted: int = 1
        company_identifier: int = int("".join(findall(r"\d+", str(company_details["file_number"]))))
        company_type: str = "".join(findall(r"[A-Z]+", str(company_details["file_number"])))
        if status == 200:
            company_details["date_verified"] = date_verified
            company_details["is_extracted"] = is_extracted
            company_details["company_identifier"] = company_identifier
            company_details["company_type"] = company_type
            response = self.getCompanyDetails().updateCorporateMetadataDomesticCivil(company_details, document_file.company_detail)
            self.getLogger().inform(f"The data has been successfully updated into the Company Details table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {company_details}")
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataDomesticPrivate(self, dataset: Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]], document_file: DocumentFiles) -> int:
        """
        Storing the corporate data that is extracted from the
        corporate registry for a private domestic company.

        Parameters:
            dataset: {status: int, company_details: {business_registration_number: string, name: string, file_number: string, category: string, date_incorporation: int, nature: string, status: string}, business_details: {registered_address: string, name: string, nature: string, operational: string}, certificates: [{certificate: string, type: str, date_effective: int, date_expiry: int}], office_bearers: [{position: string, name: string, address: string, date_appointment: int}], shareholders: [{name: string, amount: int, type: string, currency: string}], members: [{name: string, amount: int, date_start: int, currency: string}], annual_return: [{date_annual_return: int, date_annual_meeting: int, date_filled: int}], financial_summaries: [{financial_year: int, currency: string, date_approved: int, unit: int}], profit_statement: {financial_summary: {financial_year: int, currency: string, date_approved: int, unit: int}, turnover: float, cost_of_sales: float, gross_profit: float, other_income: float, distribution_cost: float, administration_cost: float, expenses: float, finance_cost: float, net_profit_before_taxation: float, taxation: float, net_profit: float}, state_capital: {type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}, balance_sheet: {balance_sheet: {financial_year: int, currency: string, unit: int}, assets: {non_current_assets: {property_plant_equipment: float, investment_properties: float, intangible_assets: float, other_investments: float, subsidiaries_investments: float, biological_assets: float, others: float, total: float}, current_assets: {inventories: float, trade: float, cash: float, others: float, total: float}, total: float}, liabilities: {equity_and_liabilities: {share_capital: float, other_reserves: float, retained_earnings: float, others: float, total: float}, non_current: {long_term_borrowings: float, deferred_tax: float, long_term_provisions: float, others: float, total: float}, current: {trade: float, short_term_borrowings: float, current_tax_payable: float, short_term_provisions: float, others: float, total: float}, total_liabilities: float, total_equity_and_liabilities: float}}, charges: [{volume: int, property: string, nature: string, amount: int, date_charged: int, date_filled: int, currency: string}], liquidators: {liquidator: {name: string, appointed_date: int, address: string}, affidavits: [{date_filled: int, date_from: int, date_to: int}]}, receivers: {receiver: {name: string, date_appointed: int, address: string}, reports: [{date_filled: int, date_from: int, date_to: int}], affidavits: [{date_filled: int, date_from: int, date_to: int}]}, administrators: {administrator: {name: string, date_appointed: int, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}, details: [{type: string, date_start: int, date_end: int, status: string}], objections: [{date_objection: int, objector: string}]}: The data that has been extracted from the corporate registry.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        data_extraction_status: int = dataset["status"] # type: ignore
        if data_extraction_status == 200:
            company_detail_response: int = self.storeCorporateDataDomesticPrivateCompanyDetails(data_extraction_status, dataset["company_details"], document_file) # type: ignore
            business_detail_response: int = self.storeCorporateDataDomesticPrivateBusinessDetail(company_detail_response, dataset["business_details"], document_file) # type: ignore
            certificate_response: int = self.storeCorporateDataDomesticCertificate(business_detail_response, dataset["certificates"], document_file) # type: ignore
            office_bearers_response: int = self.storeCorporateDataDomesticOfficeBearers(certificate_response, dataset["office_bearers"], document_file) # type: ignore
            shareholder_response: int = self.storeCorporateDataDomesticShareholders(office_bearers_response, dataset["shareholders"], document_file) # type: ignore
            member_response: int = self.storeCorporateDataDomesticMembers(shareholder_response, dataset["members"], document_file) # type: ignore
            annual_return_response: int = self.storeCorporateDataDomesticAnnualReturn(member_response, dataset["annual_return"], document_file) # type: ignore
            financial_summary_response: int = self.storeCorporateDataDomesticFinancialSummary(annual_return_response, dataset["financial_summaries"], document_file) # type: ignore
            profit_statement_response: int = self.storeCorporateDataDomesticProfitStatement(financial_summary_response, dataset["profit_statement"], document_file) # type: ignore
            state_capital_response: int = self.storeCorporateDataDomesticStateCapital(profit_statement_response, dataset["state_capital"], document_file) # type: ignore
            balance_sheet_response: int = self.storeCorporateDataDomesticBalanceSheet(state_capital_response, dataset["balance_sheet"], document_file) # type: ignore
            charges_response: int = self.storeCorporateDataDomesticCharges(balance_sheet_response, dataset["charges"], document_file) # type: ignore
            liquidators_response: int = self.storeCorporateDataDomesticLiquidators(charges_response, dataset["liquidators"], document_file) # type: ignore
            receivers_response: int = self.storeCorporateDataDomesticReceivers(liquidators_response, dataset["receivers"], document_file) # type: ignore
            administrators_response: int = self.storeCorporateDataDomesticAdministrators(receivers_response, dataset["administrators"], document_file) # type: ignore
            details_response: int = self.storeCorporateDataDomesticDetails(administrators_response, dataset["details"], document_file) # type: ignore
            objections_response: int = self.storeCorporateDataDomesticObjections(details_response, dataset["objections"], document_file) # type: ignore
            response = objections_response
        else:
            response = 500
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {data_extraction_status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataDomesticObjections(self, status: int, objections: List[Dict[str, Union[int, str]]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on the objections result set.

        Parameters:
            status: int: The status of the data manipulation.
            objections: [{date_objection: int, objector: string}]: The data that has been extracted for the objections table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        ok: int = 200
        service_unavailable: int = 503
        created: int = 201
        if status >= 200 and status <= 299 and len(objections) == 0:
            self.getLogger().inform(f"There is no data to be inserted into the Objections table.\nStatus: {ok}\nIdentifier: {document_file.company_detail}\nData: {objections}")
            return ok
        if status < 200 and status > 299:
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {status}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
            return service_unavailable
        statuses: List[int] = list(set([self.getObjections().addObjection(objection, document_file.company_detail) for objection in objections]))
        response: int = created if len(statuses) == 1 and statuses[0] == created else service_unavailable
        self.getLogger().inform(f"Data has been inserted into the Objections table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {objections}")
        return response

    def storeCorporateDataDomesticDetails(self, status: int, details: List[Dict[str, Union[str, int, None]]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on the details result set.

        Parameters:
            status: int: The status of the data manipulation.
            details: [{type: string, date_start: int, date_end: int|null, status: string}]: The data that has been extracted for the details table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        ok: int = 200
        service_unavailable: int = 503
        created: int = 201
        if status >= 200 and status <= 299 and len(details) == 0:
            self.getLogger().inform(f"There is no data to be inserted into the Details table.\nStatus: {ok}\nIdentifier: {document_file.company_detail}\nData: {details}")
            return ok
        if status < 200 and status > 299:
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {service_unavailable}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
            return service_unavailable
        statuses: List[int] = list(set([self.getDetails().addDetail(detail, document_file.company_detail) for detail in details]))
        response: int = created if len(statuses) == 1 and statuses[0] == created else service_unavailable
        self.getLogger().inform(f"The data has been successfully inserted into the Details table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {details}")
        return response

    def storeCorporateDataDomesticAdministrators(self, status: int, administrators: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on administrators result set.

        Parameters:
            status: int: The status of the data manipulation.
            administrators: {administrator: {name: string, date_appointed: int, designation: string, address: string}, accounts: [{date_filled: int, date_from: int, date_to: int}]}: The data that has been extracted for the administrators table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        if status >= 200 and status <= 299 and not administrators:
            response = 200
            self.getLogger().inform(f"There is no data to be inserted into the Administrators table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {administrators}")
        elif status >= 200 and status <= 299 and len(administrators) != 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Builder.storeCorporateDataDomesticAdministrators()")
            exit()
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataDomesticReceivers(self, status: int, receivers: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on receivers result set.

        Parameters:
            status: int: The status of the data manipulation.
            receivers: {receiver: {name: string, date_appointed: int, address: string}, reports: [{date_filled: int, date_from: int, date_to: int}], affidavits: [{date_filled: int, date_from: int, date_to: int}]}: The data that has been extracted for the receivers table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        if status >= 200 and status <= 299 and not receivers:
            response = 200
            self.getLogger().inform(f"There is no data to be inserted into the Receivers table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {receivers}")
        elif status >= 200 and status <= 299 and len(receivers) != 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Builder.storeCorporateDataDomesticReceivers()")
            exit()
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataDomesticLiquidators(self, status: int, liquidators: Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]], document_file: DocumentFiles) -> int:
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
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Builder.storeCorporateDataDomesticLiquidators()")
            exit()
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataDomesticCharges(self, status: int, charges: List[Dict[str, Union[int, str]]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on the charges result set.

        Parameters:
            status: int: The status of the data manipulation.
            charges: [{volume: string, property: string, nature: string, amount: int, date_charged: int, date_filled: int, currency: string}]: The data that has been extracted for the charges table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        ok: int = 200
        service_unavailable: int = 503
        created: int = 201
        if status >= 200 and status <= 299 and len(charges) == 0:
            self.getLogger().inform(f"There is no data to be inserted into the Charges table.\nStatus: {ok}\nIdentifier: {document_file.company_detail}\nData: {charges}")
            return ok
        if status < 200 and status > 299:
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {service_unavailable}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
            return service_unavailable
        statuses: List[int] = [self.getCharges().addCharge(charge, document_file.company_detail) for charge in charges]
        response: int = created if len(statuses) == 1 and statuses[0] == created else service_unavailable
        self.getLogger().inform(f"The data has been successfully inserted in the Charges table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {charges}")
        return response

    def storeCorporateDataDomesticBalanceSheet(self, status: int, balance_sheet: Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], document_file: DocumentFiles) -> int:
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
        ok: int = 200
        service_unavailable: int = 503
        created: int = 201
        if status < 200 and status > 299:
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {status}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
            return status
        if status >= 200 and status <= 299 and not balance_sheet:
            self.getLogger().inform(f"There is no data to be inserted into the Balance Sheet table.\nStatus: {ok}\nIdentifier: {document_file.company_detail}\nData: {balance_sheet}")
            return ok
        if not balance_sheet:
            return status
        response = self.getBalanceSheets().addBalanceSheet(balance_sheet["balance_sheet"], document_file.company_detail) # type: ignore
        if response != created:
            self.getLogger().error(f"An error occurred while inserting the balance sheet into the relational database server.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {balance_sheet}")
            return service_unavailable
        archived_balance_sheet: BalanceSheets = self.getBalanceSheets().getSpecific(document_file.company_detail, balance_sheet["balance_sheet"]["financial_year"]) # type: ignore
        response = self.getAssets().addAssets(balance_sheet["assets"], archived_balance_sheet.identifier) # type: ignore
        if response != created:
            self.getLogger().error(f"An error occurred while inserting the assets into the relational database server.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {balance_sheet}")
            return service_unavailable
        assets: Assets = self.getAssets().getSpecific(archived_balance_sheet.identifier)
        response = self.getNonCurrentAssets().addAsset(balance_sheet["assets"]["non_current_assets"], assets.identifier) # type: ignore
        if response != created:
            self.getLogger().error(f"An error occurred while inserting the non current assets into the relational database server.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {balance_sheet}")
            return service_unavailable
        response = self.getCurrentAssets().addAsset(balance_sheet["assets"]["current_assets"], assets.identifier) # type: ignore
        if response != created:
            self.getLogger().error(f"An error occurred while inserting the current assets into the relational database server.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {balance_sheet}")
            return service_unavailable
        response = self.getLiabilities().addLiabilities(balance_sheet["liabilities"], archived_balance_sheet.identifier) # type: ignore
        if response != created:
            self.getLogger().error(f"An error occurred while inserting the liabilities into the relational database server.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {balance_sheet}")
            return service_unavailable
        liabilities: Liabilities = self.getLiabilities().getSpecific(archived_balance_sheet.identifier)
        response = self.getEquityAndLiabilities().addLiability(balance_sheet["liabilities"]["equity_and_liabilities"], liabilities.identifier) # type: ignore
        if response != created:
            self.getLogger().error(f"An error occurred while inserting the equity and liabilities into the relational database server.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {balance_sheet}")
            return service_unavailable
        response = self.getNonCurrentLiabilities().addLiability(balance_sheet["liabilities"]["non_current"], liabilities.identifier) # type: ignore
        if response != created:
            self.getLogger().error(f"An error occurred while inserting the non current liabilities into the relational database server.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {balance_sheet}")
            return service_unavailable
        response = self.getCurrentLiabilities().addLiability(balance_sheet["liabilities"]["current"], liabilities.identifier) # type: ignore
        if response != created:
            self.getLogger().error(f"An error occurred while inserting the non current liabilities into the relational database server.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {balance_sheet}")
            return service_unavailable
        return response

    def storeCorporateDataDomesticProfitStatement(self, status: int, profit_statement: Dict[str, Union[Dict[str, Union[int, str]], float]], document_file: DocumentFiles) -> int:
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
        ok: int = 200
        accepted: int = 202
        service_unavailable: int = 503
        if status < 200 and status > 299:
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {status}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
            return status
        if status >= 200 and status <= 299 and not profit_statement:
            self.getLogger().inform(f"There is no data to be inserted into the Profit Statement table.\nStatus: {ok}\nIdentifier: {document_file.company_detail}\nData: {profit_statement}")
            return ok
        if not profit_statement:
            return status
        financial_summary: FinancialSummaries = self.getFinancialSummaries().getSpecific(document_file.company_detail, profit_statement["financial_summary"]["financial_year"]) # type: ignore
        financial_summary.unit = profit_statement["financial_summary"]["unit"] # type: ignore
        response = self.getFinancialSummaries().update(financial_summary)
        response = self.getProfitStatements().addProfitStatement(profit_statement, financial_summary.identifier) if response == accepted else service_unavailable
        self.getLogger().inform(f"The data has been successfully inserted into the Profit Statements table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {profit_statement}")
        return response

    def storeCorporateDataDomesticFinancialSummary(self, status: int, financial_summaries: List[Dict[str, Union[int, str]]], document_file: DocumentFiles) -> int:
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
        ok: int = 200
        created: int = 201
        service_unavailable: int = 503
        if status < 200 and status > 299:
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {status}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
            return status
        if status >= 200 and status <= 299 and len(financial_summaries) == 0:
            self.getLogger().inform(f"There is no data to be inserted into the Financial Summaries table.\nStatus: {ok}\nIdentifier: {document_file.company_detail}\nData: {financial_summaries}")
            return ok
        statuses: List[int] = list(set([self.getFinancialSummaries().addFinancialSummary(financial_summary, document_file.company_detail) for financial_summary in financial_summaries]))
        response: int = created if len(statuses) == 1 and statuses[0] == created else service_unavailable
        self.getLogger().inform(f"Data has been stored into the Financial Summaries table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {financial_summaries}")
        return response

    def storeCorporateDataDomesticAnnualReturn(self, status: int, annual_return: List[Dict[str, int]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on the annual return result set.

        Parameters:
            status: int: The status of the data manipulation.
            annual_return: [{date_annual_return: int, date_annual_meeting: int, date_filled: int}]: The data that has been extracted for the annual return table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        ok: int = 200
        created: int = 201
        service_unavailable: int = 503
        if status < 200 and status > 299:
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {status}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
            return status
        if status >= 200 and status <= 299 and len(annual_return) == 0:
            self.getLogger().inform(f"There is no data to be inserted into the Annual Return table.\nStatus: {ok}\nIdentifier: {document_file.company_detail}\nData: {annual_return}")
            return ok
        statuses: List[int] = list(set([self.getAnnualReturns().addAnnualReturn(annual_return_statement, document_file.company_detail) for annual_return_statement in annual_return]))
        response: int = created if len(statuses) == 1 and statuses[0] else service_unavailable
        self.getLogger().inform(f"Data has been stored into the Annual Returns table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {annual_return}")
        return response

    def storeCorporateDataDomesticMembers(self, status: int, members: List[Dict[str, Union[str, int]]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on the members result set.

        Parameters:
            status: int: The status of the data manipulation.
            members: [{name: string, amount: int, date_start: int, currency: string}]: The data that has been extracted for the members table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        if status == 201 and len(members) > 0:
            response = self._storeCorporateDataDomesticMembers(members, document_file.company_detail)
            self.getLogger().inform(f"Data has been stored into the Members table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {members}")
        elif status == 201 and len(members) == 0:
            response = 200
            self.getLogger().inform(f"There is no data to be inserted into the Members table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {members}")
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def _storeCorporateDataDomesticMembers(self, members: List[Dict[str, Union[str, int]]], company_detail: int) -> int:
        """
        Storing the members data of a private domestic company into
        the relational database server.

        Parameters:
            members: [{name: string, amount: int, date_start: int, currency: string}]: The data that has been extracted for the members table.
            company_detail: int: The identfier of the company.

        Returns:
            int
        """
        relational_database_responses: List[int] = []
        response: int
        for index in range(0, len(members), 1):
            relational_database_responses.append(self.getMembers().addMember(members[index], company_detail))
        relational_database_responses = list(set(relational_database_responses))
        if len(relational_database_responses) == 1 and relational_database_responses[0] == 201:
            response = relational_database_responses[0]
        else:
            response = max(relational_database_responses)
        return response

    def storeCorporateDataDomesticCertificate(self, status: int, certificates: List[Dict[str, Union[str, int]]], document_file: DocumentFiles) -> int:
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
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Builder.storeCorporateDataDomesticCertificate()")
            exit()
        elif status == 201 and len(certificates) == 0:
            response = 200
            self.getLogger().inform(f"There is no data to be inserted into the Certificate table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {certificates}")
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataDomesticShareholders(self, status: int, shareholders: List[Dict[str, Union[str, int]]], document_file: DocumentFiles) -> int:
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
        if status >= 200 and status <= 299:
            response = self._storeCorporateDataDomesticShareholders(shareholders, document_file.company_detail)
            self.getLogger().inform(f"The data has been successfully updated into the Shareholders table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {shareholders}")
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def _storeCorporateDataDomesticShareholders(self, shareholders: List[Dict[str, Union[str, int]]], company_detail: int) -> int:
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
        elif len(responses) == 0:
            response = 200
        else:
            response = 503
        return response

    def storeCorporateDataDomesticOfficeBearers(self, status: int, office_bearers: List[Dict[str, Union[str, int]]], document_file: DocumentFiles) -> int:
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
            response = self._storeCorporateDataDomesticOfficeBearers(office_bearers, document_file)
            self.getLogger().inform(f"The data has been successfully updated into the Office Bearers table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {office_bearers}")
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def _storeCorporateDataDomesticOfficeBearers(self, office_bearers: List[Dict[str, Union[str, int]]], document_file: DocumentFiles) -> int:
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

    def storeCorporateDataDomesticStateCapital(self, status: int, state_capital: List[Dict[str, Union[str, int]]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation State Capital result set.

        Parameters:
            status: int: The status of the data manipulation.
            state_capital: [{type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}]: The data that has been extracted for the shareholder table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        if status >= 200 and status <= 299 and not state_capital:
            response = 200
            self.getLogger().inform(f"There is no data to be inserted into the State Capital table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {state_capital}")
        elif status >= 200 and status <= 299 and len(state_capital) > 0:
            response = self._storeCorporateDataDomesticStateCapital(state_capital, document_file.company_detail)
            self.getLogger().inform(f"The data has been successfully updated into the State Capital table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {state_capital}")
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def _storeCorporateDataDomesticStateCapital(self, state_capital: List[Dict[str, Union[str, int]]], company_detail: int) -> int:
        """
        Storing the state capital of the domestic companies.

        Parameters:
            state_capital: [{type: string, amount: int, currency: string, state_capital: int, amount_unpaid: int, par_value: int}]: The data that has been extracted for the shareholder table.
            company_detail: int: The identifier of the company.

        Returns:
            int
        """
        response: int
        responses: List[int] = []
        for index in range(0, len(state_capital), 1):
            responses.append(self.getStateCapital().addStateCapital(state_capital[index], company_detail))
        responses = list(set(responses))
        if len(responses) == 1 and responses[0] == 201:
            response = responses[0]
        else:
            response = responses[0]
        return response

    def storeCorporateDataDomesticPrivateBusinessDetail(self, company_detail: int, business_details: List[Dict[str, str]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on the Business Details result
        set.

        Parameters:
            company_detail: int: The status of the data manipulation.
            business_details: [{registered_address: string, name: string, nature: string, operational_address: string}]: The data that has been extracted for the business details table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        if company_detail == 202:
            response = self._storeCorporateDataDomesticPrivateBusinessDetail(business_details, document_file.company_detail)
            self.getLogger().inform(f"The data has been successfully updated into the Business Details table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {business_details}")
        else:
            response = company_detail
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {company_detail}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataDomesticCivilBusinessDetail(self, status: int, business_details: Dict[str, str], document_file: DocumentFiles) -> int:
        """
        Manipulating the data processed for the business details of
        a société civile or société commerciale.

        Parameters:
            status: int: The status of the previous operation.
            business_details: {registered_address: string}: The data that has been extracted for the business details table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        if status == 202:
            response = self.getBusinessDetails().addBusinessDetailsDomesticCivil(business_details, document_file.company_detail)
            self.getLogger().inform(f"The data has been successfully updated into the Business Details table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {business_details}")
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def _storeCorporateDataDomesticPrivateBusinessDetail(self, business_details: List[Dict[str, str]], company_detail: int) -> int:
        """
        Adding the business details into the relational database
        server.

        Parameters:
            business_details: [{registered_address: string, name: string, nature: string, operational_address: string}]: The data that has been extracted for the business details table.
            company_detail: int: The identifier of the company.

        Returns:
            int
        """
        response: int
        responses: List[int] = []
        for index in range(0, len(business_details), 1):
            responses.append(self.getBusinessDetails().addBusinessDetailsDomestic(business_details[index], company_detail))
        responses = list(set(responses))
        if len(responses) == 1 and responses[0] == 201:
            response = 201
            self.getLogger().inform(f"The data has been successfully updated into the Business Details table.\nStatus: {response}\nIdentifier: {company_detail}\nData: {business_details}")
        else:
            response = 503
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {response}\nCompany Detail Identifier: {company_detail}")
        return response

    def storeCorporateDataDomesticPrivateCompanyDetails(self, data_extraction: int, company_details: Dict[str, Union[str, int]], document_file: DocumentFiles) -> int:
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
            response = self.getCompanyDetails().updateCorporateMetadataDomesticPrivate(company_details, document_file.company_detail)
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
        status: int
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
        if amount != 0 and amount_found / amount >= 0.5:
            status = 200
        elif amount_found == 0:
            status = 429
        elif amount == 0:
            status = 404
        else:
            status = 409
        logs: Tuple[str, str, int, int, int, int, int] = ("downloadCorporateFile", quarter.quarter, int(datetime.strptime(date, "%Y-%m-%d").timestamp()), int(datetime.strptime(date, "%Y-%m-%d").timestamp()), status, amount, amount_found)
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
            date_to: str = datetime.strftime(datetime.strptime(quarter.start_date, "%m/%d/%Y") + timedelta(weeks=1), "%m/%d/%Y")
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
            date_end = logs[index].date_to if logs[index].date_to > date_end else date_end
        return datetime.strftime(datetime.strptime(datetime.fromtimestamp(date_end).strftime("%m/%d/%Y"), "%m/%d/%Y") + timedelta(days=1), "%m/%d/%Y")

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
            date_start = logs[index].date_start if logs[index].date_start < date_start else date_start
        return datetime.strftime(datetime.strptime(datetime.fromtimestamp(date_start).strftime("%m/%d/%Y"), "%m/%d/%Y") - timedelta(days=1), "%m/%d/%Y")

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
        date_end = datetime.strftime(datetime.strptime(date_start, "%m/%d/%Y") + timedelta(weeks=1), "%m/%d/%Y")
        date_end_unixtime: float = datetime.strptime(date_end, "%m/%d/%Y").timestamp()
        current_date: datetime = datetime.now() - timedelta(days=1)
        current_time: float = current_date.timestamp()
        if date_end_unixtime > current_time:
            date_end = self.getDateEnd(logs)
            date_start = datetime.strftime(datetime.strptime(date_end, "%m/%d/%Y") - timedelta(weeks=1), "%m/%d/%Y")
        return {
            "start_date": date_start,
            "end_date": date_end
        }

    def validateCorporateMetadata(self, response: Dict[str, int], request: Dict[str, str], quarter: FinancialCalendar) -> None:
        """
        Validating the response from the Crawler to save the data
        into the database server.

        Parameters:
            response: {status: int, amount: int}: The response from the crawler.
            request: {start_date: string, end_date: string}: The request for the crawler.
            quarter: FinancialCalendar

        Returns:
            void
        """
        method_name: str = "collectCorporateMetadata"
        date_start = int(datetime.strptime(str(request["start_date"]), "%m/%d/%Y").timestamp())
        date_end = int(datetime.strptime(str(request["end_date"]), "%m/%d/%Y").timestamp())
        parameters: Tuple[str, str, int, int, int, int, int] = (method_name, quarter.quarter, date_start, date_end, int(response["status"]), int(response["amount"]), len(self.getCrawler().getCorporateMetadata()))
        self.setData(self.getCrawler().getCorporateMetadata())
        self.getCrawler().getDriver().quit()
        self.getLogger().inform("Storing the corporate metadata!")
        self.storeCorporateMetadata()
        self.getFinCorpLogs().postSuccessfulCorporateDataCollectionRun(parameters)  # type: ignore

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

    def curateStateCapital(self) -> None:
        """
        Curating the data that is in the State Capital table.
        Santizing the type of the stated capital for a better
        filtering of the data.  Sanitizing the current of the stated
        capital for a better filtering and conversion of the data.

        Returns:
            void
        """
        quarter: FinancialCalendar = self.getFinancialCalendar().getCurrentQuarter()  # type: ignore
        current_time: int = int(time())
        self.setStateCapitalData(self.getStateCapital().get())
        self.curateStateCapitalType()
        self.curateStateCapitalCurrency()
        self.getStateCapitalData().sort(key=lambda stated_capital: stated_capital.identifier)
        response: int = self.updateCuratedStateCapital()
        log: Tuple[str, str, int, int, int, int, int] = ("curateStateCapital", quarter.quarter, current_time, current_time, response, len(self.getStateCapitalData()), len(self.getStateCapitalData()))
        self.getFinCorpLogs().postSuccessfulCorporateDataCollectionRun(log) # type: ignore

    def updateCuratedStateCapital(self) -> int:
        """
        Storing the curated stated capital data that are in the
        cache memory into the relational database server.

        Returns:
            int
        """
        good: int = 202
        bad: int = 503
        statuses: List[int] = list(set([self.getStateCapital().updateStatedCapital(stated_capital) for stated_capital in self.getStateCapitalData()]))
        return good if len(statuses) == 1 and statuses[0] == good else bad

    def curateStateCapitalCurrency(self) -> None:
        """
        Sanitizing the current of the stated capital for a better
        filtering and conversion of the data.

        Returns:
            void
        """
        self.curateStateCapitalCurrencyMur()
        self.curateStateCapitalCurrencyUsd()
        self.curateStateCapitalCurrencySd()

    def curateStateCapitalCurrencySd(self) -> None:
        """
        Filtering the data for the Singapore Dollar currency.

        Returns:
            void
        """
        singapore_dollar: List[StateCapital] = [stated_capital for stated_capital in self.getStateCapitalData() if stated_capital.currency != None and "singapore" in stated_capital.currency.lower()]
        filtered_data: List[StateCapital] = [stated_capital for stated_capital in self.getStateCapitalData() if stated_capital not in singapore_dollar]
        self.setStateCapitalData([])
        self.getLogger().inform(f"Stated Capital: Currency: Filtering the data for the Singapore Dollar currency.\nAmount: {len(singapore_dollar)}")
        for index in range(0, len(singapore_dollar), 1):
            singapore_dollar[index].currency = "Singapore Dollar"
        self.setStateCapitalData(singapore_dollar + filtered_data)

    def curateStateCapitalCurrencyUsd(self) -> None:
        """
        Filtering the data for the United States Dollar currency.

        Returns:
            void
        """
        united_states_dollar: List[StateCapital] = [stated_capital for stated_capital in self.getStateCapitalData() if stated_capital.currency != None and "us" in stated_capital.currency.lower()]
        filtered_data: List[StateCapital] = [stated_capital for stated_capital in self.getStateCapitalData() if stated_capital not in united_states_dollar]
        self.setStateCapitalData([])
        self.getLogger().inform(f"Stated Capital: Currency: Filtering the data for the United States Dollar currency.\nAmount: {len(united_states_dollar)}")
        for index in range(0, len(united_states_dollar), 1):
            united_states_dollar[index].currency = "United States Dollar"
        self.setStateCapitalData(united_states_dollar + filtered_data)

    def curateStateCapitalCurrencyMur(self) -> None:
        """
        Filtering the data for the Mauritian Rupee currency.

        Returns:
            void
        """
        mauritian_rupee: List[StateCapital] = [stated_capital for stated_capital in self.getStateCapitalData() if stated_capital.currency != None and ("mauritius" in stated_capital.currency.lower() or "rupee" in stated_capital.currency.lower())]
        filtered_data: List[StateCapital] = [stated_capital for stated_capital in self.getStateCapitalData() if stated_capital not in mauritian_rupee]
        self.setStateCapitalData([])
        self.getLogger().inform(f"Stated Capital: Currency: Filtering the data for the Mauritian Rupee currency.\nAmount: {len(mauritian_rupee)}")
        for index in range(0, len(mauritian_rupee), 1):
            mauritian_rupee[index].currency = "Mauritian Rupee"
        self.setStateCapitalData(mauritian_rupee + filtered_data)

    def curateStateCapitalType(self) -> None:
        """
        Santizing the type of the stated capital for a better
        filtering of the data.

        Returns:
            void
        """
        self.curateStateCapitalTypeOrdinary()
        self.curateStateCapitalTypeSociale()
        self.curateStateCapitalTypeD()
        self.curateStateCapitalTypeB()
        self.curateStateCapitalTypeA()
        self.curateStateCapitalTypeManagement()
        self.curateStateCapitalTypeC()
        self.curateStateCapitalTypeFounder()
        self.curateStateCapitalTypePreference()

    def curateStateCapitalTypePreference(self) -> None:
        """
        Filtering the data for the preference type.

        Returns:
            void
        """
        preference: List[StateCapital] = [stated_capital for stated_capital in self.getStateCapitalData() if stated_capital.type != None and ("preference" in stated_capital.type.lower())]
        filtered_data: List[StateCapital] = [stated_capital for stated_capital in self.getStateCapitalData() if stated_capital not in preference]
        self.setStateCapitalData([])
        self.getLogger().inform(f"Stated Capital: Type: Filtering the data for the Preference type.\nAmount: {len(preference)}")
        for index in range(0, len(preference), 1):
            preference[index].type = "Preference"
        self.setStateCapitalData(preference + filtered_data)

    def curateStateCapitalTypeFounder(self) -> None:
        """
        Filtering the data for the founder type.

        Returns:
            void
        """
        founder: List[StateCapital] = [stated_capital for stated_capital in self.getStateCapitalData() if stated_capital.type != None and ("founder" in stated_capital.type.lower())]
        filtered_data: List[StateCapital] = [stated_capital for stated_capital in self.getStateCapitalData() if stated_capital not in founder]
        self.setStateCapitalData([])
        self.getLogger().inform(f"Stated Capital: Type: Filtering the data for the Founder type.\nAmount: {len(founder)}")
        for index in range(0, len(founder), 1):
            founder[index].type = "Founder"
        self.setStateCapitalData(founder + filtered_data)

    def curateStateCapitalTypeC(self) -> None:
        """
        Filtering the data for the C type.

        Returns:
            void
        """
        c_type: List[StateCapital] = [stated_capital for stated_capital in self.getStateCapitalData() if stated_capital.type != None and ("class c" in stated_capital.type.lower())]
        filtered_data: List[StateCapital] = [stated_capital for stated_capital in self.getStateCapitalData() if stated_capital not in c_type]
        self.setStateCapitalData([])
        self.getLogger().inform(f"Stated Capital: Type: Filtering the data for the Class C type.\nAmount: {len(c_type)}")
        for index in range(0, len(c_type), 1):
            c_type[index].type = "Class C"
        self.setStateCapitalData(c_type + filtered_data)

    def curateStateCapitalTypeManagement(self) -> None:
        """
        Filtering the data for the management type.

        Returns:
            void
        """
        management: List[StateCapital] = [stated_capital for stated_capital in self.getStateCapitalData() if stated_capital.type != None and ("management" in stated_capital.type.lower())]
        filtered_data: List[StateCapital] = [stated_capital for stated_capital in self.getStateCapitalData() if stated_capital not in management]
        self.setStateCapitalData([])
        self.getLogger().inform(f"Stated Capital: Type: Filtering the data for the management type.\nAmount: {len(management)}")
        for index in range(0, len(management), 1):
            management[index].type = "Management"
        self.setStateCapitalData(management + filtered_data)

    def curateStateCapitalTypeA(self) -> None:
        """
        Filtering the data for the A type.

        Returns:
            void
        """
        class_a: List[StateCapital] = [stated_capital for stated_capital in self.getStateCapitalData() if stated_capital.type != None and ("class a" in stated_capital.type.lower())]
        filtered_data: List[StateCapital] = [stated_capital for stated_capital in self.getStateCapitalData() if stated_capital not in class_a]
        self.setStateCapitalData([])
        self.getLogger().inform(f"Stated Capital: Type: Filtering the data for the A type.\nAmount: {len(class_a)}")
        for index in range(0, len(class_a), 1):
            class_a[index].type = "Class A"
        self.setStateCapitalData(class_a + filtered_data)

    def curateStateCapitalTypeB(self) -> None:
        """
        Filtering the data for the B type.

        Returns:
            void
        """
        class_b: List[StateCapital] = [stated_capital for stated_capital in self.getStateCapitalData() if stated_capital.type != None and ("class b" in stated_capital.type.lower())]
        filtered_data: List[StateCapital] = [stated_capital for stated_capital in self.getStateCapitalData() if stated_capital not in class_b]
        self.setStateCapitalData([])
        self.getLogger().inform(f"Stated Capital: Type: Filtering the data for the B type.\nAmount: {len(class_b)}")
        for index in range(0, len(class_b), 1):
            class_b[index].type = "Class B"
        self.setStateCapitalData(class_b + filtered_data)

    def curateStateCapitalTypeD(self) -> None:
        """
        Filtering the data for the D type.

        Returns:
            void
        """
        class_d: List[StateCapital] = [stated_capital for stated_capital in self.getStateCapitalData() if stated_capital.type != None and ("class d" in stated_capital.type.lower())]
        filtered_data: List[StateCapital] = [stated_capital for stated_capital in self.getStateCapitalData() if stated_capital not in class_d]
        self.setStateCapitalData([])
        self.getLogger().inform(f"Stated Capital: Type: Filtering the data for the D type.\nAmount: {len(class_d)}")
        for index in range(0, len(class_d), 1):
            class_d[index].type = "Class D"
        self.setStateCapitalData(class_d + filtered_data)

    def curateStateCapitalTypeSociale(self) -> None:
        """
        Filtering the data for the sociale type.

        Returns:
            void
        """
        sociale: List[StateCapital] = [stated_capital for stated_capital in self.getStateCapitalData() if stated_capital.type != None and ("social" in stated_capital.type.lower() or "interet" in stated_capital.type.lower())]
        filtered_data: List[StateCapital] = [stated_capital for stated_capital in self.getStateCapitalData() if stated_capital not in sociale]
        self.setStateCapitalData([])
        self.getLogger().inform(f"Stated Capital: Type: Filtering the data for the sociale type.\nAmount: {len(sociale)}")
        for index in range(0, len(sociale), 1):
            sociale[index].type = "Part Sociale"
        self.setStateCapitalData(sociale + filtered_data)

    def curateStateCapitalTypeOrdinary(self) -> None:
        """
        Filtering the data for the ordinary type.

        Returns:
            void
        """
        ordinary: List[StateCapital] = [stated_capital for stated_capital in self.getStateCapitalData() if stated_capital.type != None and "ordinary" in stated_capital.type.lower() and "class" not in stated_capital.type.lower()]
        filtered_data: List[StateCapital] = [stated_capital for stated_capital in self.getStateCapitalData() if stated_capital not in ordinary]
        self.setStateCapitalData([])
        self.getLogger().inform(f"Stated Capital: Type: Filtering the data for the ordinary type.\nAmount: {len(ordinary)}")
        for index in range(0, len(ordinary), 1):
            ordinary[index].type = "Ordinary"
        self.setStateCapitalData(ordinary + filtered_data)

    def curateBusinessDetails(self) -> None:
        """
        Curating the data that is in the Business Details table. The
        registered addresses have to be sanitized for the
        geographical information system to be able to process it
        afterwards.  The names have to be sanitized to reflect the
        companies they are affliated with.  The natures have to be
        sanitized to be processed afterwards to obtain the sector of
        activity of the company by doing a sentiment analysis.  The
        operational addresses have to be sanitized for the
        geographical information system to be able to process it
        afterwards.

        Returns:
            void
        """
        quarter: FinancialCalendar = self.getFinancialCalendar().getCurrentQuarter()  # type: ignore
        current_time: int = int(time())
        self.setBusinessDetailsData(self.getBusinessDetails().getBusinessDetails())
        self.setCompanyDetailsData([self.getCompanyDetails().getSpecificCompanyDetails(identifier) for identifier in list(set([business_detail.CompanyDetail for business_detail in self.getBusinessDetailsData()]))])
        self.sanitizeBusinessDetailsRegisteredAddresses()
        self.sanitizeBusinessDetailsName()
        self.sanitizeBusinessDetailsNature()
        self.sanitizeBusinessDetailOperationalAddress()
        response: int = self.updateCuratedBusinessDetails()
        log: Tuple[str, str, int, int, int, int, int] = ("curateBusinessDetails", quarter.quarter, current_time, current_time, response, len(self.getBusinessDetailsData()), len(self.getBusinessDetailsData()))
        self.getFinCorpLogs().postSuccessfulCorporateDataCollectionRun(log) # type: ignore

    def updateCuratedBusinessDetails(self) -> int:
        """
        Storing the curated business details data that are in the
        cache memory into the relational database server.

        Returns:
            int
        """
        good: int = 202
        bad: int = 503
        statuses: List[int] = list(set([self.getBusinessDetails().updateBusinessDetail(business_detail) for business_detail in self.getBusinessDetailsData()]))
        return good if len(statuses) == 1 and statuses[0] == good else bad

    def sanitizeBusinessDetailsRegisteredAddresses(self) -> None:
        """
        Sanitizing the registered addresses which are going to be
        used by the geographical information system to be able to
        process it afterwards.

        Returns:
            void
        """
        self.sanitizeBusinessDetailsRegisteredAddressesFormat()
        self.sanitizeBusinessDetailsRegisteredAddressesErroneous()
        self.santizeBusinessDetailsRegisteredAddressesFormatting()

    def santizeBusinessDetailsRegisteredAddressesFormatting(self) -> None:
        """
        Sanitizing and standardizing the formatting of registered addresses in business details.

        This method processes a list of business details, modifying the registered addresses to ensure a consistent format. It applies various replacements, such as removing or substituting specific substrings, capitalizing words, and correcting abbreviations.

        The function logs the number of business details being processed before applying transformations.  The replacements list contains tuples defining:
            - `current_value`: The substring to be replaced.
            - `new_value`: The replacement string.
            - `is_start`: A boolean indicating whether the replacement should apply only if `current_value` appears at the beginning of the address.

        Returns:
            None
        """
        replacements: List[Tuple[str, str, bool]] = [("-", "", True), (", ", "", True), (". ", "", True), ("(B) ", "", True), ("(", "", True), ("& ", "", True), (" morc ", " Morcellement ", False), (" st,", " Street, ", False), (" rd, ", " Road, ", False), (" ave ", " Avenue ", False), (" ste ", " Sainte ", False), ("apps ", "Appartment ", False), ("appt ", "Appartment ", False), ("apt ", "Appartment ", False), ("blk ", "Block ", False), (" rt ", " Route ", False), (" rd ", " Road, ", False), (" ave, ", " Avenue ", False), (" mt ", " Montagne ", False), (" - ", " ", False), (" se ", " Sugar Estate ", False), ("blvd", "Boulevard ", True), ("grnw ", "Grand River North West, ", False), ("govt ", "Government ", False), ("imp ", "Impasse ", False), ("morc ", "Morcellement ", False), ("morc.", "Morcellement ", False), ("mont", "Montagne ", False), ("pte ", "Pointe ", False)]
        business_details: List[BusinessDetails] = []
        self.getLogger().inform(f"Business Details: Registered Address: Formatting the registered addresses into the correct format for processing.\nAmount: {len(self.getBusinessDetailsData())}")
        for business_detail in self.getBusinessDetailsData():
            business_details = self.__businessDetailsRegisteredAddressesFormat(business_details, replacements, business_detail)
        self.setBusinessDetailsData(business_details)

    def __businessDetailsRegisteredAddressesFormat(self, processeds: List[BusinessDetails], replacements: List[Tuple[str, str, bool]], business_detail: BusinessDetails) -> List[BusinessDetails]:
        """
        Applying formatting corrections to a business's registered address.

        This method modifies the `registered_address` of a given `BusinessDetails` object based on a list of replacement rules and appends the processed object to a list.

        Parameters:
            processeds (List[BusinessDetails]): A list to store processed business details.
            replacements (List[Tuple[str, str, bool]]): A list of tuples where:
                - `current` (str): The substring to replace.
                - `new` (str): The replacement string.
                - `is_start` (bool): If True, the replacement applies only if `current` appears at the beginning of the address.
            business_detail (BusinessDetails): The business detail object to be formatted.

        Returns:
            List[BusinessDetails]: The updated list of processed business details.
        """
        registered_address: Union[str, None] = business_detail.registered_address
        if not registered_address:
            processeds.append(business_detail)
            return processeds
        for current, new, is_start in replacements:
            registered_address = self.__businessDetailsRegisteredAddressesFormatCorrectValue(current, new, is_start, registered_address)
        business_detail.registered_address = registered_address
        processeds.append(business_detail)
        return processeds

    def __businessDetailsRegisteredAddressesFormatCorrectValue(self, current_needle: str, new_needle: str, is_start: bool, registered_address: str) -> str:
        """
        Applying a specific formatting correction to a registered address.

        This method checks whether a given substring (`current_needle`) is present in the `registered_address` and replaces it with `new_needle` based on the specified conditions.

        Parameters:
            current_needle (str): The substring to be replaced.
            new_needle (str): The replacement string.
            is_start (bool): If True, the replacement is applied only if `current_needle` appears at the beginning of `registered_address`.
            registered_address (str): The address string to be formatted.

        Returns:
            str
        """
        if is_start and registered_address.startswith(current_needle):
            return registered_address.replace(current_needle, new_needle, 1)
        if not is_start and current_needle in registered_address.lower():
            return registered_address.replace(current_needle, new_needle)
        return registered_address

    def sanitizeBusinessDetailsRegisteredAddressesFormat(self)-> None:
        """
        Formating the registered addresses into the correct format
        for processing.

        Returns:
            void
        """
        business_details: List[BusinessDetails] = []
        self.getLogger().inform(f"Business Details: Registered Address: Formating the registered addresses into the correct format for processing.\nAmount: {len(self.getBusinessDetailsData())}")
        for index in range(0, len(self.getBusinessDetailsData()), 1):
            business_detail: BusinessDetails = self.getBusinessDetailsData()[index]
            registered_address: Union[str, None] = " ".join([address for address in business_detail.registered_address.split(" ") if address != ""]).title() if business_detail.registered_address != None else business_detail.registered_address
            business_detail.registered_address = registered_address
            business_details.append(business_detail)
        self.setBusinessDetailsData(business_details)

    def sanitizeBusinessDetailOperationalAddress(self) -> None:
        """
        Sanitizing the operational addresses which are going to be
        used by the geographical information system to be able to
        process it afterwards.

        Returns:
            void
        """
        self.sanitizeBusinessDetailOperationalAddressFormat()
        self.sanitizeBusinessDetailOperationalAddressMissingAddress()
        self.sanitizeBusinessDetailOperationalAddressTruncatedAddress()

    def sanitizeBusinessDetailOperationalAddressTruncatedAddress(self) -> None:
        """
        Setting the data of the operational address to be the one of
        the registered for the ones that have truncated data.

        Returns:
            void
        """
        truncated_data: List[BusinessDetails] = [business_details for business_details in self.getBusinessDetailsData() if business_details.operational_address != None and business_details.registered_address != None and business_details.operational_address in business_details.registered_address]
        filtered_business_details: List[BusinessDetails] = [business_details for business_details in self.getBusinessDetailsData()if business_details not in truncated_data]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Operational Address: Setting the data of the operational address to be the one of the registered for the ones that have truncated data.\nAmount: {len(truncated_data)}")
        for index in range(0, len(truncated_data), 1):
            truncated_data[index].operational_address = truncated_data[index].registered_address
        self.setBusinessDetailsData(truncated_data + filtered_business_details)

    def sanitizeBusinessDetailOperationalAddressMissingAddress(self) -> None:
        """
        Setting the data operational address to be the one of the
        registered address for the ones missing data.

        Returns:
            void
        """
        missing_addresses: List[BusinessDetails] = [business_details for business_details in self.getBusinessDetailsData() if business_details.operational_address == "Mauritius" or business_details.operational_address == "() Mauritius" or business_details.operational_address == "Mauritius Mauritius"]
        filtered_business_details: List[BusinessDetails] = [business_details for business_details in self.getBusinessDetailsData()if business_details not in missing_addresses]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Operational Address: Setting the data operational address to be the one of the registered address for the ones missing data.\nAmount: {len(missing_addresses)}")
        for index in range(0, len(missing_addresses), 1):
            missing_addresses[index].operational_address = missing_addresses[index].registered_address
        self.setBusinessDetailsData(missing_addresses + filtered_business_details)

    def sanitizeBusinessDetailOperationalAddressFormat(self) -> None:
        """
        Formating the operational addresses into the correct format
        for processing.

        Returns:
            void
        """
        business_details: List[BusinessDetails] = []
        self.getLogger().inform(f"Business Details: Operational Address: Formating the operational addresses into the correct format for processing.\nAmount: {len(self.getBusinessDetailsData())}")
        for index in range(0, len(self.getBusinessDetailsData()), 1):
            business_detail: BusinessDetails = self.getBusinessDetailsData()[index]
            operational_address: Union[str, None] = " ".join([address for address in business_detail.operational_address.split(" ") if address != ""]).title() if business_detail.operational_address != None else business_detail.operational_address
            business_detail.operational_address = operational_address
            business_details.append(business_detail)
        self.setBusinessDetailsData(business_details)

    def sanitizeBusinessDetailsRegisteredAddressesErroneous(self) -> None:
        """
        Sanitizing the registered addresses that are going to be
        used by the geographical information system to be able to
        process it afterwards.

        Returns:
            void
        """
        erroneous_registered_addresses: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.registered_address != None and bool(search(r"\d", business_detail.registered_address)) == True]
        self.getLogger().inform(f"Business Details: Registered Address: Sanitizing the registered addresses that are going to be used by the geographical information system to be able to process it afterwards.\nAmount: {len(erroneous_registered_addresses)}")
        filtered_business_details: List[BusinessDetails] = [business_details for business_details in self.getBusinessDetailsData()if business_details not in erroneous_registered_addresses]
        self.setBusinessDetailsData([])
        for index in range(0, len(erroneous_registered_addresses), 1):
            registered_addresses: List[str] = erroneous_registered_addresses[index].registered_address.split(" ") # type: ignore
            registered_addresses = [address for address in registered_addresses if address != ""]
            registered_addresses = [address for address in registered_addresses if bool(search(r"\d", address)) == False]
            registered_addresses = [address for address in registered_addresses if address != "No"]
            registered_addresses = [address for address in registered_addresses if address != "No."]
            registered_addresses = [address for address in registered_addresses if address != "Floor"]
            registered_addresses = [address for address in registered_addresses if address != "Lot"]
            registered_addresses = [address for address in registered_addresses if address != "Plot"]
            registered_addresses = [address for address in registered_addresses if address != "Suite"]
            registered_addresses = [address for address in registered_addresses if address != "Level"]
            registered_addresses = [address for address in registered_addresses if address != "Effective"]
            registered_addresses = [address for address in registered_addresses if address != "Date"]
            registered_addresses = [address for address in registered_addresses if address != "For"]
            registered_addresses = [address for address in registered_addresses if address != "Registered"]
            registered_addresses = [address for address in registered_addresses if address != "Office"]
            registered_addresses = [address for address in registered_addresses if address != "Address:"]
            registered_addresses = [address for address in registered_addresses if address != "(Ex"]
            registered_addresses = [address for address in registered_addresses if address != "Office"]
            registered_addresses = [address for address in registered_addresses if address != "Gds"]
            registered_addresses = [address for address in registered_addresses if address != "-"]
            registered_addresses = [address for address in registered_addresses if address != "Apt."]
            registered_addresses = [address for address in registered_addresses if address != "Hse"]
            registered_addresses = [address.capitalize() for address in registered_addresses]
            registered_address: str = " ".join(registered_addresses)
            erroneous_registered_addresses[index].registered_address = registered_address
        self.setBusinessDetailsData(filtered_business_details + erroneous_registered_addresses)

    def sanitizeBusinessDetailsNameSameNames(self) -> None:
        """
        Replacing placeholder business names with their corresponding company names.

        This method processes business details where the `name` field contains placeholder values such as `"."` or `"-"`. It replaces these placeholders with the actual company names retrieved from `CompanyDetails`.

        Returns:
            None
        """
        names: List[str] = [".", "-"]
        same_names: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.name in names]
        filtered_business_data: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail not in same_names]
        self.getLogger().inform(f"Business Details: Name: The names are being sanitized where '.' will be replaced by their company names.\nAmount: {len(same_names)}")
        for business_detail in same_names:
            company_detail: CompanyDetails = [company_detail for company_detail in self.getCompanyDetailsData() if company_detail.identifier == business_detail.CompanyDetail][0]
            business_detail.name = company_detail.name.title()
        self.setBusinessDetailsData(same_names + filtered_business_data)

    def sanitizeBusinessDetailsNameCountriesNames(self) -> None:
        """
        Sanitizing the names where the country names are in the
        business names.

        Returns:
            void
        """
        countries_names: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.name != None and "MAURITIUS" in business_detail.name.upper()]
        filtered_business_data: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail not in countries_names]
        self.getLogger().inform(f"Business Details: Name: The names are being sanitized where the values which are the country names will be replaced by their company names.\nAmount: {len(countries_names)}")
        self.setBusinessDetailsData([])
        for index in range(0, len(countries_names), 1):
            company_detail: CompanyDetails = [company_detail for company_detail in self.getCompanyDetailsData() if company_detail.identifier == countries_names[index].CompanyDetail][0]
            countries_names[index].name = company_detail.name.title()
        self.setBusinessDetailsData(countries_names + filtered_business_data)

    def sanitizeBusinessDetailsNameNoNameDomesticCompanies(self) -> None:
        """
        Sanitizing the names where there is no name for the domestic
        companies.

        Returns:
            void
        """
        no_name_domestic_companies: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.name == None and business_detail.operational_address != None]
        filtered_business_data: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail not in no_name_domestic_companies]
        self.getLogger().inform(f"Business Details: Name: The names are being sanitized where there is no business name given that they are domestic companies which are the country names will be replaced by their company names.\nAmount: {len(no_name_domestic_companies)}")
        self.setBusinessDetailsData([])
        for index in range(0, len(no_name_domestic_companies), 1):
            company_detail: CompanyDetails = [company_detail for company_detail in self.getCompanyDetailsData() if company_detail.identifier == no_name_domestic_companies[index].CompanyDetail][0]
            no_name_domestic_companies[index].name = company_detail.name.title()
        self.setBusinessDetailsData(no_name_domestic_companies + filtered_business_data)

    def sanitizeBusinessDetailsNameAddressesAsNames(self) -> None:
        """
        Sanitizing the names where there is the addresses in the
        name.

        Returns:
            void
        """
        addresses_as_names: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.name != None and "road" in business_detail.name.lower()]
        filtered_business_data: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail not in addresses_as_names]
        self.getLogger().inform(f"Business Details: Name: The names are being sanitized where they are the addresses in the names which are the country names will be replaced by their company names.\nAmount: {len(addresses_as_names)}")
        self.setBusinessDetailsData([])
        for index in range(0, len(addresses_as_names), 1):
            company_detail: CompanyDetails = [company_detail for company_detail in self.getCompanyDetailsData() if company_detail.identifier == addresses_as_names[index].CompanyDetail][0]
            addresses_as_names[index].name = company_detail.name.title()
        self.setBusinessDetailsData(addresses_as_names + filtered_business_data)

    def sanitizeBusinessDetailsNameNamesAsNatures(self) -> None:
        """
        Sanitizing the names where they are the natures.

        Returns:
            void
        """
        names_as_natures: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.name != None and business_detail.name == business_detail.nature]
        filtered_business_data: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail not in names_as_natures]
        self.getLogger().inform(f"Business Details: Name: The names are being sanitized where the business name are the business natures which are the country names will be replaced by their company names.\nAmount: {len(names_as_natures)}")
        self.setBusinessDetailsData([])
        for index in range(0, len(names_as_natures), 1):
            company_detail: CompanyDetails = [company_detail for company_detail in self.getCompanyDetailsData() if company_detail.identifier == names_as_natures[index].CompanyDetail][0]
            names_as_natures[index].name = company_detail.name.title()
        self.setBusinessDetailsData(names_as_natures + filtered_business_data)

    def sanitizeBusinessDetailsName(self) -> None:
        """
        Sanitizing the names to reflect the companies they are
        affliated with.

        Returns:
            void
        """
        self.sanitizeBusinessDetailsNameSameNames()
        self.sanitizeBusinessDetailsNameCountriesNames()
        self.sanitizeBusinessDetailsNameNoNameDomesticCompanies()
        self.sanitizeBusinessDetailsNameAddressesAsNames()
        self.sanitizeBusinessDetailsNameNamesAsNatures()
        self.sanitizeBusinessDetailsNameFormat()

    def sanitizeBusinessDetailsNameFormat(self) -> None:
        """
        Sanitizing and standardizing the formatting of business names.

        This method processes a list of business details, ensuring that business names follow proper capitalization and format rules. It converts names to title case and standardizes specific abbreviations.  The function logs the number of business details being processed before making modifications.

        Returns:
            None
        """
        business_details: List[BusinessDetails] = []
        self.getLogger().inform(f"Business Details: Name: The names are being sanitized where the correct values are to be applied.\nAmount: {len(self.getBusinessDetailsData())}")
        for business_detail in self.getBusinessDetailsData():
            if business_detail.name:
                name: str = business_detail.name.title()
                name = name.replace(" Ltd", " LTD")
                business_detail.name = name
            business_details.append(business_detail)
        self.setBusinessDetailsData(business_details)

    def sanitizeBusinessDetailsNature(self) -> None:
        """
        The natures have to be sanitized to be processed afterwards
        to obtain the sector of activity of the company by doing a
        sentiment analysis.

        Returns:
            void
        """
        self.sanitizeBusinessDetailsNatureSameAsName()
        self.sanitizeBusinessDetailsNatureJobContractors()
        self.sanitizeBusinessDetailsNatureNotElsewhereClassified()
        self.sanitizeBusinessDetailsNatureOtherProfessionalScientificTechnicalActivities()
        self.sanitizeBusinessDetailsNatureFirms()
        self.sanitizeBusinessDetailsNatureGeneralRetailers()
        self.sanitizeBusinessDetailsNatureWholesalers()
        self.sanitizeBusinessDetailsNatureHeadOffices()
        self.sanitizeBusinessDetailsNatureWebPortals()
        self.sanitizeBusinessDetailsNatureRestaurants()
        self.sanitizeBusinessDetailsNatureInvestmentCompanies()
        self.sanitizeBusinessDetailsNatureRealEstate()
        self.sanitizeBusinessDetailsNatureManagementCompanies()
        self.sanitizeBusinessDetailsNatureOtherBusinessSupportActivites()
        self.sanitizeBusinessDetailsNatureFreightTransportation()
        self.sanitizeBusinessDetailsNatureMotorVehicleRental()
        self.sanitizeBusinessDetailsNatureRentingOfPassengerCar()
        self.sanitizeBusinessDetailsNaturePrePrimaryEducation()
        self.sanitizeBusinessDetailsNatureFrozenProductsRetailers()
        self.sanitizeBusinessDetailsNatureOtherTourismReservationActivities()
        self.sanitizeBusinessDetailsNatureClothingRetailers()
        self.sanitizeBusinessDetailsNatureHardwareRetailers()
        self.sanitizeBusinessDetailsNatureBreadManufacturers()
        self.sanitizeBusinessDetailsNatureRepairElectricalEquipment()
        self.sanitizeBusinessDetailsNaturePhotoAndVideoEditing()
        self.sanitizeBusinessDetailsNatureResidentialNursingCareActivities()
        self.sanitizeBusinessDetailsNatureConstructionOfBuildings()
        self.sanitizeBusinessDetailsNatureDevelopmentOfBuildings()
        self.sanitizeBusinessDetailsNaturePlantingAndEstablishingOfCrops()
        self.sanitizeBusinessDetailsNaturePackagingActivities()
        self.sanitizeBusinessDetailsNatureEventCatering()

    def sanitizeBusinessDetailsNatureEventCatering(self) -> None:
        """
        Sanitizing the nature where they are classified as event
        catering.

        Returns:
            void
        """
        event_catering: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and "event catering" in business_detail.nature.lower()]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in event_catering]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where they are classified as event catering.\nAmount: {len(event_catering)}")
        for index in range(0, len(event_catering), 1):
            event_catering[index].nature = "Event Catering"
        self.setBusinessDetailsData(event_catering + filtered_business_details)

    def sanitizeBusinessDetailsNaturePackagingActivities(self) -> None:
        """
        Sanitizing the nature where they are classified as packaging
        activities.

        Returns:
            void
        """
        packaging_activities: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and "packaging" in business_detail.nature.lower()]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in packaging_activities]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where they are classified as packaging activities.\nAmount: {len(packaging_activities)}")
        for index in range(0, len(packaging_activities), 1):
            packaging_activities[index].nature = "Packaging Activities"
        self.setBusinessDetailsData(packaging_activities + filtered_business_details)

    def sanitizeBusinessDetailsNaturePlantingAndEstablishingOfCrops(self) -> None:
        """
        Sanitizing the nature where they are classified as
        planting and establishing crops.

        Returns:
            void
        """
        planting_and_establishing_of_crops: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and ("planting" in business_detail.nature.lower() and "crops" in business_detail.nature.lower())]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in planting_and_establishing_of_crops]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where they are classified as planting and establishing crops.\nAmount: {len(planting_and_establishing_of_crops)}")
        for index in range(0, len(planting_and_establishing_of_crops), 1):
            planting_and_establishing_of_crops[index].nature = "Planting And Establishing Of Crops"
        self.setBusinessDetailsData(planting_and_establishing_of_crops + filtered_business_details)

    def sanitizeBusinessDetailsNatureDevelopmentOfBuildings(self) -> None:
        """
        Sanitizing the nature where they are classified as
        development of buildings.

        Returns:
            void
        """
        development_of_buildings: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and ("development" in business_detail.nature.lower() and "building" in business_detail.nature.lower())]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in development_of_buildings]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where they are classified as development of buildings.\nAmount: {len(development_of_buildings)}")
        for index in range(0, len(development_of_buildings), 1):
            development_of_buildings[index].nature = "Construction Of Buildings"
        self.setBusinessDetailsData(development_of_buildings + filtered_business_details)

    def sanitizeBusinessDetailsNatureConstructionOfBuildings(self) -> None:
        """
        Sanitizing the nature where they are classified as
        construction of buildings.

        Returns:
            void
        """
        construction_of_buildings: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and ("construction" in business_detail.nature.lower() and "building" in business_detail.nature.lower())]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in construction_of_buildings]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where they are classified as construction of buildings.\nAmount: {len(construction_of_buildings)}")
        for index in range(0, len(construction_of_buildings), 1):
            construction_of_buildings[index].nature = "Construction Of Buildings"
        self.setBusinessDetailsData(construction_of_buildings + filtered_business_details)

    def sanitizeBusinessDetailsNatureResidentialNursingCareActivities(self) -> None:
        """
        Sanitizing the nature where they are classified as
        residential nursing care activities.

        Returns:
            void
        """
        residential_nursing_care_activities: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and ("Residential" in business_detail.nature and "Nursing" in business_detail.nature)]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in residential_nursing_care_activities]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where they are classified as residential nursing care activities.\nAmount: {len(residential_nursing_care_activities)}")
        for index in range(0, len(residential_nursing_care_activities), 1):
            residential_nursing_care_activities[index].nature = "Residential Nursing Care Activities"
        self.setBusinessDetailsData(residential_nursing_care_activities + filtered_business_details)

    def sanitizeBusinessDetailsNaturePhotoAndVideoEditing(self) -> None:
        """
        Sanitizing the nature where they are photographers.

        Returns:
            void
        """
        content_creators: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and "Photograph" in business_detail.nature]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in content_creators]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where they are photographers.\nAmount: {len(content_creators)}")
        for index in range(0, len(content_creators), 1):
            content_creators[index].nature = "Photo And Video Editing"
        self.setBusinessDetailsData(content_creators + filtered_business_details)

    def sanitizeBusinessDetailsNatureRepairElectricalEquipment(self) -> None:
        """
        Sanitizing the nature where they are repairers of electrical
        equipment.

        Returns:
            void
        """
        electrical_repairers: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and ("Repair" in business_detail.nature and "Electrical" in business_detail.nature and "Equipment" in business_detail.nature)]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in electrical_repairers]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where they are repairers of electrical equipment.\nAmount: {len(electrical_repairers)}")
        for index in range(0, len(electrical_repairers), 1):
            electrical_repairers[index].nature = "Repair Of Electrical Equipment"
        self.setBusinessDetailsData(electrical_repairers + filtered_business_details)

    def sanitizeBusinessDetailsNatureBreadManufacturers(self) -> None:
        """
        Sanitizing the nature where they are bread manufacturers.

        Returns:
            void
        """
        bread_manufacturers: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and ("Manufacture" in business_detail.nature and "Bread" in business_detail.nature)]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in bread_manufacturers]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where they are bread manufacturers.\nAmount: {len(bread_manufacturers)}")
        for index in range(0, len(bread_manufacturers), 1):
            bread_manufacturers[index].nature = "Manufacture Of Bread"
        self.setBusinessDetailsData(bread_manufacturers + filtered_business_details)

    def sanitizeBusinessDetailsNatureHardwareRetailers(self) -> None:
        """
        Sanitizing the nature where they are hardware retailers.

        Returns:
            void
        """
        hardware_retailers: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and ("Retail" in business_detail.nature and "Hardware" in business_detail.nature)]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in hardware_retailers]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where they are hardware retailers.\nAmount: {len(hardware_retailers)}")
        for index in range(0, len(hardware_retailers), 1):
            hardware_retailers[index].nature = "Retail Sale Of Hardware"
        self.setBusinessDetailsData(hardware_retailers + filtered_business_details)

    def sanitizeBusinessDetailsNatureClothingRetailers(self) -> None:
        """
        Sanitizing the nature where they are clothing retailers.

        Returns:
            void
        """
        clothing_retailers: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and ("retail" in business_detail.nature.lower() and "clothing" in business_detail.nature.lower())]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in clothing_retailers]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where they are clothing retailers.\nAmount: {len(clothing_retailers)}")
        for index in range(0, len(clothing_retailers), 1):
            clothing_retailers[index].nature = "Retail Sale Of Clothing"
        self.setBusinessDetailsData(clothing_retailers + filtered_business_details)

    def sanitizeBusinessDetailsNatureOtherTourismReservationActivities(self) -> None:
        """
        Sanitizing the nature where they are clasified as other
        tourism reservation activities.

        Returns:
            void
        """
        other_tourism_reservation_activities: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and ("Other" in business_detail.nature and "Tourism" in business_detail.nature)]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in other_tourism_reservation_activities]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where they are clasified as other tourism reservation activities.\nAmount: {len(other_tourism_reservation_activities)}")
        for index in range(0, len(other_tourism_reservation_activities), 1):
            other_tourism_reservation_activities[index].nature = "Other Tourism Reservation Services"
        self.setBusinessDetailsData(other_tourism_reservation_activities + filtered_business_details)

    def sanitizeBusinessDetailsNatureFrozenProductsRetailers(self) -> None:
        """
        Sanitizing the nature where they are frozen products
        retailers.

        Returns:
            void
        """
        frozen_product_retailers: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and ("Retail" in business_detail.nature and "Poultry" in business_detail.nature)]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in frozen_product_retailers]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where they are frozen products retailers.\nAmount: {len(frozen_product_retailers)}")
        for index in range(0, len(frozen_product_retailers), 1):
            frozen_product_retailers[index].nature = "Retail Sale of Frozen Products"
        self.setBusinessDetailsData(frozen_product_retailers + filtered_business_details)

    def sanitizeBusinessDetailsNaturePrePrimaryEducation(self) -> None:
        """
        Sanitizing the nature where they are pre-primary schools.

        Returns:
            void
        """
        pre_primary_school: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and ("Pre" in business_detail.nature and "Primary" in business_detail.nature)]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in pre_primary_school]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where they are pre-primary schools.\nAmount: {len(pre_primary_school)}")
        for index in range(0, len(pre_primary_school), 1):
            pre_primary_school[index].nature = "Pre-Primary Education"
        self.setBusinessDetailsData(pre_primary_school + filtered_business_details)

    def sanitizeBusinessDetailsNatureRentingOfPassengerCar(self) -> None:
        """
        Sanitizing the nature where they are motor vehicles rental
        companies.

        Returns:
            void
        """
        motor_vehicle_rentals: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and ("Renting" in business_detail.nature and "Car" in business_detail.nature)]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in motor_vehicle_rentals]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where they are motor vehicles rental companies.\nAmount: {len(motor_vehicle_rentals)}")
        for index in range(0, len(motor_vehicle_rentals), 1):
            motor_vehicle_rentals[index].nature = "Motor Vehicles Rental"
        self.setBusinessDetailsData(motor_vehicle_rentals + filtered_business_details)

    def sanitizeBusinessDetailsNatureMotorVehicleRental(self) -> None:
        """
        Sanitizing the nature where they are motor vehicles rental
        companies.

        Returns:
            void
        """
        motor_vehicle_rentals: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and ("Contractor" in business_detail.nature and "Motor" in business_detail.nature)]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in motor_vehicle_rentals]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where they are motor vehicles rental companies.\nAmount: {len(motor_vehicle_rentals)}")
        for index in range(0, len(motor_vehicle_rentals), 1):
            motor_vehicle_rentals[index].nature = "Motor Vehicles Rental"
        self.setBusinessDetailsData(motor_vehicle_rentals + filtered_business_details)

    def sanitizeBusinessDetailsNatureFreightTransportation(self) -> None:
        """
        Sanitizing the nature where they are freight transportation
        companies.

        Returns:
            void
        """
        freight_transportations: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and "Freight Transport" in business_detail.nature]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in freight_transportations]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where they are freight transportation companies.\nAmount: {len(freight_transportations)}")
        for index in range(0, len(freight_transportations), 1):
            freight_transportations[index].nature = "Freight Transport"
        self.setBusinessDetailsData(freight_transportations + filtered_business_details)

    def sanitizeBusinessDetailsNatureOtherBusinessSupportActivites(self) -> None:
        """
        Sanitizing the nature where they are classified as Other
        Business Support Activities.

        Returns:
            void
        """
        other_business_support_activities: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and "Other Business Support Service Activities" in business_detail.nature]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in other_business_support_activities]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where they are classified as Other Business Support Activities.\nAmount: {len(other_business_support_activities)}")
        for index in range(0, len(other_business_support_activities), 1):
            other_business_support_activities[index].nature = "Other Business Support Service Activities"
        self.setBusinessDetailsData(other_business_support_activities + filtered_business_details)

    def sanitizeBusinessDetailsNatureManagementCompanies(self) -> None:
        """
        Sanitizing the nature where they are management companies.

        Returns:
            void
        """
        management_companies: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and "Holding" in business_detail.nature]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in management_companies]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where they are management companies.\nAmount: {len(management_companies)}")
        for index in range(0, len(management_companies), 1):
            management_companies[index].nature = "Management Companies"
        self.setBusinessDetailsData(management_companies + filtered_business_details)

    def sanitizeBusinessDetailsNatureRealEstate(self) -> None:
        """
        Sanitizing the nature where they are real estate.

        Returns:
            void
        """
        real_estate: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and "real estate" in business_detail.nature.lower()]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in real_estate]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where they are real estate.\nAmount: {len(real_estate)}")
        for index in range(0, len(real_estate), 1):
            real_estate[index].nature = "Real Estate Activities"
        self.setBusinessDetailsData(real_estate + filtered_business_details)

    def sanitizeBusinessDetailsNatureInvestmentCompanies(self) -> None:
        """
        Sanitizing the nature where they are investment companies.

        Returns:
            void
        """
        investment_companies: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and ("investment" in business_detail.nature.lower() and "companies" in business_detail.nature.lower())]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in investment_companies]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where they are investment companies.\nAmount: {len(investment_companies)}")
        for index in range(0, len(investment_companies), 1):
            investment_companies[index].nature = "Investment Companies"
        self.setBusinessDetailsData(investment_companies + filtered_business_details)

    def sanitizeBusinessDetailsNatureRestaurants(self) -> None:
        """
        Sanitizing the nature where they are restaurants.

        Returns:
            void
        """
        restaurants: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and ("Restaurants" in business_detail.nature or "Restaurant" in business_detail.nature)]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in restaurants]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where they are restaurants.\nAmount: {len(restaurants)}")
        for index in range(0, len(restaurants), 1):
            restaurants[index].nature = "Restaurants"
        self.setBusinessDetailsData(restaurants + filtered_business_details)

    def sanitizeBusinessDetailsNatureWebPortals(self) -> None:
        """
        Sanitizing the nature where they are web portals.

        Returns:
            void
        """
        web_portals: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and "web portals" in business_detail.nature.lower()]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in web_portals]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where they are web portals.\nAmount: {len(web_portals)}")
        for index in range(0, len(web_portals), 1):
            web_portals[index].nature = "Activities Of Head Offices"
        self.setBusinessDetailsData(web_portals + filtered_business_details)

    def sanitizeBusinessDetailsNatureHeadOffices(self) -> None:
        """
        Sanitizing the nature where they are head offices.

        Returns:
            void
        """
        head_offices: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and "head offices" in business_detail.nature.lower()]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in head_offices]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where they are head offices.\nAmount: {len(head_offices)}")
        for index in range(0, len(head_offices), 1):
            head_offices[index].nature = "Activities Of Head Offices"
        self.setBusinessDetailsData(head_offices + filtered_business_details)

    def sanitizeBusinessDetailsNatureWholesalers(self) -> None:
        """
        Sanitizing the nature where they are wholesalers.

        Returns:
            void
        """
        wholesalers: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and "non-specialised wholesale trade" in business_detail.nature.lower()]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in wholesalers]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where they are wholesalers.\nAmount: {len(wholesalers)}")
        for index in range(0, len(wholesalers), 1):
            wholesalers[index].nature = "Non-Specialised Wholesale Trade"
        self.setBusinessDetailsData(wholesalers + filtered_business_details)

    def sanitizeBusinessDetailsNatureGeneralRetailers(self) -> None:
        """
        Sanitizing the nature where they are general retailers.

        Returns:
            void
        """
        general_retailers: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and ("general retailer" in business_detail.nature.lower() or "foodstuff" in business_detail.nature.lower())]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in general_retailers]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where they are general retailers.\nAmount: {len(general_retailers)}")
        for index in range(0, len(general_retailers), 1):
            general_retailers[index].nature = "General Retailer"
        self.setBusinessDetailsData(general_retailers + filtered_business_details)

    def sanitizeBusinessDetailsNatureFirms(self) -> None:
        """
        Sanitizing the nature where '(Firm)' are removed.

        Returns:
            void
        """
        firms: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and "(Firm)" in business_detail.nature]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in firms]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where it is 'Other Professional, Scientific And Technical Activities'.\nAmount: {len(firms)}")
        for index in range(0, len(firms), 1):
            nature: str = str(firms[index].nature).replace("(Firm)", "")
            firms[index].nature = nature
        self.setBusinessDetailsData(firms + filtered_business_details)

    def sanitizeBusinessDetailsNatureOtherProfessionalScientificTechnicalActivities(self) -> None:
        """
        Sanitizing the nature where it is 'Other Professional,
        Scientific And Technical Activities'.

        Returns:
            void
        """
        other_professional_scientific_technical_activities: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and ("other" in business_detail.nature.lower() and "professional" in business_detail.nature.lower())]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in other_professional_scientific_technical_activities]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where it is 'Other Professional, Scientific And Technical Activities'.\nAmount: {len(other_professional_scientific_technical_activities)}")
        for index in range(0, len(other_professional_scientific_technical_activities), 1):
            other_professional_scientific_technical_activities[index].nature = "Other Professional, Scientific And Technical Activities"
        self.setBusinessDetailsData(other_professional_scientific_technical_activities + filtered_business_details)

    def sanitizeBusinessDetailsNatureNotElsewhereClassified(self) -> None:
        """
        Sanitizing the nature where it is the "Not Elsewhere
        Classfied" but it will be changed to "Other Business Support
        Activities".

        Returns:
            void
        """
        not_elsewhere_classified: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and ("N.E.C" in business_detail.nature or "n.e.c" in business_detail.nature)]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in not_elsewhere_classified]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where it is the 'Not Elsewhere Classfied' but it will be changed to 'Other Business Support Activities'.\nAmount: {len(not_elsewhere_classified)}")
        for index in range(0, len(not_elsewhere_classified), 1):
            not_elsewhere_classified[index].nature = "Other Business Support Activities"
        self.setBusinessDetailsData(not_elsewhere_classified + filtered_business_details)

    def sanitizeBusinessDetailsNatureJobContractors(self) -> None:
        """
        Sanitizing the nature where it is the "Job Contractor" but
        it will be changed to "Other Business Support Activities".

        Returns:
            void
        """
        job_contractors: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and ("job contractor" in business_detail.nature.lower() or "A," in business_detail.nature or "grade" in business_detail.nature.lower())]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in job_contractors]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where it is the 'Job Contractor' but it will be changed to 'Other Business Support Activities'.\nAmount: {len(job_contractors)}")
        for index in range(0, len(job_contractors), 1):
            job_contractors[index].nature = "Other Business Support Activities"
        self.setBusinessDetailsData(job_contractors + filtered_business_details)

    def sanitizeBusinessDetailsNatureSameAsName(self) -> None:
        """
        Sanitizing the nature where it is the same as the name but
        it will be changed to "Other Business Support Activities".

        Returns:
            void
        """
        same_as_name: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and business_detail.name != None and (business_detail.nature == business_detail.name or business_detail.nature in business_detail.name)]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData()if business_detail not in same_as_name]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the nature where it is the same as the name but it will be changed to 'Other Business Support Activities'.\nAmount: {len(same_as_name)}")
        for index in range(0, len(same_as_name), 1):
            same_as_name[index].nature = "Other Business Support Activities"
        self.setBusinessDetailsData(same_as_name + filtered_business_details)

    def curateOfficeBearer(self) -> None:
        """
        Curating the data that is in the Office Bearers table.
        Curating the positions into the form needed.  Curating and
        sanitizing the name into the form needed.  Curating and
        sanitizing the address in to the form needed.

        Returns:
            void
        """
        no_content: int = 204
        accepted: int = 202
        created: int = 201
        quarter: FinancialCalendar = self.getFinancialCalendar().getCurrentQuarter()  # type: ignore
        current_time: int = int(time())
        self.setOfficeBearerData(self.getOfficeBearers().get())
        amount: int = len(self.getOfficeBearerData())
        self.curateOfficeBearerPosition()
        self.curateOfficeBearerName()
        self.curateOfficeBearerAddress()
        dataset: List[OfficeBearer] = [office_bearer for office_bearer in self.getOfficeBearerData()]
        for index in range(0, len(dataset), 1):
            identifier: int = index + 1
            dataset[index].identifier = identifier
        self.setOfficeBearerData(dataset)
        amount_found: int = len(self.getOfficeBearerData())
        status: int = self.getOfficeBearers().delete()
        statuses: List[int] = list(set([self.getOfficeBearers().addCuratedDirectors(office_bearer) for office_bearer in self.getOfficeBearerData()])) if status == no_content else [status]
        status = accepted if len(statuses) == 1 and statuses[0] == created else statuses[0]
        log: Tuple[str, str, int, int, int, int, int] = ("curateOfficeBearer", quarter.quarter, current_time, current_time, status, amount, amount_found)
        self.getFinCorpLogs().postSuccessfulCorporateDataCollectionRun(log) # type: ignore

    def curateOfficeBearerPosition(self) -> None:
        """
        Standardizing the formatting of office bearer positions.

        This method processes office bearer data, ensuring that all position titles are properly capitalized using title case.

        Returns:
            None
        """
        office_bearers: List[OfficeBearer] = self.getOfficeBearerData()
        self.getLogger().inform(f"Office Bearer: Position: Curating the positions into the form needed.\nAmount: {len(office_bearers)}")
        for office_bearer in office_bearers:
            position: str = office_bearer.position.title()
            office_bearer.position = position
        self.setOfficeBearerData(office_bearers)

    def curateOfficeBearerName(self) -> None:
        """
        Curating and sanitizing the names of office bearers by filtering out invalid names and formatting valid ones.

        The function performs the following steps:
            1. Retrieves a list of office bearers.
            2. Filters out office bearers whose names contain numeric digits.
            3. Further filters out names that contain predefined keywords.
            4. Formats the remaining names by applying title case and replacing "Ltd" with "LTD".
            5. Logs the number of deleted and retained office bearers.
            6. Updates the office bearer data with the cleaned list.

        Returns:
            None
        """
        keywords: List[str] = ["C/O", "C.O", "Business Park", "Country", "Road", "Street", "Avenue", "Lane", "Building", "Mountain", "Commercial Centre", "Business Centre", "House", "Rue "]
        office_bearers: List[OfficeBearer] = self.getOfficeBearerData()
        deleted: List[OfficeBearer] = [office_bearer for office_bearer in office_bearers if search(r"\d", office_bearer.name)]
        filtered_data: List[OfficeBearer] = [office_bearer for office_bearer in office_bearers if office_bearer not in deleted and not any(keyword in office_bearer.name for keyword in keywords)]
        for office_bearer in filtered_data:
            office_bearer.name = office_bearer.name.title().replace("Ltd", "LTD")
        self.getLogger().inform(f"Office Bearer: Name: Curating and sanitizing the Name into the form needed.\nDeleted Amount: {len(deleted)}\nFiltered Data: {len(filtered_data)}")
        self.setOfficeBearerData(filtered_data)

    def curateOfficeBearerAddress(self) -> None:
        """
        Curating and sanitizing the address into the form needed.

        Returns:
            void
        """
        filtered_data: List[OfficeBearer] = [office_bearer for office_bearer in self.getOfficeBearerData() if office_bearer.address != None]
        filtered_data = [office_bearer for office_bearer in filtered_data if ", " in str(office_bearer.address)]
        for index in range(0, len(filtered_data), 1):
            address: str = str(filtered_data[index].address).title()
            filtered_data[index].address = address
        self.getLogger().inform(f"Office Bearer: Address: Curating and sanitizing the address into the form needed.\nFiltered Data: {len(filtered_data)}")
        self.setOfficeBearerData(filtered_data)

    def curateShareholders(self) -> None:
        """
        Curating the data that is in the Shareholders table.
        Curating and sanitizing the type of the shareholders.
        Curating and sanitizing the currency of the shareholders.
        Curating and sanitizing the name of the shareholders.

        Returns:
            void
        """
        no_content: int = 204
        accepted: int = 202
        created: int = 201
        quarter: FinancialCalendar = self.getFinancialCalendar().getCurrentQuarter()  # type: ignore
        current_time: int = int(time())
        self.setShareholderData(self.getShareholders().get())
        amount: int = len(self.getShareholderData())
        self.curateShareholdersType()
        self.curateShareholdersCurrency()
        self.curateShareholdersName()
        dataset: List[Shareholder] = [shareholder for shareholder in self.getShareholderData()]
        for index in range(0, len(dataset), 1):
            identifier: int = index + 1
            dataset[index].identifier = identifier
        self.setShareholderData(dataset)
        amount_found: int = len(self.getShareholderData())
        status: int = self.getShareholders().delete()
        statuses: List[int] = list(set([self.getShareholders().addCuratedShareholder(shareholder) for shareholder in self.getShareholderData()])) if status == no_content else [status]
        status = accepted if len(statuses) == 1 and statuses[0] == created else statuses[0]
        log: Tuple[str, str, int, int, int, int, int] = ("curateShareholders", quarter.quarter, current_time, current_time, status, amount, amount_found)
        self.getFinCorpLogs().postSuccessfulCorporateDataCollectionRun(log) # type: ignore

    def curateShareholdersType(self) -> None:
        """
        Curating and sanitizing the type of the shares.

        Returns:
            void
        """
        ordinary: List[Shareholder] = [shareholder for shareholder in self.getShareholderData() if "ordinary" in shareholder.type_shares.lower()]
        remaining_data: List[Shareholder] = [shareholder for shareholder in self.getShareholderData() if shareholder not in ordinary]
        social_part: List[Shareholder] = [shareholder for shareholder in remaining_data if shareholder.type_shares.lower() == "part sociale" or shareholder.type_shares.lower() == "part d'interet"]
        remaining_data = [shareholder for shareholder in remaining_data if shareholder not in social_part]
        class_d: List[Shareholder] = [shareholder for shareholder in remaining_data if "class d" in shareholder.type_shares.lower()]
        remaining_data = [shareholder for shareholder in remaining_data if shareholder not in class_d]
        ordinary = ordinary + remaining_data
        for index in range(0, len(ordinary), 1):
            type: str = "Ordinary"
            ordinary[index].type_shares = type
        self.getLogger().inform(f"Shareholders: Type: Curating and sanitizing the type of the shares for Ordinary Shares.\nAmount: {len(ordinary)}")
        for index in range(0, len(social_part), 1):
            type: str = "Part Sociale"
            social_part[index].type_shares = type
        self.getLogger().inform(f"Shareholders: Type: Curating and sanitizing the type of the shares for Part Sociale.\nAmount: {len(social_part)}")
        for index in range(0, len(class_d), 1):
            type: str = "Class D"
            class_d[index].type_shares = type
        self.getLogger().inform(f"Shareholders: Type: Curating and sanitizing the type of the shares for Class D Shares.\nAmount: {len(class_d)}")
        self.setShareholderData(ordinary + social_part + class_d)

    def curateShareholdersCurrency(self) -> None:
        """
        Curating and sanitizing the currency of the shareholders.

        Returns:
            void
        """
        mauritian_rupee: List[Shareholder] = [shareholder for shareholder in self.getShareholderData() if "mauritius rupee" in shareholder.currency.lower()]
        remaining_data: List[Shareholder] = [shareholder for shareholder in self.getShareholderData() if shareholder not in mauritian_rupee]
        us_dollar: List[Shareholder] = [shareholder for shareholder in remaining_data if "us dollar" in shareholder.currency.lower()]
        remaining_data = [shareholder for shareholder in remaining_data if shareholder not in us_dollar]
        mauritian_rupee = mauritian_rupee + remaining_data
        for index in range(0, len(mauritian_rupee), 1):
            currency: str = "Mauritius Rupee"
            mauritian_rupee[index].currency = currency
        self.getLogger().inform(f"Shareholders: Currency: Curating and sanitizing the currency of the shares for Mauritian Rupee.\nAmount: {len(mauritian_rupee)}")
        for index in range(0, len(us_dollar), 1):
            currency: str = "US Dollar"
            us_dollar[index].currency = currency
        self.getLogger().inform(f"Shareholders: Currency: Curating and sanitizing the currency of the shares for American Dollar.\nAmount: {len(us_dollar)}")
        self.setShareholderData(mauritian_rupee + us_dollar)

    def curateShareholdersName(self) -> None:
        """
        Curating and sanitizing the name of the shareholders.

        Returns:
            void
        """
        filtered_data: List[Shareholder] = [shareholder for shareholder in self.getShareholderData() if "service address" not in shareholder.name.lower()]
        filtered_data = [shareholder for shareholder in filtered_data if "street" not in shareholder.name.lower()]
        filtered_data = [shareholder for shareholder in filtered_data if "lane" not in shareholder.name.lower()]
        filtered_data = [shareholder for shareholder in filtered_data if "morcellement" not in shareholder.name.lower()]
        filtered_data = [shareholder for shareholder in filtered_data if "port louis" not in shareholder.name.lower()]
        filtered_data = [shareholder for shareholder in filtered_data if "mauritius rupee" not in shareholder.name.lower()]
        filtered_data = [shareholder for shareholder in filtered_data if "avenue" not in shareholder.name.lower()]
        filtered_data = [shareholder for shareholder in filtered_data if "quatre bornes" not in shareholder.name.lower()]
        filtered_data = [shareholder for shareholder in filtered_data if shareholder.name.lower() != "mauritius"]
        filtered_data = [shareholder for shareholder in filtered_data if "vacoas" not in shareholder.name.lower()]
        filtered_data = [shareholder for shareholder in filtered_data if "office bearers" not in shareholder.name.lower()]
        filtered_data = [shareholder for shareholder in filtered_data if "position" not in shareholder.name.lower()]
        filtered_data = [shareholder for shareholder in filtered_data if "gerant" not in shareholder.name.lower()]
        filtered_data = [shareholder for shareholder in filtered_data if "date issued" not in shareholder.name.lower()]
        filtered_data = [shareholder for shareholder in filtered_data if "road" not in shareholder.name.lower()]
        filtered_data = [shareholder for shareholder in filtered_data if "," not in shareholder.name.lower()]
        filtered_data = [shareholder for shareholder in filtered_data if "part" not in shareholder.name.lower()]
        filtered_data = [shareholder for shareholder in filtered_data if "d'interet" not in shareholder.name.lower()]
        filtered_data = [shareholder for shareholder in filtered_data if "louis mauritius" not in shareholder.name.lower()]
        filtered_data = [shareholder for shareholder in filtered_data if " rd " not in shareholder.name.lower()]
        filtered_data = [shareholder for shareholder in filtered_data if "floor" not in shareholder.name.lower()]
        filtered_data = [shareholder for shareholder in filtered_data if "goodlands" not in shareholder.name.lower()]
        filtered_data = [shareholder for shareholder in filtered_data if "nhdc" not in shareholder.name.lower()]
        filtered_data = [shareholder for shareholder in filtered_data if "mahebourg" not in shareholder.name.lower()]
        filtered_data = [shareholder for shareholder in filtered_data if "rue" not in shareholder.name.lower()]
        filtered_data = [shareholder for shareholder in filtered_data if " morc " not in shareholder.name.lower()]
        for index in range(0, len(filtered_data), 1):
            name: str = filtered_data[index].name.title().replace("ltd", "LTD").replace("Ltd", "LTD")
            filtered_data[index].name = name
        self.getLogger().inform(f"Shareholders: Name: Curating and sanitizing the name of the shareholders.\nAmount: {len(filtered_data)}")
        self.setShareholderData(filtered_data)

    def curateMembers(self) -> None:
        """
        Curating the data that is in the Members table.  Curating
        the currency in the members table.  Curating and sanitizing
        the names of the members. Curating the amount of the shares
        of the members and filtering based on them.

        Returns:
            void
        """
        no_content: int = 204
        accepted: int = 202
        created: int = 201
        quarter: FinancialCalendar = self.getFinancialCalendar().getCurrentQuarter()  # type: ignore
        current_time: int = int(time())
        self.setMemberData(self.getMembers().get())
        amount: int = len(self.getMemberData())
        self.curateMembersCurrencies()
        self.curateMembersNames()
        self.curateMembersAmount()
        dataset: List[Member] = [member for member in self.getMemberData()]
        for index in range(0, len(dataset), 1):
            identifier: int = index + 1
            dataset[index].identifier = identifier
        self.setMemberData(dataset)
        amount_found: int = len(self.getMemberData())
        status: int = self.getMembers().delete()
        statuses: List[int] = list(set([self.getMembers().addCuratedMember(member) for member in self.getMemberData()])) if status == no_content else [status]
        status = accepted if len(statuses) == 1 and statuses[0] == created else statuses[0]
        log: Tuple[str, str, int, int, int, int, int] = ("curateMembers", quarter.quarter, current_time, current_time, status, amount, amount_found)
        self.getFinCorpLogs().postSuccessfulCorporateDataCollectionRun(log) # type: ignore

    def curateMembersCurrencies(self) -> None:
        """
        Curating the currency in the members table.

        Returns:
            None
        """
        mauritian_rupee: List[Member] = [member for member in self.getMemberData() if "mauritius rupee" in member.currency.lower()]
        remaining_data: List[Member] = [member for member in self.getMemberData() if member not in mauritian_rupee]
        us_dollar: List[Member] = [member for member in remaining_data if "us dollar" in member.currency.lower()]
        remaining_data = [member for member in remaining_data if member not in us_dollar]
        mauritian_rupee = mauritian_rupee + remaining_data
        for index in range(0, len(mauritian_rupee), 1):
            currency: str = "Mauritius Rupee"
            mauritian_rupee[index].currency = currency
        self.getLogger().inform(f"Members: Currency: Curating and sanitizing the currency of the members for Mauritian Rupee.\nAmount: {len(mauritian_rupee)}")
        for index in range(0, len(us_dollar), 1):
            currency: str = "Mauritius Rupee"
            us_dollar[index].currency = currency
        self.getLogger().inform(f"Members: Currency: Curating and sanitizing the currency of the members for American Dollar.\nAmount: {len(us_dollar)}")
        self.setMemberData(mauritian_rupee + us_dollar)

    def curateMembersNames(self) -> None:
        """
        Curating and sanitizing the names of the members.

        Returns:
            None
        """
        filtered_data: List[Member] = [member for member in self.getMemberData() if "service address" not in member.name.lower()]
        filtered_data = [member for member in filtered_data if "street" not in member.name.lower()]
        filtered_data = [member for member in filtered_data if "lane" not in member.name.lower()]
        filtered_data = [member for member in filtered_data if "morcellement" not in member.name.lower()]
        filtered_data = [member for member in filtered_data if "port louis" not in member.name.lower()]
        filtered_data = [member for member in filtered_data if "mauritius rupee" not in member.name.lower()]
        filtered_data = [member for member in filtered_data if "avenue" not in member.name.lower()]
        filtered_data = [member for member in filtered_data if "quatre bornes" not in member.name.lower()]
        filtered_data = [member for member in filtered_data if member.name.lower() != "mauritius"]
        filtered_data = [member for member in filtered_data if "vacoas" not in member.name.lower()]
        filtered_data = [member for member in filtered_data if "office bearers" not in member.name.lower()]
        filtered_data = [member for member in filtered_data if "position" not in member.name.lower()]
        filtered_data = [member for member in filtered_data if "gerant" not in member.name.lower()]
        filtered_data = [member for member in filtered_data if "date issued" not in member.name.lower()]
        filtered_data = [member for member in filtered_data if "road" not in member.name.lower()]
        filtered_data = [member for member in filtered_data if "," not in member.name.lower()]
        filtered_data = [member for member in filtered_data if "part" not in member.name.lower()]
        filtered_data = [member for member in filtered_data if "d'interet" not in member.name.lower()]
        filtered_data = [member for member in filtered_data if "louis mauritius" not in member.name.lower()]
        filtered_data = [member for member in filtered_data if " rd " not in member.name.lower()]
        filtered_data = [member for member in filtered_data if "floor" not in member.name.lower()]
        filtered_data = [member for member in filtered_data if "goodlands" not in member.name.lower()]
        filtered_data = [member for member in filtered_data if "nhdc" not in member.name.lower()]
        filtered_data = [member for member in filtered_data if "mahebourg" not in member.name.lower()]
        filtered_data = [member for member in filtered_data if "rue" not in member.name.lower()]
        filtered_data = [member for member in filtered_data if " morc " not in member.name.lower()]
        for index in range(0, len(filtered_data), 1):
            name: str = filtered_data[index].name.title().replace("ltd", "LTD").replace("Ltd", "LTD")
            filtered_data[index].name = name
        self.getLogger().inform(f"Members: Name: Curating and sanitizing the name of the members.\nAmount: {len(filtered_data)}")
        self.setMemberData(filtered_data)

    def curateMembersAmount(self) -> None:
        """
        Curating the amount of the shares of the members and
        filtering based on them.

        Returns:
            None
        """
        filtered_data: List[Member] = [member for member in self.getMemberData() if member.amount > 0]
        self.getLogger().inform(f"Members: Amount: Curating and sanitizing the amount of the shares of the members.\nAmount: {len(filtered_data)}")
        self.setMemberData(filtered_data)
