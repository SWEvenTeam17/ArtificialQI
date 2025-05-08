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

const LLMComparator = ({ sessions }) => {
  const [selectedSessionData, setSelectedSessionData] = useState([]);
  const [selectedLLMS, setSelectedLLMS] = useState({
    firstLLM: "",
    secondLLM: "",
  });
  const [comparisonData, setComparisonData] = useState([]);
  const [llmNames, setLlmNames] = useState({});

  const fetchSessionData = async (id) => {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/session_list/${id}`
    );
    const data = await response.json();
    setSelectedSessionData(data);

    const namesMap = {};
    data.llm.forEach((llm) => {
      namesMap[llm.id] = llm.name;
    });
    setLlmNames(namesMap);
  };

  const fetchComparisonData = async (first_llm_id, second_llm_id, session_id) => {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/llm_comparison/?first_llm_id=${first_llm_id}&second_llm_id=${second_llm_id}&session_id=${session_id}`
    );
    const data = await response.json();
    setComparisonData(data);
  };

  useEffect(() => {
    if (
      selectedLLMS.firstLLM &&
      selectedLLMS.secondLLM &&
      selectedSessionData.id
    ) {
      fetchComparisonData(
        selectedLLMS.firstLLM,
        selectedLLMS.secondLLM,
        selectedSessionData.id
      );
    }
  }, [selectedLLMS, selectedSessionData]);

  const groupedData = {};
  comparisonData.forEach((item) => {
    const promptText = item.prompt.prompt_text;
    if (!groupedData[promptText]) {
      groupedData[promptText] = { prompt: promptText };
    }

    const llmKey =
      item.llm.id == selectedLLMS.firstLLM
        ? "llm1"
        : "llm2";

    groupedData[promptText][`${llmKey}_semantic`] = parseFloat(
      item.evaluation.semantic_evaluation
    );
    groupedData[promptText][`${llmKey}_external`] = parseFloat(
      item.evaluation.external_evaluation
    );
  });

  const chartData = Object.values(groupedData);

  return (
    <div className="container-fluid p-5">
      {/* Selezione sessione */}
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

      {/* Selezione LLM */}
      {selectedSessionData.length !== 0 && (
        <div className="row row-cols-md-2 row-cols-1 p-3">
          <div className="col">
            <select
              onChange={(e) => {
                e.target.value !== "0"
                  ? setSelectedLLMS((prev) => ({
                      ...prev,
                      firstLLM: e.target.value,
                    }))
                  : setSelectedLLMS((prev) => ({ ...prev, firstLLM: "" }));
              }}
              className="form-select"
            >
              <option value="0"> Seleziona un LLM</option>
              {selectedSessionData.llm
                .filter((llm) => llm.id != selectedLLMS.secondLLM)
                .map((llm, index) => (
                  <option value={llm.id} key={index}>
                    {llm.name}
                  </option>
                ))}
            </select>
          </div>
          <div className="col">
            <select
              onChange={(e) => {
                e.target.value !== "0"
                  ? setSelectedLLMS((prev) => ({
                      ...prev,
                      secondLLM: e.target.value,
                    }))
                  : setSelectedLLMS((prev) => ({ ...prev, secondLLM: "" }));
              }}
              className="form-select"
            >
              <option value="0"> Seleziona un LLM</option>
              {selectedSessionData.llm
                .filter((llm) => llm.id != selectedLLMS.firstLLM)
                .map((llm, index) => (
                  <option value={llm.id} key={index}>
                    {llm.name}
                  </option>
                ))}
            </select>
          </div>
        </div>
      )}

      {/* Grafici */}
      {selectedLLMS.firstLLM && selectedLLMS.secondLLM && chartData.length > 0 && (
        <div className="container-fluid">
          <h4 className="text-center">Valutazione Semantica</h4>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart
              layout="vertical"
              data={chartData}
              margin={{ top: 20, right: 30, left: 100, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis dataKey="prompt" type="category" />
              <Tooltip />
              <Legend />
              <Bar
                dataKey="llm1_semantic"
                fill="#8884d8"
                name={llmNames[selectedLLMS.firstLLM]}
              >
                <LabelList dataKey="llm1_semantic" position="right" />
              </Bar>
              <Bar
                dataKey="llm2_semantic"
                fill="#82ca9d"
                name={llmNames[selectedLLMS.secondLLM]}
              >
                <LabelList dataKey="llm2_semantic" position="right" />
              </Bar>
            </BarChart>
          </ResponsiveContainer>

          <h4 className="mt-5 text-center">Valutazione Esterna</h4>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart
              layout="vertical"
              data={chartData}
              margin={{ top: 20, right: 30, left: 100, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis dataKey="prompt" type="category" />
              <Tooltip />
              <Legend />
              <Bar
                dataKey="llm1_external"
                fill="#ffc658"
                name={llmNames[selectedLLMS.firstLLM]}
              >
                <LabelList dataKey="llm1_external" position="right" />
              </Bar>
              <Bar
                dataKey="llm2_external"
                fill="#ff8042"
                name={llmNames[selectedLLMS.secondLLM]}
              >
                <LabelList dataKey="llm2_external" position="right" />
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
};

export default LLMComparator;
