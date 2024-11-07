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
