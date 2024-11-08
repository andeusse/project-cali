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
