import { useState } from "react";

function App() {
  const [json, setJson] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/upload-parse", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setJson(data);
    } catch (err) {
      console.error("Error uploading:", err);
      setJson({ error: "Upload failed." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8 flex flex-col items-center gap-6">
      <h1 className="text-2xl font-bold">Health Report Uploader</h1>

      <input
        type="file"
        accept="image/*"
        onChange={handleUpload}
        className="file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-500 file:text-white hover:file:bg-indigo-600"
      />

      {loading && <p className="text-gray-500">Uploading...</p>}

      {json && (
        <pre className="bg-white p-4 rounded shadow max-w-xl w-full overflow-auto text-sm">
          {JSON.stringify(json, null, 2)}
        </pre>
      )}
    </div>
  );
}

export default App;
