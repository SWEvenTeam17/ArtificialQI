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
import { useTestComparatorContext } from "../contexts/test-comparator/TestComparatorContext";

export default function LLMComparisonChart() {
  const { chartData, llmNames, selectedLLMS } = useTestComparatorContext();
  return (
    <div data-cy="comparison-chart" className="container-fluid">
      <h4 className="text-center">
        Valutazione per insieme di domande - Semantica
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
        Valutazione per insieme di domande - Esterna
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
  );
}
