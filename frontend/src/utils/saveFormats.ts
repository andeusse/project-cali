import { array2CSV } from './array2CSV';
import { saveAs } from 'file-saver';

export const DownloadCSV = (
  columns: Array<Array<number | string>>,
  headers: Array<string>,
  fileName: string
) => {
  var blob = new Blob([array2CSV(columns, headers)], {
    type: 'text/csv;charset=utf-8',
  });
  saveAs(blob, `${fileName}.csv`);
};
