import { useTestFormContext } from "@/app/components/contexts/session/test-form/TestFormContext";
import Form from "next/form";
export default function JSONView() {
  const { handleJSONSubmit, handleJSONFileChange, loading } =
    useTestFormContext();
  return (
    <>
      <div className="text-center fs-3 mb-4">
        <h5 className="text-primary fw-bold mb-4">Input JSON</h5>
        <Form onSubmit={handleJSONSubmit}>
          <div className="mb-3">
            <input
              type="file"
              accept=".json"
              onChange={handleJSONFileChange}
              className="form-control w-50 mx-auto"
            />
          </div>
          <button
            type="submit"
            className="btn btn-primary w-50 rounded-5"
            disabled={loading}
          >
            {loading ? (
              <span
                className="spinner-border spinner-border-sm"
                role="status"
                aria-hidden="true"
              ></span>
            ) : (
              "Invia"
            )}
          </button>
        </Form>
      </div>
    </>
  );
}
