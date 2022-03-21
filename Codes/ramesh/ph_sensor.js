// Ph Calculation
// Ranges
// 0-7 => Acidic
// 7 => Neutral
// abve 7 => Basic

const express = require("express");
const { calculate } = require("./commonfile");
const app = express();
app.use(express.json());
const port = process.env.PORT || 3002;

app.get("/phsensor", (req, res) => {
  ph = Number(calculate(req.body.value)) / 100;
  if (ph < 7) {
    console.log("pH level is " + ph + "  Acidic");
  } else if (ph === 7) {
    console.log("pH level is " + ph + "  Neutral");
  } else {
    console.log("pH level is " + ph + "  Basic");
  }
});

app.listen(port, () => {
  console.log("Server is up on port " + port);
});

//sample data
//01 45 69 44 35 40 00 43 99  pH level is 7.25  basic
