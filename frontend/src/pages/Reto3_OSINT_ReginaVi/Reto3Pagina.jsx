import { useState, useEffect, useCallback, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../../api';
import PerfilInstagram from './PerfilInstagram';
import PanelHallazgos from './PanelHallazgos';

const PERFIL_FETCHERS = {
  marco: api.obtenerPerfilMarco,
  carlos: api.obtenerPerfilCarlos,
  nexova: api.obtenerPerfilNexova,
  camila: api.obtenerPerfilCamila,
};

export default function Reto3Pagina({ nickname, setNickname }) {
  const navigate = useNavigate();
  const sandboxRef = useRef(null);

  const [currentProfile, setCurrentProfile] = useState('marco');
  const [profileData, setProfileData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [pistas, setPistas] = useState([]);
  const [progreso, setProgreso] = useState(null);
  const [checkingFlow, setCheckingFlow] = useState(true);
  const [segundosRestantes, setSegundosRestantes] = useState(null);

  /* Verificar flujo */
  useEffect(() => {
    if (!nickname) {navigate('/'); return;}
    api.obtenerEstadoRetos(nickname).then((estado) => {
      if (!estado.reto1) navigate('/reto1');
      else if (!estado.reto2) navigate('/reto2');
      else setCheckingFlow(false);
    }).catch(() => setCheckingFlow(false));
  }, [nickname, navigate]);

  /* Cargar perfil del sandbox */
  useEffect(() => {
    if (checkingFlow) return;
    setLoading(true);
    const fetcher = PERFIL_FETCHERS[currentProfile];
    if (fetcher) {
      fetcher()
        .then(setProfileData)
        .catch(console.error)
        .finally(() => setLoading(false));
    }
  }, [currentProfile, checkingFlow]);

  /* Scroll al top al cambiar de perfil */
  useEffect(() => {
    if (sandboxRef.current) sandboxRef.current.scrollTop = 0;
  }, [currentProfile]);

  /* Cargar preguntas de pistas */
  useEffect(() => {
    api.obtenerPistas().then(setPistas).catch(console.error);
  }, []);

  /* Cargar / refrescar progreso */
  const refreshProgreso = useCallback(() => {
    if (!nickname) return;
    api
      .obtenerProgreso(nickname)
      .then(setProgreso)
      .catch((err) => {
        if (err.status === 404) {
          localStorage.removeItem('nickname');
          setNickname('');
          navigate('/');
        }
      });
  }, [nickname, navigate, setNickname]);

  useEffect(() => {
    if (checkingFlow || !nickname) return;
    api.iniciarReto3(nickname).finally(refreshProgreso);
  }, [checkingFlow, nickname, refreshProgreso]);

  /* Sincroniza el cronómetro local con lo que diga el backend */
  useEffect(() => {
    if (progreso?.segundos_restantes !== undefined) {
      setSegundosRestantes(progreso.segundos_restantes);
    }
  }, [progreso]);

  /* Cuenta regresiva visual (1 en 1 segundo) */
  useEffect(() => {
    if (segundosRestantes === null || segundosRestantes <= 0 || progreso?.reto_completado) return;
    const t = setTimeout(() => setSegundosRestantes((s) => Math.max(s-1, 0)), 1000);
    return () => clearTimeout(t);
  }, [segundosRestantes, progreso]);

  /* Reconsulta el progreso cada 5s: detecta si el tiempo se agotó en el backend */
  useEffect(() => {
    if (checkingFlow || progreso?.reto_completado) return;
    const interval = setInterval(refreshProgreso, 5000);
    return () => clearInterval(interval);
  }, [checkingFlow, progreso?.reto_completado, refreshProgreso]);

  /* Navegar a resultados cuando se completa el reto */
  useEffect(() => {
    if (progreso?.reto_completado) {
      const t = setTimeout(() => navigate('/resultado'), 3500);
      return () => clearTimeout(t);
    }
  }, [progreso, navigate]);

  const handleNavigate = (profileId) => {
    if (PERFIL_FETCHERS[profileId]) setCurrentProfile(profileId);
  };

  const handleFinalizar = () => {
    api.finalizarReto3(nickname).finally(refreshProgreso);
  };

  if (!nickname || checkingFlow) return null;

  return (
    <main className="reto3">
      <div className="reto3-layout">
        <div className="reto3-sandbox" ref={sandboxRef}>
          {loading || !profileData ? (
            <div className="reto3-loading">
              <span className="reto3-loading-text">Cargando perfil...</span>
            </div>
          ) : (
            <PerfilInstagram
              profile={profileData}
              onNavigate={handleNavigate}
              currentProfileId={currentProfile}
            />
          )}
        </div>

        <div className="reto3-panel-wrapper">
          <PanelHallazgos
            pistas={pistas}
            progreso={progreso}
            nickname={nickname}
            onHallazgoSubmitted={refreshProgreso}
            onRetoCompleted={refreshProgreso}
            onVerResultados={() => navigate('/resultado')}
            segundosRestantes={segundosRestantes}
            onFinalizar={handleFinalizar}
          />
        </div>
      </div>
    </main>
  );
}