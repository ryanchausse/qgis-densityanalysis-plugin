# QGIS Density Analysis Plugin

This plugin automates the creation of vector density heatmaps in QGIS with a heatmap explorer to examine the areas of greatest concentrations. It has two processing algorithms to create a gradient style and random style so that they can be used in QGIS models. Another tool allows a copied style or a .qml file to be pasted onto all selected layers. It provides an algorithm to create a raster density map of polygons and a pseudocolor processing algorithm to style the results. Once installed, the plugin is located under ***Plugins->Density analysis*** in the QGIS menu or on the toolbar. Some algorithms can be found in the *Processing Toolbox*.

<div style="text-align:center"><img src="help/menu.jpg" alt="Density Analysis"></div>

Note that one of the algorithms used in this plugin makes use of **H3** (Hexagonal hierarchical geospatial indexing system). This is an incredibly fast algorithm for generating hexagon density maps, but requires installation of the **H3 python library**. The H3 package can be installed by running the OSGeo4W shell as system administrator and running 'pip install h3' or whatever method you use to install python packages. After spending some time working with it, I think it would be beneficial to include it as one of the QGIS libraries in the future. In one test using the QGIS ***Create grid*** processing algorithm, followed by ***Count points in a polygon*** algorithm took 63.18 seconds to process spatially indexed point data. To do the same thing with H3 only took 3.79 seconds.

## <img src="help/densitygrid.png" alt="Random style" width="25" height="24"> Create styled density map

Given point features this will create a rectangle, diamond, or hexagon grid histogram of points that occur in each polygon grid cell. This algorithm uses the QGIS ***Count points in polygon*** algorithm which is fairly time intensive even though it has been masterfully implemented in core QGIS and significantly beats the speed implemented in commercial software. To optimize the speed make sure your input data is spatially indexed; otherwise, this algorithm will be painfully slow. The advantage to this algorithm is that it gives the most control over the size of the polygon grid cells. If speed is more important then use either the ***Create geohash density map*** or ***Create H3 density map***. Both of these use geohash indexing to count points in each geohash grid cell and they are very fast. The former creates a square or rectangular grid and H3 creates a hexagon grid. For H3 support the H3 library needs to be installed in QGIS. The disadvantages of these geohash density maps is that they have fixed resolutions and you cannot choose anything in between, but this is also what makes them fast.

Here is an example of crime in Chicago. Each point on the left is a criminal event. On the right is a hexagon heatmap counting the number of events in each cell and displaying it as a heatmap. The darker the red, the more crime is in that area. 

<div style="text-align:center"><img src="help/chicago_crime.jpg" alt="Chicago crime" width="1000"></div>

This shows the parameters used in the algorithm.

<div style="text-align:center"><img src="help/kernel_density.png" alt="Density Algorithm"></div>

These are the input parameters:

* ***Input point vector layer*** - Select one of your point feature layers. Note that counting features in polygons is a time consuming process. If you have a large data set, make sure your input point vector layer has a spatial index; otherwise, this will be very slow.
* ***Grid extent*** - Select a grid extent. In this case the extent comes from the extent of the input vector layer.
* ***Minimum cell histogram count*** - This is minimum number of features required to be within each cell for a cell to be created. A value of 0 will display the entire grid. A value of 1 means that at least one event was within the cell boundaries.
* ***Grid type*** - This is the grid type that is created. It can either be a rectangle, diamond, or hexagon. 
* ***Grid cell width*** - This is the width of the grid cell as defined by ***Grid measurement unit***.
* ***Grid cell height*** - This is the height of the grid cell as defined by ***Grid measurement unit***.
* ***Grid measurement unit*** - The unit of measure for the grid cell width and heights. Choices are Kilometers, Meters, Miles, Yards, Feet, Nautical Miles, and Degrees.
* ***Maximum grid width or height*** - This prevents a grid of huge proportions from being created and allows the user to correct the input parameters. If the width or height of the grid is exceeded, then it generates an error with a message of the grid size that would be created by the current settings and the cell width or height that needs to be used to fit within this grid size. You can always increase this number if you want a denser grid.
* ***Number of gradient colors*** - This specifies the number of categories that are going to be used. In this example we used 15. When we look at the output layer, it shows each category and the number of events that can occur within the category.

    <div style="text-align:center"><img src="help/values.png" alt="Cell counts"></div>

* ***Select a color ramp*** - This is a list of the QGIS color ramps (default Reds) that will be applied to the layer.
* ***Color ramp mode*** - Select one of Equal Count (Quantile), Equal Interval, Logarithmic scale ,Natural Breaks (Jenks), Pretty Breaks, or Standard Deviation.
* ***No feature outlines*** - If checked, it will not draw grid cell outlines.

## <img src="icons/geohash.png" alt="Geohash map" width="24" height="24"> Create styled geohash density map

This algorithm iterates through every point indexing them using a geohash with a count of the number of times each geohash has been seen. The bounds of each geohash cell is then created as a polygon. Depending on the resolution these polygon are either a square or rectangle. Here is an example.

<div style="text-align:center"><img src="help/geohash_example.png" alt="Geohash Density Map"></div>

