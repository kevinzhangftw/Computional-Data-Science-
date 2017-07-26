import sys
from pyspark.sql import SparkSession, functions, types, Row
import re

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



def main():
    in_directory = sys.argv[1]
    # DEBUG
    # somerows = create_row_rdd(in_directory)
    # print('ROW LINES START HERE-----------------------------------', somerows.take(5))
    # print('ROW LINES END HERE-------------------------------------') ; return
    logs = spark.createDataFrame(create_row_rdd(in_directory))

    logs.show() ; return

    # TODO: calculate r.

    r = 0 # TODO: it isn't zero.
    print("r = %g\nr^2 = %g" % (r, r**2))


if __name__=='__main__':
    main()