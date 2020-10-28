from flask import Flask, request, make_response,jsonify
import json
import os
from flask_cors import cross_origin
import datetime
from sendEmail import EmailSender

doctors = {"CAR": "Dr. A. Meenakshi, M.D, DM[Cardiology]", "ENT": "Dr. P. Jayanth kumar DLO., DO-HNS(RCS Eng.)., FEBORL-HNS(EB).,",
           "DERMA": "Dr. N.P. Shankarnarayanan., DTM+H.,", "ORTHO": "Dr. R. Umapathy Sivam, MS., (Ortho)", "GM": "Dr. A. Rasu, M.D(GEN. MED).,", "PDT": "Dr. R. Selvan, DNB(Paed.)., DCH.,"}
depts = {"CAR":"Cardiologist","ENT":"Ear,Nose and Throat doctor","ORTHO":"Orthologist","GM":"General Medicine Doctor","PDT":"Paediatrician","DERMA":"Dermatologist"}
app = Flask(__name__)

daye = datetime.datetime.now()
hr = int(daye.strftime("%H"))
day = int(daye.strftime("%w"))


# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():

    req = request.get_json(silent=True, force=True)

    #print("Request:")
    #print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    #print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def test(req):

    return {
        "fulfillmentText": "fulfillmentText"
    }

def processRequest(req):
    
    
    #sessionID = req.get('responseId')

    result = req.get("queryResult")

    intent = result.get("intent").get('displayName')

    print(intent)
   

    if intent == "department_selection":

        dept = result.get("parameters").get("dept")
        print(dept)
        print()

        fulfillmentText = "You want an appointment for ,(" + depts[dept] + ") , Enter your name :"
        return {
            "fulfillmentText": fulfillmentText
        }

    elif intent == "name_entry":

        pass


    elif intent == "details":

        if (day != 0 and 8 < hr < 22):
            parameters = result.get("parameters")
           
            p_mail = parameters.get("p_email")
            
            doctor = doctors[result.get("outputContexts")[0].get("parameters").get("dept")]
            print(doctor, end="/n")
            
            apt_time = str(hr+1) + ':' + daye.strftime("%M")
            
            fulfillmentText = "Your appointment is successful" + \
                'You have an appoinment with "' + doctor + '"at ' + apt_time
            
            email_sender = EmailSender()
            
            email_message = "You have an appoinment with " + doctor + " at " + apt_time + \
                "\n\nTry visiting our Hospital website 'dashealthhospitals.com' to know more about the doctors 😊"
            
            email_sender.send_email_to_student(p_mail, email_message)

            #email_message_support = "You have to consult "+p_name+" at " + apt_time + "\n\nTry visiting our Hospital website 'dashealthhospitals.com' to know more about the docotr and ouselves.. 😊"
            #email_sender.send_email_to_support(cust_name=p_name, cust_contact=p_phone,
                                            #cust_email=p_mail, course_name=dept, body=email_message_support)
            
            
            return {
                "fulfillmentText": fulfillmentText
            }

        elif hr < 8 or hr > 22:
            apt_time = str(hr) + ':' + daye.strftime("%M")
            fulfillmentText = "Appointment is unsuccessful , since the time is " + apt_time + "Earlier than 8:00 or later than 22:00 😞" +"\n\n ...Try calling our hospital number : 04440504050 , incase of emergency"

            return {
                "fulfillmentText": fulfillmentText
            }

        elif day==0:

            fulfillmentText = "Your appointment is unsuccessful, since it is sunday today 🤷‍♂️,\nSORRY FOR YOUR INCONVENICE" + \
                "\n\n...Try calling our hospital number : 04440504050 , incase of emergency"

            return {
                "fulfillmentText": fulfillmentText
            }

    else:
        
        fulfillmentText = "Your appointment is unsuccessful, try making in-person appointment in our hospital (hospital number : 04440504050) ,\nSORRY FOR YOUR INCONVENICE 😞"

        return {
            "fulfillmentText": fulfillmentText
        }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
    
