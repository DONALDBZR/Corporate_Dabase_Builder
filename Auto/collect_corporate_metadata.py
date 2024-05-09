from datetime import datetime
from datetime import timedelta
from sys import path


path.insert(0, "/home/admin/Documents/Darkness4869/fincorp")


from Models.Builder import Builder


module_limit_execution = datetime.now() + timedelta(minutes=15)
module_limit_execution_time = module_limit_execution.timestamp()
while datetime.now().timestamp() < module_limit_execution_time:
    Corporate_Database_Builder = Builder()
    Corporate_Database_Builder.collectCorporateMetadata()