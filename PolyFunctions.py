from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

#    pyeq2 is a collection of equations expressed as Python classes
#
#    Copyright (C) 2013 James R. Phillips
#    2548 Vera Cruz Drive
#    Birmingham, AL 35235 USA
#
#    email: zunzun@zunzun.com
#
#    License: BSD-style (see LICENSE.txt in main source directory)

import numpy
numpy.seterr(all= 'ignore')


# duplicated in IExtendedVersionHandler.py
def ConvertInfAndNanToLargeNumber(inArray):
    inArray[numpy.isnan(inArray)] = 1.0E300
    inArray[numpy.isinf(inArray)] = 1.0E300
    return inArray


class PowerTerm(object):

    def __init__(self, variableName, codeName, powerString, logFlag):
        self.power = float(powerString)
        self.logFlag = logFlag

        # data flags
        self.cannotAcceptDataWith_Zero = False
        self.cannotAcceptDataWith_Negative = False
        self.cannotAcceptDataWith_Positive = False
        if self.logFlag:
            self.cannotAcceptDataWith_Zero = True
            self.cannotAcceptDataWith_Negative = True
        if  numpy.modf(self.power)[0]: # fractional power
            self.cannotAcceptDataWith_Negative = True
        if self.power < 0.0:
            self.cannotAcceptDataWith_Zero = True
            self.cannotAcceptDataWith_Negative = True

            # code
        if self.logFlag:
            self.HTML = f'ln({variableName})<sup>{powerString}</sup>'
            self.JAVA = f'Math.pow(Math.log({codeName}), {powerString})'
            self.CPP = f'pow(log({codeName}), {powerString})'
            self.CSHARP = f'Math.Pow(Math.Log({codeName}), {powerString})'
            self.PYTHON = f'math.pow(math.log({codeName}), {powerString})'
            self.SCILAB = f'(log({codeName}) ^ {powerString})'
        else:
            self.HTML = f'{variableName}<sup>{powerString}</sup>'
            self.JAVA = f'Math.pow({codeName}, {powerString})'
            self.CPP = f'pow({codeName}, {powerString})'
            self.CSHARP = f'Math.Pow({codeName}, {powerString})'
            self.PYTHON = f'math.pow({codeName}, {powerString})'
            self.PYTHON = f'math.pow({codeName}, {powerString})'
            self.SCILAB = f'({codeName} ^ {powerString})'

    def value(self, x):
        try:
            if self.logFlag:
                returnValue = numpy.power(numpy.log(x), self.power)
            else:
                returnValue = numpy.power(x, self.power)
            return ConvertInfAndNanToLargeNumber(returnValue)
        except:
            return 1.0E300 * numpy.ones_like(x)



class Offset_Term(object):
    cannotAcceptDataWith_Zero = False
    cannotAcceptDataWith_Negative = False
    cannotAcceptDataWith_Positive = False

    def __init__(self, variableName, codeName):
        self.HTML = 'Offset'
        self.JAVA = 'Offset'
        self.CPP = 'Offset'
        self.CSHARP = 'Offset'
        self.PYTHON = 'Offset'
        self.SCILAB = 'Offset'

    def value(self, x):
        return numpy.ones_like(x)


class ArcTangent_Term(object):
    cannotAcceptDataWith_Zero = False
    cannotAcceptDataWith_Negative = False
    cannotAcceptDataWith_Positive = False

    def __init__(self, variableName, codeName):
        self.HTML = f'atan({variableName})'
        self.JAVA = f'Math.atan({codeName})'
        self.CPP = f'atan({codeName})'
        self.CSHARP = f'Math.Atan({codeName})'
        self.PYTHON = f'math.atan({codeName})'
        self.SCILAB = f'atan({codeName})'

    def value(self, x):
        try:
            returnValue = numpy.arctan(x)
            return ConvertInfAndNanToLargeNumber(returnValue)
        except:
            return 1.0E300 * numpy.ones_like(x)


class HyperbolicCosine_Term(object):
    cannotAcceptDataWith_Zero = False
    cannotAcceptDataWith_Negative = False
    cannotAcceptDataWith_Positive = False

    def __init__(self, variableName, codeName):
        self.HTML = f'cosh({variableName})'
        self.JAVA = f'Math.cosh({codeName})'
        self.CPP = f'cosh({codeName})'
        self.CSHARP = f'Math.Cosh({codeName})'
        self.PYTHON = f'math.cosh({codeName})'
        self.SCILAB = f'cosh({codeName})'

    def value(self, x):
        try:
            returnValue = numpy.cosh(x)
            return ConvertInfAndNanToLargeNumber(returnValue)
        except:
            return 1.0E300 * numpy.ones_like(x)


class VariableUnchanged_Term(object):
    cannotAcceptDataWith_Zero = False
    cannotAcceptDataWith_Negative = False
    cannotAcceptDataWith_Positive = False

    def __init__(self, variableName, codeName):
        self.HTML = variableName
        self.JAVA = codeName
        self.CPP = codeName
        self.CSHARP = codeName
        self.PYTHON = codeName
        self.SCILAB = codeName

    def value(self, x):
        return x


