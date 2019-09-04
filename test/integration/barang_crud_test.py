import json
from test import app, client, cache, create_token

class TestBarangCrud():
    var = 0

    def test_Barang_getlist(self, client): # client dr init test
        token = create_token()
        res = client.get('/barang/semuabarang',
                            # headers={'Authorization':'Bearer ' + token},
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_Barang_getlist_nonlapak(self, client): # client dr init test
        token = create_token()
        res = client.get('/barang/semuabarang',
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_Barang_getlist_nonlapak(self, client): # client dr init test
        token = create_token()
        res = client.get('/barang/semuabarang1',
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 401
    
    def test_Barang_get_invalid_id_token(self, client):
        res = client.get('/barang1/'+str(TestBarangCrud.var))
        
        res_json = json.loads(res.data)
        assert res.status_code == 404
    
    def test_Barang_get_valid_id_token(self, client):
        token = create_token()
        res = client.get('/barang/2')
        
        res_json = json.loads(res.data)
        assert res.status_code == 401
    
    def test_Barang_delete_token(self, client):
        token = create_token()
        res = client.delete('/barang/4')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404
    
    def test_Barang_invalid_delete_token(self, client):
        token = create_token()
        res = client.delete('/barang/500',
                        headers={'Authorization':'Bearer ' + token})
        
        res_json = json.loads(res.data)
        assert res.status_code == 404
    
    def test_Barang_valid_search(self, client): # client dr init test
        token = create_token()
        res = client.get('/barang/search',
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_Barang_invalid_search(self, client): # client dr init test
        token = create_token()
        res = client.get('/barang/search/1',
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404
    
    def test_Barang_valid_send_email(self, client):
        token = create_token()
        data = {
            'namaPembeli':'mahar',
            'emailtujuan':'maharraden765@gmail.com',
            'Barang':'murah dan bagus',
            'ID':'4',
            'alamat':'Jombang',
            'total':'800000000',
        }
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.post('/barang/nembak', data=json.dumps(data),
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        TestBarangCrud.var = res_json['barang_id']
        assert res.status_code == 200

    def test_Barang_valid_send_email(self, client):
        token = create_token()
        data = {
            'namaPembeli':'mahar',
            'emailtujuan':'maharraden765@gmail.com',
            'Barang':'murah dan bagus',
            'ID':'4',
            'alamat':'Jombang',
            'total':'800000000',
            'total1':'800000000',
        }
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.post('/barang/nembak', data=json.dumps(data),
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200