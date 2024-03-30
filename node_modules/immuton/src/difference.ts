import filter from './filter.js';
import includes from './includes.js';

/**
 * Returns those items from the first given array that has no equal values
 * in the second array. The returned array may contain duplicates if the
 * original array also contains duplicates. If no values are filtered out,
 * then returns the original reference.
 */

function difference<A, B>(a: A[], b: B[]): Array<Exclude<A, B>>;
function difference<T>(a: T[], b: T[]): T[] {
  return filter(a, (value) => !includes(b, value));
}

export default difference;
