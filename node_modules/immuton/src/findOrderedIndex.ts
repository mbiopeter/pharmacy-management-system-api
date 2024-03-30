import compare from './compare.js';

/**
 * Returns the last index to insert the given value to an already sorted array,
 * so that once indexed to that position, the array will still be sorted.
 */
export default function findOrderedIndex<T>(values: T[], value: T, ordering: keyof T, direction: 'asc' | 'desc') {
  let index = 0;
  while (index < values.length && compare(value[ordering], values[index][ordering], direction) >= 0) {
    index += 1;
  }
  return index;
}
