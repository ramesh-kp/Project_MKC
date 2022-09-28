msg = 'Message'
sensor = "Sensor"

# def errorMessage(validationMsg, exceptionMsg=''):
#     if len(exceptionMsg.strip()) == 0:
#         exceptionMsg = validationMsg
#     # logging.getLogger("info_logger").info(exceptionMsg)
#     return ({msg: validationMsg})

def errorMessage(validationMsg,sensor_details=""):
    print(validationMsg)
    return ({sensor_details:sensor,msg: validationMsg})



validation = {
    "MKC1" : "variable not found",
    "MKC2" : "File not found",
    "MKC3" : "Data already added.",
    "MKC4" : "Sensor not found.",
    "MKC5" : "Invalid literal for int() with base 16.",
    "MKC6" : "Invalid input format.",
    "MKC7" : "Please provide required data"
}