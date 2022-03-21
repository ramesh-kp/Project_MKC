const hexToBinary = require("hex-to-binary");
var binary = require("binary-to-decimal");

const calculate = (input) => {
  value = hexToBinary(input.replace(/\s+/g, "").substring(6, 14));
  signed_bit = Number(value[0]);
  exponent = Number(binary.decimal(value.substring(1, 9))) - 127;
  fraction_bits = value.substring(9, value.length);

  if (exponent >= 0) {
    decimal_value = Number(
      binary.decimal("1" + fraction_bits.substring(0, exponent))
    );
    fraction_number = Number(
      parseFloat(
        "0." +
          binary.decimal(
            "0." + fraction_bits.substring(exponent, fraction_bits.length)
          )
      ).toFixed(2)
    );
    last_value = decimal_value + fraction_number;
  }
  if (signed_bit == "0") {
    return last_value;
  } else {
    return "-" + last_value;
  }
};
module.exports = { calculate };
