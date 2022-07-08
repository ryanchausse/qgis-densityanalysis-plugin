import os
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import Qt
from qgis.core import QgsStyle, QgsSymbol, QgsGraduatedSymbolRenderer, QgsClassificationLogarithmic
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterEnum,
    QgsProcessingParameterNumber,
    QgsProcessingParameterString,
    QgsProcessingParameterMapLayer,
    QgsProcessingParameterField)
import processing


class GraduatedStyleAlgorithm(QgsProcessingAlgorithm):
    PrmNoOutline = 'NO_OUTLINE'
    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterMapLayer(
                'INPUT', 'Input map layer', defaultValue=None,
                types=[QgsProcessing.TypeVectorAnyGeometry ])
        )
        self.addParameter(
            QgsProcessingParameterField(
                'GROUP_FIELD',
                'Field used for styling',
                parentLayerParameterName='INPUT',
                type=QgsProcessingParameterField.Any,
                defaultValue='NUMPOINTS',
                optional=False)
        )
        style = QgsStyle.defaultStyle()
        ramp_names = style.colorRampNames()
        ramp_name_param = QgsProcessingParameterString('RAMP_NAMES', 'Graduated color ramp name', defaultValue='Reds')
        ramp_name_param.setMetadata( {'widget_wrapper': {'value_hints': ramp_names } } )
        self.addParameter(ramp_name_param)
        self.addParameter(
            QgsProcessingParameterEnum(
                'MODE',
                'Mode',
                options=['Equal Count (Quantile)','Equal Interval','Logrithmic scale','Natural Breaks (Jenks)','Pretty Breaks','Standard Deviation'],
                defaultValue=0,
                optional=False)
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                'CLASSES',
                'Number of classes',
                QgsProcessingParameterNumber.Integer,
                defaultValue=15,
                minValue=2,
                optional=False)
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                'NO_OUTLINE',
                'No feature outlines',
                True,
                optional=False)
        )

    def processAlgorithm(self, parameters, context, feedback):
        layer = self.parameterAsVectorLayer(parameters, 'INPUT', context)
        attr = self.parameterAsString(parameters, 'GROUP_FIELD', context)
        ramp_name = self.parameterAsString(parameters, 'RAMP_NAMES', context)
        mode = self.parameterAsInt(parameters, 'MODE', context)
        num_classes = self.parameterAsInt(parameters, 'CLASSES', context)
        no_outline = self.parameterAsBool(parameters, 'NO_OUTLINE', context)
        
        if mode == 0: # Quantile
            grad_mode = QgsGraduatedSymbolRenderer.Quantile
        elif mode == 1: # Equal Interval
            grad_mode = QgsGraduatedSymbolRenderer.EqualInterval
        elif mode == 2: # Logrithmic scale
            grad_mode = QgsGraduatedSymbolRenderer.Quantile
        elif mode == 3: # Natural Breaks (Jenks)
            grad_mode = QgsGraduatedSymbolRenderer.Jenks
        elif mode == 4: # Pretty Breaks
            grad_mode = QgsGraduatedSymbolRenderer.Pretty
        elif mode == 5: # Standard Deviation
            grad_mode = QgsGraduatedSymbolRenderer.StdDev

        geomtype = layer.geometryType()
        symbol = QgsSymbol.defaultSymbol(geomtype)
        if no_outline:
            symbol.symbolLayer(0).setStrokeStyle(Qt.PenStyle(Qt.NoPen))
        style = QgsStyle.defaultStyle()
        ramp = style.colorRamp(ramp_name)
        new_renderer = QgsGraduatedSymbolRenderer.createRenderer(
            layer, # The layer
            attr, # Attribute name
            num_classes, # Number of classes
            grad_mode, # Mode
            symbol, # QgsSymbol
            ramp # Our color ramp
        )
        if mode == 2:
            new_renderer.setClassificationMethod(QgsClassificationLogarithmic())
        layer.setRenderer(new_renderer)
        # feedback.pushInfo('dump: {}'.format(new_renderer.dump()))
        # new_renderer.updateClasses(layer, num_classes)
        layer.triggerRepaint()
        return({})

    def name(self):
        return 'gratuatedstyle'

    def displayName(self):
        return 'Apply a graduated style'

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), 'icons/gradient.png'))

    def createInstance(self):
        return GraduatedStyleAlgorithm()
