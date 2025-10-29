import requests
import pytest
import time


class TestRedfishAPI:
     def test_1_authentication(self):
        url = "https://localhost:2443/redfish/v1/SessionService/Sessions"

        data = {
                "UserName": "root",
                "Password": "0penBmc",
            }
        respons = requests.post(url, json=data, verify=False, timeout=10)
        #print(respons)
        assert respons.status_code in [200, 201]
        response_data = respons.json()
        #print(response_data)
        #{'@odata.id': '/redfish/v1/SessionService/Sessions/1GsUerjcr2', '@odata.type': '#Session.v1_7_0.Session', 'ClientOriginIPAddress': '10.0.2.2', 'Description': 'Manager User Session', 'Id': '1GsUerjcr2', 'Name': 'User Session', 'Roles': ['Administrator'], 'UserName': 'root'}
        assert "Id" in response_data
        assert "X-Auth-Token" in respons.headers
       #print(respons.headers["X-Auth-Token"])
        return respons.headers["X-Auth-Token"]
        
     def test_2_get_system_info(self):
        
        auth_token = self.test_1_authentication()
        url = "https://localhost:2443/redfish/v1/Systems/system"
        header = {"X-Auth-Token":auth_token}
        resp = requests.get(url,headers=header, verify=False, timeout=10)
        info_json= resp.json()
        #print(info_json)

        assert "PowerState" in info_json
        assert "Status" in info_json
        assert resp.status_code == 200
        return(info_json)
        
     def test_3_power_on_server(self):
        reps_statte_bef = self.test_2_get_system_info().get("PowerState")
        #print(reps_statte_bef)
        auth_token = self.test_1_authentication()
        url = "https://localhost:2443/redfish/v1/Systems/system/Actions/ComputerSystem.Reset"
        header = {"X-Auth-Token":auth_token}
        resp = requests.post(url,headers=header,json={"ResetType": "On"}, verify=False, timeout=10)
        
        assert resp.status_code == 204
        
        time.sleep(15) 
        reps_statte_aff = self.test_2_get_system_info().get("PowerState")
        #print(reps_statte_aff)
        #assert reps_statte_bef != reps_statte_aff

     def test_4_check_cpu_temperature(self):
        auth_token = self.test_1_authentication()
        url = "https://localhost:2443/redfish/v1/Chassis/chassis/Thermal"
        header = {"X-Auth-Token":auth_token}
        resp = requests.get(url,headers=header, verify=False, timeout=10)
        info_json= resp.json()
        assert "Temperatures" in info_json
        assert resp.status_code == 200
        cont_el = len(info_json.get("Temperatures"))
        #print(cont_el)
        #assert cont_el > 0, "отсутсвует температура"


         


        
obj = TestRedfishAPI()
obj.test_4_check_cpu_temperature()


