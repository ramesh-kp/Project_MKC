def energymeter_salve_id(current_id, new_id):
    output_hex = hex(current_id).replace('0x', '') + \
        hex(new_id).replace('0x', '')
    output_int = int(output_hex, 16)
    return output_int


energymeter_salve_id(200, 255)
