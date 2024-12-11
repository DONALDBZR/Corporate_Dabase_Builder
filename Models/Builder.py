"""
The module which will have the main corporate database
builder.

Authors:
    Andy Ewen Gaspard
"""


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
from Models.Members import Member
from datetime import datetime, timedelta
from Environment import Environment
from typing import List, Tuple, Union, Dict
from time import time, sleep
from re import findall, search
from Models.Mail import Mail
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
    __members: Member
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
        self.setMembers(Member())
        self.getLogger().inform("The builder has been initialized and all of its dependencies are injected!")

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

    def getMembers(self) -> Member:
        return self.__members

    def setMembers(self, members: Member) -> None:
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
        # recipient: str = "andyg@finclub.mu"
        # carbon_copy: str = "andygaspard@hotmail.com"
        # subject: str = "Corporate Database Builder: Module 3: Extraction"
        # message: str
        # self.setMailer(Mail())
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
        # if response >= 200 and response <= 299:
        #     message = f"The Corporate Database Builder has extracted {final_amount} corporate registries for {date}.  Please verify the log file of the application to ensure that these files are correctly extracted or that there are any errors in the application.  Please note that it is a computer generated mail.  For any communication, contact the ones that are attached as carbon copies."
        #     subject = "Corporate Database Builder: Module 3: Extraction"
        # else:
        #     message = f"The Corporate Database Builder has extracted {final_amount} corporate registries for {date} but there should be some data that are missing.  Please verify the log file of the application to ensure that these files are correctly extracted or that there are any errors in the application.  Please note that it is a computer generated mail.  For any communication, contact the ones that are attached as carbon copies."
        #     subject = "Corporate Database Builder: Module 3: Extraction - Failed"
        # self.getMailer().send(recipient, subject, message, carbon_copy)
        if response >= 500 and response <= 599:
            exit()
        # self.cleanExtractionCacheDirectory()

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
            void
        """
        response: int
        data_manipulations: List[int] = []
        for index in range(0, len(document_files), 1):
            company_detail: CompanyDetails = self.getCompanyDetails().getSpecificCompanyDetails(document_files[index].company_detail)
            file_generation_status: int = self.getDocumentReader().generatePortableDocumentFile(document_files[index])
            data_extraction: Union[Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]], Dict[str, Union[int, Dict[str, Union[str, int]], Dict[str, str], List[Dict[str, Union[str, int]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]], Dict[str, Union[Dict[str, str], List[Dict[str, int]]]]]]] = self.getDocumentReader().extractData(file_generation_status, document_files[index], company_detail)
            data_manipulations.append(self.storeCorporateData(data_extraction, document_files[index], company_detail))
        data_manipulations = list(set(data_manipulations))
        if len(data_manipulations) == 1 and data_manipulations[0] == 201:
            response = 200
            self.getLogger().inform(f"The corporate data has been extracted successfully and stored into the relational database server.\nStatus: {response}")
        else:
            response = 503
            self.getLogger().error(f"The corporate data has been extracted successfully and stored into the relational database server.\nStatus: {response}")
        return response

    def storeCorporateData(self, dataset: Union[Dict[str, Union[int, Dict[str, Union[str, int]], List[Dict[str, str]], List[Dict[str, Union[str, int]]], List[Dict[str, int]], Dict[str, Union[Dict[str, Union[int, str]], float]], Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Union[Dict[str, float], float]]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]]]], Dict[str, Union[int, Dict[str, Union[str, int]], Dict[str, str], List[Dict[str, Union[str, int]]], Dict[str, Union[Dict[str, Union[str, int]], List[Dict[str, int]]]], Dict[str, Union[Dict[str, str], List[Dict[str, int]]]]]]], document_file: DocumentFiles, company_detail: CompanyDetails) -> int:
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
        response: int
        if company_detail.category.upper() == "DOMESTIC":
            response = self.storeCorporateDataDomestic(dataset, document_file, company_detail) # type: ignore
        elif company_detail.category.upper() == "AUTHORISED COMPANY":
            response = self.storeCorporateDataAuthorisedCompany(dataset, document_file) # type: ignore
        elif company_detail.category.upper() == "GLOBAL BUSINESS COMPANY":
            response = self.storeCorporateDataGlobalBusinessCompany(dataset, document_file) # type: ignore
        elif company_detail.category.upper() == "FOREIGN(DOM BRANCH)":
            response = self.storeCorporateDataForeignDomestic(dataset, document_file) # type: ignore
        else:
            self.getLogger().error(f"The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Builder.storeCorporateData()\nCategory: {company_detail.category}")
            exit()
        if response >= 200 and response <= 299:
            response = 201
        return response

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
        elif company_detail.nature.upper() == "CIVIL":
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
        response: int
        if status >= 200 and status <= 299 and len(objections) == 0:
            response = 200
            self.getLogger().inform(f"There is no data to be inserted into the Objections table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {objections}")
        elif status >= 200 and status <= 299 and len(objections) != 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Builder.storeCorporateDataDomesticObjections()")
            exit()
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
        return response

    def storeCorporateDataDomesticDetails(self, status: int, details: List[Dict[str, Union[str, int]]], document_file: DocumentFiles) -> int:
        """
        Doing the data manipulation on the details result set.

        Parameters:
            status: int: The status of the data manipulation.
            details: [{type: string, date_start: int, date_end: int, status: string}]: The data that has been extracted for the details table.
            document_file: {identifier: int, file_data: bytes, company_detail: int}: The data about the corporate registry.

        Returns:
            int
        """
        response: int
        if status >= 200 and status <= 299 and len(details) == 0:
            response = 200
            self.getLogger().inform(f"There is no data to be inserted into the Details table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {details}")
        elif status >= 200 and status <= 299 and len(details) != 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Builder.storeCorporateDataDomesticDetails()")
            exit()
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
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
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Builder.storeCorporateDataDomesticCharges()")
            exit()
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
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
        if status >= 200 and status <= 299 and not balance_sheet:
            response = 200
            self.getLogger().inform(f"There is no data to be inserted into the Balance Sheet table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {balance_sheet}")
        elif status >= 200 and status <= 299 and len(balance_sheet) != 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Builder.storeCorporateDataDomesticBalanceSheet()")
            exit()
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
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
        if status >= 200 and status <= 299 and not profit_statement:
            response = 200
            self.getLogger().inform(f"There is no data to be inserted into the Profit Statement table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {profit_statement}")
        elif status >= 200 and status <= 299 and len(profit_statement) != 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Builder.storeCorporateDataDomesticProfitStatement()")
            exit()
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
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
        response: int
        if status >= 200 and status <= 299 and len(financial_summaries) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Builder.storeCorporateDataDomesticFinancialSummary()")
            exit()
        elif status >= 200 and status <= 299 and len(financial_summaries) == 0:
            response = 200
            self.getLogger().inform(f"There is no data to be inserted into the Financial Summaries table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {financial_summaries}")
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
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
        response: int
        if status >= 200 and status <= 299 and len(annual_return) > 0:
            self.getLogger().error("The application will abort the extraction as the function has not been implemented!\nStatus: 503\nFunction: Builder.storeCorporateDataDomesticAnnualReturn()")
            exit()
        elif status >= 200 and status <= 299 and len(annual_return) == 0:
            response = 200
            self.getLogger().inform(f"There is no data to be inserted into the Annual Return table.\nStatus: {response}\nIdentifier: {document_file.company_detail}\nData: {annual_return}")
        else:
            response = status
            self.getLogger().error(f"An error occurred in the application.  The extraction will be aborted and the corporate registry will be removed from the processing server.\nStatus: {response}\nExtraction Status: {status}\nCompany Detail Identifier: {document_file.company_detail}\nDocument File Identifier: {document_file.identifier}")
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

    def curateBusinessDetails(self) -> None:
        """
        Curating the data that is in the Business Details table.
        The erroneous registered addresses have to be sanitized for
        the geographical information system to be able to process it
        afterwards.  The names have to be sanitized to reflect the
        companies they are affliated with.  The natures have to be
        sanitized to be processed afterwards to obtain the sector of
        activity of the company by doing a sentiment analysis.

        Returns:
            void
        """
        line_break: str = "-" * 10
        quarter: FinancialCalendar = self.getFinancialCalendar().getCurrentQuarter()  # type: ignore
        self.setBusinessDetailsData(self.getBusinessDetails().getBusinessDetails())
        self.setCompanyDetailsData([self.getCompanyDetails().getSpecificCompanyDetails(identifier) for identifier in list(set([business_detail.CompanyDetail for business_detail in self.getBusinessDetailsData()]))])
        self.sanitizeBusinessDetailsErroneousRegisteredAddresses()
        self.sanitizeBusinessDetailsName()
        self.sanitizeBusinessDetailsNature()
        print(f"{line_break}\n{quarter=}\n{line_break}\nBusiness Details (Amount): {len(self.getBusinessDetailsData())}\n{line_break}\nCompanies (Amount): {len(self.getCompanyDetailsData())}\n{line_break}")
        for index in range(0, len(self.getBusinessDetailsData()), 1):
            iteration: int = index + 1
            self.getLogger().debug(f"{iteration=}\n{self.getBusinessDetailsData()[index]}")
        exit()

    def sanitizeBusinessDetailsErroneousRegisteredAddresses(self) -> None:
        """
        Sanitizing the registered addresses that are going to be
        used by the geographical information system to be able to
        process it afterwards.

        Returns:
            void
        """
        erroneous_registered_addresses: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.registered_address != None and bool(search(r"\d", business_detail.registered_address)) == True]
        self.getLogger().inform(f"Business Details: The registered addresses are being sanitized!\nAmount: {len(erroneous_registered_addresses)}")
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
        Sanitizing the names which are equal to ".".

        Returns:
            void
        """
        same_names: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.name == "."]
        filtered_business_data: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail not in same_names]
        self.getLogger().inform(f"Business Details: Name: The names are being sanitized where '.' will be replaced by their company names.\nAmount: {len(same_names)}")
        self.setBusinessDetailsData([])
        for index in range(0, len(same_names), 1):
            company_detail: CompanyDetails = [company_detail for company_detail in self.getCompanyDetailsData() if company_detail.identifier == same_names[index].CompanyDetail][0]
            same_names[index].name = company_detail.name
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
            countries_names[index].name = company_detail.name
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
            no_name_domestic_companies[index].name = company_detail.name
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
            addresses_as_names[index].name = company_detail.name
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
            names_as_natures[index].name = company_detail.name
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

    def sanitizeBusinessDetailsNature(self) -> None:
        """
        The natures have to be sanitized to be processed afterwards
        to obtain the sector of activity of the company by doing a
        sentiment analysis.

        Returns:
            void
        """
        self.sanitizeBusinessDetailsNatureGeneralRetailers()
        self.sanitizeBusinessDetailsNatureOtherBusinessSupportServiceActivities()
        self.sanitizeBusinessDetailsNatureFirms()
        self.sanitizeBusinessDetailsNatureNotElsewhereClassified()

    def sanitizeBusinessDetailsNatureGeneralRetailers(self) -> None:
        """
        Sanitizing the natures for the general retailers.

        Returns:
            void
        """
        general_retailers: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and "general retailer" in business_detail.nature.lower()]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail not in general_retailers]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the natures for the general retailers.\nAmount: {len(general_retailers)}")
        for index in range(0, len(general_retailers), 1):
            general_retailers[index].nature = "General Retailer"
        self.setBusinessDetailsData(general_retailers + filtered_business_details)

    def sanitizeBusinessDetailsNatureOtherBusinessSupportServiceActivities(self) -> None:
        """
        Sanitizing the natures for Other Business Support Service
        Activities.

        Returns:
            void
        """
        other_business_support_service_activities: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and "other" in business_detail.nature.lower() and "support" in business_detail.nature.lower()]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail not in other_business_support_service_activities]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the natures for other business support service activities.\nAmount: {len(other_business_support_service_activities)}")
        for index in range(0, len(other_business_support_service_activities), 1):
            other_business_support_service_activities[index].nature = "Other Business Support Service Activities"
        self.setBusinessDetailsData(other_business_support_service_activities + filtered_business_details)

    def sanitizeBusinessDetailsNatureFirms(self) -> None:
        """
        Sanitizing the natures there are firms in the nature.

        Returns:
            void
        """
        firms: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and "(firm)" in business_detail.nature.lower()]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail not in firms]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the natures there are firms in the nature.\nAmount: {len(firms)}")
        for index in range(0, len(firms), 1):
            nature: str = firms[index].nature.replace("(Firm)", "") # type: ignore
            firms[index].nature = nature
        self.setBusinessDetailsData(firms + filtered_business_details)

    def sanitizeBusinessDetailsNatureNotElsewhereClassified(self) -> None:
        """
        Sanitizing the natures there are NEC.

        Returns:
            void
        """
        others: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail.nature != None and "N.E.C" in business_detail.nature.upper()]
        filtered_business_details: List[BusinessDetails] = [business_detail for business_detail in self.getBusinessDetailsData() if business_detail not in others]
        self.setBusinessDetailsData([])
        self.getLogger().inform(f"Business Details: Nature: Sanitizing the natures there are NEC.\nAmount: {len(others)}")
        for index in range(0, len(others), 1):
            others[index].nature = "Other Business Support Service Activities"
        self.setBusinessDetailsData(others + filtered_business_details)