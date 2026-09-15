import { useNavigate } from 'react-router-dom';
import RegistroNickname from '../components/RegistroNickname';
import Ranking from '../components/Ranking';

export default function Home({ nickname, setNickname }) {
  const navigate = useNavigate();

  const handleRetoClick = () => {
    if (nickname) {
      navigate('/reto1');
    } else {
      document.querySelector('.registro-input-group')?.scrollIntoView({
        behavior: 'smooth',
        block: 'center',
      });
    }
  };

  return (
    <main className="home">
      <section className="hero">
        <div className="hero-content">
          <h1 className="hero-title">
            ¿Qué tan fácil es comprometer
            <br />
            tu integridad digital?
          </h1>
          <p className="hero-subtitle">
            La última línea de defensa eres tu.
          </p>
          <RegistroNickname nickname={nickname} setNickname={setNickname} />
        </div>
        <div className="hero-decoration">
          <div className="hero-grid" />
        </div>
      </section>

      {/* Retos */}
      <section className="retos-section container">
        <h2 className="section-title">Retos disponibles</h2>
        <div className="retos-grid">
          <div
            className={`reto-card ${nickname ? 'reto-card-active': 'reto-card-disabled'}`}
            onClick={() => nickname && navigate('/reto1')}
            role="button"
            tabIndex={0}
          >
            <div className="reto-card-number">01</div>
            <h3 className="reto-card-title">Contraseñas Seguras</h3>
            <p className="reto-card-desc">
              Aprende a crear contraseñas que realmente protejan tus cuentas.
            </p>
            <span className={`reto-card-badge ${nickname ? 'reto-card-badge-active': ''}`}>
              {nickname ? 'Disponible': 'Registrate'}
            </span>
          </div>

          <div
            className={`reto-card ${nickname ? 'reto-card-active' : 'reto-card-disabled'}`}
            onClick={() => nickname && navigate('/reto2')}
            role="button"
            tabIndex={0}
          >
            <div className="reto-card-number">02</div>
            <h3 className="reto-card-title">Detección de Phishing</h3>
            <p className="reto-card-desc">
              ¿Puedes identificar un correo falso? Pon a prueba tu criterio.
            </p>
            <span className={`reto-card-badge ${nickname ? 'reto-card-badge-active' : ''}`}>
              {nickname ? 'Disponible' : 'Registrate'}
            </span>
          </div>

          <div
            className={`reto-card ${nickname ? 'reto-card-active' : 'reto-card-disabled'}`}
            onClick={() => nickname && navigate('/reto3')}
            role="button"
            tabIndex={0}
          >
            <div className="reto-card-number">03</div>
            <h3 className="reto-card-title">Investigacion OSINT</h3>
            <p className="reto-card-desc">
              Descubre cuanta información se puede encontrar sobre alguien en
              internet.
            </p>
            <span className={`reto-card-badge ${nickname ? 'reto-card-badge-active' : ''}`}>
              {nickname ? 'Disponible' : 'Registrate'}
            </span>
          </div>
        </div>
      </section>

      {/* Ranking */}
      <section className="ranking-section container">
        <Ranking />
      </section>
    </main>
  );
}