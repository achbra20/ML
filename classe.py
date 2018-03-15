import requests
import pandas as pd
from singleton_decorator import singleton

class  Service_Api:

   # todo consomation des service web
   def c_api(self, url):
      response = requests.get(url)
      print(response)
      data = response.json()
      return pd.DataFrame(data)

   # todo indexation des champs
   def index_all( self,list , champ):
      dict = []
      b = True
      j = 1
      for index, request in list.iterrows():
         for req in dict:
            if req["label"] == request[champ]:
               b = False
               break
            else:
               b = True

         if b == True:
            dict.append({"label": request[champ], "rank": j})
            j = j + 1
         b = False
      return pd.DataFrame(dict)

   # todo claculer les nombres des champs egaux
   def rank(self, list, champ):
       Statistique = []
       b = True
       for index, request in list.iterrows():
           for req in Statistique:
               if req["label"].upper().replace(" ","")==request[champ].upper().replace(" ",""):
                   req["count"] = req["count"] + 1
                   b = False
                   break
               else:
                   b = True
           if b == True:
               Statistique.append({"label": request[champ], "count": 1, })
               b = False
           Statistique = sorted(Statistique, key=lambda k: k['count'], reverse=True)
       return  pd.DataFrame(Statistique)

   # todo separer les request avec des destination multiple
   def speration(self,list, champ, sp):
       Statistique = []
       b = True
       for index, request in list.iterrows():
           if request[champ] != "":
               x = request[champ].split(sp)
               for i in range(len(x)):
                   Statistique.append(
                       {"label": x[i]})
       return pd.DataFrame(Statistique)

   # todo found les id de la list_f dans la list_p selon l'egalité des champ_p = champ_f
   def found_id(self,list_p,champ_p,champ_id,list_f,champ_f):
       rank = []
       for index, request in list_f.iterrows():
           for index, req in list_p.iterrows():
               if req[champ_p].upper() == request[champ_f].upper() and req[champ_p]!="" :
                   rank.append({'label':req[champ_p],'id':req[champ_id]})
                   break
       return rank

   # todo found ligne in list by list[champ]="critaire"
   def found_by(self, list , champ ,critaire):
       req_country = []
       for index, request  in list.iterrows():
           if request[champ] == critaire:
               req_country.append(request)

       return pd.DataFrame(req_country)



   # Country.to_json('temp.json', orient='records', lines=True)

class Destination:

    url2 = "http://www.awesome.test/Api_ml/all_location"
    service = Service_Api()
    def top_crm_win_destination(self,url,urlcrm,country):
        All_request = self.service.c_api(url)
        All_request2 = self.service.c_api(urlcrm)
        win_dis= self.top_10_distination(All_request,country)
        crm_dis= self.top_10_distination_crm(All_request2, country)
        all= win_dis.append(crm_dis)
        print(len(all))
        rank = self.service.rank(all, "label")
        print(rank)
        All_location = self.service.c_api(self.url2)
        rank2 = self.service.found_id(All_location, "address", "location_id", rank, "label")
        new_list = rank2[0:10]
        return new_list

    # todo found the top 10 distination form specific country
    def top_10_distination(self,  All_request,country):
        Country = self.service.found_by(All_request, "country", country)
        destination = self.service.speration(Country, "request_destination","/")
        return destination

    def top_10_distination_crm(self,All_request,country ):
        Country = self.service.found_by(All_request, "pays", country)
        destination = self.service.speration(Country, "destination_lib_francais"," ")
        destination2 = self.service.speration(Country, "destination_lib_francais", "/")
        destination3 = self.service.speration(Country, "destination_lib_francais", "-")
        destination.append(destination2)
        destination.append(destination3)
        return destination


class Boats:

    url2= "http://www.awesome.test/Api_ml/all_boats_discription"
    service = Service_Api()
    #todo top 10 of boat sailing  for specifec country
    def top_10_yacht(self,country,url):
        All_request = self.service.c_api(url)
        Country = self.service.found_by(All_request, "country", country)
        boats = self.service.rank(Country, "boat_model")
        new_list = self.boat_found_id(boats)
        new_list = new_list[0:10]
        result = sorted(new_list, key=lambda k: k['score'], reverse=True)
        return result

    #todo found a specfic boat from the brand, shipyard and model
    def boat_found_id(self, list):
        all_request = self.service.c_api(self.url2)
        boats_id = []
        for index, boat in list.iterrows():
            for index, boats in all_request.iterrows():
                ch = boats["boat_brand"] + " " + boats["boat_model"] + " " + boats["shipyard_name"]
                ch2 = boats["shipyard_name"] + " " + boats["boat_brand"] + " " + boats["boat_model"]
                if ch.upper() in boat["label"].upper():
                    boats_id.append({"id": boats["boat_id"], "score": boat["count"], "name": ch})
                    break
                elif ch2.upper() in boat["label"].upper():
                    boats_id.append({"id": boats["boat_id"], "score": boat["count"], "name": ch})
                    break
        return boats_id

    #todo found the top boat form specific distinatin and country
    def top_10_yacht_destination(self,url,country,destination):
        All_request = self.service.c_api(url)
        url2= "http://www.awesome.test/Api_ml/all_request_destination?destination="+destination+"&country="+country
        boat_d = self.service.c_api(url2)
        rank = self.service.rank(boat_d, "boat_model")
        new_list = self.boat_found_id(rank)
        return new_list

    def boat_type(self, url, bateau_type ,cruise_type):
        type_boat =[]
        All_request = self.service.c_api(url)
        for index, boats in All_request.iterrows():
            if boats["boat_type"].upper() == bateau_type.upper() and boats["cruise_type"].upper() == cruise_type.upper():
                type_boat.append(boats)
        return pd.DataFrame(type_boat)

    def top_10_yacht_type(self,url):
        boats = self.boat_type(url,"Motoryacht", "Boat+skipper")
        boats = self.service.rank(boats, "boat_model")
        new_list = self.boat_found_id(boats)
        new_list = new_list[0:20]
        new_list = sorted(new_list, key=lambda k: k['score'], reverse=True)
        return new_list

