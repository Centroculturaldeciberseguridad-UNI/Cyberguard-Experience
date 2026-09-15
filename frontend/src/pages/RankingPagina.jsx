import { useState, useEffect } from 'react';
import { api } from '../api';

export default function RankingPagina() {
  const [ranking, setRanking] = useState([]);
  const [top, setTop] = useState(10);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api
      .obtenerRanking(top)
      .then((data) => setRanking(data.ranking))
      .catch(() => setRanking([]))
      .finally(() => setLoading(false));
  }, [top]);

  return (
    <main className="rp-page">
      <div className="rp-container">
        <div className="rp-header">
          <div>
            <h1 className="rp-title">Ranking General</h1>
            <p className="rp-subtitle">
              Clasificacion de participantes por puntuacion total
            </p>
          </div>
          <div className="ranking-toggle">
            <button
              className={`btn btn-sm ${top === 10 ? 'btn-active' : ''}`}
              onClick={() => setTop(10)}
            >
              Top 10
            </button>
            <button
              className={`btn btn-sm ${top === 50 ? 'btn-active' : ''}`}
              onClick={() => setTop(50)}
            >
              Top 50
            </button>
          </div>
        </div>

        {loading ? (
          <div className="rp-loading">Cargando ranking...</div>
        ) : ranking.length === 0 ? (
          <div className="rp-empty">
            <span className="rp-empty-icon">&gt;_</span>
            <p>Aun no hay participantes con puntaje.</p>
            <p className="rp-empty-hint">
              Registra un nickname y completa los retos para aparecer aqui.
            </p>
          </div>
        ) : (
          <div className="rp-table">
            <div className="rp-thead">
              <span className="rp-th rp-th-pos">#</span>
              <span className="rp-th rp-th-nick">Participante</span>
              <span className="rp-th rp-th-pts">Puntos</span>
            </div>
            {ranking.map((entry, index) => (
              <div
                key={entry.nickname}
                className={`rp-row ${index < 3 ? `rp-row-top${index + 1}` : ''}`}
              >
                <span className="rp-td rp-td-pos">
                  {index === 0
                    ? '\u{1F947}'
                    : index === 1
                      ? '\u{1F948}'
                      : index === 2
                        ? '\u{1F949}'
                        : index + 1}
                </span>
                <span className="rp-td rp-td-nick">{entry.nickname}</span>
                <span className="rp-td rp-td-pts">{entry.puntos_total}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}