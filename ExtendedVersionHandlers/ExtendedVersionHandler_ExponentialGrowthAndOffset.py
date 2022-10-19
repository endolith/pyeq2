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

import pyeq2
from . import IExtendedVersionHandler

import numpy
numpy.seterr(all= 'ignore')


class ExtendedVersionHandler_ExponentialGrowthAndOffset(IExtendedVersionHandler.IExtendedVersionHandler):
    
    def AssembleDisplayHTML(self, inModel):
        x_or_xy = 'x' if inModel.GetDimensionality() == 2 else 'xy'
        if inModel.baseEquationHasGlobalMultiplierOrDivisor_UsedInExtendedVersions:
            return f'{inModel._HTML}<br>{inModel._leftSideHTML} = {inModel._leftSideHTML} * exp({x_or_xy}) + Offset'

        try:
            cd = inModel.GetCoefficientDesignators()
            return f'{inModel._HTML}<br>{inModel._leftSideHTML} = {inModel._leftSideHTML} * ({cd[-2]} * exp({x_or_xy})) + Offset'

        except:
            return f'{inModel._HTML}<br>{inModel._leftSideHTML} = {inModel._leftSideHTML} * (exp({x_or_xy})) + Offset'


    def AssembleDisplayName(self, inModel):
        return f'{inModel._baseName} With Exponential Growth And Offset'


    def AssembleSourceCodeName(self, inModel):
        return inModel.__module__.split('.')[-1] + '_' + inModel.__class__.__name__ + "_ExponentialGrowthAndOffset"


    def AssembleCoefficientDesignators(self, inModel):
        if inModel.baseEquationHasGlobalMultiplierOrDivisor_UsedInExtendedVersions:
            return inModel._coefficientDesignators + ['Offset']
        else:
            return inModel._coefficientDesignators + [inModel.listOfAdditionalCoefficientDesignators[len(inModel._coefficientDesignators)], 'Offset']


    # overridden from abstract parent class
    def AppendAdditionalCoefficientBounds(self, inModel):
        if inModel.baseEquationHasGlobalMultiplierOrDivisor_UsedInExtendedVersions:
            if inModel.upperCoefficientBounds != []:
                inModel.upperCoefficientBounds.append(None)
            if inModel.lowerCoefficientBounds != []:
                inModel.lowerCoefficientBounds.append(None)
        else:
            if inModel.upperCoefficientBounds != []:
                inModel.upperCoefficientBounds.append(None)
                inModel.upperCoefficientBounds.append(None)
            if inModel.lowerCoefficientBounds != []:
                inModel.lowerCoefficientBounds.append(None)
                inModel.lowerCoefficientBounds.append(None)


    def AssembleOutputSourceCodeCPP(self, inModel):
        x_or_xy = 'x_in' if inModel.GetDimensionality() == 2 else 'x_in * y_in'
        if inModel.baseEquationHasGlobalMultiplierOrDivisor_UsedInExtendedVersions:
            return inModel.SpecificCodeCPP() + "\ttemp = temp * exp(" + x_or_xy + ") + Offset;\n"
        cd = inModel.GetCoefficientDesignators()
        return inModel.SpecificCodeCPP() + "\ttemp = temp * ("  + cd[-2] + ' * exp(' + x_or_xy + ")) + Offset;\n"
        

    def GetAdditionalDataCacheFunctions(self, inModel, inDataCacheFunctions):
        foundX = False
        foundXY = False
        for i in inDataCacheFunctions: # if these are already in the cache, we don't need to add them again
            if i[0] == 'ExpX' and inModel.GetDimensionality() == 2:
                foundX = True
            if i[0] == 'ExpXY' and inModel.GetDimensionality() == 3:
                foundXY = True

        if inModel.GetDimensionality() == 2:
            if not foundX:
                return inDataCacheFunctions + \
                           [[pyeq2.DataCache.DataCacheFunctions.ExpX(NameOrValueFlag=1), []]]
        elif not foundXY:
            return inDataCacheFunctions + \
                       [[pyeq2.DataCache.DataCacheFunctions.ExpXY(NameOrValueFlag=1), []]]
        return inDataCacheFunctions


    def GetAdditionalModelPredictions(self, inBaseModelCalculation, inCoeffs, inDataCacheDictionary, inModel):
        if inModel.GetDimensionality() == 2:
            return (
                self.ConvertInfAndNanToLargeNumber(
                    inBaseModelCalculation * inDataCacheDictionary['ExpX']
                    + inCoeffs[len(inCoeffs) - 1]
                )
                if inModel.baseEquationHasGlobalMultiplierOrDivisor_UsedInExtendedVersions
                else self.ConvertInfAndNanToLargeNumber(
                    inBaseModelCalculation
                    * (inCoeffs[len(inCoeffs) - 2] * inDataCacheDictionary['ExpX'])
                    + inCoeffs[len(inCoeffs) - 1]
                )
            )

        if inModel.baseEquationHasGlobalMultiplierOrDivisor_UsedInExtendedVersions:
            return self.ConvertInfAndNanToLargeNumber(inBaseModelCalculation * inDataCacheDictionary['ExpXY'] + inCoeffs[len(inCoeffs)-1])
        else:
            return self.ConvertInfAndNanToLargeNumber(inBaseModelCalculation * (inCoeffs[len(inCoeffs)-2] * inDataCacheDictionary['ExpXY']) + inCoeffs[len(inCoeffs)-1])
