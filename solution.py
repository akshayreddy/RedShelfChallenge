import json, copy
import pandas as pd
from collections import OrderedDict

# Final output is stored in this
result = []
all_buckets = OrderedDict()

def load_transform(purchase_data, purchase_buckets):
    #--------------------Load-----------------------------
    # Lower casings the attributes and sorting the purchase_data data by order_id
    purchase_data = pd.read_csv(purchase_data,sep=',',names =["order_id", "isbn", "publisher", "school","price","duration","order_datetime"]).apply(lambda x: x.astype(str).str.lower()).sort_values('order_id')
    purchase_buckets = pd.read_csv(purchase_buckets,sep=',',names = ["publisher", "price", "duration"]).apply(lambda x: x.astype(str).str.lower())

    #------------------------------------------------------------

    #--------------------Transform 1-----------------------------
    # To ensure the order of buckets and handeling the duplicate buckets
    for key, bucket in purchase_buckets.iterrows():
        value = bucket["publisher"] +','+bucket["price"]+','+bucket["duration"]

        if value in all_buckets:
            all_buckets[value]["count"]+=1
        else:
            all_buckets[value]={"purchases":[], "count":1}

    # If "*,*,*" is not in purchase_buckets, then initailize it
    if "*,*,*" not in all_buckets:
        all_buckets["*,*,*"] = {"purchases":[], "count":1}

    #---------------------------------------------------------------
    return purchase_data, purchase_buckets


#--------------------Classification-----------------------------
class Order:
    def __init__(self, order):
        self.__catogary = [0,'*','*','*']
        self.__bestcatogary = [0,'*','*','*']
        self.__publisher = order['publisher']
        self.__duration = order['duration']
        self.__price = order['price']
        self.order = ",".join([i for i in order])

    def classify(self, bucket_publisher, bucket_duration, bucket_price ):

        #all fields match
        if (self.__publisher == bucket_publisher and self.__duration == bucket_duration and self.__price == bucket_price):
            self.__catogary = copy.deepcopy([7,bucket_publisher,bucket_price,bucket_duration])

        #publisher and duration  match
        elif (self.__publisher == bucket_publisher and self.__duration == bucket_duration and self.__price != bucket_price):
            self.__catogary = copy.deepcopy([6,bucket_publisher,bucket_price,bucket_duration])

        #publisher and price match
        elif (self.__publisher == bucket_publisher and self.__duration != bucket_duration and self.__price == bucket_price):
            self.__catogary = copy.deepcopy([5,bucket_publisher,bucket_price,bucket_duration])

        #duration and price match
        elif (self.__publisher != bucket_publisher and self.__duration == bucket_duration and self.__price == bucket_price):
            self.__catogary = copy.deepcopy([4,bucket_publisher,bucket_price,bucket_duration])

        #only publisher match
        elif (self.__publisher == bucket_publisher and self.__duration != bucket_duration and self.__price != bucket_price):
            self.__catogary = copy.deepcopy([3,bucket_publisher,bucket_price,bucket_duration])

        #only duration match
        elif (self.__publisher != bucket_publisher and self.__duration == bucket_duration and self.__price != bucket_price):
            self.__catogary = copy.deepcopy([2,bucket_publisher,bucket_price,bucket_duration])

        #only price match
        elif (self.__publisher != bucket_publisher and self.__duration != bucket_duration and self.__price == bucket_price):
            self.__catogary = copy.deepcopy([1,bucket_publisher,bucket_price,bucket_duration])

        #choosing the catagory/ bucket with highest priority.
        if self.__catogary[0] > self.__bestcatogary[0]:
            self.__bestcatogary = self.__catogary

        self.__catogary = [0,'*','*','*']

    # Updating the purchases list
    def categorize(self):
        bucket = ",".join(self.__bestcatogary[1:])
        all_buckets[bucket]["purchases"].append(self.order)

    def __str__(self):
        return self.order

# This creates an order object and then loops over the available buckets to select the suitable bucket
def starter(purchase_data, purchase_buckets):
    purchase_data, purchase_buckets = load_transform(purchase_data, purchase_buckets)

    for Dindex,order in purchase_data.iterrows():
        obj = Order(order)
        for Bindex, bucket in purchase_buckets.iterrows():
            obj.classify(bucket_publisher = bucket["publisher"], bucket_duration = bucket["duration"], bucket_price = bucket["price"])
        obj.categorize()

    #--------------------Transform 2-------------------------------
    for key, value in enumerate(all_buckets):
        result.append({"bucket":value, "purchases":all_buckets[value]["purchases"]})

        # if there are more than one buckets with same name, update the ordered dictionary with
        # json object having no purchases
        if all_buckets[value]["count"] > 1:
            result.append({"bucket":value, "purchases":[]})

    #------------------------------------------------------------

    # Exporting the data to output.json
    f = open('output.json','w')
    f.write(json.dumps(result))
    f.close()

if __name__ == '__main__':
    starter('purchase_data.csv','purchase_buckets.csv')
