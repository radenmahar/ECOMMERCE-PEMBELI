import json
from . import app, client, cache, create_token

class TestPembeliCrud():
    var = 0
    def test_Pembeli_valid_input_post_name(self, client):
        token = create_token()
        data = {
            'nama_pembeli':'raden',
            'user_name':'mahar',
            'contact_pembeli':'082283511672',
            'email_pembeli':'panji@alterra.id',
            'password_pembeli':'agh765vx765',
        }
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.post('/pembeli', data=json.dumps(data),
                        # headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        TestPembeliCrud.var = res_json['id_pembeli']
        assert res.status_code == 200
    
    def test_Pembeli_invalid_post_name(self, client):
        token = create_token()
        data = {
            'nama_pembeli':'raden',
            'user_name':'mahar',
            'contact_pembeli':'082283511672',
            'email_pembeli':'panji@alterra.id',
            'password_pembeli':'agh765vx765',
        }
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.post('/pembeli/1', data=json.dumps(data),
                        # headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 500
    

    def test_Pembeli_valid_input_put(self, client):
        token = create_token()
        data = {
            'nama_pembeli':'Bambang',
        }
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.put('/pembeli/'+str(TestPembeliCrud.var), data=json.dumps(data),
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 500
    
    def test_Pembeli_invalid_input_put(self, client):
        token = create_token()
        data = {
            'nama_pembeli':'manga',
        }
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.put('/pembeli1/'+str(TestPembeliCrud.var), data=json.dumps(data),
                        # headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_Pembeli_getlist(self, client): # client dr init test
        token = create_token()
        res = client.get('/pembeli/listpembeli',
                            # headers={'Authorization':'Bearer ' + token},
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_Pembeli_get_invalid_id_token(self, client):
        res = client.get('/pembeli/'+str(TestPembeliCrud.var),
                        headers={'Authorization':'Bearer abc'})
        
        res_json = json.loads(res.data)
        assert res.status_code == 500
    
    def test_Pembeli_get_valid_id_token(self, client):
        token = create_token()
        res = client.get('/pembeli/'+str(TestPembeliCrud.var),
                        headers={'Authorization':'Bearer ' + token})
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_Pembeli_delete_token(self, client):
        token = create_token()
        res = client.delete('/pembeli/'+str(TestPembeliCrud.var),
                        headers={'Authorization':'Bearer ' + token})
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_Pembeli_invalid_delete_token(self, client):
        token = create_token()
        res = client.delete('/pembeli/500',
                        headers={'Authorization':'Bearer ' + token})
        
        res_json = json.loads(res.data)
        assert res.status_code == 404
    
    def test_Pembeli_invalid_getlist(self, client): # client dr init test
        token = create_token()
        res = client.get('/pembeli/list1',
                            # headers={'Authorization':'Bearer ' + token},
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 500