import { useState } from 'react';
import { api } from '../../api';
import './PanelHallazgos.css';

export default function PanelHallazgos({
  pistas,
  progreso,
  nickname,
  onHallazgoSubmitted,
  onRetoCompleted,
  onVerResultados,
  segundosRestantes,
  onFinalizar,
}) {
  const [inputs, setInputs] = useState({});
  const [loadingClave, setLoadingClave] = useState(null);
  const [resultados, setResultados] = useState({});
  const [pistaPagada, setPistaPagada] = useState(null);
  const [loadingPP, setLoadingPP] = useState(false);

  const [pwInput, setPwInput] = useState('');
  const [loadingPw, setLoadingPw] = useState(false);
  const [pwResult, setPwResult] = useState(null);

  const hallazgosMap = {};
  if (progreso?.hallazgos) {
    progreso.hallazgos.forEach((h) => { hallazgosMap[h.clave] = h; });
  }

  const datosConfirmados = pistas
    .filter((p) => hallazgosMap[p.clave]?.es_correcto)
    .map((p) => ({ etiqueta: p.etiqueta, valor: hallazgosMap[p.clave].valor_ingresado }));

  const intentosUsados = progreso?.intentos_password?.length || 0;
  const retoCompletado = progreso?.reto_completado || false;
  const puntosH = progreso?.puntos_hallazgos || 0;
  const puntosP = progreso?.puntos_password || 0;
  const maxPuntosH = pistas.reduce((s, p) => s + p.puntos, 0);
  const tiempoAgotado = segundosRestantes !== null && segundosRestantes <= 0;
  const bloqueado = retoCompletado || tiempoAgotado;

  const formatTiempo = (s) => {
    if (s === null || s === undefined) return '--:--';
    const m = Math.floor(s/60).toString().padStart(2, '0');
    const sec = (s%60).toString().padStart(2, '0');
    return `${m}:${sec}`;
  };

  const onChange = (clave, val) =>
    setInputs((prev) => ({ ...prev, [clave]: val }));

  const submitHallazgo = async (clave, conPistaPagada = false) => {
    const valor = inputs[clave]?.trim();
    if (!valor) return;
    setLoadingClave(clave);
    try {
      const res = conPistaPagada
        ? await api.usarPistaPagada(nickname, clave, valor)
        : await api.enviarHallazgo(nickname, clave, valor);
      setResultados((prev) => ({ ...prev, [clave]: res }));
      onHallazgoSubmitted();
    } catch (err) {
      setResultados((prev) => ({ ...prev, [clave]: { error: err.message } }));
    } finally {
      setLoadingClave(null);
    }
  };

  const pedirPistaPagada = async (clave) => {
    setLoadingPP(true);
    try {
      const info = await api.obtenerInfoPistaPagada(clave);
      setPistaPagada(info);
    } catch { setPistaPagada(null); }
    finally { setLoadingPP(false); }
  };

  const submitPassword = async () => {
    if (!pwInput.trim()) return;
    setLoadingPw(true);
    try {
      const res = await api.intentarPassword(nickname, pwInput.trim());
      setPwResult(res);
      setPwInput('');
      onRetoCompleted();
    } catch (err) {
      setPwResult({ error: err.message });
    } finally {
      setLoadingPw(false);
    }
  };

  return (
    <div className="ph">
      <div className="ph-head">
        <h2 className="ph-title">Expediente OSINT</h2>
        <div className="ph-head-right">
          <span className={`ph-timer ${segundosRestantes !== null && segundosRestantes <= 60 ? 'ph-timer-urgente': ''}`}>
            ⏱ {formatTiempo(segundosRestantes)}
          </span>
        </div>
        <div className="ph-score">
          <span className="ph-score-num">{puntosH + puntosP}</span>
          <span className="ph-score-max">/ {maxPuntosH + 200} pts</span>
        </div>
      </div>

      {/* Bloque A */}
      <div className="ph-block">
        <h3 className="ph-block-title">Datos personales</h3>
        <p className="ph-block-desc">
          Investiga los perfiles del sandbox y completa cada campo.
        </p>

        {pistas.map((pista) => {
          const guardado = hallazgosMap[pista.clave];
          const local = resultados[pista.clave];
          const yaOk = guardado || (local && local.es_correcto !== undefined);
          const correcto = guardado?.es_correcto ?? local?.es_correcto;
          const pts = guardado?.puntos_obtenidos ?? local?.puntos_obtenidos;

          return (
            <div key={pista.clave} className={`ph-pista ${yaOk ? 'ph-pista-done' : ''}`}>
              <div className="ph-pista-top">
                <span className="ph-pista-q">{pista.pregunta}</span>
                <span className="ph-pista-pts">{pista.puntos} pts</span>
              </div>

              {yaOk ? (
                <div className={`ph-res ${correcto ? 'ph-res-ok' : 'ph-res-fail'}`}>
                  {correcto ? `Correcto (+${pts} pts)` : `Incorrecto (${pts} pts)`}
                </div>
              ) : (
                <>
                  <div className="ph-pista-row">
                    <input
                      className="input ph-input"
                      placeholder="Tu respuesta..."
                      value={inputs[pista.clave] || ''}
                      onChange={(e) => onChange(pista.clave, e.target.value)}
                      disabled={bloqueado}
                    />
                    <button
                      className="btn btn-primary btn-sm"
                      onClick={() => submitHallazgo(pista.clave)}
                      disabled={loadingClave === pista.clave || !inputs[pista.clave]?.trim() || bloqueado}
                    >
                      {loadingClave === pista.clave ? '...' : 'Enviar'}
                    </button>
                  </div>

                  {local?.error && <p className="ph-err">{local.error}</p>}

                  {pista.tiene_pista_pagada && !retoCompletado && (
                    <div className="ph-pp">
                      {pistaPagada?.clave === pista.clave ? (
                        <div className="ph-pp-box">
                          <p className="ph-pp-text">{pistaPagada.texto_pista}</p>
                          <p className="ph-pp-cost">(Costo: -{pistaPagada.costo_pista} pts si aciertas)</p>
                          <button
                            className="btn btn-sm"
                            onClick={() => submitHallazgo(pista.clave, true)}
                            disabled={loadingClave === pista.clave || !inputs[pista.clave]?.trim()}
                          >
                            Enviar con pista pagada
                          </button>
                        </div>
                      ) : (
                        <button
                          className="btn btn-sm ph-pp-btn"
                          onClick={() => pedirPistaPagada(pista.clave)}
                          disabled={loadingPP}
                        >
                          {loadingPP ? '...' : 'Pedir pista (-10 pts)'}
                        </button>
                      )}
                    </div>
                  )}
                </>
              )}
            </div>
          );
        })}
      </div>

      {/* Datos confirmados */}
      {datosConfirmados.length > 0 && (
        <div className="ph-block ph-confirmados">
          <h3 className="ph-block-title">Datos Confirmados</h3>
          <ul className="ph-confirmados-lista">
            {datosConfirmados.map((d) => (
              <li key={d.etiqueta} className="ph-confirmado-item">
                <span className="ph-confirmado-label">{d.etiqueta}:</span>
                <span className="ph-confirmado-valor">{d.valor}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Bloque B */}
      <div className="ph-block ph-pw-block">
        <h3 className="ph-block-title">Contraseña corporativa</h3>
        <p className="ph-block-desc">
          Usa la información recopilada para intentar adivinar la contraseña de la cuenta corporativa de Marco.
        </p>
        <p className="ph-pw-hint">
          Intento 1: 200 pts &middot; Intento 2: 120 pts &middot; Intento 3: 60 pts
        </p>

        {retoCompletado ? (
          <div className="ph-pw-done">
            <p className="ph-pw-done-title">
              {progreso?.intentos_password?.some((i) => i.es_correcto)
                ? 'Contraseña descifrada!'
                : 'Se agotaron los intentos.'}
            </p>
            {progreso?.intentos_password?.map((it) => (
              <div key={it.intento_numero} className="ph-pw-intento">
                Intento {it.intento_numero}:{' '}
                <span className={it.es_correcto ? 'ph-res-ok' : 'ph-res-fail'}>
                  {it.es_correcto ? `Correcto (+${it.puntos_obtenidos} pts)` : 'Incorrecto'}
                </span>
              </div>
            ))}
          </div>
        ) : (
          <>
            <div className="ph-pista-row">
              <input
                className="input ph-input"
                placeholder="Contraseña..."
                value={pwInput}
                onChange={(e) => setPwInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && submitPassword()}
                disabled={intentosUsados >= 3 || bloqueado}
              />
              <button
                className="btn btn-primary"
                onClick={submitPassword}
                disabled={loadingPw || !pwInput.trim() || intentosUsados >= 3 || bloqueado}
              >
                {loadingPw ? '...' : 'Intentar'}
              </button>
            </div>
            <p className="ph-pw-count">Intentos usados: {intentosUsados} / 3</p>
            {pwResult?.error && <p className="ph-err">{pwResult.error}</p>}
            <button className="btn btn-sm ph-terminar-btn" onClick={onFinalizar}>
              Terminar reto
            </button>
          </>
        )}
      </div>

      {/* Resultado final */}
      {retoCompletado && (
        <div className="ph-final">
          <h3 className="ph-final-title">Reto completado</h3>
          <p className="ph-final-pts">
            Puntuación final:{' '}
            <strong>{progreso?.puntos_total_reto3 ?? puntosH + puntosP} pts</strong>
          </p>
          <button className="btn btn-primary" onClick={onVerResultados} style={{ marginTop: '1rem' }}>
            Ver resultados finales
          </button>
          <p className="ph-final-auto">Redirección automática en unos segundos...</p>
        </div>
      )}
    </div>
  );
}