This shows the algorithm dialog.

<div style="text-align:center"><img src="help/geohash_alg.png" alt="Geohash Density Map Algorithm"></div>

The styling parameters are the same as the above algorithm. The resolution is determined by ***Geohash resolution*** as follows:

<table style="margin-left: auto; margin-right: auto;">
<tr>
<th>Resolution<br>Level</th>
<th>Approximate<br>Dimensions</th>
</tr>
<tr>
<td style="text-align: center">1</td>
<td style="text-align: center">≤ 5,000km X 5,000km</td>
</tr>
<tr>
<td style="text-align: center">2</td>
<td style="text-align: center">≤ 1,250km X 625km</td>
</tr>
<tr>
<td style="text-align: center">3</td>
<td style="text-align: center">≤ 156km X 156km</td>
</tr>
<tr>
<td style="text-align: center">4</td>
<td style="text-align: center">≤ 39.1km X 19.5km</td>
</tr>
<tr>
<td style="text-align: center">5</td>
<td style="text-align: center">≤ 4.89km X 4.89km</td>
</tr>
<tr>
<td style="text-align: center">6</td>
<td style="text-align: center">≤ 1.22km X 0.61km</td>
</tr>
<tr>
<td style="text-align: center">7</td>
<td style="text-align: center">≤ 153m X 153m</td>
</tr>
<tr>
<td style="text-align: center">8</td>
<td style="text-align: center">≤ 38.2m X 19.1m</td>
</tr>
<tr>
<td style="text-align: center">9</td>
<td style="text-align: center">≤ 4.77m X 4.77m</td>
</tr>
<tr>
<td style="text-align: center">10</td>
<td style="text-align: center">≤ 1.19m X 0.596m</td>
</tr>
<tr>
<td style="text-align: center">11</td>
<td style="text-align: center">≤ 149mm X 149mm</td>
</tr>
<tr>
<td style="text-align: center">12</td>
<td style="text-align: center">≤ 37.2mm X 18.6mm</td>
</tr>
</table>

## <img src="icons/h3.png" alt="H3 density map" width="24" height="24"> Create styled H3 density map

This algorithm uses the H3 (Hexagonal hierarchical geospatial indexing system) library for fast density map generation. It iterates through every point using H3 indexing with a count of the number of times each H3 index has been seen. Each H3 cell is then created as a polygon. The polygons are in a hexagon shape. 

