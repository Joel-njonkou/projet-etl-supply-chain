import type { Explanation } from "@/api/types";

export function ExplanationCard({ e, source }: { e: Explanation; source: "llm" | "template" | "" }) {
  const lists: { title: string; values: string[] }[] = [
    { title: "Éléments observés", values: e.preuves },
    { title: "Hypothèse alternative", values: e.hypothese_alternative ? [e.hypothese_alternative] : [] },
    { title: "Limites", values: e.limites },
    { title: "Vérifications recommandées", values: e.verifications },
  ].filter(({ values }) => values.length > 0);
  return (
    <section className="explanation-box">
      <div className="explanation-title"><h3>{e.titre}</h3><span className="status-pill">{source === "llm" ? "Analyse IA" : "Analyse standard"}</span></div>
      <p>{e.resume}</p>
      <div className="explanation-hypothesis"><strong>Hypothèse</strong><span>{e.hypothese}</span><small>Confiance : {e.confiance}</small></div>
      {lists.map(({ title, values }) => <div className="explanation-list" key={title}><strong>{title}</strong><ul>{values.map((value, index) => <li key={`${title}-${index}`}>{value}</li>)}</ul></div>)}
    </section>
  );
}