class HyperbolicSine_Term(object):
    cannotAcceptDataWith_Zero = False
    cannotAcceptDataWith_Negative = False
    cannotAcceptDataWith_Positive = False

    def __init__(self, variableName, codeName):
        self.HTML = f'sinh({variableName})'
        self.JAVA = f'Math.sinh({codeName})'
        self.CPP = f'sinh({codeName})'
        self.CSHARP = f'Math.Sinh({codeName})'
        self.PYTHON = f'math.sinh({codeName})'
        self.SCILAB = f'sinh({codeName})'

    def value(self, x):
        try:
            returnValue = numpy.sinh(x)
            return ConvertInfAndNanToLargeNumber(returnValue)
        except:
            return 1.0E300 * numpy.ones_like(x)


class Exponential_VariableUnchanged_Term(object):
    cannotAcceptDataWith_Zero = False
    cannotAcceptDataWith_Negative = False
    cannotAcceptDataWith_Positive = False

    def __init__(self, variableName, codeName):
        self.HTML = f'exp({variableName})'
        self.JAVA = f'Math.exp({codeName})'
        self.CPP = f'exp({codeName})'
        self.CSHARP = f'Math.Exp({codeName})'
        self.PYTHON = f'math.exp({codeName})'
        self.SCILAB = f'exp({codeName})'

    def value(self, x):
        try:
            returnValue = numpy.exp(x)
            return ConvertInfAndNanToLargeNumber(returnValue)
        except:
            return 1.0E300 * numpy.ones_like(x)


class Exponential_VariableTimesNegativeOne_Term(object):
    cannotAcceptDataWith_Zero = False
    cannotAcceptDataWith_Negative = False
    cannotAcceptDataWith_Positive = False

    def __init__(self, variableName, codeName):
        self.HTML = f'exp(-{variableName})'
        self.JAVA = f'Math.exp(-1.0 * {codeName})'
        self.CPP = f'exp(-1.0 * {codeName})'
        self.CSHARP = f'Math.Exp(-1.0 * {codeName})'
        self.PYTHON = f'math.exp(-1.0 * {codeName})'
        self.SCILAB = f'exp(-1.0 * {codeName})'

    def value(self, x):
        try:
            returnValue = numpy.exp(-x)
            return ConvertInfAndNanToLargeNumber(returnValue)
        except:
            return 1.0E300 * numpy.ones_like(x)


class Sine_Term(object):
    cannotAcceptDataWith_Zero = False
    cannotAcceptDataWith_Negative = False
    cannotAcceptDataWith_Positive = False

    def __init__(self, variableName, codeName):
        self.HTML = f'sin({variableName})'
        self.JAVA = f'Math.sin({codeName})'
        self.CPP = f'sin({codeName})'
        self.CSHARP = f'Math.Sin({codeName})'
        self.PYTHON = f'math.sin({codeName})'
        self.SCILAB = f'sin({codeName})'

    def value(self, x):
        try:
            returnValue = numpy.sin(x)
            return ConvertInfAndNanToLargeNumber(returnValue)
        except:
            return 1.0E300 * numpy.ones_like(x)


class Cosine_Term(object):
    cannotAcceptDataWith_Zero = False
    cannotAcceptDataWith_Negative = False
    cannotAcceptDataWith_Positive = False

    def __init__(self, variableName, codeName):
        self.HTML = f'cos({variableName})'
        self.JAVA = f'Math.cos({codeName})'
        self.CPP = f'cos({codeName})'
        self.CSHARP = f'Math.Cos({codeName})'
        self.PYTHON = f'math.cos({codeName})'
        self.SCILAB = f'cos({codeName})'

    def value(self, x):
        try:
            returnValue = numpy.cos(x)
            return ConvertInfAndNanToLargeNumber(returnValue)
        except:
            return 1.0E300 * numpy.ones_like(x)


class Tangent_Term(object):
    cannotAcceptDataWith_Zero = False
    cannotAcceptDataWith_Negative = False
    cannotAcceptDataWith_Positive = False

    def __init__(self, variableName, codeName):
        self.HTML = f'tan({variableName})'
        self.HTML = f'tan({variableName})'
        self.JAVA = f'Math.tan({codeName})'
        self.CPP = f'tan({codeName})'
        self.CSHARP = f'Math.Tan({codeName})'
        self.PYTHON = f'math.tan({codeName})'
        self.SCILAB = f'tan({codeName})'

    def value(self, x):
        try:
            returnValue = numpy.tan(x)
            return ConvertInfAndNanToLargeNumber(returnValue)
        except:
            return 1.0E300 * numpy.ones_like(x)


