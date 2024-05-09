from Models.Builder import Builder
from datetime import datetime
from datetime import timedelta


module_limit_execution = datetime.now() + timedelta(minutes=15)
module_limit_execution_time = module_limit_execution.timestamp()
while datetime.now().timestamp() < module_limit_execution_time:
    Corporate_Database_Builder = Builder()
    Corporate_Database_Builder.collectCorporateMetadata()