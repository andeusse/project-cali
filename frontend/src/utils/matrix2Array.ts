import { Matrix } from 'react-spreadsheet';

export const matrix2Array = (
  e: Matrix<{
    value: number;
  }>,
  index: number
) => {
  return e[index].map((cell) => {
    if (cell && cell.value) {
      const value = parseFloat(cell.value.toString());
      if (!isNaN(value)) {
        return value;
      }
    }
    return 0;
  });
};
