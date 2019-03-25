settings = {

    "aoifile": "https://gdh-data.ams3.digitaloceanspaces.com/boundaries/camkox-purple.geojson",
    "systems": ["URB","AG","IND","FOR","HYDRO","EI","LDH","MIX"],
    "outputdirectory": "output",
    "workingdirectory": "working",
    "corinedata": "CORINE-lc.zip",
}


processchains = {
    "URB": {
        "red": [11100,11210,11220,11230,],
        "yellow": [12210,12220,12230,12300,12400,13100,13300,31000,40000,50000],
        "green": [ 11240,11300,12100,13400,14100,14200,20000,21000,22000,23000,24000,25000,32000,33000]
    },
    "AG": {
        "red":  [21000,22000,23000,24000,25000],
        "yellow": [11100,11210,11220,11230,11240,11300,12100,12220,12230,12300,12400,13100,13300],
        "green": [31000,32000,33000,13100,13300,13400,14100,14200,13400,14100,14200,40000,50000]
    },
    
    "IND": {
        "red": [12100,12210,12220,12230,12300,12400,13100,13300,],
        "yellow": [40000,50000],
        "green": [11100,11210,11220,11230,11240,11300,13400,14100,14200,20000,21000,22000,23000,24000,25000,31000,32000,33000]
    },
    
    "FOR": {
        "red": [31000,33000,40000],
        "yellow": [50000,11100,11210,11220,11230,11240,11300,12100,12210,12220,12230,12300,12400,13300,14100,20000],
        "green": [21000,22000,23000,24000,25000,40000,13100]
    },
    
    "HYDRO": {
        "red": [50000],
        "yellow": [],
        "green": [31000,32000,33000,40000,13400]
    },

    "EI": {
        "red": [],
        "yellow": [20000,21000,22000,23000,24000,25000,31000,32000,33000,40000,50000],
        "green": [11100,11210,11220,11230,11240,11300,12100,12210,12220,12230,12300,12400,13100,13300,13400,14100,14200]
    },
    "LDH": {
        "red": [11230,11240,11300],
        "yellow": [11100,11210,11220,12210,12220,12230,12400,31000,32000,40000,50000],
        "green": [12100,12300,13100,14100,14200,20000,21000,22000,23000,24000,25000]
    },
    "MIX": {
        "red": [11000],
        "yellow": [12210,12220,12230,12300,12400,22000,23000,24000,25000,31000,32000,33000,40000,50000],
        "green": [11210,11220,11230,11240,11300,12100,13100,13300,13400,14100,14200,20000,21000,]
    }

}
