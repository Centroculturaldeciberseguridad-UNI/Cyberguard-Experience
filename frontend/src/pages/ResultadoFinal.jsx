import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api';

export default function ResultadoFinal({ nickname, setNickname }) {
  const navigate = useNavigate();
  const [posicion, setPosicion] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!nickname) {
      navigate('/');
      return;
    }
    api
      .obtenerPosicion(nickname)
      .then(setPosicion)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [nickname, navigate]);

  const handleNuevoUsuario = () => {
    setNickname('');
    navigate('/');
  };

  if (loading) {
    return (
      <main className="rf-page">
        <div className="rf-card">
          <p className="rf-loading">Calculando resultados...</p>
        </div>
      </main>
    );
  }

  const d = posicion?.desglose || {};
  const total = posicion?.puntos_total || 0;

  let rankingMsg = '';
  let rankingClass = '';
  if (posicion?.en_top10) {
    rankingMsg = '¡Increible! Estas en el Top 10 del ranking.';
    rankingClass = 'rf-rank-gold';
  } else if (posicion?.en_top50) {
    rankingMsg = '¡Buen trabajo! Estas en el Top 50 del ranking.';
    rankingClass = 'rf-rank-silver';
  } else {
    rankingMsg = 'Sigue practicando para mejorar.';
    rankingClass = 'rf-rank-bronze';
  }

  return (
    <main className="rf-page">
      <div className="rf-card">
        <h1 className="rf-title">Resultados Finales</h1>
        <p className="rf-nick">
          Participante: <strong>{nickname}</strong>
        </p>

        <div className="rf-breakdown">
          <div className="rf-row">
            <span>Retos 1 (Contraseñas Seguras)</span>
            <span className="rf-pts">{d.reto1 || 0} pts</span>
          </div>
          <div className="rf-row">
            <span>Reto 2 (Detección Phishing)</span>
            <span className="rf-pts">{d.reto2 || 0} pts</span>
          </div>
          <div className="rf-row">
            <span>Reto 3 (Investigacion OSINT)</span>
            <span className="rf-pts">{d.reto3 || 0} pts</span>
          </div>
          <div className="rf-row rf-total-row">
            <span>Puntuación total</span>
            <span className="rf-total-pts">{total} pts</span>
          </div>
        </div>

        <div className={`rf-ranking-msg ${rankingClass}`}>
          {posicion?.posicion && (
            <p className="rf-pos">Posición #{posicion.posicion}</p>
          )}
          <p>{rankingMsg}</p>
        </div>

        <button className="btn btn-primary rf-btn" onClick={handleNuevoUsuario}>
          Nuevo participante
        </button>
      </div>
    </main>
  );
}