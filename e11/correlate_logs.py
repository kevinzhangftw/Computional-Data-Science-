import sys
from pyspark.sql import SparkSession, functions, types, Row
from pyspark.sql.functions import lit
import re
import math

spark = SparkSession.builder.appName('correlate logs').getOrCreate()

assert sys.version_info >= (3, 4) # make sure we have Python 3.4+
assert spark.version >= '2.1' # make sure we have Spark 2.1+

line_re = re.compile("^(\\S+) - - \\[\\S+ [+-]\\d+\\] \"[A-Z]+ \\S+ HTTP/\\d\\.\\d\" \\d+ (\\d+)$")


def line_to_row(line):
    """
    Take a logfile line and return a Row object with hostname and bytes transferred. Return None if regex doesn't match.
    """
    m = line_re.match(line)
    if m:
        return m.group(1), m.group(2)
    else:
        return None

def not_none(row):
    """
    Is this None? Hint: .filter() with it.
    """
    return row is not None


def create_row_rdd(in_directory):
    log_lines = spark.sparkContext.textFile(in_directory)
    # DEBUG
    # print('LOG LINES START HERE-----------------------------------',log_lines.take(2))
    # print('LOG LINES END HERE-------------------------------------------------------')
    # TODO: return an RDD of Row() objects
    return log_lines.map(line_to_row).filter(not_none)

def calcCoef(ones, x, x2, y, y2, xy):
    nxy = ones * xy
    sumXsumY = x * y
    nxysumXsumY = nxy - sumXsumY

    nx2 = ones * x2
    xExp = x ** 2
    sqnx2xExp = math.sqrt(nx2 - xExp)

        ny2 = ones * y2
        yExp = y ** 2
        sqny2yExp = math.sqrt(ny2 - yExp)

    r = nxysumXsumY / (sqnx2xExp * sqny2yExp)

    return r

def main():
    in_directory = sys.argv[1]
    logs = spark.createDataFrame(create_row_rdd(in_directory))
    # logs.show() ; return
    # _1 is hostname
    hostGroup = logs.groupBy(logs['_1'])
    hostData = hostGroup.agg(
                functions.count(logs['_1']).alias('x'),
                functions.sum(logs['_2']).alias('y')
            )
    # hostData = hostData.withColumn("ones", lit(1))
    hostData = hostData.withColumn("x^2", hostData['x']**2)
    hostData = hostData.withColumn("y^2", hostData['y']**2)
    hostData = hostData.withColumn("x*y", hostData['x']*hostData['y'])
    # reordering the columns
    # hostData = hostData.select(
    #     # hostData['ones'],
    #     hostData['x'],
    #     hostData['x^2'],
    #     hostData['y'],
    #     hostData['y^2'],
    #     hostData['x*y'],
    # )
    # hostData.show() ; return
    
    hostDataGroup = hostData.groupBy()
    # hostDataGroup.sum().show() ; return
    ones= hostData.count()
    # ones= hostDataGroup.sum().first()[0]
    x   = hostDataGroup.sum().first()[0]
    x2  = hostDataGroup.sum().first()[2]
    y   = hostDataGroup.sum().first()[1]
    y2  = hostDataGroup.sum().first()[3]
    xy  = hostDataGroup.sum().first()[4]


    r = calcCoef(ones, x, x2, y, y2, xy)
    print("r = %g\nr^2 = %g" % (r, r**2))


if __name__=='__main__':
    main()