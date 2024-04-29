import { AxiosError } from 'axios';
import { useState, useCallback, useEffect } from 'react';
import { updateModel } from '../api/digitalTwinsModels';
import moment from 'moment';
import { errorResp, resp } from '../types/api';
import { GraphType } from '../types/graph';
import { data2Graph } from '../utils/data2Graph';
import { CommonDigitalTwinsParameter } from '../types/models/common';

export const useControlPlayer = <T extends CommonDigitalTwinsParameter, G>(
  url: string,
  model: T
) => {
  const [data, setData] = useState<G | undefined>();

  const [historicData, setHistoricData] = useState<any>({});

  const [lastTime, setLastTime] = useState<moment.Moment | null>();

  const [graphs, setGraphs] = useState<GraphType[]>();

  const [isPlaying, setIsPlaying] = useState(false);

  const [error, setError] = useState('');

  const queryApi = useCallback(() => {
    updateModel<T, resp<G>>(url, model)
      .then((resp) => {
        if (isPlaying) {
          setData((_) => {
            const d = resp.data.model;
            for (const key in d) {
              setHistoricData((oldState: any) => {
                if (oldState[key] === undefined) {
                  oldState[key] = [];
                }
                oldState[key].push(d[key]);
                return oldState;
              });
            }
            setHistoricData((oldState: any) => {
              if (oldState['time'] === undefined) {
                const newDate = moment();
                setLastTime(newDate);
                oldState['time'] = [newDate.format('LTS')];
              } else {
                const newDate = moment(lastTime).add(
                  model.timeMultiplier.value *
                    Math.floor(model.queryTime / 1000),
                  's'
                );
                setLastTime(newDate);
                oldState['time'].push(newDate.format('LTS'));
              }
              return oldState;
            });
            setGraphs(data2Graph(historicData));
            return d;
          });
          setError('');
        }
      })
      .catch((err: AxiosError<errorResp>) => {
        setIsPlaying(false);
        setError(
          `Error al realizar la consulta con el código: ${
            err.response?.status
          } y con mensaje de error: ${
            err.response?.data.message
          } y fecha ${moment()}`
        );
      })
      .finally(() => {});
  }, [historicData, isPlaying, model, url, lastTime]);

  useEffect(() => {
    setLastTime(moment());
  }, [isPlaying]);

  useEffect(() => {
    const interval: NodeJS.Timer = setInterval(() => {
      if (isPlaying) {
        queryApi();
      }
    }, model.queryTime);
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
    setHistoricData({});
    setGraphs(undefined);
    setError('');
  };

  return [data, graphs, isPlaying, error, onPlay, onPause, onStop] as const;
};
