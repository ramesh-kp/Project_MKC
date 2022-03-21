// COD Calculations
// Ranges
// 0-150 => Green
// 150-1500 => Yellow
// above 1500 => Red

const express = require("express");
const { calculate } = require("./commonfile");
const app = express();
app.use(express.json());
const port = process.env.PORT || 3002;

app.get("/codcalculation", (req, res) => {
  cod = Number(calculate(req.body.value));
  if (cod <= 150) {
    console.log("cod level is " + cod + "  - Green");
  } else if (cod < 1500) {
    console.log("cod level is " + cod + "  - Yellow");
  } else {
    console.log("cod level is " + cod + "  - Red");
  }
});

app.listen(port, () => {
  console.log("Server is up on port " + port);
});

//sample data
// 01 45 69 44 35 40 00 43 99  cod level is 725  - Yellow
// 01 45 69 42 60 00 00 43 99  cod level is 56  - Green
// 01 45 69 43 16 00 00 43 99  cod level is 150  - Green
// 01 45 69 44 C8 00 00 43 99  cod level is 1600  - Red
