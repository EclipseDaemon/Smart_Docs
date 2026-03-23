import { useState, useRef } from "react";
import Sidebar from "../components/Sidebar";
import { documentService } from "../services/documentService";

const Upload = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");
  const [dragOver, setDragOver] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = (f: File) => {
    setFile(f);
    setSuccess(false);
    setError("");
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const dropped = e.dataTransfer.files[0];
    if (dropped) handleFile(dropped);
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    setError("");
    try {
      await documentService.uploadDocument(file);
      setSuccess(true);
      setFile(null);
    } catch {
      setError("Upload failed. Please try again.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div style={{ display: "flex", minHeight: "100vh", background: "#0a0a0a" }}>
      <Sidebar />
      <main style={{ marginLeft: "220px", flex: 1, padding: "40px" }}>
        <div style={{ marginBottom: "32px" }}>
          <h1 style={{ color: "#ffffff", fontSize: "20px", fontWeight: 600 }}>
            Upload Document
          </h1>
          <p style={{ color: "#444444", fontSize: "14px", marginTop: "4px" }}>
            Supports PDF and Word documents
          </p>
        </div>

        <div style={{ maxWidth: "480px" }}>
          <div
            onClick={() => inputRef.current?.click()}
            onDragOver={(e) => {
              e.preventDefault();
              setDragOver(true);
            }}
            onDragLeave={() => setDragOver(false)}
            onDrop={handleDrop}
            style={{
              border: `2px dashed ${dragOver ? "#ffffff" : "#1e1e1e"}`,
              borderRadius: "10px",
              padding: "60px 40px",
              textAlign: "center",
              cursor: "pointer",
              background: dragOver ? "#111111" : "transparent",
              transition: "all 0.15s ease",
            }}
          >
            <p style={{ color: "#666666", fontSize: "14px" }}>
              {file ? file.name : "Drop file here or click to browse"}
            </p>
            {file && (
              <p
                style={{ color: "#444444", fontSize: "12px", marginTop: "8px" }}
              >
                {(file.size / 1024).toFixed(1)} KB
              </p>
            )}
          </div>

          <input
            ref={inputRef}
            type="file"
            accept=".pdf,.docx,.doc"
            style={{ display: "none" }}
            onChange={(e) =>
              e.target.files?.[0] && handleFile(e.target.files[0])
            }
          />

          {success && (
            <div
              style={{
                marginTop: "16px",
                padding: "12px",
                background: "#0f2d1a",
                border: "1px solid #166534",
                borderRadius: "6px",
                color: "#22c55e",
                fontSize: "13px",
              }}
            >
              Document uploaded successfully
            </div>
          )}

          {error && (
            <div
              style={{
                marginTop: "16px",
                padding: "12px",
                background: "#2d0f0f",
                border: "1px solid #991b1b",
                borderRadius: "6px",
                color: "#ef4444",
                fontSize: "13px",
              }}
            >
              {error}
            </div>
          )}

          <button
            onClick={handleUpload}
            disabled={!file || uploading}
            style={{
              marginTop: "16px",
              width: "100%",
              padding: "11px",
              background: !file || uploading ? "#1e1e1e" : "#ffffff",
              color: !file || uploading ? "#444444" : "#000000",
              border: "none",
              borderRadius: "6px",
              fontSize: "14px",
              fontWeight: 600,
              cursor: !file || uploading ? "not-allowed" : "pointer",
            }}
          >
            {uploading ? "Uploading..." : "Upload"}
          </button>
        </div>
      </main>
    </div>
  );
};

export default Upload;
