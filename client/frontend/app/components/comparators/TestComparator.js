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

const TestComparator = ({ sessions }) => {
  const [selectedSessionData, setSelectedSessionData] = useState([]);
  const [selectedLLMS, setSelectedLLMS] = useState({
    firstLLM: "",
    secondLLM: "",
  });
  const [llmNames, setLlmNames] = useState({});
  const [blockComparisonData, setBlockComparisonData] = useState([]);

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
    setLlmNames(namesMap);
  };

  const fetchBlockComparisonData = async (firstLLM, secondLLM) => {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/question_blocks/compare/?first_llm_id=${firstLLM}&second_llm_id=${secondLLM}`,
    );
    const data = await response.json();
    setBlockComparisonData(data.common_blocks);
  };

  useEffect(() => {
    if (selectedLLMS.firstLLM && selectedLLMS.secondLLM) {
      fetchBlockComparisonData(selectedLLMS.firstLLM, selectedLLMS.secondLLM);
    }
  }, [selectedLLMS]);

  const chartData = blockComparisonData.map((block) => ({
    block: block.block_name,
    [`${llmNames[selectedLLMS.firstLLM]} - Semantica`]:
      block.llms[selectedLLMS.firstLLM].semantic_avg,
    [`${llmNames[selectedLLMS.secondLLM]} - Semantica`]:
      block.llms[selectedLLMS.secondLLM].semantic_avg,
    [`${llmNames[selectedLLMS.firstLLM]} - Esterna`]:
      block.llms[selectedLLMS.firstLLM].external_avg,
    [`${llmNames[selectedLLMS.secondLLM]} - Esterna`]:
      block.llms[selectedLLMS.secondLLM].external_avg,
  }));

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
            <option value="0">Seleziona una sessione</option>
            {sessions.map((session, index) => (
              <option key={index} value={session.id}>
                {session.title}
              </option>
            ))}
          </select>
        </div>
      </div>

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
              <option value="0">Seleziona un LLM</option>
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
              <option value="0">Seleziona un LLM</option>
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

      {selectedLLMS.firstLLM &&
        selectedLLMS.secondLLM &&
        chartData.length > 0 && (
          <div className="container-fluid">
            <h4 className="text-center">Valutazione per Blocco - Semantica</h4>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart
                layout="vertical"
                data={chartData}
                margin={{ top: 20, right: 30, left: 100, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="block" type="category" />
                <Tooltip />
                <Legend />
                <Bar
                  dataKey={`${llmNames[selectedLLMS.firstLLM]} - Semantica`}
                  fill="#8884d8"
                >
                  <LabelList position="right" />
                </Bar>
                <Bar
                  dataKey={`${llmNames[selectedLLMS.secondLLM]} - Semantica`}
                  fill="#82ca9d"
                >
                  <LabelList position="right" />
                </Bar>
              </BarChart>
            </ResponsiveContainer>

            <h4 className="mt-5 text-center">
              Valutazione per Blocco - Esterna
            </h4>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart
                layout="vertical"
                data={chartData}
                margin={{ top: 20, right: 30, left: 100, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="block" type="category" />
                <Tooltip />
                <Legend />
                <Bar
                  dataKey={`${llmNames[selectedLLMS.firstLLM]} - Esterna`}
                  fill="#ffc658"
                >
                  <LabelList position="right" />
                </Bar>
                <Bar
                  dataKey={`${llmNames[selectedLLMS.secondLLM]} - Esterna`}
                  fill="#ff8042"
                >
                  <LabelList position="right" />
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
    </div>
  );
};

export default TestComparator;
