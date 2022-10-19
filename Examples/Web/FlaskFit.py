import os, sys, inspect

# ensure pyeq2 can be imported
if sys.path[0].find('pyeq2-master') != -1:raise Exception('Please rename git checkout directory from "pyeq2-master" to "pyeq2"')
exampleFileDirectory = sys.path[0][:sys.path[0].rfind(os.sep)]
pyeq2ImportDirectory =  os.path.join(os.path.join(exampleFileDirectory, '..'), '..')
if pyeq2ImportDirectory not in sys.path:
    sys.path.append(pyeq2ImportDirectory)

import pyeq2, GraphUtils, TextUtils
from flask import Flask
from flask import request


# override Flask's default file cache for the files we generate
class MyFlask(Flask):
    def get_send_file_max_age(self, name):
        if name.lower().endswith('.png'):
            return 0.000001
        if name.lower().endswith('.txt'):
            return 0.000001
        if name.lower().endswith('.html'):
            return 0.000001
        return Flask.get_send_file_max_age(self, name)


app = MyFlask(__name__)
app.debug = True # only for development, never for production


@app.route('/')
def test_curve_fiting_and_plotting():

    # HTML for 2D fitter form
    htmlToReturn_2Dform = '''
<table border=1 cellpadding=20>
<tr><td><b>Example 2D f(x) Web Fitter</b></td></tr>
<tr><td>
<form action="/simplefitter_2D" method="post" target=_blank>
--- 2D Text Data ---<br>
<textarea  rows="10" cols="45" name="textdata" wrap=off>
Example 2D data for testing
  X        Y
5.357    10.376
5.457    10.489
5.936    11.049
6.161    11.327 ending text is ignored
6.697    12.054
8.442    14.744
9.769    17.068
9.861    17.104

</textarea>
<br><br>
    --- Example 2D Equations ---<br>
<input type="radio" name="equation" value="Linear" checked>Linear Polynomial<br>
<input type="radio" name="equation" value="Quadratic">Quadratic Polynomial<br>
<input type="radio" name="equation" value="Cubic">Cubic Polynomial<br>
<input type="radio" name="equation" value="WitchA">Witch Of Maria Agnesi A<br>
<input type="radio" name="equation" value="VanDeemter">VanDeemter Chromatography<br>
<input type="radio" name="equation" value="GammaRayDegreesB">Gamma Ray Angular Distribution (degrees) B<br>
<input type="radio" name="equation" value="ExponentialWithOffset">Exponential With Offset<br>
<br>
<table><tr>
<td>
<input type="submit" value="Submit">
</td>
<td align="left">
<input type="radio" name="target" value="SSQABS" checked>Lowest Sum Of Squared Absolute Error<br>
<input type="radio" name="target" value="LNQREL">Lowest Sum Of Squared Log[Pred/Actual]<br>
<input type="radio" name="target" value="SSQREL">Lowest Sum Of Squared Relative Error<br>
<input type="radio" name="target" value="ODR">Lowest Sum Of Squared Orthogonal Distance<br>
</td>
</tr></table>
</form>
<br><br>
<a href="/equationlist_2D">Link to all standard 2D equations</a>
</td></tr></table>
'''



    # HTML for 3D fitter form
    htmlToReturn_3Dform = '''
<table border=1 cellpadding=20>
<tr><td><b>Example 3D f(x,y) Web Fitter</b></td></tr>
<tr><td>
<form action="/simplefitter_3D" method="post" target=_blank>
--- 3D Text Data ---<br>
<textarea  rows="10" cols="45" name="textdata" wrap=off>
Example 3D data for testing
    X      Y       Z
  3.017  2.175   0.0320
  2.822  2.624   0.0629
  1.784  3.144   6.570
  1.712  3.153   6.721
  2.972  2.106   0.0313
  2.719  2.542   0.0643
  2.0 2.6 4.0  ending text is ignored
  1.479  2.957   6.583
  1.387  2.963   6.744
  2.843  1.984   0.0315
  2.485  2.320   0.0639
  0.742  2.568   6.581
  0.607  2.571   6.753
</textarea>
<br><br>
    --- Example 3D Equations ---<br>
<input type="radio" name="equation" value="Linear" checked>Linear Polynomial<br>
<input type="radio" name="equation" value="FullQuadratic">Full Quadratic Polynomial<br>
<input type="radio" name="equation" value="FullCubic">Full Cubic Polynomial<br>
<input type="radio" name="equation" value="MonkeySaddleA">Monkey Saddle A<br>
<input type="radio" name="equation" value="GaussianCurvatureOfWhitneysUmbrellaA">Gaussian Curvature Of Whitneys Umbrella A<br>
<input type="radio" name="equation" value="NIST_NelsonAutolog">NIST Nelson Autolog<br>
<input type="radio" name="equation" value="CustomPolynomialOne">Custom Polynomial One<br>
<br>

<table><tr>
<td>
<input type="submit" value="Submit">
</td>
<td align="left">
<input type="radio" name="target" value="SSQABS" checked>Lowest Sum Of Squared Absolute Error<br>
<input type="radio" name="target" value="LNQREL">Lowest Sum Of Squared Log[Pred/Actual]<br>
<input type="radio" name="target" value="SSQREL">Lowest Sum Of Squared Relative Error<br>
<input type="radio" name="target" value="ODR">Lowest Sum Of Squared Orthogonal Distance<br>
</td>
</tr></table>
</form>

<br><br>

<a href="/equationlist_3D">Link to all standard 3D equations</a>
</td></tr></table>
'''

    s = '<html><body>' + '<table><tr>'
    s += f'<td>{htmlToReturn_2Dform}</td>'
    s += '<td> </td>'
    s += f'<td>{htmlToReturn_3Dform}</td>'
    s += '</tr></table>'
    s +='</body></html>'

    return s



