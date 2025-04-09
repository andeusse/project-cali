import moment from 'moment';

export const array2Array = (
  columns: Array<Array<number | string | moment.Moment>>
): Array<Array<number | string | moment.Moment>> => {
  let rows = [];
  for (let i = 0; i < columns[0].length; i++) {
    let row = [];
    for (let j = 0; j < columns.length; j++) {
      var value = columns[j][i];
      if (moment.isMoment(value)) {
        row.push(value.toISOString());
        continue;
      }
      row.push(columns[j][i]);
    }
    rows.push(row);
  }
  return rows;
};
