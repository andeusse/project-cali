export const array2CSV = (
  arrays: Array<Array<number | string>>,
  headers: Array<string>
): string => {
  const headerCSV = headers.join(',');
  let csvString = headerCSV + '\n';
  for (let i = 0; i < arrays[0].length; i++) {
    let newLine = '';
    for (let j = 0; j < arrays.length; j++) {
      newLine = newLine + arrays[j][i];
      newLine = j !== arrays.length - 1 ? newLine + ',' : newLine + '\n';
    }
    csvString = csvString + newLine;
  }
  return csvString;
};
