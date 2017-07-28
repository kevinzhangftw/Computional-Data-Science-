import sys
from pyspark.sql import SparkSession, functions, types
# from pyspark.sql.functions import lit
import string, re

spark = SparkSession.builder.appName('first Spark app').getOrCreate()

assert sys.version_info >= (3, 4) # make sure we have Python 3.4+
assert spark.version >= '2.1' # make sure we have Spark 2.1+

wordbreak = r'[%s\s]+' % (re.escape(string.punctuation),)
# regex that matches spaces and/or punctuation

def createWordcountdf(in_directory):
    firstRead = spark.read.text(in_directory)
    secondRead = firstRead.select(
                    functions.split(firstRead[0], wordbreak).alias('words')
                )
    thirdRead = secondRead.select(
                    functions.explode(secondRead.words)
                )
    fourthRead = thirdRead.select(
                    functions.lower(thirdRead[0])
                )
    return fourthRead

def main():
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]

    read = createWordcountdf(in_directory) #split, explode, and lowercase

    #filter blank lines
    read = read.filter(read[0] != '')
    # count the words
    group = read.groupBy(read[0])
    wordCount = group.agg(functions.count(read[0]))
    
    #order the words
    wordCount = wordCount.orderBy('count(lower(col))', ascending=False)
    #rename the columns
    wordCount = wordCount.select(
        wordCount[0].alias('word'),
        wordCount[1].alias('count'),
        )
    # wordCount.show() ; return

    wordCount.write.csv(out_directory, compression=None, mode='overwrite')


if __name__=='__main__':
    main()
