import { isAxiosError } from "axios";
import { Link } from "react-router-dom";
import { useAnomalies, useExplain } from "@/api/hooks";
import { ExplanationCard } from "@/components/ExplanationCard";
import { QueryState } from "@/components/QueryState";
import { Spinner } from "@/components/Spinner";

export function Anomalies() {
  const query = useAnomalies();
  const explain = useExplain();
  return (
    <div className="page-stack">
      <div className="page-heading"><div><p className="eyebrow">SURVEILLANCE</p><h1>Anomalies de livraison</h1><p className="muted">Périodes présentant un taux de retard atypique.</p></div><span className="status-pill status-warning">Analyse statistique</span></div>
      <QueryState q={query} empty={(data) => data.length === 0}>
        {(items) => <div className="anomaly-list">{items.map((anomaly) => (
          <article key={anomaly.id} className="panel anomaly-card">
            <header className="anomaly-header"><div><p className="eyebrow">ANOMALIE · {anomaly.granularite}</p><h2>Semaine du {anomaly.periode_debut}</h2><p className="muted">Jusqu’au {anomaly.periode_fin}</p></div><span className="anomaly-score">z = {anomaly.z_score.toFixed(2)}</span></header>
            <div className="anomaly-metrics"><div><strong>{anomaly.taux_retard_pct.toFixed(1)} %</strong><span>Taux de retard</span></div><div><strong>{anomaly.reference_pct.toFixed(1)} %</strong><span>Référence</span></div><div><strong>{anomaly.volume.toLocaleString("fr-FR")}</strong><span>Expéditions</span></div></div>
            <footer className="anomaly-actions"><Link className="table-link" to={`/anomalies/${anomaly.id}`}>Voir les détails ↗</Link><button className="button button-primary" disabled={explain.isPending && explain.variables === anomaly.id} onClick={() => explain.mutate(anomaly.id)}>{explain.isPending && explain.variables === anomaly.id ? <Spinner label="Analyse…" size="small" /> : anomaly.explanation ? "Régénérer l’explication" : "Expliquer l’anomalie"}</button></footer>
            {explain.isError && explain.variables === anomaly.id && <p role="alert" className="error-message">{isAxiosError(explain.error) && explain.error.response?.status === 403 ? "Droits insuffisants : le rôle analyste est requis." : "L’explication n’a pas pu être générée. Réessayez."}</p>}
            {anomaly.explanation && <ExplanationCard e={anomaly.explanation} source={anomaly.explanation_source} />}
          </article>
        ))}</div>}
      </QueryState>
    </div>
  );
}
