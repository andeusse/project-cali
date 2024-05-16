import { CellChange } from '@silevis/reactgrid';

export const CellChange2Array = (
  e: CellChange[],
  array: Array<Array<number>>
) => {
  e.forEach((change) => {
    if ('value' in change.newCell) {
      array[change.rowId.valueOf() as number][
        change.columnId.valueOf() as number
      ] = change.newCell.value;
    }
  });
  return array;
};
