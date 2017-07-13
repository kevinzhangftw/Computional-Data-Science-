import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('weather ETL').getOrCreate()

assert sys.version_info >= (3, 4) # make sure we have Python 3.4+
assert spark.version >= '2.1' # make sure we have Spark 2.1+

observation_schema = types.StructType([
    types.StructField('station', types.StringType(), False),
    types.StructField('date', types.StringType(), False),
    types.StructField('observation', types.StringType(), False),
    types.StructField('value', types.IntegerType(), False),
    types.StructField('mflag', types.StringType(), False),
    types.StructField('qflag', types.StringType(), False),
    types.StructField('sflag', types.StringType(), False),
    types.StructField('obstime', types.StringType(), False),
])


def main():
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]

    weather = spark.read.csv(in_directory, schema=observation_schema)
    # weather.show(); return   
    qflagNull = weather.filter(weather['qflag'].isNull())
    # qflagNull.show(); return
    caStation = qflagNull.filter(functions.substring(qflagNull.station, 1, 2) == 'CA')
    # caStation.show(); return
    tmaxObserv = caStation.filter(functions.substring(caStation.observation, 1, 4) == 'TMAX')
    # tmaxObserv.show(); return

    cleaned_data = tmaxObserv.select(
        tmaxObserv['station'],
        tmaxObserv['date'],
        (tmaxObserv['value'] / 10).alias('TMAX')
    )
    # cleaned_data.show()

    cleaned_data.write.json(out_directory, compression='gzip', mode='overwrite')


if __name__=='__main__':
    main()