export const array2CSV = (
  columns: Array<Array<number | string>>,
  headers: Array<string>
): string => {
  const headerCSV = headers.join(',');
  let csvString = headerCSV + '\n';
  for (let i = 0; i < columns[0].length; i++) {
    let newLine = '';
    for (let j = 0; j < columns.length; j++) {
      newLine = newLine + columns[j][i];
      newLine = j !== columns.length - 1 ? newLine + ',' : newLine + '\n';
    }
    csvString = csvString + newLine;
  }
  return csvString;
};

export const array2Array = (
  columns: Array<Array<number | string>>
): Array<Array<number | string>> => {
  let rows = [];
  for (let i = 0; i < columns[0].length; i++) {
    let row = [];
    for (let j = 0; j < columns.length; j++) {
      row.push(columns[j][i]);
    }
    rows.push(row);
  }
  return rows;
};