@app.route('/simplefitter_2D', methods=['POST'])
def simplefitter_2D_NoFormDataValidation():
    formTextData = request.form['textdata']
    formEquation = request.form['equation']
    formFittingTarget = request.form['target']

    if formEquation == 'Cubic':
        equation = pyeq2.Models_2D.Polynomial.Cubic(formFittingTarget)
    elif formEquation == 'ExponentialWithOffset':
        equation = pyeq2.Models_2D.Exponential.Exponential(formFittingTarget, 'Offset')

    elif formEquation == 'GammaRayDegreesB':
        equation = pyeq2.Models_2D.LegendrePolynomial.GammaRayAngularDistributionDegreesB(formFittingTarget)
    elif formEquation == 'Linear':
        equation = pyeq2.Models_2D.Polynomial.Linear(formFittingTarget)
    elif formEquation == 'Quadratic':
        equation = pyeq2.Models_2D.Polynomial.Quadratic(formFittingTarget)
    elif formEquation == 'VanDeemter':
        equation = pyeq2.Models_2D.Engineering.VanDeemterChromatography(formFittingTarget)
    elif formEquation == 'WitchA':
        equation = pyeq2.Models_2D.Miscellaneous.WitchOfAgnesiA(formFittingTarget)
    # the name of the data here is from the form
    # check for functions requiring non-zero nor non-negative data such as 1/x, etc.
    try:
        pyeq2.dataConvertorService().ConvertAndSortColumnarASCII(formTextData, equation, False)
    except:
        return equation.reasonWhyDataRejected

    # check for number of coefficients > number of data points to be fitted
    coeffCount = len(equation.GetCoefficientDesignators())
    dataCount = len(equation.dataCache.allDataCacheDictionary['DependentData'])
    if coeffCount > dataCount:
        return f"This equation requires a minimum of {repr(coeffCount)} data points, you supplied {repr(dataCount)}."


    equation.Solve()
    equation.CalculateModelErrors(equation.solvedCoefficients, equation.dataCache.allDataCacheDictionary)
    equation.CalculateCoefficientAndFitStatistics()

    # save fit statistics to a text file
    fitStatisticsFilePath = "static/fitstatistics_2D.txt" # simplefitter_2D
    TextUtils.SaveCoefficientAndFitStatistics(fitStatisticsFilePath,  equation)

    # save source code to a single text file, all available languages
    sourceCodeFilePath = "static/sourcecode_2D.html" # simplefitter_2D
    TextUtils.SaveSourceCode(sourceCodeFilePath,  equation)

    # create graph
    graphFilePath = "static/model_and_scatterplot_2D.png" # simplefitter_2D
    title = "Example Of An HTML FORM Model"
    xAxisLabel = "X data"
    yAxisLabel = "Y data"
    GraphUtils.SaveModelScatterConfidence(graphFilePath,
                                          equation, title, xAxisLabel, yAxisLabel) 

    absErrorPlotFilePath = "static/abs_error_2D.png" # simplefitter_2D
    title = "Absolute Error For An HTML FORM Model"
    GraphUtils.SaveAbsErrorScatterPlot(absErrorPlotFilePath, equation, title, yAxisLabel)

    absErrorHistFilePath = "static/abs_error_hist_2D.png" # simplefitter_2D
    title = "Absolute Error"
    GraphUtils.SaveDataHistogram(absErrorHistFilePath, equation.modelAbsoluteError, title)

    if equation.dataCache.DependentDataContainsZeroFlag != 1:
        percentErrorPlotFilePath = "static/per_error_2D.png" # simplefitter_2D
        title = "Percent Error For An HTML FORM Model"
        GraphUtils.SavePercentErrorScatterPlot(percentErrorPlotFilePath, equation, title, yAxisLabel)

        perErrorHistFilePath = "static/per_error_hist_2D.png" # simplefitter_2D
        title = "Percent Error"
        GraphUtils.SaveDataHistogram(perErrorHistFilePath, equation.modelPercentError, title)


    # generate HTML
    htmlToReturn = ''
    htmlToReturn +=  equation.GetDisplayName() + '<br><br>\n'
    htmlToReturn +=  equation.GetDisplayHTML() + '<br><br>\n'
    htmlToReturn += '<a href="' + fitStatisticsFilePath + '">Link to parameter and fit statistics</a><br><br>\n'
    htmlToReturn += '<a href="' + sourceCodeFilePath + '">Link to source code, all available languages</a><br><br>\n'
    htmlToReturn +=  '<img src="' + graphFilePath + '"> <br>\n'
    htmlToReturn +=  '<img src="' + absErrorPlotFilePath + '"><br>\n'
    htmlToReturn +=  '<img src="' + absErrorHistFilePath + '"><br>\n'

    if equation.dataCache.DependentDataContainsZeroFlag != 1:
        htmlToReturn +=  '<img src="' + percentErrorPlotFilePath + '"><br><br>\n'
        htmlToReturn +=  '<img src="' + perErrorHistFilePath + '"><br><br>\n'

    return f'<html><body>{htmlToReturn}</body></html>'



