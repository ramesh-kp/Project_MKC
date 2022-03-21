// TSS Calculations
// Ranges
// 0-7 =>good
// 7  =>average
// above 7 => Bad

const express = require("express");
const { calculate } = require("./commonfile");
const app = express();
app.use(express.json());
const port = process.env.PORT || 3002;

app.get("/tsssensor", (req, res) => {
  tss = Number(calculate(req.body.value)) / 100;
  if (tss < 7) {
    console.log("tss level is " + tss + "  Good");
  } else if (tss === 7) {
    console.log("tss level is " + tss + "  Average");
  } else {
    console.log("tss level is " + tss + "  Bad");
  }
});

app.listen(port, () => {
  console.log("Server is up on port " + port);
});