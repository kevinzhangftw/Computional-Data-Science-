import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('reddit averages').getOrCreate()

assert sys.version_info >= (3, 4) # make sure we have Python 3.4+
assert spark.version >= '2.1' # make sure we have Spark 2.1+

schema = types.StructType([
    types.StructField('id', types.IntegerType(), False),
    types.StructField('x', types.FloatType(), False),
    types.StructField('y', types.FloatType(), False),
    types.StructField('z', types.FloatType(), False),
])

def main():
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]

    pagecounts = spark.read.json(in_directory)
    pagecounts.show() ; return
    
    # averages_by_subreddit.write.csv(out_directory + '-subreddit', mode='overwrite')
    # averages_by_score.write.csv(out_directory + '-score', mode='overwrite')


if __name__=='__main__':
    main()