

from app.execute._app import Application

input_variables = [
    {
        'source':'MODIS/061/MYD13Q1',
        'variable':'NDVI'

    },
    {
        'source':'MODIS/061/MOD11A1',
        'variable':'LST_Day_1km'

    },
    {
        'source':'NASA/ORNL/DAYMET_V4',
        'variable':'prcp'

    }


    
]
    


app = Application(input_variables)
app.execute({'Latitud':20.57,'Longitud':-90.22524},'2022-10-10')
