import requests
import json
url = "https://api.squadcast.com/v3/services/"
headers = {
  'Authorization': 'Bearer ',
  'Content-Type': 'application/json'
}

def getTeamIdByName(teamName):
  response = requests.request("GET", "https://api.squadcast.com/v3/teams", headers=headers, data={})
  teams=response.json()
  teams=teams["data"]
  for team in teams:
    if(team["name"]==teamName):
      return team["id"]
  return ""

def getServiceIdByName(serviceName):
  response = requests.request("GET", "https://api.squadcast.com/v3/services", headers=headers, data={})
  services=response.json()
  services=services["data"]
  for service in services:
    if(service["name"]==serviceName):
      return service["id"]
  return ""

def copyEscalationPilicies(teamName,serviceName):
  teamId=getTeamIdByName(teamName)
  sorceServiceId=getServiceIdByName(serviceName)
  if(len(sorceServiceId)>0):
    response = requests.request("GET", url+sorceServiceId, headers=headers, data={})
    if(response.status_code==200):
      data=response.json()
      escalationPolicyID=data["data"]["escalation_policy_id"]
      escalationPolicy=data["data"]["escalation_policy"]
      if(len(teamId)>0):
        res = requests.request("GET", url+"?owner_id="+teamId, headers=headers, data={})
        if(res.status_code==200):
          serviceData=res.json()
          services=serviceData["data"]
          for service in services:
            if(service["id"]!=sorceServiceId):
              temp_dict={"escalation_policy_id":escalationPolicyID,"escalation_policy":escalationPolicy}
              tempPayload=json.dumps(temp_dict)
              ress = requests.request("PUT", url+service["id"], headers=headers, data=tempPayload)
              print(ress.json())
      else:
        print("Team Name: "+teamName+" doesn't exist")
    else:
      print(response.text)
  else:
    print("Service Name: "+serviceName+" doesn't exist")

def copyTaggingRules(teamName,serviceName):
  teamId=getTeamIdByName(teamName)
  sorceServiceId=getServiceIdByName(serviceName)
  copyAutomatedRules(teamId,sorceServiceId,'tagging-rules')

def copyRoutingRules(teamName,serviceName):
  teamId=getTeamIdByName(teamName)
  sorceServiceId=getServiceIdByName(serviceName)
  copyAutomatedRules(teamId,sorceServiceId,'routing-rules')

def copyDedupRules(teamName,serviceName):
  teamId=getTeamIdByName(teamName)
  sorceServiceId=getServiceIdByName(serviceName)
  copyAutomatedRules(teamId,sorceServiceId,'deduplication-rules')

def copySuppRules(teamName,serviceName):
  teamId=getTeamIdByName(teamName)
  sorceServiceId=getServiceIdByName(serviceName)
  copyAutomatedRules(teamId,sorceServiceId,'suppression-rules')

def copyAutomatedRules(teamId,sorceServiceId,path):
  response = requests.request("GET", url+sorceServiceId+"/"+path, headers=headers, data={})
  if(response.status_code==200):
    data=response.json()
    rules=data["data"]["rules"]
    res = requests.request("GET", url+"?owner_id="+teamId, headers=headers, data={})
    if(res.status_code==200):
      serviceData=res.json()
      services=serviceData["data"]
      for service in services:
        if(service["id"]!=sorceServiceId):
          createAutomatedRules(service["name"],path,rules)
  else:
    print(response.text)

def createAutomatedRules(serviceName,automationRuleName,rules):
  temp_dict={"rules":rules}
  tempPayload=json.dumps(temp_dict)
  serviceId=getServiceIdByName(serviceName)
  ress = requests.request("POST", url+serviceId+"/"+automationRuleName, headers=headers, data=tempPayload)
  print(ress.json())

def createSchedule(name, colour, description = "", teamName = ""):
  teamName = getTeamIdByName(teamName)
  temp_dict = {"name":name,"colour":colour,"description":description,"teamId":teamName}
  tempPayload=json.dumps(temp_dict)
  ress = requests.request("POST", "https://api.squadcast.com/v3/schedules", headers=headers, data=tempPayload)
  print(ress.json())
  return ress.json()

createSchedule("abc punit134","#0f61dd")
