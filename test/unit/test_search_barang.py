from blueprints.Pembeli.model import Pembeli
from blueprints.Pembeli.resources import Weather
from blueprints import db, app 
from mock import patch
from test import reset_database

class TestPembeli():

    reset_database()

    def test_search(self):

        data = {
                "nama_pembeli": "pantat",
                "user_name": "panji",
                "contact_pembeli": "082283511672",
                "email_pembeli": "maharraden765@gmail.com",
                "password_pembeli": "raden",
                "status": True
            }

        # insert data
        user = Pembeli(data['nama_pembeli'], data['user_name'], data['contact_pembeli'], data['email_pembeli'], data['password_pembeli'], data['status'])
        db.session.add(user)
        db.session.commit()

        namapembeli = "pantat"

        assert Pembeli.is_exists(namapembeli) == True
    
    @patch.object(Weather, 'get')
    def testGetWeatherMock(self, mock_get):

        response = {
                        "city": "Bandung",
                        "organization": "AS9657 Melsa-i-net AS",
                        "timezone": "Asia/Jakarta",
                        "current_weather": {
                            "date": "2019-09-04:07",
                            "temp": 27.6
                        }
                    }
        
        mock_get.return_value = response

        assert Weather.get('/weather?ip=202.138.233.162') == response