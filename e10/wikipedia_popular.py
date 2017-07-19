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
	# return df.withColumn('filename', path_to_hour('filename'))
	return df.withColumn('filename', path_to_hour('filename'))


def main():
	in_directory = sys.argv[1]
	out_directory = sys.argv[2]
	pgcountsfilenames = spark.read.csv(in_directory, schema=schema, sep=' ').withColumn(
										'filename', functions.input_file_name())
	filenamesConverted = convertFilenames(pgcountsfilenames)
	# filenamesConverted.show() ; return
	
	mainRemoved = filenamesConverted.filter(
					functions.substring(filenamesConverted.title, 1, 9) != 'Main_Page')
	spcRemoved = mainRemoved.filter(
					functions.substring(mainRemoved.title, 1, 8) != 'Special:')
	enOnly = spcRemoved.filter(
					functions.substring(spcRemoved.lang, 1, 2) == 'en')
	# enOnly.show() ; return
	
	grouped = enOnly.groupBy(enOnly['filename'])
	groups = grouped.agg(
		functions.max(enOnly['request'])
		)
	# groups.sort(groups['filename']).show(); return
	groups = groups.cache()

	cond = [(groups['max(request)'] == enOnly['request']), 
			(groups['filename'] == enOnly['filename'])]
	joined_data = groups.join(enOnly, cond).drop(enOnly['filename'])
	joined_dataS = joined_data.sort(joined_data['filename'])
	# joined_dataS.show() ;return

	# joined_dataS = joined_dataS.cache()

	highestCountPerHr = joined_dataS.select(
		joined_dataS['filename'].alias('date'),
		joined_dataS['title'],
		joined_dataS['max(request)'],
	)
	# highestCountPerHr.show() ; return

	highestCountPerHr.write.csv(out_directory, mode='overwrite')


if __name__=='__main__':
	main()