@app.route('/simplefitter_3D', methods=['POST'])
def simplefitter_3D_NoFormDataValidation():
    
    formTextData = request.form['textdata']
    formEquation = request.form['equation']
    formFittingTarget = request.form['target']

    if formEquation == 'CustomPolynomialOne':
        equation = pyeq2.Models_3D.Polynomial.UserSelectablePolynomial(formFittingTarget, "Default", 3, 1)

    elif formEquation == 'FullCubic':
        equation = pyeq2.Models_3D.Polynomial.FullCubic(formFittingTarget)
    elif formEquation == 'FullQuadratic':
        equation = pyeq2.Models_3D.Polynomial.FullQuadratic(formFittingTarget)
    elif formEquation == 'GaussianCurvatureOfWhitneysUmbrellaA':
        equation = pyeq2.Models_3D.Miscellaneous.GaussianCurvatureOfWhitneysUmbrellaA(formFittingTarget)
    elif formEquation == 'Linear':
        equation = pyeq2.Models_3D.Polynomial.Linear(formFittingTarget)
    elif formEquation == 'MonkeySaddleA':
        equation = pyeq2.Models_3D.Miscellaneous.MonkeySaddleA(formFittingTarget)
    elif formEquation == 'NIST_NelsonAutolog':
        equation = pyeq2.Models_3D.NIST.NIST_NelsonAutolog(formFittingTarget)
    # the name of the data here is from the form
    # check for functions requiring non-zero nor non-negative data such as 1/x, etc.
    try:
        pyeq2.dataConvertorService().ConvertAndSortColumnarASCII(formTextData, equation, False)
    except:
        return equation.reasonWhyDataRejected

    # check for number of coefficients > number of data points to be fitted
    coeffCount = len(equation.GetCoefficientDesignators())
    dataCount = len(equation.dataCache.allDataCacheDictionary['DependentData'])
    if coeffCount > dataCount:
        return f"This equation requires a minimum of {repr(coeffCount)} data points, you supplied {repr(dataCount)}."


    equation.Solve()
    equation.CalculateModelErrors(equation.solvedCoefficients, equation.dataCache.allDataCacheDictionary)
    equation.CalculateCoefficientAndFitStatistics()

    # save fit statistics to a text file
    fitStatisticsFilePath = "static/fitstatistics_3D.txt" # simplefitter_3D
    TextUtils.SaveCoefficientAndFitStatistics(fitStatisticsFilePath,  equation)

    # save source code to a single text file, all available languages
    sourceCodeFilePath = "static/sourcecode_3D.html" # simplefitter_3D
    TextUtils.SaveSourceCode(sourceCodeFilePath,  equation)

    # create graphs
    graphFilePath_Surface = "static/surface.png" # surface plot
    graphFilePath_Contour = "static/contour.png" # contour plot
    surfaceTitle = "Example Surface Plot"
    contourTitle = "Example Contour Plot"
    xAxisLabel = "X data"
    yAxisLabel = "Y data"
    zAxisLabel = "Z data"
    GraphUtils.SurfaceAndContourPlots(graphFilePath_Surface,
                                      graphFilePath_Contour,
                                      equation, surfaceTitle, contourTitle,
                                      xAxisLabel, yAxisLabel, zAxisLabel)

    absErrorPlotFilePath = "static/abs_error_3D.png" # simplefitter_3D
    title = "Absolute Error For An HTML FORM Model"
    GraphUtils.SaveAbsErrorScatterPlot(absErrorPlotFilePath, equation, title, zAxisLabel)

    absErrorHistFilePath = "static/abs_error_hist_3D.png" # simplefitter_3D
    title = "Absolute Error"
    GraphUtils.SaveDataHistogram(absErrorHistFilePath, equation.modelAbsoluteError, title)

    if equation.dataCache.DependentDataContainsZeroFlag != 1:
        perErrorPlotFilePath = "static/per_error_3D.png" # simplefitter_3D
        title = "Percent Error For An HTML FORM Model"
        GraphUtils.SavePercentErrorScatterPlot(perErrorPlotFilePath, equation, title, zAxisLabel)

        perErrorHistFilePath = "static/per_error_hist_3D.png" # simplefitter_3D
        title = "Percent Error"
        GraphUtils.SaveDataHistogram(perErrorHistFilePath, equation.modelPercentError, title)

    # generate HTML
    htmlToReturn = ''
    htmlToReturn +=  equation.GetDisplayName() + '<br><br>\n'
    htmlToReturn +=  equation.GetDisplayHTML() + '<br><br>\n'
    htmlToReturn += '<a href="' + fitStatisticsFilePath + '">Link to parameter and fit statistics</a><br><br>\n'
    htmlToReturn += '<a href="' + sourceCodeFilePath + '">Link to source code, all available languages</a><br><br>\n'
    htmlToReturn +=  '<img src="' + graphFilePath_Surface + '"><br><br>\n'
    htmlToReturn +=  '<img src="' + graphFilePath_Contour + '"><br><br>\n'
    htmlToReturn +=  '<img src="' + absErrorPlotFilePath + '"><br><br>\n'
    htmlToReturn +=  '<img src="' + absErrorHistFilePath + '"><br><br>\n'
    if equation.dataCache.DependentDataContainsZeroFlag != 1:
        htmlToReturn +=  '<img src="' + perErrorPlotFilePath + '"><br><br>\n'
        htmlToReturn +=  '<img src="' + perErrorHistFilePath + '"><br><br>\n'

    return f'<html><body>{htmlToReturn}</body></html>'



