import React, { useEffect, useState } from "react";
import "./App.css"; // Arquivo CSS para estilização

function App() {
  const [logs, setLogs] = useState([]);
  const [filter, setFilter] = useState("all"); // Filtro: "all", "malicious", "non-malicious"

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8765");
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setLogs((prevLogs) => [...prevLogs, data]);
      } catch (error) {
        console.error("Erro ao analisar mensagem WebSocket:", error, event.data);
      }
    };

    return () => ws.close();
  }, []);

  // Filtrar logs conforme a classificação
  const filteredLogs = logs.filter((log) => {
    if (filter === "malicious") return log.classification === "Malicious";
    if (filter === "non-malicious") return log.classification === "Non-malicious";
    return true; // "all"
  });

  // Contadores de logs
  const maliciousCount = logs.filter((log) => log.classification === "Malicious").length;
  const nonMaliciousCount = logs.filter((log) => log.classification === "Non-malicious").length;

  return (
    <div className="app-container">
      <h1>Logs do Webserver</h1>

      <div className="filter-container">
        <button
          className={filter === "all" ? "active" : ""}
          onClick={() => setFilter("all")}
        >
          Todos ({logs.length})
        </button>
        <button
          className={filter === "malicious" ? "active" : ""}
          onClick={() => setFilter("malicious")}
        >
          Maliciosos ({maliciousCount})
        </button>
        <button
          className={filter === "non-malicious" ? "active" : ""}
          onClick={() => setFilter("non-malicious")}
        >
          Não Maliciosos ({nonMaliciousCount})
        </button>
      </div>

      <table className="log-table">
        <thead>
          <tr>
            <th>Log</th>
            <th>Classificação</th>
          </tr>
        </thead>
        <tbody>
          {filteredLogs.map((log, index) => (
            <tr key={index} className={log.classification === "Malicious" ? "malicious" : "non-malicious"}>
              <td>{log.log}</td>
              <td>{log.classification}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {filteredLogs.length === 0 && <p className="no-logs">Nenhum log encontrado para o filtro atual.</p>}
    </div>
  );
}

export default App;
