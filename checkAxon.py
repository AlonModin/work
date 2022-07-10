"""
Find the records:
- for a specific sighting
- collected in the last 14 days
- which contain namednodes content-type
"""
import datetime
import os
import pandas as pd
from pandas.io.json import json_normalize
from pandas import to_datetime, set_option

from svtools import axon_ingest

content_types = ["intel-status-scope-logs-v1"]
days_ago = 7
end_epoch = int(datetime.datetime.utcnow().timestamp())
start_epoch = int((datetime.datetime.utcnow() - datetime.timedelta(days=days_ago)).timestamp())
print(os.getpid())

# setup axon_ingest
axon_ingest.settings.AXON_DB_SERVER = "prod"
axon_ingest.settings.DB_CLIENT = "axon"
axon_ingest.authenticate()
query = axon_ingest.Query()

# SELECT - axon metadata fields
select_fields = [
    "_id",
    "ts",
    "_tsDate",
    "platform.tla",
    "source.toolext_status_scope",
    "_contentTypes",
    "platform.stepping",
    "contents.intel-svtools-report-v1.insights.message",
    "contents.intel-svtools-report-v1.insights.message"
]
for field in select_fields:
    query.select(field)
# WHERE - conditions on metadata
query.where("ts", "ge", start_epoch, where_condition="and")
query.where("ts", "le", end_epoch, where_condition="and")
query.where("source.toolext_status_scope", "exists", True, where_condition='and')
query.where("platform.tla", "eq", "ADL", where_condition='and')

# QUERY
results = query.fetchall()

# shape data
df = json_normalize(results)
df = pd.DataFrame(df)

print()
#df["_id"].tolist()
#using data frame
# """[
#         {
#             "$match": {
#               "$and": [
#                 {
#                 "$and": [
#                     {
#                       "source.toolext_status_scope": {VV
#                         "$exists": true
#                       }
#                     },
#                     {
#                       "_contentTypes": {
#                         "$in": [
#                           "intel-svtools-report-v1"
#                           ]
#                       }
#                     },
#                     {
#                       "contents.intel-svtools-report-v1.insights.message": {
#                         "$regex": "MDAT",
#                         "$options": "i"
#                       }
#                     },
#                     {
#                       "platform.tla": {VV
#                         "$eq": "ADL"
#                       }
#                     }
#                   ]
#                 },
#                 {
#                   "$and": [
#                     {
#                       "ts": {VV
#                         "$gte": end_time
#                       }
#                     },
#                     {
#                       "ts": {VV
#                         "$lte": start_time
#                       }
#                     }
#                   ]
#                 }
#               ]
#             }
#         },
#         {
#             "$project": {
#               "_id": 1,
#               "platform": 1,
#               "insight_messages": {
#                 "$arrayToObject": {
#                     "$map": {
#                       "input": "$contents.intel-svtools-report-v1.insights",
#                       "as": "el",
#                       "in": {
#                         "k": "$$el.message",
#                         "v": "1"
#                       }
#                     }
#                   }
#               },
#               "contents.intel-pythonsv-standard-v1.status_scope.versions.pysvtools.status_scope_ext": 1,
#               "contents.intel-pythonsv-standard-v1.status_scope.executed_plugins": 1
#             }
#         },
#         {
#             "$limit": 100000
#         }
#     ]"""