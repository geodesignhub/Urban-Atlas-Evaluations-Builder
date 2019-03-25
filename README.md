# Geodesignhub Urban Atlas Evaluation Maps Builder
This program uses CORINE landcover data from [Copernicus portal](https://land.copernicus.eu/local/urban-atlas/urban-atlas-2012/) to develop Evaluation maps for [Geodesignhub](https://www.geodesignhub.com/). It uses simple rules to parse the existing data and build evaluation maps that can be used directly on Geodesignhub. Urban Atlas data is available only for Europe so this tool can be used to make evaluation maps only for Europe.

Making evaluation maps is the most time consuming part of a Geodesign study, using this script it can be automated. The following evaluation maps are generated:

* Urban (URB / HSG + COM)
* Agriculture (AG)
* Industrial (IND)
* Forests (FOR)
* Hydrology (HYDRO)

Find out more about evaluation maps at the [Making Evaluations Maps](https://community.geodesignhub.com/t/making-evaluation-maps/62) in our community page. 

At the moment, this is best suited for generating evaluations at urban area level anywhere Urban Atlas data is avialable. For larger areas this type of Evaluation map creation is not recommended.

If you are new to Geodesignhub, please see our course at [Teachable.com](https://geodesignhub.teachable.com/p/geodesign-with-geodesignhub/)  

## Installation
Use the requirements.txt file to install libraries that are required for the program

```
pip install requirements.txt
```

## 3-Step process
**1. Download raw data**

1. Go to [Copernicus portal](https://land.copernicus.eu/local/urban-atlas/urban-atlas-2012?tab=download) to order and download the CORINE vector data and clip it to your area of interest.
2. Save the clipped layer as a GeoPackage and put it in the ```working``` folder in the directory, create one if you dont have it. 

**2. Update config.py**

1. Update the config file to point to the AOI file and the CORINE file using the correct filename.

**3. Upload Evaluations**

1. Run the `UA-evaluations-generator.py` script and check the `output` folder for the Evaluation GeoJSON that can be uploaded to Geodesignhub

