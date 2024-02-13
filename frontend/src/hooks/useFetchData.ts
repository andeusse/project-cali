import { useEffect, useState } from 'react';
import api from '../api/api';

export const useFetchData = <T extends any>(url: string, body: T) => {
  const [data, setData] = useState<unknown>(null);
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    const fetchData = async (): Promise<void> => {
      try {
        setLoading(true);
        api
          .get<T>(url)
          .then((res) => {
            setData(JSON.parse(res.data as string));
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
  }, [url]);
  return [data, error, loading] as const;
};
