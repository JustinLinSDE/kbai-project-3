# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image
import numpy as np

from ProblemSet import ProblemSet


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.

    def Solve(self, problem):

        result = self.loadChoices(problem)
        question = result[0]
        choices = result[1]

        if problem.problemType == "2x2":

            # AB DPR
            dprAB = self.calculateDPR(question.get('A'), question.get('B'))
            iprAB = self.interPixelRatio(question.get('A'),question.get('B'))

            score = {}
            for key in choices.keys():
                value = self.calculateScore(question.get('C'),choices.get(key),dprAB,iprAB)
                score.update({key: value})
            scoreValue = list(score.values())
            scoreKey = list(score.keys())
            return int(scoreKey[scoreValue.index(min(scoreValue))])
        elif problem.problemType == "3x3":
            #horizontal DPR
            dprAB = self.calculateDPR(question.get('A'), question.get('B'))
            dprBC = self.calculateDPR(question.get('B'), question.get('C'))
            dprDE = self.calculateDPR(question.get('D'), question.get('E'))
            dprEF = self.calculateDPR(question.get('E'), question.get('F'))
            dprGH = self.calculateDPR(question.get('G'), question.get('H'))

            #vertical DPR
            dprAD = self.calculateDPR(question.get('A'), question.get('D'))
            dprDG = self.calculateDPR(question.get('D'), question.get('G'))
            dprBE = self.calculateDPR(question.get('B'), question.get('E'))
            dprEH = self.calculateDPR(question.get('E'), question.get('H'))
            dprCF = self.calculateDPR(question.get('C'), question.get('F'))


            #horizontal DPR
            rmsABC_DPR = np.math.sqrt((dprAB - dprBC)**2 / 2.0)
            rmsDEF_DPR = np.math.sqrt((dprDE - dprEF)**2 / 2.0)

            #vertical DPR
            rmsADG_DPR = np.math.sqrt((dprAD -dprDG)**2 / 2.0)
            rmsBEH_DPR = np.math.sqrt((dprBE - dprEH)**2 / 2.0)

            #horizontal IPR
            iprAB = self.interPixelRatio(question.get('A'), question.get('B'))
            iprBC = self.interPixelRatio(question.get('B'), question.get('C'))
            iprDE = self.interPixelRatio(question.get('D'), question.get('E'))
            iprEF = self.interPixelRatio(question.get('E'), question.get('F'))
            iprGH = self.interPixelRatio(question.get('G'), question.get('H'))

            #vertical IPR
            iprAD = self.interPixelRatio(question.get('A'), question.get('D'))
            iprDG = self.interPixelRatio(question.get('D'), question.get('G'))
            iprBE = self.interPixelRatio(question.get('B'), question.get('E'))
            iprEH = self.interPixelRatio(question.get('E'), question.get('H'))
            iprCF = self.interPixelRatio(question.get('C'), question.get('F'))

            # horizontal IPR
            rmsABC_IPR = np.math.sqrt((iprAB - iprBC) ** 2 / 2.0)
            rmsDEF_IPR = np.math.sqrt((iprDE - iprEF) ** 2 / 2.0)

            # vertical IPR
            rmsADG_IPR = np.math.sqrt((iprAD - iprDG) ** 2 / 2.0)
            rmsBEH_IPR = np.math.sqrt((iprBE - iprEH) ** 2 / 2.0)


            score = {}
            for key in choices.keys():

                horizontalValueDPR = self.calculateRMS(rmsABC_DPR, rmsDEF_DPR, dprGH, question.get('H'), choices.get(key))
                verticalValueDPR = self.calculateRMS(rmsADG_DPR, rmsBEH_DPR, dprCF, question.get('F'), choices.get(key))

                horizontalValueIPR = self.calculateRMS(rmsABC_IPR, rmsDEF_IPR, iprGH, question.get('H'), choices.get(key))
                verticalValueIPR = self.calculateRMS(rmsADG_IPR, rmsBEH_IPR, iprCF, question.get('F'), choices.get(key))

                value = 0.9 * (horizontalValueDPR + verticalValueDPR) + 0.1 * (horizontalValueIPR + verticalValueIPR)
                score.update({key: value})
            scoreValue = list(score.values())
            scoreKey = list(score.keys())
            print(int(scoreKey[scoreValue.index(min(scoreValue))]))
            return int(scoreKey[scoreValue.index(min(scoreValue))])
        else:
            return -1

    def calculateRMS (self, rmsOne, rmsTwo, neighborDPR, neighbor, choice):
        currentDPR = self.calculateDPR(neighbor, choice)
        rmsChoice = np.math.sqrt((neighborDPR - currentDPR)**2 / 2.0)
        firstTwo = rmsOne - rmsTwo
        lastTwo =  rmsTwo - rmsChoice
        rms = np.math.sqrt((firstTwo - lastTwo)**2 / 2.0)
        return rms

    def calculateScore (self, imageQuestion, imageChoice, tagetDPR, targetIPR):
        currentDPR = self.calculateDPR(imageQuestion, imageChoice)
        currentIPR = self.interPixelRatio(imageQuestion, imageChoice)
        dprDistance = abs(currentDPR - tagetDPR)
        iprDistance = abs(currentIPR - targetIPR)
        score = 0.9 * dprDistance + 0.1 * iprDistance
        return score

    def calculateDPR (self, image1, image2):
        npMatrix1 = self.blackWhite(image1)
        npMatrix2 = self.blackWhite(image2)
        ratio1 = self.blackPixelRatio(npMatrix1)
        ratio2 = self.blackPixelRatio(npMatrix2)
        return ratio1 - ratio2

    def loadChoices(self, problem):
        result = []
        choicesMap = {}
        questionMap = {}
        for element in problem.figures:

            # print(element)
            # print(type(element))
            if element.isdigit():
                choicesMap.update({element: Image.open(problem.figures[element].visualFilename)})
            else:
                questionMap.update({element: Image.open(problem.figures[element].visualFilename)})
        result.append(questionMap)
        result.append(choicesMap)
        return result

    def blackWhite(self, image):
        row = image.size[0]
        column = image.size[1]
        blackWhiteMatrix = np.ones((image.size[0], image.size[1]), dtype=bool)
        # print(row)
        # print(column)
        pixelMatrix = image.load()
        whiteColor = (255,255,255,255)
        for i in range(blackWhiteMatrix.shape[0]):
            for j in range(blackWhiteMatrix.shape[0]):
                if (pixelMatrix[i, j] == whiteColor):
                    blackWhiteMatrix[i, j] = False
        return blackWhiteMatrix


    def blackPixelRatio(self, npMatrix):
        black = np.count_nonzero(npMatrix)
        ratio = float (black)/(npMatrix.shape[0] * npMatrix.shape[1])
        return ratio

    def interPixelRatio(self, image1, image2):
        row = image1.size[0]
        column = image1.size[1]
        pixelMatrix1 = image1.load()
        pixelMatrix2 = image2.load()
        whiteColor = (255, 255, 255, 255)
        sameBlackNum = 0.0;
        totalBlackNum = 0.0;
        for i in range(row):
            for j in range(column):
                if (pixelMatrix1[i, j] != whiteColor or pixelMatrix2[i, j] != whiteColor):
                    totalBlackNum += 1
                if (pixelMatrix1[i, j] != whiteColor and pixelMatrix2[i, j] != whiteColor):
                    sameBlackNum += 1
        if totalBlackNum != 0:
            return sameBlackNum/totalBlackNum
        else:
            return 0


if __name__ == "__main__":
    problems =  ProblemSet('Basic Problems C')
    #problems = problems.loadProble.loadProblem
    for element in problems.problems:
        # if (element.name == 'Basic Problem C-03'):
            agent = Agent()
            agent.Solve(element)



