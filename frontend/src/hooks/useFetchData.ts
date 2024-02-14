import { useEffect, useState } from 'react';
import api from '../api/api';

export const useFetchData = <BodyType extends any, RespType extends any>(
  url: string,
  body: BodyType
) => {
  const [data, setData] = useState<RespType | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    const fetchData = async (): Promise<void> => {
      try {
        setLoading(true);
        api
          .post<RespType>(url, body)
          .then((res) => {
            setError(null);
            setData(res.data);
          })
          .catch((error) => {
            setError(error);
          })
          .finally(() => {
            setLoading(false);
          });
      } catch (error) {
        setError(error as string);
      }
    };
    fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [url]);
  return [data, error, loading] as const;
};
