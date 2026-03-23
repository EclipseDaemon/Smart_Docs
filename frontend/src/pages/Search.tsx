import { useState } from "react";
import Sidebar from "../components/Sidebar";
import { documentService } from "../services/documentService";
import type { Document } from "../types";

const Search = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Document[]>([]);
  const [searched, setSearched] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    try {
      const data = await documentService.searchDocuments(query);
      setResults(data);
      setSearched(true);
    } catch {
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: "flex", minHeight: "100vh", background: "#0a0a0a" }}>
      <Sidebar />
      <main style={{ marginLeft: "220px", flex: 1, padding: "40px" }}>
        <div style={{ marginBottom: "32px" }}>
          <h1 style={{ color: "#ffffff", fontSize: "20px", fontWeight: 600 }}>
            Search
          </h1>
          <p style={{ color: "#444444", fontSize: "14px", marginTop: "4px" }}>
            Search across all your documents
          </p>
        </div>

        <form
          onSubmit={handleSearch}
          style={{ maxWidth: "480px", marginBottom: "32px" }}
        >
          <div style={{ display: "flex", gap: "8px" }}>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search documents..."
              style={{
                flex: 1,
                padding: "10px 14px",
                background: "#0f0f0f",
                border: "1px solid #1e1e1e",
                borderRadius: "6px",
                color: "#ffffff",
                fontSize: "14px",
                outline: "none",
              }}
            />
            <button
              type="submit"
              disabled={loading}
              style={{
                padding: "10px 20px",
                background: "#ffffff",
                color: "#000000",
                border: "none",
                borderRadius: "6px",
                fontSize: "14px",
                fontWeight: 600,
                cursor: "pointer",
              }}
            >
              {loading ? "..." : "Search"}
            </button>
          </div>
        </form>

        {searched && (
          <div>
            <p
              style={{
                color: "#444444",
                fontSize: "13px",
                marginBottom: "16px",
              }}
            >
              {results.length} result{results.length !== 1 ? "s" : ""} for "
              {query}"
            </p>
            {results.length === 0 ? (
              <p style={{ color: "#333333", fontSize: "14px" }}>
                No documents found
              </p>
            ) : (
              <div
                style={{ display: "flex", flexDirection: "column", gap: "8px" }}
              >
                {results.map((doc) => (
                  <div
                    key={doc.id}
                    style={{
                      background: "#0f0f0f",
                      border: "1px solid #1e1e1e",
                      borderRadius: "8px",
                      padding: "16px 20px",
                    }}
                  >
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
                        marginTop: "4px",
                      }}
                    >
                      {doc.file_type.toUpperCase()} · {doc.original_filename}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
};

export default Search;
