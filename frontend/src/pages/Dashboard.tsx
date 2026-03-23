import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import { documentService } from "../services/documentService";
import type  { Document } from "../types";

const Dashboard = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    documentService
      .getDocuments()
      .then(setDocuments)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const formatSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString("en-IN", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  };

  return (
    <div style={{ display: "flex", minHeight: "100vh", background: "#0a0a0a" }}>
      <Sidebar />
      <main style={{ marginLeft: "220px", flex: 1, padding: "40px" }}>
        <div style={{ marginBottom: "32px" }}>
          <h1 style={{ color: "#ffffff", fontSize: "20px", fontWeight: 600 }}>
            Documents
          </h1>
          <p style={{ color: "#444444", fontSize: "14px", marginTop: "4px" }}>
            {documents.length} document{documents.length !== 1 ? "s" : ""}{" "}
            uploaded
          </p>
        </div>

        {loading ? (
          <div style={{ color: "#444444", fontSize: "14px" }}>Loading...</div>
        ) : documents.length === 0 ? (
          <div
            style={{
              border: "1px dashed #1e1e1e",
              borderRadius: "8px",
              padding: "60px",
              textAlign: "center",
            }}
          >
            <p style={{ color: "#444444", fontSize: "14px" }}>
              No documents yet
            </p>
            <p style={{ color: "#333333", fontSize: "13px", marginTop: "8px" }}>
              Upload your first document to get started
            </p>
          </div>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
            {documents.map((doc) => (
              <div
                key={doc.id}
                style={{
                  background: "#0f0f0f",
                  border: "1px solid #1e1e1e",
                  borderRadius: "8px",
                  padding: "16px 20px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                }}
              >
                <div
                  style={{ display: "flex", alignItems: "center", gap: "12px" }}
                >
                  <span
                    style={{
                      fontSize: "11px",
                      padding: "3px 8px",
                      background: "#141414",
                      border: "1px solid #1e1e1e",
                      borderRadius: "4px",
                      color: "#666666",
                      textTransform: "uppercase",
                    }}
                  >
                    {doc.file_type}
                  </span>
                  <div>
                    <p
                      style={{
                        color: "#ffffff",
                        fontSize: "14px",
                        fontWeight: 500,
                      }}
                    >
                      {doc.title}
                    </p>
                    <p
                      style={{
                        color: "#444444",
                        fontSize: "12px",
                        marginTop: "2px",
                      }}
                    >
                      {formatSize(doc.file_size)} · {formatDate(doc.created_at)}
                    </p>
                  </div>
                </div>
                <span
                  style={{
                    fontSize: "12px",
                    color: doc.is_processed ? "#22c55e" : "#f59e0b",
                    background: doc.is_processed ? "#0f2d1a" : "#2d1f0a",
                    padding: "3px 10px",
                    borderRadius: "20px",
                  }}
                >
                  {doc.is_processed ? "Processed" : "Processing"}
                </span>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
};

export default Dashboard;
