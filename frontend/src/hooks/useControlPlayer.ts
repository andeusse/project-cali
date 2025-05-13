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
import Constants from '../config/constants';

export const useControlPlayer = <T extends CommonDigitalTwinsParameter, G>(
  url: string,
  model: T
) => {
  const dispatch = useAppDispatch();
  const [failureCount, setFailureCount] = useState(0);

  const [data, setData] = useState<G | undefined>();

  const [historicData, setHistoricData] = useState<any>({});

  const [charts, setCharts] = useState<ChartValues>();

  const [isPlaying, setIsPlaying] = useState(false);

  const [firstQuery, setFirstQuery] = useState(true);

  const [errorMessage, setErrorMessage] = useState<
    AxiosError<errorResp> | undefined
  >(undefined);

  const resetErrorState = useCallback(() => {
    dispatch(
      setError({
        isShown: false,
        message: '',
      })
    );
  }, [dispatch]);

  useEffect(() => {
    if (
      failureCount >= Constants.MAX_RETRIES_BEFORE_STOP &&
      errorMessage !== undefined
    ) {
      setFailureCount(0);
      setIsPlaying(false);
      dispatch(
        setError({
          isShown: true,
          message: Constants.GetErrorWithDate(
            errorMessage.message,
            errorMessage.code
          ),
        })
      );
    }
  }, [dispatch, errorMessage, failureCount]);

  const queryApi = useCallback(() => {
    modelsAPI<T, resp<G>>(url, model)
      .then((resp) => {
        if (isPlaying || firstQuery) {
          setFirstQuery(false);
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
                const newDate: moment.Moment = moment();
                oldState['time'] = [newDate];
              } else {
                var newDate: moment.Moment = moment();
                if (model.digitalTwinStepTime !== undefined) {
                  newDate = moment(
                    oldState['time'][oldState['time'].length - 1]
                  ).add(
                    model.timeMultiplier.value *
                      Math.floor(model.digitalTwinStepTime.value),
                    's'
                  );
                } else {
                  newDate = moment(
                    oldState['time'][oldState['time'].length - 1]
                  ).add(
                    model.timeMultiplier.value *
                      Math.floor(model.queryTime / 1000),
                    's'
                  );
                }
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
        setFailureCount((prev) => prev + 1);
        setErrorMessage(err);
      })
      .finally(() => {});
  }, [firstQuery, historicData, isPlaying, model, resetErrorState, url]);

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
    queryApi();
  };

  const onPause = () => {
    setIsPlaying(false);
    setFirstQuery(true);
    resetErrorState();
  };

  const onStop = () => {
    model.iteration = 1;
    setIsPlaying(false);
    setFirstQuery(true);
    setData(undefined);
    setHistoricData({});
    setCharts(undefined);
    resetErrorState();
    setFailureCount(0);
  };

  return [data, charts, isPlaying, onPlay, onPause, onStop] as const;
};
