import sys
from pyspark.sql import SparkSession, functions, types
import re

spark = SparkSession.builder.appName('reddit averages').getOrCreate()

assert sys.version_info >= (3, 4) # make sure we have Python 3.4+
assert spark.version >= '2.1' # make sure we have Spark 2.1+

schema = types.StructType([
	types.StructField('lang', types.StringType(), False),
	types.StructField('title', types.StringType(), False),
	types.StructField('request', types.IntegerType(), False),
	types.StructField('return bytes', types.IntegerType(), False),
])

def getTimeStr(path):
	regex = r"(20\d{2})(\d{2})(\d{2})-(\d{2})"
	match = re.search(regex, path)
	return match.group()

def convertFilenames(df):
	path_to_hour = functions.udf(getTimeStr, returnType=types.StringType())
	return df.withColumn('filename', path_to_hour('filename'))


def main():
	in_directory = sys.argv[1]
	out_directory = sys.argv[2]

	# pagecounts = spark.read.csv(in_directory, schema=schema, sep=' ')
	# pagecounts.show() ; return

	pgcountsfilenames = spark.read.csv(in_directory, schema=schema, sep=' ').withColumn(
										'filename', functions.input_file_name())
	filenamesConverted = convertFilenames(pgcountsfilenames)
	filenamesConverted.show() ; return
	# filenamesConverted.select('filename').show() ; return

	
	
	# averages_by_subreddit.write.csv(out_directory + '-subreddit', mode='overwrite')
	# averages_by_score.write.csv(out_directory + '-score', mode='overwrite')


if __name__=='__main__':
	main()