import { saveAs } from 'file-saver';
import { utils, write } from 'xlsx';

import { array2CSV } from './array2CSV';

export const DownloadCSV = (
  columns: Array<Array<number | string>>,
  headers: Array<string>,
  fileName: string
) => {
  var blob = new Blob([array2CSV(columns, headers)], {
    type: 'text/csv;charset=default',
  });
  saveAs(blob, `${fileName}.xlsx`);
};

export const DownloadExcel = (
  data: Array<Array<number | string>>,
  fileName: string
) => {
  const worksheet = utils.json_to_sheet(data);
  const workbook = utils.book_new();
  utils.book_append_sheet(workbook, worksheet, 'Data');
  const excelBuffer = write(workbook, { bookType: 'xlsx', type: 'array' });
  const blob = new Blob([excelBuffer], { type: 'application/octet-stream' });
  saveAs(blob, `${fileName}.xlsx`);
};
