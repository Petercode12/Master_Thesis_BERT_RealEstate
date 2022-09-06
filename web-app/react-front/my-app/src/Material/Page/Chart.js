import React, { useState, useEffect } from "react";
import ReactApexChart from "react-apexcharts";
import "../Style/Chart.css";
import axios from "axios";

const data = [
  {
    id: 1,
    type: "Chung cư",
    owner: "Ms Trinh",
    price: "1400000000",
    address:
      "Đường Quốc Lộ 13, Phường Thuận Giao, Thành phố Thuận An, Bình Dương",
    license: "Sổ hồng",
  },
  {
    id: 2,
    type: "Chung cư",
    owner: "minh an",
    price: "200000000",
    address: "Thành phố Thuận An, Bình Dương",
    license: "Hợp đồng mua bán",
  },
  {
    id: 3,
    type: "Đất thổ cư",
    owner: "nguyễn văn tịch",
    price: "830000000",
    address: "Đường Quốc Lộ 13, Xã Trừ Văn Thố, Huyện Bàu Bàng, Bình Dương",
    license: "Sổ hồng",
  },
  {
    id: 4,
    type: "Chung cư",
    owner: "ngocnguyen.bds71@gmail.com",
    price: "2640000000",
    address:
      "Đường Quốc Lộ 13, Phường Thuận Giao, Thành phố Thuận An, Bình Dương",
    license: "Sổ hồng",
  },
  {
    id: 5,
    type: "Nhà hẻm, ngõ",
    owner: "HUỲNH GIAO",
    price: "4500000",
    address: "Đường dx140, Phường Tân An, Thành phố thủ Dầu Một, Bình Dương",
    license: "Sổ hồng",
  },
  {
    id: 6,
    type: "Chung cư",
    owner: "C Xoan",
    price: "1450000000",
    address: "Đường Quốc Lộ 13, Phường Thuận Giác",
    license: "Sổ hồng",
  },
  {
    id: 7,
    type: "Nhà hẻm, ngõ",
    owner: "Tan Phuoc",
    price: "1800000000",
    address: "Đường Quốc Lộ 1, Phường Thuận Giác",
    license: "Sổ hồng",
  },
  {
    id: 8,
    type: "Đất thổ cư",
    owner: "Manh Hung",
    price: "1210000000",
    address: "Đường Quốc Lộ 8, Phường Tân Bình",
    license: "Sổ hồng",
  },
  {
    id: 9,
    type: "Nhà xưởng, nhà kho",
    owner: "Mrs. Dung",
    price: "1400000000",
    address: "Đường Quốc Lộ 13, Phường Bình Tân",
    license: "Hợp đồng mua bán",
  },
  {
    id: 10,
    type: "Đất thổ cư",
    owner: "Mrs. Phụng",
    price: "1200000000",
    address: "Xa lộ hà nội, TPHCM",
    license: "Sổ hồng",
  },
  {
    id: 11,
    type: "Nhà xưởng, nhà kho",
    owner: "Mr Khoi",
    price: "1800000000",
    address: "Phường Hòa Bình, Biên Hòa",
    license: "Hợp đồng mua bán",
  },
  {
    id: 12,
    type: "Đất thổ cư",
    owner: "Mr. Phan",
    price: "1100000000",
    address: "Phường Thanh Bình, Biên Hòa",
    license: "Sổ hồng",
  },
  {
    id: 13,
    type: "Đất thổ cư",
    owner: "Ms Loc",
    price: "1200000000",
    address: "Quận 10, TPHCM",
    license: "Sổ hồng",
  },
  {
    id: 14,
    type: "Nhà hẻm, ngõ",
    owner: "Ms Trang",
    price: "900000000",
    address: "Quận 7, TPHCM",
    license: "Hợp đồng mua bán",
  },
  {
    id: 15,
    type: "Đất thổ cư",
    owner: "Ms Thuy",
    price: "1300000000",
    address: "Quận 7, TPHCM",
    license: "Sổ hồng",
  },
];

export default function Chart() {
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

  const state = {
    series: [
      {
        name: "Desktops",
        data: [10, 41, 35, 51, 49, 62, 69, 91, 148],
      },
    ],
    options: {
      chart: {
        height: 350,
        type: "line",
        zoom: {
          enabled: false,
        },
      },
      dataLabels: {
        enabled: false,
      },
      stroke: {
        curve: "straight",
      },
      title: {
        text: "Line Chart",
        align: "left",
      },
      grid: {
        row: {
          colors: ["#f3f3f3", "transparent"], // takes an array which will be repeated on columns
          opacity: 0.5,
        },
      },
      xaxis: {
        categories: [
          "Jan",
          "Feb",
          "Mar",
          "Apr",
          "May",
          "Jun",
          "Jul",
          "Aug",
          "Sep",
        ],
      },
    },
  };

  const state2 = {
    series: [
      {
        data: [400, 430, 448, 470, 540, 580, 690, 1100, 1200, 1380],
      },
    ],
    options: {
      chart: {
        type: "bar",
        height: 350,
      },
      title: {
        text: "Bar Chart",
        align: "left",
      },
      plotOptions: {
        bar: {
          borderRadius: 4,
          horizontal: true,
        },
      },
      dataLabels: {
        enabled: false,
      },
      xaxis: {
        categories: [
          "South Korea",
          "Canada",
          "United Kingdom",
          "Netherlands",
          "Italy",
          "France",
          "Japan",
          "United States",
          "China",
          "Germany",
        ],
      },
    },
  };

  const state3 = {
    series: [44, 55, 13, 43, 22],
    options: {
      chart: {
        width: 380,
        type: "pie",
      },
      title: {
        text: "Pie Chart",
        align: "left",
      },
      labels: ["Team A", "Team B", "Team C", "Team D", "Team E"],
      responsive: [
        {
          breakpoint: 480,
          options: {
            chart: {
              width: 200,
            },
            legend: {
              position: "bottom",
            },
          },
        },
      ],
    },
  };

  return (
    <div id="chart">
      <div>
        <div id="lineChart">
          <ReactApexChart
            options={state.options}
            series={state.series}
            type="line"
            height={350}
          />
        </div>
        <div id="barChart">
          <ReactApexChart
            options={state2.options}
            series={state2.series}
            type="bar"
            height={350}
          />
        </div>
      </div>

      <div id="pieChart">
        <ReactApexChart
          options={state3.options}
          series={state3.series}
          type="pie"
          width={380}
        />
      </div>
    </div>
  );
}
