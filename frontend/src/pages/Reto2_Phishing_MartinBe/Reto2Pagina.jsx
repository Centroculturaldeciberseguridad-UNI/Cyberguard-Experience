import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../../api';
import './Reto2Pagina.css';

export default function Reto2Pagina({ nickname, setNickname }) {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [caso, setCaso] = useState(null);
  const [pista, setPista] = useState('');
  const [feedback, setFeedback] = useState(null);
  const [enviando, setEnviando] = useState(false);
  const [resumenFinal, setResumenFinal] = useState(null);

  useEffect(() => {
    if (!nickname) {
      navigate('/');
      return;
    }
    iniciarOReanudar();
  }, [nickname, navigate]);

  const iniciarOReanudar = async () => {
    try {
      setLoading(true);
      await api.iniciarReto2(nickname);
      const actual = await api.obtenerCasoActualReto2(nickname);
      if (actual.completado) {
        const res = await api.obtenerResultadoReto2(nickname);
        setResumenFinal(res);
      } else {
        setCaso(actual);
      }
    } catch (err) {
      console.error('Error al iniciar Reto 2:', err);
    } finally {
      setLoading(false);
    }
  };

  const handlePedirPista = async () => {
    try {
      const res = await api.pedirPistaReto2(nickname);
      setPista(res.hint);
    } catch (err) {
      console.error('Error al pedir pista:', err);
    }
  };

  const handleResponder = async (esPhishing) => {
    try {
      setEnviando(true);
      const res = await api.enviarRespuestaReto2(nickname, esPhishing);
      setFeedback(res);
    } catch (err) {
      console.error('Error al responder caso:', err);
    } finally {
      setEnviando(false);
    }
  };

  const handleSiguienteCaso = async () => {
    setFeedback(null);
    setPista('');
    if (feedback?.completado) {
      const res = await api.obtenerResultadoReto2(nickname);
      setResumenFinal(res);
    } else {
      try {
        setLoading(true);
        const actual = await api.obtenerCasoActualReto2(nickname);
        setCaso(actual);
      } catch (err) {
        console.error('Error al cargar siguiente caso:', err);
      } finally {
        setLoading(false);
      }
    }
  };

  if (loading) {
    return (
      <main className="reto2-container">
        <div className="reto2-results-card">
          <p style={{ color: 'var(--text-muted)' }}>Cargando casos de phishing...</p>
        </div>
      </main>
    );
  }

  if (resumenFinal) {
    return (
      <main className="reto2-container">
        <header className="reto2-header">
          <span className="reto2-badge-num">RETO 02 / 03 - COMPLETADO</span>
          <h1 className="reto2-title">¡Misión de Detección Finalizada!</h1>
        </header>

        <div className="reto2-results-card">
          <p style={{ fontSize: '1.1rem', color: 'var(--text-secondary)' }}>
            Has completado la evaluación de correos sospechosos y técnicas de ingeniería social.
          </p>

          <div className="results-stats-grid">
            <div className="stat-box">
              <div className="stat-label">Casos Analizados</div>
              <div className="stat-value">{resumenFinal.total_casos}</div>
            </div>
            <div className="stat-box">
              <div className="stat-label">Aciertos</div>
              <div className="stat-value" style={{ color: 'var(--accent)' }}>{resumenFinal.aciertos}</div>
            </div>
            <div className="stat-box">
              <div className="stat-label">Puntaje Final</div>
              <div className="stat-value" style={{ color: '#00f2fe' }}>
                {resumenFinal.puntaje_obtenido} / {resumenFinal.puntos_maximos} pts
              </div>
            </div>
          </div>

          <button className="btn-goto-reto3" onClick={() => navigate('/reto3')}>
            Continuar al Reto 3: Investigación OSINT ➔
          </button>
        </div>
      </main>
    );
  }

  if (!caso) return null;

  return (
    <main className="reto2-container">
      <header className="reto2-header">
        <span className="reto2-badge-num">RETO 02 / 03</span>
        <h1 className="reto2-title">Phishing Detective</h1>
        <p className="reto2-subtitle">
          El 36% de las violaciones de datos comienzan con un correo engañoso. Analiza cada mensaje, examina remitentes y enlaces, y determina si es seguro o un ataque.
        </p>
      </header>

      {/* Barra de progreso y estado */}
      <div className="reto2-statusbar">
        <div>
          Caso <strong>{caso.caso_numero}</strong> de {caso.total_casos}
        </div>
        <div>
          Dificultad:{' '}
          <span className={`diff-badge diff-${caso.difficulty}`}>
            {caso.difficulty === 'easy' ? 'Fácil (40 pts)' : caso.difficulty === 'medium' ? 'Media (50 pts)' : 'Difícil (60 pts)'}
          </span>
        </div>
        <div className="score-display">
          Puntos acumulados: <strong>{caso.puntaje_acumulado} pts</strong>
        </div>
      </div>

      {/* Visor de Correo */}
      <div className="email-client-card">
        <div className="email-header">
          <div className="email-meta-row">
            <span className="email-meta-label">De:</span>
            <span className="email-meta-value">
              <strong>{caso.sender_name}</strong> &lt;
              <span className="email-sender-address">{caso.sender_email}</span>&gt;
            </span>
          </div>
          <div className="email-meta-row">
            <span className="email-meta-label">Para:</span>
            <span className="email-meta-value">{nickname ? `${nickname}@corporativo.com` : 'usuario@corporativo.com'}</span>
          </div>
          <div className="email-meta-row" style={{ marginTop: '0.6rem' }}>
            <span className="email-meta-label">Asunto:</span>
            <span className="email-subject">{caso.subject}</span>
          </div>
        </div>

        <div className="email-body-content">
          <p>{caso.body}</p>

          {caso.display_url && (
            <div className="email-link-preview">
              <span className="link-icon">🔗</span>
              <div>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block' }}>
                  ENLACE ADJUNTO DETECTADO:
                </span>
                <span className="link-url">{caso.display_url}</span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Opciones de respuesta o Feedback */}
      {!feedback ? (
        <div className="email-actions-container">
          <div className="hint-section">
            {!pista ? (
              <button
                type="button"
                className="hint-btn"
                onClick={handlePedirPista}
              >
                💡 Solicitar Pista (-30% puntos)
              </button>
            ) : (
              <div className="hint-text-box">
                <strong>💡 Pista:</strong> {pista}
              </div>
            )}
          </div>

          <div className="decision-buttons">
            <button
              className="btn-choice btn-legit"
              onClick={() => handleResponder(false)}
              disabled={enviando}
            >
              ✅ Es Legítimo (Seguro)
            </button>
            <button
              className="btn-choice btn-phishing"
              onClick={() => handleResponder(true)}
              disabled={enviando}
            >
              🚨 Es Phishing (Malicioso)
            </button>
          </div>
        </div>
      ) : (
        <div className="feedback-card">
          <div className="fb-header">
            <span
              className="fb-title"
              style={{ color: feedback.correcta ? 'var(--accent)' : 'var(--danger)' }}
            >
              {feedback.correcta ? '🎉 ¡Respuesta Correcta!' : '❌ Respuesta Incorrecta'}
            </span>
            <span
              className="fb-pts"
              style={{ color: feedback.puntos_ganados > 0 ? 'var(--accent)' : 'var(--danger)' }}
            >
              {feedback.puntos_ganados > 0 ? `+${feedback.puntos_ganados}` : feedback.puntos_ganados} pts
            </span>
          </div>

          {feedback.indicadores && feedback.indicadores.length > 0 && (
            <div>
              <div className="fb-indicators-title">Indicadores clave de esta amenaza:</div>
              {feedback.indicadores.map((ind, i) => (
                <div key={i} className="fb-indicator-item">
                  <div className="fb-ind-label">⚠️ {ind.label}</div>
                  <div className="fb-ind-desc">{ind.description}</div>
                </div>
              ))}
            </div>
          )}

          {feedback.educational_tip && (
            <div className="fb-tip-box">
              <strong>💡 Consejo de Seguridad:</strong> {feedback.educational_tip}
            </div>
          )}

          <button className="btn-next-case" onClick={handleSiguienteCaso}>
            {feedback.completado ? 'Ver Resultados del Reto 2 ➔' : 'Siguiente Caso ➔'}
          </button>
        </div>
      )}
    </main>
  );
}
