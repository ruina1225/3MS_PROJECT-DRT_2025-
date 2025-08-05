import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer
} from "recharts";

function SignupStatsChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get("/users/signup-stats")
      .then((res) => {
        console.log("받아온 데이터", res.data);
        setData(res.data); // ✅ 수정된 부분
      })
      .catch((err) => {
        console.error("에러 발생:", err);
      });
  }, []);

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="count" fill="#8884d8" />
      </BarChart>
    </ResponsiveContainer>
  );
}

export default SignupStatsChart;

