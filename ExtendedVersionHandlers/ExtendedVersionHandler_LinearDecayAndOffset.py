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


class ExtendedVersionHandler_LinearDecayAndOffset(IExtendedVersionHandler.IExtendedVersionHandler):
    
    def AssembleDisplayHTML(self, inModel):
        x_or_xy = 'x' if inModel.GetDimensionality() == 2 else 'xy'
        if inModel.baseEquationHasGlobalMultiplierOrDivisor_UsedInExtendedVersions:
            return f'{inModel._HTML}<br>{inModel._leftSideHTML} = {inModel._leftSideHTML} / {x_or_xy} + Offset'

        try:
            cd = inModel.GetCoefficientDesignators()
            return f'{inModel._HTML}<br>{inModel._leftSideHTML} = {inModel._leftSideHTML} / ({cd[-2]} * {x_or_xy}) + Offset'

        except:
            return f'{inModel._HTML}<br>{inModel._leftSideHTML} = {inModel._leftSideHTML} / ({x_or_xy}) + Offset'


    def AssembleDisplayName(self, inModel):
        return f'{inModel._baseName} With Linear Decay And Offset'


    def AssembleSourceCodeName(self, inModel):
        return inModel.__module__.split('.')[-1] + '_' + inModel.__class__.__name__ + "_LinearDecayAndOffset"


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
            return inModel.SpecificCodeCPP() + "\ttemp = temp / (" + x_or_xy + ") + Offset;\n"
        cd = inModel.GetCoefficientDesignators()
        return inModel.SpecificCodeCPP() + "\ttemp = temp / ("  + cd[-2] + ' * ' + x_or_xy + ") + Offset;\n"
        

    # overridden from abstract parent class
    def ShouldDataBeRejected(self, inModel):
        
        if inModel.dataCache.independentData1ContainsZeroFlag == True: # cannot divide by zero
            return True
        if inModel.dataCache.independentData2ContainsZeroFlag == True: # cannot divide by zero
            return True

        if (inModel.independentData1CannotContainPositiveFlag == True) and (inModel.dataCache.independentData1ContainsPositiveFlag == True):
            return True
        if (inModel.independentData2CannotContainPositiveFlag == True) and (inModel.dataCache.independentData2ContainsPositiveFlag == True):
            return True
        if (inModel.independentData1CannotContainNegativeFlag == True) and (inModel.dataCache.independentData1ContainsNegativeFlag == True):
            return True
        return (
            inModel.independentData2CannotContainNegativeFlag == True
            and inModel.dataCache.independentData2ContainsNegativeFlag == True
        )


    def GetAdditionalModelPredictions(self, inBaseModelCalculation, inCoeffs, inDataCacheDictionary, inModel):
        if inModel.GetDimensionality() == 2:
            return (
                self.ConvertInfAndNanToLargeNumber(
                    inBaseModelCalculation / inDataCacheDictionary['X']
                    + inCoeffs[len(inCoeffs) - 1]
                )
                if inModel.baseEquationHasGlobalMultiplierOrDivisor_UsedInExtendedVersions
                else self.ConvertInfAndNanToLargeNumber(
                    inBaseModelCalculation
                    / (inCoeffs[len(inCoeffs) - 2] * inDataCacheDictionary['X'])
                    + inCoeffs[len(inCoeffs) - 1]
                )
            )

        if inModel.baseEquationHasGlobalMultiplierOrDivisor_UsedInExtendedVersions:
            return self.ConvertInfAndNanToLargeNumber(inBaseModelCalculation / inDataCacheDictionary['XY'] + inCoeffs[len(inCoeffs)-1])
        else:
            return self.ConvertInfAndNanToLargeNumber(inBaseModelCalculation / (inCoeffs[len(inCoeffs)-2] * inDataCacheDictionary['XY']) + inCoeffs[len(inCoeffs)-1])
    
    

