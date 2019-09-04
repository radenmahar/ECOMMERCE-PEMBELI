import json
from test import app, client, cache, create_token, reset_database

class TestKeranjangCrud():
    var = 0
    reset_database()
    def test_Keranjang_valid_input_post(self, client):
        token = create_token()
        data = {
            'id_pembeli':'1',
            'id_barang':'1',
            'nama_barang':'mahar',
            'user_name':'mapan',
            'nama_pembeli':'ucok',
            'harga_barang':'54000000',
            'image_barang':'adakdsakjhdkjadk',
        }
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.post('/keranjang', data=json.dumps(data),
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
               
        
        res_json = json.loads(res.data)
        TestKeranjangCrud.var = res_json['id_keranjang']
        assert res.status_code == 500

    def test_Keranjang_valid_input_post(self, client):
        token = create_token()
        data = {
            'id_pembeli':'1',
            'id_barang':'1',
            'nama_barang':'mahar',
            'user_name':'mapan',
            'nama_pembeli':'ucok',
            'image_barang':'adakdsakjhdkjadk',
        }
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.post('/keranjang', data=json.dumps(data),
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_Keranjang_getlist(self, client): # client dr init test
        token = create_token()
        res = client.get('/keranjang/semuadikeranjang',
                            # headers={'Authorization':'Bearer ' + token},
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_Keranjang_get_invalid_id_token(self, client):
        res = client.get('/keranjang/'+str(TestKeranjangCrud.var),
                        headers={'Authorization':'Bearer abc'})
        
        res_json = json.loads(res.data)
        assert res.status_code == 404
    
    def test_Keranjang_get_valid_id_token(self, client):
        token = create_token()
        res = client.get('/keranjang/'+str(TestKeranjangCrud.var),
                        headers={'Authorization':'Bearer ' + token})
        
        res_json = json.loads(res.data)
        assert res.status_code == 404
    
    # def test_Keranjang_delete_token(self, client):
    #     token = create_token()
    #     res = client.delete('/keranjang/'+str(TestKeranjangCrud.var),
    #                     headers={'Authorization':'Bearer ' + token})
        
    #     res_json = json.loads(res.data)
    #     assert res.status_code == 200
    
    def test_Keranjang_invalid_delete_token(self, client):
        token = create_token()
        res = client.delete('/keranjang/500',
                        headers={'Authorization':'Bearer ' + token})
        
        res_json = json.loads(res.data)
        assert res.status_code == 404
    
    def test_Keranjang_invalid_getlist(self, client): # client dr init test
        token = create_token()
        res = client.get('/keranjang/semuadikeranjang/1',
                            # headers={'Authorization':'Bearer ' + token},
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404