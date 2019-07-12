import redis
import json


connect = redis.Redis(host='192.168.0.110', port=6379, db=1)

for i in range(5):

    result = connect.rpop('cookies')
    print(result)