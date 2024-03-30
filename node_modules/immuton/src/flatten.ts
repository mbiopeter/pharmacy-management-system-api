import empty from './empty.js';

/**
 * Flattens an array of arrays to a flat array with the items from
 * the nested arrays. This only performs a shallow flatten.
 * If only one of the included arrays is non-empty, then returns
 * a reference to that array.
 * @param arrays An array of arrays
 */
function flatten<T>(arrays: T[][]): T[] {
  const { length } = arrays;
  if (!length) {
    return arrays as unknown as T[];
  }
  let result: T[] | undefined;
  for (let i = 0; i < length; i += 1) {
    const array = arrays[i];
    if (array.length) {
      if (result != null) {
        // More than one non-empty array.
        // Fall back to native flatten.
        return (empty as T[]).concat(...arrays);
      }
      // First non-empty array
      result = array;
    }
  }
  return result || empty;
}

export default flatten;
