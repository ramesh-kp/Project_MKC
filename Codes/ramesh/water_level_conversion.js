// Water Level Calculations
// Ranges
// above 60% => good
// 30% to 60% => average
// Below 30% => Bad

const express = require("express");
const { calculate } = require("./commonfile");
const app = express();
app.use(express.json());
const port = process.env.PORT || 3002;

app.get("/waterlevel", (req, res) => {
  (radius = 2.425), (pi = 3.14), (total_capacity = 75), (usage__per_day = 0.2);
  current_height = 4 - calculate(req.body.value);
  current_volume = pi * radius * radius * current_height;
  available_water = ((current_volume / total_capacity) * 100).toFixed(2);
  available_days = current_volume.toFixed(2) / 0.2;
  console.log("Water Available = " + available_water + "%");
  console.log("Available Days = " + available_days + " Days");
});

app.listen(port, () => {
  console.log("Server is up on port " + port);
});

//datas
// 01 45 69 40 20 00 00 43 99 Water Available = 36.93% Available Days = 138.5 Days
// 01 45 69 3F 99 99 99 43 99  Water Available = 68.94% Available Days = 258.5 Days
// 01 45 69 40 33 33 33 43 99  Water Available = 29.54% Available Days = 110.8 Days
