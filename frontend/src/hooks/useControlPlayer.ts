import { AxiosError } from 'axios';
import { useState, useCallback, useEffect } from 'react';
import { updateModel } from '../api/digitalTwinsModels';
import moment from 'moment';
import { resp } from '../types/api';
import { GraphType } from '../types/graph';
import { data2Graph } from '../utils/data2Graph';

export const useControlPlayer = <T, G>(url: string, model: T) => {
  const [data, setData] = useState<G | undefined>();

  const [historicData, setHistoricData] = useState<any>({});

  const [graphs, setGraphs] = useState<GraphType[]>();

  const [isPlaying, setIsPlaying] = useState(false);

  const [error, setError] = useState('');

  const queryApi = useCallback(() => {
    updateModel<T, resp<G>>(url, model)
      .then((resp) => {
        setData((_) => {
          const d = resp.data.model;
          for (const key in d) {
            setHistoricData((o: any) => {
              if (o[key] === undefined) {
                o[key] = [];
              }
              o[key].push(d[key]);
              return o;
            });
          }
          setHistoricData((o: any) => {
            if (o['time'] === undefined) {
              o['time'] = [];
            }
            o['time'].push(moment().format('LTS'));
            return o;
          });
          setGraphs(data2Graph(historicData));
          return d;
        });
        setError('');
      })
      .catch((err: AxiosError) => {
        setError(`Error al realizar la consulta con el mesaje: ${err.message}`);
      })
      .finally(() => {});
  }, [historicData, model, url]);

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
    setData(undefined);
    setHistoricData(undefined);
    setGraphs(undefined);
    setError('');
  };

  return [data, graphs, isPlaying, error, onPlay, onPause, onStop] as const;
};
