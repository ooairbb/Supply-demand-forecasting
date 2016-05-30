import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta


class Evaluate:
    def __init__(self):
        self.actualDict = self.loadDict('actual.csv')
        self.predictonDict = self.loadDict('prediction.csv')
        return
    def loadDict(self, filename):
        df = pd.read_csv(filename, header=None)
        res = {}
        for _, row in df.iterrows():
            res[(row[0], row[1])] = row[2]
        return res
    def calFinalResult(self):
        res = []
        for key, value in self.predictonDict.iteritems():
            actual = self.actualDict[key]
            if actual == 0:
                continue
            prediction = value
            temp = (actual - prediction)/float(actual)
            res.append(abs(temp))
        print "final result: {}".format(np.mean(res))
        return np.mean(res)
    def generateTestDate(self):
        startDate = datetime.strptime('2016-01-01', '%Y-%m-%d')
        
        res = []
        for i in range(21):
            deltatime = timedelta(days = i)
            item = (startDate + deltatime).date()
            res.append(str(item))
        return res
    def generateTestSlots(self):
        res = []
        testDates = self.generateTestDate()
        slots = [46,58,70,82,94,106,118,130,142]
        for testDate in testDates:
            for slot in slots:
                res.append(testDate + '-'+ str(slot))
        return res
    def generateTestDistrict(self):
        return [i+ 1 for i in range(66)]
    def generateTestCSV(self):
        testSlots = self.generateTestSlots()
#         testDistricts = self.generateTestDistrict()
        allOderFilePath = '../data/citydata/season_1/training_data/order_data/temp/allorders.csv'
        df = pd.read_csv(allOderFilePath)
        df = df.loc[df['time_slotid'].isin(testSlots)]
        #map 2016-01-22-1 to 2016-01-22-001
        df['timeslotrank'] = df['time_slotid'].map(lambda x: "-".join(x.split('-')[:3] + [x.split('-')[-1].zfill(3)]))
        df = df.sort_values(by = ['timeslotrank','start_district_id'])
        df.to_csv('actual_0.csv', columns=['start_district_id', 'time_slotid', 'missed_request'], header=None, index=None)
        return
    def run(self):
#         self.calFinalResult()
        self.generateTestCSV()
        return
    


if __name__ == "__main__":   
    obj= Evaluate()
    obj.run()