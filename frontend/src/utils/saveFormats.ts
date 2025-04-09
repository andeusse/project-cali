import { saveAs } from 'file-saver';
import { utils, write } from 'xlsx';

export const DownloadCSV = (
  data: Array<Array<number | string | moment.Moment>>,
  fileName: string
) => {
  const worksheet = utils.json_to_sheet(data);
  const workbook = utils.book_new();
  utils.book_append_sheet(workbook, worksheet, 'Data');
  const buffer = write(workbook, { bookType: 'csv', type: 'array' });
  const blob = new Blob([buffer], { type: 'text/csv;charset=default' });
  saveAs(blob, `${fileName}.csv`);
};

export const DownloadExcel = (
  data: Array<Array<number | string | moment.Moment>>,
  fileName: string
) => {
  const worksheet = utils.json_to_sheet(data);
  const workbook = utils.book_new();
  utils.book_append_sheet(workbook, worksheet, 'Data');
  const buffer = write(workbook, { bookType: 'xlsx', type: 'array' });
  const blob = new Blob([buffer], { type: 'application/octet-stream' });
  saveAs(blob, `${fileName}.xlsx`);
};
