msg = 'Message'
sensor="Sensor"

# def errorMessage(validationMsg, exceptionMsg=''):
#     if len(exceptionMsg.strip()) == 0:
#         exceptionMsg = validationMsg
#     # logging.getLogger("info_logger").info(exceptionMsg)
#     return ({msg: validationMsg})


def errorMessage(validationMsg, sensor_details=''):
    if len(sensor_details.strip())==0:
        result = ({msg:validationMsg})
        return result
    else:
        result = ({sensor:sensor_details,msg:validationMsg})
        return (result)

validation = {
    "MKC1" : 101,
    "MKC2" : 102,
    "MKC3" : 103,
    "MKC4" : 104,
    "MKC5" : 105,
    "MKC6" : 106,
    "MKC7" : 107
}
