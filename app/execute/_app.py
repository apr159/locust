from datetime import datetime, timedelta
import ee

class Application:

    def __init__(self,input_variables):
        self.input_variables = input_variables
        


    def execute(self, row,date_end):
        self.get_model()
        self.authenticate()
        self.query_data(row,date_end)
        self.test()

    def get_model(self):
        return None
    
    def authenticate(self):
        ee.Authenticate()
        ee.Initialize(project='ee-apr160')
        print(ee.String('Hello from the Earth Engine servers!').getInfo())
        return None
    
    def query_data(self,row,date_end):

        def add_date(image):
            img_date = ee.Date(image.date())
            img_date = ee.Number.parse(img_date.format('YYYYMMdd'))
            return image.addBands(ee.Image(img_date).rename('date').toInt())

        def save_coordinate(Sentinel_data,row, feature):
            features = []
            poi_geometry = ee.Geometry.Point([row['Longitud'], row['Latitud']])
            poi_properties = dict(row)
            poi_feature = ee.Feature(poi_geometry, poi_properties)
            features.append(poi_feature)
            ee_fc = ee.FeatureCollection(features) 
            def rasterExtraction(image):
                feature = image.sampleRegions(
                    collection = ee_fc, # feature collection here
                    scale = 10 # Cell size of raster
                )
                return feature
    
            results = Sentinel_data.filterBounds(ee_fc).select(feature).map(add_date).map(rasterExtraction).flatten()

     
            nested_list = results.reduceColumns(ee.Reducer.toList(2), ['date',feature]).values().get(0)
            data = nested_list.getInfo()
            return data

        date_end = datetime.strptime(date_end, '%Y-%m-%d')
        date_start = date_end - timedelta(days=96)
        for input_variable in self.input_variables:
            Sentinel_data = ee.ImageCollection(input_variable['source']) \
                .filterDate(date_start,date_end) \
                .map(add_date)
            x = save_coordinate(Sentinel_data,row,input_variable['variable'])
            print(x)

    
    def test(self):
        return None