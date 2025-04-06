from datetime import datetime
from datetime import timedelta
from sys import path


path.insert(0, "/home/darkness4869/Documents/Corporate_Database_Builder")


from Models.Builder import Builder


module_limit_execution: datetime = datetime.now() + timedelta(seconds=10764.077)
module_limit_execution_time: float = module_limit_execution.timestamp()
while datetime.now().timestamp() < module_limit_execution_time:
    Corporate_Database_Builder: Builder = Builder()
    Corporate_Database_Builder.downloadCorporateFile()
