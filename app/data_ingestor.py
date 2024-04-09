"""Parser for input csv"""


import csv

class DataIngestor:
    """Store needed info from csv in a nested dict"""
    def __init__(self, csv_path: str):
        # Read csv from csv_path
        with open(csv_path, 'r', encoding="utf-8") as infile:
            reader = list(csv.reader(infile))
            entries = [[reader[i][4], reader[i][8], float(reader[i][11]), reader[i][30], reader[i][31]]
                       for i in range(1, len(reader))]

            d = {}
            for (_, e) in enumerate(entries):
                state, question, value, strat_category, strat = e
                d.setdefault(question, {}).setdefault(state, {}).setdefault(strat_category, {}).setdefault(strat, []).append(value)

            self.data = d

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]
