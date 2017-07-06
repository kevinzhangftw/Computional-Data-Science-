import pandas as pd
import sys
import gzip
from math import radians, cos, sin, asin, sqrt
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

OUTPUT_TEMPLATE = (
    "Initial (invalid) T-test p-value: {initial_ttest_p:.3g}\n"
    "Original data normality p-values: {initial_weekday_normality_p:.3g} {initial_weekend_normality_p:.3g}\n"
    "Original data equal-variance p-value: {initial_levene_p:.3g}\n"
    "Transformed data normality p-values: {transformed_weekday_normality_p:.3g} {transformed_weekend_normality_p:.3g}\n"
    "Transformed data equal-variance p-value: {transformed_levene_p:.3g}\n"
    "Weekly data normality p-values: {weekly_weekday_normality_p:.3g} {weekly_weekend_normality_p:.3g}\n"
    "Weekly data equal-variance p-value: {weekly_levene_p:.3g}\n"
    "Weekly T-test p-value: {weekly_ttest_p:.3g}\n"
    "Mann–Whitney U-test p-value: {utest_p:.3g}"
)


reddit_counts_json_compressed = sys.argv[1]
reddit_counts_json = gzip.open(reddit_counts_json_compressed, 'rt', encoding='utf-8')
reddit_counts = pd.read_json(reddit_counts_json, lines=True)

filterYears = reddit_counts[
    reddit_counts.apply(lambda x:
                        (x.date.year==2012 or x.date.year==2013) and
                        x.subreddit=='canada'
                        , axis=1)]
weekends= filterYears[filterYears.date.apply(lambda x: x.weekday() >= 5)]
weekdays= filterYears[filterYears.date.apply(lambda x: x.weekday() < 5)]

ittest = stats.ttest_ind(weekends['comment_count'], weekdays['comment_count'])
iweekendn = stats.normaltest(weekends['comment_count']).pvalue
iweekdayn = stats.normaltest(weekdays['comment_count']).pvalue
ilevene = stats.levene(weekends['comment_count'], weekdays['comment_count']).pvalue
nuweekends = np.sqrt(weekends['comment_count'])
tweekendn = stats.normaltest(nuweekends).pvalue
nuweekdays = np.sqrt(weekdays['comment_count'])
tweekdayn=stats.normaltest(nuweekdays).pvalue
tlevene=stats.levene(nuweekends, nuweekdays).pvalue

weekends['year']= weekends.apply(lambda x: x.date.year, axis=1)
weekends['weekofyear']= weekends.apply(lambda x: x.date.weekofyear, axis=1)
weekendsMean = weekends.groupby(['year', 'weekofyear']).mean()
wweekendn=stats.normaltest(weekendsMean['comment_count']).pvalue

weekdays['year']= weekdays.apply(lambda x: x.date.year, axis=1)
weekdays['weekofyear']= weekdays.apply(lambda x: x.date.weekofyear, axis=1)
weekdaysMean = weekdays.groupby(['year', 'weekofyear']).mean()
wweekdayn=stats.normaltest(weekdaysMean['comment_count']).pvalue

wlevene= stats.levene(weekdaysMean['comment_count'], weekendsMean['comment_count']).pvalue
wttest= stats.ttest_ind(weekendsMean['comment_count'], weekdaysMean['comment_count'])
utest = stats.mannwhitneyu(weekends['comment_count'], weekdays['comment_count'])





print(OUTPUT_TEMPLATE.format(
        initial_ttest_p=ittest.pvalue,
        initial_weekday_normality_p=iweekdayn,
        initial_weekend_normality_p=iweekendn,
        initial_levene_p=ilevene,
        transformed_weekday_normality_p=tweekdayn,
        transformed_weekend_normality_p=tweekendn,
        transformed_levene_p=tlevene,
        weekly_weekday_normality_p=wweekdayn,
        weekly_weekend_normality_p=wweekendn,
        weekly_levene_p=wlevene,
        weekly_ttest_p=wttest.pvalue,
        utest_p=utest.pvalue,
        )
	)



