import { AxiosError } from 'axios';
import { useState, useCallback, useEffect } from 'react';
import { modelsAPI } from '../api/digitalTwinsModels';
import moment from 'moment';
import { errorResp, resp } from '../types/api';
import { ChartValues } from '../types/graph';
import { data2Graph } from '../utils/data2Graph';
import { CommonDigitalTwinsParameter } from '../types/models/common';
import { useAppDispatch } from '../redux/reduxHooks';
import { setError } from '../redux/slices/errorSlice';

export const useControlPlayer = <T extends CommonDigitalTwinsParameter, G>(
  url: string,
  model: T
) => {
  const dispatch = useAppDispatch();
  const [data, setData] = useState<G | undefined>();

  const [historicData, setHistoricData] = useState<any>({});

  const [charts, setCharts] = useState<ChartValues>();

  const [isPlaying, setIsPlaying] = useState(false);

  const queryApi = useCallback(() => {
    modelsAPI<T, resp<G>>(url, model)
      .then((resp) => {
        if (isPlaying) {
          model.iteration += 1;
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
                oldState['time'] = [newDate];
              } else {
                const newDate = moment(
                  oldState['time'][oldState['time'].length - 1]
                ).add(
                  model.timeMultiplier.value *
                    Math.floor(model.queryTime / 1000),
                  's'
                );
                oldState['time'].push(newDate);
              }
              return oldState;
            });
            setCharts(data2Graph(historicData));
            return d;
          });
          resetErrorState();
        }
      })
      .catch((err: AxiosError<errorResp>) => {
        setIsPlaying(false);
        dispatch(
          setError({
            isShown: true,
            message: `${moment()}: Error al realizar la consulta con el código: ${
              err.code
            } y con mensaje de error: ${err.message}`,
          })
        );
      })
      .finally(() => {});
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [historicData, isPlaying, model, url]);

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
    setIsPlaying(true);
  };

  const resetErrorState = () => {
    dispatch(
      setError({
        isShown: false,
        message: '',
      })
    );
  };

  const onPause = () => {
    setIsPlaying(false);
    resetErrorState();
  };

  const onStop = () => {
    model.iteration = 1;
    setIsPlaying(false);
    setData(undefined);
    setHistoricData({});
    setCharts(undefined);
    resetErrorState();
  };

  return [data, charts, isPlaying, onPlay, onPause, onStop] as const;
};
