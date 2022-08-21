# To The Great OutDoors
Jean Golding Institute Data [competition][compRef] on Ordnance Survey (OS) data. 

## Principle
The UK has a wealth of natural and man-made wonders to explore, but finding what's best for you might be challenging. This proof of concept application is designed to help you get back outside safely, to explore the places that are best for you. Be it some green space near your office to spend your lunch break, a nature reserve to spend a weekend, or a different part of the country to go on holiday in.

## Data
The data sources used in the construction of this application and rough purpose.  Data from OS all come from the non-premium free and open tier. Data from the National Trust and from English Heritage are Covered by the Open Government Licence.

1) [OS Open Greenspace][OSgreenspace]: Core database of outdoor locations
2) [OS Boundry-Line][OSBoundry]: Filtering on location data
3) [OS 1:250 000 Scale Colour Raster][OSRaster]: Used so polygon / point data can be seen relative to locations. 
4) [National Trust locations][NatTrust]: Additional locations that requires a membership to enter
5) [English Heritage][EngHeritage]: Addition locations of historical interest not already included

Due to size requirements, these files are not included in this repository and must be downloaded separately. More information provided within the ***Installation and Use*** instructions.

## Technical Design

Core design principle is to have the marginal cost of operation to be as low as possible, and to utilise the OS dataset as much as possible. Therefore:

1) Only open data has been utilised, with external data only from Open Government Licences.
2) No premium services are used, such as ESRI for displaying maps as an example.
3) No cost requirements for experimenting with the prototype.

The app is designed as Django app, which means it's back end is in python with some front end web (HTML, CSS, Javascript) mixed in as well. Therefore, should you wish to use it, it should be possible to iterate and then deploy to any sever that supports Django as a framework. **However**, this project is only a proof of concept, and is therefore in DEBUG mode. Should you want to deploy it, make sure you do so safely. 

**Warning** Whilst it is  possible to run with different browsers, there has only been enough time to validate chrome. As the CSS controls include webkit, if you do not use chrome, many features may not work correctly. 

## Installation and Use

A full walk-through of installation and a demo of the use of the app is available [here][YoutubeVid]. The following contains a more concise set of written instructions, where it is expected that you already know more or less what you are doing with python and django.

First you need to clone this repository to a working directory on your own PC. Then install the virtual environment from the requirements.txt. If you want to build the data from source, you will need to download all the data from the links above, and fill in the yaml file template with the full path to those files. You will then need to rename the envTemplate back to env. 

You **must** run RasterMaps.py within the DataConstruction dir, as otherwise the OS raster map data will not exist within the django static directory. However, for times sake, you can download the database of the compiled data [here][dropboxLink]. Make sure to place it in the same directory as manage.py. Once this is complete, you can then run the django app using manage.py with runserver and you should be good to go.

You can also download the cached national trust html link files [here][DropboxNatTrustHtml] 


<!--Links-->
[compRef]: https://bristol.ac.uk/golding/events/2022/a-map-with-a-view.html
[OSgreenspace]: https://osdatahub.os.uk/downloads/open/OpenGreenspace
[OSBoundry]: https://osdatahub.os.uk/downloads/open/BoundaryLine
[OSRaster]: https://osdatahub.os.uk/downloads/open/250kScaleColourRaster
[OSTerrian]: https://osdatahub.os.uk/downloads/open/Terrain50
[NatTrust]: https://open-data-national-trust.hub.arcgis.com/
[EngHeritage]: https://historicengland.org.uk/listing/the-list/data-downloads/
[YoutubeVid]: https://youtu.be/okuzQdlP30Y
[NatTrustLinks]: https://en.wikipedia.org/wiki/List_of_National_Trust_properties_in_England
[DropboxNatTrustHtml]: https://www.dropbox.com/scl/fo/smtc5sza89ulym7n6gtic/h?dl=0&rlkey=l8v33vgbqww05smj6dizly0a6
[dropboxLink]:https://www.dropbox.com/s/zz6q2it6zpvgxka/db.sqlite3?dl=0