To create H3 density maps you will need to install the H3 Library (<a href="https://h3geo.org/">https://h3geo.org/</a>).
The H3 package can be installed by running the OSGeo4W shell as system administrator and running 'pip install h3' or whatever method you use to install python packages. The H3 algorithms will give a warning message if H3 has not been installed.

Here is an example.

<div style="text-align:center"><img src="help/h3_example.png" alt="H3 Density Map"></div>

This shows the algorithm dialog.

<div style="text-align:center"><img src="help/h3_alg.png" alt="H3 Density Map Algorithm"></div>

The styling parameters are the same as the ***Create Density Map Grid*** algorithm. The resolution is determined by ***H3 resolution*** as follows:

<table style="margin-left: auto; margin-right: auto;">
<tr>
<th>Resolution<br>Level</th>
<th>Average Hexagon<br>Edge Length</th>
</tr>
<tr>
<td style="text-align: center">0</td>
<td style="text-align: center">1107.71 km</td>
</tr>
<tr>
<td style="text-align: center">1</td>
<td style="text-align: center">418.68 km</td>
</tr>
<tr>
<td style="text-align: center">2</td>
<td style="text-align: center">158.24 km</td>
</tr>
<tr>
<td style="text-align: center">3</td>
<td style="text-align: center">59.81 km</td>
</tr>
<tr>
<td style="text-align: center">4</td>
<td style="text-align: center">22.61 km</td>
</tr>
<tr>
<td style="text-align: center">5</td>
<td style="text-align: center">8.54 km</td>
</tr>
<tr>
<td style="text-align: center">6</td>
<td style="text-align: center">3.23 km</td>
</tr>
<tr>
<td style="text-align: center">7</td>
<td style="text-align: center">1.22 km</td>
</tr>
<tr>
<td style="text-align: center">8</td>
<td style="text-align: center">461.35 m</td>
</tr>
<tr>
<td style="text-align: center">9</td>
<td style="text-align: center">174.38 m</td>
</tr>
<tr>
<td style="text-align: center">10</td>
<td style="text-align: center">65.91 m</td>
</tr>
<tr>
<td style="text-align: center">11</td>
<td style="text-align: center">24.91 m</td>
</tr>
<tr>
<td style="text-align: center">12</td>
<td style="text-align: center">9.42 m</td>
</tr>
<tr>
<td style="text-align: center">13</td>
<td style="text-align: center">3.56 m</td>
</tr>
<tr>
<td style="text-align: center">14</td>
<td style="text-align: center">1.35 m</td>
</tr>
<tr>
<td style="text-align: center">15</td>
<td style="text-align: center">0.51 m</td>
</tr>
</table>

## <img src="help/densityexplorer.png" alt="Density explorer tool" width="25" height="24"> Density map analysis tool

With this tool you can quickly look at the top scoring values. Select the original point layer and the density heatmap polygon layer generated by the above algorithms. ID and Count will probably automatically select the right attribute, but ID should be set to a unique identifier, and count should be set to the histogram count attribute which is **NUMPOINTS**.

<div style="text-align:center"><img src="help/densityanalysis.png" alt="Heatmap density analysis"></div>

Once the parameters have been set, click on ***Display Density Values*** and the top scores will be listed. If you click on any of entries only that grid cell will be display. A drop down set of actions specifies whether QGIS will ***Auto pan*** or ***Auto zoom*** to the selected feature or ***No action*** taken. You can then examine the features within the grid cell. You can also click and drag to select more than one, or Ctrl-click to add or subtract from the selection. Here is an example view.

<div style="text-align:center"><img src="help/example.png" alt="Example"></div>

## <img src="help/applystyles.png" alt="Density explorer tool" width="28" height="28"> Apply style to selected layers

QGIS lacks a function to paste a style to more than one layer so this tool was developed to fix that lack in capability. If you have a .qml style or have a style copied on the clipboard you can apply it to all the selected layers. 

<div style="text-align:center"><img src="help/applystyle.png" alt="Apply style to selected layers"></div>

When pasting a graduated style the symbol class values are preserved unless ***Automatically reclassify graduated layers*** is checked. When checked, each layer's minimum and maximum are evaluated along with the graduated mode to reclassify the values.

## Applying graduated and random categorized styles

The purpose of these two algorithms, is to set random and graduated styles using an algorithm. This makes it possible to set a layer's style in the model builder.

* <img src="icons/gradient.png" alt="Graduated style" width="24" height="24"> ***Apply a graduated style*** - This applies a graduated style to a layer. This is one of the building blocks to create a heatmap.

    <div style="text-align:center"><img src="help/graduated.png" alt="Graduated algorithm"></div>

    This parallels the layer styling panel. It does not include all the styling parameters, but focuses on those which are important for heatmap styling. Select your input layer, the style field, select one of the color ramp names, mode and number of classes. Mode can be Equal Count (Quantile), Equal Interval, Logarithmic scale, Natural Breaks (Jenks), Pretty Breaks, or Standard Deviation. If ***No feature outlines*** is checked, then the features will not have outlines.

* <img src="icons/random.png" alt="Random style" width="24" height="24"> ***Apply a random categorized style*** - This applies a random categorized style to a layer.

    <div style="text-align:center"><img src="help/random.png" alt="Random categorized style algorithm"></div>
    
    Specify the input layer and the field to distinguish between different categories. If ***No feature outlines*** is checked, then the features will not have outlines.

## <img src="icons/polydensity.png" alt="Create a polygon density map" width="28" height="28"> Create a polygon raster density map

This routine differs from the previous density map algorithms because it uses a raster image to accumulate the summation of rasterized polygon layers. Here is an example of the result of summing a cluster of polygons.

<div style="text-align:center"><img src="help/polygondensity.jpg" alt="Polygon density map"></div>

The parameters in dialog box are as follows:

<div style="text-align:center"><img src="help/polygondensitymap.png" alt="Polygon density map"></div>

* ***Grid extent*** - Select a grid extent. In this case it is not set and defaults to the extent of the input layer.
* ***Grid cell width or image width in pixels*** - If ***Grid measurement unit*** is set to **Dimensions in pixels** then this represents the width of the output image that will be created to span the extent of the polygon data; otherwise, each pixel represents the width value defined by ***Grid measurement unit***. For example if ***Grid measurement unit*** is set to Kilometers and this value is set to 2, then every pixel represents a width of 2 kilometers.
* ***Grid cell height or image height in pixels*** - If ***Grid measurement unit*** is set to **Dimensions in pixels** then this represents the height of the output image that will be created to span the extent of the polygon data; otherwise, each pixel represents the height value defined by ***Grid measurement unit***. For example if ***Grid measurement unit*** is set to Meters and this value is set to 20, then every pixel represents a height of 20 meters.
* ***Grid measurement unit*** - This specifies what the values represent in ***Grid cell width or image width in pixels*** and ***Grid cell height or image height in pixels***. The values are **Dimensions in pixels**, **Kilometers**, **Meters**, **Miles**, **Yards**, **Feet**, **Nautical Miles**, and **Degrees**.
* ***Maximum width or height dimensions for output image*** - Because it would be easy to create an astronomically large image if inappropriate values are used above, this provides a check to make sure they are reasonable. It will error out if the width or height of the resulting output image were to exceed this value.

## <img src="icons/styleraster.png" alt="Create a polygon density map" width="28" height="28"> Apply a pseudocolor raster style

<div style="text-align:center"><img src="help/pseudocolorstyle.png" alt="Pseudocolor raster style dialog"></div>

This achieves some of the functionality you get from right-mouse clicking on a single band image and selecting properties and selecting the *Symbology* tab and choosing ***Singleband pseudocolor*** for the ***Render type**. For more information on the parameters visit the QGIS documentation.