class HyperbolicTangent_Term(object):
    cannotAcceptDataWith_Zero = False
    cannotAcceptDataWith_Negative = False
    cannotAcceptDataWith_Positive = False

    def __init__(self, variableName, codeName):
        self.HTML = f'tanh({variableName})'
        self.HTML = f'tanh({variableName})'
        self.JAVA = f'Math.tanh({codeName})'
        self.CPP = f'tanh({codeName})'
        self.CSHARP = f'Math.Tanh({codeName})'
        self.PYTHON = f'math.tanh({codeName})'
        self.SCILAB = f'tanh({codeName})'

    def value(self, x):
        try:
            returnValue = numpy.tanh(x)
            return ConvertInfAndNanToLargeNumber(returnValue)
        except:
            return 1.0E300 * numpy.ones_like(x)


class Log_Term(object):
    cannotAcceptDataWith_Zero = True
    cannotAcceptDataWith_Negative = True
    cannotAcceptDataWith_Positive = False

    def __init__(self, variableName, codeName):
        self.HTML = f'ln({variableName})'
        self.JAVA = f'Math.log({codeName})'
        self.CPP = f'log({codeName})'
        self.CSHARP = f'Math.Log({codeName})'
        self.PYTHON = f'math.log({codeName})'
        self.SCILAB = f'log({codeName})'

    def value(self, x):
        try:
            returnValue = numpy.log(x)
            return ConvertInfAndNanToLargeNumber(returnValue)
        except:
            return 1.0E300 * numpy.ones_like(x)


# the order of occurrence in this list is the order of display
def GenerateListForPolyfunctionals_WithParameters(variableName, codeName, dimensionality):
    termList = [Offset_Term(variableName, codeName)]

    termList.append(PowerTerm(variableName, codeName, powerString='0.5', logFlag=False))
    termList.append(VariableUnchanged_Term(variableName, codeName))
    termList.append(PowerTerm(variableName, codeName, powerString='1.5', logFlag=False))
    termList.append(PowerTerm(variableName, codeName, powerString='2', logFlag=False))
    termList.append(PowerTerm(variableName, codeName, powerString='-0.5', logFlag=False))
    termList.append(PowerTerm(variableName, codeName, powerString='-1', logFlag=False))
    termList.append(PowerTerm(variableName, codeName, powerString='-2', logFlag=False))

    termList.append(Log_Term(variableName, codeName))
    termList.append(PowerTerm(variableName, codeName, powerString='2', logFlag=True))
    termList.append(PowerTerm(variableName, codeName, powerString='-1', logFlag=True))
    termList.append(PowerTerm(variableName, codeName, powerString='-2', logFlag=True))

    termList.append(Exponential_VariableUnchanged_Term(variableName, codeName))
    termList.append(Exponential_VariableTimesNegativeOne_Term(variableName, codeName))

    termList.append(Sine_Term(variableName, codeName))
    termList.append(Cosine_Term(variableName, codeName))
    termList.append(Tangent_Term(variableName, codeName))

    # 3D makes an overwhelmimg number of X and Y permutations, only add these for 2D
    if dimensionality == 2:
        termList.append(HyperbolicSine_Term(variableName, codeName))
        termList.append(HyperbolicCosine_Term(variableName, codeName))
        termList.append(ArcTangent_Term(variableName, codeName))
        termList.append(HyperbolicTangent_Term(variableName, codeName))

    return termList
    

def GenerateListForPolyfunctionals_2D():
    return GenerateListForPolyfunctionals_WithParameters('x', 'x_in', 2)
    

def GenerateListForPolyfunctionals_3D_X():
    return GenerateListForPolyfunctionals_WithParameters('x', 'x_in', 3)


def GenerateListForPolyfunctionals_3D_Y():
    return GenerateListForPolyfunctionals_WithParameters('y', 'y_in', 3)


# this list is small due to my available CPU, you can add more to be thorough
def GenerateListForRationals_2D(variableName = 'x', codeName = 'x_in'):
    termList = [Offset_Term(variableName, codeName)]

    termList.append(VariableUnchanged_Term(variableName, codeName))
    termList.append(PowerTerm(variableName, codeName, powerString='-1', logFlag=False))

    termList.append(PowerTerm(variableName, codeName, powerString='2', logFlag=False))
    termList.append(PowerTerm(variableName, codeName, powerString='-2', logFlag=False))

    termList.append(Log_Term(variableName, codeName))
    termList.append(PowerTerm(variableName, codeName, powerString='-1', logFlag=True))

    termList.append(Exponential_VariableUnchanged_Term(variableName, codeName))
    termList.append(Exponential_VariableTimesNegativeOne_Term(variableName, codeName))

    return termList

# the order of occurrence in this list is the order of display
def GenerateListForCustomPolynomials_WithParameters(variableName, codeName):
    return [
        PowerTerm(variableName, codeName, powerString=str(i), logFlag=False)
        for i in range(-8, 9)
    ]


def GenerateListForCustomPolynomials_2D():
    return GenerateListForCustomPolynomials_WithParameters('x', 'x_in')
