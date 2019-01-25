<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor version="1.0.0" 
 xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" 
 xmlns="http://www.opengis.net/sld" 
 xmlns:ogc="http://www.opengis.net/ogc" 
 xmlns:xlink="http://www.w3.org/1999/xlink" 
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <!-- a Named Layer is the basic building block of an SLD document -->
  <NamedLayer>
    <Name>default_raster</Name>
    <UserStyle>
    <!-- Styles can have names, titles and abstracts -->
      <Title>Default Raster</Title>
      <Abstract>A sample style that draws a raster, good for displaying imagery</Abstract>
      <!-- FeatureTypeStyles describe how to render different features -->
      <!-- A FeatureTypeStyle for rendering rasters -->
      <FeatureTypeStyle>
        <FeatureTypeName>Feature</FeatureTypeName>
        <Rule>
          <RasterSymbolizer>
            <Opacity>1.0</Opacity>
            <ColorMap>
              <ColorMapEntry color="#bab6b6" quantity="0" label="0" opacity="1"/>
	      <ColorMapEntry color="#1a7739" quantity="1" label="1" opacity="1"/>
	      <ColorMapEntry color="#94db64" quantity="2" label="2" opacity="1"/>
              <ColorMapEntry color="#dbbe81" quantity="3" label="3" opacity="1"/>
              <ColorMapEntry color="#db8b29" quantity="4" label="4" opacity="1"/>
              <ColorMapEntry color="#cc4c33" quantity="5" label="5" opacity="1"/>
      	    </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>

