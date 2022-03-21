// Temperatore Calculations
// Ranges
// 0-600 =>good
// 600-900  =>average
// above 900 => Bad

const express = require("express");
const { calculate } = require("./commonfile");

const app = express();
app.use(express.json());
const port = process.env.PORT || 3002;
app.get("/temperature", (req, res) => {
  const output = calculate(req.body.value);
  console.log("temperature = " + output);
});

app.listen(port, () => {
  console.log("Server is up on port " + port);
});

//smple data
// 01 45 69 (42 02 85 1E) 43 99 - 32.63
// 01 45 69 (41 E6 00 00) 43 99 - 28.75
// 01 45 69 (41 C0 00 00) 43 99 - 24.0
// https://www.ultimatesolver.com/en/ieee-754
