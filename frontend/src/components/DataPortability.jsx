import { useState } from "react";

export default function DataPortability({ exportUrl, onImport }) {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  async function upload() {
    if (!file) return;
    const result = await onImport(file);
    setMessage(`${result.rows_processed} rows processed · ${result.results_recorded} results recorded`);
    setFile(null);
  }

  return (
    <section className="panel data-panel">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Data portability</p>
          <h2>CSV in, CSV out</h2>
        </div>
      </div>
      <p className="section-copy">Move competition data between spreadsheets and the platform without proprietary lock-in.</p>
      <div className="data-actions">
        <a className="button secondary" href={exportUrl}>Export season</a>
        <input type="file" accept=".csv,text/csv" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <button className="secondary" onClick={upload} disabled={!file}>Import CSV</button>
      </div>
      {message && <p className="note success">{message}</p>}
    </section>
  );
}
