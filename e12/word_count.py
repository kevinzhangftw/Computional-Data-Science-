import sys
from pyspark.sql import SparkSession, functions, types
import string, re

spark = SparkSession.builder.appName('first Spark app').getOrCreate()

assert sys.version_info >= (3, 4) # make sure we have Python 3.4+
assert spark.version >= '2.1' # make sure we have Spark 2.1+

wordbreak = re.compile( r'[%s\s]+' % (re.escape(string.punctuation),))  
# regex that matches spaces and/or punctuation

def countEachRow(wordrow):
    m = wordbreak.search(wordrow)
    counter = 0
    if m:
        # find number of objects in m
    else:


def createWordcountdf(in_directory):
    firstRead = spark.read.text(in_directory)

    #for every row, count the number of words in it 
    return firstRead.map(countEachRow)

def main():
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]

    # DataFrame.read.text

    firstRead = spark.read.text(in_directory)
    firstRead.show(); return

    groups = groups.sort(groups['bin']).coalesce(2)
    groups.write.csv(out_directory, compression=None, mode='overwrite')


if __name__=='__main__':
    main()
