import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('reddit relative scores').getOrCreate()

assert sys.version_info >= (3, 4) # make sure we have Python 3.4+
assert spark.version >= '2.1' # make sure we have Spark 2.1+

schema = types.StructType([ # commented-out fields won't be read
    #types.StructField('archived', types.BooleanType(), False),
    types.StructField('author', types.StringType(), False),
    #types.StructField('author_flair_css_class', types.StringType(), False),
    #types.StructField('author_flair_text', types.StringType(), False),
    #types.StructField('body', types.StringType(), False),
    #types.StructField('controversiality', types.LongType(), False),
    #types.StructField('created_utc', types.StringType(), False),
    #types.StructField('distinguished', types.StringType(), False),
    #types.StructField('downs', types.LongType(), False),
    #types.StructField('edited', types.StringType(), False),
    #types.StructField('gilded', types.LongType(), False),
    #types.StructField('id', types.StringType(), False),
    #types.StructField('link_id', types.StringType(), False),
    #types.StructField('name', types.StringType(), False),
    #types.StructField('parent_id', types.StringType(), True),
    #types.StructField('retrieved_on', types.LongType(), False),
    types.StructField('score', types.LongType(), False),
    #types.StructField('score_hidden', types.BooleanType(), False),
    types.StructField('subreddit', types.StringType(), False),
    #types.StructField('subreddit_id', types.StringType(), False),
    #types.StructField('ups', types.LongType(), False),
])

def isPositive(x):
    if x > 0:
        return True
    else:
        return False

def calcRelScore(score, avgScore):
    return score/avgScore

def addRelScore(df):
    getRelScore = functions.udf(calcRelScore, returnType=types.FloatType())
    return df.withColumn('rel_score', getRelScore('score', 'avg(score)'))

def main():
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]

    comments = spark.read.json(in_directory, schema=schema)
    
    groupedSubreddit = comments.groupBy(comments['subreddit'])
    averages_by_subreddit = groupedSubreddit.agg(
        functions.avg(comments['score'])
        )
    # averages_by_subreddit.show() ; return

    # checkPositive = functions.udf(isPositive, returnType=types.BooleanType())
    # positiveAvgs = averages_by_subreddit.filter(checkPositive('avg(score)')== True)
    positiveAvgs = averages_by_subreddit.filter(averages_by_subreddit['avg(score)']>0)
    
    #broadcast the small table
    positiveAvgs = functions.broadcast(positiveAvgs)
    
    joinavgs = comments.join(positiveAvgs, on='subreddit')
    joinavgs = joinavgs.cache()
    # joinavgs.show() ; return

    relScoreComments = addRelScore(joinavgs)
    # relScoreComments.show() ; return
    groupedRelSub = relScoreComments.groupBy(relScoreComments['subreddit'])
    group_by_sub_maxRel = groupedRelSub.agg(
        functions.max(relScoreComments['rel_score'])
        )

    # group_by_sub_maxRel.show() ; return
    cond = [(group_by_sub_maxRel['subreddit'] == relScoreComments['subreddit']), 
            (group_by_sub_maxRel['max(rel_score)'] == relScoreComments['rel_score'])]
    
    # broadcast smalle table 
    group_by_sub_maxRel = functions.broadcast(group_by_sub_maxRel)
    
    joinRelAuthor = group_by_sub_maxRel.join(relScoreComments, cond).drop(relScoreComments['subreddit'])
    joinRelAuthor = joinRelAuthor.cache()
    # joinRelAuthor.show() ; return

    best_author = joinRelAuthor.select(
        joinRelAuthor['subreddit'],
        joinRelAuthor['author'],
        joinRelAuthor['rel_score'],
    )

    # best_author.show();return

    best_author.write.json(out_directory, mode='overwrite')

if __name__=='__main__':
    main()