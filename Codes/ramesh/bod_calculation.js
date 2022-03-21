// BOD Calculation
// Ranges
// 0-100 => Good
// 100- 300 => Average
// above 300 => Bad

const express = require("express");
const { calculate } = require("./commonfile");
const app = express();
app.use(express.json());
const port = process.env.PORT || 3002;

app.get("/bodcalculation", (req, res) => {
  bod = Number(calculate(req.body.value));
  if (bod <= 100) {
    console.log("bod level is " + bod + "  - Good");
  } else if (bod < 300) {
    console.log("bod level is " + bod + "  - Average");
  } else {
    console.log("bod level is " + bod + "  - Bad");
  }
});

app.listen(port, () => {
  console.log("Server is up on port " + port);
});