@app.route('/equationlist_2D', methods=['GET'])
def equationlist_2D():
    htmlToReturn = '' + '<table border=1>'
    for submodule in inspect.getmembers(pyeq2.Models_2D):
        if inspect.ismodule(submodule[1]):
            for equationClass in inspect.getmembers(submodule[1]):
                if inspect.isclass(equationClass[1]):
                    for extendedVersionName in ['Default', 'Offset']:
                        if (
                            extendedVersionName.find('Offset') != -1
                            and equationClass[1].autoGenerateOffsetForm
                            == False
                        ):
                            continue

                        equation = equationClass[1]('SSQABS', extendedVersionName)
                        htmlToReturn += '<tr>'
                        htmlToReturn += f'<td nowrap>2D {submodule[0]}</td>'
                        htmlToReturn += f'<td nowrap>{equation.GetDisplayName()}</td>'
                        htmlToReturn += f'<td nowrap>{equation.GetDisplayHTML()}</td>'
                        htmlToReturn += '</tr>'

    htmlToReturn += '</table>'

    return f'<html><body>{htmlToReturn}</body></html>'


@app.route('/equationlist_3D', methods=['GET'])
def equationlist_3D():
    htmlToReturn = '' + '<table border=1>'
    for submodule in inspect.getmembers(pyeq2.Models_3D):
        if inspect.ismodule(submodule[1]):
            for equationClass in inspect.getmembers(submodule[1]):
                if inspect.isclass(equationClass[1]):
                    for extendedVersionName in ['Default', 'Offset']:
                        if (
                            extendedVersionName.find('Offset') != -1
                            and equationClass[1].autoGenerateOffsetForm
                            == False
                        ):
                            continue

                        equation = equationClass[1]('SSQABS', extendedVersionName)
                        htmlToReturn += '<tr>'
                        htmlToReturn += f'<td nowrap>3D {submodule[0]}</td>'
                        htmlToReturn += f'<td nowrap>{equation.GetDisplayName()}</td>'
                        htmlToReturn += f'<td nowrap>{equation.GetDisplayHTML()}</td>'
                        htmlToReturn += '</tr>'

    htmlToReturn += '</table>'

    return f'<html><body>{htmlToReturn}</body></html>'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
