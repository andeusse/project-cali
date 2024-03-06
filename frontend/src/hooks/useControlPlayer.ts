import { AxiosError } from 'axios';
import { useState, useCallback, useEffect } from 'react';
import { updateModel } from '../api/digitalTwinsModels';

export const useControlPlayer = <T, G>(url: string, model: T) => {
  const [data, setData] = useState<G | undefined>(undefined);

  const [isPlaying, setIsPlaying] = useState(false);

  const [error, setError] = useState('');

  const queryApi = useCallback(() => {
    updateModel<T, G>(url, model)
      .then((resp) => {
        setData(resp.data);
        console.log(resp.data);

        setError('');
      })
      .catch((err: AxiosError) => {
        setError(`Error al realizar la consulta con el mesaje: ${err.message}`);
      })
      .finally(() => {});
  }, [model, url]);

  useEffect(() => {
    const interval: NodeJS.Timer = setInterval(() => {
      if (isPlaying) {
        queryApi();
      }
    }, 5000);
    return () => {
      clearInterval(interval);
    };
  }, [isPlaying, queryApi, model]);

  const onPlay = () => {
    queryApi();
    setIsPlaying(true);
  };

  const onPause = () => {
    setIsPlaying(false);
    setError('');
  };

  const onStop = () => {
    setIsPlaying(false);
    setError('');
  };

  return [data, isPlaying, error, onPlay, onPause, onStop] as const;
};
