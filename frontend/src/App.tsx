import { useEffect, useMemo, useState } from "react";
import Plot from "react-plotly.js";
import { analyzeDataset, fetchInvestigations, saveInvestigation, uploadCsv } from "./api";
import type { AnalysisResult, DatasetInfo, SavedInvestigation } from "./types";

function percent(value: number) { return `${(value * 100).toFixed(1)}%`; }

export default function App() {
  const [dataset, setDataset] = useState<DatasetInfo | null>(null);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [actual, setActual] = useState("");
  const [predicted, setPredicted] = useState("");
  const [comparison, setComparison] = useState("");
  const [sliceColumn, setSliceColumn] = useState("");
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const [history, setHistory] = useState<SavedInvestigation[]>([]);
  const [investigationName, setInvestigationName] = useState("Initial investigation");

  const featureColumns = useMemo(
    () => dataset?.columns.filter(c => c !== actual && c !== predicted && c !== comparison) ?? [],
    [dataset, actual, predicted, comparison]
  );

  async function refreshHistory() {
    try { setHistory(await fetchInvestigations()); } catch { /* API may not be running yet */ }
  }
  useEffect(() => { void refreshHistory(); }, []);

  async function onUpload(file?: File) {
    if (!file) return;
    setBusy(true); setMessage(""); setResult(null);
    try {
      const uploaded = await uploadCsv(file);
      setDataset(uploaded);
      const guessActual = uploaded.columns.find(c => ["actual", "actual_label", "y_true", "target"].includes(c.toLowerCase())) || uploaded.columns[0];
      const guessPredicted = uploaded.columns.find(c => ["predicted", "prediction", "y_pred", "model_prediction"].includes(c.toLowerCase())) || uploaded.columns[1] || uploaded.columns[0];
      setActual(guessActual);
      setPredicted(guessPredicted);
      setComparison("");
      setSliceColumn("");
      setMessage(`Loaded ${uploaded.row_count.toLocaleString()} rows from ${uploaded.filename}. Select the label columns and run the investigation.`);
    } catch (error) { setMessage(error instanceof Error ? error.message : "Upload failed."); }
    finally { setBusy(false); }
  }

  async function runAnalysis() {
    if (!dataset || !actual || !predicted) return;
    setBusy(true); setMessage("");
    try {
      const analyzed = await analyzeDataset({
        dataset_id: dataset.dataset_id, actual_column: actual, predicted_column: predicted,
        ...(comparison ? { comparison_column: comparison } : {}),
        ...(sliceColumn ? { slice_column: sliceColumn } : {}),
      });
      setResult(analyzed);
      setMessage("Investigation completed. Review sample counts and limitations before interpreting slice differences.");
    } catch (error) { setMessage(error instanceof Error ? error.message : "Analysis failed."); }
    finally { setBusy(false); }
  }

  async function onSave() {
    if (!result) return;
    setBusy(true);
    try {
      await saveInvestigation(investigationName.trim() || "Untitled investigation", result);
      setMessage("Investigation summary saved.");
      await refreshHistory();
    } catch (error) { setMessage(error instanceof Error ? error.message : "Could not save investigation."); }
    finally { setBusy(false); }
  }

  const metrics = result?.metrics;
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-mark">MF</div>
        <div className="brand-copy"><strong>MODEL-FAILURE</strong><span>ATLAS / WORKBENCH</span></div>
        <div className="side-label">WORKSPACE</div>
        <a className="nav-item active"> <span>◫</span> Investigation</a>
        <a className="nav-item" href="#history"><span>◷</span> Saved investigations</a>
        <div className="sidebar-bottom"><span className="status-dot" /> LOCAL WORKSPACE <small>v1.0.0</small></div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div><div className="eyebrow">MODEL QUALITY / INVESTIGATION</div><h1>Failure investigation</h1></div>
          <div className="top-status"><span className="status-dot" /> ANALYSIS ENVIRONMENT</div>
        </header>

        <section className="intro">
          <div><div className="eyebrow">EXPLAINABLE EVALUATION WORKBENCH</div>
            <h2>Look beyond the score.</h2>
            <p>Find where your model struggles, inspect its mistakes, and compare performance across data groups.</p>
          </div>
          <div className="intro-symbol">⌁</div>
        </section>

        <section className="panel upload-panel">
          <div className="section-heading"><div><span className="step">01</span><h3>Dataset ingestion</h3></div><span className="muted">CSV · UTF-8 · MAX 10 MB</span></div>
          <label className="dropzone">
            <input type="file" accept=".csv,text/csv" onChange={e => void onUpload(e.target.files?.[0])} />
            <span className="upload-icon">↑</span>
            <strong>{dataset ? "Replace dataset" : "Upload labelled dataset"}</strong>
            <span>Choose a CSV containing features, actual labels and model predictions</span>
            <em>Browse CSV file</em>
          </label>
          {dataset && <div className="dataset-meta">
            <strong>{dataset.filename}</strong><span>{dataset.row_count.toLocaleString()} rows</span><span>{dataset.column_count} columns</span>
          </div>}
          {dataset && Object.keys(dataset.missing_values).length > 0 &&
            <div className="notice warning">Missing feature values detected: {Object.entries(dataset.missing_values).map(([k,v]) => `${k}: ${v}`).join(" · ")}. Label columns must be complete.</div>}
        </section>

        {dataset && <section className="panel">
          <div className="section-heading"><div><span className="step">02</span><h3>Configure evaluation</h3></div><span className="muted">SELECT COLUMNS</span></div>
          <div className="config-grid">
            <label>Actual label column<select value={actual} onChange={e => setActual(e.target.value)}>{dataset.columns.map(c => <option key={c}>{c}</option>)}</select></label>
            <label>Prediction column<select value={predicted} onChange={e => setPredicted(e.target.value)}>{dataset.columns.map(c => <option key={c}>{c}</option>)}</select></label>
            <label>Compare with (optional)<select value={comparison} onChange={e => setComparison(e.target.value)}><option value="">No comparison</option>{dataset.columns.filter(c => c !== actual && c !== predicted).map(c => <option key={c}>{c}</option>)}</select></label>
            <label>Investigate slices by<select value={sliceColumn} onChange={e => setSliceColumn(e.target.value)}><option value="">No slice analysis</option>{featureColumns.map(c => <option key={c}>{c}</option>)}</select></label>
          </div>
          <button className="primary-button" disabled={busy || actual === predicted} onClick={() => void runAnalysis()}>{busy ? "Working…" : "Run investigation →"}</button>
          {actual === predicted && <span className="inline-error">Actual and prediction columns must be different.</span>}
        </section>}

        {message && <div className="message" role="status">{message}</div>}

        {result && metrics && <>
          <div className="results-heading"><div><div className="eyebrow">INVESTIGATION OUTPUT</div><h2>Performance overview</h2></div><span className="result-tag">ANALYSIS COMPLETE</span></div>
          <section className="metric-grid">
            <Metric label="ACCURACY" value={percent(metrics.accuracy)} detail={`${metrics.sample_count.toLocaleString()} evaluated rows`} />
            <Metric label="PRECISION · WEIGHTED" value={percent(metrics.precision_weighted)} detail="Weighted by class support" />
            <Metric label="RECALL · WEIGHTED" value={percent(metrics.recall_weighted)} detail="Weighted by class support" />
            <Metric label="F1 SCORE · WEIGHTED" value={percent(metrics.f1_weighted)} detail="Weighted harmonic mean" />
          </section>

          {result.comparison && <section className="panel">
            <div className="section-heading"><div><span className="step">03</span><h3>Model comparison</h3></div><span className="muted">SAME LABELLED ROWS</span></div>
            <div className="comparison-grid">
              <div><span>{result.comparison.primary_name}</span><strong>{percent(result.comparison.primary.accuracy)}</strong><small>Accuracy</small></div>
              <div><span>{result.comparison.comparison_name}</span><strong>{percent(result.comparison.comparison.accuracy)}</strong><small>Accuracy</small></div>
              <div><span>ACCURACY DIFFERENCE</span><strong>{((result.comparison.comparison.accuracy - result.comparison.primary.accuracy) * 100).toFixed(1)} pp</strong><small>Comparison model minus primary</small></div>
            </div>
          </section>}

          {result.slices.length > 0 && <section className="panel">
            <div className="section-heading"><div><span className="step">04</span><h3>Data slice investigation</h3></div><span className="muted">FEATURE: {sliceColumn.toUpperCase()}</span></div>
            <p className="panel-description">Groups are sorted by lowest observed accuracy. Small sample sizes can make these estimates unstable.</p>
            <div className="chart-wrap"><Plot data={[{type:"bar", x:result.slices.map(s=>s.slice), y:result.slices.map(s=>s.accuracy*100), marker:{color:"#6b8cff"}, text:result.slices.map(s=>`${percent(s.accuracy)} · n=${s.sample_count}`), textposition:"outside", cliponaxis:false}]} layout={{autosize:true, height:300, margin:{l:48,r:20,t:25,b:80}, paper_bgcolor:"rgba(0,0,0,0)", plot_bgcolor:"rgba(0,0,0,0)", font:{color:"#aeb9d0"}, yaxis:{title:"Accuracy (%)", range:[0,110], gridcolor:"#273149"}, xaxis:{tickangle:-20, gridcolor:"rgba(0,0,0,0)"}}} config={{displayModeBar:false,responsive:true}} style={{width:"100%"}} /></div>
            <div className="table-scroll"><table><thead><tr><th>SLICE</th><th>ROWS</th><th>ACCURACY</th><th>ERRORS</th><th>F1 WEIGHTED</th></tr></thead><tbody>{result.slices.map(s=><tr key={s.slice}><td>{s.slice}</td><td>{s.sample_count}</td><td>{percent(s.accuracy)}</td><td>{s.error_count}</td><td>{percent(s.f1_weighted)}</td></tr>)}</tbody></table></div>
          </section>}

          <section className="panel">
            <div className="section-heading"><div><span className="step">05</span><h3>Failure example explorer</h3></div><span className="error-count">{result.error_count} INCORRECT PREDICTIONS</span></div>
            {result.error_count === 0 ? <div className="empty-state">No incorrect predictions found in this dataset.</div> :
              <div className="table-scroll"><table><thead><tr><th>CSV ROW</th><th>ACTUAL</th><th>PREDICTED</th><th>FEATURE VALUES</th></tr></thead><tbody>{result.errors.map((e,i)=><tr key={`${e.row_number}-${i}`}><td>#{e.row_number}</td><td><span className="label-chip">{e.actual}</span></td><td><span className="label-chip bad">{e.predicted}</span></td><td className="feature-cell">{Object.entries(e.features).map(([k,v])=>`${k}: ${v ?? "—"}`).join(" · ")}</td></tr>)}</tbody></table></div>}
            {result.error_count > result.error_display_limit && <p className="muted">Showing the first {result.error_display_limit} errors. Total errors: {result.error_count}.</p>}
          </section>

          <section className="panel save-panel">
            <div><div className="eyebrow">REPRODUCIBILITY</div><h3>Save this investigation</h3><p className="panel-description">Store the evaluation summary and findings in the local database.</p></div>
            <div className="save-controls"><input value={investigationName} onChange={e=>setInvestigationName(e.target.value)} maxLength={160} aria-label="Investigation name" /><button className="primary-button" disabled={busy || !investigationName.trim()} onClick={()=>void onSave()}>Save investigation</button></div>
          </section>
          <div className="notice">{result.interpretation_note}</div>
          {Object.keys(result.missing_feature_values).length > 0 && <div className="notice warning">Missing values in feature columns: {JSON.stringify(result.missing_feature_values)}. These rows are excluded only from a slice when the selected slice feature is missing; overall metrics use all rows.</div>}
        </>}

        <section className="panel history-panel" id="history">
          <div className="section-heading"><div><span className="step">↺</span><h3>Saved investigations</h3></div><button className="text-button" onClick={()=>void refreshHistory()}>Refresh</button></div>
          {history.length === 0 ? <div className="empty-state">No saved investigations yet. Run an analysis and save it to build your history.</div> :
            <div className="table-scroll"><table><thead><tr><th>NAME</th><th>DATASET</th><th>ACCURACY</th><th>SAVED</th></tr></thead><tbody>{history.map(item=><tr key={item.id}><td>{item.name}</td><td>{item.dataset_name}</td><td>{percent(item.summary.metrics.accuracy)}</td><td>{item.created_at ? new Date(item.created_at).toLocaleString() : "—"}</td></tr>)}</tbody></table></div>}
        </section>
        <footer>MODEL-FAILURE ATLAS <span>INVESTIGATE WITH EVIDENCE · NOT ASSUMPTIONS</span></footer>
      </main>
    </div>
  );
}

function Metric({label,value,detail}:{label:string;value:string;detail:string}) {
  return <article className="metric-card"><span>{label}</span><strong>{value}</strong><small>{detail}</small></article>;
}
