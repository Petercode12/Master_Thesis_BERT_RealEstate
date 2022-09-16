import React, { useState, useEffect } from "react";
import ReactApexChart from "react-apexcharts";
import "../Style/Chart.css";
import axios from "axios";
import { Chart } from "react-google-charts";

export default function Charts() {
  const [posts, setPosts] = useState([]);
  useEffect(() => {
    axios({
      url: "http://127.0.0.1:8000/house/",
      method: "GET",
    })
      .then((res) => {
        console.log(res);
        setPosts(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  // Pie Chart
  let labelsForPieChart = {};
  for (const post of posts) {
    if (!labelsForPieChart.hasOwnProperty(post["LoaiHinh"])) {
      labelsForPieChart = { ...labelsForPieChart, [post["LoaiHinh"]]: 1 };
    } else {
      labelsForPieChart[post["LoaiHinh"]] += 1;
    }
  }
  let labelsList = Object.keys(labelsForPieChart);
  let valuesList = Object.values(labelsForPieChart);
  let pieDataList = [];
  for (let i = 0; i < labelsList.length; i++) {
    pieDataList = [...pieDataList, [labelsList[i], valuesList[i]]];
  }
  const pieData = [["Loai hinh", "So luong"], ...pieDataList];

  // Line Chart
  let jsonForLineChart = {};
  labelsList.forEach((label) => {
    jsonForLineChart = { ...jsonForLineChart, [label]: [] };
  });

  for (const post of posts) {
    if (post.DienTich !== null && !isNaN(post.DienTich)) {
      // Temporary limit < 3000 - do not need this
      if (Number(post.DienTich) < 3000) {
        jsonForLineChart[post.LoaiHinh].push(Number(post.DienTich));
      }
    }
  }
  const maxLength = Math.max(...valuesList) / 5; // Temporarily divide into 5 - origin: Not divide
  for (let i in jsonForLineChart) {
    var meanValue = parseInt(
      jsonForLineChart[i].reduce(
        (a, b) => a + b / jsonForLineChart[i].length,
        0
      )
    );
    for (let j = jsonForLineChart[i].length; j <= maxLength; j++) {
      jsonForLineChart[i].push(meanValue);
    }
    console.log("Mean value: ", meanValue);
    console.log("Values: ", jsonForLineChart[i].length);
  }
  console.log("JSON after inserting: ", jsonForLineChart);

  let dataLineChart = [["Index", ...labelsList]];
  for (let i = 1; i <= maxLength; i++) {
    let dataListElement = [i.toString()];
    for (let j in jsonForLineChart) {
      dataListElement.push(jsonForLineChart[j][i - 1]);
    }
    dataLineChart.push(dataListElement);
  }
  console.log("Data for Line Chart: ", dataLineChart);
  return (
    <div>
      <Chart
        chartType="PieChart"
        data={pieData}
        options={{
          title: "Tỉ lệ của các loại hình BĐS",
          sliceVisibilityThreshold: 0, // 20%
        }}
        width={"100%"}
        height={"400px"}
      />

      <Chart
        chartType="LineChart"
        width="100%"
        height="400px"
        data={dataLineChart}
        options={{
          title:
            "Độ biến động về diện tích của từng loại hình (Diện tích < 3000)",
          curveType: "function",
          legend: { position: "bottom" },
        }}
      />
    </div>
  );
}
