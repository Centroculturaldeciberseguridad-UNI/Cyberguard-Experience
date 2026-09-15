import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api';

const RETOS = {
  1: {
    titulo: 'Contraseñas Seguras',
    descripcion:
      'El 81% de las brechas de seguridad involucran contraseñas débiles o robadas. En este reto evaluamos tu capacidad para crear contraseñas que realmente protejan tus cuentas.',
    puntos: 200,
    apiCall: api.completarReto1,
    next: '/reto2',
    color: '#00b4d8',
  },
  2: {
    titulo: 'Detección de Phishing',
    descripcion:
      'El phishing representa el 36% de todas las violaciones de datos. En este reto evaluamos tu capacidad para identificar correos y mensajes fraudulentos.',
    puntos: 300,
    apiCall: api.completarReto2,
    next: '/reto3',
    color: '#ff3366',
  },
};

export default function RetoIntro({ retoNum, nickname, setNickname }) {
  const navigate = useNavigate();
  const [estado, setEstado] = useState('loading');
  const [error, setError] = useState('');
  const reto = RETOS[retoNum];

  /* Redirigir si no hay nickname */
  useEffect(() => {
    if (!nickname) navigate('/');
  }, [nickname, navigate]);

  /* Flujo automatico */
  useEffect(() => {
    if (!nickname || !reto) return;

    let cancelled = false;

    const run = async () => {
      // 1. Verificar si ya esta completado
      try {
        const estadoR = await api.obtenerEstadoRetos(nickname);
        if (estadoR[`reto${retoNum}`]) {
          if (!cancelled) setEstado('ya_completado');
          await new Promise((r) => setTimeout(r, 1500));
          if (!cancelled) navigate(reto.next);
          return;
        }
      } catch {
        // Si falla, continuamos
      }

      // 2. Mostrar intro
      if (!cancelled) setEstado('intro');
      await new Promise((r) => setTimeout(r, 2500));
      if (cancelled) return;

      // 3. Completando
      if (!cancelled) setEstado('completando');
      try {
        await reto.apiCall(nickname);
      } catch (err) {
        if (err.status === 409) {
          // Ya completado, ok
        } else {
          if (!cancelled) setError(err.message);
          return;
        }
      }
      await new Promise((r) => setTimeout(r, 2000));
      if (cancelled) return;

      // 4. Listo
      if (!cancelled) setEstado('done');
      await new Promise((r) => setTimeout(r, 2000));
      if (!cancelled) navigate(reto.next);
    };

    run();
    return () => { cancelled = true; };
  }, [nickname, retoNum]);

  if (!reto) return null;

  return (
    <main className="ri-page">
      <div className="ri-card">
        <div className="ri-number" style={{ color: reto.color }}>
          {String(retoNum).padStart(2, '0')}
        </div>

        <h1 className="ri-title">{reto.titulo}</h1>

        {estado === 'loading' && (
          <p className="ri-status ri-muted">Verificando...</p>
        )}

        {estado === 'ya_completado' && (
          <>
            <p className="ri-status ri-muted">
              Ya completaste este reto anteriormente.
            </p>
            <p className="ri-status ri-muted">Continuando...</p>
          </>
        )}

        {estado === 'intro' && (
          <>
            <p className="ri-desc">{reto.descripcion}</p>
            <div className="ri-bar-wrap">
              <div className="ri-bar-fill" style={{ width: '0%', background: reto.color }} />
            </div>
            <p className="ri-status ri-muted">Preparando evaluación...</p>
          </>
        )}

        {estado === 'completando' && (
          <>
            <p className="ri-desc">{reto.descripcion}</p>
            <div className="ri-bar-wrap">
              <div
                className="ri-bar-fill ri-bar-animate"
                style={{ background: reto.color }}
              />
            </div>
            <p className="ri-status" style={{ color: reto.color }}>
              Evaluando...
            </p>
          </>
        )}

        {estado === 'done' && (
          <>
            <div className="ri-check">&#10003;</div>
            <p className="ri-pts">
              Reto completado: <strong>{reto.puntos} puntos</strong>
            </p>
            <p className="ri-status ri-muted">Continuando al siguiente reto...</p>
          </>
        )}

        {error && (
          <div className="ri-error">
            <p>{error}</p>
            <button className="btn btn-primary" onClick={() => window.location.reload()}>
              Reintentar
            </button>
          </div>
        )}
      </div>
    </main>
  );
}