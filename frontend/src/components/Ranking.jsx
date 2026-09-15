import { useState, useEffect } from 'react';
import { api } from '../api';

export default function Ranking() {
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
    <div className="ranking">
      <div className="ranking-header">
        <h2 className="ranking-title">Ranking</h2>
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
        <div className="ranking-loading">Cargando ranking...</div>
      ) : ranking.length === 0 ? (
        <div className="ranking-empty">
          <span className="ranking-empty-icon">&gt;_</span>
          <p>Aun no hay participantes. Se el primero!</p>
        </div>
      ) : (
        <div className="ranking-list">
          {ranking.map((entry, index) => (
            <div
              key={entry.nickname}
              className={`ranking-item ${index < 3 ? `ranking-top-${index + 1}` : ''}`}
            >
              <span className="ranking-pos">
                {index === 0 ? '\u{1F947}' : index === 1 ? '\u{1F948}' : index === 2 ? '\u{1F949}' : `#${index + 1}`}
              </span>
              <span className="ranking-nick">{entry.nickname}</span>
              <span className="ranking-pts">{entry.puntos_total} pts</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}