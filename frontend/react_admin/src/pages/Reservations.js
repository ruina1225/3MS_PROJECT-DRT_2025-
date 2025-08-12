import React, { useEffect, useState } from "react";

function Reservations() {
  const [visits, setVisits] = useState([]);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [loading, setLoading] = useState(false);

  // 날짜 변경 시 호출할 함수 (필터 적용)
  const fetchVisits = async (start, end) => {
    setLoading(true);
    try {
      let url = "http://localhost:1122/visits/filtered";

      const params = [];
      if (start) params.push(`start_date=${start}`);
      if (end) params.push(`end_date=${end}`);
      if (params.length) url += "?" + params.join("&");

      const res = await fetch(url);
      if (!res.ok) throw new Error("조회 실패");
      const data = await res.json();
      setVisits(data);
    } catch (err) {
      console.error(err);
      alert("데이터 조회 중 오류 발생");
    }
    setLoading(false);
  };

  // 컴포넌트 처음 마운트 시 전체 조회
  useEffect(() => {
    fetchVisits("", "");
  }, []);

  // 날짜 변경 핸들러
  const handleStartDateChange = (e) => {
    const val = e.target.value;
    setStartDate(val);
    fetchVisits(val, endDate);
  };

  const handleEndDateChange = (e) => {
    const val = e.target.value;
    setEndDate(val);
    fetchVisits(startDate, val);
  };

  return (
    <div>
      <h1>📅 예약 관리 페이지</h1>

      <div style={{ marginBottom: 20 }}>
        <label>
          시작 날짜:{" "}
          <input type="date" value={startDate} onChange={handleStartDateChange} />
        </label>
        <label style={{ marginLeft: 20 }}>
          종료 날짜:{" "}
          <input type="date" value={endDate} onChange={handleEndDateChange} />
        </label>
      </div>

      {loading ? (
        <p>로딩 중...</p>
      ) : visits.length === 0 ? (
        <p>조회 결과가 없습니다.</p>
      ) : (
        <table border="1" cellPadding="8" cellSpacing="0">
          <thead>
            <tr>
              <th>방문 ID</th>
              <th>사용자</th>
              <th>방문 시간</th>
              <th>출발지 (위도, 경도)</th>
              <th>도착지 (위도, 경도)</th>
              <th>경로 ID</th>
              <th>사용자 얼굴 사진</th>
            </tr>
          </thead>
          <tbody>
            {visits.map((visit) => (
              <tr key={visit.visit_id}>
                <td>{visit.visit_id}</td>
                <td>{visit.username} (ID: {visit.user_id})</td>
                <td>{new Date(visit.visit_time).toLocaleString()}</td>
                <td>
                  {visit.pickup_lat}, {visit.pickup_lng}
                </td>
                <td>
                  {visit.dropoff_lat}, {visit.dropoff_lng}
                </td>
                <td>{visit.route_id}</td>
                <td>
                  {visit.user_image ? (
                    <img
                      src={`http://localhost:1122${visit.user_image}`}
                      alt="User Face"
                      width={60}
                      height={60}
                      style={{ borderRadius: "10%" }}
                    />
                  ) : (
                    "No Image"
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default Reservations;
