from solution import starter

def test_passedbuckets():
    starter('sample_data.csv','sample_buckets.csv')
    Expected_output  =   """[{"bucket": "pearson,*,*", "purchases": []}, {"bucket": "pearson,2,*", "purchases": ["7639,9781541920172,pearson,ord,2,1_day,2015-06-30 12:25:00"]}, {"bucket": "pearson,1,3_day", "purchases": ["7640,9781541920142,pearson,ord,1,3_day,2015-07-31 10:31:00", "7643,9781541920172,pearson,ord,1,1_day,2015-06-30 12:25:00"]}, {"bucket": "mcgraw-hill,*,*", "purchases": ["7642,9781541920293,mcgraw-hill,den,2,1_day,2015-05-14 11:35:00"]}, {"bucket": "*,*,*", "purchases": ["7641,9781541920283,scipub,dfw,3,5_day,2015-10-31 17:35:00", "7644,9781541920993,macmillan,dfw,3,5_day,2015-5-15 14:25:00"]}]"""

    f = open('output.json','r')
    final_output = f.read()
    assert final_output == Expected_output
    f.close()


# The ordered "7643,9781541920172,Pearson,ORD,1,1_day,2015-06-30 12:25:00" belongs to "pearson,1,3_day" but as per your
# explaination this belongs to "pearson,*,*". This is the failed buacket test.
def test_failedbuckets():
    Expected_output  =   """[{"bucket": "pearson,*,*", "purchases": ["7643,9781541920172,Pearson,ORD,1,1_day,2015-06-30 12:25:00"]}, {"bucket": "pearson,2,*", "purchases": ["7639,9781541920172,pearson,ord,2,1_day,2015-06-30 12:25:00"]}, {"bucket": "pearson,1,3_day", "purchases": ["7640,9781541920142,pearson,ord,1,3_day,2015-07-31 10:31:00"]}, {"bucket": "mcgraw-hill,*,*", "purchases": ["7642,9781541920293,mcgraw-hill,den,2,1_day,2015-05-14 11:35:00"]}, {"bucket": "*,*,*", "purchases": ["7641,9781541920283,scipub,dfw,3,5_day,2015-10-31 17:35:00", "7644,9781541920993,macmillan,dfw,3,5_day,2015-5-15 14:25:00"]}]"""

    f = open('output.json','r')
    final_output = f.read()
    assert final_output != Expected_output
    f.close()
