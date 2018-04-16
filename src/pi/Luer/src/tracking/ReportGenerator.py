import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error
from math import sqrt
import os
import csv
'''
ReportGenerator
    INPUT:
        - path to true data
        - path to calculated data

    OUTPUT:
        - plots
        - Results.txt with error results and header

    TO-DO
    1. Generate plots
    2. Calculate errors
    3. Output plots and errors to a project report folder

'''
def getDist(pt1,pt2):
    x1,y1 = pt1
    x2,y2 = pt2
    return sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

class ReportGenerator(object):
    def __init__(self,videoPath,truePath,testPath,timingPath,keypointFinder,featureMatcher):
        self.truePath = truePath
        self.testPath = testPath
        self.timingPath = timingPath
        self.videoPath = videoPath.split('.')[0]
        self.trueData = []
        self.testData = []
        self.timingData = []
        self.keypointFinder = keypointFinder
        self.featureMatcher = featureMatcher
        self.reportPath = ensure_dir("reports/" + self.videoPath + self.keypointFinder + self.featureMatcher)



    def calculateErrors(self):
        # Generate and write to results in resultsFile
        true = []
        test = []
        timing = []

        # Read true data
        with open(self.truePath,'r') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for x,y in readCSV:
                x = int(x)
                y = int(y)
                true.append([x,y])

        # Read test data
        with open(self.testPath,'r') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for x,y in readCSV:
                x = float(x)
                y = float(y)
                test.append([x,y])

        # Trim first data points to have equal sized
        self.trueData = true[2:]
        self.testData = test

        dist = []
        y_actual = [0 for i in range(len(self.trueData))]

        # Calculate Euclidian Distance between points
        for i in range(len(self.trueData)):
            dist.append(getDist(self.trueData[i],self.testData[i]))

        rms = (sqrt(mean_squared_error(y_actual, dist)))
        mea = mean_absolute_error(y_actual,dist)

        sampling = []
        matching = []
        tracking = []
        frames = []
        frameNumber = 1
        with open(self.timingPath,'r') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for sample,match,track in readCSV:
                sampling.append(float(sample))
                matching.append(float(match))
                tracking.append(float(track))
                # print(type(float(sample)))
                frames.append(frameNumber)
                frameNumber += 1


        plt.scatter(frames, sampling, s=10, c='b', marker="o", label=self.keypointFinder)
        plt.scatter(frames, matching, s=10, c='r', marker="o", label=self.featureMatcher)
        plt.scatter(frames, tracking, s=10, c='g', marker="o", label='tracking')
        plt.xlabel("Frame Number")
        plt.ylabel("Time Taken")
        plt.legend(loc='upper left')
        plt.xlim(xmin=0)
        plt.ylim(ymin=0)
        plt.savefig(self.reportPath+"/timingVsFrame.png")

        resultsString = "Performance Results for " + self.videoPath + ".mp4/.avi" + ":\n"
        resultsString += "Keypoint Finding Method: " + self.keypointFinder + "\n"
        resultsString += "Feature Matching Method: " + self.featureMatcher + "\n"
        # resultsString += "Average FPS: " + str(avgFPS) + "\n"
        resultsString += "Root mean square Error: " + str(rms) + " \n"
        resultsString += "Mean Absolute Error: " + str(mea) + " \n"

        resultsFile = open(self.reportPath + "/results.txt", "w")
        resultsFile.write(resultsString)
        resultsFile.close()
        print("results written to " + self.reportPath + "/results.txt")


    def generateReport(self):
        # generatePlots()
        print("GENERATING REPORT")
        calculateErrors()
