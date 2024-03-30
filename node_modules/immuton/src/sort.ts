import compare from './compare.js';
import empty from './empty.js';
import isEqual from './isEqual.js';

interface SortableItem {
  value: unknown;
  sorter: unknown;
  index: number;
}

const buffers: SortableItem[][] = [];

/**
 * Sorts the given array of values by using the sorting value returned by the given
 * function for each item in the array, and using the given direction.
 * Optionally also filters only values whose
 * attribute values are "before" or "after" of the given 'since' value
 * depending on the direction.
 */
export default function sort<T, V>(
  values: T[],
  iterator: (item: T, index: number) => V,
  // eslint-disable-next-line default-param-last
  direction: 'asc' | 'desc' = 'asc',
  since?: V,
): T[] {
  // Re-use the first available buffer, or create a new one
  const buffer = buffers.pop() || [];
  // NOTE: As JavaScript sort is not stable, make it stable by including the index with each item
  buffer.length = values.length;
  let altered = false;
  let bufferIndex = 0;
  values.forEach((value, index) => {
    const sorter = iterator(value, index);
    if (since != null) {
      if (direction === 'desc' && sorter >= since) {
        buffer.length -= 1;
        altered = true;
        return;
      }
      if (direction !== 'desc' && sorter <= since) {
        buffer.length -= 1;
        altered = true;
        return;
      }
    }
    const item = buffer[bufferIndex];
    if (item) {
      item.value = value;
      item.sorter = sorter;
      item.index = index;
    } else {
      buffer[bufferIndex] = { value, sorter, index };
    }
    bufferIndex += 1;
  });
  // Return the buffer to the cache
  buffers.push(buffer);
  if (values.length && !buffer.length) {
    // Filtered out everything
    return empty;
  }
  const comparator = (a: SortableItem, b: SortableItem) => compare(a.sorter, b.sorter, direction) || a.index - b.index;
  // Sort the items
  buffer.sort(comparator);
  // If already in order, return the value
  if (!altered && buffer.every((item, i) => isEqual(item.value, values[i]))) {
    return values;
  }
  // Return the sorted values
  return buffer.map((item) => item.value as T);
}
