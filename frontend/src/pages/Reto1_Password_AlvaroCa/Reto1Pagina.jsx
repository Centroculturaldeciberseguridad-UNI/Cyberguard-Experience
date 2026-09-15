import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../../api';
import './Reto1Pagina.css';

export default function Reto1Pagina({ nickname, setNickname }) {
  const navigate = useNavigate();
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [guardando, setGuardando] = useState(false);
  const [mejorPuntaje, setMejorPuntaje] = useState(0);
  const [intentos, setIntentos] = useState(0);

  useEffect(() => {
    if (!nickname) {
      navigate('/');
    }
  }, [nickname, navigate]);

  const handleEvaluar = async (e) => {
    if (e) e.preventDefault();
    if (!password.trim() || loading) return;

    try {
      setLoading(true);
      const res = await api.evaluarPassword(nickname, password);
      setData(res);
      setIntentos((prev) => prev + 1);
      if (res.puntaje > mejorPuntaje) {
        setMejorPuntaje(res.puntaje);
      }
    } catch (err) {
      console.error('Error evaluando password:', err);
      alert(err.message || 'Error al evaluar la contraseña');
    } finally {
      setLoading(false);
    }
  };

  const handleProbarEjemplo = (ejemplo) => {
    setPassword(ejemplo);
    setData(null);
  };

  const handleCompletar = async () => {
    if (!data) return;
    try {
      setGuardando(true);
      const puntosFinales = Math.max(mejorPuntaje, data?.puntaje || 0);
      await api.completarReto1(nickname, puntosFinales);
      navigate('/reto2');
    } catch (err) {
      console.error('Error al completar reto 1:', err);
      alert(err.message || 'Error al guardar puntaje');
    } finally {
      setGuardando(false);
    }
  };

  const nivelColor = () => {
    if (!data) return '#5a5a72';
    switch (data.nivel) {
      case 1: return '#ff3366';
      case 2: return '#ffaa00';
      case 3: return '#00b4d8';
      case 4: return '#00f2fe';
      case 5: return '#00ff88';
      default: return '#5a5a72';
    }
  };

  return (
    <main className="reto1-container">
      <header className="reto1-header">
        <span className="reto1-badge-num">RETO 01 / 03</span>
        <h1 className="reto1-title">Simulador de Fuerza Bruta y Contraseñas</h1>
        <p className="reto1-subtitle">
          El 81% de las brechas ocurren por contraseñas vulnerables. Pon a prueba tu capacidad creando una contraseña resistente ante clústeres de fuerza bruta.
        </p>
      </header>

      <div className="reto1-card">
        {/* Formulario de Input de contraseña y botón de evaluación */}
        <form className="password-form" onSubmit={handleEvaluar}>
          <div className="password-input-row">
            <div className="password-input-wrap">
              <input
                type={showPassword ? 'text' : 'password'}
                className="password-input"
                placeholder="Escribe tu contraseña a evaluar..."
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value);
                  if (data) setData(null);
                }}
                maxLength={100}
                autoFocus
              />
              <button
                type="button"
                className="toggle-pwd-btn"
                onClick={() => setShowPassword(!showPassword)}
                title={showPassword ? 'Ocultar' : 'Mostrar'}
              >
                {showPassword ? '👁️' : '🔒'}
              </button>
            </div>

            <button
              type="submit"
              className="btn-evaluar-password"
              disabled={loading || !password.trim()}
            >
              {loading ? (
                <>
                  <span className="spinner-mini"></span> Auditando...
                </>
              ) : (
                '🔍 Auditar Contraseña'
              )}
            </button>
          </div>
        </form>

        {/* Muestras rápidas */}
        <div className="quick-samples">
          <span>Probar patrones comunes:</span>
          <button type="button" className="sample-chip" onClick={() => handleProbarEjemplo('123456')}>123456</button>
          <button type="button" className="sample-chip" onClick={() => handleProbarEjemplo('password2026')}>password2026</button>
          <button type="button" className="sample-chip" onClick={() => handleProbarEjemplo(nickname ? `${nickname}123` : 'usuario123')}>{nickname ? `${nickname}123` : 'usuario123'}</button>
          <button type="button" className="sample-chip" onClick={() => handleProbarEjemplo('Sol*Luna#9921!')}>Sol*Luna#9921!</button>
          <button type="button" className="sample-chip" onClick={() => handleProbarEjemplo('X9$kL#8mQ!vW@2zT')}>X9$kL#8mQ!vW@2zT</button>
        </div>

        {/* Estado previo: Instrucciones antes de evaluar */}
        {!data && !loading && (
          <div className="reto1-instructions-box">
            <div className="instructions-icon">🛡️</div>
            <div className="instructions-body">
              <h3>Ingresa tu propuesta y presiona "Auditar Contraseña"</h3>
              <p>
                Los resultados de seguridad, nivel de robustez, entropía de Shannon, tiempo de crackeo y puntaje se revelarán una vez envíes tu contraseña a auditoría.
              </p>
            </div>
          </div>
        )}

        {/* Loader durante el análisis */}
        {loading && (
          <div className="evaluating-box">
            <div className="evaluating-spinner"></div>
            <p>Ejecutando simulación de ataque y midiendo entropía criptográfica...</p>
          </div>
        )}

        {/* Resultados: Solo se muestran una vez enviada y evaluada la contraseña */}
        {data && !loading && (
          <div className="reto1-results-section">
            {/* Medidor de nivel */}
            <div className="meter-container">
              <div className="meter-header">
                <span className="meter-level-name" style={{ color: nivelColor() }}>
                  Nivel: {data.nivel_nombre}
                </span>
                <span
                  className="meter-pts-badge"
                  style={{
                    backgroundColor: `${nivelColor()}22`,
                    color: nivelColor(),
                    border: `1px solid ${nivelColor()}66`
                  }}
                >
                  Puntaje obtenido: {data.puntaje} / 200 pts
                </span>
              </div>
              <div className="meter-track">
                <div
                  className="meter-fill"
                  style={{
                    width: `${(data.nivel / 5) * 100}%`,
                    backgroundColor: nivelColor()
                  }}
                />
              </div>
            </div>

            {/* Grilla de Métricas */}
            <div className="metrics-grid">
              <div className="metric-card">
                <div className="metric-label">Longitud (L)</div>
                <div className="metric-value">{data.longitud} carac.</div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Alfabeto (R)</div>
                <div className="metric-value">{data.tamano_alfabeto} tipos</div>
                <div className="charset-badges">
                  <span className={`charset-badge ${data.tiene_minusculas ? 'active' : ''}`}>a-z</span>
                  <span className={`charset-badge ${data.tiene_mayusculas ? 'active' : ''}`}>A-Z</span>
                  <span className={`charset-badge ${data.tiene_numeros ? 'active' : ''}`}>0-9</span>
                  <span className={`charset-badge ${data.tiene_simbolos ? 'active' : ''}`}>!@#</span>
                </div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Entropía Shannon</div>
                <div className="metric-value">{data.entropia_bits} bits</div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Tiempo (10^10 hashes/s)</div>
                <div className="metric-value" style={{ fontSize: '1rem', color: nivelColor() }}>
                  {data.tiempo_legible}
                </div>
              </div>
            </div>

            {/* Comparativa Hardware */}
            {data.tiempos_hardware && (
              <div className="hardware-box">
                <div className="hardware-title">
                  ⚡ <strong>Simulación de Ataque por Potencia de Hardware:</strong>
                </div>
                <div className="hardware-list">
                  <div className="hardware-item">
                    <span className="hw-name">💻 PC de Hogar (CPU 10 MH/s)</span>
                    <span className="hw-time">{data.tiempos_hardware.cpu_antiguo}</span>
                  </div>
                  <div className="hardware-item">
                    <span className="hw-name">🎮 GPU Gaming RTX (1 GH/s)</span>
                    <span className="hw-time">{data.tiempos_hardware.gpu_gaming}</span>
                  </div>
                  <div className="hardware-item">
                    <span className="hw-name">⛏️ Clúster Minero (10 GH/s)</span>
                    <span className="hw-time">{data.tiempos_hardware.rig_mineria}</span>
                  </div>
                  <div className="hardware-item">
                    <span className="hw-name">🌐 Supercomputador (1 TH/s)</span>
                    <span className="hw-time">{data.tiempos_hardware.supercomputadora}</span>
                  </div>
                </div>
              </div>
            )}

            {/* Alertas de vulnerabilidades */}
            {data.tiene_vulnerabilidad && data.vulnerabilidades.length > 0 && (
              <div className="vuln-alert">
                <div className="vuln-alert-title">🚨 Vulnerabilidades Detectadas:</div>
                <ul className="vuln-list">
                  {data.vulnerabilidades.map((v, idx) => (
                    <li key={idx}>• {v}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Feedback / Sugerencias */}
            <div className="feedback-box">
              <p>{data.feedback}</p>
            </div>

            {/* Mensaje de optimización si desea mejorar */}
            <div className="reintentar-hint">
              <span>💡 ¿Deseas mejorar tu puntaje? Puedes cambiar la contraseña arriba y presionar <strong>"Auditar Contraseña"</strong> nuevamente.</span>
            </div>
          </div>
        )}

        {/* Footer y botón para completar */}
        <div className="reto1-footer-actions">
          <div className="intentos-tracker">
            Participante: <strong>{nickname}</strong> | {data ? (
              <>Puntaje actual: <strong>{data.puntaje} / 200 pts</strong> | Mejor marca: <strong>{mejorPuntaje} / 200 pts</strong></>
            ) : (
              <span>Audita una contraseña para obtener puntaje</span>
            )}
          </div>
          <button
            className="btn-completar-reto1"
            onClick={handleCompletar}
            disabled={guardando || !data}
            title={!data ? 'Primero debes auditar una contraseña' : 'Continuar al Reto 2'}
          >
            {guardando ? 'Guardando puntaje...' : 'Guardar y Continuar al Reto 2 ➔'}
          </button>
        </div>
      </div>
    </main>
  );
}

