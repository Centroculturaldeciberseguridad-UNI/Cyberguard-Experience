import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api';

export default function RegistroNickname({ nickname, setNickname }) {
  const [input, setInput] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const data = await api.registrarNickname(input.trim());
      setNickname(data.nickname);
      navigate('/reto3');
    } catch (err) {
      if (err.status === 409) {
        setError('Ese nickname ya está en uso. Elige otro.');
      } else {
        setError(err.message || 'Error al registrar. Intenta de nuevo.');
      }
    } finally {
      setLoading(false);
    }
  };

  if (nickname) {
    return (
      <div className="registro-registrado">
        <p className="registro-saludo">
          Hola, <span className="registro-nombre">{nickname}</span>
        </p>
        <button className="btn btn-primary" onClick={() => navigate('/reto3')}>
          Ir al Reto OSINT &rarr;
        </button>
      </div>
    );
  }

  return (
    <form className="registro-form" onSubmit={handleSubmit}>
      <div className="registro-input-group">
        <span className="registro-prompt">&gt;_</span>
        <input
          type="text"
          className="input registro-input"
          placeholder="Ingresa tu nickname..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          maxLength={30}
          autoFocus
        />
        <button
          type="submit"
          className="btn btn-primary"
          disabled={loading || input.trim().length < 3}
        >
          {loading ? '...' : 'Registrarse'}
        </button>
      </div>
      {error && <p className="registro-error">{error}</p>}
      <p className="registro-hint">
        3-30 caracteres. Solo letras, numeros y guiones.
      </p>
    </form>
  );
}