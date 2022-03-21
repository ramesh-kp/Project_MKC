// TDS Calculations
// Ranges
// 0-600 =>good
// 600-900  =>average
// above 900 => Bad

const express = require("express");
const { calculate } = require("./commonfile");
const app = express();
app.use(express.json());
const port = process.env.PORT || 3002;

app.get("/tdssensor", (req, res) => {
  tds = Number(calculate(req.body.value));
  if (tds <= 600) {
    console.log("tds level is " + tds + "  - Good");
  } else if (tds <= 900) {
    console.log("tds level is " + tds + "  - Average");
  } else {
    console.log("tds level is " + tds + "  - Bad");
  }
});

app.listen(port, () => {
  console.log("Server is up on port " + port);
});
