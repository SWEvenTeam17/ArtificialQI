import { useState, useEffect } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LabelList,
} from "recharts";

const QuestionComparator = ({ sessions }) => {
  const [selectedSessionData, setSelectedSessionData] = useState([]);
  const [selectedLLM, setSelectedLLM] = useState({ id: null });
  const [comparisonData, setComparisonData] = useState([]);
  const [averages, setAverages] = useState({
    semantic_average: 0,
    external_average: 0,
  });

  const fetchSessionData = async (id) => {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/session_list/${id}`,
    );
    const data = await response.json();
    setSelectedSessionData(data);

    const namesMap = {};
    data.llm.forEach((llm) => {
      namesMap[llm.id] = llm.name;
    });
  };

  const fetchComparisonData = async (llm_id, session_id) => {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/prompt_comparison/?llm_id=${llm_id}&session_id=${session_id}`,
    );
    const data = await response.json();
    setComparisonData(data.tests);
    setAverages({
      semantic_average: data.averages["semantic_average"],
      external_average: data.averages["external_average"],
    });
  };

  useEffect(() => {
    if (selectedLLM?.id && selectedSessionData.id) {
      fetchComparisonData(selectedLLM.id, selectedSessionData.id);
    }
  }, [selectedLLM, selectedSessionData]);

  const groupedData = {};
  comparisonData?.forEach((item) => {
    const promptText = item.prompt.promptText;
    if (!groupedData[promptText]) {
      groupedData[promptText] = { prompt: promptText };
    }

    groupedData[promptText][`${item.llm.id}_semantic`] = parseFloat(
      item.evaluation.semantic_evaluation,
    );
    groupedData[promptText][`${item.llm.id}_external`] = parseFloat(
      item.evaluation.external_evaluation,
    );
  });

  const chartData = Object.values(groupedData);

  const avgChartData = [
    {
      name: "Media",
      "Valutazione Semantica": averages.semantic_average,
      "Valutazione Esterna": averages.external_average,
    },
  ];

  return (
    <div className="container-fluid p-5">
      <div className="row text-center justify-content-center">
        <div className="col-md-6 col-12">
          <select
            onChange={(e) => {
              e.target.value === "0"
                ? setSelectedSessionData([])
                : fetchSessionData(e.target.value);
            }}
            className="form-select"
          >
            <option value={"0"}>Seleziona una sessione</option>
            {sessions.map((session, index) => (
              <option key={index} value={session.id}>
                {session.title}
              </option>
            ))}
          </select>
        </div>
      </div>

      {selectedSessionData.length !== 0 && (
        <div className="row text-center justify-content-center">
          <div className="col-md-6 col-12 p-3">
            <select
              onChange={(e) => {
                const selectedLlmId = e.target.value;
                const selectedLlm = selectedSessionData.llm.find(
                  (llm) => llm.id === parseInt(selectedLlmId),
                );
                setSelectedLLM(selectedLlm || {});
              }}
              className="form-select"
            >
              <option value="0">Seleziona un LLM</option>
              {selectedSessionData.llm.map((llm, index) => (
                <option value={llm.id} key={index}>
                  {llm.name}
                </option>
              ))}
            </select>
          </div>
        </div>
      )}

      {selectedLLM?.id &&
        selectedSessionData.length !== 0 &&
        chartData.length > 0 && (
          <div className="container-fluid">
            <h4 className="text-center">Media per Domande</h4>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart
                layout="vertical"
                data={avgChartData}
                margin={{ top: 20, right: 30, left: 100, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="name" type="category" />
                <Tooltip />
                <Legend />
                <Bar dataKey="Valutazione Semantica" fill="#8884d8">
                  <LabelList dataKey="Valutazione Semantica" position="right" />
                </Bar>
                <Bar dataKey="Valutazione Esterna" fill="#82ca9d">
                  <LabelList dataKey="Valutazione Esterna" position="right" />
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
    </div>
  );
};

export default QuestionComparator;
